"""SystemUI scan-list parsing and wait assertions."""
from __future__ import annotations

import time
from xml.etree import ElementTree

import pytest

from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


def visible_systemui_ssids(settings_ui: AndroidSettingsUI) -> tuple[str, ...]:
    root = ElementTree.fromstring(settings_ui.device.dump_hierarchy())
    names = []
    for item in root.iter("node"):
        if item.get("resource-id") != "com.android.systemui:id/wifi_list":
            continue
        texts = [
            node.get("text", "").strip()
            for node in item.iter("node")
            if node.get("text", "").strip()
        ]
        if texts:
            names.append(texts[0])
    return tuple(names)


def wait_systemui_ssid(
    settings_ui: AndroidSettingsUI,
    ssid: str,
    *,
    present: bool,
    timeout: float,
) -> tuple[str, ...]:
    deadline = time.monotonic() + timeout
    visible: tuple[str, ...] = ()
    while time.monotonic() < deadline:
        visible = visible_systemui_ssids(settings_ui)
        if (ssid in visible) == present:
            return visible
        time.sleep(1.0)
    state = "出现" if present else "消失"
    pytest.fail(f"等待 SSID {ssid!r} 在 SystemUI {state}超时，可见={visible!r}")
    raise AssertionError("pytest.fail should not return")


def systemui_scan_snapshot(
    settings_ui: AndroidSettingsUI,
) -> tuple[tuple[str, str], ...]:
    root = ElementTree.fromstring(settings_ui.device.dump_hierarchy())
    rows = []
    for item in root.iter("node"):
        if item.get("resource-id") != "com.android.systemui:id/wifi_list":
            continue
        values = {
            node.get("resource-id", ""): node.get("text", "").strip()
            for node in item.iter("node")
        }
        title = values.get("com.android.systemui:id/wifi_title", "")
        if title:
            rows.append(
                (title, values.get("com.android.systemui:id/wifi_summary", ""))
            )
    return tuple(rows)
