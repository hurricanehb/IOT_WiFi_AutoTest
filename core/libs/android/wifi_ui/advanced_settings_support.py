"""Device and lifecycle UI support owned by WLAN advanced-settings tests."""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable, cast

import uiautomator2 as u2

from core.utils.log_handler import get_logger


class AdvancedSettingsSupportUI:
    def __init__(self, serial: str, artifact_dir: Path) -> None:
        self.serial = serial
        self.artifact_dir = artifact_dir
        self.device = u2.connect(serial)
        self.device.settings["wait_timeout"] = 10.0

    def open_wifi_settings(self) -> None:
        for attempt in range(3):
            if attempt == 0:
                self.device.shell("am force-stop com.android.settings")
            elif attempt == 1:
                self.reset_uiautomator()
            elif attempt == 2:
                self.device.press("home")
                self.device.shell("am force-stop com.android.settings")
                self.reset_uiautomator()
            self.device.shell(
                "am start -W -a android.settings.WIFI_SETTINGS -f 0x10008000"
            )
            if self._wifi_page_title().wait(timeout=10.0):
                return
        self.fail_with_artifacts("WiFi 设置页未显示 WLAN")

    def open_airplane_mode_settings(self) -> None:
        """Open the system Airplane mode settings page."""
        self.device.screen_on()
        self.device.shell("wm dismiss-keyguard")
        for attempt in range(3):
            if attempt == 1:
                self.reset_uiautomator()
            elif attempt == 2:
                self.device.press("home")
                self.device.shell("am force-stop com.android.settings")
                self.reset_uiautomator()
            self.device.shell(
                "am start -W -a android.settings.AIRPLANE_MODE_SETTINGS -f 0x10008000"
            )
            if self._airplane_mode_page_title().wait(timeout=10.0):
                return
        self.fail_with_artifacts("飞行模式设置页未显示")

    def reset_uiautomator(self) -> None:
        self.device.reset_uiautomator()
        time.sleep(1.0)

    def set_wifi_switch(self, enabled: bool) -> None:
        self.set_wifi_enabled_from_settings(enabled)

    def set_wifi_enabled_from_settings(self, enabled: bool) -> None:
        """Set WLAN through the visible Internet page in Android Settings."""
        self.open_wifi_settings()
        switch = self._wifi_settings_switch()
        if self._selector_is_checked(switch) != enabled:
            bounds = switch.info["bounds"]
            self.device.click(
                (bounds["left"] + bounds["right"]) // 2,
                (bounds["top"] + bounds["bottom"]) // 2,
            )

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            switch = self._wifi_settings_switch()
            if self._selector_is_checked(switch) == enabled:
                return
            time.sleep(0.2)
        self.fail_with_artifacts(
            f"互联网页面的 WLAN 开关未切换为 {'开启' if enabled else '关闭'}"
        )

    def set_airplane_mode_from_settings(
        self, enabled: bool, *, timeout: float = 8.0
    ) -> None:
        """Set Airplane mode through its visible Android Settings page."""
        self.open_airplane_mode_settings()
        switch = self._airplane_mode_settings_switch()
        if self._selector_is_checked(switch) == enabled:
            return
        self._click_selector_center(switch)

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            switch = self._airplane_mode_settings_switch()
            if self._selector_is_checked(switch) == enabled:
                return
            time.sleep(0.3)
        self.fail_with_artifacts(
            f"飞行模式设置页的开关未切换为 {'开启' if enabled else '关闭'}"
        )

    def set_quick_settings_wifi_enabled(self, enabled: bool) -> None:
        from core.libs.android.systemui_pages.quick_settings_page import (
            open_internet_dialog,
            systemui_wifi_toggle,
        )

        navigation_ui = cast(Any, self)
        open_internet_dialog(navigation_ui, capture=False)
        toggle = systemui_wifi_toggle(navigation_ui)
        if self._selector_is_checked(toggle) != enabled:
            bounds = toggle.info["bounds"]
            center_x = (bounds["left"] + bounds["right"]) // 2
            center_y = (bounds["top"] + bounds["bottom"]) // 2
            self.device.shell(f"input tap {center_x} {center_y}")

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            toggle = self.device(resourceId="com.android.systemui:id/wifi_toggle")
            if toggle.exists and self._selector_is_checked(toggle) == enabled:
                get_logger(__name__).info(
                    "SystemUI WLAN 开关状态已确认：%s", "开启" if enabled else "关闭"
                )
                self._close_quick_settings_internet_panel()
                return
            time.sleep(0.2)
        self.fail_with_artifacts(
            f"SystemUI 互联网面板中的 WLAN 开关未切换为 {'开启' if enabled else '关闭'}"
        )

    def _close_quick_settings_internet_panel(self) -> None:
        """Re-locate Done after WLAN-driven dialog layout changes."""
        for attempt in range(3):
            done = self.device(
                resourceId="com.android.systemui:id/done_button",
                enabled=True,
                clickable=True,
            )
            if not done.wait(timeout=5.0):
                self.fail_with_artifacts("SystemUI 互联网面板未找到可点击的完成按钮")
            bounds = done.info["bounds"]
            center_x = (bounds["left"] + bounds["right"]) // 2
            center_y = (bounds["top"] + bounds["bottom"]) // 2
            get_logger(__name__).info(
                "SystemUI 完成按钮点击：attempt=%s, center=(%s, %s)",
                attempt + 1, center_x, center_y,
            )
            self.device.shell(f"input tap {center_x} {center_y}")
            dialog = self.device(resourceId="com.android.systemui:id/internet_dialog_title")
            if dialog.wait_gone(timeout=2.0):
                self._dismiss_quick_settings()
                return
        self.fail_with_artifacts("重新定位并点击完成后 SystemUI 互联网面板仍未关闭")

    def _dismiss_quick_settings(self) -> None:
        """Dismiss the shade and verify its hierarchy is no longer visible."""
        width, height = self.device.window_size()
        for command in (
            f"input swipe {width // 2} {height * 9 // 10} {width // 2} {height // 5} 300",
            f"input swipe {width // 2} {height * 9 // 16} {width // 2} {height // 10} 300",
            "cmd statusbar collapse",
        ):
            self.device.shell(command)
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                hierarchy = self.device.dump_hierarchy()
                if not any(
                    marker in hierarchy
                    for marker in (
                        "com.android.systemui:id/qs_frame",
                        "com.android.systemui:id/internet_dialog_title",
                    )
                ):
                    return
                time.sleep(0.2)
        self.fail_with_artifacts("点击完成、上滑并尝试收起后快速设置栏未退出")

    def _quick_settings_is_foreground(self) -> bool:
        current_app = self.device.app_current()
        return current_app.get("package") == "com.android.systemui"

    def _wifi_settings_switch(self) -> Any:
        switch = self.device(
            packageName="com.android.settings",
            resourceIdMatches=r"^(?:com\.android\.settings:id/switchWidget|android:id/switch_widget)$",
        )
        if not switch.wait(timeout=5.0):
            self.fail_with_artifacts("未找到互联网页面的 WLAN 开关")
        return switch

    @staticmethod
    def _selector_is_checked(selector: Any) -> bool:
        return bool(selector.info.get("checked"))

    def _quick_settings_entry(self, labels: Iterable[str]) -> Any | None:
        for label in labels:
            pattern = self._quick_settings_label_pattern(label)
            for selector in (
                self.device(descriptionMatches=pattern),
                self.device(textMatches=pattern),
            ):
                if selector.exists:
                    return selector
        return None

    def _wait_for_quick_settings_entry(
        self, labels: Iterable[str], timeout: float = 5.0
    ) -> Any | None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            entry = self._quick_settings_entry(labels)
            if entry is not None:
                return entry
            time.sleep(0.2)
        return None

    def _click_selector_center(self, selector: Any) -> None:
        bounds = selector.info["bounds"]
        self.device.click(
            (bounds["left"] + bounds["right"]) // 2,
            (bounds["top"] + bounds["bottom"]) // 2,
        )

    def _click_quick_settings_internet_panel_entry(self, selector: Any) -> None:
        """Open Internet panel from the chevron in a split Quick Settings tile."""
        bounds = selector.info["bounds"]
        chevron_center = self._quick_settings_chevron_center(
            self.device.dump_hierarchy(), bounds
        )
        if chevron_center is not None:
            self.device.click(*chevron_center)
            return
        self._click_selector_center(selector)

    @staticmethod
    def _quick_settings_chevron_center(
        hierarchy: str, tile_bounds: dict[str, int]
    ) -> tuple[int, int] | None:
        """Return the Internet tile's chevron center when System UI exposes one."""
        root = ET.fromstring(hierarchy)
        adjacent_chevrons: list[tuple[int, int, int]] = []
        for node in root.iter("node"):
            if node.attrib.get("resource-id") != "com.android.systemui:id/chevron":
                continue
            match = re.fullmatch(
                r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",
                node.attrib.get("bounds", ""),
            )
            if match is None:
                continue
            left, top, right, bottom = map(int, match.groups())
            if not (
                tile_bounds["left"] <= left
                and right <= tile_bounds["right"]
                and tile_bounds["top"] <= top
                and bottom <= tile_bounds["bottom"]
            ):
                if (
                    left >= tile_bounds["right"]
                    and top <= tile_bounds["bottom"]
                    and bottom >= tile_bounds["top"]
                ):
                    adjacent_chevrons.append(
                        (
                            abs((top + bottom) // 2 - (tile_bounds["top"] + tile_bounds["bottom"]) // 2),
                            (left + right) // 2,
                            (top + bottom) // 2,
                        )
                    )
                continue
            return (left + right) // 2, (top + bottom) // 2

        if adjacent_chevrons:
            _, center_x, center_y = min(adjacent_chevrons)
            return center_x, center_y

        return None

    def _quick_settings_tile(self, labels: Iterable[str]) -> Any | None:
        for label in labels:
            pattern = self._quick_settings_label_pattern(label)
            for selector in (
                self.device(descriptionMatches=pattern),
                self.device(textMatches=pattern),
            ):
                if selector.exists and selector.info.get("checkable"):
                    return selector
        return None

    @staticmethod
    def _quick_settings_tile_is_enabled(tile: Any) -> bool:
        return bool(tile.info.get("checked"))

    @staticmethod
    def _quick_settings_label_pattern(label: str) -> str:
        compact_label = "".join(label.split())
        return (
            r"^\s*"
            + r"\s*".join(re.escape(character) for character in compact_label)
            + r"\s*(?:[,，].*)?$"
        )

    def _wifi_page_title(self) -> Any:
        return self.device(textMatches=r"(?i)^(WLAN|Wi-?Fi)$")

    def _airplane_mode_page_title(self) -> Any:
        return self.device(
            packageName="com.android.settings",
            textMatches=r"(?i)^(飞行模式|Airplane mode)$",
        )

    def _airplane_mode_settings_switch(self) -> Any:
        switch = self.device(
            packageName="com.android.settings",
            resourceIdMatches=r"^(?:com\.android\.settings:id/switchWidget|android:id/switch_widget)$",
        )
        if not switch.wait(timeout=5.0):
            self.fail_with_artifacts("未找到飞行模式设置页的开关")
        return switch

    def require_text(self, text: str, timeout: float = 10.0) -> Any:
        selector = self.device(text=text)
        if not selector.wait(timeout=timeout):
            self.fail_with_artifacts(f"未找到文本控件 {text!r}")
        return selector

    def click_text(self, text: str, timeout: float = 10.0) -> None:
        if not self.device(text=text).click_exists(timeout=timeout):
            self.fail_with_artifacts(f"无法点击文本控件 {text!r}")

    def click_description(self, description: str, timeout: float = 10.0) -> None:
        if not self.device(description=description).click_exists(timeout=timeout):
            self.fail_with_artifacts(f"无法点击无障碍控件 {description!r}")

    def scroll_to_text(self, text: str) -> None:
        for attempt in range(2):
            if self.device(text=text).wait(timeout=12.0):
                return
            scrollable = self.device(scrollable=True)
            if scrollable.exists and scrollable.scroll.to(text=text):
                return
            if attempt == 0:
                self.device.shell("cmd wifi start-scan")
                time.sleep(3.0)
        self.fail_with_artifacts(f"页面中未找到可滚动文本 {text!r}")

    def _click_qr_scanner_button(self) -> None:
        selectors = (
            self.device(resourceId="com.android.settings:id/button_icon"),
            self.device(description="扫描二维码"),
            self.device(description="Scan QR code"),
        )
        for selector in selectors:
            if selector.click_exists(timeout=2.0):
                return
        self.fail_with_artifacts("未找到 WiFi 扫描二维码按钮")

    def open_wifi_qr_scanner(self, entry_point: str) -> None:
        """Open the camera scanner through one of the two documented paths."""
        self.open_wifi_settings()
        add_network_text = "+ 添加网络"
        try:
            self.scroll_to_text(add_network_text)
        except AssertionError:
            add_network_text = "Add network"
            self.scroll_to_text(add_network_text)

        if entry_point == "add_network_entry":
            self._click_qr_scanner_button()
            return
        if entry_point == "ssid_editor":
            self.click_text(add_network_text)
            self._click_qr_scanner_button()
            return
        raise ValueError(f"未知 WiFi 扫码入口: {entry_point!r}")

    def fail_with_artifacts(self, message: str) -> None:
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        hierarchy_path = self.artifact_dir / "advanced_settings_ui_failure.xml"
        screenshot_path = self.artifact_dir / "advanced_settings_ui_failure.png"
        hierarchy_path.write_text(self.device.dump_hierarchy(), encoding="utf-8")
        self.device.screenshot(str(screenshot_path))
        raise AssertionError(
            f"{message}；UI hierarchy={hierarchy_path}，screenshot={screenshot_path}"
        )

    def press_back(self) -> None:
        self.device.press("back")