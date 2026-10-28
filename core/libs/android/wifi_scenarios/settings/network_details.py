"""Settings connected-network details scenarios."""
from __future__ import annotations

import re
import time
from typing import Callable, Sequence, cast

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.ip_configuration import (
    assert_wifi_link_details,
    collect_wifi_ipv4_info,
)

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import ssid_match
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry, get_wifi_list_entry

_CONNECTED_TEXTS = ("已连接", "Connected")
_SIGNAL_TEXTS = ("信号强度", "Signal strength", "极好", "良好", "较差", "Excellent", "Good", "Fair", "Poor")
_FREQUENCY_TEXTS = ("频率", "Frequency", "2.4 GHz", "2.4GHz", "5 GHz", "5GHz", "Sub-1G", "sub-1G")
_SECURITY_TEXTS = ("安全性", "Security", "WPA2", "WPA3", "开放", "Open")


def _contains_any(blob: str, candidates: Sequence[str]) -> bool:
    lower = blob.casefold()
    return any(candidate.casefold() in lower for candidate in candidates)


def _open_connected_network_details(
    summary: str,
    ssid: str,
    settings_ui: AndroidSettingsUI,
) -> str:
    settings_ui.open_wifi_settings()
    time.sleep(3.0)
    settings_ui.scroll_to_text(ssid)
    if not settings_ui.device(text=ssid).click_exists(timeout=5.0):
        settings_ui.fail_with_artifacts(f"{summary}: 无法点击已连接网络 {ssid!r}")
    time.sleep(2.0)
    hierarchy = settings_ui.device.dump_hierarchy()
    markers = ("网络详情", "Network details", "忘记", "Forget", "断开连接", "Disconnect")
    if not _contains_any(hierarchy, markers):
        settings_ui.fail_with_artifacts(f"{summary}: 点击 {ssid!r} 后未进入网络详情页")
    return hierarchy


def _assert_detail_field(
    summary: str,
    hierarchy: str,
    label: str,
    candidates: Sequence[str],
) -> None:
    if not _contains_any(hierarchy, candidates):
        pytest.fail(f"{summary}: 网络详情未显示{label}；候选={list(candidates)!r}")


def _network_details_entry(summary: str, wifi_yaml: dict) -> WiFiEntry:
    entry = cast(
        WiFiEntry,
        get_wifi_list_entry(
            wifi_yaml, entry_id="wifi_signal_level_traditional_ap1"
        ),
    )
    if not entry:
        pytest.skip(
            f"{summary}: 缺少 wifi_signal_level_traditional_ap1 测试数据"
        )
    return entry


def _click_first_text(
    summary: str,
    settings_ui: AndroidSettingsUI,
    candidates: Sequence[str],
) -> str:
    for text in candidates:
        if settings_ui.device(text=text).click_exists(timeout=2.0):
            return text
    settings_ui.fail_with_artifacts(
        f"{summary}: 网络详情未找到操作按钮 {list(candidates)!r}"
    )
    return ""


