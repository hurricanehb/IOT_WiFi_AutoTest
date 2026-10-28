"""RSSI reconnect-threshold scenarios driven by the laboratory attenuator."""
from __future__ import annotations

import time
from collections.abc import Callable, Mapping

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import (
    bssid_from_wifi_status,
    scan_result_rssi_for_bssid,
    scan_result_rssis,
    status_ssids,
)
from core.libs.android.wifi_scenarios.dual_link_failover import wait_for_link_bssid
from core.libs.android.wifi_scenarios.signal_level import (
    signal_level_entry,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status


def _target_is_connected(
    run_shell_cmd: Callable[[str], str], ssid: str
) -> bool:
    return ssid in status_ssids(run_shell_cmd("cmd wifi status"))


def _wait_for_ssid(
    run_shell_cmd: Callable[[str], str], ssid: str, *, timeout: float
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _target_is_connected(run_shell_cmd, ssid):
            return
        time.sleep(0.5)
    pytest.fail(f"WiFi did not reconnect to {ssid!r} within {timeout:g}s")


def _wait_for_stable_disconnection(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    ssid: str,
    *,
    timeout: float = 90.0,
    stable_samples: int = 5,
) -> None:
    deadline = time.monotonic() + timeout
    consecutive = 0
    last_status = ""
    while time.monotonic() < deadline:
        last_status = run_shell_cmd("cmd wifi status")
        if ssid in status_ssids(last_status):
            consecutive = 0
        else:
            consecutive += 1
            if consecutive >= stable_samples:
                return
        time.sleep(1.0)
    allure.attach(
        last_status or "<empty>",
        f"{summary}-maximum-attenuation-status.txt",
        allure.attachment_type.TEXT,
    )
    pytest.fail(
        f"{summary}: {ssid!r} did not remain disconnected at maximum "
        f"attenuation; current BSSID={bssid_from_wifi_status(last_status)!r}"
    )


def _scan_target_rssi(
    run_shell_cmd: Callable[[str], str],
    ssid: str,
    bssid: str,
) -> int | None:
    run_shell_cmd("cmd wifi start-scan")
    time.sleep(2.0)
    results = run_shell_cmd("cmd wifi list-scan-results")
    if bssid:
        return scan_result_rssi_for_bssid(results, bssid)
    values = scan_result_rssis(results, ssid)
    return max(values) if values else None


@allure.step("Verify WiFi reconnects only above the RSSI threshold")
def run_reconnect_rssi_threshold_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    hyper: bool,
    no_reconnect_rssi: int,
    reconnect_rssi: int,
    expected_band: str = "",
    no_reconnect_sec: float = 15.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    if reconnect_rssi != no_reconnect_rssi + 1:
        raise ValueError("reconnect RSSI must be exactly 1 dB above no-reconnect RSSI")

    entry, ap_index = signal_level_entry(wifi_yaml, hyper=hyper)
    ssid = str(entry.get("ssid") or "")
    if not ssid:
        pytest.skip(f"{summary}: signal-level WiFi profile is missing")
    target_bssid = ""
    if not hyper:
        bssids = entry.get("bssids")
        if not isinstance(bssids, Mapping):
            pytest.skip(f"{summary}: traditional WiFi profile has no band BSSIDs")
        target_bssid = str(bssids.get(expected_band) or "").lower()
        if not target_bssid:
            pytest.skip(f"{summary}: no BSSID configured for {expected_band}")

    channel = attenuator.channel_for(hyper=hyper, ap_index=ap_index)
    current = dict(attenuator.read_attenuations())
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]

    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        connect_entry = {**entry, **({"bssid": target_bssid} if target_bssid else {})}
        network_id = wifi.find_network_id_by_ssid(ssid)
        if network_id:
            wifi.forget_network(network_id)
        if not wifi.connect_wifi_block(connect_entry):
            pytest.fail(f"{summary}: failed to connect {ssid!r}")
        if hyper:
            _wait_for_ssid(run_shell_cmd, ssid, timeout=35.0)
        else:
            wait_for_link_bssid(summary, run_shell_cmd, "wlan0", target_bssid)

        attenuator.set_attenuation(channel, attenuator.max_attenuation_db)
        _wait_for_stable_disconnection(summary, run_shell_cmd, ssid)

        sweep_log: list[str] = []
        attenuation = float(attenuator.max_attenuation_db)
        confirmed_no_reconnect = False
        confirmed_no_reconnect_rssi: int | None = None
        first_reconnect_rssi: int | None = None
        fine_sweep = False
        target_seen = False
        while attenuation >= 0:
            attenuator.set_attenuation(channel, attenuation)
            time.sleep(2.0)
            scan_rssi = _scan_target_rssi(
                run_shell_cmd, ssid, target_bssid
            )
            if scan_rssi is None and target_seen:
                scan_rssi = _scan_target_rssi(
                    run_shell_cmd, ssid, target_bssid
                )
            connected = _target_is_connected(run_shell_cmd, ssid)
            sweep_log.append(
                f"attenuation={attenuation:g} dB, scan_rssi={scan_rssi}, "
                f"connected={connected}"
            )
            if scan_rssi is not None:
                target_seen = True
            if (
                scan_rssi is not None
                and scan_rssi >= no_reconnect_rssi - 10
            ):
                fine_sweep = True
            if connected:
                time.sleep(2.0)
                if _target_is_connected(run_shell_cmd, ssid):
                    if not hyper:
                        status = run_shell_cmd("cmd wifi status")
                        actual_bssid = bssid_from_wifi_status(status)
                        if actual_bssid != target_bssid:
                            pytest.fail(
                                f"{summary}: reconnected to wrong band/BSSID "
                                f"{actual_bssid!r}, expected {target_bssid!r}"
                            )
                    first_reconnect_rssi = scan_rssi
                    break
            if (
                scan_rssi is not None
                and abs(scan_rssi - no_reconnect_rssi) <= 1
                and not confirmed_no_reconnect
            ):
                time.sleep(no_reconnect_sec)
                if _target_is_connected(run_shell_cmd, ssid):
                    first_reconnect_rssi = _scan_target_rssi(
                        run_shell_cmd, ssid, target_bssid
                    )
                    sweep_log.append(
                        f"hold at attenuation={attenuation:g} dB, "
                        f"scan_rssi={first_reconnect_rssi}, connected=True"
                    )
                    break
                confirmed_no_reconnect = True
                confirmed_no_reconnect_rssi = scan_rssi
                sweep_log.append(
                    f"confirmed no reconnect at scan_rssi={scan_rssi}"
                )

            step = 1.0 if fine_sweep or (target_seen and scan_rssi is None) else 5.0
            attenuation -= step
        allure.attach(
            "\n".join(sweep_log),
            f"{summary}-reconnect-rssi-sweep.txt",
            allure.attachment_type.TEXT,
        )
        if first_reconnect_rssi is None:
            pytest.fail(f"{summary}: did not reconnect during the RSSI sweep")
        if not confirmed_no_reconnect:
            pytest.fail(
                f"{summary}: reconnected before confirming the no-reconnect "
                f"point {no_reconnect_rssi} dBm; first={first_reconnect_rssi!r}"
            )
        if abs(first_reconnect_rssi - reconnect_rssi) > 2:
            pytest.fail(
                f"{summary}: reconnected RSSI expected {reconnect_rssi}±2 dBm, "
                f"actual={first_reconnect_rssi!r}"
            )
        print(
            f"[{summary}] stable disconnect confirmed; no reconnect at "
            f"{confirmed_no_reconnect_rssi} dBm; first reconnect at "
            f"{first_reconnect_rssi} dBm"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")