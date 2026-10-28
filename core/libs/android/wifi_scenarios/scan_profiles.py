"""Shared WiFi scan-profile loading helpers."""
from __future__ import annotations

from typing import cast

import pytest

from core.libs.android.wifi_control.entries import WiFiEntry
from core.testdata_loader import get_ssid_pwd_entry


def scan_profile_entry(
    wifi_yaml: dict,
    profile_id: str,
    summary: str,
) -> WiFiEntry:
    profile = get_ssid_pwd_entry(wifi_yaml, entry_id=profile_id)
    if not profile:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 profile id={profile_id!r}")
    return cast(
        WiFiEntry,
        {
            **profile,
            "pwd": str(profile.get("password") or ""),
            "encrypt": str(profile.get("security") or "WPA2").upper(),
            "type": "normal",
            "expect": "connected",
        },
    )
