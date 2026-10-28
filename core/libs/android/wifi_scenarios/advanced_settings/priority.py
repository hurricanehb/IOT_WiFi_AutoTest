"""Android WLAN priority scenarios."""
from __future__ import annotations

import sys

import pytest

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.utils.log_handler import get_logger

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_priorty').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def run_wlan_priority_display_case(settings_ui, capsys, expected_priority: str) -> None:
    """Set a WLAN priority and verify the value displayed on its row."""
    priority_ui = WiFiAdvancedSettingsUI(settings_ui)
    priority_ui.open()
    priority_ui.open_wlan_priority_selector()
    priority_ui.select_wlan_priority(expected_priority)
    priority_ui.confirm_wlan_priority_selection()
    displayed_priority = priority_ui.wlan_priority_summary()
    message = f'设备"WLAN优先等级"栏显示"{displayed_priority}"'
    if not priority_ui.wlan_priority_matches(displayed_priority, expected_priority):
        _write_uncaptured_line(capsys, f"{message}，设置失败，不符合用例预期")
        pytest.fail(f"{message}，设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def _set_wlan_priority_to_advanced(settings_ui) -> None:
    """Set WLAN priority to advanced and ensure the row displays it."""
    priority_ui = WiFiAdvancedSettingsUI(settings_ui)
    priority_ui.open()
    priority_ui.open_wlan_priority_selector()
    priority_ui.select_wlan_priority("高级")
    priority_ui.confirm_wlan_priority_selection()
    displayed_priority = priority_ui.wlan_priority_summary()
    if not priority_ui.wlan_priority_matches(displayed_priority, "高级"):
        pytest.fail(
            "设置 WLAN 优先等级为“高级”后菜单栏未显示“高级”："
            f"实际为 {displayed_priority!r}"
        )

def _assert_wlan_priority_persists(
    settings_ui, capsys, lifecycle_action, success_message: str, failure_message: str
) -> None:
    """Verify advanced priority remains displayed after a lifecycle action."""
    _set_wlan_priority_to_advanced(settings_ui)
    lifecycle_action()

    priority_ui = WiFiAdvancedSettingsUI(settings_ui)
    priority_ui.open()
    displayed_priority = priority_ui.wlan_priority_summary()
    if priority_ui.wlan_priority_matches(displayed_priority, "高级"):
        _write_uncaptured_line(capsys, success_message)
        return
    _write_uncaptured_line(capsys, failure_message)
    pytest.fail(f"{failure_message}：WLAN优先等级实际显示 {displayed_priority!r}")

def _toggle_wlan_from_settings(settings_ui) -> None:
    """Disable and re-enable WLAN through Settings' visible Internet page."""
    settings_ui.set_wifi_enabled_from_settings(False)
    settings_ui.set_wifi_enabled_from_settings(True)

def _toggle_wlan_from_quick_settings(settings_ui) -> None:
    """Disable and re-enable WLAN through the Quick Settings Internet panel."""
    settings_ui.set_quick_settings_wifi_enabled(False)
    settings_ui.set_quick_settings_wifi_enabled(True)

def _toggle_airplane_mode_from_settings(settings_ui) -> None:
    """Enable and disable Airplane mode through the Android Settings page."""
    settings_ui.set_airplane_mode_from_settings(True)
    settings_ui.set_airplane_mode_from_settings(False)

def run_wlan_priority_options_case(settings_ui, capsys) -> None:
    priority_ui = WiFiAdvancedSettingsUI(settings_ui)
    priority_ui.open()
    priority_ui.open_wlan_priority_selector()
    actual_options = priority_ui.wlan_priority_options()
    expected_options = ("普通", "初级", "中级", "高级")
    options_match = len(actual_options) == len(expected_options) and all(
        priority_ui.wlan_priority_matches(actual, expected)
        for actual, expected in zip(actual_options, expected_options)
    )
    if not options_match:
        message = "设备WLAN优先等级可选项不符合用例预期"
        _write_uncaptured_line(capsys, message)
        pytest.fail(f"{message}：实际选项为{actual_options!r}")
    _write_uncaptured_line(capsys, "设备WLAN优先等级可选项符合用例预期")

def run_wlan_priority_default_case(settings_ui, capsys) -> None:
    priority_ui = WiFiAdvancedSettingsUI(settings_ui)
    priority_ui.open()
    displayed_priority = priority_ui.wlan_priority_summary()
    message = f'设备"WLAN优先等级"栏默认显示"{displayed_priority}"'
    if not priority_ui.wlan_priority_matches(displayed_priority, "普通"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    priority_ui.open_wlan_priority_selector()
    selected_priority = priority_ui.selected_wlan_priority()
    message = f'设备"WLAN优先等级"弹窗默认选中"{selected_priority}"'
    if not priority_ui.wlan_priority_matches(selected_priority, "普通"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_priority_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_priority_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
        "设备关机重启，WLAN优先等级设置不变，符合用例预期",
        "设备关机重启后，WLAN优先等级设置发生改变，不符合用例预期",
    )

def run_wlan_priority_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_priority_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_settings(settings_ui),
        "设备关开WLAN开关，WLAN优先等级设置不变，符合用例预期",
        "设备关开WLAN开关后，WLAN优先等级设置发生改变，不符合用例预期",
    )

def run_wlan_priority_quick_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_priority_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_quick_settings(settings_ui),
        "设备快速设置栏关开WLAN开关，WLAN优先等级设置不变，符合用例预期",
        "设备快速设置栏关开WLAN开关后，WLAN优先等级设置发生改变，不符合用例预期",
    )

def run_wlan_priority_airplane_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_priority_persists(
        settings_ui,
        capsys,
        lambda: _toggle_airplane_mode_from_settings(settings_ui),
        "设备关开飞行模式，WLAN优先等级设置不变，符合用例预期",
        "设备关开飞行模式后，WLAN优先等级设置发生改变，不符合用例预期",
    )
