"""SettingsUI scenarios for WLAN switching and stability."""
from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import scan_result_ssids
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.settings._helpers import (
    resolve_entry as _resolve_entry,
    visible_ssids,
    wlan_list_blob,
)
from core.libs.android.systemui_pages.quick_settings_page import (
    open_internet_dialog,
    systemui_wifi_toggle,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.utils.log_handler import get_logger

log = get_logger(__name__)


@allure.step("执行 WLAN 开启验证")
def run_wlan_switch_on_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
    *,
    min_scan_ssids: int = 1,
    scan_wait_sec: float = 6.0,
) -> None:
    """WlanSwitch_Vali_001：开关开启后射频生效且扫描列表非空。"""
    attach_wifi_status(summary, run_shell_cmd)
    if not wifi.set_wifi_enabled(True):
        pytest.fail(f"{summary}: 无法开启 WLAN 开关")
    if not wifi.is_wifi_enabled():
        pytest.fail(f"{summary}: WLAN 开关开启后射频仍为关闭")

    wifi_on = run_shell_cmd("settings get global wifi_on").strip()
    print(f"[{summary}] settings get global wifi_on = {wifi_on!r}")
    if wifi_on not in ("1", "2"):
        pytest.fail(f"{summary}: 全局开关 wifi_on 期望为开启态，实际={wifi_on!r}")

    run_shell_cmd("cmd wifi start-scan")
    time.sleep(scan_wait_sec)
    scan_blob = run_shell_cmd("cmd wifi list-scan-results")
    ssids = scan_result_ssids(scan_blob)
    print(f"[{summary}] 扫描到 {len(ssids)} 个 SSID: {ssids[:15]!r}")
    if len(ssids) < max(1, min_scan_ssids):
        pytest.fail(
            f"{summary}: 扫描列表 SSID 数量不足（需要>={min_scan_ssids}，实际={len(ssids)}）"
            f"\n{scan_blob[:800]}"
        )
    blob = wlan_list_blob(settings_ui)
    visible = [name for name in ssids if name.lower() in blob.lower()]
    if not visible:
        settings_ui.fail_with_artifacts(
            f"{summary}: WLAN 设置页未显示任何扫描到的 SSID（扫描={ssids[:10]!r}）"
        )
    log.info("%s: WLAN 列表已显示 SSID %r", summary, visible[:10])


def _scan_always_value(run_shell_cmd: Callable[[str], str]) -> str:
    return run_shell_cmd("settings get global wifi_scan_always_enabled").strip()


def _set_scan_always(run_shell_cmd: Callable[[str], str], value: str) -> None:
    run_shell_cmd(f"settings put global wifi_scan_always_enabled {value}")


@allure.step("执行 WLAN 关闭验证")
def run_wlan_switch_off_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    scan_wait_sec: float = 6.0,
) -> None:
    """WlanSwitch_Vali_002：关闭开关后射频关闭且扫描列表为空。"""
    attach_wifi_status(summary, run_shell_cmd)
    original = _scan_always_value(run_shell_cmd)
    try:
        _set_scan_always(run_shell_cmd, "0")
        if not wifi.set_wifi_enabled(False):
            pytest.fail(f"{summary}: 无法关闭 WLAN 开关")
        if wifi.is_wifi_enabled():
            pytest.fail(f"{summary}: WLAN 开关关闭后射频仍为开启")

        wifi_on = run_shell_cmd("settings get global wifi_on").strip()
        print(f"[{summary}] settings get global wifi_on = {wifi_on!r}")
        if wifi_on != "0":
            pytest.fail(f"{summary}: 全局开关 wifi_on 期望为 '0'，实际={wifi_on!r}")

        ssids = visible_ssids(run_shell_cmd, scan_wait_sec=scan_wait_sec)
        print(f"[{summary}] 关闭后扫描到 {len(ssids)} 个 SSID: {ssids[:10]!r}")
        if ssids:
            pytest.fail(f"{summary}: WLAN 关闭后扫描列表应为空，实际={ssids[:10]!r}")
    finally:
        _set_scan_always(run_shell_cmd, original if original.isdigit() else "1")
        wifi.set_wifi_enabled(True)


def _airplane_mode_value(run_shell_cmd: Callable[[str], str]) -> str:
    return run_shell_cmd("settings get global airplane_mode_on").strip()


def _set_airplane_mode(
    run_shell_cmd: Callable[[str], str], enabled: bool, *, settle_sec: float = 3.0
) -> None:
    value = "1" if enabled else "0"
    action = "enable" if enabled else "disable"
    run_shell_cmd(f"cmd connectivity airplane-mode {action}")
    time.sleep(settle_sec)
    actual = _airplane_mode_value(run_shell_cmd)
    if actual != value:
        pytest.fail(f"飞行模式设置未生效，期望={value!r}，实际={actual!r}")


