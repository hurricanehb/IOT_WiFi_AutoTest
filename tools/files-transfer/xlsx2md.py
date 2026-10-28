import argparse
import re
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent

HEADER_MARKERS = frozenset(
    {
        "层级",
        "用例层级",
        "目录名称",
        "用例标题",
        "测试点",
        "摘要",
        "优先级",
        "预置条件",
        "前置条件",
        "操作步骤",
        "测试步骤",
        "预期结果",
    }
)

COLUMN_ALIASES = {
    "层级": "层级",
    "用例层级": "层级",
    "目录名称": "目录名称",
    "用例标题": "用例标题",
    "测试点": "用例标题",
    "优先级": "优先级",
    "预置条件": "前置条件",
    "前置条件": "前置条件",
    "操作步骤": "操作步骤",
    "测试步骤": "操作步骤",
    "预期结果": "预期结果",
    "预 期结果": "预期结果",
    "摘要": "摘要",
    "类型": "类型",
    "类型（自动化/手工）": "类型",
    "标签": "标签",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将测试用例 Excel 转换为 Markdown 文件")
    parser.add_argument(
        "-i",
        "--input",
        default="testcases.xlsx",
        help="Excel 输入文件路径（默认：脚本同目录下的 testcases.xlsx）",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="testcases.md",
        help="Markdown 输出文件路径（单 sheet 模式，默认：testcases.md）",
    )
    parser.add_argument(
        "-s",
        "--sheet",
        default=None,
        help="指定 sheet 名称（默认：第一个 sheet）",
    )
    parser.add_argument(
        "--all-sheets",
        action="store_true",
        help="为 Excel 中每个 sheet 分别生成 Markdown 文件",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="多 sheet 模式下的输出目录（默认：与 Excel 同名的子目录）",
    )
    return parser.parse_args()


def resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    return (SCRIPT_DIR / path).resolve()


def detect_header_row(raw_df: pd.DataFrame) -> int:
    for idx, row in raw_df.iterrows():
        cells = {str(v).strip() for v in row if pd.notna(v) and str(v).strip()}
        if len(cells & HEADER_MARKERS) >= 3:
            return int(idx)
    return 0


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        key = str(col).strip()
        if key in COLUMN_ALIASES:
            rename_map[col] = COLUMN_ALIASES[key]
    return df.rename(columns=rename_map)


def read_sheet_dataframe(excel_path: Path, sheet_name: str) -> pd.DataFrame:
    raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    header_row = detect_header_row(raw)
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=header_row)
    df = normalize_columns(df)
    df = df.fillna("")
    return df.ffill()


def pick_col(dataframe: pd.DataFrame, *candidates: str) -> str:
    for col in candidates:
        if col in dataframe.columns:
            return col
    return candidates[0]


def strip_trailing_whitespace(content: str) -> str:
    """Remove trailing whitespace from every physical Markdown line."""
    return "\n".join(line.rstrip() for line in content.splitlines())


