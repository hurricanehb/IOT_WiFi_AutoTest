"""Quick Settings and internet-panel UI helpers."""
from __future__ import annotations

import re
import time

from core.libs.android.settings_pages.settings_page import AndroidSettingsUI

INTERNET_TILE_PATTERN = r"(?i).*(互联网|Internet|WLAN|Wi-?Fi).*"
WIFI_SETTINGS_PATTERN = r"(?i)^(WLAN设置|WLAN settings|Wi-?Fi settings)$"
SEE_ALL_PATTERN = r"(?i)^(查看全部|See all)$"


def capture_systemui(settings_ui: AndroidSettingsUI, stage: str) -> str:
    settings_ui.artifact_dir.mkdir(parents=True, exist_ok=True)
    hierarchy = settings_ui.device.dump_hierarchy()
    (settings_ui.artifact_dir / f"{stage}.xml").write_text(hierarchy, encoding="utf-8")
    settings_ui.device.screenshot(str(settings_ui.artifact_dir / f"{stage}.png"))
    return hierarchy


def open_quick_settings(settings_ui: AndroidSettingsUI) -> None:
    for attempt in range(3):
        settings_ui.device.press("home")
        time.sleep(0.5)
        settings_ui.device.shell("cmd statusbar collapse")
        time.sleep(0.5)
        if attempt == 1:
            settings_ui.reset_uiautomator()
        settings_ui.device.shell("cmd statusbar expand-settings")
        deadline = time.monotonic() + 4.0
        while time.monotonic() < deadline:
            hierarchy = settings_ui.device.dump_hierarchy()
            if "com.android.systemui:id/qs_frame" in hierarchy:
                time.sleep(0.8)
                return
            time.sleep(0.4)
    settings_ui.fail_with_artifacts("快捷设置面板未展开")


def internet_tile(settings_ui: AndroidSettingsUI):
    selector = settings_ui.device(
        descriptionMatches=INTERNET_TILE_PATTERN,
        clickable=True,
    )
    if not selector.wait(timeout=5.0):
        settings_ui.fail_with_artifacts("快捷设置面板未找到 WLAN/互联网磁贴")
    return selector


