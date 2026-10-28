"""UIAutomator2 helper for the Welcome WLAN list."""
from __future__ import annotations

import random
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn

from core.utils.log_handler import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class HyperWiFiLabel:
    ssid: str
    bounds: dict[str, int]


@dataclass(frozen=True)
class WelcomeWifiNetwork:
    ssid: str
    bounds: dict[str, int]


class WelcomeWlanUI:
    WELCOME_PACKAGE = "com.sunmi.welcome"
    SSID_RESOURCE_ID = "com.sunmi.welcome:id/item_tv_wifi_name"
    LOCK_RESOURCE_ID = "com.sunmi.welcome:id/item_iv_lock"
    PASSWORD_RESOURCE_ID = "com.sunmi.welcome:id/et_content"
    PASSWORD_HINT_TEXT = "请输入密码"
    CLEAR_PASSWORD_RESOURCE_ID = "com.sunmi.welcome:id/iv_clear"
    PASSWORD_VISIBILITY_RESOURCE_ID = "com.sunmi.welcome:id/cb_password"
    ADVANCED_OPTIONS_RESOURCE_ID = "com.sunmi.welcome:id/cb_options"
    IP_SELECTOR_RESOURCE_ID = "com.sunmi.welcome:id/ll_ip_selector"
    IP_MODE_TEXT_RESOURCE_ID = "com.sunmi.welcome:id/tv_ip_selector"
    STATIC_IP_RESOURCE_ID = "com.sunmi.welcome:id/rl_static"
    DHCP_IP_RESOURCE_ID = "com.sunmi.welcome:id/rl_dhcp"
    CANCEL_RESOURCE_ID = "com.sunmi.welcome:id/btn_negative"
    CONNECT_RESOURCE_ID = "com.sunmi.welcome:id/btn_positive"
    CONFIG_SCROLL_RESOURCE_ID = "com.sunmi.welcome:id/scrollView"
    DETAILS_SCROLL_RESOURCE_ID = "com.sunmi.welcome:id/scrollview"
    HYPERWIFI_INTRO_TITLE = "HYPER Wi-Fi"
    HYPERWIFI_INTRO_CLOSE_RESOURCE_ID = "com.sunmi.welcome:id/btn_close"
    EXPAND_ALL_TEXT = "展开全部"
    DELETE_NETWORK_TEXT = "删除此网络"
    STATIC_FIELD_LABELS = {
        "ip_address": ("IP地址", "IP 地址"),
        "gateway": ("网关",),
        "prefix_length": ("网络前缀长度",),
        "dns1": ("DNS1", "DNS 1"),
        "dns2": ("DNS2", "DNS 2"),
    }

    def __init__(self, device: Any, artifact_dir: Path) -> None:
        self.device = device
        self.artifact_dir = artifact_dir

    def find_hyperwifi_label(
        self, max_swipes: int = 30, *, preferred_ssid: str | None = None
    ) -> HyperWiFiLabel | None:
        self._require_wlan_list()
        if preferred_ssid is not None:
            if not self.find_ssid(preferred_ssid, max_swipes=max_swipes):
                return None
            return self._visible_hyperwifi_label(preferred_ssid=preferred_ssid)

        self._scroll_to_top()

        for _ in range(max_swipes + 1):
            label = self._visible_hyperwifi_label(preferred_ssid=preferred_ssid)
            if label is not None:
                return label

            if self._expand_all_if_present():
                continue

            previous_signature = self._list_signature()
            self._swipe_to_next_page()
            if previous_signature == self._list_signature():
                return None

        return None

    def find_ssid(self, ssid: str, max_swipes: int | None = None) -> bool:
        self._require_wlan_list()
        if ssid in self._visible_ssids():
            return True

        swipe_limit = 30 if max_swipes is None else max(0, max_swipes)
        for swipe_page in (self._swipe_to_previous_page, self._swipe_to_next_page):
            seen_signatures: set[tuple[tuple[str, int, int], ...]] = set()
            for swipe_count in range(swipe_limit + 1):
                if ssid in self._visible_ssids():
                    return True

                if self._expand_all_if_present():
                    if ssid in self._visible_ssids():
                        return True

                if swipe_count == swipe_limit:
                    break

                previous_signature = self._list_signature()
                if previous_signature in seen_signatures:
                    break
                seen_signatures.add(previous_signature)
                swipe_page()
                if previous_signature == self._list_signature():
                    if ssid in self._visible_ssids():
                        return True
                    break

        return False

    def wait_for_ssid(
        self, ssid: str, timeout: float = 20.0, poll_interval: float = 0.5
    ) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.find_ssid(ssid):
                return True
            time.sleep(poll_interval)
        return self.find_ssid(ssid)

    def is_network_config_open(self) -> bool:
        return bool(
            self.device(resourceId=self.CONFIG_SCROLL_RESOURCE_ID).exists
            and self.device(resourceId=self.CANCEL_RESOURCE_ID).exists
        )

    def wait_for_network_status(
        self, ssid: str, status_texts: tuple[str, ...], timeout: float = 20.0
    ) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._network_has_status(ssid, status_texts):
                return True
            time.sleep(0.5)
        return self._network_has_status(ssid, status_texts)

    def open_encrypted_network_config(
        self, preferred_ssid: str | None = None, timeout: float = 5.0
    ) -> str:
        self._close_existing_network_config()
        self._require_wlan_list()
        if preferred_ssid is not None and not self.wait_for_ssid(preferred_ssid):
            self.fail_with_artifacts(f"Welcome WLAN 列表未找到指定 WiFi {preferred_ssid!r}")
        network = self._find_encrypted_network(preferred_ssid)
        if network is None:
            target = preferred_ssid or "任意加密 WiFi"
            self.fail_with_artifacts(f"Welcome WLAN 列表未找到 {target}")

        bounds = network.bounds
        self.device.click(
            (bounds["left"] + bounds["right"]) // 2,
            (bounds["top"] + bounds["bottom"]) // 2,
        )
        if not self.device(resourceId=self.PASSWORD_RESOURCE_ID).wait(timeout=timeout):
            self.fail_with_artifacts("加密网络连接配置框弹出异常")
        return network.ssid

    def connect_open_network(self, ssid: str, timeout: float = 2.0) -> None:
        self._close_existing_network_config()
        self._require_wlan_list()
        if not self.wait_for_ssid(ssid):
            self.fail_with_artifacts(f"Welcome WLAN 列表未找到指定开放 WiFi {ssid!r}")
        network = self._find_open_network(ssid)
        if network is None:
            self.fail_with_artifacts(f"Welcome WLAN 列表未找到指定开放 WiFi {ssid!r}")

        bounds = network.bounds
        self.device.click(
            (bounds["left"] + bounds["right"]) // 2,
            (bounds["top"] + bounds["bottom"]) // 2,
        )
        if self.device(resourceId=self.PASSWORD_RESOURCE_ID).wait(timeout=timeout):
            self.fail_with_artifacts("点击开放 WiFi 后错误弹出连接配置框")

    def enter_password(self, password: str) -> bool:
        password_field = self.device(resourceId=self.PASSWORD_RESOURCE_ID)
        if not password_field.wait(timeout=5.0):
            self.fail_with_artifacts("未找到连接配置框密码输入框")
        password_field.set_text(password)
        displayed_password = password_field.get_text()
        return displayed_password == password or (
            len(displayed_password) == len(password)
            and bool(displayed_password)
            and set(displayed_password) == {"•"}
        )

    def clear_password(self) -> None:
        password_field = self.device(resourceId=self.PASSWORD_RESOURCE_ID)
        if not password_field.wait(timeout=5.0):
            self.fail_with_artifacts("未找到连接配置框密码输入框")
        password_field.clear_text()

    def dismiss_keyboard(self) -> None:
        deadline = time.monotonic() + 5.0
        back_sent = False
        while True:
            response = self.device.shell("dumpsys input_method")
            if response.exit_code != 0:
                self.fail_with_artifacts("无法查询输入法状态")
            shown = re.search(r"\bmInputShown=(true|false)\b", response.output)
            if shown is None:
                self.fail_with_artifacts("输入法状态未包含 mInputShown，无法安全关闭键盘")
            if shown.group(1) == "false":
                return
            if not back_sent:
                self.device.press("back")
                back_sent = True
            if time.monotonic() >= deadline:
                self.fail_with_artifacts("按 Back 后软键盘未关闭")
            time.sleep(0.2)

    def _wait_for_stable_bounds(self, selector: Any) -> None:
        deadline = time.monotonic() + 5.0
        previous = None
        stable_samples = 0
        while time.monotonic() < deadline:
            bounds = dict(selector.info["bounds"])
            stable_samples = stable_samples + 1 if bounds == previous else 0
            if stable_samples >= 3:
                return
            previous = bounds
            time.sleep(0.2)
        self.fail_with_artifacts("Welcome 控件边界在动画后未稳定")

    def clear_password_with_button(self) -> None:
        clear = self.device(resourceId=self.CLEAR_PASSWORD_RESOURCE_ID)
        if not clear.click_exists(timeout=5.0):
            self.fail_with_artifacts("无法点击密码输入框删除按钮")
        displayed_password = self._password_field().get_text()
        if displayed_password not in ("", self.PASSWORD_HINT_TEXT):
            self.fail_with_artifacts("点击密码输入框删除按钮后内容未清空")

    def is_password_masked(self) -> bool:
        displayed_password = self._password_field().get_text()
        return bool(displayed_password) and set(displayed_password) == {"•"}

    def toggle_password_visibility(self) -> None:
        visibility = self.device(resourceId=self.PASSWORD_VISIBILITY_RESOURCE_ID)
        if not visibility.wait(timeout=5.0):
            self.fail_with_artifacts("无法点击密码明文/密文切换按钮")
        initially_checked = bool(visibility.info.get("checked"))
        visibility.click()
        deadline = time.monotonic() + 2.0
        while time.monotonic() < deadline:
            if bool(visibility.info.get("checked")) != initially_checked:
                return
            time.sleep(0.1)
        self.fail_with_artifacts("点击密码明文/密文切换按钮后状态未变化")

    def open_advanced_options(self) -> None:
        options = self.device(resourceId=self.ADVANCED_OPTIONS_RESOURCE_ID)
        if not options.wait(timeout=5.0):
            self.fail_with_artifacts("未找到高级选项下拉按钮")
        if not options.info.get("checked"):
            options.click()
        if not self.device(resourceId=self.IP_SELECTOR_RESOURCE_ID).wait(timeout=5.0):
            self.fail_with_artifacts("高级选项未显示 IP 设置")
        self._wait_for_stable_bounds(self.device(resourceId=self.IP_SELECTOR_RESOURCE_ID))

    def current_ip_mode(self) -> str:
        mode_text = self.device(resourceId=self.IP_MODE_TEXT_RESOURCE_ID)
        if not mode_text.wait(timeout=5.0):
            self.fail_with_artifacts("未找到 IP 设置当前值")
        mode = mode_text.get_text()
        if mode not in ("DHCP", "静态"):
            self.fail_with_artifacts(f"IP 设置当前值异常：{mode!r}")
        return mode

    def select_ip_mode(self, mode: str) -> None:
        resource_ids = {"DHCP": self.DHCP_IP_RESOURCE_ID, "静态": self.STATIC_IP_RESOURCE_ID}
        if mode not in resource_ids:
            raise ValueError(f"不支持的 IP 设置：{mode!r}")
        for attempt in range(2):
            selector = self.device(resourceId=self.IP_SELECTOR_RESOURCE_ID)
            self._wait_for_stable_bounds(selector)
            if not selector.click_exists(timeout=5.0):
                self.fail_with_artifacts("无法点击 IP 设置下拉按钮")
            option = self.device(resourceId=resource_ids[mode])
            if option.click_exists(timeout=5.0):
                if self.current_ip_mode() != mode:
                    self.fail_with_artifacts(f"IP 设置切换 {mode!r} 未生效")
                return
            if attempt == 0:
                time.sleep(0.5)
        self.fail_with_artifacts(f"IP 设置未显示 {mode!r} 选项")

    def ip_mode_options(self) -> set[str]:
        selector = self.device(resourceId=self.IP_SELECTOR_RESOURCE_ID)
        self._wait_for_stable_bounds(selector)
        if not selector.click_exists(timeout=5.0):
            self.fail_with_artifacts("无法点击 IP 设置下拉按钮")
        dhcp_option = self.device(resourceId=self.DHCP_IP_RESOURCE_ID)
        static_option = self.device(resourceId=self.STATIC_IP_RESOURCE_ID)
        if not dhcp_option.wait(timeout=5.0) or not static_option.wait(timeout=5.0):
            self.fail_with_artifacts("IP 设置选项未完整显示")
        options = {
            mode
            for mode, resource_id in (("DHCP", self.DHCP_IP_RESOURCE_ID), ("静态", self.STATIC_IP_RESOURCE_ID))
            if self.device(resourceId=resource_id).exists
        }
        if not dhcp_option.click_exists(timeout=1.0):
            self.fail_with_artifacts("无法关闭 IP 设置选项")
        return options

    def static_field_labels(self) -> set[str]:
        return {
            name
            for name in self.STATIC_FIELD_LABELS
            if self._find_static_field(name) is not None
        }

    def set_static_field(
        self, name: str, value: str, *, verify_readback: bool = True
    ) -> str:
        actual = ""
        field = self._require_static_field(name)
        field_info = field.info
        resource_id = str(
            field_info.get("resourceName") or field_info.get("resourceId") or ""
        ).strip()
        for attempt in range(2):
            bounds = field.info["bounds"]
            self.device.click(
                (bounds["left"] + bounds["right"]) // 2,
                (bounds["top"] + bounds["bottom"]) // 2,
            )
            time.sleep(0.3)
            field = (
                self.device(resourceId=resource_id)
                if resource_id
                else self._require_static_field(name)
            )
            field.clear_text()
            if not value:
                self.dismiss_keyboard()
                return ""
            field.set_text(value)
            if not verify_readback:
                self.dismiss_keyboard()
                return value
            time.sleep(0.3)
            actual = field.get_text()
            if actual == value:
                break
            if attempt == 0:
                time.sleep(0.5)
        self.dismiss_keyboard()
        return actual

    def clear_static_field_with_button(self, name: str) -> None:
        for _ in range(2):
            field = self._require_static_field(name)
            previous_text = field.get_text()
            bounds = field.info["bounds"]
            self.device.click(
                (bounds["left"] + bounds["right"]) // 2,
                (bounds["top"] + bounds["bottom"]) // 2,
            )
            time.sleep(0.3)
            field = self._require_static_field(name)
            bounds = field.info["bounds"]
            clear = self.device(resourceId=self.CLEAR_PASSWORD_RESOURCE_ID)
            if clear.exists and self._bounds_overlap_vertically(bounds, clear.info["bounds"]):
                clear.click()
            else:
                field.clear_text()
            time.sleep(0.3)
            current_text = self._require_static_field(name).get_text()
            if current_text != previous_text:
                return
        self.fail_with_artifacts(f"点击静态 IP 字段 {name!r} 删除按钮后内容未变化")

    def is_connect_enabled(self) -> bool:
        connect = self.device(resourceId=self.CONNECT_RESOURCE_ID)
        if not connect.wait(timeout=5.0):
            self.fail_with_artifacts("未找到连接配置框连接按钮")
        return bool(connect.info.get("enabled"))

    def connect_network(self) -> None:
        connect = self.device(resourceId=self.CONNECT_RESOURCE_ID)
        if not connect.click_exists(timeout=5.0):
            self.fail_with_artifacts("无法点击连接配置框连接按钮")

    def cancel_network_config(self) -> None:
        self.dismiss_keyboard()
        cancel = self.device(resourceId=self.CANCEL_RESOURCE_ID)
        if not cancel.wait(timeout=5.0):
            self.fail_with_artifacts("未找到连接配置框取消按钮")
        self._wait_for_stable_bounds(cancel)
        if not cancel.click_exists(timeout=5.0):
            self.fail_with_artifacts("无法关闭连接配置框")
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if (
                not self.is_network_config_open()
                and self.device.app_current().get("package") == self.WELCOME_PACKAGE
            ):
                return
            time.sleep(0.1)
        self.fail_with_artifacts("取消连接配置框后未返回 Welcome WLAN 页面")

    def open_connected_network_details(self, ssid: str) -> None:
        self._close_existing_network_config()
        self._require_wlan_list()
        if not self.wait_for_ssid(ssid):
            self.fail_with_artifacts(f"Welcome WLAN 列表未找到指定 WiFi {ssid!r}")
        network = self.device(resourceId=self.SSID_RESOURCE_ID, text=ssid)
        if not network.click_exists(timeout=5.0):
            self.fail_with_artifacts(f"无法点击已连接 WiFi {ssid!r}")

    def delete_network_from_details(self) -> None:
        details_scroll = self.device(resourceId=self.DETAILS_SCROLL_RESOURCE_ID)
        if not details_scroll.wait(timeout=5.0):
            self.fail_with_artifacts("未找到网络详情弹窗滚动区域")
        if not details_scroll.scroll.to(text=self.DELETE_NETWORK_TEXT):
            self.fail_with_artifacts("网络详情弹窗未找到删除此网络按钮")
        delete = self.device(text=self.DELETE_NETWORK_TEXT)
        if delete.click_exists(timeout=5.0):
            return
        self.fail_with_artifacts("网络详情弹窗未找到删除此网络按钮")

    def click_hyperwifi_label_and_wait_for_intro(
        self, label: HyperWiFiLabel, timeout: float = 5.0
    ) -> bool:
        current_label = self._visible_hyperwifi_label(preferred_ssid=label.ssid)
        if current_label is None:
            return False
        hierarchy_before_click = self.device.dump_hierarchy()
        bounds = current_label.bounds
        self.device.click(
            (bounds["left"] + bounds["right"]) // 2,
            (bounds["top"] + bounds["bottom"]) // 2,
        )
        return self._wait_for_hyperwifi_intro(
            hierarchy_before_click, timeout=timeout
        )

    def close_hyperwifi_intro(self) -> None:
        close = self.device(resourceId=self.HYPERWIFI_INTRO_CLOSE_RESOURCE_ID)
        if not close.click_exists(timeout=5.0):
            self.fail_with_artifacts("未找到 HyperWiFi 介绍弹窗关闭按钮")
        if not close.wait_gone(timeout=5.0):
            self.fail_with_artifacts("点击关闭后 HyperWiFi 介绍弹窗未消失")
        self._require_wlan_list()

    def expand_all_and_confirm_more_ssids(
        self, max_swipes: int = 30, timeout: float = 5.0
    ) -> bool:
        self._require_wlan_list()
        self._scroll_to_top()
        collapsed_ssids: set[str] = set()
        first_page_ssids: set[str] | None = None

        for swipe_count in range(max_swipes + 1):
            visible_ssids = self._visible_ssids()
            if first_page_ssids is None:
                first_page_ssids = visible_ssids
            collapsed_ssids.update(visible_ssids)
            expand_all = self.device(text=self.EXPAND_ALL_TEXT)
            if expand_all.exists:
                log.info("Welcome WLAN: 点击“展开全部”，检查新增 SSID")
                expand_all.click()
                return self._wait_for_more_ssids(
                    collapsed_ssids, max_swipes=max_swipes, timeout=timeout
                )

            if swipe_count == max_swipes:
                log.error("Welcome WLAN: 达到滑动上限，尚未确认列表末尾或找到“展开全部”")
                return False
            previous_signature = self._list_signature()
            self._swipe_to_next_page()
            if previous_signature == self._list_signature():
                if self._is_inset_wlan_layout():
                    added_ssids = collapsed_ssids - first_page_ssids
                    log.info(
                        "Welcome WLAN: 大屏内嵌列表无“展开全部”，"
                        "实际滚动后新增 %d 个 SSID",
                        len(added_ssids),
                    )
                    return bool(added_ssids)
                log.error("Welcome WLAN: 手持全屏布局未找到“展开全部”")
                return False

        return False

    def _wait_for_hyperwifi_intro(
        self, hierarchy_before_click: str, timeout: float
    ) -> bool:
        deadline = time.monotonic() + timeout
        while True:
            hierarchy = self.device.dump_hierarchy()
            if self._hierarchy_contains_hyperwifi_text(hierarchy):
                return True
            if hierarchy != hierarchy_before_click:
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.2)

    def fail_with_artifacts(self, message: str) -> NoReturn:
        self.artifact_dir.mkdir(parents=True, exist_ok=True)
        hierarchy_path = self.artifact_dir / "welcome_wlan_failure.xml"
        screenshot_path = self.artifact_dir / "welcome_wlan_failure.png"
        hierarchy_path.write_text(self.device.dump_hierarchy(), encoding="utf-8")
        self.device.screenshot(str(screenshot_path))
        failure_message = (
            f"{message}；UI hierarchy={hierarchy_path}，screenshot={screenshot_path}"
        )
        try:
            print(failure_message, file=sys.__stderr__, flush=True)
        except OSError:
            print(failure_message, file=sys.stderr, flush=True)
        raise AssertionError(failure_message)

    def _require_wlan_list(self) -> None:
        current_app = self.device.app_current()
        if current_app.get("package") != self.WELCOME_PACKAGE:
            self.fail_with_artifacts("当前页面不是 Welcome WLAN 列表")
        if not self.device(resourceId=self.SSID_RESOURCE_ID).wait(timeout=5.0):
            self.fail_with_artifacts("Welcome WLAN 列表未显示")

    def _scroll_to_top(self) -> None:
        for _ in range(30):
            before = self._list_signature()
            self._swipe_to_previous_page()
            if before == self._list_signature():
                return

    def _visible_hyperwifi_label(
        self, preferred_ssid: str | None = None
    ) -> HyperWiFiLabel | None:
        labels = self._hyperwifi_labels_from_hierarchy(self.device.dump_hierarchy())
        if preferred_ssid is not None:
            for label in labels:
                if label.ssid == preferred_ssid:
                    return label
            return None
        if labels:
            return labels[0]
        return None

    def _visible_ssids(self) -> set[str]:
        root = ET.fromstring(self.device.dump_hierarchy())
        return {
            node.attrib.get("text", "")
            for node in root.iter("node")
            if node.attrib.get("resource-id") == self.SSID_RESOURCE_ID
            and node.attrib.get("text", "")
        }

    def _wlan_list_bounds(self) -> dict[str, int]:
        root = ET.fromstring(self.device.dump_hierarchy())
        parents = {child: parent for parent in root.iter() for child in parent}
        for node in root.iter("node"):
            if node.attrib.get("resource-id") != self.SSID_RESOURCE_ID:
                continue
            current = parents.get(node)
            while current is not None:
                if (
                    current.attrib.get("scrollable") == "true"
                    or current.attrib.get("class") == "androidx.recyclerview.widget.RecyclerView"
                ):
                    bounds = self._parse_bounds(current.attrib["bounds"])
                    if bounds["right"] > bounds["left"] and bounds["bottom"] > bounds["top"]:
                        return bounds
                current = parents.get(current)
        self.fail_with_artifacts("Welcome WLAN 列表未找到有效的滚动区域边界")

    def _is_inset_wlan_layout(self) -> bool:
        root = ET.fromstring(self.device.dump_hierarchy())
        screen = root.find("node")
        if screen is None or not screen.attrib.get("bounds"):
            return False
        screen_bounds = self._parse_bounds(screen.attrib["bounds"])
        for node in root.iter("node"):
            if node.attrib.get("resource-id") != "com.sunmi.welcome:id/ll_cell":
                continue
            panel = self._parse_bounds(node.attrib["bounds"])
            return (
                screen_bounds["left"] < panel["left"] < panel["right"] < screen_bounds["right"]
                and screen_bounds["top"] < panel["top"] < panel["bottom"] < screen_bounds["bottom"]
            )
        return False

    def _password_field(self):
        password_field = self.device(resourceId=self.PASSWORD_RESOURCE_ID)
        if not password_field.wait(timeout=5.0):
            self.fail_with_artifacts("未找到连接配置框密码输入框")
        return password_field

    def _close_existing_network_config(self) -> None:
        cancel = self.device(resourceId=self.CANCEL_RESOURCE_ID)
        if not cancel.exists:
            return
        self.cancel_network_config()
        if not self.device(resourceId=self.SSID_RESOURCE_ID).wait(timeout=5.0):
            self.fail_with_artifacts("关闭遗留连接配置框后未返回 Welcome WLAN 列表")

    def _require_static_field(self, name: str):
        field = self._find_static_field(name)
        if field is None:
            self.fail_with_artifacts(f"未找到静态 IP 配置字段 {name!r}")
        return field

    def _find_static_field(self, name: str):
        if name not in self.STATIC_FIELD_LABELS:
            raise ValueError(f"未知静态 IP 配置字段：{name!r}")
        for forward in (True, False):
            for _ in range(10):
                for label in self.STATIC_FIELD_LABELS[name]:
                    field = self._field_next_to_label(label)
                    if field is not None:
                        return field
                config_scroll = self.device(resourceId=self.CONFIG_SCROLL_RESOURCE_ID)
                if not config_scroll.exists:
                    return None
                before = self.device.dump_hierarchy()
                self._swipe_in_bounds(config_scroll.info["bounds"], forward=forward)
                if before == self.device.dump_hierarchy():
                    break
        return None

    def _field_next_to_label(self, label: str, *, recover_clipped: bool = True):
        label_selector = self.device(text=label)
        if not label_selector.exists:
            return None
        label_bounds = label_selector.info["bounds"]
        fields = self.device(className="android.widget.EditText")
        candidates = [fields[index] for index in range(fields.count)]
        if not candidates:
            return None
        label_right = label_bounds["right"]
        same_row_fields = [
            field
            for field in candidates
            if self._bounds_overlap_vertically(label_bounds, field.info["bounds"])
            and field.info["bounds"]["left"] >= label_right
        ]
        if same_row_fields:
            return min(
                same_row_fields,
                key=lambda field: field.info["bounds"]["left"] - label_right,
            )
        below_label_fields = [
            field
            for field in candidates
            if field.info["bounds"]["top"] >= label_bounds["bottom"]
            and self._bounds_overlap_horizontally(label_bounds, field.info["bounds"])
        ]
        if below_label_fields:
            return min(
                below_label_fields,
                key=lambda field: field.info["bounds"]["top"] - label_bounds["bottom"],
            )
        config_scroll = self.device(resourceId=self.CONFIG_SCROLL_RESOURCE_ID)
        scroll_info = config_scroll.info if config_scroll.exists else None
        scroll_bounds = scroll_info.get("bounds") if isinstance(scroll_info, dict) else None
        if (
            recover_clipped
            and scroll_bounds
            and label_bounds["bottom"] >= scroll_bounds["bottom"] - 8
        ):
            scroll_height = scroll_bounds["bottom"] - scroll_bounds["top"]
            center_x = (scroll_bounds["left"] + scroll_bounds["right"]) // 2
            start_y = scroll_bounds["bottom"] - max(1, scroll_height // 8)
            end_y = max(scroll_bounds["top"] + 1, start_y - scroll_height // 2)
            self.device.swipe(center_x, start_y, center_x, end_y, duration=0.2)
            time.sleep(0.3)
            return self._field_next_to_label(label, recover_clipped=False)
        return None

    @staticmethod
    def _bounds_overlap_vertically(
        first: dict[str, int], second: dict[str, int]
    ) -> bool:
        return first["top"] < second["bottom"] and second["top"] < first["bottom"]

    @staticmethod
    def _bounds_overlap_horizontally(
        first: dict[str, int], second: dict[str, int]
    ) -> bool:
        return first["left"] < second["right"] and second["left"] < first["right"]

    def _find_encrypted_network(
        self, preferred_ssid: str | None
    ) -> WelcomeWifiNetwork | None:
        root = ET.fromstring(self.device.dump_hierarchy())
        networks: list[WelcomeWifiNetwork] = []
        for row in root.iter("node"):
            if row.attrib.get("clickable") != "true":
                continue
            descendants = list(row.iter("node"))
            ssid_nodes = [
                node
                for node in descendants
                if node.attrib.get("resource-id") == self.SSID_RESOURCE_ID
                and node.attrib.get("text", "")
            ]
            has_lock = any(
                node.attrib.get("resource-id") == self.LOCK_RESOURCE_ID
                for node in descendants
            )
            if len(ssid_nodes) != 1 or not has_lock:
                continue
            ssid_node = ssid_nodes[0]
            network = WelcomeWifiNetwork(
                ssid=ssid_node.attrib["text"],
                bounds=self._parse_bounds(row.attrib["bounds"]),
            )
            if preferred_ssid == network.ssid:
                return network
            networks.append(network)
        return random.choice(networks) if preferred_ssid is None and networks else None

    def _network_has_status(self, ssid: str, status_texts: tuple[str, ...]) -> bool:
        root = ET.fromstring(self.device.dump_hierarchy())
        for row in root.iter("node"):
            if row.attrib.get("clickable") != "true":
                continue
            descendants = list(row.iter("node"))
            if not any(
                node.attrib.get("resource-id") == self.SSID_RESOURCE_ID
                and node.attrib.get("text") == ssid
                for node in descendants
            ):
                continue
            return any(
                status_text in node.attrib.get("text", "")
                for status_text in status_texts
                for node in descendants
            )
        return False

    def _find_open_network(self, ssid: str) -> WelcomeWifiNetwork | None:
        root = ET.fromstring(self.device.dump_hierarchy())
        for row in root.iter("node"):
            if row.attrib.get("clickable") != "true":
                continue
            descendants = list(row.iter("node"))
            ssid_nodes = [
                node
                for node in descendants
                if node.attrib.get("resource-id") == self.SSID_RESOURCE_ID
                and node.attrib.get("text") == ssid
            ]
            has_lock = any(
                node.attrib.get("resource-id") == self.LOCK_RESOURCE_ID
                for node in descendants
            )
            if len(ssid_nodes) == 1 and not has_lock:
                ssid_node = ssid_nodes[0]
                return WelcomeWifiNetwork(
                    ssid=ssid_node.attrib["text"],
                    bounds=self._parse_bounds(row.attrib["bounds"]),
                )
        return None

    def _hyperwifi_labels_from_hierarchy(self, hierarchy: str) -> list[HyperWiFiLabel]:
        root = ET.fromstring(hierarchy)
        labels: list[HyperWiFiLabel] = []
        seen_bounds: set[tuple[int, int, int, int]] = set()

        for row in root.iter("node"):
            descendants = list(row.iter("node"))
            ssid_nodes = [
                node
                for node in descendants
                if node.attrib.get("resource-id") == self.SSID_RESOURCE_ID
            ]
            if len(ssid_nodes) != 1:
                continue
            ssid_node = ssid_nodes[0]
            ssid_bounds = self._parse_bounds(ssid_node.attrib["bounds"])

            for node in descendants:
                if not self._is_hyperwifi_label_node(node):
                    continue
                label_bounds = self._parse_bounds(node.attrib["bounds"])
                if not self._is_right_side_label(ssid_bounds, label_bounds):
                    continue
                bounds_key = (
                    label_bounds["left"],
                    label_bounds["top"],
                    label_bounds["right"],
                    label_bounds["bottom"],
                )
                if bounds_key in seen_bounds:
                    continue
                seen_bounds.add(bounds_key)
                labels.append(
                    HyperWiFiLabel(
                        ssid=ssid_node.attrib.get("text", ""),
                        bounds=label_bounds,
                    )
                )
        return labels

    @staticmethod
    def _hierarchy_contains_hyperwifi_text(hierarchy: str) -> bool:
        root = ET.fromstring(hierarchy)
        for node in root.iter("node"):
            for attribute in ("text", "content-desc"):
                text = node.attrib.get(attribute, "")
                if "hyperwifi" in "".join(text.casefold().split()).replace("-", ""):
                    return True
        return False

    @staticmethod
    def _is_hyperwifi_label_node(node: ET.Element) -> bool:
        return (
            node.attrib.get("class") == "android.widget.ImageView"
            and node.attrib.get("clickable") == "true"
            and not node.attrib.get("resource-id")
        )

    @staticmethod
    def _parse_bounds(bounds: str) -> dict[str, int]:
        left_top, right_bottom = bounds.removeprefix("[").removesuffix("]").split("][")
        left, top = (int(value) for value in left_top.split(","))
        right, bottom = (int(value) for value in right_bottom.split(","))
        return {"left": left, "top": top, "right": right, "bottom": bottom}

    @staticmethod
    def _is_right_side_label(
        ssid_bounds: dict[str, int], image_bounds: dict[str, int]
    ) -> bool:
        image_center_y = (image_bounds["top"] + image_bounds["bottom"]) // 2
        return (
            image_bounds["left"] > ssid_bounds["right"]
            and ssid_bounds["top"] - 16 <= image_center_y <= ssid_bounds["bottom"] + 16
        )

    def _expand_all_if_present(self) -> bool:
        expand_all = self.device(text=self.EXPAND_ALL_TEXT)
        if not expand_all.exists:
            return False
        expand_all.click()
        time.sleep(0.5)
        return True

    def _wait_for_more_ssids(
        self, collapsed_ssids: set[str], max_swipes: int, timeout: float
    ) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._visible_ssids() - collapsed_ssids:
                return True
            time.sleep(0.2)

        for _ in range(max_swipes):
            previous_signature = self._list_signature()
            self._swipe_to_next_page()
            if self._visible_ssids() - collapsed_ssids:
                return True
            if previous_signature == self._list_signature():
                return False

        return False

    def _swipe_to_previous_page(self) -> None:
        self._swipe_wlan_list(forward=False)

    def _swipe_to_next_page(self) -> None:
        self._swipe_wlan_list(forward=True)

    def _swipe_wlan_list(self, *, forward: bool) -> None:
        # Some landscape ROMs report portrait window_size(); hierarchy bounds
        # already use the coordinate space accepted by input gestures.
        self._swipe_in_bounds(self._wlan_list_bounds(), forward=forward)

    def _swipe_in_bounds(self, bounds: dict[str, int], *, forward: bool) -> None:
        center_x = (bounds["left"] + bounds["right"]) // 2
        height = bounds["bottom"] - bounds["top"]
        upper_y = bounds["top"] + height // 5
        lower_y = bounds["bottom"] - height // 5
        self.device.swipe(
            center_x,
            lower_y if forward else upper_y,
            center_x,
            upper_y if forward else lower_y,
            duration=0.2,
        )
        time.sleep(0.3)

    def _list_signature(self) -> tuple[tuple[str, int, int], ...]:
        root = ET.fromstring(self.device.dump_hierarchy())
        signature = []
        for node in root.iter("node"):
            if node.attrib.get("resource-id") != self.SSID_RESOURCE_ID:
                continue
            bounds = self._parse_bounds(node.attrib["bounds"])
            signature.append((node.attrib.get("text", ""), bounds["top"], bounds["bottom"]))
        return tuple(signature)