def dataframe_to_md(df: pd.DataFrame) -> str:
    title_col = pick_col(df, "用例标题", "测试点")
    pre_col = pick_col(df, "前置条件", "预置条件")
    exp_col = pick_col(df, "预期结果", "预 期结果")

    if title_col not in df.columns:
        raise ValueError(f"Excel 中未找到用例标题列，当前列：{list(df.columns)}")

    level_series = pd.to_numeric(df.get("层级"), errors="coerce")
    title_mask = df[title_col].astype(str).str.strip().ne("")
    valid_levels = level_series[title_mask & level_series.notna()]
    if valid_levels.empty:
        raise ValueError("Excel 中未找到可输出的用例标题行，请检查'用例标题'列内容。")

    level4_has_title = bool(((level_series == 4) & title_mask).any())
    min_title_level = int(valid_levels.min())
    output_min_level = 4 if level4_has_title else min_title_level

    current_levels: dict[int, str] = {}
    md_lines: list[str] = []
    last_titles = {"L1": "", "L2": "", "L3": ""}

    for _, row in df.iterrows():
        level = int(row.get("层级", 0) or 0)
        dirname = str(row.get("目录名称", "")).strip()
        title = str(row.get(title_col, "")).strip()

        if dirname:
            current_levels[level] = dirname

        if level >= output_min_level and title:
            l1 = current_levels.get(1, "")
            l2 = current_levels.get(2, "")
            l3 = current_levels.get(3, "")

            if l1 != last_titles["L1"]:
                md_lines.append(f"# {l1}")
                last_titles["L1"] = l1
                last_titles["L2"] = ""
                last_titles["L3"] = ""
            if l2 != last_titles["L2"]:
                md_lines.append(f"## {l2}")
                last_titles["L2"] = l2
                last_titles["L3"] = ""
            if l3 != last_titles["L3"]:
                md_lines.append(f"### {l3}")
                last_titles["L3"] = l3

            md_lines.append(f"#### {title}")

            priority = str(row.get("优先级", "")).strip()
            summary = str(row.get("摘要", "")).strip()
            type_ = str(row.get("类型", "")).strip()
            tag = str(row.get("标签", "")).strip()
            pre = str(row.get(pre_col, "")).strip()
            step = str(row.get("操作步骤", "")).strip()
            exp = str(row.get(exp_col, "")).strip()

            md_lines.append(f"**属性：** 优先级：{priority}；摘要：{summary}；类型：{type_}；标签：{tag}\n")
            md_lines.append("**前置条件：**")
            md_lines.append(pre if pre else "无")
            md_lines.append("")
            md_lines.append("**操作步骤：**")
            md_lines.append(step if step else "无")
            md_lines.append("")
            md_lines.append("**预期结果：**")
            md_lines.append(exp if exp else "无")
            md_lines.append("\n---\n")

    content = "\n".join(line for line in md_lines if line.strip())
    return strip_trailing_whitespace(content)


def safe_sheet_filename(sheet_name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", sheet_name).strip()
    return name or "sheet"


def convert_sheet(excel_path: Path, sheet_name: str, output_file: Path) -> int:
    df = read_sheet_dataframe(excel_path, sheet_name)
    content = dataframe_to_md(df)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")
    case_count = content.count("\n#### ")
    return case_count


def main() -> None:
    args = parse_args()
    excel_path = resolve_path(args.input)

    if not excel_path.exists():
        raise FileNotFoundError(
            f"未找到 Excel 文件：{excel_path}\n"
            f"请检查路径，或使用参数指定，例如：\n"
            f"python {Path(__file__).name} -i testcases_perf.xlsx -o testcases_perf.md"
        )

    if args.all_sheets:
        output_dir = resolve_path(args.output_dir) if args.output_dir else excel_path.with_suffix("").parent / excel_path.stem
        xl = pd.ExcelFile(excel_path)
        total_cases = 0
        written: list[tuple[str, Path, int]] = []

        for sheet_name in xl.sheet_names:
            output_file = output_dir / f"{safe_sheet_filename(sheet_name)}.md"
            try:
                case_count = convert_sheet(excel_path, sheet_name, output_file)
                total_cases += case_count
                written.append((sheet_name, output_file, case_count))
                print(f"✅ [{sheet_name}] -> {output_file.name} ({case_count} 条用例)")
            except ValueError as exc:
                print(f"⚠️  [{sheet_name}] 跳过：{exc}")

        print(f"\n共生成 {len(written)} 个 Markdown 文件，合计 {total_cases} 条用例。")
        print(f"输出目录：{output_dir.resolve()}")
        return

    sheet_name = args.sheet
    output_file = resolve_path(args.output)
    if sheet_name is None:
        sheet_name = pd.ExcelFile(excel_path).sheet_names[0]

    case_count = convert_sheet(excel_path, sheet_name, output_file)
    print(f"✅ 已生成 {output_file.resolve()}（{case_count} 条用例）。不包含 TOC，仅包含分级测试用例结构。")


if __name__ == "__main__":
    main()
