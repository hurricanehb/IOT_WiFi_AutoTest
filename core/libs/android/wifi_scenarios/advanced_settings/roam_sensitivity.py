"""Android WLAN roam sensitivity scenarios."""
from __future__ import annotations

import re

import sys

import pytest

from core.libs.android.wifi_scenarios.ip_configuration import reboot_and_wait

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI

from core.utils.log_handler import get_logger

WLAN_ROAM_SENSITIVITY_PROPERTY_COMMAND = (
    'getprop | grep -iE "persist.vendor.wifi.roam_delta"'
)

WLAN_ROAM_SENSITIVITY_CYCLE = (("5dB", "5"), ("7dB", "7"), ("9dB", "9"))

WLAN_ROAM_SENSITIVITY_CYCLE_COUNT = 10

_WLAN_ROAM_SENSITIVITY_PROPERTY_PATTERN = re.compile(
    r"^\s*(?:\[?\s*persist\.vendor\.wifi\.roam[_\.]delta\s*\]?\s*(?::|=)\s*"
    r"\[?\s*)?(?P<value>\d+)\s*\]?\s*$",
    re.IGNORECASE,
)

def _write_uncaptured_line(capsys, message: str) -> None:
    """Write a result line directly to the terminal outside pytest capture."""
    get_logger('test_func_advwlanset_roamsens').info("%s", message)
    with capsys.disabled():
        stdout = sys.__stdout__ or sys.stdout
        if stdout is None:
            raise RuntimeError("标准输出不可用")
        stdout.write(f"\n{message}\n")
        stdout.flush()

def _wlan_roam_sensitivity_property_value(command_output: str) -> str | None:
    """Return the exact roaming-sensitivity property value from ADB output."""
    for line in command_output.splitlines():
        match = _WLAN_ROAM_SENSITIVITY_PROPERTY_PATTERN.fullmatch(line)
        if match is not None:
            return match.group("value")
    return None

def run_wlan_roam_sensitivity_display_case(
    settings_ui, capsys, expected_sensitivity: str
) -> None:
    """Set a roaming sensitivity and verify the value displayed on its row."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()
    sensitivity_ui.open_wlan_roam_sensitivity_selector()
    sensitivity_ui.select_wlan_roam_sensitivity(expected_sensitivity)
    sensitivity_ui.confirm_wlan_roam_sensitivity_selection()
    displayed_sensitivity = sensitivity_ui.wlan_roam_sensitivity_summary()
    message = f'设备"WLAN漫游灵敏度"栏显示"{displayed_sensitivity}"'
    if not sensitivity_ui.wlan_roam_sensitivity_matches(
        displayed_sensitivity, expected_sensitivity
    ):
        _write_uncaptured_line(capsys, f"{message}，设置失败，不符合用例预期")
        pytest.fail(f"{message}，设置失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，设置成功，符合用例预期")

def run_wlan_roam_sensitivity_custom_value_case(
    settings_ui, capsys, value: str, expected_summary: str
) -> None:
    """Save a custom sensitivity and verify its preference-row summary."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_sensitivity = sensitivity_ui.set_wlan_roam_sensitivity_custom_value(
        value
    )
    message = (
        f'设备WLAN漫游灵敏度显示"{displayed_sensitivity}"，设置自定义灵敏度'
    )
    if not sensitivity_ui.wlan_roam_sensitivity_matches(
        displayed_sensitivity, expected_summary
    ):
        _write_uncaptured_line(capsys, f"{message}失败，不符合用例预期")
        pytest.fail(f"{message}失败，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}成功，符合用例预期")

