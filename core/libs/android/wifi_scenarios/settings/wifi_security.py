"""SettingsUI scenarios for WiFi security filtering."""
from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import Any

import pytest

from core.libs.android.wifi_scenarios.lab_requirements import env_value, require_env_value
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.settings._helpers import visible_ssids
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI
from core.utils.log_handler import get_logger

log = get_logger(__name__)


def run_wifi_security_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    scan_wait_sec: float = 6.0,
) -> None:
    """WifiSec_Vali_001：关闭 WiFi 安全后，弱加密网络恢复显示。"""
    require_env_value(
        "WIFISEC_SWITCH",
        "off",
        summary,
        hint="请在 安全-安全中心-WiFi安全 关闭开关后设置 WIFISEC_SWITCH=off",
    )
    weak_ssid = env_value("WIFISEC_WEAK_SSID")
    if not weak_ssid:
        pytest.skip(f"{summary}: 需设置 WIFISEC_WEAK_SSID 指向 open/WEP 陪测 AP")

    if not wifi.set_wifi_enabled(True):
        pytest.fail(f"{summary}: 无法打开 WiFi 射频")

    ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
    print(f"[{summary}] 扫描到 {len(ssids)} 个 SSID: {ssids[:15]!r}")
    if not any(name.lower() == weak_ssid.lower() for name in ssids):
        pytest.fail(
            f"{summary}: WiFi 安全关闭后弱加密网络 {weak_ssid!r} 仍未显示；"
            f"扫描结果={ssids[:15]!r}"
        )
    log.info("%s: 弱加密网络 %r 已在扫描列表中显示", summary, weak_ssid)


def run_wifi_security_filter_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_ap_action: Any,
    *,
    insecure_security: str,
    scan_wait_sec: float = 6.0,
    settle_sec: float = 5.0,
) -> None:
    """WiFiSec_Vali_002/003：过滤弱加密网络，但显示同 SSID 的 WPA2 网络。"""
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")

    security = insecure_security.strip().lower()
    if security not in ("open", "wep40"):
        raise ValueError(f"不支持的弱加密方式: {insecure_security!r}")

    ssid = f"PyAutoTest_WifiSec_{'Open' if security == 'open' else 'WEP'}"
    password = "" if security == "open" else "12345"
    if not wifi.set_wifi_enabled(True):
        pytest.fail(f"{summary}: 无法打开 WiFi 射频")

    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=password,
        security=security,
        band="5g",
        verify=True,
    )
    time.sleep(settle_sec)
    insecure_ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
    if any(name.lower() == ssid.lower() for name in insecure_ssids):
        pytest.fail(
            f"{summary}: WiFi 安全开启后仍显示 {security} 网络 {ssid!r}；"
            f"扫描结果={insecure_ssids[:15]!r}"
        )

    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password="24681357",
        security="wpa2-aes",
        band="5g",
        verify=True,
    )
    time.sleep(settle_sec)
    secure_ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
    if not any(name.lower() == ssid.lower() for name in secure_ssids):
        pytest.fail(
            f"{summary}: AP 改为 WPA2 后未显示网络 {ssid!r}；"
            f"扫描结果={secure_ssids[:15]!r}"
        )
    log.info("%s: 已验证 %s 网络过滤及 WPA2 网络恢复显示", summary, security)


def run_wifi_security_option_absent_case(
    summary: str,
    add_network_ui: WiFiAddNetworkUI,
    *,
    forbidden_options: Sequence[str],
) -> None:
    """WiFiSec_Vali_009/010：WiFi 安全开启时不提供弱安全类型。"""
    add_network_ui.open()
    try:
        options = add_network_ui.security_options()
        print(f"[{summary}] 添加网络安全性选项: {options!r}")
        if not options:
            pytest.fail(f"{summary}: 未读取到任何添加网络安全性选项")
        normalized = {option.casefold() for option in options}
        forbidden = {option.casefold() for option in forbidden_options}
        found = sorted(normalized & forbidden)
        if found:
            pytest.fail(f"{summary}: 安全性列表不应包含弱安全选项 {found!r}")
    finally:
        add_network_ui.cancel()
