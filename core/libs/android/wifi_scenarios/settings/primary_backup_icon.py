"""Settings primary/backup WiFi ordering scenarios."""

from __future__ import annotations

from collections.abc import Callable, Mapping
import re
import time
from typing import cast
from xml.etree import ElementTree

import allure
from PIL import Image
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.libs.android.wifi_scenarios.dual_link import (
    connect_dual_link_in_order,
    dual_link_legs as _entry_legs,
    primary_backup_entry,
    tune_dual_link_rssi,
    wait_for_primary_link,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.signal_level import signal_level_entry
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


_BOUNDS_RE = re.compile(r"\[(\d+),(\d+)]\[(\d+),(\d+)]")


def settings_ssid_rows(hierarchy: str, ssids: tuple[str, str]) -> dict[str, int]:
    """Return target SSID row top coordinates from the Settings hierarchy."""
    root = ElementTree.fromstring(hierarchy)
    parents = {child: parent for parent in root.iter() for child in parent}
    wanted = {ssid.casefold(): ssid for ssid in ssids}
    rows: dict[str, int] = {}
    for node in root.iter("node"):
        key = node.get("text", "").strip().casefold()
        if key not in wanted:
            continue
        container = node
        while container is not None and container.get("clickable") != "true":
            container = parents.get(container)
        if container is None:
            continue
        match = _BOUNDS_RE.fullmatch(container.get("bounds", ""))
        if match is not None:
            rows[wanted[key]] = int(match.group(2))
    return rows


def ssid_title_bounds(hierarchy: str, ssid: str) -> tuple[int, int, int, int] | None:
    root = ElementTree.fromstring(hierarchy)
    for node in root.iter("node"):
        if node.get("text", "").strip().casefold() != ssid.casefold():
            continue
        match = _BOUNDS_RE.fullmatch(node.get("bounds", ""))
        if match is not None:
            return (
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                int(match.group(4)),
            )
    return None


def has_orange_highlight(image: Image.Image, bounds: tuple[int, int, int, int]) -> bool:
    """Detect the product's orange primary-network title pixels."""
    rgb_image = image.convert("RGB").crop(bounds)
    orange_pixels = sum(
        1
        for x in range(rgb_image.width)
        for y in range(rgb_image.height)
        for red, green, blue in [cast(tuple[int, int, int], rgb_image.getpixel((x, y)))]
        if red >= 170 and 45 <= green <= 190 and blue <= 120 and red >= green + 45
    )
    return orange_pixels >= 4


def _assert_settings_primary(
    summary: str,
    settings_ui: AndroidSettingsUI,
    entry: DualWiFiEntry,
    expected: str,
) -> None:
    traditional, hyper = _entry_legs(entry)
    legs = {
        "wifi": cast(Mapping[str, str], traditional),
        "hyper": cast(Mapping[str, str], hyper),
    }
    expected_ssid = str(legs[expected].get("ssid") or "")
    other = "hyper" if expected == "wifi" else "wifi"
    other_ssid = str(legs[other].get("ssid") or "")
    settings_ui.open_wifi_settings()
    time.sleep(3.0)
    hierarchy = settings_ui.device.dump_hierarchy()
    rows = settings_ssid_rows(hierarchy, (expected_ssid, other_ssid))
    if set(rows) != {expected_ssid, other_ssid}:
        settings_ui.fail_with_artifacts(
            f"{summary}: WLAN 列表未同时显示双链路，rows={rows!r}"
        )
    if rows[expected_ssid] >= rows[other_ssid]:
        settings_ui.fail_with_artifacts(
            f"{summary}: primary {expected_ssid!r} 未显示在首行，rows={rows!r}"
        )

    bounds = ssid_title_bounds(hierarchy, expected_ssid)
    image = cast(Image.Image, settings_ui.device.screenshot(format="pillow"))
    if bounds is None or not has_orange_highlight(image, bounds):
        settings_ui.fail_with_artifacts(
            f"{summary}: primary {expected_ssid!r} 标题未检测到橙色高亮"
        )
    allure.attach(hierarchy, "Settings WLAN hierarchy", allure.attachment_type.XML)
    print(f"[{summary}] primary={expected}, first={expected_ssid!r}, rows={rows!r}")


@allure.step("执行 Settings 主备网络显示与切换验证")
def run_primary_backup_icon_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    attenuator: AttenuatorRig | None,
    *,
    settle_sec: float = 4.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")

    number_match = re.search(r"PriBakIcon_UI_(00[1-4])$", summary)
    if number_match is None:
        raise ValueError(f"未知 PriBakIcon 用例: {summary}")
    number = int(number_match.group(1))
    entry = primary_backup_entry(wifi_yaml)
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = attenuator.read_attenuations()
    if any(channel not in original for channel in channels.values()):
        pytest.fail(f"{summary}: 衰减器查询缺少目标通道，channels={channels!r}, state={original!r}")

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: RSSI 校准前双链路连接失败 "
                f"found={found!r} missing={missing!r}"
            )

        # 屏蔽箱内 0 dB 时传统 AP 约 -55 dBm，使用双方均可达的等强点。
        initial_targets = {"wifi": -80, "hyper": -50} if number == 2 else {"wifi": -60, "hyper": -60}
        tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            initial_targets,
            settle_sec=settle_sec,
        )
        initial_primary = "hyper" if number == 2 else "wifi"
        order = (initial_primary, "wifi" if initial_primary == "hyper" else "hyper")
        connect_dual_link_in_order(summary, wifi, entry, order)
        wait_for_primary_link(summary, run_shell_cmd, initial_primary)
        _assert_settings_primary(summary, settings_ui, entry, initial_primary)

        if number == 3:
            tune_dual_link_rssi(
                run_shell_cmd,
                attenuator,
                channels,
                entry,
                {"wifi": -80, "hyper": -70},
                settle_sec=settle_sec,
            )
            wait_for_primary_link(summary, run_shell_cmd, "hyper")
            _assert_settings_primary(summary, settings_ui, entry, "hyper")
            tune_dual_link_rssi(
                run_shell_cmd,
                attenuator,
                channels,
                entry,
                {"wifi": -60, "hyper": -70},
                settle_sec=settle_sec,
            )
            wait_for_primary_link(summary, run_shell_cmd, "wifi")
            _assert_settings_primary(summary, settings_ui, entry, "wifi")
        elif number == 4:
            traditional, _ = _entry_legs(entry)
            traditional_ssid = str(traditional.get("ssid") or "")
            network_id = wifi.find_network_id_by_ssid(traditional_ssid)
            if not network_id or not wifi.forget_network(network_id):
                pytest.fail(f"{summary}: 无法断开 primary {traditional_ssid!r}")
            wait_for_primary_link(summary, run_shell_cmd, "hyper")
            _assert_settings_primary(summary, settings_ui, entry, "hyper")
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])