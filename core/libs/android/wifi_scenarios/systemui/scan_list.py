"""SystemUI WiFi scan-list workflows."""
from __future__ import annotations

import re
import time
from typing import Any, Callable, cast
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import (
    assert_dual_wifi_connected,
    assert_wifi_connected,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import scan_result_capabilities
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.scan_profiles import scan_profile_entry
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    assert_ssid_visible_in_scan,
)
from core.libs.android.systemui_pages.quick_settings_page import (
    capture_systemui,
    open_internet_dialog,
)
from core.libs.android.wifi_scenarios.systemui.scan_assertions import (
    visible_systemui_ssids,
    wait_systemui_ssid,
)
from core.libs.android.settings_pages.connection_config_page import WiFiConnectionConfigUI
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import (
    dual_wifi_ssids,
    get_dual_wifi_entry,
)


_SCAN_ENCODING_PROFILES = {
    1: "ssid_utf8_chinese_10",
    2: "ssid_gbk_chinese_16",
    3: "ssid_shift_jis_japanese_16",
    4: "ssid_cp949_korean",
}
_SCAN_DEFAULT_PROFILE = "scanner_default"


def configure_scan_ap(
    wifi_ap_action,
    entry: WiFiEntry,
    *,
    security: str = "wpa2-aes",
    band: str = "5g",
) -> str:
    ssid = str(entry.get("ssid") or "")
    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=str(entry.get("pwd") or ""),
        security=security,
        band=band,
        ssid_encoding=str(entry.get("ssid_encoding") or "utf-8"),
        verify=True,
    )
    return ssid


def connect_from_systemui(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    entry: WiFiEntry,
    *,
    encrypted: bool,
) -> None:
    ssid = str(entry.get("ssid") or "")
    config_ui = WiFiConnectionConfigUI(settings_ui)
    wifi.clear_saved_networks()
    config_ui.open_for_ssid(ssid, lambda: open_internet_dialog(settings_ui))
    if encrypted:
        config_ui.require_dialog(ssid)
        config_ui.set_password(str(entry.get("pwd") or ""))
        config_ui.save()
    elif config_ui.dialog_exists():
        config_ui.cancel()
        pytest.fail(f"{summary}: 开放网络不应弹出连接配置框")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)


def assert_dual_rows(
    summary: str,
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> tuple[dict, list[str]]:
    entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
    if not entry:
        pytest.skip(f"{summary}: 缺少 dual_wifi_24g_hyperwifi_us 配置")
    connected = assert_dual_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        hyper_region="US",
        entry_id="dual_wifi_24g_hyperwifi_us",
        failure_label="systemui_scan_list",
    )
    open_internet_dialog(settings_ui, capture=False)
    hierarchy = capture_systemui(settings_ui, "scan_list_dual_wifi")
    missing = [ssid for ssid in dual_wifi_ssids(entry) if ssid not in hierarchy]
    if missing:
        pytest.fail(f"{summary}: SystemUI 未显示双 WiFi 条目 {missing!r}")
    return entry, connected


