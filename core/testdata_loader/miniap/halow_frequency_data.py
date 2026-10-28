"""Halow 频点/信道对照表（testdata/miniap/halow_frequency_tables.yaml）。"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from core.utils.config_loader import miniap_data_path
from core.utils.data_parser import load_yaml

HALOW_FREQUENCY_YAML = "halow_frequency_tables.yaml"


def halow_frequency_yaml() -> Path:
    return miniap_data_path(HALOW_FREQUENCY_YAML)


def load_halow_frequency_tables() -> Dict[str, Any]:
    data = load_yaml(halow_frequency_yaml())
    return data if isinstance(data, dict) else {}


def country_code(region: str, *, tables: Optional[Dict[str, Any]] = None) -> str:
    """Return legacy hex id from country_codes (US / EU / EUs)."""
    data = tables if tables is not None else load_halow_frequency_tables()
    codes = data.get("country_codes") or {}
    key = (region or "").strip()
    return str(codes.get(key) or "")


def special_id(region: str, *, tables: Optional[Dict[str, Any]] = None) -> str:
    """Return miniAP dwrite SPECIAL_ID for US / EU."""
    data = tables if tables is not None else load_halow_frequency_tables()
    codes = data.get("country_codes") or {}
    key = (region or "").strip().upper()
    if key == "EU":
        return str(codes.get("EUs") or codes.get("EU") or "")
    return str(codes.get(key) or "")


def channels_from_frequency_map(freq_map: Any) -> List[int]:
    """Extract sorted unique channel numbers from {frequency: channel} map."""
    if not isinstance(freq_map, dict):
        return []
    out: List[int] = []
    for ch in freq_map.values():
        try:
            out.append(int(ch))
        except (TypeError, ValueError):
            continue
    return sorted(set(out))


def us_channels(bandwidth_mhz: int, *, tables: Optional[Dict[str, Any]] = None) -> List[int]:
    data = tables if tables is not None else load_halow_frequency_tables()
    us = data.get("US") or {}
    key = f"bandwidth_{bandwidth_mhz}mhz"
    return channels_from_frequency_map(us.get(key))


def eu_channels(band: str, *, tables: Optional[Dict[str, Any]] = None) -> List[int]:
    data = tables if tables is not None else load_halow_frequency_tables()
    eu = data.get("EU") or {}
    band_key = (band or "").lower()
    if "800" in band_key:
        return channels_from_frequency_map(eu.get("band_800mhz_1mhz"))
    if "900" in band_key:
        return channels_from_frequency_map(eu.get("band_900mhz_1mhz"))
    return channels_from_frequency_map(eu.get("full"))
