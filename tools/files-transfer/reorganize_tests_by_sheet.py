#!/usr/bin/env python3
"""按 Excel sheet 模块将 wifi_connection 下用例迁移到 testcases/android 子目录。"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from testcase_parser import parse_testcase_blocks
from wifi_sheet_dirs import (
    ANDROID_CASES,
    LEGACY_FILE_DIRS,
    MD_DIR,
    ensure_sheet_dirs,
    sheet_output_dir,
)

SRC = ANDROID_CASES / "wifi_connection"
CASE_ID_RE = re.compile(r'@pytest\.mark\.case_id\("([^"]+)"\)')


def build_summary_to_sheet() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for md in sorted(MD_DIR.glob("*.md")):
        for case in parse_testcase_blocks(md):
            mapping[case["case_id"]] = md.stem
    return mapping


def resolve_target_sheet(filename: str, summaries: set[str], summary_to_sheet: dict[str, str]) -> str | None:
    if filename in LEGACY_FILE_DIRS:
        return None

    sheets = {summary_to_sheet[s] for s in summaries if s in summary_to_sheet}
    sheets.discard("")
    if not sheets:
        return None
    if len(sheets) == 1:
        return next(iter(sheets))
    raise ValueError(f"{filename} 跨多个 sheet：{sorted(sheets)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按 Excel sheet 模块整理 WiFi 测试文件")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印计划，不创建目录或移动文件",
    )
    return parser.parse_args()


def reorganize(*, dry_run: bool = False) -> int:
    if not SRC.exists():
        if dry_run:
            print(f"源目录不存在，无待迁移文件：{SRC}")
            return 0
        print(f"源目录不存在：{SRC}")
        return 1

    if not dry_run:
        ensure_sheet_dirs()
    summary_to_sheet = build_summary_to_sheet()
    moved: list[tuple[Path, Path]] = []
    skipped: list[str] = []

    for src_file in sorted(SRC.glob("test_*.py")):
        if src_file.name in LEGACY_FILE_DIRS:
            dest_dir = ANDROID_CASES / LEGACY_FILE_DIRS[src_file.name]
            dest = dest_dir / src_file.name
            if dest.exists() and dest.read_bytes() != src_file.read_bytes():
                raise FileExistsError(f"目标已存在且内容不同：{dest}")
            if not dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_file), str(dest))
            moved.append((src_file, dest))
            continue

        summaries = set(CASE_ID_RE.findall(src_file.read_text(encoding="utf-8")))
        try:
            sheet = resolve_target_sheet(src_file.name, summaries, summary_to_sheet)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        if sheet is None:
            skipped.append(src_file.name)
            continue

        dest_dir = sheet_output_dir(sheet)
        dest = dest_dir / src_file.name
        if dest.exists() and dest.read_bytes() != src_file.read_bytes():
            raise FileExistsError(f"目标已存在且内容不同：{dest}")
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_file), str(dest))
        moved.append((src_file, dest))

    by_dir: dict[str, list[str]] = defaultdict(list)
    for _, dest in moved:
        by_dir[dest.parent.name].append(dest.name)

    action = "计划迁移" if dry_run else "已迁移"
    print(f"{action} {len(moved)} 个文件：")
    for folder, files in sorted(by_dir.items()):
        print(f"  {folder}/ ({len(files)})")

    if dry_run:
        if skipped:
            print(f"\n未映射（将保留在 wifi_connection/）：{skipped}")
        print("\n预览完成，未创建目录或移动文件。")
        return 0

    remaining = list(SRC.glob("test_*.py"))
    if remaining:
        print(f"\n保留在 wifi_connection/ 的文件 ({len(remaining)}):")
        for path in remaining:
            print(f"  {path.name}")
    elif SRC.exists() and not any(SRC.iterdir()):
        SRC.rmdir()
        print("\nwifi_connection/ 已为空，目录已删除。")
    elif SRC.exists():
        print(f"\nwifi_connection/ 仍含非 test_*.py 文件，目录保留。")

    if skipped:
        print(f"\n未映射（仍留在 wifi_connection/）：{skipped}")
    return 0


def main() -> int:
    args = parse_args()
    return reorganize(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
