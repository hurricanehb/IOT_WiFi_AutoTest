"""Page object for the observed WiFi scan-list connection dialog."""
from __future__ import annotations

import time
from typing import Callable

from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


class WiFiConnectionConfigUI:
    def __init__(self, settings: AndroidSettingsUI) -> None:
        self.settings = settings
        self.device = settings.device

    def open_for_ssid(self, ssid: str, open_networks: Callable[[], None] | None = None) -> None:
        if open_networks is None:
            self.settings.open_wifi_settings()
        else:
            open_networks()
        self.settings.scroll_to_text(ssid)
        if not self.device(text=ssid).click_exists(timeout=5.0):
            self.settings.fail_with_artifacts(f"无法点击 WLAN 条目 {ssid!r}")
        time.sleep(1.0)

    def open_hyperwifi_intro(
        self, ssid: str, open_networks: Callable[[], None] | None = None
    ) -> None:
        if open_networks is None:
            self.settings.open_wifi_settings()
        else:
            open_networks()
        self.settings.scroll_to_text(ssid)
        title_bounds = self.device(text=ssid).info["bounds"]
        buttons = self.device(resourceId="com.android.settings:id/turbolink_button")
        for index in range(buttons.count):
            button = buttons[index]
            button_bounds = button.info["bounds"]
            if (
                button_bounds["top"] < title_bounds["bottom"]
                and button_bounds["bottom"] > title_bounds["top"]
            ):
                button.click()
                break
        else:
            self.settings.fail_with_artifacts(
                f"WLAN 条目 {ssid!r} 右侧未显示 HyperWiFi Logo"
            )

        if not self.device(
            resourceId="com.android.settings:id/lottie_view"
        ).wait(timeout=5.0):
            self.settings.fail_with_artifacts("点击 HyperWiFi Logo 后未显示介绍界面")

    def close_hyperwifi_intro(self) -> None:
        self.device(resourceId="android:id/button2").click_exists(timeout=2.0)

    def dialog_exists(self) -> bool:
        return self.device(resourceId="com.android.settings:id/l_wifidialog").exists

    def require_dialog(self, ssid: str) -> None:
        if not self.device(resourceId="com.android.settings:id/l_wifidialog").wait(timeout=5.0):
            self.settings.fail_with_artifacts(f"未显示 {ssid!r} 的连接配置框")

    def title(self) -> str:
        return self.device(resourceId="com.android.settings:id/alertTitle").get_text()

    def password_field(self):
        return self.device(resourceId="com.android.settings:id/password")

    def set_password(self, value: str) -> str:
        field = self.password_field()
        if not field.exists:
            self.settings.fail_with_artifacts("连接配置框未显示密码输入框")
        field.click()
        field.clear_text()
        field.set_text(value)
        time.sleep(0.2)
        actual = field.get_text()
        self.device.press("back")
        return actual

    def save_enabled(self) -> bool:
        button = self.device(resourceId="android:id/button1")
        if not button.exists:
            self.settings.fail_with_artifacts("连接配置框未显示保存按钮")
        return bool(button.info.get("enabled"))

    def save(self) -> None:
        if not self.save_enabled():
            self.settings.fail_with_artifacts("连接配置框保存按钮不可用")
        self.device(resourceId="android:id/button1").click()

    def cancel(self) -> None:
        self.device(resourceId="android:id/button2").click_exists(timeout=2.0)

    def toggle_password_visibility(self) -> bool:
        button = self.device(resourceId="com.android.settings:id/text_input_end_icon")
        if not button.exists:
            self.settings.fail_with_artifacts("连接配置框未显示密码可见性按钮")
        before = bool(button.info.get("checked"))
        button.click()
        time.sleep(0.2)
        after = bool(button.info.get("checked"))
        if after == before:
            self.settings.fail_with_artifacts("密码可见性按钮点击后状态未改变")
        return after

    def open_advanced_options(self) -> None:
        button = self.device(resourceId="com.android.settings:id/wifi_advanced_togglebox")
        if not button.click_exists(timeout=2.0):
            self.settings.fail_with_artifacts("连接配置框未显示高级选项入口")

    def ip_mode(self) -> str:
        selector = self.device(resourceId="com.android.settings:id/ip_settings")
        if not selector.exists:
            self.settings.fail_with_artifacts("高级选项未显示 IP 设置")
        return selector.get_text()

    def select_ip_mode(self, mode: str) -> None:
        selector = self.device(resourceId="com.android.settings:id/ip_settings")
        selector.click()
        for text in (mode, mode.upper()):
            if self.device(text=text).click_exists(timeout=1.0):
                return
        self.settings.fail_with_artifacts(f"IP 设置未提供选项 {mode!r}")