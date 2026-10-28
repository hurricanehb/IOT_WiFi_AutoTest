"""Settings WLAN scan-list long-press menu scenarios."""

from __future__ import annotations

from collections.abc import Callable, Sequence
import re
import time
from typing import Any, cast
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import ssid_match
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.scan_profiles import scan_profile_entry
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_wifi_list_entry


def scan_list_menu_items(hierarchy: str) -> tuple[str, ...]:
    root = ElementTree.fromstring(hierarchy)
    focused_lists = [
        node
        for node in root.iter("node")
        if node.get("class") == "android.widget.ListView"
        and node.get("focused") == "true"
    ]
    scope = focused_lists[-1] if focused_lists else root
    return tuple(
        text
        for node in scope.iter("node")
        if node.get("resource-id") == "android:id/title"
        and (text := node.get("text", "").strip())
    )


def _entry(
    wifi_yaml: dict,
    summary: str,
    *,
    entry_id: str | None = None,
    ssid: str | None = None,
) -> WiFiEntry:
    entry = cast(
        WiFiEntry,
        get_wifi_list_entry(wifi_yaml, entry_id=entry_id, ssid=ssid),
    )
    if not entry:
        pytest.skip(f"{summary}: 缺少测试数据 entry_id={entry_id!r}, ssid={ssid!r}")
    return entry


def _open_long_press_menu(
    summary: str,
    settings_ui: AndroidSettingsUI,
    ssid: str,
) -> tuple[str, ...]:
    settings_ui.open_wifi_settings()
    time.sleep(3.0)
    settings_ui.scroll_to_text(ssid)
    settings_ui.device(text=ssid).long_click(duration=1.0)
    time.sleep(1.0)
    items = scan_list_menu_items(settings_ui.device.dump_hierarchy())
    if not items or items[0] != ssid:
        settings_ui.fail_with_artifacts(
            f"{summary}: 长按 {ssid!r} 后未显示对应快捷菜单，items={items!r}"
        )
    return items


def _assert_menu_items(
    summary: str,
    actual: Sequence[str],
    expected: Sequence[str],
) -> None:
    missing = [item for item in expected if item not in actual]
    if missing:
        pytest.fail(
            f"{summary}: 快捷菜单缺少 {missing!r}，实际={list(actual)!r}"
        )


def _click_menu_item(
    summary: str,
    settings_ui: AndroidSettingsUI,
    text: str,
) -> None:
    item = settings_ui.device(text=text)
    if not item.click_exists(timeout=3.0):
        settings_ui.fail_with_artifacts(
            f"{summary}: 快捷菜单无法点击 {text!r}"
        )
    deadline = time.monotonic() + 3.0
    while time.monotonic() < deadline:
        if not item.exists:
            return
        time.sleep(0.1)
    settings_ui.fail_with_artifacts(
        f"{summary}: 点击 {text!r} 后快捷菜单未关闭"
    )


def _is_saved(wifi: WiFiControl, ssid: str) -> bool:
    return any(ssid_match(ssid, saved) for saved in wifi.list_saved_networks())


