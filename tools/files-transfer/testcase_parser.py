"""Standalone Markdown testcase parsing helpers for file-transfer tools."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


def parse_testcase_blocks(doc_path: Path) -> List[Dict[str, str]]:
    """Parse Markdown ``####`` testcase blocks into metadata dictionaries."""
    text = doc_path.read_text(encoding="utf-8")
    blocks = text.split("#### ")[1:]
    cases: List[Dict[str, str]] = []

    for block in blocks:
        lines = block.splitlines()
        title = (lines[0] if lines else "").strip()
        body = "\n".join(lines)
        attr = re.search(
            r"\*\*属性：\*\*\s*优先级：([^；\n]*)；摘要：([^；\n]*)；类型：([^；\n]*)；标签：([^\n]*)",
            body,
        )
        if not attr:
            continue

        pre = ""
        pre_match = re.search(r"\*\*前置条件：\*\*\s*\n(.*?)\n\*\*操作步骤：\*\*", body, re.S)
        if pre_match:
            pre = " ".join(line.strip() for line in pre_match.group(1).splitlines() if line.strip())

        priority, case_id, case_type, tag = (value.strip() for value in attr.groups())
        if not case_id or case_id == "/":
            continue
        cases.append(
            {
                "title": title,
                "priority": priority,
                "case_type": case_type,
                "tag": tag,
                "pre": pre,
                "case_id": case_id,
            }
        )
    return cases


def normalized_product_tag(case: Dict[str, str]) -> str:
    """Return the registered pytest product marker for a testcase."""
    title = (case.get("title") or "").lower()
    case_id = (case.get("case_id") or "").lower()
    raw = (case.get("tag") or "").lower()
    if "hyperwifi" in raw or "hyperwifi" in title or "hyperwifi" in case_id:
        return "hyperwifi"
    if raw == "common" or "common" in raw:
        return "common"
    if "wifi" in raw or "wifi" in title or "wifi" in case_id:
        return "wifi"
    return raw or "common"


def is_automation_case(case: Dict[str, str]) -> bool:
    return "自动化" in (case.get("case_type") or "")


def is_stress_summary(summary: str) -> bool:
    return "_Stress_" in summary or "_Stb_" in summary or summary.endswith("_Stress") or summary.endswith("_Stb")