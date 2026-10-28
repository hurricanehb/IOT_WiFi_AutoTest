"""Standard skip behavior for generated test cases."""
from __future__ import annotations

from collections.abc import Mapping

import pytest


def _title(case: Mapping[str, str]) -> str:
    return case.get("title") or case.get("case_id") or ""


def run_manual_placeholder(case: Mapping[str, str]) -> None:
    pytest.skip(f"manual: 《{_title(case)}》需 UI/专用 AP 配置，见 testcases.md 操作步骤")


def run_not_applicable(case: Mapping[str, str], *, reason: str) -> None:
    pytest.skip(f"not_applicable: 《{_title(case)}》{reason}")