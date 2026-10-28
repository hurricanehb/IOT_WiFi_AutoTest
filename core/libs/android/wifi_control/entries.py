"""Shared types for Android WiFi test-data records."""
from __future__ import annotations

from typing import Dict, TypedDict


class WiFiEntry(TypedDict, total=False):
    id: str
    ssid: str
    pwd: str
    password: str
    password_env: str
    lab_flag: str
    encrypt: str
    security: str
    type: str
    expect: str
    region: str
    bssid: str
    bssids: Dict[str, str]


class DualWiFiEntry(TypedDict, total=False):
    id: str
    region: str
    traditional_wifi: WiFiEntry
    hyper_wifi: WiFiEntry