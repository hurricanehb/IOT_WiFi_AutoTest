"""Reset Bluetooth and WLAN through the Android Settings UI.
(通过Android设置UI重置蓝牙和WLAN)"""
from __future__ import annotations

import time
from typing import Dict, List, Sequence, Tuple
from xml.etree import ElementTree

import uiautomator2 as u2

from core.utils.adb_helper import AdbHelper

UiBounds = Tuple[int, int, int, int]
UiNode = Tuple[Dict[str, str], UiBounds]


class BluetoothWlanResetControl:
    """Reset Bluetooth and WLAN using labeled Settings controls."""

    _SETTINGS_ACTION = "android.settings.SETTINGS"
    _SETTINGS_ROOT_FLAGS = "0x10008000"
    _SETTINGS_PACKAGE = "com.android.settings"
    _SYSTEM_LABELS = ("系统", "System")
    _RESET_OPTIONS_LABELS = ("重置选项", "Reset options")
    _RESET_BLUETOOTH_WLAN_LABELS = (
        "重置蓝牙和WLAN",
        "重置蓝牙和WLAN设置",
        "Reset Bluetooth and Wi-Fi",
        "Reset Bluetooth and Wi-Fi settings",
    )
    _RESET_CONFIRM_LABELS = ("重置", "Reset")
    _RESET_CONFIRM_RESOURCE_ID = "android:id/button1"
    _RESET_NAVIGATION_ATTEMPTS = 3
    _SETTINGS_TRANSITION_TIMEOUT_SECONDS = 5.0
    _UI_STABILITY_DELAY_SECONDS = 0.3
    _INITIAL_SCROLL_DELAY_SECONDS = 1.5
    _MAX_SCROLL_ATTEMPTS = 5

    def __init__(self, adb: AdbHelper):
        self.adb = adb
        self.device = u2.connect(adb.serial)

    @staticmethod
    def _parse_bounds(value: str) -> UiBounds:
        numbers = [
            int(number)
            for number in value.replace("][", ",").replace("[", "").replace("]", "").split(",")
        ]
        if len(numbers) != 4:
            raise ValueError(f"无效的 UI bounds: {value!r}")
        return numbers[0], numbers[1], numbers[2], numbers[3]

    def _shell_text(self, command: str) -> str:
        code, out, err = self.adb.shell_line(command)
        text = "\n".join(part for part in (out, err) if part).strip()
        if code != 0:
            raise RuntimeError(f"设备命令失败: {command}: {text or code}")
        return text

    def _settings_xml(self) -> str:
        raw = self.device.dump_hierarchy()
        start = raw.find("<?xml")
        if start < 0:
            start = raw.find("<hierarchy")
        end = raw.rfind("</hierarchy>")
        if start < 0 or end < 0:
            raise ValueError(f"未获取到 Settings UI 节点树: {raw[:200]!r}")
        return raw[start : end + len("</hierarchy>")]

    def _ui_nodes(self, xml: str) -> List[UiNode]:
        root = ElementTree.fromstring(xml)
        nodes: List[UiNode] = []
        for node in root.iter("node"):
            attributes = dict(node.attrib)
            bounds = attributes.get("bounds")
            if bounds:
                nodes.append((attributes, self._parse_bounds(bounds)))
        return nodes

    @staticmethod
    def _node_text(attributes: Dict[str, str]) -> str:
        return "".join(
            "".join(value.split())
            for value in (attributes.get("text"), attributes.get("content-desc"))
            if value
        )

    @staticmethod
    def _matches_labels(attributes: Dict[str, str], labels: Sequence[str]) -> bool:
        normalized_labels = {"".join(label.split()) for label in labels}
        return any(
            "".join(value.split()) in normalized_labels
            for value in (attributes.get("text"), attributes.get("content-desc"))
            if value
        )

    @staticmethod
    def _center(bounds: UiBounds) -> Tuple[int, int]:
        left, top, right, bottom = bounds
        return (left + right) // 2, (top + bottom) // 2

    def _find_labeled_bounds(self, xml: str, labels: Sequence[str]) -> UiBounds:
        nodes = self._settings_nodes_or_fallback(self._ui_nodes(xml))
        matches = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if self._matches_labels(attributes, labels)
        ]
        if not matches:
            raise ValueError(f"未找到控件: {'、'.join(labels)}")
        return max(matches, key=lambda item: item[1][1])[1]

    def _settings_nodes_or_fallback(self, nodes: List[UiNode]) -> List[UiNode]:
        settings_nodes = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if attributes.get("package") == self._SETTINGS_PACKAGE
        ]
        return settings_nodes or nodes

    def _find_resource_bounds(self, xml: str, resource_id: str) -> UiBounds:
        matches = [
            (attributes, bounds)
            for attributes, bounds in self._ui_nodes(xml)
            if attributes.get("resource-id") == resource_id
            and attributes.get("enabled", "true").lower() != "false"
        ]
        if not matches:
            raise ValueError(f"未找到 resource-id 为 {resource_id!r} 的控件")
        return max(matches, key=lambda item: item[1][1])[1]

    def _ui_signature(self, xml: str) -> Tuple[Tuple[str, UiBounds], ...]:
        return tuple(
            (self._node_text(attributes), bounds)
            for attributes, bounds in self._ui_nodes(xml)
            if self._node_text(attributes)
        )

    def _wait_for_stable_settings_xml(self, timeout: float = 3.0) -> str:
        deadline = time.monotonic() + timeout
        previous_xml = self._settings_xml()
        previous_signature = self._ui_signature(previous_xml)
        while time.monotonic() < deadline:
            time.sleep(self._UI_STABILITY_DELAY_SECONDS)
            current_xml = self._settings_xml()
            if self._ui_signature(current_xml) == previous_signature:
                return current_xml
            previous_xml = current_xml
            previous_signature = self._ui_signature(current_xml)
        return previous_xml

    def _wait_for_settings_transition(self, previous_signature: Tuple[Tuple[str, UiBounds], ...]) -> None:
        deadline = time.monotonic() + self._SETTINGS_TRANSITION_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            current_xml = self._settings_xml()
            if self._ui_signature(current_xml) != previous_signature:
                self._wait_for_stable_settings_xml()
                return
            time.sleep(0.2)
        raise AssertionError("打开系统设置后页面未切换")

    def _tap_labeled_item_if_visible(self, labels: Sequence[str]) -> bool:
        try:
            bounds = self._find_labeled_bounds(self._settings_xml(), labels)
        except ValueError:
            return False
        self.adb.tap(*self._center(bounds))
        return True

    @staticmethod
    def _select_scroll_bounds(
        scrollable_bounds: List[UiBounds], *, pane: str = "auto"
    ) -> UiBounds:
        if not scrollable_bounds:
            raise ValueError("Settings UI 节点树中没有可滚动区域")

        leftmost_bounds = min(scrollable_bounds, key=lambda item: item[0])
        rightmost_bounds = max(scrollable_bounds, key=lambda item: item[2])
        has_separate_panes = any(
            bounds[0] >= leftmost_bounds[2]
            for bounds in scrollable_bounds
            if bounds != leftmost_bounds
        )
        if has_separate_panes and pane == "left":
            return leftmost_bounds
        if has_separate_panes and pane == "right":
            return rightmost_bounds

        return max(
            scrollable_bounds,
            key=lambda item: (item[2] - item[0]) * (item[3] - item[1]),
        )

    def _scroll(self, xml: str, *, down: bool, pane: str = "auto") -> None:
        nodes = self._settings_nodes_or_fallback(self._ui_nodes(xml))
        bounds = [bounds for _, bounds in nodes]
        if not bounds:
            raise ValueError("Settings UI 节点树中没有可滚动区域")
        scrollable_bounds = [
            bounds
            for attributes, bounds in nodes
            if attributes.get("scrollable", "").lower() == "true"
        ]
        left, top, right, bottom = self._select_scroll_bounds(
            scrollable_bounds or bounds, pane=pane
        )
        center_x = (left + right) // 2
        height = bottom - top
        start_y = top + height * (3 if down else 1) // 4
        end_y = top + height * (1 if down else 3) // 4
        self.adb.swipe(
            center_x,
            start_y,
            center_x,
            end_y,
            300,
        )

    def _scroll_down(self, xml: str, *, pane: str = "auto") -> None:
        self._scroll(xml, down=True, pane=pane)

    def _scroll_up(self, xml: str, *, pane: str = "auto") -> None:
        self._scroll(xml, down=False, pane=pane)

    def _scroll_to_top(self, *, pane: str = "auto") -> None:
        for _ in range(self._MAX_SCROLL_ATTEMPTS):
            self._scroll_up(self._wait_for_stable_settings_xml(), pane=pane)

    def _wait_for_labeled_bounds(
        self,
        labels: Sequence[str],
        *,
        timeout: float = 8.0,
        scroll: bool = False,
        scroll_pane: str = "auto",
    ) -> UiBounds:
        deadline = time.monotonic() + timeout
        last_error = ""
        next_scroll_at = time.monotonic() + self._INITIAL_SCROLL_DELAY_SECONDS
        scroll_attempts = 0
        while True:
            xml = self._settings_xml()
            try:
                return self._find_labeled_bounds(xml, labels)
            except ValueError as error:
                last_error = str(error)
            if time.monotonic() >= deadline:
                raise AssertionError(f"未加载 {'、'.join(labels)} 控件: {last_error}")
            if (
                scroll
                and scroll_attempts < self._MAX_SCROLL_ATTEMPTS
                and time.monotonic() >= next_scroll_at
            ):
                if scroll_attempts == 0:
                    self._scroll_to_top(pane=scroll_pane)
                self._scroll_down(
                    self._wait_for_stable_settings_xml(), pane=scroll_pane
                )
                scroll_attempts += 1
                next_scroll_at = time.monotonic() + 0.5
            time.sleep(0.2)

    def _wait_for_resource_bounds(
        self, resource_id: str, *, timeout: float = 8.0
    ) -> UiBounds:
        deadline = time.monotonic() + timeout
        last_error = ""
        while True:
            xml = self._settings_xml()
            try:
                return self._find_resource_bounds(xml, resource_id)
            except ValueError as error:
                last_error = str(error)
            if time.monotonic() >= deadline:
                raise AssertionError(f"未加载 {resource_id!r} 控件: {last_error}")
            time.sleep(0.2)

    def _find_reset_confirm_bounds(self, xml: str) -> UiBounds:
        try:
            return self._find_resource_bounds(xml, self._RESET_CONFIRM_RESOURCE_ID)
        except ValueError:
            return self._find_labeled_bounds(xml, self._RESET_CONFIRM_LABELS)

    def _wait_for_reset_confirm_bounds(self, *, timeout: float = 8.0) -> UiBounds:
        deadline = time.monotonic() + timeout
        last_error = ""
        while True:
            try:
                return self._find_reset_confirm_bounds(self._settings_xml())
            except ValueError as error:
                last_error = str(error)
            if time.monotonic() >= deadline:
                raise AssertionError(f"未加载重置确认控件: {last_error}")
            time.sleep(0.2)

    def _tap_labeled_item(
        self,
        labels: Sequence[str],
        *,
        scroll: bool = False,
        scroll_pane: str = "auto",
    ) -> None:
        bounds = self._wait_for_labeled_bounds(
            labels, scroll=scroll, scroll_pane=scroll_pane
        )
        stable_xml = self._wait_for_stable_settings_xml()
        try:
            bounds = self._find_labeled_bounds(stable_xml, labels)
        except ValueError:
            bounds = self._wait_for_labeled_bounds(
                labels, scroll=scroll, scroll_pane=scroll_pane
            )
        self.adb.tap(*self._center(bounds))

    def _wait_for_confirm_to_close(self) -> None:
        deadline = time.monotonic() + 8.0
        while True:
            try:
                self._find_resource_bounds(
                    self._settings_xml(), self._RESET_CONFIRM_RESOURCE_ID
                )
            except ValueError:
                return
            if time.monotonic() >= deadline:
                raise AssertionError("点击“重置”后确认窗口未关闭")
            time.sleep(0.2)

    def _confirm_reset(self) -> None:
        self._wait_for_reset_confirm_bounds()
        stable_xml = self._wait_for_stable_settings_xml()
        try:
            bounds = self._find_reset_confirm_bounds(stable_xml)
        except ValueError:
            self._tap_labeled_item(self._RESET_CONFIRM_LABELS)
        else:
            self.adb.tap(*self._center(bounds))
        self._wait_for_confirm_to_close()

    def _reset_from_reset_options(self) -> None:
        self._tap_labeled_item(
            self._RESET_BLUETOOTH_WLAN_LABELS,
            scroll=True,
            scroll_pane="right",
        )
        self._confirm_reset()

    def _open_settings(self) -> None:
        previous_signature = self._ui_signature(self._settings_xml())
        code, out, err = self.adb.shell(
            "am",
            "start",
            "-a",
            self._SETTINGS_ACTION,
            "-f",
            self._SETTINGS_ROOT_FLAGS,
        )
        if code != 0:
            details = "\n".join(part for part in (out, err) if part).strip()
            raise RuntimeError(f"无法打开系统设置: {details or code}")
        self._wait_for_settings_transition(previous_signature)

    def _reset_bluetooth_and_wlan_once(self) -> None:
        if self._tap_labeled_item_if_visible(self._RESET_BLUETOOTH_WLAN_LABELS):
            self._confirm_reset()
            return
        self._open_settings()
        self._tap_labeled_item(
            self._SYSTEM_LABELS, scroll=True, scroll_pane="left"
        )
        self._tap_labeled_item(
            self._RESET_OPTIONS_LABELS, scroll=True, scroll_pane="right"
        )
        self._reset_from_reset_options()

    def reset_bluetooth_and_wlan(self) -> None:
        """Reset Bluetooth and WLAN from the current page or Settings root."""
        for attempt in range(1, self._RESET_NAVIGATION_ATTEMPTS + 1):
            try:
                self._reset_bluetooth_and_wlan_once()
                return
            except AssertionError:
                if attempt == self._RESET_NAVIGATION_ATTEMPTS:
                    raise
                self._open_settings()