def run_wlan_roam_sensitivity_custom_value_cannot_save_case(
    settings_ui, capsys, value: str
) -> None:
    """Verify an out-of-range custom roaming sensitivity cannot be saved."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value, save_enabled = (
        sensitivity_ui.enter_wlan_roam_sensitivity_custom_value(value)
    )
    message = (
        f'设备设置WLAN漫游灵敏度为"{displayed_value}"，不在规定范围内，'
    )
    if save_enabled:
        _write_uncaptured_line(capsys, f"{message}设置保存成功，不符合用例预期")
        pytest.fail(f"{message}设置保存成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法设置保存，符合用例预期")

def run_wlan_roam_sensitivity_illegal_value_cannot_input_case(
    settings_ui, capsys, value: str, value_kind: str
) -> None:
    """Verify a custom roaming sensitivity rejects an illegal value."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    displayed_value = sensitivity_ui.attempt_wlan_roam_sensitivity_custom_value(value)
    message = f"设备设置WLAN漫游灵敏度为{value_kind}，为非法值，"
    if sensitivity_ui.wlan_roam_sensitivity_custom_input_matches(
        displayed_value, value
    ):
        _write_uncaptured_line(capsys, f"{message}输入成功，不符合用例预期")
        pytest.fail(f"{message}输入成功，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}无法输入，符合用例预期")