@allure.step("执行飞行模式 WLAN 开关验证")
def run_airplane_wlan_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    settle_sec: float = 5.0,
) -> None:
    """WlanSwitch_Int_002：飞行模式与 WLAN 开关、自动重连交互。"""
    attach_wifi_status(summary, run_shell_cmd)
    entry = _resolve_entry(
        wifi_yaml, index=None, ssid=None, summary=summary, run_shell_cmd=run_shell_cmd
    )
    original_airplane = _airplane_mode_value(run_shell_cmd)
    original_wifi = wifi.is_wifi_enabled()
    try:
        if original_airplane == "1":
            _set_airplane_mode(run_shell_cmd, False, settle_sec=settle_sec)
        target = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)

        _set_airplane_mode(run_shell_cmd, True, settle_sec=settle_sec)
        if wifi.is_wifi_enabled():
            pytest.fail(f"{summary}: 开启飞行模式后 WLAN 开关未自动关闭")

        if not wifi.set_wifi_enabled(True, settle_sec=settle_sec):
            pytest.fail(f"{summary}: 飞行模式下无法重新开启 WLAN")
        reconnected = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)

        _set_airplane_mode(run_shell_cmd, False, settle_sec=settle_sec)
        if not wifi.set_wifi_enabled(False, settle_sec=settle_sec):
            pytest.fail(f"{summary}: 关闭飞行模式后无法关闭 WLAN")
        if not wifi.set_wifi_enabled(True, settle_sec=settle_sec):
            pytest.fail(f"{summary}: 关闭飞行模式后无法重新开启 WLAN")
        final = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        print(
            f"[{summary}] 飞行模式 WLAN 交互通过："
            f"初始={target!r}，飞行模式内重连={reconnected!r}，最终={final!r}"
        )
    finally:
        current_airplane = _airplane_mode_value(run_shell_cmd)
        expected_airplane = original_airplane == "1"
        if current_airplane in ("0", "1") and (current_airplane == "1") != expected_airplane:
            _set_airplane_mode(run_shell_cmd, expected_airplane, settle_sec=settle_sec)
        wifi.set_wifi_enabled(original_wifi, settle_sec=settle_sec)


def _clear_crash_log(run_shell_cmd: Callable[[str], str]) -> None:
    run_shell_cmd("logcat -b crash -c")


def _assert_settings_alive_without_crash(
    summary: str, run_shell_cmd: Callable[[str], str]
) -> None:
    pid = run_shell_cmd("pidof com.android.settings").strip()
    if not pid or not any(part.isdigit() for part in pid.split()):
        pytest.fail(f"{summary}: 操作后 Settings 进程不存在，疑似闪退")
    crash_log = run_shell_cmd("logcat -b crash -d").strip()
    lower = crash_log.lower()
    if "fatal exception" in lower and (
        "com.android.settings" in lower or "com.android.systemui" in lower
    ):
        pytest.fail(f"{summary}: 检测到 Settings/SystemUI 闪退日志\n{crash_log[-2000:]}")


@allure.step("执行 WLAN 开关稳定性验证")
def run_wlan_toggle_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
    *,
    cycles: int = 20,
    settle_sec: float = 0.3,
) -> None:
    """WlanSwitch_Stb_001：快速关闭/开启 WLAN 20 次且 Settings 不闪退。"""
    attach_wifi_status(summary, run_shell_cmd)
    original = wifi.is_wifi_enabled()
    _clear_crash_log(run_shell_cmd)
    settings_ui.open_wifi_settings()
    try:
        for cycle in range(1, cycles + 1):
            if not wifi.set_wifi_enabled(False, settle_sec=settle_sec):
                pytest.fail(f"{summary}: 第 {cycle}/{cycles} 轮无法关闭 WLAN")
            if not wifi.set_wifi_enabled(True, settle_sec=settle_sec):
                pytest.fail(f"{summary}: 第 {cycle}/{cycles} 轮无法开启 WLAN")
            if cycle % 5 == 0:
                print(f"[{summary}] WLAN 快速开关已完成 {cycle}/{cycles} 轮")
        _assert_settings_alive_without_crash(summary, run_shell_cmd)
    finally:
        wifi.set_wifi_enabled(original)


