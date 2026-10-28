"""Page object for Android WiFi DHCP/static IP settings."""
from __future__ import annotations

import time
from typing import Dict, List

from uiautomator2.exceptions import UiObjectNotFoundError

from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


STATIC_FIELD_ORDER = ("ip_address", "gateway", "prefix_length", "dns1", "dns2")
STATIC_FIELD_LABELS = ("IP 地址", "网关", "网络前缀长度")
STATIC_FIELD_LABEL_PREFIX = {
    "ip_address": "IP 地址",
    "gateway": "网关",
    "prefix_length": "网络前缀长度",
    "dns1": "DNS 1",
    "dns2": "DNS 2",
}
STATIC_FIELD_RESOURCE_ID = {
    "ip_address": "com.android.settings:id/ipaddress",
    "gateway": "com.android.settings:id/gateway",
    "prefix_length": "com.android.settings:id/network_prefix_length",
    "dns1": "com.android.settings:id/dns1",
    "dns2": "com.android.settings:id/dns2",
}
STATIC_FIELD_CLEAR_RESOURCE_ID = {
    name: resource_id.replace(":id/", ":id/clear_")
    for name, resource_id in STATIC_FIELD_RESOURCE_ID.items()
}
IP_SETTINGS_RESOURCE_ID = "com.android.settings:id/ip_settings"
SAVE_BUTTON_RESOURCE_ID = "android:id/button1"
CANCEL_BUTTON_RESOURCE_ID = "android:id/button2"


