"""Product-independent dual-WiFi role and RSSI helpers."""
from __future__ import annotations

import re
import time
from collections.abc import Callable, Mapping
from typing import cast

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.libs.android.wifi_scenarios.signal_level import (
    _hyper_rssi_reader,
    _traditional_rssi_reader,
    signal_level_entry,
    tune_attenuation_for_rssi,
)

_ROLE_RE = re.compile(
    r"iface=(?P<iface>[\w.-]+)\s+role=(?P<role>ROLE_CLIENT_\w+)",
    re.IGNORECASE,
)
_PRIMARY_ROLE = "ROLE_CLIENT_PRIMARY"


def primary_link_from_status(status: str) -> str | None:
    """Return ``wifi`` or ``hyper`` from ``cmd wifi status`` role blocks."""
    for match in _ROLE_RE.finditer(status or ""):
        if match.group("role").upper() != _PRIMARY_ROLE:
            continue
        iface = match.group("iface").lower()
        return "hyper" if iface.startswith("hyper") or iface == "wlan1" else "wifi"
    return None


def primary_backup_entry(wifi_yaml: dict) -> DualWiFiEntry:
    traditional, _ = signal_level_entry(wifi_yaml, hyper=False)
    hyper, _ = signal_level_entry(wifi_yaml, hyper=True)
    if not traditional.get("ssid") or not hyper.get("ssid"):
        pytest.skip("wifi_ssid.yaml 缺少主备图标实验室网络配置")
    return cast(
        DualWiFiEntry,
        {"traditional_wifi": traditional, "hyper_wifi": hyper},
    )


def dual_link_legs(entry: DualWiFiEntry) -> tuple[WiFiEntry, WiFiEntry]:
    traditional = entry.get("traditional_wifi")
    hyper = entry.get("hyper_wifi")
    if not isinstance(traditional, dict) or not isinstance(hyper, dict):
        pytest.fail("主备网络配置必须同时包含 traditional_wifi 和 hyper_wifi")
    return traditional, hyper


def wait_for_link_ssid(
    wifi: WiFiControl,
    ssid: str,
    *,
    timeout: float = 35.0,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        found, _ = wifi.match_associated_ssids([ssid], use_dumpsys_for_missing=True)
        if found:
            return
        time.sleep(1.0)
    pytest.fail(f"连接 {ssid!r} 超时")


def connect_dual_link_in_order(
    summary: str,
    wifi: WiFiControl,
    entry: DualWiFiEntry,
    order: tuple[str, str],
) -> None:
    """Forget both legs, then associate them in the requested logical order."""
    if set(order) != {"wifi", "hyper"}:
        raise ValueError(f"双链路连接顺序无效: {order!r}")
    wifi.forget_dual_wifi_entry(entry)
    traditional, hyper = dual_link_legs(entry)
    legs = {"wifi": traditional, "hyper": hyper}
    for link in order:
        block = legs[link]
        ssid = str(block.get("ssid") or "")
        wifi.connect_wifi_block(block)
        wait_for_link_ssid(wifi, ssid)
        print(f"[{summary}] 已按顺序连接 {link}: {ssid!r}")
    ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=45.0)
    if not ok:
        pytest.fail(f"{summary}: 双链路连接失败 found={found!r} missing={missing!r}")


def wait_for_primary_link(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    expected: str,
    *,
    timeout: float = 45.0,
) -> str:
    """Wait until ``cmd wifi status`` reports the expected logical primary."""
    deadline = time.monotonic() + timeout
    last_status = ""
    while time.monotonic() < deadline:
        last_status = run_shell_cmd("cmd wifi status")
        if primary_link_from_status(last_status) == expected:
            allure.attach(last_status, "cmd wifi status - primary", allure.attachment_type.TEXT)
            return last_status
        time.sleep(1.0)
    pytest.fail(
        f"{summary}: 等待 {expected} 成为 primary 超时；"
        f"实际={primary_link_from_status(last_status)!r}\n{last_status[:1200]}"
    )


def tune_dual_link_rssi(
    run_shell_cmd: Callable[[str], str],
    attenuator: AttenuatorRig,
    channels: dict[str, int],
    entry: DualWiFiEntry,
    targets: Mapping[str, int],
    *,
    settle_sec: float,
    traditional_bssid: str = "",
    links: tuple[str, ...] = ("wifi", "hyper"),
) -> dict[str, tuple[float, int | None]]:
    traditional, _ = dual_link_legs(entry)
    raw_readers = {
        "wifi": _traditional_rssi_reader(
            run_shell_cmd,
            str(traditional.get("ssid") or ""),
            traditional_bssid,
        ),
        "hyper": _hyper_rssi_reader(run_shell_cmd),
    }
    results: dict[str, tuple[float, int | None]] = {}
    if not links or any(link not in raw_readers for link in links):
        raise ValueError(f"无效的双链路 RSSI 校准顺序: {links!r}")
    for link in links:
        def read_rssi() -> int | None:
            for _ in range(3):
                measured = raw_readers[link]()
                if measured is not None:
                    return measured
                time.sleep(1.0)
            return None

        attenuation, measured = tune_attenuation_for_rssi(
            attenuator,
            channels[link],
            targets[link],
            read_rssi,
            settle_sec=settle_sec,
            tolerance_db=2,
        )
        results[link] = (attenuation, measured)
        print(
            f"[DualLink] {link}: target={targets[link]} dBm, "
            f"measured={measured} dBm, attenuation={attenuation:g} dB"
        )
    return results
