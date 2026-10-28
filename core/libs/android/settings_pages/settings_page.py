"""UIAutomator2 wrapper for Android system Settings pages."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import uiautomator2 as u2


class AndroidSettingsUI:
    def __init__(self, serial: str, artifact_dir: Path) -> None:
        self.serial = serial
        self.artifact_dir = artifact_dir
        self._connect()

    def _connect(self) -> None:
        self.device = u2.connect(self.serial)
        self.device.settings["wait_timeout"] = 10.0

    def prepare(self) -> None:
        for attempt in range(2):
            try:
                self.device.screen_on()
                self.device.shell("wm dismiss-keyguard")
                self.device.info
                break
            except Exception:
                if attempt == 1:
                    raise
                self._connect()
                self.reset_uiautomator()
        self.device.shell("am force-stop com.android.vending")
        self.device.press("home")
        time.sleep(0.5)

    def open_wifi_settings(self) -> None:
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
                "am start -W -a android.settings.WIFI_SETTINGS -f 0x10008000"
            )
            if self._wifi_page_title().wait(timeout=10.0):
                return
        self.fail_with_artifacts("WiFi 设置页未显示 WLAN")

    def _wifi_settings_switch(self) -> Any:
        switch = self.device(
            packageName="com.android.settings",
            resourceIdMatches=r"^(?:com\.android\.settings:id/switchWidget|android:id/switch_widget)$",
        )
        if not switch.wait(timeout=5.0):
            self.fail_with_artifacts("WLAN 设置页未找到开关控件")
        return switch

    def wifi_switch_checked(self) -> bool:
        switch = self._wifi_settings_switch()
        return bool(switch.info.get("checked"))

    def set_wifi_switch(self, enabled: bool, *, timeout: float = 8.0) -> None:
        self.open_wifi_settings()
        switch = self._wifi_settings_switch()
        if bool(switch.info.get("checked")) == enabled:
            return
        switch.click()
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.wifi_switch_checked() == enabled:
                return
            time.sleep(0.3)
        self.fail_with_artifacts(
            f"WLAN 开关点击后未切换为 {'开启' if enabled else '关闭'}"
        )

    def set_quick_settings_wifi_enabled(self, enabled: bool) -> None:
        from core.libs.android.systemui_pages.quick_settings_page import set_wifi_enabled

        set_wifi_enabled(self, enabled)

    def reset_uiautomator(self) -> None:
        self.device.reset_uiautomator()
        time.sleep(1.0)

    def _wifi_page_title(self) -> Any:
        return self.device(
            packageName="com.android.settings",
            textMatches=r"(?i)^(WLAN|Wi-?Fi)$",
        )

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
        hierarchy_path = self.artifact_dir / "settings_ui_failure.xml"
        screenshot_path = self.artifact_dir / "settings_ui_failure.png"
        hierarchy_path.write_text(self.device.dump_hierarchy(), encoding="utf-8")
        self.device.screenshot(str(screenshot_path))
        raise AssertionError(
            f"{message}；UI hierarchy={hierarchy_path}，screenshot={screenshot_path}"
        )

    def press_back(self) -> None:
        self.device.press("back")