def _click_control(settings_ui: AndroidSettingsUI, control) -> None:
    bounds = control.info["bounds"]
    width = bounds["right"] - bounds["left"]
    x = bounds["right"] - max(20, width // 8)
    y = (bounds["top"] + bounds["bottom"]) // 2
    settings_ui.device.shell(f"input tap {x} {y}")


def wait_for_resource(
    settings_ui: AndroidSettingsUI,
    resource_id: str,
    timeout: float,
) -> bool:
    deadline = time.monotonic() + timeout
    marker = f'resource-id="{resource_id}"'
    while time.monotonic() < deadline:
        if marker in settings_ui.device.dump_hierarchy():
            return True
        time.sleep(0.3)
    return False


def wait_for_any_resource(
    settings_ui: AndroidSettingsUI,
    resource_ids: tuple[str, ...],
    timeout: float,
) -> bool:
    deadline = time.monotonic() + timeout
    markers = tuple(f'resource-id="{resource_id}"' for resource_id in resource_ids)
    while time.monotonic() < deadline:
        hierarchy = settings_ui.device.dump_hierarchy()
        if any(marker in hierarchy for marker in markers):
            return True
        time.sleep(0.3)
    return False


def open_internet_dialog(
    settings_ui: AndroidSettingsUI,
    *,
    capture: bool = True,
) -> float:
    started = time.monotonic()
    for _ in range(3):
        open_quick_settings(settings_ui)
        _click_control(settings_ui, internet_tile(settings_ui))
        if wait_for_resource(
            settings_ui,
            "com.android.systemui:id/internet_dialog_title",
            4.0,
        ):
            break
        settings_ui.device.shell("cmd statusbar collapse")
        time.sleep(0.8)
    else:
        settings_ui.fail_with_artifacts("点击 WLAN/互联网磁贴后未显示网络面板")
    if not wait_for_any_resource(
        settings_ui,
        (
            "com.android.systemui:id/wifi_connected_layout",
            "com.android.systemui:id/wifi_list",
            "com.android.systemui:id/wifi_toggle",
        ),
        5.0,
    ):
        settings_ui.fail_with_artifacts("网络面板未显示 WLAN 连接行或扫描列表")
    elapsed = time.monotonic() - started
    if capture:
        hierarchy = capture_systemui(settings_ui, "internet_dialog")
        if not re.search(r"WLAN|Wi-?Fi|互联网|Internet", hierarchy, re.IGNORECASE):
            settings_ui.fail_with_artifacts("点击 WLAN/互联网磁贴后未显示网络面板")
    return elapsed


def systemui_wifi_toggle(settings_ui: AndroidSettingsUI):
    toggle = settings_ui.device(resourceId="com.android.systemui:id/wifi_toggle")
    if not toggle.wait(timeout=5.0):
        settings_ui.fail_with_artifacts("SystemUI 网络面板未找到 WLAN 开关")
    return toggle


def set_wifi_enabled(settings_ui: AndroidSettingsUI, enabled: bool) -> None:
    open_internet_dialog(settings_ui, capture=False)
    toggle = systemui_wifi_toggle(settings_ui)
    if bool(toggle.info.get("checked")) != enabled:
        bounds = toggle.info["bounds"]
        center_x = (bounds["left"] + bounds["right"]) // 2
        center_y = (bounds["top"] + bounds["bottom"]) // 2
        settings_ui.device.shell(f"input tap {center_x} {center_y}")

    deadline = time.monotonic() + 5.0
    while time.monotonic() < deadline:
        toggle = settings_ui.device(resourceId="com.android.systemui:id/wifi_toggle")
        if toggle.exists and bool(toggle.info.get("checked")) == enabled:
            break
        time.sleep(0.2)
    else:
        settings_ui.fail_with_artifacts(
            f"SystemUI 互联网面板中的 WLAN 开关未切换为 {'开启' if enabled else '关闭'}"
        )

    done = settings_ui.device(resourceId="com.android.systemui:id/done_button")
    if not done.wait(timeout=5.0):
        settings_ui.fail_with_artifacts("SystemUI 互联网面板未找到完成按钮")
    _click_control(settings_ui, done)
    dialog = settings_ui.device(resourceId="com.android.systemui:id/internet_dialog_title")
    if not dialog.wait_gone(timeout=5.0):
        settings_ui.fail_with_artifacts("点击完成后 SystemUI 互联网面板未关闭")
    width, height = settings_ui.device.window_size()
    for command in (
        f"input swipe {width // 2} {height * 9 // 10} {width // 2} {height // 5} 300",
        f"input swipe {width // 2} {height * 9 // 16} {width // 2} {height // 10} 300",
        "cmd statusbar collapse",
    ):
        settings_ui.device.shell(command)
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            hierarchy = settings_ui.device.dump_hierarchy()
            if not any(
                marker in hierarchy
                for marker in (
                    "com.android.systemui:id/qs_frame",
                    "com.android.systemui:id/internet_dialog_title",
                )
            ):
                return
            time.sleep(0.2)
    settings_ui.fail_with_artifacts("点击完成、上滑并尝试收起后快速设置栏未退出")


def open_all_wifi_networks(settings_ui: AndroidSettingsUI) -> None:
    selector = settings_ui.device(resourceId="com.android.systemui:id/see_all_layout")
    if selector.click_exists(timeout=5.0):
        return
    selector = settings_ui.device(textMatches=SEE_ALL_PATTERN)
    if not selector.click_exists(timeout=3.0):
        settings_ui.fail_with_artifacts("未找到或无法点击查看全部/WLAN 设置按钮")