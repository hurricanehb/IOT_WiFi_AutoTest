"""SystemUI WiFi encryption-icon scenarios."""
from __future__ import annotations

import os
import re
from typing import Any, Callable
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.ssid_parsers import scan_result_capabilities
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    assert_ssid_visible_in_scan,
)
from core.libs.android.systemui_pages.quick_settings_page import (
    capture_systemui,
    open_internet_dialog,
)
from core.libs.android.wifi_scenarios.systemui.scan_assertions import (
    visible_systemui_ssids,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


def assert_encryption_icon(
    summary: str,
    settings_ui: AndroidSettingsUI,
    scan_blob: str,
    ssid: str,
    *,
    encrypted: bool,
) -> None:
    root = ElementTree.fromstring(settings_ui.device.dump_hierarchy())
    matching_rows = []
    for item in root.iter("node"):
        if item.get("resource-id") != "com.android.systemui:id/wifi_list":
            continue
        title = next(
            (
                child.get("text", "")
                for child in item.iter("node")
                if child.get("resource-id") == "com.android.systemui:id/wifi_title"
            ),
            "",
        )
        if title == ssid:
            matching_rows.append(item)
    if len(matching_rows) != 1:
        pytest.fail(f"{summary}: SystemUI 中 SSID {ssid!r} 条目数={len(matching_rows)}")
    resources = {
        child.get("resource-id", "") for child in matching_rows[0].iter("node")
    }
    has_lock = "com.android.systemui:id/wifi_end_icon" in resources
    capabilities = scan_result_capabilities(scan_blob, ssid)
    if has_lock != encrypted:
        pytest.fail(
            f"{summary}: SSID={ssid!r} 锁图标={has_lock}，"
            f"期望={encrypted}，capabilities={capabilities!r}"
        )


@allure.step("执行 SystemUI 加密图标验证")
def run_systemui_encrypt_icon_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any,
) -> None:
    """Validate lock-icon behavior for AP-supported encrypted/open matrices."""
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"EncryptIcon_UI_(00[12])$", summary)
    if not match:
        raise ValueError(f"未知 SystemUI EncryptIcon 用例: {summary}")
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    encrypted = match.group(1) == "001"
    modes = (
        ("wpa-aes", "WPA"),
        ("wpa2-aes", "WPA2"),
        ("wpa3-aes", "WPA3"),
    ) if encrypted else (
        ("open", "Open"),
        ("enhanced-open", "OWE"),
    )
    checked = []
    unobservable = []
    try:
        for security, label in modes:
            ssid = f"PyAutoTest_{label}"
            password = "A1secure!" if encrypted else ""
            wifi_ap_action.configure_wifi(
                ssid=ssid,
                password=password,
                security=security,
                band="5g",
                verify=True,
            )
            assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
            scan_blob = run_shell_cmd("cmd wifi list-scan-results")
            capabilities = scan_result_capabilities(scan_blob, ssid)
            capability_blob = " ".join(capabilities).upper()
            expected_tokens = {
                "wpa-aes": ("WPA-PSK",),
                "wpa2-aes": ("WPA2", "RSN-PSK"),
                "wpa3-aes": ("SAE",),
                "enhanced-open": ("OWE",),
            }
            required = expected_tokens.get(security, ())
            if required and not any(token in capability_blob for token in required):
                pytest.fail(
                    f"{summary}: AP 安全模式未生效，SSID={ssid!r}，"
                    f"security={security!r}，capabilities={capabilities!r}"
                )
            capability_encrypted = any(
                token in capability.upper()
                for capability in capabilities
                for token in ("WEP", "WPA", "SAE", "EAP")
            )
            if capability_encrypted != encrypted:
                pytest.fail(
                    f"{summary}: AP 安全模式下发不匹配，SSID={ssid!r}，"
                    f"security={security!r}，capabilities={capabilities!r}"
                )
            open_internet_dialog(settings_ui, capture=False)
            visible = visible_systemui_ssids(settings_ui)
            candidate = ssid if ssid in visible else next(
                (
                    name
                    for name in visible
                    if any(
                        token in capability.upper()
                        for capability in scan_result_capabilities(scan_blob, name)
                        for token in ("WEP", "WPA", "SAE", "EAP")
                    ) == encrypted
                ),
                "",
            )
            if not candidate:
                unobservable.append((label, visible))
                continue
            assert_encryption_icon(
                summary, settings_ui, scan_blob, candidate, encrypted=encrypted
            )
            checked.append(label)
        capture_systemui(settings_ui, f"encrypt_icon_{match.group(1)}")
        print(f"[{summary}] 已验证 SystemUI 加密图标矩阵: {checked!r}")
        if unobservable:
            details = ", ".join(label for label, _ in unobservable)
            if (os.environ.get("WIFISEC_SWITCH") or "").strip().lower() == "off":
                pytest.fail(
                    f"{summary}: 已声明 WiFi 安全关闭，但 SystemUI 未显示 "
                    f"{details} 类网络；可见={unobservable[-1][1]!r}"
                )
            pytest.skip(
                f"{summary}: AP 扫描安全属性已验证；SystemUI 未显示 {details}，"
                "需关闭 安全-安全中心-WiFi安全 并设置 WIFISEC_SWITCH=off"
            )
    finally:
        wifi_ap_action.teardown_wifi()
