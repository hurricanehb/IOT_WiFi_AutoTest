"""Traditional WiFi low-power and stress scenario runners."""
from __future__ import annotations

import os
import time
from typing import Callable

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.net_selection import (
    _read_scan_policy_log,
    assert_scan_backoff_sequence,
)
from core.libs.android.wifi_scenarios.signal_level import signal_level_entry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status


def _positive_int(name: str, default: int) -> int:
    value = int(os.getenv(name, str(default)))
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


@allure.step("Verify screen-on scan backoff with a saved-network precondition")
def run_screen_on_disconnected_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    keep_saved_network: bool,
    observation_sec: float = 170.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry, _ap_index = signal_level_entry(wifi_yaml, hyper=False)
    target_ssid = str(entry.get("ssid") or "")
    if not target_ssid:
        pytest.fail(f"{summary}: traditional WiFi profile has no SSID")

    try:
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to establish saved-network precondition")
        if not keep_saved_network:
            network_id = wifi.find_network_id_by_ssid(target_ssid)
            if network_id and not wifi.forget_network(network_id):
                pytest.fail(f"{summary}: failed to remove saved network")
        if not wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=2.0):
            pytest.fail(f"{summary}: failed to reach disconnected precondition")

        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        deadline = time.monotonic() + observation_sec
        policy_log = ""
        while time.monotonic() < deadline:
            policy_log = _read_scan_policy_log(wifi.adb)
            intervals = policy_log.count("schedulePeriodicScanTimer")
            if intervals >= 4:
                break
            time.sleep(1.0)
        assert_scan_backoff_sequence(
            policy_log,
            interface="wlan0",
            summary=summary,
            require_low_traffic=False,
        )
        allure.attach(
            policy_log or "<no scan policy log>",
            f"{summary}-screen-on-disconnected-scan.log",
            allure.attachment_type.TEXT,
        )
    finally:
        wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Run repeated screen sleep and wake cycles while WiFi remains connected")
def run_screen_cycle_stress_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    cycles: int | None = None,
    interval_sec: float = 1.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry, _ap_index = signal_level_entry(wifi_yaml, hyper=False)
    total_cycles = cycles or _positive_int("WIFILP_SCREEN_CYCLES", 1000)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect traditional WiFi")

    try:
        for cycle in range(1, total_cycles + 1):
            wifi.adb.keyevent("KEYCODE_SLEEP")
            time.sleep(interval_sec)
            wifi.adb.keyevent("KEYCODE_WAKEUP")
            wifi.adb.shell("wm", "dismiss-keyguard")
            if not wifi.match_associated_ssids([str(entry.get("ssid") or "")])[0]:
                pytest.fail(f"{summary}: WiFi disconnected during cycle {cycle}")
            if cycle % 100 == 0:
                print(f"[{summary}] completed screen cycle {cycle}/{total_cycles}")
    finally:
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Run repeated WiFi connection and disconnection cycles")
def run_connect_disconnect_stress_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    cycles: int | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry, _ap_index = signal_level_entry(wifi_yaml, hyper=False)
    total_cycles = cycles or _positive_int("WIFILP_CONNECT_CYCLES", 500)

    try:
        for cycle in range(1, total_cycles + 1):
            if not wifi.connect_wifi_block(entry):
                pytest.fail(f"{summary}: connection failed at cycle {cycle}")
            assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
            if not wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=1.0):
                pytest.fail(f"{summary}: disconnection failed at cycle {cycle}")
            if cycle % 50 == 0:
                print(f"[{summary}] completed connection cycle {cycle}/{total_cycles}")
    finally:
        wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=1.0)