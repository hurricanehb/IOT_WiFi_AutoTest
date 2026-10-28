"""SystemUI WiFi ordering and navigation scenarios."""
from __future__ import annotations

import re
import time
from typing import Callable
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.systemui_pages.quick_settings_page import (
    SEE_ALL_PATTERN,
    WIFI_SETTINGS_PATTERN,
    capture_systemui,
    internet_tile,
    open_internet_dialog,
    open_quick_settings,
)
from core.libs.android.wifi_scenarios.systemui.scan_assertions import (
    systemui_scan_snapshot,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


@allure.step("执行 SystemUI SSID 排序验证")
def run_systemui_ssid_order_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> None:
    """Assert the visible mixed WiFi/HyperWiFi list is ordered by strongest RSSI."""
    attach_wifi_status(summary, run_shell_cmd)
    run_shell_cmd("cmd wifi start-scan")
    time.sleep(3.0)
    open_internet_dialog(settings_ui)
    root = ElementTree.fromstring(settings_ui.device.dump_hierarchy())
    rows = []
    for item in root.iter("node"):
        if item.get("resource-id") != "com.android.systemui:id/wifi_list":
            continue
        title = next(
            (
                node.get("text", "").strip()
                for node in item.iter("node")
                if node.get("resource-id") == "com.android.systemui:id/wifi_title"
            ),
            "",
        )
        summary_text = next(
            (
                node.get("text", "")
                for node in item.iter("node")
                if node.get("resource-id") == "com.android.systemui:id/wifi_summary"
            ),
            "",
        )
        rssi_values = [
            int(value) for value in re.findall(r"=\d+,(-?\d+),", summary_text)
        ]
        if title and rssi_values:
            rows.append((title, max(rssi_values)))
    if len(rows) < 2:
        pytest.skip(f"{summary}: 可见且含 RSSI 的 WLAN 条目不足 2 个，实际={rows!r}")
    inversions = [
        (rows[index], rows[index + 1])
        for index in range(len(rows) - 1)
        if rows[index][1] < rows[index + 1][1]
    ]
    print(f"[{summary}] SystemUI SSID/RSSI 顺序: {rows!r}")
    capture_systemui(settings_ui, "ssid_rssi_order")
    if inversions:
        pytest.fail(f"{summary}: SSID 未按信号强到弱排序，逆序项={inversions!r}")


def _assert_open_latency(summary: str, elapsed: float, cycle: int | None = None) -> None:
    suffix = f"，第 {cycle} 次" if cycle is not None else ""
    print(f"[{summary}] WLAN 列表打开耗时{suffix}: {elapsed:.3f}s")
    if elapsed > 1.0:
        pytest.fail(f"{summary}: WLAN 列表打开耗时{suffix} {elapsed:.3f}s，要求 <=1s")


@allure.step("执行 SystemUI 页面切换验证")
def run_systemui_switch_page_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> None:
    """Execute SystemUI SwitchPage_UI_001 through SwitchPage_UI_004."""
    attach_wifi_status(summary, run_shell_cmd)
    prefix = "Func_Components_SystemUI_SwitchPage_UI_"
    if not summary.startswith(prefix) or summary[len(prefix):] not in {
        "001", "002", "003", "004"
    }:
        raise ValueError(f"未知 SystemUI SwitchPage 用例: {summary}")
    number = int(summary[len(prefix):])

    if number == 1:
        elapsed = open_internet_dialog(settings_ui)
        hierarchy = settings_ui.device.dump_hierarchy()
        required = {
            "WLAN": ("WLAN", "Wi-Fi"),
            "有线网络": ("有线网络", "Ethernet"),
            "移动数据": ("移动数据", "Mobile data"),
        }
        missing = [
            label
            for label, texts in required.items()
            if not any(text in hierarchy for text in texts)
        ]
        if missing:
            pytest.skip(f"{summary}: 当前设备未提供页面切换入口 {missing!r}")
        _assert_open_latency(summary, elapsed)
        return

    if number == 2:
        slow_cycles = []
        failed_cycles = []
        for cycle in range(1, 21):
            try:
                elapsed = open_internet_dialog(settings_ui, capture=False)
            except AssertionError as error:
                failed_cycles.append((cycle, str(error)))
                print(f"[{summary}] 第 {cycle} 次 WLAN 列表打开失败: {error}")
                continue
            print(f"[{summary}] WLAN 列表打开耗时，第 {cycle} 次: {elapsed:.3f}s")
            if elapsed > 1.0:
                slow_cycles.append((cycle, elapsed))
        capture_systemui(settings_ui, "switch_page_cycles_complete")
        if slow_cycles or failed_cycles:
            slow_details = ", ".join(
                f"#{cycle}={elapsed:.3f}s" for cycle, elapsed in slow_cycles
            )
            pytest.fail(
                f"{summary}: 打开失败 {len(failed_cycles)}/20 次；"
                f"耗时超过 1s {len(slow_cycles)}/20 次: {slow_details}"
            )
        return

    if number == 3:
        open_internet_dialog(settings_ui)
        settings_ui.device.screen_off()
        time.sleep(1.0)
        settings_ui.device.screen_on()
        settings_ui.device.unlock()
        if settings_ui.device(
            resourceId="com.android.systemui:id/internet_dialog_title"
        ).exists:
            settings_ui.fail_with_artifacts(f"{summary}: 亮屏后 WLAN 列表未消失")
        _assert_open_latency(summary, open_internet_dialog(settings_ui))
        return

    open_internet_dialog(settings_ui)
    snapshots = {systemui_scan_snapshot(settings_ui)}
    for sample in range(1, 31):
        time.sleep(10.0)
        if not settings_ui.device(
            resourceId="com.android.systemui:id/internet_dialog_title"
        ).exists:
            settings_ui.fail_with_artifacts(f"{summary}: 5 分钟内 WLAN 列表意外消失")
        snapshots.add(systemui_scan_snapshot(settings_ui))
        if sample % 6 == 0:
            print(f"[{summary}] 已观察 {sample * 10}s，扫描列表快照种类={len(snapshots)}")
    capture_systemui(settings_ui, "switch_page_refresh_5min")
    if len(snapshots) < 2:
        pytest.fail(f"{summary}: 5 分钟内 WLAN 列表内容没有任何刷新变化")


def _click_text_pattern(settings_ui: AndroidSettingsUI, pattern: str, label: str) -> None:
    selector = settings_ui.device(textMatches=pattern)
    if not selector.click_exists(timeout=3.0):
        settings_ui.fail_with_artifacts(f"未找到或无法点击{label}")


def _open_all_networks(settings_ui: AndroidSettingsUI) -> None:
    selector = settings_ui.device(resourceId="com.android.systemui:id/see_all_layout")
    if selector.click_exists(timeout=5.0):
        return
    _click_text_pattern(settings_ui, SEE_ALL_PATTERN, "查看全部/WLAN 设置按钮")


def _assert_wifi_settings(settings_ui: AndroidSettingsUI, summary: str) -> None:
    title = settings_ui.device(
        packageName="com.android.settings",
        textMatches=r"(?i)^(互联网|Internet|WLAN|Wi-?Fi)$",
    )
    if not title.wait(timeout=6.0):
        settings_ui.fail_with_artifacts(f"{summary}: 未跳转到 Settings WLAN 页面")
    capture_systemui(settings_ui, "wifi_settings")


def _assert_network_details(settings_ui: AndroidSettingsUI, summary: str) -> None:
    settings_package = settings_ui.device(packageName="com.android.settings")
    if not settings_package.wait(timeout=10.0):
        settings_ui.fail_with_artifacts(f"{summary}: 未跳转到 Settings 网络详情页面")
    hierarchy = capture_systemui(settings_ui, "network_details")
    details_markers = (
        "网络详情", "Network details", "忘记", "Forget", "断开连接", "Disconnect"
    )
    if not any(marker.casefold() in hierarchy.casefold() for marker in details_markers):
        settings_ui.fail_with_artifacts(f"{summary}: Settings 页面未显示网络详情控件")


@allure.step("执行 SystemUI 按键跳转验证")
def run_systemui_button_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Execute SystemUI Button_UI_001 through Button_UI_004."""
    attach_wifi_status(summary, run_shell_cmd)
    prefix = "Func_Components_SystemUI_Button_UI_"
    if not summary.startswith(prefix) or summary[len(prefix):] not in {
        "001", "002", "003", "004"
    }:
        raise ValueError(f"未知 SystemUI Button 用例: {summary}")
    number = int(summary[len(prefix):])

    if number == 1:
        open_internet_dialog(settings_ui)
        if not settings_ui.device(textMatches=WIFI_SETTINGS_PATTERN).click_exists(
            timeout=2.0
        ):
            _open_all_networks(settings_ui)
        _assert_wifi_settings(settings_ui, summary)
        return

    if number == 2:
        open_quick_settings(settings_ui)
        internet_tile(settings_ui).long_click(duration=1.0)
        _assert_wifi_settings(settings_ui, summary)
        return

    if number == 3:
        open_internet_dialog(settings_ui)
        _open_all_networks(settings_ui)
        _assert_wifi_settings(settings_ui, summary)
        return

    if not wifi.list_connected_ssids(trust_status_fallback=True):
        pytest.skip(f"{summary}: 当前没有已连接 WLAN，无法验证网络详情跳转")
    open_internet_dialog(settings_ui)
    connected = settings_ui.device(textMatches=r"(?i).*(已连接|Connected).*")
    if not connected.click_exists(timeout=8.0):
        settings_ui.fail_with_artifacts("网络面板未找到已连接 WLAN 条目")
    _assert_network_details(settings_ui, summary)
