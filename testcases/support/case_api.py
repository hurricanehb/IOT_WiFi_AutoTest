"""Stable case-building API shared by generated WiFi tests."""
from __future__ import annotations

from typing import Any, Callable, Dict

import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status


def wifi_case(
    case_id: str,
    title: str,
    *,
    tag: str = "",
    pre: str = "",
) -> Dict[str, str]:
    return {"case_id": case_id, "title": title, "tag": tag, "pre": pre}


def wifi_case_from_markers(case_marker: Any, case_id_marker: Any) -> Dict[str, str]:
    if case_marker is None:
        raise ValueError("缺少 @pytest.mark.wifi_case(title=..., pre=...) 元数据")
    if case_id_marker is None or not case_id_marker.args:
        raise ValueError("缺少显式 @pytest.mark.case_id(...) 标记")
    if case_marker.args:
        raise ValueError("@pytest.mark.wifi_case 仅接受关键字参数")
    metadata = dict(case_marker.kwargs)
    title = metadata.pop("title", None)
    if not title:
        raise ValueError("@pytest.mark.wifi_case 缺少 title=...")
    return wifi_case(
        str(case_id_marker.args[0]),
        str(title),
        **metadata,
    )


def wifi_case_description(case: Dict[str, str]) -> str:
    return "\n".join(
        (
            f"用例 ID：{case['case_id']}",
            f"初始条件：{case['pre']}",
            f"测试目的：验证《{case['title']}》无线连接行为符合预期",
        )
    )


def run_manual_placeholder(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
) -> None:
    attach_wifi_status(case["case_id"], run_shell_cmd)
    title = case.get("title") or case.get("case_id") or ""
    pytest.skip(f"manual: 《{title}》需 UI/专用 AP 配置，见 testcases.md 操作步骤")