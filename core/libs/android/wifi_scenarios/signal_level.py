"""Signal-level component scenarios driven by the laboratory attenuator."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import re
import time
from typing import cast
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from PIL import Image

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import (
    bssid_from_wifi_status,
    scan_result_rssi_for_bssid,
    scan_result_rssis,
    ssid_from_wifi_status,
    ssid_match,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry, get_wifi_list_entry
from core.utils.log_handler import get_logger


log = get_logger(__name__)


@dataclass(frozen=True)
class SignalLevelSpec:
    hyper: bool
    expected_bars: int
    target_rssis: tuple[int, ...]


_WIFI_SPECS = {
    1: SignalLevelSpec(False, 4, (-60,)),
    2: SignalLevelSpec(False, 3, (-66, -74)),
    3: SignalLevelSpec(False, 2, (-76, -81)),
    4: SignalLevelSpec(False, 1, (-84, -86)),
    5: SignalLevelSpec(False, 0, (-90,)),
}
_HYPER_SPECS = {
    6: SignalLevelSpec(True, 4, (-72,)),
    7: SignalLevelSpec(True, 3, (-74, -85)),
    8: SignalLevelSpec(True, 2, (-88, -92)),
    9: SignalLevelSpec(True, 1, (-95, -97)),
    10: SignalLevelSpec(True, 0, (-99,)),
}

_BAR_PATTERNS = {
    4: ("信号满格", "signal full", "four bars"),
    3: ("信号强度为三格", "three bars"),
    2: ("信号强度为两格", "two bars"),
    1: ("信号强度为一格", "one bar"),
    0: ("信号强度为零格", "无信号", "zero bars", "no signal"),
}


def signal_level_spec(summary: str) -> SignalLevelSpec:
    match = re.search(r"SignalLevel_UI_(\d{3})$", summary)
    if match is None:
        raise ValueError(f"未知 SignalLevel 用例: {summary}")
    number = int(match.group(1))
    spec = _WIFI_SPECS.get(number) or _HYPER_SPECS.get(number)
    if spec is None:
        raise ValueError(f"未知 SignalLevel 用例: {summary}")
    return spec


def signal_level_entry(wifi_yaml: dict, *, hyper: bool) -> tuple[WiFiEntry, int]:
    profile = wifi_yaml.get("signal_level_lab") or {}
    if not isinstance(profile, dict):
        raise ValueError("signal_level_lab 必须为映射")

    ap_index = int(profile.get("ap_index", 1))
    if hyper:
        dual_entry = get_dual_wifi_entry(
            wifi_yaml,
            entry_id=str(profile.get("hyper_dual_entry_id") or ""),
        )
        entry = dual_entry.get("hyper_wifi") or {}
    else:
        entry = get_wifi_list_entry(
            wifi_yaml,
            entry_id=str(profile.get("traditional_entry_id") or ""),
        )
    return cast(WiFiEntry, entry if isinstance(entry, dict) else {}), ap_index


def parse_signal_bars(description: str) -> int | None:
    normalized = (description or "").casefold()
    for bars, patterns in _BAR_PATTERNS.items():
        if any(pattern.casefold() in normalized for pattern in patterns):
            return bars
    return None


def signal_bars_for_ssid(hierarchy: str, ssid: str) -> int | None:
    """Extract the target SSID's signal bars from Settings or SystemUI XML."""
    root = ElementTree.fromstring(hierarchy)
    wanted = ssid.casefold()
    for node in root.iter("node"):
        description = node.get("content-desc", "")
        if wanted in description.casefold():
            bars = parse_signal_bars(description)
            if bars is not None:
                return bars

        descendants = tuple(node.iter("node"))
        has_target = any(
            child.get("text", "").strip().casefold() == wanted
            for child in descendants
        )
        if not has_target:
            continue
        for child in descendants:
            bars = parse_signal_bars(child.get("content-desc", ""))
            if bars is not None:
                return bars
    return None


