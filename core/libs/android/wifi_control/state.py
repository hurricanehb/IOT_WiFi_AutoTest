"""WiFi state/query helper used by WiFiControl."""
from __future__ import annotations

import re
import time
from typing import List, Tuple

from core.libs.android.wifi_control.ssid_parsers import (
    is_not_connected_status,
    parse_list_networks,
    saved_network_ssids,
    ssid_from_dumpsys,
    ssid_from_list_networks,
    ssid_from_wifi_status,
    ssid_match,
    status_ssids,
)
from core.utils.adb_helper import AdbHelper


class WiFiState:
    """Read/query WiFi state and SSID association status."""

    def __init__(
        self,
        adb: AdbHelper,
    ):
        self.adb = adb

    def _wifi_status_text(self) -> str:
        code, out, err = self.adb.shell("cmd", "wifi", "status")
        if code == 0 and (out or err):
            return (out + "\n" + err).strip()
        fallback_code, fallback_out, fallback_err = self.adb.shell_line(
            "cmd wifi status"
        )
        if fallback_code != 0:
            return ""
        return (fallback_out + "\n" + fallback_err).strip()

    def _ssid_from_wifi_status(self) -> str:
        code, out, err = self.adb.shell("cmd", "wifi", "status")
        text = ((out or "") + "\n" + (err or "")).strip()
        if code != 0 or not text:
            return ""
        return ssid_from_wifi_status(text)

    def _ssid_from_list_networks(self) -> str:
        blob = self.list_networks_blob()
        if not blob:
            return ""
        return ssid_from_list_networks(blob)

    def _ssid_from_dumpsys_wifi(self) -> str:
        code, out, err = self.adb.shell("dumpsys", "wifi")
        text = (out or "") + (err or "")
        if code != 0 or not text.strip():
            return ""
        return ssid_from_dumpsys(text)

    def get_connected_ssid(self) -> str:
        ssids = self.list_connected_ssids()
        if ssids:
            return ssids[0]
        for fn in (
            self._ssid_from_wifi_status,
            self._ssid_from_list_networks,
            self._ssid_from_dumpsys_wifi,
        ):
            value = fn()
            if value:
                return value
        return ""

    def _parse_list_networks(self) -> List[Tuple[str, str, bool]]:
        _, rows = self._list_network_blob_and_rows()
        return rows

    def list_network_rows(self) -> List[Tuple[str, str, bool]]:
        return self._parse_list_networks()

    def list_networks_blob(self) -> str:
        _, out, err = self.adb.shell("cmd", "wifi", "list-networks")
        return ((out or "") + "\n" + (err or "")).strip()

    def is_wifi_enabled(self) -> bool:
        text = self._wifi_status_text().lower()
        if text:
            if re.search(r"\bdisabled\b", text) or "wifi is disabled" in text:
                return False
            if re.search(r"\benabled\b", text) or "wifi is enabled" in text:
                return True
            if re.search(r"wifi\s*state[:\s]+(enabled|on|1)\b", text):
                return True
            if re.search(r"wifi\s*state[:\s]+(disabled|off|0)\b", text):
                return False
        code, out, _ = self.adb.shell("settings", "get", "global", "wifi_on")
        if code == 0:
            value = out.strip().lower()
            if value in ("1", "true"):
                return True
            if value in ("0", "false"):
                return False
        return False

    def _list_network_blob_and_rows(self) -> Tuple[str, List[Tuple[str, str, bool]]]:
        blob = self.list_networks_blob()
        if not blob:
            return "", []
        return blob, parse_list_networks(blob)

    @staticmethod
    def _current_ssids_from_rows(rows: List[Tuple[str, str, bool]]) -> List[str]:
        seen: List[str] = []
        for _, ssid, is_current in rows:
            if is_current and ssid and ssid not in seen:
                seen.append(ssid)
        return seen

    def has_saved_networks(self) -> bool:
        blob, rows = self._list_network_blob_and_rows()
        if not blob or "no networks" in blob.lower():
            return False
        return bool(rows)

    def find_network_id_by_ssid(self, ssid: str) -> str:
        want = (ssid or "").strip()
        if not want:
            return ""
        for net_id, row_ssid, _ in self._parse_list_networks():
            if net_id and ssid_match(want, row_ssid):
                return net_id
        return ""

    def list_connected_ssids(self, *, trust_status_fallback: bool = True) -> List[str]:
        _, rows = self._list_network_blob_and_rows()
        seen = self._current_ssids_from_rows(rows)
        if seen:
            return seen

        status_text = self._wifi_status_text()
        status_lower = status_text.lower()

        if trust_status_fallback:
            for value in status_ssids(status_text):
                if value and value not in seen:
                    seen.append(value)
            if seen:
                return seen

        if not rows:
            if is_not_connected_status(status_lower):
                return []
            return []

        if is_not_connected_status(status_lower):
            return []

        if not trust_status_fallback:
            return []

        if not seen:
            one = self._ssid_from_dumpsys_wifi()
            if one:
                seen.append(one)
        return seen

    def is_disconnected(self) -> bool:
        if not self.is_wifi_enabled():
            return True
        if not self.has_saved_networks():
            return True
        if self.list_connected_ssids(trust_status_fallback=False):
            return False
        text = self._wifi_status_text().lower()
        if is_not_connected_status(text):
            return True
        return not self.list_connected_ssids()

    def wait_until_disconnected(
        self,
        timeout: float = 5.0,
        interval: float = 0.5,
    ) -> bool:
        deadline = time.time() + max(0.5, timeout)
        while time.time() < deadline:
            if self.is_disconnected():
                return True
            time.sleep(interval)
        return self.is_disconnected()

    def is_wifi_associated(self) -> bool:
        return not self.is_disconnected() and bool(self.list_connected_ssids())

    def match_associated_ssids(
        self,
        ssids: List[str],
        *,
        use_dumpsys_for_missing: bool = True,
    ) -> Tuple[List[str], List[str]]:
        wants = [(s or "").strip() for s in ssids if (s or "").strip()]
        if not wants:
            return [], []

        found: List[str] = []

        def _mark_from_sources(sources: List[str]) -> None:
            for want in wants:
                if want in found:
                    continue
                if any(ssid_match(want, cand) for cand in sources):
                    found.append(want)

        strict = self.list_connected_ssids(trust_status_fallback=False)
        _mark_from_sources(strict)
        missing = [w for w in wants if w not in found]
        if not missing:
            return found, []

        loose = self.list_connected_ssids(trust_status_fallback=True)
        _mark_from_sources(loose)
        missing = [w for w in wants if w not in found]
        if not missing or not use_dumpsys_for_missing:
            return found, missing

        text_lower = self._wifi_status_text().lower()
        if is_not_connected_status(text_lower):
            return found, missing

        code, out, err = self.adb.shell("dumpsys", "wifi")
        blob = (out or "") + "\n" + (err or "")
        if code != 0 or not blob.strip():
            return found, missing

        for want in missing[:]:
            pat = rf'SSID:\s*"{re.escape(want)}"'
            if re.search(pat, blob, re.IGNORECASE):
                found.append(want)
        missing = [w for w in wants if w not in found]
        return found, missing

    def list_current_networks(self) -> List[Tuple[str, str]]:
        rows: List[Tuple[str, str]] = []
        for net_id, ssid, is_current in self._parse_list_networks():
            if is_current and net_id:
                rows.append((net_id, ssid))
        return rows

    def list_saved_networks(self) -> List[str]:
        blob = self.list_networks_blob()
        if not blob:
            return []
        return saved_network_ssids(blob)
