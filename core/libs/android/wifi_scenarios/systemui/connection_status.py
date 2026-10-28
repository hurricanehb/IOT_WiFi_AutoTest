"""SystemUI WiFi connection-status scenarios."""
from __future__ import annotations

import re
import time
from typing import Any, Callable

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import (
    assert_dual_wifi_connected,
    assert_wifi_connected,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.scan_profiles import scan_profile_entry
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    assert_ssid_visible_in_scan,
)
from core.libs.android.systemui_pages.quick_settings_page import (
    capture_systemui,
    open_internet_dialog,
)
from core.libs.android.wifi_scenarios.systemui.scan_list import configure_scan_ap
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry


_NO_INTERNET_STATUS_TEXTS = (
    "无法提供互联网连接",
    "无法访问互联网",
    "No internet access",
    "No internet",
)
_WRONG_PASSWORD_STATUS_TEXTS = (
    "请检查密码",
    "密码不正确",
    "身份验证出现问题",
    "Check password",
    "Authentication problem",
    "已保存",
    "Saved",
)
_SCAN_DEFAULT_PROFILE = "scanner_default"


def assert_systemui_text(
    summary: str,
    hierarchy: str,
    candidates: tuple[str, ...],
    *,
    present: bool,
    label: str,
) -> None:
    folded = hierarchy.casefold()
    hits = [text for text in candidates if text.casefold() in folded]
    if present and not hits:
        pytest.fail(f"{summary}: SystemUI 未显示{label}，候选={candidates!r}")
    if not present and hits:
        pytest.fail(f"{summary}: SystemUI 不应显示{label}，实际命中={hits!r}")


def assert_systemui_connected_state(
    summary: str,
    settings_ui: AndroidSettingsUI,
    ssids: list[str],
    *,
    internet: bool,
) -> str:
    open_internet_dialog(settings_ui, capture=False)
    hierarchy = capture_systemui(settings_ui, "connstat_systemui")
    missing = [ssid for ssid in ssids if ssid and ssid not in hierarchy]
    if missing:
        pytest.fail(f"{summary}: SystemUI 未显示已连接网络 {missing!r}")
    if "com.android.systemui:id/wifi_connected_layout" not in hierarchy:
        pytest.fail(f"{summary}: SystemUI 未显示已连接网络布局")
    assert_systemui_text(
        summary,
        hierarchy,
        _NO_INTERNET_STATUS_TEXTS,
        present=not internet,
        label="无互联网状态",
    )
    return hierarchy


@allure.step("执行 SystemUI 连接状态验证")
def run_systemui_conn_status_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any = None,
) -> None:
    """Execute ConnStat cases fully controllable by the current lab APIs."""
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"ConnStat_(UI|Int)_(\d{3})$", summary)
    if not match:
        raise ValueError(f"未知 SystemUI ConnStat 用例: {summary}")
    group, number_text = match.groups()
    number = int(number_text)

    if group == "Int":
        if number not in (2, 4, 6):
            raise ValueError(f"当前能力未实现的 SystemUI ConnStat 用例: {summary}")
        entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
        if not entry:
            pytest.skip(f"{summary}: 缺少 dual_wifi_24g_hyperwifi_us 配置")
        connected = assert_dual_wifi_connected(
            wifi,
            wifi_yaml,
            run_shell_cmd,
            hyper_region="US",
            entry_id="dual_wifi_24g_hyperwifi_us",
            failure_label="systemui_connstat",
        )
        if number == 2:
            assert_systemui_connected_state(
                summary, settings_ui, connected, internet=True
            )
            return
        key = "traditional_wifi" if number == 4 else "hyper_wifi"
        target = str((entry.get(key) or {}).get("ssid") or "")
        survivor_key = "hyper_wifi" if key == "traditional_wifi" else "traditional_wifi"
        survivor = str((entry.get(survivor_key) or {}).get("ssid") or "")
        targets = wifi.forget_targets_for_connected_ssids([target])
        if not targets:
            pytest.skip(f"{summary}: 无法解析 {target!r} 的 network id")
        for network_id, _ in targets:
            wifi.forget_network(network_id)
        time.sleep(5.0)
        current = wifi.list_connected_ssids(trust_status_fallback=True)
        if target in current or survivor not in current:
            pytest.fail(
                f"{summary}: 单链路移除后状态错误，目标={target!r}，"
                f"保留={survivor!r}，当前={current!r}"
            )
        if target in wifi.list_saved_networks():
            pytest.fail(f"{summary}: 取消保存后仍存在网络 {target!r}")
        assert_systemui_connected_state(
            summary, settings_ui, [survivor], internet=True
        )
        return

    if number not in (1, 4, 6):
        raise ValueError(f"当前能力未实现的 SystemUI ConnStat 用例: {summary}")
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    entry = scan_profile_entry(wifi_yaml, _SCAN_DEFAULT_PROFILE, summary)
    target = str(entry.get("ssid") or "")
    try:
        configure_scan_ap(wifi_ap_action, entry)
        assert_ssid_visible_in_scan(run_shell_cmd, target, summary=summary)
        if number == 4:
            wifi.clear_saved_networks()
            wifi.connect_wpa2(target, "wrong_pwd_00000")
            time.sleep(20.0)
            if target in wifi.list_connected_ssids(trust_status_fallback=True):
                pytest.fail(f"{summary}: 错误密码却连接成功 {target!r}")
            open_internet_dialog(settings_ui, capture=False)
            hierarchy = capture_systemui(settings_ui, "connstat_wrong_password")
            assert_systemui_text(
                summary,
                hierarchy,
                _WRONG_PASSWORD_STATUS_TEXTS,
                present=True,
                label="密码错误/已保存状态",
            )
            wifi.clear_saved_networks()
            return

        connected = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        assert_systemui_connected_state(summary, settings_ui, [connected], internet=True)
        if number == 6:
            if not wifi.disconnect_all(post_wait_sec=2.0):
                pytest.fail(f"{summary}: 断开后仍存在 WLAN 连接")
            open_internet_dialog(settings_ui, capture=False)
            hierarchy = capture_systemui(settings_ui, "connstat_disconnected")
            if "com.android.systemui:id/wifi_connected_layout" in hierarchy:
                pytest.fail(f"{summary}: 断开后 SystemUI 仍显示已连接布局")
    finally:
        wifi_ap_action.teardown_wifi()