def _wait_connected(wifi: WiFiControl, ssid: str, timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if any(ssid_match(ssid, current) for current in connected):
            return True
        time.sleep(0.5)
    return False


def _configure_scan_ap(
    wifi_ap_action: Any,
    entry: WiFiEntry,
    *,
    security: str,
) -> str:
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


def _wait_settings_ssid(
    settings_ui: AndroidSettingsUI,
    ssid: str,
    *,
    timeout: float,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        settings_ui.device.shell("cmd wifi start-scan")
        settings_ui.open_wifi_settings()
        if settings_ui.device(text=ssid).wait(timeout=2.0):
            return
    settings_ui.fail_with_artifacts(
        f"等待 SSID {ssid!r} 在 Settings 出现超时"
    )


def _forget_if_saved(wifi: WiFiControl, ssid: str) -> None:
    network_id = wifi.find_network_id_by_ssid(ssid)
    if network_id:
        wifi.forget_network(network_id)


@allure.step("执行 Settings WLAN 扫描列表快捷菜单验证")
def run_settings_scan_list_ops_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"ScanListOps_UI_(00[1-9]|010)$", summary)
    if match is None:
        raise ValueError(f"未知 Settings ScanListOps 自动化用例: {summary}")
    number = int(match.group(1))

    if number in (2, 10):
        if wifi_ap_action is None:
            pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
        target_entry = scan_profile_entry(
            wifi_yaml,
            "ssid_ascii_min_password_min",
            summary,
        )
        target_ssid = str(target_entry.get("ssid") or "")
        try:
            _configure_scan_ap(wifi_ap_action, target_entry, security="open")
            _wait_settings_ssid(
                settings_ui,
                target_ssid,
                timeout=20.0,
            )
            _forget_if_saved(wifi, target_ssid)
            items = _open_long_press_menu(summary, settings_ui, target_ssid)
            _assert_menu_items(summary, items, ("连接",))
            unexpected = {"分享", "取消保存", "断开连接"} & set(items)
            if unexpected:
                pytest.fail(
                    f"{summary}: 未保存未连接网络错误显示 {sorted(unexpected)!r}"
                )
            if number == 2:
                return

            _click_menu_item(summary, settings_ui, "连接")
            if not _wait_connected(wifi, target_ssid):
                pytest.fail(f"{summary}: 开放网络未直接连接 {target_ssid!r}")
            _forget_if_saved(wifi, target_ssid)
            wifi_ap_action.teardown_wifi()

            _configure_scan_ap(
                wifi_ap_action,
                target_entry,
                security="wpa2-aes",
            )
            _wait_settings_ssid(
                settings_ui,
                target_ssid,
                timeout=20.0,
            )
            items = _open_long_press_menu(summary, settings_ui, target_ssid)
            _assert_menu_items(summary, items, ("连接",))
            _click_menu_item(summary, settings_ui, "连接")
            password = settings_ui.device(
                resourceId="com.android.settings:id/password"
            )
            advanced = settings_ui.device(
                resourceId="com.android.settings:id/wifi_advanced_togglebox"
            )
            if not password.wait(timeout=5.0) or not advanced.exists:
                settings_ui.fail_with_artifacts(
                    f"{summary}: 加密网络未显示密码和高级选项"
                )
            return
        finally:
            wifi_ap_action.teardown_wifi()

    connected_entry = _entry(
        wifi_yaml,
        summary,
        entry_id="wifi_signal_level_traditional_ap1",
    )
    connected_ssid = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=connected_entry,
    )
    items = _open_long_press_menu(summary, settings_ui, connected_ssid)
    _assert_menu_items(
        summary,
        items,
        ("分享", "取消保存", "断开连接"),
    )

    if number == 1:
        return
    if number == 4:
        _click_menu_item(summary, settings_ui, "分享")
        time.sleep(2.0)
        hierarchy = settings_ui.device.dump_hierarchy()
        if connected_ssid not in hierarchy or not re.search(
            r"分享\s*WLAN|Share\s*Wi-?Fi|qrcode|qr_code",
            hierarchy,
            re.IGNORECASE,
        ):
            settings_ui.fail_with_artifacts(
                f"{summary}: 分享页未显示 SSID 和二维码信息"
            )
        return
    if number == 5:
        _click_menu_item(summary, settings_ui, "取消保存")
        if not wifi.wait_until_disconnected(timeout=10.0):
            pytest.fail(f"{summary}: 取消保存后 WLAN 未断开")
        if _is_saved(wifi, connected_ssid):
            pytest.fail(f"{summary}: 取消保存后仍存在 {connected_ssid!r}")
        return
    if number == 6:
        _click_menu_item(summary, settings_ui, "断开连接")
        if not wifi.wait_until_disconnected(timeout=10.0):
            pytest.fail(f"{summary}: 点击断开连接后 WLAN 未断开")
        if not _is_saved(wifi, connected_ssid):
            pytest.fail(f"{summary}: 断开连接后保存列表缺少 {connected_ssid!r}")
        return

    _click_menu_item(summary, settings_ui, "断开连接")
    if not wifi.wait_until_disconnected(timeout=10.0):
        pytest.fail(f"{summary}: 无法建立已保存未连接状态")
    if not _is_saved(wifi, connected_ssid):
        pytest.fail(f"{summary}: 断开后未保存 {connected_ssid!r}")
    saved_items = _open_long_press_menu(summary, settings_ui, connected_ssid)
    _assert_menu_items(summary, saved_items, ("连接", "取消保存", "修改"))
    if number == 3:
        return
    if number == 7:
        _click_menu_item(summary, settings_ui, "连接")
        if not _wait_connected(wifi, connected_ssid):
            pytest.fail(f"{summary}: 已保存网络未重新连接 {connected_ssid!r}")
        return
    if number == 8:
        _click_menu_item(summary, settings_ui, "修改")
        password = settings_ui.device(resourceId="com.android.settings:id/password")
        advanced = settings_ui.device(
            resourceId="com.android.settings:id/wifi_advanced_togglebox"
        )
        if not password.wait(timeout=5.0) or not advanced.exists:
            settings_ui.fail_with_artifacts(
                f"{summary}: 修改页未显示密码和高级选项"
            )
        return
    if number == 9:
        _click_menu_item(summary, settings_ui, "取消保存")
        if _is_saved(wifi, connected_ssid):
            pytest.fail(f"{summary}: 取消保存后仍存在 {connected_ssid!r}")
        return
    raise ValueError(f"未实现的 Settings ScanListOps 用例: {summary}")