@allure.step("执行 WLAN 列表滚动稳定性验证")
def run_wlan_list_scroll_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
    *,
    cycles: int = 20,
) -> None:
    """WlanSwitch_Stb_002：快速上下滑动 WLAN 列表 20 次且 Settings 不闪退。"""
    attach_wifi_status(summary, run_shell_cmd)
    _clear_crash_log(run_shell_cmd)
    settings_ui.open_wifi_settings()
    width, height = settings_ui.device.window_size()
    center = width // 2
    top = max(1, height // 4)
    bottom = max(top + 1, height * 3 // 4)
    for cycle in range(1, cycles + 1):
        settings_ui.device.swipe(center, bottom, center, top, 0.12)
        settings_ui.device.swipe(center, top, center, bottom, 0.12)
        hierarchy = settings_ui.device.dump_hierarchy()
        if "com.android.settings" not in hierarchy:
            settings_ui.fail_with_artifacts(
                f"{summary}: 第 {cycle}/{cycles} 轮滑动后离开 Settings 或控件树为空"
            )
        if cycle % 5 == 0:
            print(f"[{summary}] WLAN 列表上下滑动已完成 {cycle}/{cycles} 轮")
    _assert_settings_alive_without_crash(summary, run_shell_cmd)


@allure.step("执行热点 WLAN 开关验证")
def run_hotspot_wlan_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    settle_sec: float = 5.0,
) -> None:
    """WlanSwitch_Int_001：SoftAP 开启时 WLAN 可切换并自动重连。"""
    attach_wifi_status(summary, run_shell_cmd)
    original_wifi = wifi.is_wifi_enabled()
    entry = _resolve_entry(
        wifi_yaml, index=None, ssid=None, summary=summary, run_shell_cmd=run_shell_cmd
    )
    target = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    hotspot_ssid = "PyAutoTest_WlanSwitch"
    run_shell_cmd(f"cmd wifi start-softap {hotspot_ssid} wpa2 24681357 -b 2")
    try:
        time.sleep(settle_sec)
        interface = run_shell_cmd("ip link show wlan1")
        flags = interface.partition("<")[2].partition(">")[0].split(",")
        if "state UP" not in interface and "UP" not in flags:
            pytest.fail(f"{summary}: 热点启动后未发现 wlan1 接口\n{interface[:500]}")
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if not any(name.lower() == target.lower() for name in connected):
            pytest.fail(f"{summary}: 开启热点后 STA 连接丢失，当前={connected!r}")

        if not wifi.set_wifi_enabled(False, settle_sec=settle_sec):
            pytest.fail(f"{summary}: 热点开启时无法关闭 WLAN")
        if not wifi.set_wifi_enabled(True, settle_sec=settle_sec):
            pytest.fail(f"{summary}: 热点开启时无法重新打开 WLAN")
        final = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        print(f"[{summary}] 热点与 WLAN 共存、开关及自动重连通过：{final!r}")
    finally:
        run_shell_cmd("cmd wifi stop-softap")


@allure.step("执行跨组件 WLAN 开关验证")
def run_cross_component_wlan_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
    *,
    settle_sec: float = 2.0,
) -> None:
    """WlanSwitch_Int_003：Settings 与 SystemUI 双向切换状态一致。"""
    attach_wifi_status(summary, run_shell_cmd)
    original = wifi.is_wifi_enabled()
    try:
        settings_ui.set_wifi_switch(False)
        time.sleep(settle_sec)
        if wifi.is_wifi_enabled():
            pytest.fail(f"{summary}: Settings 关闭 WLAN 后射频仍为开启")

        open_internet_dialog(settings_ui, capture=False)
        toggle = systemui_wifi_toggle(settings_ui)
        if bool(toggle.info.get("checked")):
            pytest.fail(f"{summary}: Settings 关闭 WLAN 后 SystemUI 开关未同步")
        toggle.click()
        time.sleep(settle_sec)
        if not wifi.is_wifi_enabled():
            pytest.fail(f"{summary}: SystemUI 点击 WLAN 磁贴后射频未开启")

        settings_ui.open_wifi_settings()
        if not settings_ui.wifi_switch_checked():
            pytest.fail(f"{summary}: SystemUI 开启 WLAN 后 Settings 开关未同步")

        settings_ui.set_wifi_switch(False)
        settings_ui.set_wifi_switch(True)
        if not wifi.is_wifi_enabled():
            pytest.fail(f"{summary}: Settings 再次开启 WLAN 后射频未同步")
        print(f"[{summary}] Settings 与 SystemUI WLAN 状态双向一致")
    finally:
        wifi.set_wifi_enabled(original)


@allure.step("执行错误密码重连稳定性验证")
def run_wrong_password_reconnect_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any,
    *,
    cycles: int = 20,
    settle_sec: float = 2.0,
) -> None:
    """WlanSwitch_Stb_003：错误密码拒绝、正确密码重连 20 次且不闪退。"""
    attach_wifi_status(summary, run_shell_cmd)
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    ssid = "PyAutoTest_WlanStability"
    password = "24681357"
    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=password,
        security="wpa2-aes",
        band="5g",
        verify=True,
    )
    entry: WiFiEntry = {
        "ssid": ssid,
        "pwd": password,
        "encrypt": "WPA2",
        "type": "normal",
        "expect": "connected",
    }
    time.sleep(settle_sec)
    _clear_crash_log(run_shell_cmd)
    settings_ui.open_wifi_settings()
    try:
        for cycle in range(1, cycles + 1):
            wifi.clear_saved_networks(max_rounds=2, settle_sec=0.1)
            wifi.connect_wpa2(ssid, "wrong_pwd_00000")
            time.sleep(settle_sec)
            connected = wifi.list_connected_ssids(trust_status_fallback=True)
            if any(name.lower() == ssid.lower() for name in connected):
                pytest.fail(f"{summary}: 第 {cycle}/{cycles} 轮错误密码却连接成功")
            assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
            if cycle % 5 == 0:
                print(f"[{summary}] 错误密码拒绝并重连已完成 {cycle}/{cycles} 轮")
        _assert_settings_alive_without_crash(summary, run_shell_cmd)
    finally:
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.1)
