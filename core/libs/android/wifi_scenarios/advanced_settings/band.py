"""Android WLAN band scenarios."""
from __future__ import annotations

import sys

import pytest

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.utils.log_handler import get_logger

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_band').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def run_wlan_band_display_case(settings_ui, capsys, expected_band: str) -> None:
    """Set a WLAN band and verify the value displayed on its preference row."""
    band_ui = WiFiAdvancedSettingsUI(settings_ui)
    band_ui.open()
    band_ui.open_wlan_band_selector()
    band_ui.select_wlan_band(expected_band)
    band_ui.confirm_wlan_band_selection()
    displayed_band = band_ui.wlan_band_summary()
    message = f'设备"WLAN频段设置"栏显示"{displayed_band}"'
    if not band_ui.wlan_band_matches(displayed_band, expected_band):
        _write_uncaptured_line(capsys, f"{message},设置失败，不符合用例预期")
        pytest.fail(f"{message},设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def _assert_wlan_band_persists(settings_ui, capsys, lifecycle_action) -> None:
    """Change the WLAN band, then verify the selected value persists."""
    band_ui = WiFiAdvancedSettingsUI(settings_ui)
    band_ui.open()
    initial_band = band_ui.wlan_band_summary()
    for current_band, expected_band in (
        ("自动选择", "2.4GHz"),
        ("2.4GHz", "5GHz"),
        ("5GHz", "自动选择"),
    ):
        if band_ui.wlan_band_matches(initial_band, current_band):
            break
    else:
        pytest.fail(
            f"WLAN频段设置当前显示 {initial_band!r}，"
            "无法在自动选择、2.4GHz、5GHz 间切换"
        )

    band_ui.open_wlan_band_selector()
    band_ui.select_wlan_band(expected_band)
    band_ui.confirm_wlan_band_selection()
    displayed_band = band_ui.wlan_band_summary()
    if not band_ui.wlan_band_matches(displayed_band, expected_band):
        pytest.fail(
            f"将 WLAN 频段从 {initial_band!r} 设置为 {expected_band!r} 后菜单栏显示异常："
            f"实际为 {displayed_band!r}"
        )

    lifecycle_action()

    band_ui = WiFiAdvancedSettingsUI(settings_ui)
    band_ui.open()
    displayed_band = band_ui.wlan_band_summary()
    message = f'设备关机重启后，"WLAN频段设置"栏显示"{displayed_band}"'
    if band_ui.wlan_band_matches(displayed_band, expected_band):
        _write_uncaptured_line(capsys, f"{message}，设置不变，符合用例预期")
        return
    _write_uncaptured_line(capsys, f"{message}，设置发生改变，不符合用例预期")
    pytest.fail(
        f"{message}：期望 {expected_band!r}，不符合用例预期"
    )

def run_wlan_band_default_case(settings_ui, capsys) -> None:
    band_ui = WiFiAdvancedSettingsUI(settings_ui)
    band_ui.open()
    displayed_band = band_ui.wlan_band_summary()
    message = f'设备"WLAN频段设置"栏默认显示"{displayed_band}"'
    if not band_ui.wlan_band_matches(displayed_band, "自动选择"):
        _write_uncaptured_line(capsys, f"{message},不符合用例预期")
        pytest.fail(f"{message},不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    band_ui.open_wlan_band_selector()
    selected_band = band_ui.selected_wlan_band()
    message = f'设备"WLAN频段设置"弹窗默认选中"{selected_band}"'
    if not band_ui.wlan_band_matches(selected_band, "自动选择"):
        _write_uncaptured_line(capsys, f"{message},不符合用例预期")
        pytest.fail(f"{message},不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_band_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_band_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
    )
