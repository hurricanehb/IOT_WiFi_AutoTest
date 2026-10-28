"""Android WiFi control via ADB (cmd wifi / settings)."""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

from core.libs.android.wifi_control.cleanup import WiFiCleanup
from core.libs.android.wifi_control.connector import WiFiConnector
from core.libs.android.wifi_control.state import WiFiState
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger

log = get_logger(__name__)


class WiFiControl:
    """Control WiFi state and query status. Behavior varies by Android version."""

    def __init__(self, adb: Optional[AdbHelper] = None):
        self.adb = adb or AdbHelper()
        self._state = WiFiState(self.adb)
        self._cleanup = WiFiCleanup(
            self.adb,
            state=self._state,
            logger=log,
        )
        self._connector = WiFiConnector(
            self.adb,
            state=self._state,
            set_wifi_enabled=self.set_wifi_enabled,
            disconnect_all=self.disconnect_all,
            logger=log,
        )

    def _wifi_status_text(self) -> str:
        return self._state._wifi_status_text()

    def is_wifi_enabled(self) -> bool:
        return self._state.is_wifi_enabled()

    def _apply_wifi_toggle(self, on: bool) -> None:
        """Try known enable/disable command variants (vendor ROMs differ)."""
        word = "enable" if on else "disable"
        state = "enabled" if on else "disabled"
        attempts = [
            ("cmd", "wifi", "set-wifi-enabled", state),
            ("cmd", "wifi", "set-wifi-enabled", word),
            ("svc", "wifi", word),
            (
                "settings",
                "put",
                "global",
                "wifi_on",
                "1" if on else "0",
            ),
        ]
        for args in attempts:
            code, out, err = self.adb.shell(*args)
            if code == 0:
                log.debug("set_wifi_enabled ok via %s", " ".join(args))
                return
            log.debug("set_wifi_enabled miss %s: %s", " ".join(args), err or out)
        for line in (
            f"cmd wifi set-wifi-enabled {state}",
            f"cmd wifi set-wifi-enabled {word}",
            f"svc wifi {word}",
        ):
            code, out, err = self.adb.shell_line(line)
            if code == 0:
                log.debug("set_wifi_enabled ok via shell_line: %s", line)
                return
            log.debug("set_wifi_enabled miss shell_line %s: %s", line, err or out)

    def set_wifi_enabled(self, on: bool, settle_sec: float = 1.5) -> bool:
        """
        Enable/disable WiFi; always verifies radio state after trying fallbacks.

        Do not trust adb exit code alone — some builds return 0 without toggling.
        """
        if self.is_wifi_enabled() == on:
            return True
        self._apply_wifi_toggle(on)
        time.sleep(settle_sec)
        if self.is_wifi_enabled() == on:
            return True
        # Second pass after short delay (slow radios / policy services)
        self._apply_wifi_toggle(on)
        time.sleep(settle_sec)
        ok = self.is_wifi_enabled() == on
        if not ok:
            log.warning(
                "set_wifi_enabled(%s) 未生效，status=%r",
                on,
                self._wifi_status_text()[:300],
            )
        return ok

    def get_connected_ssid(self) -> str:
        return self._state.get_connected_ssid()

    def list_networks_blob(self) -> str:
        return self._state.list_networks_blob()

    def has_saved_networks(self) -> bool:
        return self._state.has_saved_networks()

    def find_network_id_by_ssid(self, ssid: str) -> str:
        return self._state.find_network_id_by_ssid(ssid)

    def list_connected_ssids(self, *, trust_status_fallback: bool = True) -> List[str]:
        return self._state.list_connected_ssids(
            trust_status_fallback=trust_status_fallback
        )

    def is_disconnected(self) -> bool:
        return self._state.is_disconnected()

    def wait_until_disconnected(
        self,
        timeout: float = 5.0,
        interval: float = 0.5,
    ) -> bool:
        return self._state.wait_until_disconnected(
            timeout=timeout,
            interval=interval,
        )

    def is_wifi_associated(self) -> bool:
        return self._state.is_wifi_associated()

    def match_associated_ssids(
        self,
        ssids: List[str],
        *,
        use_dumpsys_for_missing: bool = True,
    ) -> Tuple[List[str], List[str]]:
        return self._state.match_associated_ssids(
            ssids,
            use_dumpsys_for_missing=use_dumpsys_for_missing,
        )

    def list_current_networks(self) -> List[Tuple[str, str]]:
        return self._state.list_current_networks()

    def forget_targets_for_connected_ssids(
        self, connected_ssids: Optional[List[str]] = None
    ) -> List[Tuple[str, str]]:
        return self._cleanup.forget_targets_for_connected_ssids(connected_ssids)

    def disconnect_all(
        self,
        settle_sec: float = 2.0,
        max_rounds: int = 2,
        *,
        post_wait_sec: float = 5.0,
    ) -> bool:
        return self._cleanup.disconnect_all(
            settle_sec=settle_sec,
            max_rounds=max_rounds,
            post_wait_sec=post_wait_sec,
        )

    def list_saved_networks(self) -> List[str]:
        return self._state.list_saved_networks()

    def forget_network(self, network_id: str) -> bool:
        return self._cleanup.forget_network(network_id)

    def clear_saved_networks(
        self,
        *,
        max_rounds: int = 2,
        settle_sec: float = 0.5,
    ) -> List[Tuple[str, str]]:
        return self._cleanup.clear_saved_networks(
            max_rounds=max_rounds,
            settle_sec=settle_sec,
        )

    def open_wifi_settings(self) -> None:
        self._connector.open_wifi_settings()

    def connect_wpa2(self, ssid: str, password: str) -> bool:
        """Try `cmd wifi connect-network` (Android 10+). May fail on vendor builds."""
        return self._connector.connect_wpa2(ssid, password)

    def connect_wpa3(self, ssid: str, password: str) -> bool:
        """Try WPA3 variants; some builds use `wpa3`, others use `sae`."""
        return self._connector.connect_wpa3(ssid, password)

    def connect_open(self, ssid: str) -> bool:
        return self._connector.connect_open(ssid)

    def connect_wifi_block(self, block: WiFiEntry) -> bool:
        return self._connector.connect_wifi_block(block)

    def ensure_wifi_connected(
        self,
        entry: WiFiEntry,
        *,
        max_attempts: int = 3,
        settle_sec: float = 3.0,
    ) -> bool:
        return self._connector.ensure_wifi_connected(
            entry,
            max_attempts=max_attempts,
            settle_sec=settle_sec,
        )

    def last_connect_attempts(self) -> List[Dict[str, Any]]:
        return list(getattr(self._connector, "last_connect_attempts", []))

    def ensure_dual_wifi_connected(
        self,
        entry: DualWiFiEntry,
        *,
        timeout: float = 60.0,
        interval: float = 3.0,
        settle_after_connect: float = 5.0,
    ) -> Tuple[bool, List[str], List[str]]:
        return self._connector.ensure_dual_wifi_connected(
            entry,
            timeout=timeout,
            interval=interval,
            settle_after_connect=settle_after_connect,
        )

    def forget_dual_wifi_entry(self, entry: DualWiFiEntry) -> List[Tuple[str, str]]:
        return self._cleanup.forget_dual_wifi_entry(entry)

    def resolve_password(self, password_env: str) -> str:
        return WiFiConnector.resolve_password(password_env)
