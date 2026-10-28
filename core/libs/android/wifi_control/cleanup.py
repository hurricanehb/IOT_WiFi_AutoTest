"""WiFi cleanup/disconnect helper used by WiFiControl."""
from __future__ import annotations

import time
from typing import List, Tuple

from core.libs.android.wifi_control.state import WiFiState
from core.libs.android.wifi_control.entries import DualWiFiEntry
from core.utils.adb_helper import AdbHelper


class WiFiCleanup:
    """Handle disconnect/forget/cleanup workflows."""

    def __init__(
        self,
        adb: AdbHelper,
        *,
        state: WiFiState,
        logger,
    ):
        self.adb = adb
        self._state = state
        self._log = logger

    def forget_network(self, network_id: str) -> bool:
        net_id = (network_id or "").strip()
        if not net_id:
            return False
        code, out, err = self.adb.shell("cmd", "wifi", "forget-network", net_id)
        if code != 0:
            code, out, err = self.adb.shell_line(f"cmd wifi forget-network {net_id}")
        ok = code == 0
        if not ok:
            self._log.debug(
                "forget-network %s 返回 rc=%s: %s",
                net_id,
                code,
                (err or out or "").strip()[:120],
            )
        return ok

    def forget_targets_for_connected_ssids(
        self, connected_ssids: List[str] | None = None
    ) -> List[Tuple[str, str]]:
        ssids = (
            connected_ssids
            if connected_ssids is not None
            else self._state.list_connected_ssids()
        )
        targets: List[Tuple[str, str]] = []
        seen_ids: set[str] = set()
        for ssid in ssids:
            net_id = self._state.find_network_id_by_ssid(ssid)
            if net_id and net_id not in seen_ids:
                seen_ids.add(net_id)
                targets.append((net_id, ssid))
        return targets

    def _run_disconnect_fallback(self) -> None:
        for args in (("cmd", "wifi", "disconnect"),):
            self.adb.shell(*args)
        self.adb.shell_line("cmd wifi disconnect")

    def _disconnect_one_round(
        self,
        *,
        round_idx: int,
        rounds: int,
        settle_sec: float,
    ) -> bool:
        connected = self._state.list_connected_ssids()
        if not connected:
            self._log.debug("disconnect_all 完成（第 %d 轮前已无连接）", round_idx + 1)
            return True

        targets = self.forget_targets_for_connected_ssids(connected)
        if targets:
            self._log.debug(
                "disconnect_all 第 %d/%d 轮：forget-network %r",
                round_idx + 1,
                rounds,
                targets,
            )
            for net_id, _ssid in targets:
                self.forget_network(net_id)
                time.sleep(0.5)
        else:
            self._log.debug(
                "disconnect_all 第 %d/%d 轮：未匹配 network id，SSID=%r\n%s",
                round_idx + 1,
                rounds,
                connected,
                self._state.list_networks_blob()[:400],
            )

        self._run_disconnect_fallback()
        time.sleep(settle_sec)
        return self._state.is_disconnected()

    def disconnect_all(
        self,
        settle_sec: float = 2.0,
        max_rounds: int = 2,
        *,
        post_wait_sec: float = 5.0,
    ) -> bool:
        if not self._state.is_wifi_enabled():
            return True

        connected = self._state.list_connected_ssids()
        if not connected:
            self._log.debug("disconnect_all：无 WiFi 连接，退出")
            return True

        self._log.debug("disconnect_all 开始，已连接 SSID=%r", connected)
        rounds = max(1, min(max_rounds, 2))

        for round_idx in range(rounds):
            if self._disconnect_one_round(
                round_idx=round_idx,
                rounds=rounds,
                settle_sec=settle_sec,
            ):
                self._log.debug("disconnect_all 完成（第 %d 轮后）", round_idx + 1)
                return True

        if self._state.wait_until_disconnected(
            timeout=post_wait_sec,
            interval=0.5,
        ):
            self._log.debug("disconnect_all 完成（轮询 %ss 后已断开）", post_wait_sec)
            return True

        residual = self._state.list_connected_ssids()
        if residual and not self._state.has_saved_networks():
            self._log.debug(
                "disconnect_all：list-networks 已无保存网络，忽略 status 滞后 SSID=%r",
                residual,
            )
            return True

        if residual:
            self._log.warning(
                "disconnect_all 后仍有关联：SSID=%r list-networks:\n%s",
                residual,
                self._state.list_networks_blob()[:400],
            )
        return self._state.is_disconnected()

    def clear_saved_networks(
        self,
        *,
        max_rounds: int = 2,
        settle_sec: float = 0.5,
    ) -> List[Tuple[str, str]]:
        forgotten: List[Tuple[str, str]] = []
        seen_ids: set[str] = set()
        rounds = max(1, min(max_rounds, 3))

        for _ in range(rounds):
            rows = self._state.list_network_rows()
            targets: List[Tuple[str, str]] = []
            for net_id, ssid, _is_current in rows:
                if net_id and net_id not in seen_ids:
                    targets.append((net_id, ssid))

            if not targets:
                break

            for net_id, ssid in targets:
                if self.forget_network(net_id):
                    forgotten.append((net_id, ssid))
                seen_ids.add(net_id)
                time.sleep(settle_sec)

        return forgotten

    def forget_dual_wifi_entry(self, entry: DualWiFiEntry) -> List[Tuple[str, str]]:
        forgotten: List[Tuple[str, str]] = []
        seen_ids: set[str] = set()
        for key in ("traditional_wifi", "hyper_wifi"):
            block = entry.get(key)
            if not isinstance(block, dict):
                continue
            ssid = (block.get("ssid") or "").strip()
            if not ssid:
                continue
            net_id = self._state.find_network_id_by_ssid(ssid)
            if net_id and net_id not in seen_ids:
                if self.forget_network(net_id):
                    forgotten.append((net_id, ssid))
                seen_ids.add(net_id)
        return forgotten
