"""Android SoftAP control through Settings UI and Wi-Fi service state."""
from __future__ import annotations

import re
import time
from typing import Callable, Dict, List, Tuple
from xml.etree import ElementTree

import uiautomator2 as u2

from core.utils.adb_helper import AdbHelper

UiBounds = Tuple[int, int, int, int]
UiNode = Tuple[Dict[str, str], UiBounds]


class SoftAPControl:
    """Control the system WLAN hotspot without ROM-specific coordinates."""

    _SETTINGS_ACTION = "android.settings.TETHER_SETTINGS"
    _SETTINGS_ROOT_FLAGS = "0x10008000"
    _MAIN_SWITCH = "WLAN热点"
    _AUTO_OFF_SWITCH = "自动关闭热点"
    _SECURITY_LABEL = "安全性"
    _SECURITY_OPTIONS = (
        "WPA3-Personal",
        "WPA2/WPA3-Personal",
        "WPA2-Personal",
        "无",
    )
    _COMPATIBILITY_LABELS = ("速度与兼容性", "速度和兼容性", "AP Band", "AP频段")
    _COMPATIBILITY_OPTIONS = ("2.4GHz", "5GHz")
    _BAND_OPTION_PATTERN = re.compile(
        r"(?:首选|优先|仅|prefer(?:red)?|only)?"
        r"(2\.4|5(?:\.0)?|6(?:\.0)?)GHz(?:频段|band)?",
        re.IGNORECASE,
    )

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
    def _matches_label(attributes: Dict[str, str], label: str) -> bool:
        normalized_label = "".join(label.split())
        return any(
            "".join(value.split()) == normalized_label
            for value in (attributes.get("text"), attributes.get("content-desc"))
            if value
        )

    @staticmethod
    def _center(bounds: UiBounds) -> Tuple[int, int]:
        left, top, right, bottom = bounds
        return (left + right) // 2, (top + bottom) // 2

    @staticmethod
    def _vertical_gap(first: UiBounds, second: UiBounds) -> int:
        if first[3] < second[1]:
            return second[1] - first[3]
        if second[3] < first[1]:
            return first[1] - second[3]
        return 0

    def _find_labeled_bounds(self, xml: str, label: str) -> UiBounds:
        for attributes, bounds in self._ui_nodes(xml):
            if self._matches_label(attributes, label):
                return bounds
        raise ValueError(f"未找到文本或 content-desc 为 {label!r} 的控件")

    def _labeled_summary(self, label: str) -> str:
        nodes = self._ui_nodes(self._settings_xml())
        labeled_nodes = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if self._matches_label(attributes, label)
        ]
        if not labeled_nodes:
            raise ValueError(f"未找到文本或 content-desc 为 {label!r} 的控件")

        label_attributes, label_bounds = labeled_nodes[0]
        label_text = self._node_text(label_attributes)
        candidates = [
            (self._node_text(attributes), bounds)
            for attributes, bounds in nodes
            if self._node_text(attributes) and self._node_text(attributes) != label_text
        ]
        if not candidates:
            raise ValueError(f"未找到 {label!r} 的摘要文本")

        def score(candidate: Tuple[str, UiBounds]) -> Tuple[int, int, int]:
            _, bounds = candidate
            return (
                self._vertical_gap(label_bounds, bounds),
                abs(label_bounds[0] - bounds[0]),
                abs(self._center(label_bounds)[1] - self._center(bounds)[1]),
            )

        return min(candidates, key=score)[0]

    def _find_labeled_switch(self, xml: str, label: str) -> UiNode:
        nodes = self._ui_nodes(xml)
        labeled_nodes = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if self._matches_label(attributes, label)
        ]
        if not labeled_nodes:
            raise ValueError(f"未找到文本或 content-desc 为 {label!r} 的控件")

        for attributes, bounds in labeled_nodes:
            if attributes.get("checkable", "").lower() == "true":
                return attributes, bounds

        switches = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if attributes.get("checkable", "").lower() == "true"
        ]
        if not switches:
            raise ValueError(f"未找到 {label!r} 对应的 checkable 开关")

        def score(candidate: UiNode) -> Tuple[int, int, int, int]:
            attributes, bounds = candidate
            label_bounds = min(
                labeled_nodes,
                key=lambda item: self._vertical_gap(item[1], bounds),
            )[1]
            label_x, label_y = self._center(label_bounds)
            switch_x, switch_y = self._center(bounds)
            resource = attributes.get("resource-id", "").lower()
            class_name = attributes.get("class", "").lower()
            return (
                self._vertical_gap(label_bounds, bounds),
                abs(label_y - switch_y),
                0 if switch_x >= label_x else 1,
                0 if "switch" in resource or "switch" in class_name else 1,
            )

        return min(switches, key=score)

    def _switch_enabled(self, label: str) -> bool:
        attributes, _ = self._find_labeled_switch(self._settings_xml(), label)
        checked = attributes.get("checked")
        if checked is None:
            raise ValueError(f"{label!r} 控件没有 checked 属性")
        return checked.lower() == "true"

    @staticmethod
    def _checked(attributes: Dict[str, str], label: str) -> bool:
        checked = attributes.get("checked")
        if checked is None:
            raise ValueError(f"{label!r} 控件没有 checked 属性")
        return checked.lower() == "true"

    def _hotspot_switch_state_and_bounds(self) -> Tuple[bool, UiBounds]:
        attributes, bounds = self._find_labeled_switch(
            self._settings_xml(), self._MAIN_SWITCH
        )
        return self._checked(attributes, self._MAIN_SWITCH), bounds

    @staticmethod
    def _is_selected(attributes: Dict[str, str]) -> bool:
        return any(
            attributes.get(name, "").lower() == "true"
            for name in ("checked", "selected")
        )

    @classmethod
    def _band_option(cls, attributes: Dict[str, str]) -> str | None:
        for name in ("text", "content-desc"):
            text = "".join(attributes.get(name, "").split())
            match = cls._BAND_OPTION_PATTERN.fullmatch(text)
            if match:
                return f"{float(match.group(1)):g}GHz"
        return None

    @classmethod
    def _band_summary(cls, attributes: Dict[str, str]) -> str:
        text = cls._node_text(attributes)
        band = cls._band_option(attributes)
        if band is None:
            return text
        return re.sub(
            r"(?:2\.4|5(?:\.0)?|6(?:\.0)?)GHz",
            band, text, flags=re.IGNORECASE,
        )

    def _compatibility_setting(self, xml: str) -> Tuple[str, UiBounds]:
        """Resolve a band preference by its own title/summary subtree."""
        root = ElementTree.fromstring(xml)
        parents = {child: parent for parent in root.iter() for child in parent}
        candidates: List[Tuple[bool, str, UiBounds]] = []
        for summary in root.iter("node"):
            if not summary.get("resource-id", "").endswith("/summary"):
                continue
            row = parents.get(summary)
            while row is not None:
                descendants = list(row.iter("node"))
                titles = [
                    node for node in descendants
                    if node.get("resource-id", "").endswith("/title")
                ]
                summaries = [
                    node for node in descendants
                    if node.get("resource-id", "").endswith("/summary")
                ]
                if len(titles) == 1 and len(summaries) == 1:
                    known_title = any(
                        self._matches_label(titles[0].attrib, label)
                        for label in self._COMPATIBILITY_LABELS
                    )
                    band = self._band_option(summary.attrib)
                    bounds = row.get("bounds") or titles[0].get("bounds")
                    if (
                        bounds and (known_title or band is not None)
                        and not any(
                            node.get("checkable", "").lower() == "true"
                            for node in descendants
                        )
                    ):
                        text = self._band_summary(summary.attrib)
                        candidates.append((known_title, text, self._parse_bounds(bounds)))
                        break
                row = parents.get(row)

        preferred = [candidate for candidate in candidates if candidate[0]] or candidates
        if len(preferred) == 1:
            _, summary_text, bounds = preferred[0]
            return summary_text, bounds
        if preferred:
            raise ValueError("发现多个可能的热点频段设置项，无法唯一定位")
        for label in self._COMPATIBILITY_LABELS:
            try:
                bounds = self._find_labeled_bounds(xml, label)
            except ValueError:
                continue
            try:
                text = self._labeled_summary(label)
            except ValueError:
                text = ""
            return self._band_summary({"text": text}), bounds
        raise ValueError("未找到热点频段设置项（AP Band/速度与兼容性）")

    def _option_nodes(
        self, xml: str, expected_options: Tuple[str, ...]
    ) -> List[Tuple[str, Dict[str, str], UiBounds]]:
        matches: Dict[str, UiNode] = {}
        for attributes, bounds in self._ui_nodes(xml):
            if expected_options == self._COMPATIBILITY_OPTIONS:
                option = self._band_option(attributes)
            else:
                option = next(
                    (
                        expected for expected in expected_options
                        if self._matches_label(attributes, expected)
                        or self._matches_label(attributes, f"{expected}频段")
                    ),
                    None,
                )
            if option is not None and (
                option not in matches or bounds[1] < matches[option][1][1]
            ):
                matches[option] = (attributes, bounds)
        return sorted(
            [(option, attributes, bounds) for option, (attributes, bounds) in matches.items()],
            key=lambda item: (item[2][1], item[2][0]),
        )

    def _option_page_from_xml(
        self, xml: str, expected_options: Tuple[str, ...]
    ) -> Tuple[List[str], str | None]:
        nodes = self._ui_nodes(xml)
        option_nodes = self._option_nodes(xml, expected_options)
        options = [expected for expected, _, _ in option_nodes]

        selected = next(
            (
                expected
                for expected, attributes, _ in option_nodes
                if self._is_selected(attributes)
            ),
            None,
        )
        if selected is not None:
            return options, selected

        selected_nodes = [node for node in nodes if self._is_selected(node[0])]
        for expected, _, bounds in option_nodes:
            same_row = [
                candidate
                for candidate in selected_nodes
                if self._vertical_gap(bounds, candidate[1]) == 0
            ]
            if same_row:
                return options, expected
        return options, None

    def _is_option_editor_page(
        self, xml: str, expected_options: Tuple[str, ...]
    ) -> bool:
        nodes = self._ui_nodes(xml)
        checkable_nodes = [
            (attributes, bounds)
            for attributes, bounds in nodes
            if attributes.get("checkable", "").lower() == "true"
        ]
        for _, attributes, bounds in self._option_nodes(xml, expected_options):
            if attributes.get("checkable", "").lower() == "true":
                return True
            if any(
                self._vertical_gap(bounds, checkable_bounds) == 0
                for _, checkable_bounds in checkable_nodes
            ):
                return True
        return False

    def _open_option_editor(
        self, labels: Tuple[str, ...], expected_options: Tuple[str, ...]
    ) -> Tuple[List[str], str | None]:
        current_xml = self._settings_xml()
        before_options, before_selected = self._option_page_from_xml(
            current_xml, expected_options
        )
        if self._is_option_editor_page(current_xml, expected_options):
            return before_options, before_selected

        if expected_options == self._COMPATIBILITY_OPTIONS:
            _, bounds = self._compatibility_setting(current_xml)
            self._tap(bounds)
        else:
            for label in labels:
                try:
                    self._tap(self._find_labeled_bounds(current_xml, label))
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"未找到设置项: {labels!r}")

        deadline = time.monotonic() + 5.0
        last_options: List[str] = before_options
        last_selected = None
        while True:
            current_xml = self._settings_xml()
            last_options, last_selected = self._option_page_from_xml(
                current_xml, expected_options
            )
            if (
                self._is_option_editor_page(current_xml, expected_options)
                and len(last_options) >= len(expected_options)
            ):
                return last_options, last_selected
            if time.monotonic() >= deadline:
                return last_options, last_selected
            time.sleep(0.2)

    def _tap(self, bounds: UiBounds) -> None:
        self.adb.tap(*self._center(bounds))

    def _wait_for_switch(
        self,
        label: str,
        expected: bool,
        timeout: float = 15.0,
        poll_interval_seconds: float = 0.5,
    ) -> None:
        if poll_interval_seconds <= 0:
            raise ValueError("开关状态轮询间隔必须大于 0")
        deadline = time.monotonic() + timeout
        last_error = ""
        while True:
            try:
                actual = self._switch_enabled(label)
                if actual == expected:
                    return
                last_error = f"实际状态为 {actual}"
            except ValueError as error:
                last_error = str(error)
            if time.monotonic() >= deadline:
                raise AssertionError(f"{label} 状态未变为 {expected}: {last_error}")
            time.sleep(min(poll_interval_seconds, deadline - time.monotonic()))

    def open_settings(self) -> None:
        self.adb.shell(
            "am",
            "start",
            "-a",
            self._SETTINGS_ACTION,
            "-f",
            self._SETTINGS_ROOT_FLAGS,
        )
        time.sleep(1.0)
        xml = self._settings_xml()
        try:
            self._find_labeled_switch(xml, self._AUTO_OFF_SWITCH)
        except ValueError:
            self._tap(self._find_labeled_bounds(xml, self._MAIN_SWITCH))
            deadline = time.monotonic() + 10.0
            while True:
                try:
                    self._find_labeled_switch(self._settings_xml(), self._AUTO_OFF_SWITCH)
                    return
                except ValueError as error:
                    if time.monotonic() >= deadline:
                        raise AssertionError(f"未加载 {self._AUTO_OFF_SWITCH} 控件: {error}") from error
                    time.sleep(0.5)

    def enable_hotspot(self) -> None:
        self.set_hotspot_enabled(True)

    def set_hotspot_enabled(
        self,
        enabled: bool,
        *,
        poll_interval_seconds: float = 0.5,
    ) -> None:
        """设置 WLAN 热点开关，并确认 Settings UI 中的实际状态。"""
        if self._switch_enabled(self._MAIN_SWITCH) != enabled:
            _, bounds = self._find_labeled_switch(self._settings_xml(), self._MAIN_SWITCH)
            self._tap(bounds)
        self._wait_for_switch(
            self._MAIN_SWITCH,
            enabled,
            poll_interval_seconds=poll_interval_seconds,
        )

    def _toggle_hotspot_cycles_with_cached_bounds(
        self,
        cycles: int,
        *,
        on_progress: Callable[[int, str], None] | None,
        poll_interval_seconds: float,
    ) -> None:
        current_state, cached_bounds = self._hotspot_switch_state_and_bounds()
        for cycle in range(1, cycles + 1):
            for enabled, operation in ((False, "关闭"), (True, "打开")):
                try:
                    if current_state != enabled:
                        self._tap(cached_bounds)
                    deadline = time.monotonic() + 15.0
                    while True:
                        actual_state, current_bounds = (
                            self._hotspot_switch_state_and_bounds()
                        )
                        if current_bounds != cached_bounds and actual_state != enabled:
                            cached_bounds = current_bounds
                            self._tap(cached_bounds)
                        if actual_state == enabled:
                            cached_bounds = current_bounds
                            current_state = actual_state
                            break
                        if time.monotonic() >= deadline:
                            raise AssertionError(
                                f"{self._MAIN_SWITCH} 状态未变为 {enabled}: "
                                f"实际状态为 {actual_state}"
                            )
                        time.sleep(
                            min(
                                poll_interval_seconds,
                                deadline - time.monotonic(),
                            )
                        )
                except (AssertionError, RuntimeError, ValueError) as error:
                    raise AssertionError(
                        f"设备第{cycle}次{operation}热点开关异常"
                    ) from error
                if on_progress is not None:
                    on_progress(cycle, operation)

    def toggle_hotspot_cycles(
        self,
        cycles: int,
        *,
        on_progress: Callable[[int, str], None] | None = None,
        poll_interval_seconds: float = 0.5,
        cache_main_switch_bounds: bool = False,
    ) -> None:
        """每轮关闭再打开热点；不插入固定动作间隔。"""
        if cycles < 1:
            raise ValueError("热点开关循环次数必须大于 0")
        if poll_interval_seconds <= 0:
            raise ValueError("开关状态轮询间隔必须大于 0")
        if cache_main_switch_bounds:
            self._toggle_hotspot_cycles_with_cached_bounds(
                cycles,
                on_progress=on_progress,
                poll_interval_seconds=poll_interval_seconds,
            )
            return

        for cycle in range(1, cycles + 1):
            for enabled, operation in ((False, "关闭"), (True, "打开")):
                try:
                    self.set_hotspot_enabled(
                        enabled,
                        poll_interval_seconds=poll_interval_seconds,
                    )
                except (AssertionError, RuntimeError, ValueError) as error:
                    raise AssertionError(
                        f"设备第{cycle}次{operation}热点开关异常"
                    ) from error
                if on_progress is not None:
                    on_progress(cycle, operation)

    def enable_auto_shutdown(self) -> None:
        if not self._switch_enabled(self._AUTO_OFF_SWITCH):
            _, bounds = self._find_labeled_switch(self._settings_xml(), self._AUTO_OFF_SWITCH)
            self._tap(bounds)
        self._wait_for_switch(self._AUTO_OFF_SWITCH, True)

    def disable_auto_shutdown(self) -> None:
        if self._switch_enabled(self._AUTO_OFF_SWITCH):
            _, bounds = self._find_labeled_switch(self._settings_xml(), self._AUTO_OFF_SWITCH)
            self._tap(bounds)
        self._wait_for_switch(self._AUTO_OFF_SWITCH, False)

    def is_hotspot_enabled(self) -> bool:
        return self._switch_enabled(self._MAIN_SWITCH)

    def is_auto_shutdown_enabled(self) -> bool:
        return self._switch_enabled(self._AUTO_OFF_SWITCH)

    def security_summary(self) -> str:
        return self._labeled_summary(self._SECURITY_LABEL)

    def is_security_editor_open(self) -> bool:
        return self._is_option_editor_page(
            self._settings_xml(), self._SECURITY_OPTIONS
        )

    def open_security_editor(self) -> Tuple[List[str], str | None]:
        return self._open_option_editor((self._SECURITY_LABEL,), self._SECURITY_OPTIONS)

    def open_compatibility_editor(self) -> Tuple[List[str], str | None]:
        """Read displayed band choices as canonical values, e.g. 5.0 GHz -> 5GHz."""
        return self._open_option_editor(
            self._COMPATIBILITY_LABELS, self._COMPATIBILITY_OPTIONS
        )

    def compatibility_summary(self) -> str:
        """Read the band row summary, normalizing only its band notation."""
        summary, _ = self._compatibility_setting(self._settings_xml())
        if not summary:
            raise ValueError("未找到热点频段设置项的摘要文本")
        return summary

    def connected_client_count(self) -> int:
        wifi_dump = self._shell_text("dumpsys wifi")
        connected_clients = re.search(
            r"mRole:\s*ROLE_SOFTAP_TETHERED(?:(?!Dump of SoftApManager).)*?"
            r"getConnectedClientList\(\)\.size\(\):\s*(\d+)",
            wifi_dump,
            flags=re.DOTALL,
        )
        if connected_clients:
            return int(connected_clients.group(1))
        if "ROLE_SOFTAP_TETHERED" in wifi_dump:
            raise RuntimeError("无法从活动热点的 dumpsys wifi 输出解析客户端数量")
        return 0

    def is_hotspot_active(self) -> bool:
        """通过 Wi-Fi 服务状态判断热点是否活动，不依赖 Settings 当前页面。"""
        return "ROLE_SOFTAP_TETHERED" in self._shell_text("dumpsys wifi")

    def _device_uptime_seconds(self) -> float:
        output = self._shell_text("cat /proc/uptime")
        try:
            return float(output.split()[0])
        except (IndexError, ValueError) as error:
            raise RuntimeError(f"无法解析设备运行时长: {output!r}") from error

    def _assert_expected_switch_states(
        self,
        *,
        hotspot_enabled: bool | None,
        auto_shutdown_enabled: bool | None,
    ) -> None:
        expected_states = (
            (self._MAIN_SWITCH, hotspot_enabled),
            (self._AUTO_OFF_SWITCH, auto_shutdown_enabled),
        )
        for label, expected in expected_states:
            if expected is not None and self._switch_enabled(label) != expected:
                expected_text = "开启" if expected else "关闭"
                raise AssertionError(f"等待期间 {label} 未保持{expected_text}")

    def wait_for_no_client_window(
        self,
        timeout_seconds: int,
        *,
        on_progress: Callable[[int], None],
        poll_interval_seconds: int = 10,
        expected_hotspot_enabled: bool | None = None,
        expected_auto_shutdown_enabled: bool | None = None,
    ) -> bool:
        """等待期间监控客户端和指定的热点开关状态。"""
        remaining = timeout_seconds
        last_reported_remaining = None
        while remaining > 0:
            if self.connected_client_count() > 0:
                return True
            self._assert_expected_switch_states(
                hotspot_enabled=expected_hotspot_enabled,
                auto_shutdown_enabled=expected_auto_shutdown_enabled,
            )
            if (
                last_reported_remaining is None
                or remaining <= last_reported_remaining - 60
            ):
                on_progress(remaining)
                last_reported_remaining = remaining
            sleep_seconds = min(poll_interval_seconds, remaining)
            time.sleep(sleep_seconds)
            remaining -= sleep_seconds
        if self.connected_client_count() > 0:
            return True
        self._assert_expected_switch_states(
            hotspot_enabled=expected_hotspot_enabled,
            auto_shutdown_enabled=expected_auto_shutdown_enabled,
        )
        return False

    def wait_for_auto_shutdown_window(
        self,
        *,
        earliest_shutdown_seconds: float,
        latest_shutdown_seconds: float,
        on_progress: Callable[[int], None],
        poll_interval_seconds: int = 2,
        boundary_poll_interval_seconds: float = 0.25,
        boundary_precision_window_seconds: float = 45,
    ) -> bool:
        """等待热点在指定时间窗口内因空闲自动关闭。"""
        if earliest_shutdown_seconds < 0 or latest_shutdown_seconds < earliest_shutdown_seconds:
            raise ValueError("自动关闭时间窗口无效")
        if poll_interval_seconds <= 0 or boundary_poll_interval_seconds <= 0:
            raise ValueError("自动关闭轮询间隔必须大于 0")
        if boundary_precision_window_seconds < 0:
            raise ValueError("自动关闭边界精度窗口不能小于 0")

        started_at = time.monotonic()
        started_device_uptime = self._device_uptime_seconds()
        last_reported_remaining = None
        while True:
            elapsed = time.monotonic() - started_at
            if not self.is_hotspot_active():
                device_elapsed = self._device_uptime_seconds() - started_device_uptime
                if elapsed < earliest_shutdown_seconds:
                    raise AssertionError(
                        f"WLAN热点开关过早关闭：主机侧经过 {elapsed:.1f} 秒，"
                        f"设备侧经过 {device_elapsed:.1f} 秒，"
                        f"最早允许 {earliest_shutdown_seconds:.1f} 秒"
                    )
                return False

            client_count = self.connected_client_count()
            if client_count > 0:
                return True
            if elapsed >= latest_shutdown_seconds:
                device_elapsed = self._device_uptime_seconds() - started_device_uptime
                raise AssertionError(
                    f"WLAN热点开关未在 {latest_shutdown_seconds:.1f} 秒内自动关闭："
                    f"主机侧经过 {elapsed:.1f} 秒，设备侧经过 {device_elapsed:.1f} 秒，"
                    f"当前客户端数 {client_count}"
                )

            remaining = max(0, int(latest_shutdown_seconds - elapsed))
            if last_reported_remaining is None or remaining <= last_reported_remaining - 60:
                on_progress(remaining)
                last_reported_remaining = remaining
            poll_interval = (
                boundary_poll_interval_seconds
                if elapsed >= earliest_shutdown_seconds - boundary_precision_window_seconds
                else poll_interval_seconds
            )
            time.sleep(min(poll_interval, latest_shutdown_seconds - elapsed))