"""Page object for Android WiFi add-network dialog."""
from __future__ import annotations

import re
import time
from typing import Tuple
from xml.etree import ElementTree

import pytest
from uiautomator2.exceptions import UiObjectNotFoundError

from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


class WiFiAddNetworkUI:
    def __init__(self, settings: AndroidSettingsUI) -> None:
        self.settings = settings
        self.device = settings.device

    def open(self) -> None:
        self.settings.open_wifi_settings()
        for text in ("+ 添加网络", "添加网络", "Add network"):
            selector = self.device(text=text)
            if selector.exists:
                selector.click()
                break
            scrollable = self.device(scrollable=True)
            if scrollable.exists and scrollable.scroll.to(text=text):
                self.device(text=text).click()
                break
        else:
            self.settings.fail_with_artifacts("未找到添加网络入口")
        if not self._ssid_field().wait(timeout=5.0):
            self.settings.fail_with_artifacts("添加网络页面未显示 SSID 输入框")

    def set_ssid(self, value: str) -> str:
        return self._set_text(self._ssid_field(), value, "SSID")

    def set_password(self, value: str) -> str:
        field = self._password_field()
        if not field.exists:
            self.settings.fail_with_artifacts("当前安全类型未显示密码输入框")
        return self._set_text(field, value, "密码")

    def select_security(self, security: str) -> None:
        spinner = self._security_spinner()
        spinner.click()
        aliases = {
            "open": ("无", "None"),
            "personal": ("WPA/WPA2-Personal", "WPA2-Personal"),
            "wpa3": ("WPA3-Personal",),
        }
        options = aliases.get(security, (security,))
        for attempt in range(2):
            for option in options:
                if self.device(text=option).click_exists(timeout=1):
                    time.sleep(0.3)
                    return
            if attempt == 0:
                self.settings.reset_uiautomator()
        self.settings.fail_with_artifacts(f"未找到安全性选项 {options!r}")

    def security_options(self) -> Tuple[str, ...]:
        """打开安全性下拉框并返回当前 ROM 提供的可见选项。"""
        self._security_spinner().click()
        time.sleep(0.3)
        hierarchy = self.device.dump_hierarchy()
        try:
            root = ElementTree.fromstring(hierarchy)
        except ElementTree.ParseError:
            self.settings.fail_with_artifacts("安全性选项控件树解析失败")
            return ()
        finally:
            self.device.press("back")

        options = []
        for node in root.iter("node"):
            text = (node.attrib.get("text") or "").strip()
            if text and text not in options:
                options.append(text)
        return tuple(options)

    def select_hidden(self, hidden: bool) -> None:
        advanced = self.device(
            resourceId="com.android.settings:id/wifi_advanced_togglebox"
        )
        if advanced.exists:
            advanced.click()
        spinner = self.device(resourceId="com.android.settings:id/hidden_settings")
        if not spinner.exists:
            pytest.skip("当前 Android 添加网络页面无“隐藏的网络”选项")
        spinner.click()
        options = ("是", "Yes") if hidden else ("否", "No")
        for option in options:
            if self.device(text=option).click_exists(timeout=1):
                time.sleep(0.3)
                return
        self.settings.fail_with_artifacts(f"未找到隐藏网络选项 {options!r}")

    def save_enabled(self) -> bool:
        button = self._save_button()
        if not button.exists:
            self._scroll_to_end()
            button = self._save_button()
        if not button.exists:
            self.settings.reset_uiautomator()
            self._scroll_to_end()
            button = self._save_button()
            if not button.exists:
                self.settings.fail_with_artifacts("未找到保存按钮")
        return bool(button.info.get("enabled"))

    def save(self) -> None:
        if not self.save_enabled():
            self.settings.fail_with_artifacts("保存按钮不可用")
        self._save_button().click()

    def save_rejection_message(self, timeout: float = 5.0) -> str:
        if not self.save_enabled():
            return "保存按钮不可用"
        self.device.toast.reset()
        self._save_button().click()
        message = self.device.toast.get_message(
            wait_timeout=timeout,
            cache_timeout=10.0,
            default="",
        ) or ""
        if re.search(r"无法保存网络|不能保存网络|unable to save network|couldn.?t save network", message, re.IGNORECASE):
            return message
        hierarchy = self.device.dump_hierarchy()
        match = re.search(
            r"无法保存网络|不能保存网络|unable to save network|couldn.?t save network",
            hierarchy,
            re.IGNORECASE,
        )
        if match:
            return match.group(0)
        return ""

    def cancel(self) -> None:
        self.device.press("back")

    def _security_spinner(self):
        spinner = self.device(resourceId="com.android.settings:id/security")
        if spinner.exists:
            return spinner
        spinners = self.device(className="android.widget.Spinner")
        if spinners.count < 1:
            self.settings.fail_with_artifacts("未找到安全性选项")
        return spinners[0]

    def _ssid_field(self):
        field = self.device(resourceId="com.android.settings:id/ssid")
        if field.exists:
            return field
        return self.device(className="android.widget.EditText", instance=0)

    def _password_field(self):
        field = self.device(resourceId="com.android.settings:id/password")
        if field.exists:
            return field
        fields = self.device(className="android.widget.EditText")
        return fields[1] if fields.count > 1 else field

    def _save_button(self):
        button = self.device(resourceId="android:id/button1")
        if button.exists:
            return button
        for text in ("保存", "连接", "Save", "Connect"):
            button = self.device(text=text, className="android.widget.Button")
            if button.exists:
                return button
        return button

    def _scroll_to_end(self) -> None:
        scrollable = self.device(scrollable=True)
        if scrollable.exists:
            try:
                scrollable.scroll.toEnd()
            except UiObjectNotFoundError:
                pass

    def _set_text(self, field, value: str, label: str) -> str:
        if not field.exists:
            self.settings.fail_with_artifacts(f"未找到 {label} 输入框")
        field.click()
        field.clear_text()
        field.set_text(value)
        time.sleep(0.2)
        actual = field.get_text()
        self.device.press("back")
        return actual