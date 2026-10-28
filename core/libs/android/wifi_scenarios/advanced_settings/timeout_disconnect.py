"""Android WLAN timeout disconnect scenarios."""
from __future__ import annotations

import sys

import pytest

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.utils.log_handler import get_logger

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_toreconn').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def run_wlan_timeout_disconnect_display_case(
    settings_ui, capsys, expected_timeout: str
) -> None:
    """Set a timeout-disconnect value and verify its preference-row summary."""
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    timeout_ui.open()
    timeout_ui.open_wlan_timeout_disconnect_selector()
    timeout_ui.select_wlan_timeout_disconnect(expected_timeout)
    timeout_ui.confirm_wlan_timeout_disconnect_selection()
    displayed_timeout = timeout_ui.wlan_timeout_disconnect_summary()
    message = f'设备"WLAN超时断连设置"栏显示"{displayed_timeout}"'
    if not timeout_ui.wlan_timeout_disconnect_matches(
        displayed_timeout, expected_timeout
    ):
        _write_uncaptured_line(capsys, f"{message}，设置失败，不符合用例预期")
        pytest.fail(f"{message}，设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def run_wlan_timeout_disconnect_custom_value_case(
    settings_ui, capsys, value: str, expected_summary: str
) -> None:
    """Save a custom timeout and verify its preference-row summary."""
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_timeout = timeout_ui.set_wlan_timeout_disconnect_custom_value(value)
    message = f'设备WLAN超时断连设置显示"{displayed_timeout}"，设置自定义超时时间'
    if not timeout_ui.wlan_timeout_disconnect_matches(
        displayed_timeout, expected_summary
    ):
        _write_uncaptured_line(capsys, f"{message}失败，不符合用例预期")
        pytest.fail(f"{message}失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}成功，符合用例预期")

def run_wlan_timeout_disconnect_custom_value_cannot_save_case(
    settings_ui, capsys, value: str
) -> None:
    """Verify an out-of-range or empty custom timeout cannot be saved."""
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value, save_enabled = (
        timeout_ui.enter_wlan_timeout_disconnect_custom_value(value)
    )
    message = f'设备设置WLAN超时断连时间为"{displayed_value}"，不在规定范围内，'
    if save_enabled:
        _write_uncaptured_line(capsys, f"{message}设置保存成功，不符合用例预期")
        pytest.fail(f"{message}设置保存成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法设置保存，符合用例预期")

def run_wlan_timeout_disconnect_illegal_value_cannot_input_case(
    settings_ui, capsys, value: str, value_kind: str
) -> None:
    """Verify a custom timeout rejects an illegal value."""
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value = timeout_ui.attempt_wlan_timeout_disconnect_custom_value(value)
    message = f"设备设置WLAN超时断连时间为{value_kind}，为非法值，"
    if timeout_ui.wlan_timeout_disconnect_custom_input_matches(
        displayed_value, value
    ):
        _write_uncaptured_line(capsys, f"{message}输入成功，不符合用例预期")
        pytest.fail(f"{message}输入成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法输入，符合用例预期")

def _set_wlan_timeout_disconnect_to_custom_value(settings_ui) -> None:
    """Set custom value 20 and ensure the row displays it."""
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    timeout_ui.open()
    displayed_timeout = timeout_ui.set_wlan_timeout_disconnect_custom_value("20")
    if not timeout_ui.wlan_timeout_disconnect_matches(displayed_timeout, "20秒"):
        pytest.fail(
            "设置自定义 WLAN 超时断连时间 20 后菜单栏未显示“20秒”："
            f"实际为 {displayed_timeout!r}"
        )

def _assert_wlan_timeout_disconnect_persists(
    settings_ui, capsys, lifecycle_action, success_message: str, failure_message: str
) -> None:
    """Verify custom timeout 20 remains displayed after a lifecycle action."""
    _set_wlan_timeout_disconnect_to_custom_value(settings_ui)
    lifecycle_action()

    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    timeout_ui.open()
    displayed_timeout = timeout_ui.wlan_timeout_disconnect_summary()
    if timeout_ui.wlan_timeout_disconnect_matches(displayed_timeout, "20秒"):
        _write_uncaptured_line(capsys, success_message)
        return
    _write_uncaptured_line(capsys, failure_message)
    pytest.fail(
        f"{failure_message}：WLAN超时断连设置实际显示 {displayed_timeout!r}"
    )

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

