"""WiFi connect/orchestration helper used by WiFiControl."""
from __future__ import annotations

import os
import time
from typing import Any, Callable, Dict, List, Tuple

from core.libs.android.wifi_control.ssid_parsers import ssid_match
from core.libs.android.wifi_control.state import WiFiState
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.utils.adb_helper import AdbHelper
from core.utils.config_loader import get_settings


class WiFiConnector:
    """Handle connect-network and dual-wifi orchestration."""

    def __init__(
        self,
        adb: AdbHelper,
        *,
        state: WiFiState,
        set_wifi_enabled: Callable[[bool], bool],
        disconnect_all: Callable[..., bool],
        logger,
    ):
        self.adb = adb
        self._state = state
        self._set_wifi_enabled = set_wifi_enabled
        self._disconnect_all = disconnect_all
        self._log = logger
        self.last_connect_attempts: List[Dict[str, Any]] = []

    def open_wifi_settings(self) -> None:
        self.adb.shell(
            "am",
            "start",
            "-a",
            "android.settings.WIFI_SETTINGS",
        )
        time.sleep(1.0)

    def _connect_network(
        self,
        ssid: str,
        security: str,
        credential: str,
        *,
        bssid: str = "",
    ) -> bool:
        command = [
            "cmd",
            "wifi",
            "connect-network",
            ssid,
            security,
        ]
        if credential:
            command.append(credential)
        if bssid:
            command.extend(["-b", bssid, "-r", "none"])
        code, out, err = self.adb.shell(*command)
        attempt = {
            "ssid": ssid,
            "security": security,
            "code": code,
            "out": (out or "").strip(),
            "err": (err or "").strip(),
        }
        self.last_connect_attempts.append(attempt)
        self.last_connect_attempts = self.last_connect_attempts[-5:]
        if code == 0:
            wait_sec = self._connect_wait_sec()
            deadline = time.monotonic() + wait_sec
            cur = ""
            while time.monotonic() <= deadline:
                cur = self._state.get_connected_ssid()
                found, _ = self._state.match_associated_ssids(
                    [ssid], use_dumpsys_for_missing=True
                )
                if ssid_match(ssid, cur) or found:
                    attempt["connected"] = cur or found[0]
                    return True
                time.sleep(1.0)
            attempt["connected"] = cur
            attempt["wait_sec"] = wait_sec
            return False
        self._log.debug("connect-network %s: %s %s", security, out, err)
        return False

    @staticmethod
    def _connect_wait_sec() -> float:
        return get_settings().scenario_tuning.wifi_connect_wait_sec

    def connect_wpa2(self, ssid: str, password: str, *, bssid: str = "") -> bool:
        return self._connect_network(ssid, "wpa2", password, bssid=bssid)

    def connect_wep(self, ssid: str, password: str, *, bssid: str = "") -> bool:
        return self._connect_network(ssid, "wep", password, bssid=bssid)

    def connect_owe(self, ssid: str, *, bssid: str = "") -> bool:
        return self._connect_network(ssid, "owe", "", bssid=bssid)

    def connect_wpa3(self, ssid: str, password: str, *, bssid: str = "") -> bool:
        if self._connect_network(ssid, "wpa3", password, bssid=bssid):
            return True
        if self.last_connect_attempts and self.last_connect_attempts[-1].get("code") == 0:
            return False
        return self._connect_network(ssid, "sae", password, bssid=bssid)

    def connect_open(self, ssid: str, *, bssid: str = "") -> bool:
        ok = self._connect_network(ssid, "open", "open", bssid=bssid)
        if ok:
            return True
        cur = self._state.get_connected_ssid()
        return ssid_match(ssid, cur)

    def connect_wifi_block(self, block: WiFiEntry) -> bool:
        ssid = str(block.get("ssid") or "")
        if ssid == "":
            return False
        bssid = str(block.get("bssid") or "").strip()
        encrypt = (block.get("encrypt") or "WPA2").strip().upper()
        if encrypt == "OPEN":
            return self.connect_open(ssid, bssid=bssid)
        if encrypt == "OWE":
            return self.connect_owe(ssid, bssid=bssid)
        pwd = str(block.get("pwd") or "")
        if pwd == "":
            pwd = self.resolve_password(block.get("password_env") or "")
        if pwd == "":
            self._log.warning("connect_wifi_block: 缺少密码 ssid=%r", ssid)
            return False
        if encrypt == "WEP":
            return self.connect_wep(ssid, pwd, bssid=bssid)
        if encrypt in ("WPA3", "SAE", "WPA3-SAE"):
            return self.connect_wpa3(ssid, pwd, bssid=bssid)
        return self.connect_wpa2(ssid, pwd, bssid=bssid)

    def ensure_wifi_connected(
        self,
        entry: WiFiEntry,
        *,
        max_attempts: int = 3,
        settle_sec: float = 3.0,
    ) -> bool:
        """Disconnect an unrelated network, then retry the target association."""
        target = str(entry.get("ssid") or "")
        if not target:
            return False
        found, _ = self._state.match_associated_ssids(
            [target], use_dumpsys_for_missing=True
        )
        if found:
            self._log.info("WiFi 已关联目标 SSID=%r，跳过 connect-network", target)
            return True

        connected = self._state.list_connected_ssids(trust_status_fallback=True)
        if connected and not any(ssid_match(target, ssid) for ssid in connected):
            self._log.info("未关联目标 %r，当前 %r，先断开再连接", target, connected)
            self._disconnect_all(
                settle_sec=1.5,
                max_rounds=2,
                post_wait_sec=2.0,
            )
            time.sleep(1.0)

        for attempt in range(1, max_attempts + 1):
            self._log.info(
                "连接目标 WiFi %r（第 %d/%d 次）", target, attempt, max_attempts
            )
            self.connect_wifi_block(entry)
            time.sleep(settle_sec)
            found, _ = self._state.match_associated_ssids(
                [target], use_dumpsys_for_missing=True
            )
            if found:
                return True
        return False

    @staticmethod
    def _dual_targets(
        trad: WiFiEntry,
        hyper: WiFiEntry,
    ) -> List[str]:
        targets: List[str] = []
        for block in (trad, hyper):
            ssid = (block.get("ssid") or "").strip()
            if ssid and ssid not in targets:
                targets.append(ssid)
        return targets

    def _connect_missing_dual_leg(
        self,
        *,
        block: WiFiEntry,
        missing: List[str],
        label: str,
        settle_after_connect: float,
        deadline: float,
    ) -> bool:
        """返回是否仍在超时窗口内；已超时则不再发起连接。"""
        if time.monotonic() >= deadline:
            return False
        leg_ssid = (block.get("ssid") or "").strip()
        if leg_ssid and any(ssid_match(leg_ssid, m) for m in missing):
            self._log.info("ensure_dual_wifi: 连接%s %r", label, leg_ssid)
            self.connect_wifi_block(block)
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(settle_after_connect, remaining))
        return True

    def ensure_dual_wifi_connected(
        self,
        entry: DualWiFiEntry,
        *,
        timeout: float = 60.0,
        interval: float = 3.0,
        settle_after_connect: float = 5.0,
    ) -> Tuple[bool, List[str], List[str]]:
        trad = entry.get("traditional_wifi")
        hyper = entry.get("hyper_wifi")
        if not isinstance(trad, dict) or not isinstance(hyper, dict):
            return False, [], []

        targets = self._dual_targets(trad, hyper)
        if len(targets) < 2:
            return False, [], targets

        deadline = time.monotonic() + max(10.0, timeout)
        if not self._set_wifi_enabled(True):
            return False, [], targets
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(1.0, remaining))

        found, missing = self._state.match_associated_ssids(
            targets, use_dumpsys_for_missing=False
        )
        if not missing:
            return True, found, []

        within_deadline = self._connect_missing_dual_leg(
            block=trad,
            missing=missing,
            label="传统 WiFi",
            settle_after_connect=settle_after_connect,
            deadline=deadline,
        )

        found, missing = self._state.match_associated_ssids(
            targets, use_dumpsys_for_missing=False
        )
        if not missing:
            return True, found, []
        if not within_deadline:
            return False, found, missing

        if not self._connect_missing_dual_leg(
            block=hyper,
            missing=missing,
            label="HyperWiFi",
            settle_after_connect=settle_after_connect,
            deadline=deadline,
        ):
            return False, found, missing

        while time.monotonic() < deadline:
            found, missing = self._state.match_associated_ssids(
                targets, use_dumpsys_for_missing=False
            )
            if not missing:
                self._log.info("ensure_dual_wifi: 双路已连接 %r", found)
                return True, found, []
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(interval, remaining))

        return False, found, missing

    @staticmethod
    def resolve_password(password_env: str) -> str:
        if not password_env:
            return ""
        return os.environ.get(password_env, "").strip()
