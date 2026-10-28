#!/usr/bin/env python3
"""一次性脚本：从 Markdown 用例文档写出静态 pytest 文件（运行期不读 md）。"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[2]

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from component_case_parser import parse_cases_by_subsection
from testcase_parser import is_automation_case, is_stress_summary, normalized_product_tag, parse_testcase_blocks
from wifi_sheet_dirs import (
    ANDROID_CASES,
    COMPONENT_SUBSECTION_DIRS,
    component_subsection_dir,
    ensure_sheet_dirs,
    sheet_output_dir,
)

DEFAULT_DOC = ROOT / "tools" / "files-transfer" / "testcases.md"

CHANNEL_GROUP = "Func_WlanAccess_Conn_Channel"
AP_GROUP = "Func_WlanAccess_Conn_AP"
NRC_MINIAP_CASE = "Func_WlanAccess_Conn_AP_Comp_005"

CHANNEL_PLANS: Dict[str, Dict[str, Any]] = {
    "Func_WlanAccess_Conn_Channel_Vali_001": {
        "driver": "miniAP",
        "country": "US",
        "wifi_entry_id": "hyperwifi_us",
        "bandwidths": [
            {"mhz": 1, "channels": {"start": 3, "end": 49, "step": 2}},
            {"mhz": 2, "channels": {"start": 6, "end": 46, "step": 4}},
            {"mhz": 4, "channels": {"start": 8, "end": 40, "step": 8}},
        ],
    },
    "Func_WlanAccess_Conn_Channel_Vali_002": {
        "driver": "miniAP",
        "country": "EU",
        "band": "800MHz",
        "wifi_entry_id": "hyperwifi_eu",
        "bandwidths": [{"mhz": 1, "channels": [1, 3, 5, 7, 9]}],
    },
    "Func_WlanAccess_Conn_Channel_Vali_003": {
        "driver": "miniAP",
        "country": "EU",
        "band": "900MHz",
        "wifi_entry_id": "hyperwifi_eu",
        "bandwidths": [{"mhz": 1, "channels": [31, 33, 35]}],
    },
    "Func_WlanAccess_Conn_Channel_Vali_004": {
        "driver": "ap",
        "country": "JP",
        "wifi_entry_id": "wifi_ap_ssid_default",
        "bandwidth_mhz": 20,
        "channels": {"start": 1, "end": 13},
    },
    "Func_WlanAccess_Conn_Channel_Vali_005": {
        "driver": "ap",
        "country": "US",
        "wifi_entry_id": "wifi_ap_ssid_default",
        "bandwidth_mhz": 20,
        "channels": [
            {"start": 36, "end": 48, "step": 4},
            {"start": 52, "end": 64, "step": 4},
            {"start": 100, "end": 144, "step": 4},
            {"start": 149, "end": 165, "step": 4},
        ],
    },
    "Func_WlanAccess_Conn_Channel_Vali_006": {
        "driver": "ap",
        "bandwidth_mhz": 20,
        "channels": {"start": 132, "end": 220, "step": 4},
    },
}

CASE_TYPE_SUFFIX = frozenset(
    {"Vali", "Excp", "UI", "Stb", "Int", "Comp", "Stress", "Weaknet", "Func", "EAP", "AP"}
)

LEGACY_MODULE_GLOBS = (
    "test_wifi_conn_*.py",
    "test_wifi_network_*.py",
    "test_wifi_pribaklink_*.py",
    "test_wifi_reconnect_*.py",
    "test_func_wlanaccess_*.py",
)


def group_key(summary: str) -> str:
    parts = summary.split("_")
    if len(parts) >= 6 and parts[2] == "Reconnect" and parts[3] == "StaChange" and parts[4] == "User":
        return "_".join(parts[:5])
    for i in range(len(parts) - 1, 0, -1):
        if parts[i] in CASE_TYPE_SUFFIX:
            return "_".join(parts[:i])
    return "_".join(parts[:-1])


def module_name(group: str, *, sheet_dir: str) -> str:
    slug = group.lower()
    if sheet_dir.startswith("wlan_components_"):
        return f"test_{slug}.py"
    return f"test_{sheet_dir}_{slug}.py"


def _priority(p: str) -> str:
    x = (p or "p2").strip().lower()
    return x if x in {"p0", "p1", "p2", "p3"} else "p2"


def _render_markers(case: Dict[str, str], *, component_case: bool = False) -> str:
    product = normalized_product_tag(case)
    lines = [
        f"@pytest.mark.{_priority(case['priority'])}",
        f"@pytest.mark.{product}",
    ]
    if not component_case:
        lines.extend(("@pytest.mark.wlan", "@pytest.mark.wlan_connection"))
    if is_stress_summary(case["case_id"]):
        lines.append("@pytest.mark.stress")
    if "_Weaknet_" in case["case_id"]:
        lines.append("@pytest.mark.weaknet")
    lines.append(f'@pytest.mark.case_id("{case["case_id"]}")')
    return "\n".join(lines)


def _render_test(
    case: Dict[str, str], func_name: str, *, automated: bool, component_case: bool = False
) -> str:
    summary = case["case_id"]
    pre = case.get("pre") or "设备 ADB 在线"
    title = case["title"]
    markers = _render_markers(case, component_case=component_case)

    if summary == NRC_MINIAP_CASE:
        func_params = "run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case"
        status_step = ""
        step2 = (
            "run_nrc_miniap_compatibility_case(\n"
            "        case, run_shell_cmd, wifi, wifi_yaml, miniap_action_optional,\n"
            "    )"
        )
    elif automated:
        plan = CHANNEL_PLANS.get(summary)
        if plan is None:
            raise ValueError(f"缺少信道用例 plan：{summary}")
        func_params = "run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case"
        status_step = ""
        step2 = (
            "run_channel_automation_case(\n"
            "        case, run_shell_cmd, wifi, wifi_yaml,\n"
            f"        plan={plan!r},\n"
            "        miniap_action=miniap_action_optional,\n"
            "    )"
        )
    else:
        func_params = "run_shell_cmd, wifi, wifi_yaml, wifi_case"
        status_step = ""
        step2 = "run_manual_placeholder(case, run_shell_cmd)"

    return f"""
{markers}
@pytest.mark.wifi_case(
    title={json.dumps(title, ensure_ascii=False)},
    pre={json.dumps(pre, ensure_ascii=False)},
)
def {func_name}({func_params}):
{status_step}    # 执行对应用例逻辑
    {step2.replace('case,', 'wifi_case,')}