def _set_wlan_roam_sensitivity_to_custom_value(settings_ui) -> None:
    """Set custom value 20 and ensure the row displays it."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()
    displayed_sensitivity = sensitivity_ui.set_wlan_roam_sensitivity_custom_value(
        "20"
    )
    if not sensitivity_ui.wlan_roam_sensitivity_matches(
        displayed_sensitivity, "20dB"
    ):
        pytest.fail(
            "设置自定义 WLAN 漫游灵敏度 20 后菜单栏未显示“20dB”："
            f"实际为 {displayed_sensitivity!r}"
        )

def _assert_wlan_roam_sensitivity_persists(
    settings_ui, capsys, lifecycle_action, success_message: str, failure_message: str
) -> None:
    """Verify custom sensitivity 20 remains displayed after a lifecycle action."""
    _set_wlan_roam_sensitivity_to_custom_value(settings_ui)
    lifecycle_action()

    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()
    displayed_sensitivity = sensitivity_ui.wlan_roam_sensitivity_summary()
    if sensitivity_ui.wlan_roam_sensitivity_matches(displayed_sensitivity, "20dB"):
        _write_uncaptured_line(capsys, success_message)
        return
    _write_uncaptured_line(capsys, failure_message)
    pytest.fail(
        f"{failure_message}：WLAN漫游灵敏度实际显示 {displayed_sensitivity!r}"
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

def run_wlan_roam_sensitivity_cycle_case(
    settings_ui,
    run_shell_cmd,
    capsys,
    cycle_count: int = WLAN_ROAM_SENSITIVITY_CYCLE_COUNT,
) -> None:
    """Repeat preset changes and verify each persisted sensitivity value."""
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()

    for cycle_index in range(1, cycle_count + 1):
        for sensitivity, expected_property_value in WLAN_ROAM_SENSITIVITY_CYCLE:
            sensitivity_ui.open_wlan_roam_sensitivity_selector()
            sensitivity_ui.select_wlan_roam_sensitivity(sensitivity)
            sensitivity_ui.confirm_wlan_roam_sensitivity_selection()
            displayed_sensitivity = sensitivity_ui.wlan_roam_sensitivity_summary()
            if not sensitivity_ui.wlan_roam_sensitivity_matches(
                displayed_sensitivity, sensitivity
            ):
                message = (
                    f'第{cycle_index}次“5dB”->“7dB”->“9dB”循环切换测试：'
                    f'切换"{sensitivity}"失败，菜单栏实际显示“{displayed_sensitivity}”，'
                    "不符合用例预期"
                )
                _write_uncaptured_line(capsys, message)
                pytest.fail(message)

            command_output = run_shell_cmd(WLAN_ROAM_SENSITIVITY_PROPERTY_COMMAND)
            actual_property_value = _wlan_roam_sensitivity_property_value(command_output)
            message = (
                f'第{cycle_index}次“5dB”->“7dB”->“9dB”循环切换测试：'
                f'切换"{sensitivity}"成功，后台命令返回值为（'
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

def run_wlan_roam_sensitivity_default_case(settings_ui, capsys) -> None:
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()
    displayed_sensitivity = sensitivity_ui.wlan_roam_sensitivity_summary()
    message = f'设备"WLAN漫游灵敏度"栏默认显示"{displayed_sensitivity}"'
    if not sensitivity_ui.wlan_roam_sensitivity_matches(
        displayed_sensitivity, "7dB"
    ):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

    sensitivity_ui.open_wlan_roam_sensitivity_selector()
    selected_sensitivity = sensitivity_ui.selected_wlan_roam_sensitivity()
    message = f'设备"WLAN漫游灵敏度"弹窗默认选中"{selected_sensitivity}"'
    if not sensitivity_ui.wlan_roam_sensitivity_matches(
        selected_sensitivity, "7dB"
    ):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_roam_sensitivity_options_case(settings_ui, capsys) -> None:
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    sensitivity_ui.open()
    sensitivity_ui.open_wlan_roam_sensitivity_selector()
    actual_options = sensitivity_ui.wlan_roam_sensitivity_options()
    expected_options = ("5dB", "7dB", "9dB", "自定义")
    options_match = len(actual_options) == len(expected_options) and all(
        sensitivity_ui.wlan_roam_sensitivity_matches(actual, expected)
        for actual, expected in zip(actual_options, expected_options)
    )
    if not options_match:
        message = "设备WLAN漫游灵敏度可选项不符合用例预期"
        _write_uncaptured_line(capsys, message)
        pytest.fail(f"{message}：实际选项为{actual_options!r}")
    _write_uncaptured_line(capsys, "设备WLAN漫游灵敏度可选项符合用例预期")

def run_wlan_roam_sensitivity_custom_dialog_case(settings_ui, capsys) -> None:
    sensitivity_ui = WiFiAdvancedSettingsUI(settings_ui)
    dialog_texts = sensitivity_ui.current_wlan_roam_sensitivity_custom_dialog()
    if dialog_texts is None:
        sensitivity_ui.open()
        sensitivity_ui.open_wlan_roam_sensitivity_selector()
        dialog_texts = sensitivity_ui.open_wlan_roam_sensitivity_custom_dialog()
    prompt, input_hint = dialog_texts
    message = (
        f"设备WLAN漫游灵敏度自定义选项弹出提示框显示\"{prompt}\"，"
        f"\n编辑框内显示\"{input_hint}\""
    )
    if not sensitivity_ui.wlan_roam_sensitivity_custom_dialog_matches(
        prompt, input_hint
    ):
        _write_uncaptured_line(capsys, f"{message}，不符合用例预期")
        pytest.fail(f"{message}，不符合用例预期")
    _write_uncaptured_line(capsys, f"{message}，符合用例预期")

def run_wlan_roam_sensitivity_reboot_persistence_case(wifi, settings_ui, capsys) -> None:
    _assert_wlan_roam_sensitivity_persists(
        settings_ui,
        capsys,
        lambda: reboot_and_wait(wifi),
        "设备关机重启，WLAN漫游灵敏度设置不变，符合用例预期",
        "设备关机重启后，WLAN漫游灵敏度设置发生改变，不符合用例预期",
    )

def run_wlan_roam_sensitivity_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_sensitivity_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_settings(settings_ui),
        "设备关开WLAN开关，WLAN漫游灵敏度设置不变，符合用例预期",
        "设备关开WLAN开关后，WLAN漫游灵敏度设置发生改变，不符合用例预期",
    )

def run_wlan_roam_sensitivity_quick_settings_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_sensitivity_persists(
        settings_ui,
        capsys,
        lambda: _toggle_wlan_from_quick_settings(settings_ui),
        "设备快速设置栏关开WLAN开关，WLAN漫游灵敏度设置不变，符合用例预期",
        "设备快速设置栏关开WLAN开关后，WLAN漫游灵敏度设置发生改变，不符合用例预期",
    )

def run_wlan_roam_sensitivity_airplane_toggle_persistence_case(settings_ui, capsys) -> None:
    _assert_wlan_roam_sensitivity_persists(
        settings_ui,
        capsys,
        lambda: _toggle_airplane_mode_from_settings(settings_ui),
        "设备关开飞行模式，WLAN漫游灵敏度设置不变，符合用例预期",
        "设备关开飞行模式后，WLAN漫游灵敏度设置发生改变，不符合用例预期",
    )
