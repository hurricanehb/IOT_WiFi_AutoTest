"""Internal WiFi text parsing helpers used by WiFiControl."""
from __future__ import annotations

import re
from typing import List, Tuple

UNKNOWN_SSIDS = frozenset(
    ("", "<unknown ssid>", "unknown ssid", "null", "<none>", "0x", "unknown")
)
_SCAN_RESULT_RE = re.compile(
    r"^\s*(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\s+"
    r"\d+\s+\S+\s+\S+\s+(.*?)\s+((?:\[[^\]]*\])+?)\s*$",
    re.IGNORECASE,
)


def normalize_ssid(name: str) -> str:
    value = (name or "").strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
    if not value or value.lower() in UNKNOWN_SSIDS:
        return ""
    return value


def is_not_connected_status(status_text: str) -> bool:
    text = (status_text or "").lower()
    return bool(re.search(r"(?:wifi\s+is\s+)?not\s+connected", text) or "disconnected" in text)


def ssid_match(want: str, candidate: str) -> bool:
    expected = normalize_ssid(want)
    actual = normalize_ssid(candidate)
    return bool(expected and actual and expected == actual)


def scan_result_ssids(blob: str) -> List[str]:
    """Extract SSIDs from ``cmd wifi list-scan-results`` table rows."""
    out: List[str] = []
    for line in (blob or "").splitlines():
        match = _SCAN_RESULT_RE.match(line)
        if not match:
            continue
        ssid = normalize_ssid(match.group(1))
        if ssid and ssid not in out:
            out.append(ssid)
    return out


def parse_list_networks(blob: str) -> List[Tuple[str, str, bool]]:
    """Parse `cmd wifi list-networks` into (network_id, ssid, is_current)."""
    rows: List[Tuple[str, str, bool]] = []
    if not blob:
        return rows

    for raw in blob.splitlines():
        line = raw.strip()
        if not line or line.lower().startswith("network id") or "saved networks" in line.lower():
            continue
        lower = line.lower()
        is_current = "[current]" in lower or line.startswith("*")
        mq = re.search(r'"([^"]+)"', line)
        ssid = normalize_ssid(mq.group(1)) if mq else ""
        net_id = ""
        parts = line.split()
        if parts and parts[0] == "*":
            net_id = parts[1] if len(parts) > 1 else ""
            if not ssid and len(parts) >= 3:
                ssid = normalize_ssid(parts[2].strip('"'))
        elif parts and parts[0].isdigit():
            net_id = parts[0]
            if not ssid and len(parts) >= 2:
                ssid = normalize_ssid(parts[1].strip('"'))
        if ssid or net_id:
            rows.append((net_id, ssid, is_current))
    return rows


def ssid_from_wifi_status(text: str) -> str:
    if not text:
        return ""
    m = re.search(r'SSID:\s*"([^"]*)"', text, re.IGNORECASE)
    if m:
        return normalize_ssid(m.group(1))
    m2 = re.search(r"SSID:\s*(\S+)", text, re.IGNORECASE)
    if m2:
        return normalize_ssid(m2.group(1).strip(","))
    m3 = re.search(
        r'(?:connected|current)(?:\s+to)?\s+(?:ssid\s*)?[:\s]+"([^"]+)"',
        text,
        re.IGNORECASE,
    )
    if m3:
        return normalize_ssid(m3.group(1))
    return ""


def frequency_from_wifi_status(text: str) -> int:
    """Extract the associated WiFi frequency in MHz from ``cmd wifi status``."""
    if not text:
        return 0
    match = re.search(r"\bFrequency:\s*(\d+)\s*MHz\b", text, re.IGNORECASE)
    return int(match.group(1)) if match else 0


def bssid_from_wifi_status(text: str) -> str:
    """Extract the associated WiFi BSSID from ``cmd wifi status``."""
    if not text:
        return ""
    match = re.search(
        r"\bBSSID:\s*((?:[0-9a-f]{2}:){5}[0-9a-f]{2})\b",
        text,
        re.IGNORECASE,
    )
    return match.group(1).lower() if match else ""


def ssid_from_list_networks(blob: str) -> str:
    for _net_id, ssid, is_current in parse_list_networks(blob):
        if is_current and ssid:
            return ssid
    return ""


def ssid_from_dumpsys(blob: str) -> str:
    if not blob:
        return ""
    m = re.search(r'mWifiInfo.*?SSID:\s*"([^"]*)"', blob, re.DOTALL | re.IGNORECASE)
    if m:
        return normalize_ssid(m.group(1))
    m2 = re.search(r'SSID:\s*"([^"]+)"', blob)
    if m2:
        return normalize_ssid(m2.group(1))
    return ""


def status_ssids(text: str) -> List[str]:
    """Extract all valid SSIDs from `cmd wifi status` text."""
    out: List[str] = []
    if not text:
        return out
    for mq in re.finditer(r'SSID:\s*"([^"]+)"', text, re.IGNORECASE):
        value = normalize_ssid(mq.group(1))
        if value and value not in out:
            out.append(value)
    return out


def saved_network_ssids(blob: str) -> List[str]:
    """Extract saved SSIDs from `cmd wifi list-networks` output."""
    out: List[str] = []
    for _net_id, ssid, _is_current in parse_list_networks(blob):
        if ssid and ssid not in out:
            out.append(ssid)
    return out


def scan_result_capabilities(blob: str, ssid: str) -> List[str]:
    """Return capability strings for every scan row matching ``ssid``."""
    out: List[str] = []
    for line in (blob or "").splitlines():
        match = _SCAN_RESULT_RE.match(line)
        if not match or not ssid_match(ssid, match.group(1)):
            continue
        capabilities = match.group(2)
        if capabilities not in out:
            out.append(capabilities)
    return out


def scan_result_rssis(blob: str, ssid: str) -> List[int]:
    """Return RSSI values for every scan row matching ``ssid``."""
    out: List[int] = []
    for line in (blob or "").splitlines():
        match = _SCAN_RESULT_RE.match(line)
        if not match or not ssid_match(ssid, match.group(1)):
            continue
        prefix = line[: match.start(1)].split()
        if len(prefix) < 3:
            continue
        rssi_match = re.match(r"-?\d+", prefix[2])
        if rssi_match is None:
            continue
        out.append(int(rssi_match.group()))
    return out


def scan_result_rssi_for_bssid(blob: str, bssid: str) -> int | None:
    """Return RSSI for one exact BSSID from ``cmd wifi list-scan-results``."""
    wanted = (bssid or "").strip().lower()
    for line in (blob or "").splitlines():
        parts = line.split()
        if len(parts) < 3 or parts[0].lower() != wanted:
            continue
        rssi_match = re.match(r"-?\d+", parts[2])
        if rssi_match is not None:
            return int(rssi_match.group())
    return None