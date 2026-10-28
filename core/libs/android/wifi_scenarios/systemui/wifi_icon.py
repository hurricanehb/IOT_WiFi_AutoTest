"""SystemUI connected-row WiFi icon scenarios."""
from __future__ import annotations

import re
from typing import Callable, cast

import allure
from PIL import Image
import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.systemui_pages.quick_settings_page import open_internet_dialog
from core.libs.android.wifi_scenarios.systemui.parsers import systemui_connected_wifi_row
from core.libs.android.wifi_scenarios.wifi_icon_image import has_h_glyph, has_hyper_badge
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry


_STANDARD_RE = re.compile(r"Wi[\N{NON-BREAKING HYPHEN}-]?Fi\s*([4-7])", re.IGNORECASE)


@allure.step("执行 SystemUI WLAN 标准与 HyperWiFi 图标验证")
def run_systemui_wifi_icon_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Connect the target first so icon checks never depend on list scrolling."""
    attach_wifi_status(summary, run_shell_cmd)
    entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
    if not entry:
        pytest.skip(f"{summary}: 缺少 dual_wifi_24g_hyperwifi_us 配置")
    if summary.endswith("UI_001"):
        target = entry.get("traditional_wifi")
    elif summary.endswith(("UI_002", "UI_003")):
        target = entry.get("hyper_wifi")
    else:
        raise ValueError(f"未知 SystemUI WifiIcon 用例: {summary}")
    if not isinstance(target, dict) or not str(target.get("ssid") or ""):
        pytest.skip(f"{summary}: 目标 WiFi 配置无效")
    ssid = str(target["ssid"])

    try:
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        if not wifi.ensure_wifi_connected(cast(WiFiEntry, target)):
            pytest.fail(f"{summary}: 无法连接目标网络 {ssid!r}")
        open_internet_dialog(settings_ui, capture=False)
        hierarchy = settings_ui.device.dump_hierarchy()
        row = systemui_connected_wifi_row(hierarchy)
        if row is None:
            settings_ui.fail_with_artifacts(
                f"{summary}: SystemUI 未显示已连接行，期望={ssid!r}"
            )
            raise AssertionError("fail_with_artifacts should not return")
        if row.ssid != ssid:
            settings_ui.fail_with_artifacts(
                f"{summary}: SystemUI 已连接行不匹配，期望={ssid!r}，"
                f"实际={row.ssid!r}"
            )

        settings_ui.artifact_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = settings_ui.artifact_dir / f"{summary}.png"
        settings_ui.device.screenshot(str(screenshot_path))
        image = Image.open(screenshot_path)
        allure.attach.file(
            str(screenshot_path),
            name=f"{summary}-systemui-wifi-icon",
            attachment_type=allure.attachment_type.PNG,
        )

        if summary.endswith("UI_001"):
            generations = {int(value) for value in _STANDARD_RE.findall(row.summary)}
            if not generations:
                pytest.fail(
                    f"{summary}: 已连接行未检测到 Wi-Fi 4/5/6/7 下标，"
                    f"summary={row.summary!r}"
                )
            print(f"[{summary}] 已连接 {ssid!r}，检测到标准下标 {sorted(generations)}")
            return

        if "Hyper Wi-Fi" not in row.summary.replace("‑", "-"):
            pytest.fail(f"{summary}: 已连接行未标识 Hyper Wi-Fi: {row.summary!r}")
        if summary.endswith("UI_002"):
            bounds = row.resources.get("com.android.systemui:id/wifi_label")
            if bounds is None or not has_hyper_badge(image, bounds):
                settings_ui.fail_with_artifacts(
                    f"{summary}: {ssid!r} 已连接行未识别到 HYPER Wi-Fi 徽标"
                )
            return

        bounds = row.resources.get("com.android.systemui:id/wifi_connected_icon")
        if bounds is None or not has_h_glyph(image, bounds):
            settings_ui.fail_with_artifacts(
                f"{summary}: {ssid!r} 已连接图标未识别到 H"
            )
    finally:
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        settings_ui.device.press("home")