def wifi_icon_bounds_for_ssid(
    hierarchy: str, ssid: str
) -> tuple[int, int, int, int] | None:
    root = ElementTree.fromstring(hierarchy)
    parents = {child: parent for parent in root.iter() for child in parent}
    wanted = ssid.casefold()
    for node in root.iter("node"):
        if node.get("text", "").strip().casefold() != wanted:
            continue
        container = node
        for _ in range(4):
            icons = [
                child
                for child in container.iter("node")
                if child.get("resource-id", "").endswith(
                    ("wifi_connected_icon", "wifi_icon")
                )
            ]
            if icons:
                values = [int(value) for value in re.findall(r"\d+", icons[0].get("bounds", ""))]
                return (values[0], values[1], values[2], values[3]) if len(values) == 4 else None
            container = parents.get(container)
            if container is None:
                break
    return None


def signal_bars_from_icon(image: Image.Image) -> int:
    icon = image.convert("L").resize((20, 20))
    top_arc = None
    for y in range(20):
        longest_run = 0
        current_run = 0
        for x in range(20):
            if cast(float, icon.getpixel((x, y))) < 180:
                current_run += 1
                longest_run = max(longest_run, current_run)
            else:
                current_run = 0
        if longest_run >= 8:
            top_arc = y
            break
    if top_arc is None:
        return 0
    if top_arc <= 5:
        return 4
    if top_arc <= 8:
        return 3
    if top_arc <= 11:
        return 2
    return 1


def tune_attenuation_for_rssi(
    attenuator: AttenuatorRig,
    channel: int,
    target_rssi: int,
    read_rssi: Callable[[], int | None],
    *,
    settle_sec: float = 4.0,
    tolerance_db: int = 1,
    max_attempts: int = 24,
    max_adjustment_db: float = 6.0,
    allow_missing: bool = False,
) -> tuple[float, int | None]:
    """Adjust attenuation from a measured baseline until RSSI reaches target."""
    attenuation = 0.0
    max_attenuation = float(attenuator.max_attenuation_db)
    best: tuple[float, int] | None = None
    consecutive_missing = 0

    for _ in range(max_attempts):
        attenuator.set_attenuation(channel, attenuation)
        time.sleep(settle_sec)
        measured = read_rssi()
        log.info(
            "衰减闭环 channel=%s attenuation=%s dB target=%s dBm measured=%s",
            channel,
            attenuation,
            target_rssi,
            measured,
        )
        if measured is None:
            consecutive_missing += 1
            if allow_missing and consecutive_missing >= 2:
                return attenuation, None
            next_attenuation = (
                attenuation
                if allow_missing
                else max(0.0, attenuation - max_adjustment_db / 2)
            )
            if next_attenuation == attenuation:
                if allow_missing:
                    continue
                break
            attenuation = next_attenuation
            continue
        consecutive_missing = 0

        if best is None or abs(measured - target_rssi) < abs(best[1] - target_rssi):
            best = (attenuation, measured)
        if abs(measured - target_rssi) <= tolerance_db:
            return attenuation, measured

        adjustment_limit = min(max_adjustment_db, 2.0) if measured <= -85 else max_adjustment_db
        adjustment = min(
            adjustment_limit,
            max(-adjustment_limit, float(measured - target_rssi)),
        )
        next_attenuation = min(
            max_attenuation,
            max(0.0, attenuation + adjustment),
        )
        if next_attenuation == attenuation:
            break
        attenuation = next_attenuation

    if best is None:
        pytest.fail(f"通道 {channel} 无法读取 RSSI，目标={target_rssi} dBm")
    pytest.fail(
        f"通道 {channel} 无法达到目标 RSSI {target_rssi}±{tolerance_db} dBm；"
        f"最接近值={best[1]} dBm，衰减={best[0]:g} dB"
    )


def _traditional_rssi_reader(
    run_shell_cmd: Callable[[str], str], ssid: str, bssid: str = ""
) -> Callable[[], int | None]:
    def read() -> int | None:
        run_shell_cmd("cmd wifi start-scan")
        time.sleep(2.0)
        scan_results = run_shell_cmd("cmd wifi list-scan-results")
        if bssid:
            measured = scan_result_rssi_for_bssid(scan_results, bssid)
            if measured is not None:
                return measured
        else:
            values = scan_result_rssis(scan_results, ssid)
            if values:
                return max(values)
        status = run_shell_cmd("cmd wifi status")
        if ssid_match(ssid, ssid_from_wifi_status(status)):
            match = re.search(r"\bRSSI:\s*(-?\d+)\b", status)
            if match is not None:
                return int(match.group(1))
        return None

    return read


