from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from testcases.support import case_api
from testcases.support.case_api import (
    run_manual_placeholder,
    wifi_case_description,
    wifi_case_from_markers,
)


def test_wifi_case_from_markers_combines_static_id_and_metadata() -> None:
    case_marker = SimpleNamespace(
        args=(),
        kwargs={"title": "连接目标网络", "pre": "设备 ADB 在线"},
    )
    case_id_marker = SimpleNamespace(args=("CASE-001",))

    case = wifi_case_from_markers(case_marker, case_id_marker)

    assert case == {
        "case_id": "CASE-001",
        "title": "连接目标网络",
        "tag": "",
        "pre": "设备 ADB 在线",
    }
    assert wifi_case_description(case) == (
        "用例 ID：CASE-001\n"
        "初始条件：设备 ADB 在线\n"
        "测试目的：验证《连接目标网络》无线连接行为符合预期"
    )


def test_wifi_case_from_markers_requires_explicit_case_id() -> None:
    case_marker = SimpleNamespace(args=(), kwargs={"title": "连接目标网络"})

    with pytest.raises(ValueError, match="显式.*case_id"):
        wifi_case_from_markers(case_marker, None)


def test_wifi_case_from_markers_rejects_positional_metadata() -> None:
    case_marker = SimpleNamespace(args=("连接目标网络",), kwargs={})
    case_id_marker = SimpleNamespace(args=("CASE-001",))

    with pytest.raises(ValueError, match="仅接受关键字参数"):
        wifi_case_from_markers(case_marker, case_id_marker)


def test_manual_placeholder_attaches_status_before_skip(monkeypatch) -> None:
    case = {
        "case_id": "CASE-001",
        "title": "连接目标网络",
        "tag": "",
        "pre": "设备 ADB 在线",
    }

    attach_status = Mock()
    monkeypatch.setattr(case_api, "attach_wifi_status", attach_status)
    run_shell_cmd = Mock()

    with pytest.raises(pytest.skip.Exception):
        run_manual_placeholder(case, run_shell_cmd)

    attach_status.assert_called_once_with("CASE-001", run_shell_cmd)