"""按独立 case_id 统计 testcases/ 各模块自动化率。

用法：
    python tools/automation_coverage.py              # 汇总表
    python tools/automation_coverage.py --detail     # 含每个文件明细
    python tools/automation_coverage.py --sort asc   # 按自动化率升序（优先排期）
    python tools/automation_coverage.py --weekly     # 上一个完整自然周的模块分布与新增数

计数规则：
    - pytest 收集出的每个独立 case_id 计为一条用例
    - 参数化用例中不同的 case_id 分别计数
    - 重复 case_id 全局只计一次

状态判定规则（不执行用例）：
    - placeholder：函数体内调用 run_manual_placeholder
    - not_applicable：函数体内调用 run_not_applicable
    - skip：函数体内出现 pytest.skip（且非 placeholder/not_applicable）
    - implemented：其余 test_ 函数
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TESTCASES = ROOT / "testcases"


@dataclass
class FileStat:
    implemented: list[str] = field(default_factory=list)
    placeholder: list[str] = field(default_factory=list)
    not_applicable: list[str] = field(default_factory=list)
    skip: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return (
            len(self.implemented)
            + len(self.placeholder)
            + len(self.not_applicable)
            + len(self.skip)
        )


@dataclass(frozen=True)
class CollectedCase:
    path: Path
    function_name: str
    case_id: str
    markers: frozenset[str]


class CaseIdCollector:
    def __init__(self) -> None:
        self.cases: list[CollectedCase] = []

    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        for item in items:
            markers = [
                marker
                for marker in item.iter_markers("case_id")
                if marker.args and isinstance(marker.args[0], str)
            ]
            if not markers:
                continue
            marker = markers[-1]
            self.cases.append(
                CollectedCase(
                    path=Path(str(item.path)).resolve(),
                    function_name=getattr(item, "originalname", None)
                    or item.name.split("[", 1)[0],
                    case_id=marker.args[0],
                    markers=frozenset(mark.name for mark in item.iter_markers()),
                )
            )


def _calls_name(node: ast.expr, name: str) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == name
    )


def _is_pytest_skip(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "skip"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "pytest"
    )


def classify_function(func: ast.FunctionDef) -> str:
    """implemented | placeholder | not_applicable | skip。"""
    has_placeholder = False
    has_not_applicable = False
    has_skip = False
    for node in ast.walk(func):
        if isinstance(node, ast.Call):
            if _calls_name(node, "run_manual_placeholder"):
                has_placeholder = True
            elif _calls_name(node, "run_not_applicable"):
                has_not_applicable = True
            elif _is_pytest_skip(node):
                has_skip = True
    if has_placeholder:
        return "placeholder"
    if has_not_applicable:
        return "not_applicable"
    if has_skip:
        return "skip"
    return "implemented"


def _parameter_status(param: ast.Call) -> str:
    for keyword in param.keywords:
        if keyword.arg == "status" and isinstance(keyword.value, ast.Constant):
            if keyword.value.value == "manual":
                return "placeholder"
            if keyword.value.value == "not_applicable":
                return "not_applicable"
            if keyword.value.value == "skip":
                return "skip"
    return "implemented"


def parameterized_cases(func: ast.FunctionDef) -> list[tuple[str, str]]:
    """Return declarative case rows from the local ``_case_param`` convention."""
    for decorator in func.decorator_list:
        if not (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Attribute)
            and decorator.func.attr == "parametrize"
            and len(decorator.args) >= 2
            and isinstance(decorator.args[1], (ast.Tuple, ast.List))
        ):
            continue
        rows = []
        for param in decorator.args[1].elts:
            if not (
                isinstance(param, ast.Call)
                and isinstance(param.func, ast.Name)
                and param.func.id == "_case_param"
                and param.args
                and isinstance(param.args[0], ast.Constant)
                and isinstance(param.args[0].value, str)
            ):
                return []
            rows.append((param.args[0].value, _parameter_status(param)))
        return rows
    return []


def analyze_file(path: Path) -> FileStat:
    stat = FileStat()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            rows = parameterized_cases(node)
            if rows:
                for case_id, kind in rows:
                    getattr(stat, kind).append(case_id)
                continue
            kind = classify_function(node)
            getattr(stat, kind).append(node.name)
    return stat


def function_statuses(path: Path) -> dict[str, tuple[str, dict[str, str]]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    statuses = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
            statuses[node.name] = (
                classify_function(node),
                dict(parameterized_cases(node)),
            )
    return statuses


def collect_cases(root: Path) -> tuple[list[CollectedCase], int]:
    collector = CaseIdCollector()
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        exit_code = pytest.main(
            [str(root), "--collect-only", "-q"],
            plugins=[collector],
        )
    if exit_code != pytest.ExitCode.OK:
        raise RuntimeError(
            f"pytest collection failed with exit code {int(exit_code)}\n{output.getvalue()}"
        )

    unique: dict[str, CollectedCase] = {}
    duplicates = 0
    for case in collector.cases:
        if case.case_id in unique:
            duplicates += 1
            continue
        unique[case.case_id] = case
    return list(unique.values()), duplicates


def collected_case_status(
    case: CollectedCase,
    statuses: dict[str, tuple[str, dict[str, str]]],
) -> str:
    function_status, parameter_statuses = statuses[case.function_name]
    if case.case_id in parameter_statuses:
        return parameter_statuses[case.case_id]
    if "manual_placeholder" in case.markers:
        return "placeholder"
    if "not_applicable" in case.markers:
        return "not_applicable"
    return function_status


def pct(part: int, total: int) -> str:
    return f"{part / total * 100:5.1f}%" if total else "  -  "


def coverage_summary(
    testcases: Path,
) -> tuple[dict[str, FileStat], dict[str, dict[str, FileStat]], int]:
    modules: dict[str, dict[str, FileStat]] = defaultdict(dict)
    cases, duplicate_count = collect_cases(testcases)
    status_cache: dict[Path, dict[str, tuple[str, dict[str, str]]]] = {}
    for case in cases:
        if "unit" in case.path.parts or "support" in case.path.parts:
            continue
        rel = case.path.relative_to(testcases.resolve())
        module = rel.parent.as_posix()
        stat = modules[module].setdefault(case.path.name, FileStat())
        statuses = status_cache.setdefault(case.path, function_statuses(case.path))
        getattr(stat, collected_case_status(case, statuses)).append(case.case_id)

    summaries: dict[str, FileStat] = {}
    for module, files in modules.items():
        aggregate = FileStat()
        for stat in files.values():
            aggregate.implemented += stat.implemented
            aggregate.placeholder += stat.placeholder
            aggregate.not_applicable += stat.not_applicable
            aggregate.skip += stat.skip
        summaries[module] = aggregate
    return summaries, modules, duplicate_count


def completed_week(today: date | None = None) -> tuple[date, date]:
    current = today or date.today()
    end = current - timedelta(days=current.weekday() + 1)
    return end - timedelta(days=6), end


def weekly_rows(
    before: dict[str, dict[str, int]],
    after: dict[str, dict[str, int]],
) -> list[tuple[str, dict[str, int], int, float]]:
    rows = []
    for module in sorted(set(before) | set(after)):
        current = after.get(module, {"total": 0, "implemented": 0})
        previous = before.get(module, {"total": 0, "implemented": 0})
        added = current["implemented"] - previous["implemented"]
        current_rate = current["implemented"] / current["total"] if current["total"] else 0.0
        previous_rate = (
            previous["implemented"] / previous["total"] if previous["total"] else 0.0
        )
        rows.append((module, current, added, (current_rate - previous_rate) * 100))
    return rows


def _summary_payload(summaries: dict[str, FileStat]) -> dict[str, dict[str, int]]:
    return {
        module: {
            "total": stat.total,
            "implemented": len(stat.implemented),
            "placeholder": len(stat.placeholder),
            "not_applicable": len(stat.not_applicable),
            "skip": len(stat.skip),
        }
        for module, stat in summaries.items()
    }


def _git_revision_before(moment: datetime) -> str:
    result = subprocess.run(
        ["git", "rev-list", "-1", f"--before={moment.isoformat(sep=' ')}", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    revision = result.stdout.strip()
    if not revision:
        raise RuntimeError(f"找不到 {moment:%Y-%m-%d %H:%M:%S} 之前的 Git 提交")
    return revision


def _snapshot_payload(revision: str, destination: Path) -> dict[str, dict[str, int]]:
    subprocess.run(
        ["git", "worktree", "add", "--detach", str(destination), revision],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--testcases-root",
                str(destination / "testcases"),
                "--json",
            ],
            cwd=destination,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(destination)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )


def print_weekly_report(week_start: date, week_end: date) -> None:
    start_revision = _git_revision_before(datetime.combine(week_start, datetime.min.time()))
    end_revision = _git_revision_before(
        datetime.combine(week_end + timedelta(days=1), datetime.min.time())
    )
    with tempfile.TemporaryDirectory(prefix="automation-coverage-") as temp_dir:
        temp = Path(temp_dir)
        before = _snapshot_payload(start_revision, temp / "before")
        after = _snapshot_payload(end_revision, temp / "after")

    rows = weekly_rows(before, after)
    print(f"统计周期：{week_start:%Y-%m-%d} 至 {week_end:%Y-%m-%d}")
    header = (
        f"{'模块':<44} {'总数':>4} {'已实现':>6} {'自动化率':>7} "
        f"{'新增自动化':>8} {'自动化率提升':>10}"
    )
    print(header)
    print("-" * len(header))
    for module, current, added, rate_change in rows:
        print(
            f"{module:<44} {current['total']:>4} {current['implemented']:>6} "
            f"{pct(current['implemented'], current['total']):>7} {added:>+8} "
            f"{rate_change:>+9.1f}pp"
        )
    total = sum(row[1]["total"] for row in rows)
    implemented = sum(row[1]["implemented"] for row in rows)
    added = sum(row[2] for row in rows)
    previous_total = sum(module["total"] for module in before.values())
    previous_implemented = sum(module["implemented"] for module in before.values())
    current_rate = implemented / total if total else 0.0
    previous_rate = previous_implemented / previous_total if previous_total else 0.0
    rate_change = (current_rate - previous_rate) * 100
    print("-" * len(header))
    print(
        f"{'TOTAL':<44} {total:>4} {implemented:>6} "
        f"{pct(implemented, total):>7} {added:>+8} {rate_change:>+9.1f}pp"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="testcases 自动化率统计")
    parser.add_argument("--detail", action="store_true", help="输出每个文件明细")
    parser.add_argument("--weekly", action="store_true", help="统计上一个完整自然周")
    parser.add_argument(
        "--week-ending",
        type=date.fromisoformat,
        help="指定周报结束日期（YYYY-MM-DD，需为周日）",
    )
    parser.add_argument("--json", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument(
        "--testcases-root",
        type=Path,
        default=TESTCASES,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--sort",
        choices=("asc", "desc", "name"),
        default="name",
        help="模块排序：asc=自动化率升序(优先排期) desc=降序 name=按名称",
    )
    args = parser.parse_args()

    if args.weekly or args.week_ending:
        if args.week_ending:
            if args.week_ending.weekday() != 6:
                parser.error("--week-ending 必须是周日")
            week_start, week_end = args.week_ending - timedelta(days=6), args.week_ending
        else:
            week_start, week_end = completed_week()
        print_weekly_report(week_start, week_end)
        return 0

    summaries, module_files, duplicate_count = coverage_summary(args.testcases_root)
    if args.json:
        print(json.dumps(_summary_payload(summaries), ensure_ascii=False))
        return 0

    rows = []
    totals = FileStat()
    for module, agg in summaries.items():
        totals.implemented += agg.implemented
        totals.placeholder += agg.placeholder
        totals.not_applicable += agg.not_applicable
        totals.skip += agg.skip
        rows.append((module, agg))

    def auto_rate(agg: FileStat) -> float:
        return len(agg.implemented) / agg.total if agg.total else 0.0

    if args.sort == "asc":
        rows.sort(key=lambda r: auto_rate(r[1]))
    elif args.sort == "desc":
        rows.sort(key=lambda r: -auto_rate(r[1]))

    header = f"{'模块':<44} {'总数':>4} {'已实现':>6} {'占位':>4} {'不适用':>6} {'跳过':>4} {'自动化率':>7}"
    print(header)
    print("-" * len(header))
    for module, agg in rows:
        print(
            f"{module:<44} {agg.total:>4} {len(agg.implemented):>6} "
            f"{len(agg.placeholder):>4} {len(agg.not_applicable):>6} {len(agg.skip):>4} "
            f"{pct(len(agg.implemented), agg.total):>7}"
        )
        if args.detail:
            for fname, stat in module_files[module].items():
                if stat.placeholder:
                    print(f"    {fname}: placeholder={len(stat.placeholder)}")
    print("-" * len(header))
    print(
        f"{'TOTAL':<44} {totals.total:>4} {len(totals.implemented):>6} "
        f"{len(totals.placeholder):>4} {len(totals.not_applicable):>6} {len(totals.skip):>4} "
        f"{pct(len(totals.implemented), totals.total):>7}"
    )
    if duplicate_count:
        print(f"警告：发现 {duplicate_count} 个重复 case_id，已按 ID 去重。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