@allure.step("执行 SystemUI 扫描列表验证")
def run_systemui_scan_list_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any = None,
) -> None:
    """Execute AP-backed SystemUI ScanList cases without manual phases."""
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"ScanList_(UI|Excp|Int)_(\d{3})$", summary)
    if not match:
        raise ValueError(f"未知 SystemUI ScanList 用例: {summary}")
    group, number_text = match.groups()
    number = int(number_text)

    if group == "UI" and number == 12:
        from core.libs.android.wifi_scenarios.systemui.navigation import (
            run_systemui_ssid_order_case,
        )

        run_systemui_ssid_order_case(summary, run_shell_cmd, settings_ui)
        return
    if group == "Int" and number in range(2, 7):
        entry, _ = assert_dual_rows(summary, wifi, wifi_yaml, run_shell_cmd, settings_ui)
        if number in (3, 4):
            link = "传统 WiFi" if number == 3 else "HyperWiFi"
            pytest.skip(
                f"{summary}: 已验证双链路基线；缺少可独立控制的第二{link} "
                "SSID 配置，无法执行真实切换"
            )
        if number in (5, 6):
            key = "traditional_wifi" if number == 5 else "hyper_wifi"
            target = str((entry.get(key) or {}).get("ssid") or "")
            other_key = "hyper_wifi" if number == 5 else "traditional_wifi"
            survivor = str((entry.get(other_key) or {}).get("ssid") or "")
            targets = wifi.forget_targets_for_connected_ssids([target])
            if not targets:
                pytest.skip(f"{summary}: 无法解析 {target!r} 的 network id")
            for network_id, _ in targets:
                wifi.forget_network(network_id)
            time.sleep(5.0)
            connected = wifi.list_connected_ssids(trust_status_fallback=True)
            if target in connected or survivor not in connected:
                pytest.fail(
                    f"{summary}: 单链路断开后状态错误，断开={target!r}，"
                    f"保留={survivor!r}，实际={connected!r}"
                )
            open_internet_dialog(settings_ui)
        return

    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    profile_id = (
        _SCAN_ENCODING_PROFILES[number]
        if group == "Excp" and number in _SCAN_ENCODING_PROFILES
        else _SCAN_DEFAULT_PROFILE
    )
    entry = scan_profile_entry(wifi_yaml, profile_id, summary)
    ssid = str(entry.get("ssid") or "")
    try:
        previous_ssid = ""
        if group == "UI" and number in (5, 10):
            previous_ssid = assert_wifi_connected(
                wifi, wifi_yaml, run_shell_cmd, allow_any_configured=True
            )
            if previous_ssid == ssid:
                pytest.skip(f"{summary}: 缺少不同于目标 {ssid!r} 的原连接 SSID")

        if group == "Int" and number == 1:
            insecure_ssid = "PyAutoTest_SystemUI_Open"
            insecure_entry = cast(
                WiFiEntry,
                {**entry, "ssid": insecure_ssid, "pwd": "", "encrypt": "OPEN"},
            )
            configure_scan_ap(wifi_ap_action, insecure_entry, security="open")
            time.sleep(5.0)
            run_shell_cmd("cmd wifi start-scan")
            time.sleep(3.0)
            open_internet_dialog(settings_ui, capture=False)
            if insecure_ssid in visible_systemui_ssids(settings_ui):
                pytest.fail(f"{summary}: 金融安全模式仍显示开放网络 {insecure_ssid!r}")
            configure_scan_ap(wifi_ap_action, entry)
            time.sleep(5.0)
            run_shell_cmd("cmd wifi start-scan")
            time.sleep(3.0)
            open_internet_dialog(settings_ui, capture=False)
            wait_systemui_ssid(settings_ui, ssid, present=True, timeout=5.0)
            return

        if group == "UI" and number == 2:
            open_internet_dialog(settings_ui, capture=False)
            configure_scan_ap(wifi_ap_action, entry)
            wait_systemui_ssid(settings_ui, ssid, present=True, timeout=12.0)
            capture_systemui(settings_ui, "scan_list_periodic_refresh")
            return

        configure_scan_ap(
            wifi_ap_action,
            entry,
            security="open" if group == "UI" and number == 9 else "wpa2-aes",
            band="both" if group == "UI" and number == 11 else "5g",
        )
        time.sleep(5.0)
        assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)

        if group == "UI" and number in (3, 4):
            open_internet_dialog(settings_ui, capture=False)
            wait_systemui_ssid(settings_ui, ssid, present=True, timeout=5.0)
            if number == 4:
                wifi_ap_action.teardown_wifi()
                wait_systemui_ssid(settings_ui, ssid, present=False, timeout=15.0)
            return
        if group == "UI" and number == 11:
            open_internet_dialog(settings_ui, capture=False)
            visible = wait_systemui_ssid(settings_ui, ssid, present=True, timeout=5.0)
            if visible.count(ssid) != 1:
                pytest.fail(f"{summary}: 同名双频 SSID 应仅显示一次，实际={visible!r}")
            return
        if group == "UI" and number in (8, 9) or group == "Excp":
            connect_from_systemui(
                summary,
                run_shell_cmd,
                wifi,
                wifi_yaml,
                settings_ui,
                entry,
                encrypted=not (group == "UI" and number == 9),
            )
            return

        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        if group == "UI" and number == 6:
            if not wifi.disconnect_all(post_wait_sec=2.0):
                pytest.fail(f"{summary}: 手动断开后仍存在 WLAN 连接")
            open_internet_dialog(settings_ui, capture=False)
            wait_systemui_ssid(settings_ui, ssid, present=True, timeout=5.0)
            return
        if group == "UI" and number == 7:
            wifi_ap_action.teardown_wifi()
            deadline = time.monotonic() + 10.0
            while time.monotonic() < deadline:
                if ssid not in wifi.list_connected_ssids(trust_status_fallback=True):
                    break
                time.sleep(1.0)
            else:
                pytest.fail(f"{summary}: AP 关闭 10s 后仍连接 {ssid!r}")
            open_internet_dialog(settings_ui, capture=False)
            wait_systemui_ssid(settings_ui, ssid, present=False, timeout=10.0)
            return
        if group == "UI" and number in (5, 10):
            open_internet_dialog(settings_ui, capture=False)
            hierarchy = capture_systemui(settings_ui, f"scan_list_switch_{number:03d}")
            if ssid not in hierarchy:
                pytest.fail(f"{summary}: 切换连接后 SystemUI 未显示 {ssid!r}")
            connected = wifi.list_connected_ssids(trust_status_fallback=True)
            if ssid not in connected or previous_ssid in connected:
                pytest.fail(
                    f"{summary}: SSID 切换状态错误，原={previous_ssid!r}，"
                    f"目标={ssid!r}，当前={connected!r}"
                )
            return
        raise ValueError(f"未实现的 SystemUI ScanList 用例: {summary}")
    finally:
        wifi_ap_action.teardown_wifi()