def _hyper_rssi_reader(
    run_shell_cmd: Callable[[str], str],
) -> Callable[[], int | None]:
    def read() -> int | None:
        output = run_shell_cmd("cli_app show signal")
        values = [int(value) for value in re.findall(r"rssi\s*:\s*(-?\d+)", output)]
        return values[-1] if values else None

    return read


def _assert_ui_bars(
    summary: str,
    settings_ui: AndroidSettingsUI,
    ssid: str,
    expected_bars: int,
    *,
    surface: str,
    allow_missing: bool = False,
) -> None:
    if surface == "settings":
        settings_ui.open_wifi_settings()
        settings_ui.scroll_to_text(ssid)
    elif surface == "systemui":
        from core.libs.android.systemui_pages.quick_settings_page import open_internet_dialog

        open_internet_dialog(settings_ui, capture=False)
    else:
        raise ValueError(f"未知信号等级界面: {surface!r}")

    deadline = time.monotonic() + 10.0
    actual_bars = None
    while time.monotonic() < deadline:
        hierarchy = settings_ui.device.dump_hierarchy()
        actual_bars = signal_bars_for_ssid(hierarchy, ssid)
        if actual_bars is None:
            bounds = wifi_icon_bounds_for_ssid(hierarchy, ssid)
            if bounds is not None:
                image = cast(Image.Image, settings_ui.device.screenshot(format="pillow"))
                actual_bars = signal_bars_from_icon(image.crop(bounds))
        if actual_bars == expected_bars:
            return
        time.sleep(1.0)
    if actual_bars is None:
        if allow_missing and expected_bars == 0:
            return
        settings_ui.fail_with_artifacts(
            f"{summary}: {surface} 未找到 SSID {ssid!r} 的信号图标或等级描述"
        )
    if actual_bars != expected_bars:
        settings_ui.fail_with_artifacts(
            f"{summary}: {surface} 中 SSID {ssid!r} 期望 {expected_bars} 格，"
            f"实际 {actual_bars} 格"
        )


@allure.step("执行信号等级验证")
def run_signal_level_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    attenuator: AttenuatorRig | None,
    *,
    surface: str,
    settle_sec: float = 4.0,
) -> None:
    """Run one Settings/SystemUI signal-level case and restore attenuation."""
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")

    spec = signal_level_spec(summary)
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=spec.hyper)
    ssid = (entry.get("ssid") or "").strip()
    if not ssid:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 signal_level_lab 对应网络配置")

    channel = attenuator.channel_for(hyper=spec.hyper, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: 衰减器查询结果不包含通道 {channel}: {current!r}")
    original = current[channel]

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(settle_sec)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        connected_status = run_shell_cmd("cmd wifi status")
        read_rssi = (
            _hyper_rssi_reader(run_shell_cmd)
            if spec.hyper
            else _traditional_rssi_reader(
                run_shell_cmd,
                ssid,
                bssid_from_wifi_status(connected_status),
            )
        )
        for target_rssi in spec.target_rssis:
            attenuation_db, measured_rssi = tune_attenuation_for_rssi(
                attenuator,
                channel,
                target_rssi,
                read_rssi,
                settle_sec=settle_sec,
                allow_missing=spec.expected_bars == 0,
            )
            _assert_ui_bars(
                summary,
                settings_ui,
                ssid,
                spec.expected_bars,
                surface=surface,
                allow_missing=measured_rssi is None,
            )
            print(
                f"[{summary}] {surface}: SSID={ssid!r}, channel={channel}, "
                f"attenuation={attenuation_db:g} dB, RSSI={measured_rssi}, "
                f"signal={spec.expected_bars} bars"
            )
    finally:
        attenuator.set_attenuation(channel, original)