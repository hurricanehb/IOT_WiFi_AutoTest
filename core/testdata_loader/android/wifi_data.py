"""WiFi test data helpers for testdata/android YAML files."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from core.utils.config_loader import android_data_path
from core.utils.data_parser import dump_yaml, load_yaml

WIFI_SSID_YAML = "wifi_ssid.yaml"
WEAKNET_SCENE_YAML = "weaknet_scene.yaml"


def wifi_ssid_yaml() -> Path:
    return android_data_path(WIFI_SSID_YAML)


def weaknet_scene_yaml() -> Path:
    return android_data_path(WEAKNET_SCENE_YAML)


def load_wifi_ssid() -> Dict[str, Any]:
    """Load full wifi_ssid yaml data."""
    data = load_yaml(wifi_ssid_yaml())
    return data if isinstance(data, dict) else {}


def save_wifi_ssid(data: Dict[str, Any]) -> None:
    """Overwrite wifi_ssid yaml data."""
    dump_yaml(wifi_ssid_yaml(), data)


def wifi_list_rows(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Return rows from wifi_list as dict items only."""
    d = data if data is not None else load_wifi_ssid()
    rows = d.get("wifi_list") or []
    return [r for r in rows if isinstance(r, dict)]


def get_wifi_list_entry(
    data: Optional[Dict[str, Any]] = None,
    *,
    entry_id: Optional[str] = None,
    index: Optional[int] = None,
    ssid: Optional[str] = None,
    expect: Optional[str] = None,
    wifi_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Return one wifi_list item by selector priority."""
    rows = wifi_list_rows(data)

    if entry_id:
        want_id = entry_id.strip()
        for row in rows:
            if (row.get("id") or "").strip() == want_id:
                return row
        return {}

    if ssid:
        want = ssid.strip()
        for row in rows:
            if (row.get("ssid") or "").strip() == want:
                if wifi_type and (row.get("type") or "").strip().lower() != wifi_type.strip().lower():
                    continue
                if expect and (row.get("expect") or "").strip().lower() != expect.strip().lower():
                    continue
                return row
        return {}

    if wifi_type:
        want_type = wifi_type.strip().lower()
        for row in rows:
            if (row.get("type") or "").strip().lower() == want_type:
                if expect and (row.get("expect") or "").strip().lower() != expect.strip().lower():
                    continue
                return row
        return {}

    if index is not None:
        if 0 <= index < len(rows):
            return rows[index]
        return {}

    if expect:
        want = expect.strip().lower()
        for row in rows:
            if (row.get("expect") or "").strip().lower() == want:
                return row
        return {}

    for row in rows:
        if (row.get("expect") or "connected").lower() == "connected":
            return row
    return rows[0] if rows else {}


def ssid_pwd_profile_rows(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Return SSID/password profiles with shared defaults applied."""
    d = data if data is not None else load_wifi_ssid()
    defaults = d.get("ssid_pwd_defaults") or {}
    if not isinstance(defaults, dict):
        defaults = {}

    profiles = d.get("ssid_pwd_profiles") or {}
    if isinstance(profiles, dict):
        return [
            {**defaults, **profile, "id": profile_id}
            for profile_id, profile in profiles.items()
            if isinstance(profile, dict)
        ]
    return []


def get_ssid_pwd_entry(
    data: Optional[Dict[str, Any]] = None,
    *,
    entry_id: Optional[str] = None,
    index: Optional[int] = None,
) -> Dict[str, Any]:
    """Return one SSID/password profile by id or index."""
    rows = ssid_pwd_profile_rows(data)

    if entry_id:
        want = entry_id.strip()
        for row in rows:
            if (row.get("id") or "").strip() == want:
                return row
        return {}

    if index is not None:
        if 0 <= index < len(rows):
            return rows[index]
        return {}

    return {}


def dual_wifi_list_rows(data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Return rows from dual_wifi_list as dict items only."""
    d = data if data is not None else load_wifi_ssid()
    rows = d.get("dual_wifi_list") or []
    return [r for r in rows if isinstance(r, dict)]


def get_dual_wifi_entry(
    data: Optional[Dict[str, Any]] = None,
    *,
    index: Optional[int] = None,
    entry_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Return one dual_wifi_list item by id/index."""
    rows = dual_wifi_list_rows(data)

    if entry_id:
        want = entry_id.strip()
        for row in rows:
            if (row.get("id") or "").strip() == want:
                return row
        return {}

    if index is not None:
        if 0 <= index < len(rows):
            return rows[index]
        return {}

    return rows[0] if rows else {}


def get_dual_wifi_entry_by_region(
    data: Optional[Dict[str, Any]] = None,
    *,
    region: str,
) -> Dict[str, Any]:
    """Return first dual_wifi entry matching hyper_wifi.region."""
    want = (region or "").strip().upper()
    if not want:
        return {}

    for row in dual_wifi_list_rows(data):
        hyper = row.get("hyper_wifi")
        if not isinstance(hyper, dict):
            continue
        if (hyper.get("region") or "").strip().upper() == want:
            return row
    return {}


def dual_wifi_ssids(entry: Mapping[str, Any]) -> List[str]:
    """Extract unique SSIDs from one dual_wifi entry."""
    names: List[str] = []
    for key in ("traditional_wifi", "hyper_wifi"):
        block = entry.get(key)
        if isinstance(block, dict):
            ssid = (block.get("ssid") or "").strip()
            if ssid and ssid not in names:
                names.append(ssid)
    return names


def get_expected_connected_ssids(data: Optional[Dict[str, Any]] = None) -> List[str]:
    """Return unique SSIDs expected to be connected."""
    d = data if data is not None else load_wifi_ssid()
    seen: List[str] = []

    for row in wifi_list_rows(d):
        if (row.get("expect") or "").strip().lower() != "connected":
            continue
        ssid = (row.get("ssid") or "").strip()
        if ssid and ssid not in seen:
            seen.append(ssid)

    for dual in dual_wifi_list_rows(d):
        for ssid in dual_wifi_ssids(dual):
            if ssid not in seen:
                seen.append(ssid)

    return seen