@allure.step("执行 SystemUI 默认扫描列表验证")
def run_systemui_scan_list_default_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> None:
    """Validate SSID, signal icon, and security icon for visible scan rows."""
    attach_wifi_status(summary, run_shell_cmd)
    run_shell_cmd("cmd wifi start-scan")
    time.sleep(3.0)
    scan_blob = run_shell_cmd("cmd wifi list-scan-results")
    open_internet_dialog(settings_ui)
    root = ElementTree.fromstring(settings_ui.device.dump_hierarchy())
    items = [
        node
        for node in root.iter("node")
        if node.get("resource-id") == "com.android.systemui:id/wifi_list"
    ]
    if not items:
        settings_ui.fail_with_artifacts(f"{summary}: SystemUI WLAN 扫描列表为空")

    checked = []
    for item in items:
        titles = [
            node.get("text", "").strip()
            for node in item.iter("node")
            if node.get("resource-id") == "com.android.systemui:id/wifi_title"
            and node.get("text", "").strip()
        ]
        if len(titles) != 1:
            pytest.fail(f"{summary}: WLAN 条目未显示唯一 SSID，实际={titles!r}")
        ssid = titles[0]
        resource_ids = {node.get("resource-id", "") for node in item.iter("node")}
        if "com.android.systemui:id/wifi_icon" not in resource_ids:
            pytest.fail(f"{summary}: SSID {ssid!r} 未显示信号质量图标")
        capabilities = scan_result_capabilities(scan_blob, ssid)
        if capabilities:
            encrypted = any(
                token in capability.upper()
                for capability in capabilities
                for token in ("WEP", "WPA", "SAE", "EAP")
            )
            has_lock = "com.android.systemui:id/wifi_end_icon" in resource_ids
            if has_lock != encrypted:
                pytest.fail(
                    f"{summary}: SSID {ssid!r} 加密图标不匹配，"
                    f"capabilities={capabilities!r}, has_lock={has_lock}"
                )
        checked.append(ssid)
    print(f"[{summary}] 已校验 {len(checked)} 个可见 WLAN 条目: {checked!r}")
    capture_systemui(settings_ui, "scan_list_default")
