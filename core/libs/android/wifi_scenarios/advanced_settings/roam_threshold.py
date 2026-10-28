"""Android WLAN roam threshold scenarios."""
from __future__ import annotations

import re

import sys

import pytest

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.utils.log_handler import get_logger

WLAN_ROAM_THRESHOLD_PROPERTY_COMMAND = (
    'getprop | grep -iE "persist.vendor.wifi.roam.value"'
)

WLAN_ROAM_THRESHOLD_CYCLE = (("高", "60"), ("中", "65"), ("低", "70"))

WLAN_ROAM_THRESHOLD_CYCLE_COUNT = 10

_WLAN_ROAM_THRESHOLD_PROPERTY_PATTERN = re.compile(
    r"^\s*(?:\[?\s*persist\.vendor\.wifi\.roam[._]value\s*\]?\s*(?::|=)\s*"
    r"\[?\s*)?(?P<value>\d+)\s*\]?\s*$",
    re.IGNORECASE,
)

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_roamthresh').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def _wlan_roam_threshold_property_value(command_output: str) -> str | None:
    """Return the exact roam-threshold property value from ADB output."""
    for line in command_output.splitlines():
        match = _WLAN_ROAM_THRESHOLD_PROPERTY_PATTERN.fullmatch(line)
        if match is not None:
            return match.group("value")
    return None

def run_wlan_roam_threshold_cycle_case(
    settings_ui,
    run_shell_cmd,
    capsys,
    cycle_count: int = WLAN_ROAM_THRESHOLD_CYCLE_COUNT,
) -> None:
    """Repeat high-medium-low threshold changes and verify each persisted value."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    threshold_ui.open()

    for cycle_index in range(1, cycle_count + 1):
        for threshold, expected_property_value in WLAN_ROAM_THRESHOLD_CYCLE:
            threshold_ui.open_wlan_roam_threshold_selector()
            threshold_ui.select_wlan_roam_threshold(threshold)
            threshold_ui.confirm_wlan_roam_threshold_selection()
            displayed_threshold = threshold_ui.wlan_roam_threshold_summary()
            if not threshold_ui.wlan_roam_threshold_matches(
                displayed_threshold, threshold
            ):
                message = (
                    f'第{cycle_index}次“高”->“中”->“低”循环切换测试：'
                    f'切换\"{threshold}\"失败，菜单栏实际显示“{displayed_threshold}”，'
                    "不符合用例预期"
                )
                _write_uncaptured_line(capsys, message)
                pytest.fail(message)

            command_output = run_shell_cmd(WLAN_ROAM_THRESHOLD_PROPERTY_COMMAND)
            actual_property_value = _wlan_roam_threshold_property_value(command_output)
            message = (
                f'第{cycle_index}次“高”->“中”->“低”循环切换测试：'
                f"切换\"{threshold}\"成功，后台命令返回值为（"
                f"{actual_property_value or '未读取到'}），"
            )
            if actual_property_value != expected_property_value:
                message += "返回值与所选项不一致，不符合用例预期"
                _write_uncaptured_line(capsys, message)
                pytest.fail(
                    f"{message}：期望 {expected_property_value!r}，"
                    f"命令原始输出为 {command_output!r}"
                )
            _write_uncaptured_line(
                capsys, f"{message}返回值与所选项一致，符合用例预期"
            )

def run_wlan_roam_threshold_display_case(
    settings_ui, capsys, expected_threshold: str
) -> None:
    """Set a roaming threshold and verify the value displayed on its row."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    threshold_ui.open()
    threshold_ui.open_wlan_roam_threshold_selector()
    threshold_ui.select_wlan_roam_threshold(expected_threshold)
    threshold_ui.confirm_wlan_roam_threshold_selection()
    displayed_threshold = threshold_ui.wlan_roam_threshold_summary()
    message = f'设备"WLAN漫游阈值"栏显示"{displayed_threshold}"'
    if not threshold_ui.wlan_roam_threshold_matches(
        displayed_threshold, expected_threshold
    ):
        _write_uncaptured_line(capsys, f"{message},设置失败，不符合用例预期")
        pytest.fail(f"{message},设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def run_wlan_roam_threshold_custom_value_case(
    settings_ui, capsys, value: str, expected_summary: str
) -> None:
    """Save a custom threshold and verify its preference-row summary."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_threshold = threshold_ui.set_wlan_roam_threshold_custom_value(value)
    message = f"设备WLAN漫游阈值显示\"{displayed_threshold}\"，设置自定义阈值"
    if not threshold_ui.wlan_roam_threshold_matches(
        displayed_threshold, expected_summary
    ):
        _write_uncaptured_line(capsys, f"{message}失败，不符合用例预期")
        pytest.fail(f"{message}失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}成功，符合用例预期")

def run_wlan_roam_threshold_custom_value_cannot_save_case(
    settings_ui, capsys, value: str
) -> None:
    """Verify an out-of-range custom roaming threshold cannot be saved."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value, save_enabled = (
        threshold_ui.enter_wlan_roam_threshold_custom_value(value)
    )
    message = (
        f'设备设置WLAN漫游阈值为"{displayed_value}"，不在规定范围内，'
    )
    if save_enabled:
        _write_uncaptured_line(capsys, f"{message}设置保存成功，不符合用例预期")
        pytest.fail(f"{message}设置保存成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法设置保存，符合用例预期")

