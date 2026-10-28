"""解析带 ### 子模块上下文的用例块。"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from testcase_parser import parse_testcase_blocks


def _subsections_by_title(doc_path: Path) -> Dict[str, List[str]]:
    mapping: Dict[str, List[str]] = {}
    subsection = ""
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            subsection = line[4:].strip()
        elif line.startswith("#### "):
            mapping.setdefault(line[5:].strip(), []).append(subsection)
    return mapping


def parse_cases_by_subsection(doc_path: Path) -> Dict[str, List[dict]]:
    subsections_by_title = _subsections_by_title(doc_path)
    title_counts: Dict[str, int] = {}
    grouped: Dict[str, List[dict]] = {}
    for case in parse_testcase_blocks(doc_path):
        title = case["title"]
        occurrence = title_counts.get(title, 0)
        subsections = subsections_by_title.get(title, [])
        subsection = subsections[occurrence] if occurrence < len(subsections) else ""
        title_counts[title] = occurrence + 1
        case["subsection"] = subsection
        grouped.setdefault(subsection or "default", []).append(case)
    return grouped