@allure.step("执行网络详情状态验证")
def run_network_details_status_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Validate connected state, signal, frequency, and security in details UI."""
    attach_wifi_status(summary, run_shell_cmd)
    entry = _network_details_entry(summary, wifi_yaml)
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    hierarchy = _open_connected_network_details(summary, ssid, settings_ui)

    _assert_detail_field(summary, hierarchy, "连接状态", _CONNECTED_TEXTS)
    _assert_detail_field(summary, hierarchy, "信号强度", _SIGNAL_TEXTS)
    _assert_detail_field(summary, hierarchy, "频率", _FREQUENCY_TEXTS)
    _assert_detail_field(summary, hierarchy, "安全性", _SECURITY_TEXTS)

    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    if not any(ssid_match(ssid, current) for current in connected):
        pytest.fail(f"{summary}: 打开网络详情后连接已丢失，当前={connected!r}")

    frequency = run_shell_cmd("cmd wifi status")
    if not re.search(
        r"frequency(?:Mhz)?\s*[:=]\s*\d+(?:MHz)?",
        frequency,
        re.IGNORECASE,
    ):
        pytest.fail(f"{summary}: cmd wifi status 未报告连接频率\n{frequency[:800]}")


@allure.step("执行高级网络详情验证")
def run_network_details_advanced_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    dual_entry = get_dual_wifi_entry(
        wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us"
    )
    hyper = dual_entry.get("hyper_wifi")
    if not isinstance(hyper, dict) or not hyper.get("ssid"):
        pytest.skip(f"{summary}: 缺少 HyperWiFi 网络详情测试数据")
    wifi.clear_saved_networks()
    if not wifi.connect_wifi_block(cast(WiFiEntry, hyper)):
        pytest.fail(f"{summary}: 无法连接 HyperWiFi {hyper.get('ssid')!r}")
    ssid = str(hyper["ssid"])
    _open_connected_network_details(summary, ssid, settings_ui)
    scrollable = settings_ui.device(scrollable=True)
    if not scrollable.exists or not scrollable.scroll.to(text="设备 MAC 地址"):
        settings_ui.fail_with_artifacts(f"{summary}: 无法滚动到高级网络详情")
    hierarchy = settings_ui.device.dump_hierarchy()
    for target in ("DNS", "传输链接速度", "接收链接速度"):
        if scrollable.scroll.to(text=target):
            hierarchy += settings_ui.device.dump_hierarchy()
    for label, candidates in (
        ("MAC 地址", ("MAC 地址", "MAC address")),
        ("IP 地址", ("IP 地址", "IP address")),
        ("网关", ("网关", "Gateway")),
        ("前缀长度/子网掩码", ("前缀长度", "子网掩码", "Prefix length", "Subnet mask")),
        ("DNS", ("DNS",)),
        ("链接速率", ("链接速度", "链接速率", "Link speed")),
    ):
        _assert_detail_field(summary, hierarchy, label, candidates)
    info = collect_wifi_ipv4_info(run_shell_cmd)
    assert_wifi_link_details(run_shell_cmd, info)


@allure.step("执行忘记网络验证")
def run_network_details_forget_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Forget the connected network from Settings and verify disconnection."""
    attach_wifi_status(summary, run_shell_cmd)
    entry = _network_details_entry(summary, wifi_yaml)
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    _open_connected_network_details(summary, ssid, settings_ui)
    _click_first_text(summary, settings_ui, ("取消保存", "忘记", "Forget"))
    if not wifi.wait_until_disconnected(timeout=10.0):
        pytest.fail(f"{summary}: 点击取消保存后 WLAN 仍保持连接")
    if any(ssid_match(ssid, saved) for saved in wifi.list_saved_networks()):
        pytest.fail(f"{summary}: 点击取消保存后网络仍在保存列表: {ssid!r}")


@allure.step("执行网络密码编辑验证")
def run_network_details_edit_password_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Change the saved password through Settings and verify disconnection."""
    attach_wifi_status(summary, run_shell_cmd)
    entry = _network_details_entry(summary, wifi_yaml)
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    _open_connected_network_details(summary, ssid, settings_ui)

    edit = settings_ui.device(description="修改")
    if not edit.click_exists(timeout=3.0):
        edit = settings_ui.device(descriptionMatches=r"(?i)^(Edit|Modify)$")
        if not edit.click_exists(timeout=3.0):
            settings_ui.fail_with_artifacts(f"{summary}: 网络详情未找到修改按钮")

    password = settings_ui.device(resourceId="com.android.settings:id/password")
    if not password.wait(timeout=5.0):
        settings_ui.fail_with_artifacts(f"{summary}: 修改网络对话框未显示密码输入框")
    password.clear_text()
    password.set_text("wrong_pwd_00000")
    save = settings_ui.device(resourceId="android:id/button1")
    if not save.click_exists(timeout=3.0):
        _click_first_text(summary, settings_ui, ("保存", "Save"))
    if not wifi.wait_until_disconnected(timeout=15.0):
        pytest.fail(f"{summary}: 修改为错误密码后已连接 WLAN 未断开")


@allure.step("执行断开重连验证")
def run_network_details_disconnect_reconnect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Disconnect and reconnect the saved network through Settings UI."""
    attach_wifi_status(summary, run_shell_cmd)
    entry = _network_details_entry(summary, wifi_yaml)
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    _open_connected_network_details(summary, ssid, settings_ui)
    _click_first_text(summary, settings_ui, ("断开连接", "Disconnect"))
    if not wifi.wait_until_disconnected(timeout=10.0):
        pytest.fail(f"{summary}: 点击断开连接后 WLAN 仍保持连接")

    settings_ui.open_wifi_settings()
    settings_ui.scroll_to_text(ssid)
    settings_ui.click_text(ssid)
    deadline = time.monotonic() + 15.0
    while time.monotonic() < deadline:
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if any(ssid_match(ssid, current) for current in connected):
            return
        time.sleep(0.5)
    pytest.fail(f"{summary}: 点击已保存网络后未重新连接 {ssid!r}")