class WiFiIPSettingsUI:
    def __init__(self, settings: AndroidSettingsUI) -> None:
        self.settings = settings
        self.device = settings.device

    def open_network_editor(self, ssid: str) -> None:
        for attempt in range(2):
            self.settings.open_wifi_settings()
            self.settings.scroll_to_text(ssid)
            self.settings.click_text(ssid)
            edit = self.device(description="修改")
            width, height = self.device.window_size()
            if width > height and edit.exists:
                bounds = edit.info["bounds"]
                x = (bounds["left"] + bounds["right"]) // 2
                y = (bounds["top"] + bounds["bottom"]) // 2
                self.device.shell(f"input tap {x} {y}")
            else:
                self.settings.click_description("修改")
            title = self.device(resourceId="com.android.settings:id/alertTitle")
            dialog_open = title.wait(timeout=3.0)
            if not dialog_open:
                self.settings.fail_with_artifacts("未打开 WiFi 修改对话框")
            focused_password = self.device(
                resourceId="com.android.settings:id/password", focused=True
            )
            if focused_password.exists:
                self.device.press("back")
                time.sleep(0.5)
            ip_spinner = self.device(resourceId="com.android.settings:id/ip_settings")
            if not ip_spinner.exists:
                self._scroll_dialog_to(IP_SETTINGS_RESOURCE_ID)
                toggle = self.device(
                    resourceId="com.android.settings:id/wifi_advanced_togglebox"
                )
                if not toggle.exists:
                    self._scroll_dialog_to(
                        "com.android.settings:id/wifi_advanced_togglebox"
                    )
                if toggle.wait(timeout=3.0):
                    if width > height:
                        bounds = toggle.info["bounds"]
                        x = (bounds["left"] + bounds["right"]) // 2
                        y = (bounds["top"] + bounds["bottom"]) // 2
                        self.device.shell(f"input tap {x} {y}")
                    else:
                        toggle.click()
                    time.sleep(0.5)
                    self._scroll_dialog_to(IP_SETTINGS_RESOURCE_ID)
            if ip_spinner.wait(timeout=5.0):
                return
            cancel = self.device(resourceId="android:id/button2")
            if cancel.exists:
                cancel.click()
            if attempt == 0:
                time.sleep(1.0)
        self.settings.fail_with_artifacts("未找到 IP 设置控件")

    def open_network_connection_editor(self, ssid: str, password: str) -> None:
        self.settings.open_wifi_settings()
        self.settings.scroll_to_text(ssid)
        self.settings.click_text(ssid)
        password_field = self.device(resourceId="com.android.settings:id/password")
        if not password_field.wait(timeout=5.0):
            self.settings.fail_with_artifacts("未打开 WiFi 连接对话框")
        password_field.set_text(password)
        if self.device(
            resourceId="com.android.settings:id/password", focused=True
        ).exists:
            self.device.press("back")
            time.sleep(0.5)
        if not self.device(resourceId="com.android.settings:id/privacy_settings").exists:
            toggle = self.device(
                resourceId="com.android.settings:id/wifi_advanced_togglebox"
            )
            if toggle.exists:
                self._click_control(toggle)
                time.sleep(0.5)
            self._scroll_dialog_to("com.android.settings:id/privacy_settings")
        if not self.device(
            resourceId="com.android.settings:id/privacy_settings"
        ).wait(timeout=3.0):
            self.settings.fail_with_artifacts("WiFi 连接对话框未显示隐私设置")

    def _scroll_dialog_to(self, resource_id: str) -> bool:
        for _ in range(2):
            scrollable = self.device(
                className="android.widget.ScrollView", scrollable=True
            )
            if not scrollable.wait(timeout=2.0):
                continue
            try:
                return bool(scrollable.scroll.to(resourceId=resource_id))
            except UiObjectNotFoundError:
                time.sleep(0.5)
        return False

    def current_ip_mode(self) -> str:
        spinner = self.device(resourceId=IP_SETTINGS_RESOURCE_ID)
        if spinner.exists:
            spinner_text = spinner.get_text() or ""
            for mode in ("DHCP", "静态"):
                if mode in spinner_text:
                    return mode
        for mode in ("DHCP", "静态"):
            if self.device(text=mode).exists:
                return mode
        self.settings.fail_with_artifacts("IP 设置未显示 DHCP 或静态")
        return ""

    def ip_mode_options(self) -> List[str]:
        self._ip_mode_spinner().click()
        options = [mode for mode in ("DHCP", "静态") if self.device(text=mode).exists]
        self.device.press("back")
        return options

    def select_ip_mode(self, mode: str) -> None:
        if mode not in ("DHCP", "静态"):
            raise ValueError(f"不支持的 IP 模式: {mode!r}")
        if self.current_ip_mode() == mode:
            return
        self._click_control(self._ip_mode_spinner())
        option = self.device(text=mode)
        if not option.wait(timeout=3.0):
            self.settings.fail_with_artifacts(f"IP 设置选项未显示 {mode!r}")
        self._click_control(option)
        self.settings.require_text(mode)
        time.sleep(0.5)

    def current_privacy_mode(self) -> str:
        aliases = {
            "device": ("使用设备 MAC", "Use device MAC"),
            "randomized": (
                "使用随机 MAC",
                "使用随机分配的 MAC",
                "Use randomized MAC",
            ),
        }
        selector = self.device(resourceId="com.android.settings:id/privacy_settings")
        selector_text = selector.get_text() if selector.exists else ""
        if not isinstance(selector_text, str):
            selector_text = ""
        for mode, labels in aliases.items():
            if any(label in selector_text for label in labels):
                return mode
        for mode, labels in aliases.items():
            if any(self.device(text=label).exists for label in labels):
                return mode
        self.settings.fail_with_artifacts("未找到当前 WiFi 隐私模式")
        return ""

    def select_privacy_mode(self, mode: str) -> None:
        aliases = {
            "device": ("使用设备 MAC", "Use device MAC"),
            "randomized": (
                "使用随机 MAC",
                "使用随机分配的 MAC",
                "Use randomized MAC",
            ),
        }
        if mode not in aliases:
            raise ValueError(f"不支持的 WiFi 隐私模式: {mode!r}")
        if self.current_privacy_mode() == mode:
            return
        selector = self.device(resourceId="com.android.settings:id/privacy_settings")
        if not selector.exists:
            current = self.current_privacy_mode()
            current_labels = aliases[current]
            selector = next(
                (self.device(text=label) for label in current_labels if self.device(text=label).exists),
                selector,
            )
        if not selector.exists:
            self.settings.fail_with_artifacts("未找到 WiFi 隐私模式控件")
        self._click_control(selector)
        for label in aliases[mode]:
            option = self.device(text=label)
            if option.wait(timeout=1.0):
                self._click_control(option)
                time.sleep(0.5)
                return
        self.settings.fail_with_artifacts(f"未找到 WiFi 隐私模式 {mode!r}")

    def static_field_labels(self) -> List[str]:
        self.device(scrollable=True).scroll.toEnd()
        labels = [label for label in STATIC_FIELD_LABELS if self.device(text=label).exists]
        dns_nodes = self.device(textMatches=r"DNS [12].*")
        labels.extend(dns_nodes[index].get_text() for index in range(dns_nodes.count))
        return labels

    def fill_static(self, values: Dict[str, str]) -> None:
        missing = [name for name in STATIC_FIELD_ORDER if name not in values]
        if missing:
            raise ValueError(f"静态 IP 配置缺少字段: {missing!r}")
        for name in STATIC_FIELD_ORDER:
            self.set_static_field(name, values[name])

    def set_static_field(self, name: str, value: str) -> str:
        if name not in STATIC_FIELD_ORDER:
            raise ValueError(f"未知静态 IP 字段: {name!r}")
        if not value:
            field = self._static_field(name)
            clear_button = self.device(resourceId=STATIC_FIELD_CLEAR_RESOURCE_ID[name])
            if clear_button.exists:
                clear_button.click()
                time.sleep(0.3)
                return field.get_text()
        actual = ""
        for attempt in range(2):
            field = self._static_field(name)
            bounds = field.info["bounds"]
            self.device.click(
                (bounds["left"] + bounds["right"]) // 2,
                (bounds["top"] + bounds["bottom"]) // 2,
            )
            focused = self.device(resourceId=STATIC_FIELD_RESOURCE_ID[name])
            if not focused.wait(timeout=3.0):
                self.settings.fail_with_artifacts(f"字段 {name!r} 不可操作")
            focused.clear_text()
            focused.set_text(value)
            time.sleep(0.3)
            if not value:
                return focused.get_text()
            actual = focused.get_text()
            if actual == value:
                return actual
            if attempt == 0:
                time.sleep(0.5)
        return actual

    def _finish_input(self) -> None:
        actions_visible = self.device(resourceId=SAVE_BUTTON_RESOURCE_ID).exists or self.device(
            resourceId=CANCEL_BUTTON_RESOURCE_ID
        ).exists
        if actions_visible:
            return
        focused_input = self.device(className="android.widget.EditText", focused=True)
        if focused_input.exists:
            self.device.press("enter")
            time.sleep(0.3)
        actions_visible = self.device(resourceId=SAVE_BUTTON_RESOURCE_ID).exists or self.device(
            resourceId=CANCEL_BUTTON_RESOURCE_ID
        ).exists
        if not actions_visible and self.device(
            resourceId="com.android.settings:id/alertTitle"
        ).exists:
            self.device.press("back")
            time.sleep(0.3)

    def static_values(self) -> Dict[str, str]:
        return {name: self._static_field(name).get_text() for name in STATIC_FIELD_ORDER}

    def static_value(self, name: str) -> str:
        return self._static_field(name).get_text()

    def save_enabled(self) -> bool:
        self._finish_input()
        button = self.device(resourceId=SAVE_BUTTON_RESOURCE_ID)
        if not button.exists:
            button = self.device(text="保存", className="android.widget.Button")
        if not button.exists:
            self.settings.fail_with_artifacts("未找到保存按钮")
        return bool(button.info.get("enabled"))

    def save(self) -> None:
        if not self.save_enabled():
            self.settings.fail_with_artifacts("保存按钮不可用")
        button = self.device(resourceId=SAVE_BUTTON_RESOURCE_ID)
        if not button.exists:
            button = self.device(text="保存", className="android.widget.Button")
        self._click_control(button)

    def cancel(self) -> None:
        self._finish_input()
        if self.device(resourceId=CANCEL_BUTTON_RESOURCE_ID).click_exists(timeout=3.0):
            return
        if self.device(text="取消").click_exists(timeout=3.0):
            return
        self.settings.press_back()

    def _ip_mode_spinner(self):
        spinners = self.device(className="android.widget.Spinner")
        if spinners.count < 2:
            self.settings.fail_with_artifacts(
                f"高级选项应至少有代理/IP 两个 Spinner，实际={spinners.count}"
            )
        return spinners[1]

    def _click_control(self, control) -> None:
        width, height = self.device.window_size()
        if width > height:
            bounds = control.info["bounds"]
            x = (bounds["left"] + bounds["right"]) // 2
            y = (bounds["top"] + bounds["bottom"]) // 2
            self.device.shell(f"input tap {x} {y}")
            return
        control.click()

    def _static_field(self, name: str):
        resource_id = STATIC_FIELD_RESOURCE_ID[name]
        field = self.device(resourceId=resource_id)
        if field.exists:
            return field
        if not self.device(resourceId="com.android.settings:id/alertTitle").exists:
            self.settings.fail_with_artifacts(
                f"查找字段 {name!r} 时编辑对话框已关闭"
            )
        scrollable = self.device(scrollable=True)
        if scrollable.exists and scrollable.scroll.to(resourceId=resource_id):
            field = self.device(resourceId=resource_id)
            if field.exists:
                return field

        prefix = STATIC_FIELD_LABEL_PREFIX[name]
        if not scrollable.scroll.to(textStartsWith=prefix):
            self.settings.fail_with_artifacts(f"未找到静态 IP 字段标签 {prefix!r}")
        label = self.device(textStartsWith=prefix)
        label_bottom = label.info["bounds"]["bottom"]
        fields = self.device(className="android.widget.EditText")
        candidates = [
            fields[index]
            for index in range(fields.count)
            if fields[index].info["bounds"]["top"] >= label_bottom
        ]
        if not candidates:
            self.settings.fail_with_artifacts(f"标签 {prefix!r} 下方没有输入框")
        return min(candidates, key=lambda item: item.info["bounds"]["top"])