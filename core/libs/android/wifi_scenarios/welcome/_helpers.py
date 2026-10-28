"""Shared association waits for Android Welcome WLAN scenarios."""
from __future__ import annotations

import time


def _wait_for_wifi_connection(wifi, ssid: str, timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        matched_ssids, _ = wifi.match_associated_ssids(
            [ssid], use_dumpsys_for_missing=True
        )
        if matched_ssids:
            return True
        time.sleep(0.5)
    matched_ssids, _ = wifi.match_associated_ssids([ssid], use_dumpsys_for_missing=True)
    return bool(matched_ssids)


def _wait_for_wifi_disconnection(wifi, ssid: str, timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        matched_ssids, _ = wifi.match_associated_ssids(
            [ssid], use_dumpsys_for_missing=True
        )
        if not matched_ssids:
            return True
        time.sleep(0.5)
    matched_ssids, _ = wifi.match_associated_ssids([ssid], use_dumpsys_for_missing=True)
    return not matched_ssids
