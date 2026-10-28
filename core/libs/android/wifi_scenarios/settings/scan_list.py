"""Settings WLAN scan-list scenarios."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import re
import time
from typing import Any, cast
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import scan_result_capabilities, ssid_match
from core.libs.android.wifi_scenarios.dual_link import (
    connect_dual_link_in_order,
    dual_link_legs as _entry_legs,
    wait_for_link_ssid as _wait_for_ssid,
)
from core.libs.android.wifi_scenarios.settings.wlan_switch import (
    run_wlan_list_scroll_stability_case,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.scan_profiles import scan_profile_entry
from core.libs.android.wifi_scenarios.settings.scan_list_ops import (
    _click_menu_item,
    _open_long_press_menu,
)
from core.libs.android.settings_pages.connection_config_page import WiFiConnectionConfigUI
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry


@dataclass(frozen=True)
class SettingsScanRow:
    ssid: str
    top: int
    description: str
    resource_ids: frozenset[str]


_BOUNDS_RE = re.compile(r"\[(\d+),(\d+)]\[(\d+),(\d+)]")
_RSSI_RE = re.compile(r"=\d+,(-?\d+),")
_NON_SSID_TITLES = {
    "wlan",
    "wi-fi",
    "wifi",
    "+ 添加网络",
    "添加网络",
    "add network",
    "已保存的网络",
    "saved networks",
}


def settings_scan_rows(hierarchy: str) -> list[SettingsScanRow]:
    root = ElementTree.fromstring(hierarchy)
    rows: list[SettingsScanRow] = []
    for container in root.iter("node"):
        if container.get("clickable") != "true":
            continue
        titles = [
            node.get("text", "").strip()
            for node in container.iter("node")
            if node.get("resource-id") == "android:id/title"
            and node.get("text", "").strip()
        ]
        if len(titles) != 1 or titles[0].casefold() in _NON_SSID_TITLES:
            continue
        match = _BOUNDS_RE.fullmatch(container.get("bounds", ""))
        if match is None:
            continue
        description = container.get("content-desc", "")
        if not description:
            continue
        rows.append(
            SettingsScanRow(
                ssid=titles[0],
                top=int(match.group(2)),
                description=description,
                resource_ids=frozenset(
                    node.get("resource-id", "") for node in container.iter("node")
                ),
            )
        )
    return sorted(rows, key=lambda row: row.top)


def row_rssi(row: SettingsScanRow) -> int | None:
    values = [int(value) for value in _RSSI_RE.findall(row.description)]
    return max(values) if values else None


def scan_list_user_dual_entry(wifi_yaml: dict) -> DualWiFiEntry:
    entry = get_dual_wifi_entry(
        wifi_yaml,
        entry_id="dual_wifi_24g_hyperwifi_us",
    )
    traditional = entry.get("traditional_wifi")
    hyper = entry.get("hyper_wifi")
    if not isinstance(traditional, dict) or not isinstance(hyper, dict):
        pytest.skip(
            "wifi_ssid.yaml 缺少 dual_wifi_24g_hyperwifi_us 双链路配置"
        )
    if not traditional.get("ssid") or not hyper.get("ssid"):
        pytest.skip(
            "dual_wifi_24g_hyperwifi_us 必须同时配置传统 WiFi 和 HyperWiFi SSID"
        )
    return cast(DualWiFiEntry, entry)


def _open_and_rows(settings_ui: AndroidSettingsUI, *, settle_sec: float = 3.0) -> list[SettingsScanRow]:
    settings_ui.open_wifi_settings()
    time.sleep(settle_sec)
    return settings_scan_rows(settings_ui.device.dump_hierarchy())


def _wait_settings_ssid(
    settings_ui: AndroidSettingsUI,
    ssid: str,
    *,
    present: bool,
    timeout: float,
) -> list[SettingsScanRow]:
    deadline = time.monotonic() + timeout
    rows: list[SettingsScanRow] = []
    while time.monotonic() < deadline:
        settings_ui.device.shell("cmd wifi start-scan")
        time.sleep(1.0)
        rows = _open_and_rows(settings_ui, settle_sec=0)
        if any(row.ssid == ssid for row in rows) == present:
            return rows
    state = "出现" if present else "消失"
    settings_ui.fail_with_artifacts(
        f"等待 SSID {ssid!r} 在 Settings {state}超时，当前={[row.ssid for row in rows]!r}"
    )
    return []


def _configure_ap(wifi_ap_action: Any, entry: WiFiEntry, *, security: str) -> str:
    ssid = str(entry.get("ssid") or "")
    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password="" if security == "open" else str(entry.get("pwd") or ""),
        security=security,
        band="5g",
        ssid_encoding=str(entry.get("ssid_encoding") or "utf-8"),
        verify=True,
    )
    return ssid


def _profile(wifi_yaml: dict, summary: str) -> WiFiEntry:
    return scan_profile_entry(wifi_yaml, "ssid_ascii_min_password_min", summary)


@allure.step("执行 Settings WLAN 扫描列表验证")
def run_settings_scan_list_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"ScanList_(Vali|Int)_(\d{3})$", summary)
    if match is None:
        raise ValueError(f"未知 Settings ScanList 用例: {summary}")
    group, number_text = match.groups()
    number = int(number_text)

    if group == "Vali" and number == 1:
        run_shell_cmd("cmd wifi start-scan")
        time.sleep(3.0)
        scan_blob = run_shell_cmd("cmd wifi list-scan-results")
        rows = _open_and_rows(settings_ui)
        if not rows:
            settings_ui.fail_with_artifacts(f"{summary}: Settings WLAN 扫描列表为空")
        checked = []
        for row in rows:
            has_signal_description = (
                "信号" in row.description or "signal" in row.description.casefold()
            )
            has_signal_icon = bool(
                row.resource_ids
                & {
                    "android:id/icon",
                    "com.android.settings:id/wifi_icon",
                    "com.android.settings:id/friction_icon",
                }
            )
            if not has_signal_description and not has_signal_icon:
                pytest.fail(f"{summary}: {row.ssid!r} 未显示信号质量")
            capabilities = scan_result_capabilities(scan_blob, row.ssid)
            if capabilities:
                encrypted = any(
                    token in capability.upper()
                    for capability in capabilities
                    for token in ("WEP", "WPA", "SAE", "EAP")
                )
                secure_description = "安全网络" in row.description or "secured" in row.description.casefold()
                if encrypted != secure_description:
                    pytest.fail(
                        f"{summary}: {row.ssid!r} 加密属性不匹配，"
                        f"capabilities={capabilities!r}, description={row.description!r}"
                    )
            checked.append(row.ssid)
        print(f"[{summary}] 已校验 {len(checked)} 个 Settings WLAN 条目: {checked!r}")
        return

    if group == "Vali" and number == 14:
        rows = [row for row in _open_and_rows(settings_ui) if row_rssi(row) is not None]
        if len(rows) < 2:
            pytest.skip(f"{summary}: 可见且含 RSSI 的 WLAN 条目不足 2 个")
        pairs = [(row.ssid, cast(int, row_rssi(row))) for row in rows]
        inversions = [
            (pairs[index], pairs[index + 1])
            for index in range(len(pairs) - 1)
            if pairs[index][1] < pairs[index + 1][1]
        ]
        print(f"[{summary}] Settings SSID/RSSI 顺序: {pairs!r}")
        if inversions:
            pytest.fail(f"{summary}: SSID 未按信号强到弱排序，逆序项={inversions!r}")
        return

    if group == "Int" and number in (1, 2, 3, 4):
        if number == 3:
            settings_ui.open_wifi_settings()
            settings_ui.device.press("home")
            settings_ui.device.press("recent")
            started = time.monotonic()
            width, height = settings_ui.device.window_size()
            settings_ui.device.click(width // 2, height // 2)
            if not settings_ui._wifi_page_title().wait(timeout=1.0):
                settings_ui.fail_with_artifacts(f"{summary}: 切回 Settings 后 WLAN 页面未恢复")
            elapsed = time.monotonic() - started
            print(f"[{summary}] 最近任务切回 WLAN 页面耗时={elapsed:.3f}s，要求<=1s")
            if elapsed > 1.0:
                pytest.fail(f"{summary}: WLAN 页面显示耗时 {elapsed:.3f}s，要求 <=1s")
            return
        if number == 4:
            settings_ui.device.shell("am force-stop com.android.settings")
        else:
            settings_ui.device.press("home")
        started = time.monotonic()
        settings_ui.open_wifi_settings()
        elapsed = time.monotonic() - started
        limit = 1.0 if number == 2 else 3.0
        if number == 2:
            settings_ui.device.press("power")
            time.sleep(1.0)
            started = time.monotonic()
            settings_ui.device.screen_on()
            settings_ui.device.shell("wm dismiss-keyguard")
            if not settings_ui._wifi_page_title().wait(timeout=limit):
                settings_ui.fail_with_artifacts(f"{summary}: 亮屏后 WLAN 页面未恢复")
            elapsed = time.monotonic() - started
        print(f"[{summary}] WLAN 页面显示耗时={elapsed:.3f}s，要求<={limit:g}s")
        if elapsed > limit:
            pytest.fail(f"{summary}: WLAN 页面显示耗时 {elapsed:.3f}s，要求 <= {limit:g}s")
        return

    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    entry = _profile(wifi_yaml, summary)
    security = "open" if number == 9 else "wpa2-aes"
    connection_entry = cast(
        WiFiEntry,
        {
            **entry,
            "pwd": "" if number == 9 else str(entry.get("pwd") or ""),
            "encrypt": "OPEN" if number == 9 else "WPA2",
        },
    )
    ssid = ""
    try:
        if number == 3:
            settings_ui.open_wifi_settings()
            ssid = _configure_ap(wifi_ap_action, entry, security=security)
            _wait_settings_ssid(settings_ui, ssid, present=True, timeout=15.0)
            return
        ssid = _configure_ap(wifi_ap_action, entry, security=security)
        _wait_settings_ssid(settings_ui, ssid, present=True, timeout=15.0)
        if number == 4:
            wifi_ap_action.teardown_wifi()
            _wait_settings_ssid(settings_ui, ssid, present=False, timeout=20.0)
            return
        if number not in (8, 9):
            raise ValueError(f"未实现的 Settings ScanList 用例: {summary}")

        wifi.clear_saved_networks()
        config_ui = WiFiConnectionConfigUI(settings_ui)
        config_ui.open_for_ssid(ssid)
        if number == 8:
            config_ui.require_dialog(ssid)
            config_ui.set_password(str(entry.get("pwd") or ""))
            config_ui.save()
        elif config_ui.dialog_exists():
            config_ui.cancel()
            pytest.fail(f"{summary}: 开放网络不应弹出密码配置框")
        assert_wifi_connected(
            wifi,
            wifi_yaml,
            run_shell_cmd,
            entry=connection_entry,
        )
    finally:
        wifi_ap_action.teardown_wifi()


@allure.step("执行 Settings WLAN 列表开关稳定性验证")
def run_settings_scan_list_toggle_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
    *,
    cycles: int = 20,
    refresh_timeout: float = 6.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    original = wifi.is_wifi_enabled()
    settings_ui.open_wifi_settings()
    try:
        for cycle in range(1, cycles + 1):
            settings_ui.set_wifi_switch(False)
            settings_ui.set_wifi_switch(True)
            deadline = time.monotonic() + refresh_timeout
            rows: list[SettingsScanRow] = []
            while time.monotonic() < deadline:
                run_shell_cmd("cmd wifi start-scan")
                time.sleep(0.5)
                rows = settings_scan_rows(settings_ui.device.dump_hierarchy())
                if rows:
                    break
            if not rows:
                settings_ui.fail_with_artifacts(
                    f"{summary}: 第 {cycle}/{cycles} 轮 WLAN 列表未在 "
                    f"{refresh_timeout:g}s 内刷新"
                )
            if cycle % 5 == 0:
                print(f"[{summary}] WLAN 开关及列表刷新已完成 {cycle}/{cycles} 轮")
    finally:
        wifi.set_wifi_enabled(original)


@allure.step("执行 Settings WLAN 未连接滚动稳定性验证")
def run_settings_scan_list_user_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    match = re.search(r"ScanList_User_(00[1-5])$", summary)
    if match is None:
        raise ValueError(f"未知 Settings ScanList User 用例: {summary}")
    number = int(match.group(1))
    if number == 1:
        wifi.disconnect_all(post_wait_sec=2.0)
        run_wlan_list_scroll_stability_case(
            summary,
            run_shell_cmd,
            settings_ui,
            cycles=20,
        )
        return

    entry = scan_list_user_dual_entry(wifi_yaml)
    traditional, hyper = _entry_legs(entry)
    legs = {"wifi": traditional, "hyper": hyper}

    if number == 2:
        for link in ("wifi", "hyper"):
            wifi.forget_dual_wifi_entry(entry)
            block = legs[link]
            ssid = str(block.get("ssid") or "")
            wifi.connect_wifi_block(block)
            _wait_for_ssid(wifi, ssid)
            run_wlan_list_scroll_stability_case(
                f"{summary}-{link}",
                run_shell_cmd,
                settings_ui,
                cycles=10,
            )
        return

    if number == 3:
        for order in (("wifi", "hyper"), ("hyper", "wifi")):
            connect_dual_link_in_order(summary, wifi, entry, order)
            run_wlan_list_scroll_stability_case(
                f"{summary}-{'-'.join(order)}",
                run_shell_cmd,
                settings_ui,
                cycles=10,
            )
        return

    action = "断开连接" if number == 4 else "取消保存"
    orders = (
        (("hyper", "wifi"), ("wifi", "hyper"))
        if number == 4
        else (("wifi",), ("hyper",))
    )
    for order in orders:
        connect_dual_link_in_order(summary, wifi, entry, ("wifi", "hyper"))
        for link in order:
            ssid = str(legs[link].get("ssid") or "")
            before_status = run_shell_cmd("cmd wifi status")
            _open_long_press_menu(summary, settings_ui, ssid)
            _click_menu_item(summary, settings_ui, action)
            deadline = time.monotonic() + 12.0
            association_samples: list[tuple[float, bool]] = []
            started = time.monotonic()
            while time.monotonic() < deadline:
                found, _ = wifi.match_associated_ssids(
                    [ssid],
                    use_dumpsys_for_missing=True,
                )
                association_samples.append(
                    (time.monotonic() - started, bool(found))
                )
                if not found:
                    print(
                        f"[{summary}] {ssid!r} 点击{action}后关联采样="
                        f"{association_samples!r}"
                    )
                    break
                time.sleep(0.5)
            else:
                after_status = run_shell_cmd("cmd wifi status")
                networks = wifi.list_networks_blob()
                pytest.fail(
                    f"{summary}: {action}后仍连接 {ssid!r}；"
                    f"采样={association_samples!r}\n"
                    f"点击前 status:\n{before_status[:1800]}\n"
                    f"点击后 status:\n{after_status[:1800]}\n"
                    f"list-networks:\n{networks[:1000]}\n"
                )
        run_wlan_list_scroll_stability_case(
            f"{summary}-{'-'.join(order)}",
            run_shell_cmd,
            settings_ui,
            cycles=10,
        )