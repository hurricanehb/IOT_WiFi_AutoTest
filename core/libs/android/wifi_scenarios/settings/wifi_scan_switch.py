"""SettingsUI scenarios for WiFi background scanning controls."""
from __future__ import annotations

import time
from collections.abc import Callable

import allure
import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.settings._global_settings import (
    global_setting,
    restore_global_setting,
    set_global_setting,
)
from core.libs.android.wifi_scenarios.settings._helpers import (
    visible_ssids,
    wlan_list_blob,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI

WIFI_SCAN_ALWAYS_KEY = "wifi_scan_always_enabled"


def _wifi_scan_switch_checked(settings_ui: AndroidSettingsUI) -> bool:
    device = settings_ui.device
    device.screen_on()
    device.shell("wm dismiss-keyguard")
    device.shell(
        "am start -W -a android.settings.LOCATION_SOURCE_SETTINGS -f 0x10008000"
    )
    for candidates in (
        ("位置信息服务", "定位服务", "Location services"),
        ("WLAN 扫描", "Wi-Fi scanning", "WiFi scanning"),
    ):
        for text in candidates:
            if device(text=text).click_exists(timeout=3):
                break
        else:
            settings_ui.fail_with_artifacts(
                f"无法进入 WLAN 扫描设置，未找到 {candidates!r}"
            )
    switch = device(resourceId="android:id/switch_widget")
    if not switch.wait(timeout=5.0):
        settings_ui.fail_with_artifacts("WLAN 扫描设置页未找到开关控件")
    return bool(switch.info.get("checked"))


@allure.step("验证 WLAN 扫描设置恢复出厂默认状态")
def run_wifi_scan_default_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> None:
    """WifiScanSw_UI_001：移除显式键值后验证 ROM 默认 UI 为关闭。"""
    attach_wifi_status(summary, run_shell_cmd)
    original = global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY)
    try:
        run_shell_cmd(f"settings delete global {WIFI_SCAN_ALWAYS_KEY}")
        settings_ui.device.shell("am force-stop com.android.settings")
        checked = _wifi_scan_switch_checked(settings_ui)
        default_value = global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY)
        print(
            f"[{summary}] 恢复默认后 wifi_scan_always_enabled={default_value!r}, "
            f"UI checked={checked!r}"
        )
        if default_value not in ("null", ""):
            pytest.fail(f"{summary}: 删除显式配置后仍存在键值 {default_value!r}")
        if checked:
            pytest.fail(f"{summary}: 恢复出厂默认的 WLAN 扫描开关应为关闭")
    finally:
        restore_global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY, original)
        settings_ui.device.press("home")


@allure.step("执行始终扫描验证")
def run_wifi_scan_always_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    enabled: bool,
    scan_wait_sec: float = 8.0,
) -> None:
    """WifiScanSw_Vali_001/002：WLAN 扫描设置开启/关闭时后台扫描是否有结果。"""
    attach_wifi_status(summary, run_shell_cmd)
    original = global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY)
    expected = "1" if enabled else "0"
    try:
        wifi.set_wifi_enabled(False)
        set_global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY, expected)
        time.sleep(2.0)

        current = global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY)
        print(f"[{summary}] wifi_scan_always_enabled = {current!r}（期望 {expected!r}）")
        if current != expected:
            pytest.fail(
                f"{summary}: WLAN 扫描设置未生效，期望={expected!r} 实际={current!r}"
            )

        ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
        print(f"[{summary}] 扫描到 {len(ssids)} 个 SSID: {ssids[:10]!r}")
        if enabled and not ssids:
            pytest.fail(f"{summary}: 扫描设置开启后应能扫描到 SSID，实际为空")
        if not enabled and ssids:
            pytest.fail(
                f"{summary}: 扫描设置关闭后不应有扫描结果，实际={ssids[:10]!r}"
            )
    finally:
        set_global_setting(
            run_shell_cmd,
            WIFI_SCAN_ALWAYS_KEY,
            original if original.isdigit() else "1",
        )
        wifi.set_wifi_enabled(True)


@allure.step("验证 WLAN 开关两种状态下始终扫描")
def run_wifi_scan_toggle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
    *,
    scan_wait_sec: float = 8.0,
) -> None:
    """WifiScanSw_Vali_003：始终扫描开启时 WLAN 开关不影响扫描结果。"""
    attach_wifi_status(summary, run_shell_cmd)
    original_scan = global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY)
    original_wifi = wifi.is_wifi_enabled()
    try:
        set_global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY, "1")
        if global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY) != "1":
            pytest.fail(f"{summary}: 无法开启 WLAN 扫描设置")

        for wifi_enabled in (True, False):
            if not wifi.set_wifi_enabled(wifi_enabled):
                pytest.fail(
                    f"{summary}: 无法将 WLAN 开关设为"
                    f"{'开启' if wifi_enabled else '关闭'}"
                )
            ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
            state = "开启" if wifi_enabled else "关闭"
            print(f"[{summary}] WLAN {state}时扫描到 {len(ssids)} 个 SSID")
            if not ssids:
                pytest.fail(f"{summary}: WLAN {state}时始终扫描结果为空")

            blob = wlan_list_blob(settings_ui)
            visible = [ssid for ssid in ssids if ssid.lower() in blob.lower()]
            if not visible:
                settings_ui.fail_with_artifacts(
                    f"{summary}: WLAN {state}时设置页未显示扫描条目，"
                    f"后台扫描={ssids[:10]!r}"
                )
            print(f"[{summary}] WLAN {state}时设置页可见 SSID: {visible[:10]!r}")
    finally:
        restore_global_setting(run_shell_cmd, WIFI_SCAN_ALWAYS_KEY, original_scan)
        wifi.set_wifi_enabled(original_wifi)
