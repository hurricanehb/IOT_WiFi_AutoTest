"""Pure XML parsers for SystemUI WiFi surfaces."""
from __future__ import annotations

import re
from dataclasses import dataclass
from xml.etree import ElementTree

_BOUNDS_RE = re.compile(r"\[(\d+),(\d+)]\[(\d+),(\d+)]")


@dataclass(frozen=True)
class SystemUIConnectedWifiRow:
    ssid: str
    summary: str
    resources: dict[str, tuple[int, int, int, int]]


@dataclass(frozen=True)
class SystemUIStatusBarWifiIcon:
    link: str
    bounds: tuple[int, int, int, int]
    description: str


def systemui_status_bar_wifi_icons(
    hierarchy: str,
) -> tuple[SystemUIStatusBarWifiIcon, ...]:
    root = ElementTree.fromstring(hierarchy)
    resource_links = {
        "com.android.systemui:id/wifi_signal": "wifi",
        "com.android.systemui:id/sub_wifi_signal": "hyper",
    }
    icons = []
    for node in root.iter("node"):
        link = resource_links.get(node.get("resource-id", ""))
        bounds_match = _BOUNDS_RE.fullmatch(node.get("bounds", ""))
        if link is None or bounds_match is None:
            continue
        icons.append(
            SystemUIStatusBarWifiIcon(
                link=link,
                bounds=tuple(int(value) for value in bounds_match.groups()),
                description=node.get("content-desc", "").strip(),
            )
        )
    return tuple(sorted(icons, key=lambda icon: icon.bounds[0]))


def systemui_connected_wifi_row(hierarchy: str) -> SystemUIConnectedWifiRow | None:
    root = ElementTree.fromstring(hierarchy)
    for layout in root.iter("node"):
        if layout.get("resource-id") != "com.android.systemui:id/wifi_connected_layout":
            continue
        ssid = ""
        summary = ""
        resources: dict[str, tuple[int, int, int, int]] = {}
        for node in layout.iter("node"):
            resource_id = node.get("resource-id", "")
            if resource_id == "com.android.systemui:id/wifi_connected_title":
                ssid = node.get("text", "").strip()
            elif resource_id == "com.android.systemui:id/wifi_connected_summary":
                summary = node.get("text", "").strip()
            bounds_match = _BOUNDS_RE.fullmatch(node.get("bounds", ""))
            if resource_id and bounds_match:
                resources[resource_id] = tuple(
                    int(value) for value in bounds_match.groups()
                )
        return SystemUIConnectedWifiRow(ssid, summary, resources)
    return None
