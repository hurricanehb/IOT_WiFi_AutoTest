"""Settings saved-network list scenarios."""

from __future__ import annotations

from collections.abc import Callable, Sequence
import re
import time

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import ssid_match
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_wifi_list_entry


SAVED_NETWORKS_TEXTS = ("已保存的网络", "已保存网络", "Saved networks")
FORGET_TEXTS = ("取消保存", "忘记", "Forget")
WRONG_PASSWORD_TEXTS = (
    "请检查密码",
    "密码不正确",
    "身份验证出现问题",
    "Check password",
    "Authentication problem",
)


def contains_any_text(hierarchy: str, candidates: Sequence[str]) -> bool:
    normalized = (hierarchy or "").casefold()
    return any(candidate.casefold() in normalized for candidate in candidates)


def _entry(summary: str, wifi_yaml: dict) -> dict[str, str]:
    entry = get_wifi_list_entry(
        wifi_yaml,
        entry_id="wifi_signal_level_traditional_ap1",
    )
    if not entry:
        pytest.skip(f"{summary}: 缺少 wifi_signal_level_traditional_ap1 测试数据")
    return entry


def _click_first_text(
    settings_ui: AndroidSettingsUI,
    candidates: Sequence[str],
    *,
    error: str,
) -> str:
    for text in candidates:
        if settings_ui.device(text=text).click_exists(timeout=2.0):
            return text
    settings_ui.fail_with_artifacts(error)
    return ""


def _wifi_hierarchy(settings_ui: AndroidSettingsUI) -> str:
    settings_ui.open_wifi_settings()
    time.sleep(3.0)
    return settings_ui.device.dump_hierarchy()


def _find_saved_networks_entry(settings_ui: AndroidSettingsUI) -> str:
    for text in SAVED_NETWORKS_TEXTS:
        if settings_ui.device(text=text).exists:
            return text
        scrollable = settings_ui.device(scrollable=True)
        if scrollable.exists and scrollable.scroll.to(text=text):
            return text
    return ""


def _open_saved_networks(
    summary: str,
    settings_ui: AndroidSettingsUI,
) -> str:
    settings_ui.open_wifi_settings()
    time.sleep(3.0)
    entry_text = _find_saved_networks_entry(settings_ui)
    if not entry_text:
        settings_ui.fail_with_artifacts(f"{summary}: WLAN 页未显示“已保存的网络”入口")
    if not settings_ui.device(text=entry_text).click_exists(timeout=3.0):
        settings_ui.fail_with_artifacts(f"{summary}: 无法点击“已保存的网络”入口")
    time.sleep(2.0)
    return settings_ui.device.dump_hierarchy()


def _assert_saved_ssid(
    summary: str,
    settings_ui: AndroidSettingsUI,
    ssid: str,
) -> str:
    hierarchy = _open_saved_networks(summary, settings_ui)
    if not contains_any_text(hierarchy, (ssid,)):
        settings_ui.fail_with_artifacts(
            f"{summary}: 已保存网络列表中未找到 {ssid!r}"
        )
    return hierarchy


@allure.step("执行隐藏网络保存验证")
def run_saved_hidden_network_case(
    case: dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    add_network_ui,
    wifi_ap_action,
) -> None:
    from core.libs.android.wifi_scenarios.ap_configuration import (
        run_wifi_ap_manual_add_security_case,
    )

    summary = case["case_id"]
    run_wifi_ap_manual_add_security_case(
        case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        add_network_ui,
        wifi_ap_action,
        security="wpa2-aes",
        ui_security="personal",
        hidden=True,
        ui_hidden=True,
    )
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    if not connected:
        pytest.fail(f"{summary}: 添加隐藏网络后未连接")
    _assert_saved_ssid(summary, add_network_ui.settings, connected[0])


def _assert_internet_reachable(
    summary: str,
    run_shell_cmd: Callable[[str], str],
) -> None:
    output = run_shell_cmd("ping -c 2 -W 3 www.baidu.com")
    allure.attach(output, "ping www.baidu.com", allure.attachment_type.TEXT)
    if not re.search(r"(?:0% packet loss|2 (?:packets )?received)", output, re.I):
        pytest.fail(f"{summary}: 已连接网络无法 ping 通外网\n{output[:800]}")


@allure.step("执行已保存网络列表验证")
def run_saved_network_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"SavedNet_Vali_(00[12578])$", summary)
    if match is None:
        raise ValueError(f"未知 SavedNet 自动化用例: {summary}")
    number = int(match.group(1))

    if number == 1:
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        settings_ui.open_wifi_settings()
        time.sleep(3.0)
        if _find_saved_networks_entry(settings_ui):
            settings_ui.fail_with_artifacts(
                f"{summary}: 无保存网络时仍显示“已保存的网络”入口"
            )
        return

    entry = _entry(summary, wifi_yaml)
    ssid = str(entry.get("ssid") or "")

    if number == 5:
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        wifi.connect_wpa2(ssid, "wrong_pwd_00000")
        time.sleep(15.0)
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if any(ssid_match(ssid, current) for current in connected):
            pytest.fail(f"{summary}: 错误密码不应连接成功，当前={connected!r}")
        hierarchy = _assert_saved_ssid(summary, settings_ui, ssid)
        if not contains_any_text(hierarchy, WRONG_PASSWORD_TEXTS):
            settings_ui.fail_with_artifacts(
                f"{summary}: 保存项未显示密码错误提示"
            )
        return

    connected_ssid = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=entry,
    )
    if number in (2, 7):
        _assert_internet_reachable(summary, run_shell_cmd)

    if number == 2:
        _assert_saved_ssid(summary, settings_ui, connected_ssid)
        return

    if number == 7:
        _assert_saved_ssid(summary, settings_ui, connected_ssid)
        if not settings_ui.device(text=connected_ssid).click_exists(timeout=5.0):
            settings_ui.fail_with_artifacts(
                f"{summary}: 无法从保存列表打开 {connected_ssid!r}"
            )
        time.sleep(2.0)
        _click_first_text(
            settings_ui,
            FORGET_TEXTS,
            error=f"{summary}: 保存网络详情未找到取消保存按钮",
        )
    else:
        settings_ui.open_wifi_settings()
        settings_ui.scroll_to_text(connected_ssid)
        settings_ui.click_text(connected_ssid)
        time.sleep(2.0)
        _click_first_text(
            settings_ui,
            FORGET_TEXTS,
            error=f"{summary}: 在线网络详情未找到取消保存按钮",
        )

    if not wifi.wait_until_disconnected(timeout=12.0):
        pytest.fail(f"{summary}: 取消保存后 WLAN 未断开")
    if any(ssid_match(connected_ssid, saved) for saved in wifi.list_saved_networks()):
        pytest.fail(f"{summary}: 取消保存后仍存在 {connected_ssid!r}")
