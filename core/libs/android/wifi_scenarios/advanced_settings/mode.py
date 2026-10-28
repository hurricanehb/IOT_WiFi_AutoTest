"""Android WLAN mode scenarios."""
from __future__ import annotations

import sys

import pytest

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.utils.log_handler import get_logger

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_mode').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def run_wlan_mode_display_case(settings_ui, capsys, expected_mode: str) -> None:
    """Set a WLAN mode and verify the value displayed on its preference row."""
    mode_ui = WiFiAdvancedSettingsUI(settings_ui)
    mode_ui.open()
    mode_ui.open_wlan_mode_selector()
    mode_ui.select_wlan_mode(expected_mode)
    mode_ui.confirm_wlan_mode_selection()
    displayed_mode = mode_ui.wlan_mode_summary()
    message = f'设备"WLAN模式设置"栏显示"{displayed_mode}"'
    if not mode_ui.wlan_mode_matches(displayed_mode, expected_mode):
        _write_uncaptured_line(capsys, f"{message},设置模式不成功，不符合用例预期")
        pytest.fail(f"{message},设置模式不成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置模式成功，符合用例预期")

def run_wlan_mode_default_case(settings_ui, capsys) -> None:
    mode_ui = WiFiAdvancedSettingsUI(settings_ui)
    mode_ui.open()
    displayed_mode = mode_ui.wlan_mode_summary()
    if displayed_mode != "自动选择":
        message = f'设备"WLAN模式设置"栏显示"{displayed_mode}",不符合用例预期'
        _write_uncaptured_line(capsys, message)
        pytest.fail(message)

    mode_ui.open_wlan_mode_selector()
    selected_mode = mode_ui.selected_wlan_mode()
    if selected_mode != "自动选择":
        message = f'设备"WLAN模式设置"弹窗选中"{selected_mode}",不符合用例预期'
        _write_uncaptured_line(capsys, message)
        pytest.fail(message)

    _write_uncaptured_line(
        capsys,
        '设备"WLAN模式设置"栏显示和"WLAN模式设置"弹窗选中都为"自动选择"，符合用例期望',
    )