def run_wlan_timeout_disconnect_options_case(settings_ui, capsys) -> None:
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    timeout_ui.open()
    timeout_ui.open_wlan_timeout_disconnect_selector()
    actual_options = timeout_ui.wlan_timeout_disconnect_options()
    expected_options = ("3秒", "5秒", "8秒", "12秒", "16秒", "自定义")
    options_match = len(actual_options) == len(expected_options) and all(
        timeout_ui.wlan_timeout_disconnect_matches(actual, expected)
        for actual, expected in zip(actual_options, expected_options)
    )
    if not options_match:
        message = "设备WLAN超时断连设置可选项不符合用例预期"
        _write_uncaptured_line(capsys, message)
        pytest.fail(f"{message}：实际选项为{actual_options!r}")
    _write_uncaptured_line(capsys, "设备WLAN超时断连设置可选项符合用例预期")

def run_wlan_timeout_disconnect_default_case(settings_ui, capsys) -> None:
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    timeout_ui.open()
    displayed_timeout = timeout_ui.wlan_timeout_disconnect_summary()
    message = f'设备"WLAN超时断连设置"栏默认显示"{displayed_timeout}"'
    if not timeout_ui.wlan_timeout_disconnect_matches(displayed_timeout, "8秒"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    timeout_ui.open_wlan_timeout_disconnect_selector()
    selected_timeout = timeout_ui.selected_wlan_timeout_disconnect()
    message = f'设备"WLAN超时断连设置"弹窗默认选中"{selected_timeout}"'
    if not timeout_ui.wlan_timeout_disconnect_matches(selected_timeout, "8秒"):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_timeout_disconnect_custom_dialog_case(settings_ui, capsys) -> None:
    timeout_ui = WiFiAdvancedSettingsUI(settings_ui)
    dialog_texts = timeout_ui.current_wlan_timeout_disconnect_custom_dialog()
    if dialog_texts is None:
        timeout_ui.open()
        timeout_ui.open_wlan_timeout_disconnect_selector()
        dialog_texts = timeout_ui.open_wlan_timeout_disconnect_custom_dialog()
    prompt, input_hint = dialog_texts
    message = (
        f'设备WLAN超时断连设置自定义选项弹出提示框显示"{prompt}"，'
        f'编辑框内显示"{input_hint}"'
    )
    if not timeout_ui.wlan_timeout_disconnect_custom_dialog_matches(
        prompt, input_hint
    ):
        failure_message = (
            f"{message}，不符合用例预期；"
            f"预期弹窗提示为{timeout_ui.WLAN_TIMEOUT_DISCONNECT_CUSTOM_PROMPT!r}，"
            f"预期编辑框提示为{timeout_ui.WLAN_TIMEOUT_DISCONNECT_CUSTOM_INPUT_HINT!r}"
        )
        _write_uncaptured_line(capsys, failure_message)
        pytest.fail(failure_message)
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_timeout_disconnect_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_timeout_disconnect_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
        "设备关机重启，WLAN超时断连设置不变，符合用例预期",
        "设备关机重启后，WLAN超时断连设置发生改变，不符合用例预期",
    )

def run_wlan_timeout_disconnect_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_timeout_disconnect_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_settings(settings_ui),
        "设备关开WLAN开关，WLAN超时断连设置不变，符合用例预期",
        "设备关开WLAN开关后，WLAN超时断连设置发生改变，不符合用例预期",
    )

def run_wlan_timeout_disconnect_quick_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_timeout_disconnect_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_quick_settings(settings_ui),
        "设备快速设置栏关开WLAN开关，WLAN超时断连设置不变，符合用例预期",
        "设备快速设置栏关开WLAN开关后，WLAN超时断连设置发生改变，不符合用例预期",
    )

def run_wlan_timeout_disconnect_airplane_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_timeout_disconnect_persists(
        settings_ui,
        capsys,
        lambda: _toggle_airplane_mode_from_settings(settings_ui),
        "设备关开飞行模式，WLAN超时断连设置不变，符合用例预期",
        "设备关开飞行模式后，WLAN超时断连设置发生改变，不符合用例预期",
    )
