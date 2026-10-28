"""Android WLAN energy save scenarios."""
from __future__ import annotations

import sys

import pytest

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.utils.log_handler import get_logger

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_energysave').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def run_wlan_energy_save_display_case(settings_ui, capsys, expected_mode: str) -> None:
    """Set an energy-save mode and verify its preference-row summary."""
    energy_save_ui = WiFiAdvancedSettingsUI(settings_ui)
    energy_save_ui.open()
    energy_save_ui.open_wlan_energy_save_selector()
    energy_save_ui.select_wlan_energy_save(expected_mode)
    energy_save_ui.confirm_wlan_energy_save_selection()
    displayed_mode = energy_save_ui.wlan_energy_save_summary()
    message = f'设备"WLAN省电模式设置"栏显示"{displayed_mode}"'
    if not energy_save_ui.wlan_energy_save_matches(displayed_mode, expected_mode):
        _write_uncaptured_line(capsys, f"{message}，设置失败，不符合用例预期")
        pytest.fail(f"{message}，设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def _set_wlan_energy_save_to_performance_mode(settings_ui) -> None:
    """Set performance mode and ensure its preference row displays it."""
    energy_save_ui = WiFiAdvancedSettingsUI(settings_ui)
    energy_save_ui.open()
    energy_save_ui.open_wlan_energy_save_selector()
    energy_save_ui.select_wlan_energy_save("性能模式")
    energy_save_ui.confirm_wlan_energy_save_selection()
    displayed_mode = energy_save_ui.wlan_energy_save_summary()
    if not energy_save_ui.wlan_energy_save_matches(displayed_mode, "性能模式"):
        pytest.fail(
            "设置 WLAN 省电模式为性能模式后菜单栏未显示“性能模式”："
            f"实际为 {displayed_mode!r}"
        )

def _assert_wlan_energy_save_persists(
    settings_ui, capsys, lifecycle_action, success_message: str, failure_message: str
) -> None:
    """Verify performance mode remains displayed after a lifecycle action."""
    _set_wlan_energy_save_to_performance_mode(settings_ui)
    lifecycle_action()

    energy_save_ui = WiFiAdvancedSettingsUI(settings_ui)
    energy_save_ui.open()
    displayed_mode = energy_save_ui.wlan_energy_save_summary()
    if energy_save_ui.wlan_energy_save_matches(displayed_mode, "性能模式"):
        _write_uncaptured_line(capsys, success_message)
        return
    _write_uncaptured_line(capsys, failure_message)
    pytest.fail(
        f"{failure_message}：WLAN省电模式设置实际显示 {displayed_mode!r}"
    )

def _toggle_wlan_from_settings(settings_ui) -> None:
    """Disable and re-enable WLAN through Settings' visible Internet page."""
    settings_ui.set_wifi_switch(False)
    settings_ui.set_wifi_switch(True)

def _toggle_wlan_from_quick_settings(settings_ui) -> None:
    """Disable and re-enable WLAN through the Quick Settings Internet panel."""
    settings_ui.set_quick_settings_wifi_enabled(False)
    settings_ui.set_quick_settings_wifi_enabled(True)

def _toggle_airplane_mode_from_settings(settings_ui) -> None:
    """Enable and disable Airplane mode through the Android Settings page."""
    try:
        settings_ui.set_airplane_mode_from_settings(True)
    finally:
        settings_ui.set_airplane_mode_from_settings(False)

def run_wlan_energy_save_default_case(settings_ui, capsys) -> None:
    energy_save_ui = WiFiAdvancedSettingsUI(settings_ui)
    energy_save_ui.open()
    displayed_mode = energy_save_ui.wlan_energy_save_summary()
    message = f'设备"WLAN省电模式设置"栏默认显示"{displayed_mode}"'
    if not energy_save_ui.wlan_energy_save_matches(displayed_mode, "省电模式"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    energy_save_ui.open_wlan_energy_save_selector()
    selected_mode = energy_save_ui.selected_wlan_energy_save()
    message = f'设备"WLAN省电模式设置"弹窗默认选中"{selected_mode}"'
    if not energy_save_ui.wlan_energy_save_matches(selected_mode, "省电模式"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_energy_save_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_energy_save_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
        "设备关机重启，WLAN省电模式设置不变，符合用例预期",
        "设备关机重启后，WLAN省电模式设置发生改变，不符合用例预期",
    )

def run_wlan_energy_save_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_energy_save_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_settings(settings_ui),
        "设备关开WLAN开关，WLAN省电模式设置不变，符合用例预期",
        "设备关开WLAN开关后，WLAN省电模式设置发生改变，不符合用例预期",
    )

def run_wlan_energy_save_quick_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_energy_save_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_quick_settings(settings_ui),
        "设备快速设置栏关开WLAN开关，WLAN省电模式设置不变，符合用例预期",
        "设备快速设置栏关开WLAN开关后，WLAN省电模式设置发生改变，不符合用例预期",
    )

def run_wlan_energy_save_airplane_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_energy_save_persists(
        settings_ui,
        capsys,
        lambda: _toggle_airplane_mode_from_settings(settings_ui),
        "设备关开飞行模式，WLAN省电模式设置不变，符合用例预期",
        "设备关开飞行模式后，WLAN省电模式设置发生改变，不符合用例预期",
    )