def run_wlan_roam_threshold_illegal_value_cannot_input_case(
    settings_ui, capsys, value: str, value_kind: str
) -> None:
    """Verify a custom roaming threshold rejects an illegal value."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value = threshold_ui.attempt_wlan_roam_threshold_custom_value(value)
    message = f"设备设置WLAN漫游阈值为{value_kind}，为非法值，"
    if threshold_ui.wlan_roam_threshold_custom_input_matches(
        displayed_value, value
    ):
        _write_uncaptured_line(capsys, f"{message}输入成功，不符合用例预期")
        pytest.fail(f"{message}输入成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法输入，符合用例预期")

def _set_wlan_roam_threshold_to_low(settings_ui) -> None:
    """Set the custom value 70 and ensure the row displays the low preset."""
    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    threshold_ui.open()
    displayed_threshold = threshold_ui.set_wlan_roam_threshold_custom_value("70")
    if not threshold_ui.wlan_roam_threshold_matches(displayed_threshold, "低"):
        pytest.fail(
            "设置自定义 WLAN 漫游阈值 70 后菜单栏未显示“低”："
            f"实际为 {displayed_threshold!r}"
        )

def _assert_wlan_roam_threshold_persists(
    settings_ui, capsys, lifecycle_action, success_message: str, failure_message: str
) -> None:
    """Verify custom threshold 70 remains displayed as low after a lifecycle action."""
    _set_wlan_roam_threshold_to_low(settings_ui)
    lifecycle_action()

    threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    threshold_ui.open()
    displayed_threshold = threshold_ui.wlan_roam_threshold_summary()
    if threshold_ui.wlan_roam_threshold_matches(displayed_threshold, "低"):
        _write_uncaptured_line(capsys, success_message)
        return
    _write_uncaptured_line(capsys, failure_message)
    pytest.fail(
        f"{failure_message}：WLAN漫游阈值实际显示 {displayed_threshold!r}"
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

def run_wlan_roam_threshold_default_case(settings_ui, capsys) -> None:
    roam_threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    roam_threshold_ui.open()
    displayed_threshold = roam_threshold_ui.wlan_roam_threshold_summary()
    message = f'设备"WLAN漫游阈值"栏默认显示"{displayed_threshold}"'
    if not roam_threshold_ui.wlan_roam_threshold_matches(
        displayed_threshold, "中"
    ):
        _write_uncaptured_line(capsys, f"{message},不符合用例预期")
        pytest.fail(f"{message},不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    roam_threshold_ui.open_wlan_roam_threshold_selector()
    selected_threshold = roam_threshold_ui.selected_wlan_roam_threshold()
    message = f'设备"WLAN漫游阈值"弹窗默认选中"{selected_threshold}"'
    if not roam_threshold_ui.wlan_roam_threshold_matches(
        selected_threshold, "中"
    ):
        _write_uncaptured_line(capsys, f"{message},不符合用例预期")
        pytest.fail(f"{message},不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_roam_threshold_options_case(settings_ui, capsys) -> None:
    roam_threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    roam_threshold_ui.open()
    roam_threshold_ui.open_wlan_roam_threshold_selector()
    actual_options = roam_threshold_ui.wlan_roam_threshold_options()
    expected_options = ("高", "中", "低", "自定义")
    options_match = len(actual_options) == len(expected_options) and all(
        roam_threshold_ui.wlan_roam_threshold_matches(actual, expected)
        for actual, expected in zip(actual_options, expected_options)
    )
    if not options_match:
        message = "设备WLAN漫游阈值可选项不符合用例预期"
        _write_uncaptured_line(capsys, message)
        pytest.fail(f"{message}：实际选项为{actual_options!r}")
    _write_uncaptured_line(capsys, "设备WLAN漫游阈值可选项符合用例预期")

def run_wlan_roam_threshold_custom_dialog_case(settings_ui, capsys) -> None:
    roam_threshold_ui = WiFiAdvancedSettingsUI(settings_ui)
    dialog_texts = roam_threshold_ui.current_wlan_roam_threshold_custom_dialog()
    if dialog_texts is None:
        roam_threshold_ui.open()
        roam_threshold_ui.open_wlan_roam_threshold_selector()
        dialog_texts = roam_threshold_ui.open_wlan_roam_threshold_custom_dialog()
    prompt, input_hint = dialog_texts
    message = (
        f"设备WLAN漫游阈值自定义选项弹出提示框显示\"{prompt}\"，"
        f"编辑框内显示\"{input_hint}\""
    )
    if not roam_threshold_ui.wlan_roam_threshold_custom_dialog_matches(
        prompt, input_hint
    ):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_roam_threshold_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_roam_threshold_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
        "设备关机重启，WLAN漫游阈值设置不变，符合用例预期",
        "设备关机重启后，WLAN漫游阈值设置发生改变，不符合用例预期",
    )

def run_wlan_roam_threshold_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_threshold_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_settings(settings_ui),
        "设备关开WLAN开关，WLAN漫游阈值设置不变，符合用例预期",
        "设备关开WLAN开关后，WLAN漫游阈值设置发生改变，不符合用例预期",
    )

def run_wlan_roam_threshold_quick_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_threshold_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_quick_settings(settings_ui),
        "设备快速设置栏关开WLAN开关，WLAN漫游阈值设置不变，符合用例预期",
        "设备快速设置栏关开WLAN开关后，WLAN漫游阈值设置发生改变，不符合用例预期",
    )

def run_wlan_roam_threshold_airplane_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_threshold_persists(
        settings_ui,
        capsys,
        lambda: _toggle_airplane_mode_from_settings(settings_ui),
        "设备关开飞行模式，WLAN漫游阈值设置不变，符合用例预期",
        "设备关开飞行模式后，WLAN漫游阈值设置发生改变，不符合用例预期",
    )
