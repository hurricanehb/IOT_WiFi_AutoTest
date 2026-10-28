"""Android hotspot defaults scenarios."""
from __future__ import annotations

import pytest

from core.libs.android.softap_control import SoftAPControl
from core.libs.android.wifi_scenarios.hotspot._helpers import _write_uncaptured_line


def run_hotspot_default_switch_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    hotspot_enabled = softap.is_hotspot_enabled()
    assert not hotspot_enabled, "WLAN热点开关默认应为关闭，实际已被打开"

    _write_uncaptured_line(capsys, "WLAN热点开关默认关闭")


def run_hotspot_default_security_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    security = softap.security_summary()
    expected_security = "WPA2/WPA3-Personal"
    result = (
        f'设备热点安全性默认显示为"{expected_security}"'
        if security == expected_security
        else f'设备热点安全性显示为"{security}"，不符合用例预期。'
    )
    _write_uncaptured_line(capsys, result)
    assert security == expected_security, result


def run_hotspot_default_band_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    compatibility = softap.compatibility_summary()
    expected_band = "2.4GHz"
    result = (
        f'设备热点默认频段为"{expected_band}"'
        if expected_band in compatibility
        else f'设备热点默认频段显示不是"{expected_band}"，不符合用例预期。'
    )
    _write_uncaptured_line(capsys, result)
    assert expected_band in compatibility, result


def run_hotspot_default_auto_shutdown_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    auto_shutdown_enabled = softap.is_auto_shutdown_enabled()
    result = (
        '设备热点"自动关闭热点"开关默认已打开'
        if auto_shutdown_enabled
        else '设备热点"自动关闭热点"开关被关闭，不符合用例预期。'
    )
    _write_uncaptured_line(capsys, result)
    assert auto_shutdown_enabled, result


def run_hotspot_security_editor_default_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    try:
        if not softap.is_security_editor_open():
            softap.open_settings()
        _, selected = softap.open_security_editor()
    except (AssertionError, RuntimeError, ValueError) as error:
        result = f'设备热点未能打开或读取"安全性"页面：{error}'
        _write_uncaptured_line(capsys, result)
        pytest.fail(result, pytrace=False)

    expected_security = "WPA2/WPA3-Personal"
    result = (
        '设备热点已进入"安全性"页面,选中WPA2/WPA3-Personal,符合用例预期'
        if selected == expected_security
        else f'设备热点安全性选中"{selected}"加密方式，不符合用例预期。'
    )
    _write_uncaptured_line(capsys, result)
    if selected != expected_security:
        pytest.fail(result, pytrace=False)


def run_hotspot_security_options_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    if not softap.is_security_editor_open():
        softap.open_settings()
    options, selected = softap.open_security_editor()
    expected_options = [
        "WPA3-Personal",
        "WPA2/WPA3-Personal",
        "WPA2-Personal",
        "无",
    ]
    options_match = options == expected_options
    result = (
        '设备热点"安全性页面"选项情况符合用例预期'
        if selected == "WPA2/WPA3-Personal"
        else "设备热点安全性页面选项符合用例预期，但选中不是默认的WPA2/WPA3-Personal，请关注该情况是否正常"
    ) if options_match else '设备热点"安全性页面"选项情况不符合用例预期'
    _write_uncaptured_line(capsys, result)
    assert options_match, result


def run_hotspot_band_editor_default_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    _, selected = softap.open_compatibility_editor()
    expected_band = "2.4GHz"
    result = (
        '设备热点"AP频段"默认选中2.4GHz符合用例预期'
        if selected == expected_band
        else f'设备热点"AP频段"默认选中{selected or "未识别"}不符合用例预期'
    )
    _write_uncaptured_line(capsys, result)
    assert selected == expected_band, result


def run_hotspot_band_options_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    options, selected = softap.open_compatibility_editor()
    expected_options = ["2.4GHz", "5GHz"]
    options_match = options == expected_options
    result = (
        '设备热点"AP频段"选项情况符合用例预期'
        if selected == "2.4GHz"
        else "设备热点\"AP频段\"选项符合用例预期，但选中不是默认的2.4GHz，请关注该情况是否正常"
    ) if options_match else '设备热点"AP频段"选项情况不符合用例预期'
    _write_uncaptured_line(capsys, result)
    assert options_match, result