"""


def _file_header(group: str, automated: bool, *, source_docs: Iterable[Path]) -> str:
    rel = ", ".join(doc.relative_to(ROOT).as_posix() for doc in source_docs)
    kind = "信道遍历等可 ADB 半自动" if automated else "手工/实验室场景"
    if automated:
        imports = "from core.libs.android.wifi_scenarios.channel_plan import run_channel_automation_case"
    elif group == AP_GROUP:
        imports = (
            "from core.libs.android.wifi_scenarios.ssidpwd_connection import "
            "run_nrc_miniap_compatibility_case\n"
            "from testcases.support.case_api import run_manual_placeholder"
        )
    else:
        imports = "from testcases.support.case_api import run_manual_placeholder"
    return f'''"""WiFi 连接 — {group}（{kind}）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：{rel}
"""
from __future__ import annotations

import pytest

{imports}
'''


def _resolve_func_name(case: Dict[str, str], used: Dict[str, int]) -> str:
    summary = case["case_id"]
    if summary not in used:
        used[summary] = 0
        return f"test_{summary}"
    used[summary] += 1
    slug = re.sub(r"[^\w]+", "_", case["title"]).strip("_")[:20]
    return f"test_{summary}_{slug}"


def _remove_legacy_modules(base_dir: Path) -> List[Path]:
    removed: List[Path] = []
    for pattern in LEGACY_MODULE_GLOBS:
        for path in base_dir.glob(pattern):
            path.unlink()
            removed.append(path)
    return removed


def _remove_component_modules() -> List[Path]:
    removed: List[Path] = []
    for directory in COMPONENT_SUBSECTION_DIRS.values():
        for path in (ANDROID_CASES / directory).glob("test_func_components_*.py"):
            path.unlink()
            removed.append(path)
    return removed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从 Markdown 用例文档生成 WiFi 连接 pytest 脚本")
    parser.add_argument(
        "-i",
        "--input",
        action="append",
        default=None,
        help="Markdown 输入文件，可重复指定；也可传入目录（读取其中全部 .md）",
    )
    return parser.parse_args()


def resolve_doc_paths(inputs: List[str] | None) -> List[Path]:
    if not inputs:
        return [DEFAULT_DOC]

    docs: List[Path] = []
    for raw in inputs:
        path = Path(raw)
        if not path.is_absolute():
            path = (SCRIPT_DIR / path).resolve()
        if path.is_dir():
            docs.extend(sorted(path.glob("*.md")))
        else:
            docs.append(path)
    return docs


def main() -> int:
    args = parse_args()
    docs = resolve_doc_paths(args.input)
    missing = [doc for doc in docs if not doc.exists()]
    if missing:
        for doc in missing:
            print(f"ERROR: doc not found: {doc}", file=sys.stderr)
        return 1

    sheet_cases: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    component_cases: Dict[str, Dict[str, List[Dict[str, str]]]] = {}
    sheet_docs: Dict[str, Path] = {}
    for doc in docs:
        sheet = doc.stem
        if sheet == "组件":
            grouped = parse_cases_by_subsection(doc)
            component_cases[sheet] = grouped
            count = sum(len(items) for items in grouped.values())
            print(f"Parsed {count} cases from {doc.relative_to(ROOT)} ({len(grouped)} subsections)")
            sheet_docs[sheet] = doc
            continue

        parsed = parse_testcase_blocks(doc)
        print(f"Parsed {len(parsed)} cases from {doc.relative_to(ROOT)}")
        sheet_docs[sheet] = doc
        for case in parsed:
            sheet_cases[sheet].append(case)

    if not any(sheet_cases.values()) and not component_cases:
        print("ERROR: no cases parsed", file=sys.stderr)
        return 1

    ensure_sheet_dirs()
    removed: List[Path] = []
    written: List[Path] = []
    total_cases = 0

    for sheet, cases in sorted(sheet_cases.items()):
        if not cases:
            continue
        out_dir = sheet_output_dir(sheet)
        out_dir.mkdir(parents=True, exist_ok=True)
        removed.extend(_remove_legacy_modules(out_dir))

        groups: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for case in cases:
            groups[group_key(case["case_id"])].append(case)

        for group, items in sorted(groups.items()):
            automated = group == CHANNEL_GROUP and all(is_automation_case(c) for c in items)
            used: Dict[str, int] = {}
            body = "".join(_render_test(c, _resolve_func_name(c, used), automated=automated) for c in items)
            path = out_dir / module_name(group, sheet_dir=out_dir.name)
            content = _file_header(
                group, automated, source_docs=[sheet_docs[sheet]]
            ) + body
            path.write_text(
                content.rstrip() + "\n",
                encoding="utf-8",
            )
            written.append(path)
            total_cases += len(items)

    for sheet, subsections in sorted(component_cases.items()):
        removed.extend(_remove_component_modules())
        for subsection, cases in sorted(subsections.items()):
            if not cases:
                continue
            out_dir = component_subsection_dir(subsection)
            out_dir.mkdir(parents=True, exist_ok=True)
            removed.extend(_remove_legacy_modules(out_dir))

            groups: Dict[str, List[Dict[str, str]]] = defaultdict(list)
            for case in cases:
                groups[group_key(case["case_id"])].append(case)

            for group, items in sorted(groups.items()):
                automated = group == CHANNEL_GROUP and all(is_automation_case(c) for c in items)
                used: Dict[str, int] = {}
                body = "".join(
                    _render_test(c, _resolve_func_name(c, used), automated=automated, component_case=True)
                    for c in items
                )
                path = out_dir / module_name(group, sheet_dir=out_dir.name)
                content = _file_header(
                    group, automated, source_docs=[sheet_docs[sheet]]
                ) + body
                path.write_text(
                    content.rstrip() + "\n",
                    encoding="utf-8",
                )
                written.append(path)
                total_cases += len(items)

    print(f"Parsed {total_cases} cases -> {len(written)} modules under {ANDROID_CASES.relative_to(ROOT)}")
    if removed:
        print(f"Removed {len(removed)} legacy module(s)")
    for p in sorted(written):
        n = p.read_text(encoding="utf-8").count("\ndef test_")
        print(f"  {p.name}: {n} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
