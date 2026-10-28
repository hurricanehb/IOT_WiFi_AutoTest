"""Network-selection scan scenarios and log assertions."""
from __future__ import annotations

import re
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import List, Mapping, cast

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.access_points.miniap import MiniAPAction
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_scenarios.signal_level import signal_level_entry
from core.libs.android.wifi_scenarios.signal_level import tune_attenuation_for_rssi
from core.libs.android.wifi_scenarios.signal_level import _hyper_rssi_reader
from core.libs.android.wifi_scenarios.signal_level import _traditional_rssi_reader
from core.libs.android.wifi_scenarios.dual_link_failover import (
    link_radio_metrics,
    wait_for_link_bssid,
)
from core.libs.android.wifi_scenarios.dual_link import (
    dual_link_legs,
    primary_backup_entry,
    tune_dual_link_rssi,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_control.ssid_parsers import (
    parse_list_networks,
    scan_result_rssis,
)
from core.libs.android.logcat_parsers import parse_logcat_event_offsets
from core.testdata_loader.android.wifi_data import get_wifi_list_entry
from core.utils.adb_helper import AdbHelper


_NETWORK_SELECTION_SCAN_MARKERS = (
    "allsinglescanlistener onresults",
    "start network selection",
)
_PNO_SCAN_MARKER = "pno scan started"
_CANDIDATE_SCORE_RE = re.compile(
    r'Score for candidate:\s+SSID:\s+"(?P<ssid>[^"\r\n]+)"'
    r'.*?rssiScore:\s*(?P<rssi_score>-?\d+)'
    r'.*?rssi:\s*(?P<rssi>-?\d+)\s+final score:\s*(?P<final_score>-?\d+)',
    re.IGNORECASE,
)
_RECENT_SELECTION_SKIP_RE = re.compile(
    r"(?P<interface>wlan\d+):\s*Too short since last network selection:\s*"
    r"(?P<elapsed_ms>\d+)\s*ms\.\s*Skip network selection",
    re.IGNORECASE,
)


def parse_network_selection_scan_events(log_text: str) -> List[str]:
    """Return one entry for each completed scan entering network selection."""
    events: List[str] = []
    for line in (log_text or "").splitlines():
        lower = line.lower()
        if all(marker in lower for marker in _NETWORK_SELECTION_SCAN_MARKERS):
            events.append(line.strip())
    return events


def parse_network_selection_scan_cycles(
    log_text: str,
    *,
    cluster_window_sec: float = 2.0,
) -> List[float]:
    """Group callbacks from multiple radio interfaces into logical scans."""
    offsets = parse_logcat_event_offsets(
        log_text,
        ("allsinglescanlistener onresults: start network selection",),
    )
    cycles: List[float] = []
    for offset in offsets:
        if not cycles or offset - cycles[-1] > cluster_window_sec:
            cycles.append(offset)
    return cycles


def parse_interface_scan_offsets(log_text: str, interface: str) -> List[float]:
    """Return scan-start offsets for one physical WiFi interface."""
    return parse_logcat_event_offsets(
        log_text,
        (f"startsinglescan on real: {interface.lower()}",),
    )


def parse_pno_scan_events(log_text: str) -> List[str]:
    """Return firmware PNO scan-start events."""
    return [
        line.strip()
        for line in (log_text or "").splitlines()
        if _PNO_SCAN_MARKER in line.lower()
    ]


def parse_active_default_route(route_text: str) -> tuple[str, str] | None:
    for match in re.finditer(
        r"^default\s+via\s+(\d+(?:\.\d+){3})\s+dev\s+(\S+)",
        route_text or "",
        flags=re.MULTILINE,
    ):
        gateway, interface = match.groups()
        if not interface.startswith("dummy"):
            return gateway, interface
    return None


def parse_candidate_scores(log_text: str) -> dict[str, tuple[int, int, int]]:
    scores: dict[str, tuple[int, int, int]] = {}
    for line in (log_text or "").splitlines():
        match = _CANDIDATE_SCORE_RE.search(line)
        if match is not None:
            scores[match.group("ssid")] = (
                int(match.group("rssi_score")),
                int(match.group("rssi")),
                int(match.group("final_score")),
            )
    return scores


def parse_recent_selection_skips(log_text: str) -> list[tuple[str, int]]:
    return [
        (match.group("interface").lower(), int(match.group("elapsed_ms")))
        for match in _RECENT_SELECTION_SKIP_RE.finditer(log_text or "")
    ]


def assert_recent_network_selection_skipped(
    log_text: str,
    *,
    interface: str,
    summary: str,
    maximum_elapsed_ms: int = 10_000,
) -> None:
    matching = [
        elapsed_ms
        for logged_interface, elapsed_ms in parse_recent_selection_skips(log_text)
        if logged_interface == interface.lower()
    ]
    if not matching:
        pytest.fail(f"{summary}: missing recent-selection skip log for {interface}")
    if min(matching) >= maximum_elapsed_ms:
        pytest.fail(
            f"{summary}: recent-selection skip elapsed={min(matching)} ms, "
            f"expected <{maximum_elapsed_ms} ms"
        )


def assert_candidate_score_selection(
    log_text: str,
    *,
    stronger_ssid: str,
    weaker_ssid: str,
    summary: str,
    expected_rssi_scores: tuple[int, int] | None = None,
    require_equal_final_scores: bool = False,
) -> None:
    scores = parse_candidate_scores(log_text)
    missing = [ssid for ssid in (stronger_ssid, weaker_ssid) if ssid not in scores]
    if missing:
        pytest.fail(f"{summary}: missing candidate score logs for {missing!r}")
    stronger = scores[stronger_ssid]
    weaker = scores[weaker_ssid]
    if expected_rssi_scores is not None:
        actual_rssi_scores = (stronger[0], weaker[0])
        if actual_rssi_scores != expected_rssi_scores:
            pytest.fail(
                f"{summary}: RSSI scores were {actual_rssi_scores!r}, "
                f"expected {expected_rssi_scores!r}"
            )
    if require_equal_final_scores and stronger[2] != weaker[2]:
        pytest.fail(
            f"{summary}: final scores differ: "
            f"{stronger_ssid!r}={stronger[2]}, {weaker_ssid!r}={weaker[2]}"
        )
    if stronger[1] <= weaker[1]:
        pytest.fail(
            f"{summary}: expected {stronger_ssid!r} RSSI to be stronger; "
            f"actual={stronger[1]} dBm vs {weaker[1]} dBm"
        )
    candidate_marker = f'turbolink candidate: "{stronger_ssid}"'.lower()
    if candidate_marker not in (log_text or "").lower():
        pytest.fail(f"{summary}: stronger SSID was not selected as turbolink candidate")


def assert_equal_score_prefers_stronger_candidate(
    log_text: str,
    *,
    stronger_ssid: str,
    weaker_ssid: str,
    summary: str,
) -> None:
    assert_candidate_score_selection(
        log_text,
        stronger_ssid=stronger_ssid,
        weaker_ssid=weaker_ssid,
        summary=summary,
        require_equal_final_scores=True,
    )


def assert_no_pno_scan(log_text: str, *, summary: str) -> None:
    events = parse_pno_scan_events(log_text)
    if events:
        pytest.fail(f"{summary}: unexpectedly started {len(events)} PNO scan(s)")


def assert_pno_scan_started(log_text: str, *, summary: str) -> None:
    if not parse_pno_scan_events(log_text):
        pytest.fail(f"{summary}: PNO scan did not start")


def assert_no_interface_scan(
    log_text: str,
    *,
    interface: str,
    summary: str,
) -> None:
    scans = parse_interface_scan_offsets(log_text, interface)
    if scans:
        pytest.fail(
            f"{summary}: {interface} unexpectedly started {len(scans)} scan(s)"
        )


def assert_interface_scan_started(
    log_text: str,
    *,
    interface: str,
    summary: str,
) -> None:
    if not parse_interface_scan_offsets(log_text, interface):
        pytest.fail(f"{summary}: {interface} did not start a scan")


def assert_periodic_scan_interval(
    log_text: str,
    *,
    interface: str,
    summary: str,
    expected_interval_sec: float,
    tolerance_sec: float = 2.0,
    minimum_scans: int = 2,
) -> None:
    scans = parse_interface_scan_offsets(log_text, interface)
    if len(scans) < minimum_scans:
        pytest.fail(
            f"{summary}: {interface} produced {len(scans)} scan(s), "
            f"expected at least {minimum_scans}"
        )
    intervals = [later - earlier for earlier, later in zip(scans, scans[1:])]
    invalid = [
        interval
        for interval in intervals
        if abs(interval - expected_interval_sec) > tolerance_sec
    ]
    if invalid:
        pytest.fail(
            f"{summary}: {interface} scan intervals were {intervals!r}s, "
            f"expected {expected_interval_sec:.1f}±{tolerance_sec:.1f}s"
        )


def assert_network_selection_skipped_for_sufficient_link(
    log_text: str,
    *,
    interface: str,
    summary: str,
) -> None:
    lower = (log_text or "").lower()
    expected = f"{interface.lower()}: current connected network already sufficient"
    if expected not in lower or "skip network selection" not in lower:
        pytest.fail(f"{summary}: missing sufficient-link nomination skip log")


def assert_active_stream_policy(log_text: str, *, summary: str) -> None:
    if not re.search(r"hasActiveStream\s*:\s*true", log_text or "", re.IGNORECASE):
        pytest.fail(f"{summary}: missing hasActiveStream:true policy log")


def assert_low_traffic_policy(log_text: str, *, summary: str) -> None:
    if "low ongoing traffic" not in (log_text or "").lower():
        pytest.fail(f"{summary}: missing low ongoing traffic policy log")


def assert_independent_link_network_selection(
    log_text: str,
    *,
    summary: str,
    interfaces: tuple[str, ...] = ("wlan0", "wlan1"),
) -> None:
    lower = (log_text or "").lower()
    missing_scans = [
        interface
        for interface in interfaces
        if not parse_interface_scan_offsets(log_text, interface)
    ]
    missing_decisions = [
        interface
        for interface in interfaces
        if f"{interface}: current connected network is not sufficient" not in lower
    ]
    if missing_scans or missing_decisions:
        pytest.fail(
            f"{summary}: independent network selection evidence incomplete; "
            f"missing_scans={missing_scans!r}, "
            f"missing_decisions={missing_decisions!r}"
        )


def assert_scan_backoff_started(
    log_text: str,
    *,
    interface: str,
    summary: str,
    expected_first_interval_sec: float = 20.0,
    tolerance_sec: float = 5.0,
) -> None:
    scans = parse_interface_scan_offsets(log_text, interface)
    if len(scans) < 2:
        pytest.fail(
            f"{summary}: {interface} produced fewer than two periodic scans"
        )
    interval = scans[1] - scans[0]
    if abs(interval - expected_first_interval_sec) > tolerance_sec:
        pytest.fail(
            f"{summary}: first {interface} scan interval was {interval:.1f}s, "
            f"expected {expected_first_interval_sec:.1f}±{tolerance_sec:.1f}s"
        )


def assert_scan_backoff_policy(
    log_text: str,
    *,
    interface: str,
    summary: str,
    expected_intervals_sec: tuple[int, ...] = (20, 40, 80, 160),
    require_low_traffic: bool = True,
) -> None:
    """Assert low-quality scanning and one valid current backoff interval."""
    scans = parse_interface_scan_offsets(log_text, interface)
    if not scans:
        pytest.fail(f"{summary}: {interface} did not start a periodic scan")
    lower = (log_text or "").lower()
    if "not sufficient" not in lower:
        pytest.fail(f"{summary}: missing low-quality decision log")
    if require_low_traffic and "low ongoing traffic" not in lower:
        pytest.fail(f"{summary}: missing low-traffic decision log")
    intervals = [
        int(value) // 1000
        for value in re.findall(
            r"schedulePeriodicScanTimer\s+intervalMs\s+(\d+)",
            log_text or "",
            flags=re.IGNORECASE,
        )
    ]
    if not any(interval in expected_intervals_sec for interval in intervals):
        pytest.fail(
            f"{summary}: no expected scan backoff interval found; "
            f"actual={intervals!r}, expected={expected_intervals_sec!r}"
        )


def assert_scan_backoff_sequence(
    log_text: str,
    *,
    interface: str,
    summary: str,
    expected_intervals_sec: tuple[int, ...] = (20, 40, 80, 160),
    tolerance_sec: float = 5.0,
) -> None:
    scheduled = [
        int(value) // 1000
        for value in re.findall(
            r"schedulePeriodicScanTimer\s+intervalMs\s+(\d+)",
            log_text or "",
            flags=re.IGNORECASE,
        )
    ]
    expected_index = 0
    for interval in scheduled:
        if interval == expected_intervals_sec[expected_index]:
            expected_index += 1
            if expected_index == len(expected_intervals_sec):
                break
    if expected_index != len(expected_intervals_sec):
        pytest.fail(
            f"{summary}: scheduled backoff did not contain ordered sequence "
            f"{expected_intervals_sec!r}; actual={scheduled!r}"
        )

    scans = parse_interface_scan_offsets(log_text, interface)
    expected_scan_intervals = expected_intervals_sec[:-1]
    if len(scans) < len(expected_scan_intervals) + 1:
        pytest.fail(
            f"{summary}: {interface} produced {len(scans)} scan(s), "
            f"expected at least {len(expected_scan_intervals) + 1}"
        )
    actual_scan_intervals = [
        later - earlier
        for earlier, later in zip(scans, scans[1:])
    ]
    matching_window = next(
        (
            actual_scan_intervals[index : index + len(expected_scan_intervals)]
            for index in range(
                len(actual_scan_intervals) - len(expected_scan_intervals) + 1
            )
            if all(
                abs(actual - expected) <= tolerance_sec
                for actual, expected in zip(
                    actual_scan_intervals[
                        index : index + len(expected_scan_intervals)
                    ],
                    expected_scan_intervals,
                )
            )
        ),
        None,
    )
    if matching_window is None:
        pytest.fail(
            f"{summary}: {interface} scan intervals were "
            f"{actual_scan_intervals!r}s, expected "
            f"a contiguous {expected_scan_intervals!r}±{tolerance_sec:.1f}s "
            "backoff sequence"
        )


def assert_single_immediate_scan(
    log_text: str,
    *,
    elapsed_sec: float,
    summary: str,
    max_latency_sec: float = 6.0,
) -> None:
    """Assert that one autonomous scan completed promptly after a state change."""
    events = parse_network_selection_scan_events(log_text)
    cycles = parse_network_selection_scan_cycles(log_text)
    if len(cycles) != 1:
        pytest.fail(
            f"{summary}: expected one network-selection scan cycle, "
            f"found {len(cycles)} ({len(events)} interface callbacks)"
        )
    if elapsed_sec > max_latency_sec:
        pytest.fail(
            f"{summary}: scan completed after {elapsed_sec:.1f}s, "
            f"expected <= {max_latency_sec:.1f}s"
        )


def _read_network_selection_scan_log(adb: AdbHelper) -> str:
    _code, out, err = adb.shell_line(
        "logcat -d -v threadtime | grep -F "
        "'AllSingleScanListener onResults: start network selection'"
    )
    return "\n".join(part for part in (out, err) if part).strip()


def _read_interface_scan_log(adb: AdbHelper, interface: str) -> str:
    _code, out, err = adb.shell_line(
        "logcat -d -v threadtime | grep -F "
        f"'startSingleScan on real: {interface}'"
    )
    return "\n".join(part for part in (out, err) if part).strip()


def _wait_for_interface_scans(
    adb: AdbHelper,
    interface: str,
    *,
    minimum_scans: int,
    timeout_sec: float,
    interval_sec: float = 0.5,
) -> str:
    deadline = time.monotonic() + timeout_sec
    latest = ""
    while time.monotonic() < deadline:
        latest = _read_interface_scan_log(adb, interface)
        if len(parse_interface_scan_offsets(latest, interface)) >= minimum_scans:
            return latest
        time.sleep(interval_sec)
    return latest


def _read_scan_policy_log(adb: AdbHelper) -> str:
    _code, out, err = adb.shell_line(
        "logcat -d -v threadtime | grep -i -E "
        "'startSingleScan on real|schedulePeriodicScanTimer|sufficient|"
        "low ongoing traffic|hasActiveStream'"
    )
    return "\n".join(part for part in (out, err) if part).strip()


def _read_pno_scan_log(adb: AdbHelper) -> str:
    _code, out, err = adb.shell_line(
        "logcat -d -v threadtime | grep -i -F 'Pno scan started'"
    )
    return "\n".join(part for part in (out, err) if part).strip()


def _wait_for_pno_scan(
    adb: AdbHelper,
    *,
    timeout_sec: float,
    interval_sec: float = 0.5,
) -> tuple[str, float]:
    started = time.monotonic()
    deadline = started + timeout_sec
    latest = ""
    while time.monotonic() < deadline:
        latest = _read_pno_scan_log(adb)
        if parse_pno_scan_events(latest):
            return latest, time.monotonic() - started
        time.sleep(interval_sec)
    return latest, time.monotonic() - started


@allure.step("Verify disconnected HyperWiFi scans every 20 seconds on Home")
def run_screen_on_disconnected_hyper_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    miniap_action: MiniAPAction | None,
    *,
    wifi_entry_id: str = "hyperwifi_us",
    observation_sec: float = 50.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if miniap_action is None:
        pytest.skip(f"{summary}: miniAP Telnet is not configured")
    entry = get_wifi_list_entry(wifi_yaml, entry_id=wifi_entry_id)
    if not entry:
        pytest.skip(f"{summary}: missing WiFi profile {wifi_entry_id!r}")
    target_ssid = str(entry.get("ssid") or "")
    if not wifi.connect_wifi_block(cast(WiFiEntry, entry)):
        pytest.fail(f"{summary}: failed to connect {target_ssid!r}")

    radio_stopped = False
    try:
        miniap_action.stop_radio()
        radio_stopped = True
        if not wifi.wait_until_disconnected(timeout=20.0, interval=0.5):
            pytest.fail(f"{summary}: HyperWiFi did not disconnect after radio stop")

        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        scan_log = _wait_for_interface_scans(
            wifi.adb,
            "wlan1",
            minimum_scans=3,
            timeout_sec=observation_sec,
        )
        allure.attach(
            scan_log or "<no wlan1 scans>",
            f"{summary}-disconnected-home-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_periodic_scan_interval(
            scan_log,
            interface="wlan1",
            summary=summary,
            expected_interval_sec=20.0,
            minimum_scans=3,
        )
    finally:
        if radio_stopped:
            miniap_action.start_radio()
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


def _wait_for_network_selection_scan(
    adb: AdbHelper,
    *,
    timeout_sec: float,
    interval_sec: float = 0.25,
) -> tuple[str, float]:
    started = time.monotonic()
    deadline = started + timeout_sec
    latest = ""
    while time.monotonic() < deadline:
        latest = _read_network_selection_scan_log(adb)
        if parse_network_selection_scan_events(latest):
            return latest, time.monotonic() - started
        time.sleep(interval_sec)
    return latest, time.monotonic() - started


def _observe_single_scan_after_action(
    summary: str,
    adb: AdbHelper,
    action: Callable[[], None],
    *,
    max_latency_sec: float,
    duplicate_window_sec: float,
) -> float:
    adb.shell_line("logcat -c")
    action_started = time.monotonic()
    action()
    log_text, _wait_elapsed_sec = _wait_for_network_selection_scan(
        adb,
        timeout_sec=max_latency_sec,
    )
    elapsed_sec = time.monotonic() - action_started
    time.sleep(duplicate_window_sec)
    final_log = _read_network_selection_scan_log(adb) or log_text
    allure.attach(
        final_log or "<no matching scan event>",
        name=f"{summary}-network-selection-scan.log",
        attachment_type=allure.attachment_type.TEXT,
    )
    assert_single_immediate_scan(
        final_log,
        elapsed_sec=elapsed_sec,
        summary=summary,
        max_latency_sec=max_latency_sec,
    )
    print(
        f"[{summary}] autonomous network-selection scan completed "
        f"in {elapsed_sec:.2f}s"
    )
    return elapsed_sec


def _set_airplane_mode(
    run_shell_cmd: Callable[[str], str],
    enabled: bool,
    *,
    settle_sec: float = 2.0,
) -> None:
    expected = "1" if enabled else "0"
    action = "enable" if enabled else "disable"
    run_shell_cmd(f"cmd connectivity airplane-mode {action}")
    time.sleep(settle_sec)
    actual = run_shell_cmd("settings get global airplane_mode_on").strip()
    if actual != expected:
        pytest.fail(
            f"airplane mode did not become {expected!r}; actual={actual!r}"
        )


@allure.step("Verify a connected device does not start PNO scans while asleep")
def run_pno_connected_screen_off_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 25.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry, _ap_index = signal_level_entry(wifi_yaml, hyper=True)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    target_ssid = str(entry.get("ssid") or "")
    deadline = time.monotonic() + 35.0
    while time.monotonic() < deadline:
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if found:
            break
        time.sleep(1.0)
    else:
        pytest.fail(f"{summary}: HyperWiFi association timed out")

    try:
        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(observation_sec)
        pno_log = _read_pno_scan_log(wifi.adb)
        allure.attach(
            pno_log or "<no PNO scan>",
            f"{summary}-screen-off-pno.log",
            allure.attachment_type.TEXT,
        )
        assert_no_pno_scan(pno_log, summary=summary)
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: HyperWiFi disconnected while screen was off")
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify PNO scanning and reconnection after AP signal loss")
def run_pno_disconnected_screen_off_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    hyper: bool = True,
    screen_off_before_disconnect: bool = False,
    verify_reconnect: bool = True,
    pno_timeout_sec: float = 30.0,
    reconnect_timeout_sec: float = 30.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=hyper)
    link_name = "HyperWiFi" if hyper else "traditional WiFi"
    channel = attenuator.channel_for(hyper=hyper, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect {link_name}")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: {link_name} association timed out")

        if screen_off_before_disconnect:
            wifi.adb.shell_line("logcat -c")
            wifi.adb.keyevent("KEYCODE_SLEEP")
            time.sleep(2.0)

        attenuator.set_attenuation(channel, attenuator.max_attenuation_db)
        if not wifi.wait_until_disconnected(timeout=20.0, interval=0.5):
            pytest.fail(f"{summary}: {link_name} did not disconnect after signal loss")

        if not screen_off_before_disconnect:
            wifi.adb.shell_line("logcat -c")
            wifi.adb.keyevent("KEYCODE_SLEEP")
        pno_log, pno_elapsed_sec = _wait_for_pno_scan(
            wifi.adb,
            timeout_sec=pno_timeout_sec,
        )
        allure.attach(
            pno_log or "<no PNO scan>",
            f"{summary}-disconnected-screen-off-pno.log",
            allure.attachment_type.TEXT,
        )
        assert_pno_scan_started(pno_log, summary=summary)
        if not verify_reconnect:
            print(f"[{summary}] PNO started after {pno_elapsed_sec:.2f}s")
            return

        reconnect_started = time.monotonic()
        attenuator.set_attenuation(channel, original_attenuation)
        deadline = reconnect_started + reconnect_timeout_sec
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                reconnect_elapsed_sec = time.monotonic() - reconnect_started
                print(
                    f"[{summary}] PNO started after {pno_elapsed_sec:.2f}s; "
                    f"{link_name} reconnected after {reconnect_elapsed_sec:.2f}s"
                )
                return
            time.sleep(0.5)
        pytest.fail(
            f"{summary}: {link_name} did not reconnect within "
            f"{reconnect_timeout_sec:.0f}s after PNO"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify PNO scanning and reconnection after miniAP reboot")
def run_pno_miniap_reboot_screen_off_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    miniap_action: MiniAPAction | None,
    *,
    wifi_entry_id: str = "hyperwifi_us",
    total_timeout_sec: float = 100.0,
    reconnect_limit_sec: float = 30.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if miniap_action is None:
        pytest.skip(f"{summary}: miniAP Telnet is not configured")
    entry = get_wifi_list_entry(wifi_yaml, entry_id=wifi_entry_id)
    if not entry:
        pytest.skip(f"{summary}: missing WiFi profile {wifi_entry_id!r}")
    target_ssid = str(entry.get("ssid") or "")
    if not wifi.connect_wifi_block(cast(WiFiEntry, entry)):
        pytest.fail(f"{summary}: failed to connect {target_ssid!r}")
    deadline = time.monotonic() + 35.0
    while time.monotonic() < deadline:
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if found:
            break
        time.sleep(1.0)
    else:
        pytest.fail(f"{summary}: HyperWiFi association timed out")

    disconnected = False
    pno_started_at: float | None = None
    reconnect_elapsed_sec: float | None = None
    pno_log = ""
    try:
        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(2.0)
        deadline = time.monotonic() + total_timeout_sec
        with ThreadPoolExecutor(max_workers=1) as executor:
            reboot = executor.submit(miniap_action.reboot_miniAP)
            while time.monotonic() < deadline:
                found, _missing = wifi.match_associated_ssids([target_ssid])
                if not found:
                    disconnected = True

                pno_log = _read_pno_scan_log(wifi.adb)
                if pno_started_at is None and parse_pno_scan_events(pno_log):
                    pno_started_at = time.monotonic()

                if disconnected and pno_started_at is not None and found:
                    reconnect_elapsed_sec = time.monotonic() - pno_started_at
                    break
                if reboot.done() and reboot.exception() is not None:
                    reboot.result()
                time.sleep(0.5)

            remaining_sec = max(0.0, deadline - time.monotonic())
            reboot.result(timeout=remaining_sec)

        allure.attach(
            pno_log or "<no PNO scan>",
            f"{summary}-miniap-reboot-pno.log",
            allure.attachment_type.TEXT,
        )
        if not disconnected:
            pytest.fail(f"{summary}: HyperWiFi did not disconnect during reboot")
        assert_pno_scan_started(pno_log, summary=summary)
        if reconnect_elapsed_sec is None:
            pytest.fail(
                f"{summary}: {target_ssid!r} did not reconnect within "
                f"{total_timeout_sec:.0f}s"
            )
        if reconnect_elapsed_sec >= reconnect_limit_sec:
            pytest.fail(
                f"{summary}: reconnect took {reconnect_elapsed_sec:.2f}s from "
                f"PNO start, expected <{reconnect_limit_sec:.0f}s"
            )
        print(
            f"[{summary}] miniAP reboot disconnected {target_ssid!r}; "
            f"PNO started and reconnected in {reconnect_elapsed_sec:.2f}s"
        )
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify no PNO scan starts when no networks are saved")
def run_pno_no_saved_network_screen_off_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    hyper: bool = True,
    observation_sec: float = 25.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry, _ap_index = signal_level_entry(wifi_yaml, hyper=hyper)
    if not wifi.connect_wifi_block(entry):
        link_name = "HyperWiFi" if hyper else "traditional WiFi"
        pytest.fail(f"{summary}: failed to connect {link_name}")
    target_ssid = str(entry.get("ssid") or "")
    deadline = time.monotonic() + 35.0
    while time.monotonic() < deadline:
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if found:
            break
        time.sleep(1.0)
    else:
        link_name = "HyperWiFi" if hyper else "traditional WiFi"
        pytest.fail(f"{summary}: {link_name} association timed out")

    network_id = wifi.find_network_id_by_ssid(target_ssid)
    if not network_id or not wifi.forget_network(network_id):
        pytest.fail(f"{summary}: failed to forget HyperWiFi")
    if not wifi.wait_until_disconnected(timeout=10.0, interval=0.5):
        pytest.fail(f"{summary}: HyperWiFi remained connected after forgetting")
    saved_networks = parse_list_networks(wifi.list_networks_blob())
    if saved_networks:
        pytest.fail(f"{summary}: saved networks remain: {saved_networks!r}")

    try:
        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(observation_sec)
        pno_log = _read_pno_scan_log(wifi.adb)
        allure.attach(
            pno_log or "<no PNO scan>",
            f"{summary}-no-saved-network-pno.log",
            allure.attachment_type.TEXT,
        )
        assert_no_pno_scan(pno_log, summary=summary)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify weak traditional WiFi triggers a roaming scan while asleep")
def run_screen_off_wifi_roaming_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int = -76,
    observation_sec: float = 25.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channel = attenuator.channel_for(hyper=False, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    interface = "wlan0"

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)

        def read_rssi() -> int | None:
            measured_rssi, _frequency = link_radio_metrics(
                run_shell_cmd("cmd wifi status"),
                interface,
            )
            return measured_rssi

        target_attenuation, calibrated_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            target_rssi,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
        )
        if calibrated_rssi is None or abs(calibrated_rssi - target_rssi) > 2:
            pytest.fail(
                f"{summary}: RSSI calibration failed: {calibrated_rssi} dBm"
            )

        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        attenuator.set_attenuation(channel, target_attenuation)
        time.sleep(observation_sec)
        scan_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            scan_log or "<no scan policy log>",
            f"{summary}-screen-off-roaming-policy.log",
            allure.attachment_type.TEXT,
        )
        assert_interface_scan_started(
            scan_log,
            interface=interface,
            summary=summary,
        )
        found, _missing = wifi.match_associated_ssids([str(entry.get("ssid") or "")])
        if not found:
            pytest.fail(f"{summary}: traditional WiFi disconnected at target RSSI")
        print(
            f"[{summary}] {interface} scanned while screen was off at "
            f"{calibrated_rssi} dBm"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify Settings triggers 10-second WiFi scans while awake")
def run_screen_on_settings_periodic_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    hyper: bool = True,
    target_rssi: int | None = -75,
    observation_sec: float = 35.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=hyper)
    interface = "wlan1" if hyper else "wlan0"
    link_name = "HyperWiFi" if hyper else "traditional WiFi"
    channel = attenuator.channel_for(hyper=hyper, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect {link_name}")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: {link_name} association timed out")

        measured_rssi = None
        if target_rssi is not None:
            read_rssi = (
                _hyper_rssi_reader(run_shell_cmd)
                if hyper
                else _traditional_rssi_reader(run_shell_cmd, target_ssid)
            )
            _target_attenuation, measured_rssi = tune_attenuation_for_rssi(
                attenuator,
                channel,
                target_rssi,
                read_rssi,
                settle_sec=4.0,
                tolerance_db=2,
            )
            if measured_rssi is None or abs(measured_rssi - target_rssi) > 2:
                pytest.fail(
                    f"{summary}: RSSI calibration failed: {measured_rssi} dBm"
                )

        wifi.open_wifi_settings()
        wifi.adb.shell_line("logcat -c")
        scan_log = _wait_for_interface_scans(
            wifi.adb,
            interface,
            minimum_scans=2,
            timeout_sec=observation_sec,
        )
        allure.attach(
            scan_log or "<no interface scan>",
            f"{summary}-settings-periodic-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_periodic_scan_interval(
            scan_log,
            interface=interface,
            summary=summary,
            expected_interval_sec=10.0,
        )
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: {link_name} disconnected during observation")
        print(
            f"[{summary}] {interface} maintained a 10-second Settings scan period"
            + (f" at {measured_rssi} dBm" if measured_rssi is not None else "")
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify screen-on HyperWiFi scanning follows the RSSI threshold")
def run_screen_on_hyper_rssi_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int,
    expect_scan: bool,
    observation_sec: float | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=True)
    channel = attenuator.channel_for(hyper=True, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")
    duration_sec = observation_sec or (65.0 if expect_scan else 25.0)

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: HyperWiFi association timed out")

        _target_attenuation, measured_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=4.0,
            tolerance_db=2,
            allow_missing=expect_scan,
        )
        if measured_rssi is None or abs(measured_rssi - target_rssi) > 2:
            pytest.fail(
                f"{summary}: HyperWiFi disconnected before reaching "
                f"{target_rssi} dBm; last RSSI={measured_rssi}"
            )

        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        time.sleep(duration_sec)
        scan_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            scan_log or "<no scan policy log>",
            f"{summary}-screen-on-rssi-policy.log",
            allure.attachment_type.TEXT,
        )
        if expect_scan:
            assert_scan_backoff_policy(
                scan_log,
                interface="wlan1",
                summary=summary,
                require_low_traffic=False,
            )
        else:
            assert_no_interface_scan(
                scan_log,
                interface="wlan1",
                summary=summary,
            )
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: HyperWiFi disconnected during observation")
        print(
            f"[{summary}] target={target_rssi} dBm measured={measured_rssi} dBm; "
            f"scan_expected={expect_scan}"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify screen wake resets weak-signal HyperWiFi scan backoff")
def run_screen_on_scan_backoff_reset_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int = -88,
    precondition_timeout_sec: float = 95.0,
    reset_observation_sec: float = 170.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=True)
    channel = attenuator.channel_for(hyper=True, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: HyperWiFi association timed out")

        _target_attenuation, measured_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=4.0,
            tolerance_db=2,
        )
        if measured_rssi is None or abs(measured_rssi - target_rssi) > 2:
            pytest.fail(
                f"{summary}: RSSI calibration failed: {measured_rssi} dBm"
            )

        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        deadline = time.monotonic() + precondition_timeout_sec
        before_sleep_log = ""
        while time.monotonic() < deadline:
            before_sleep_log = _read_scan_policy_log(wifi.adb)
            if re.search(
                r"schedulePeriodicScanTimer\s+intervalMs\s+80000",
                before_sleep_log,
                flags=re.IGNORECASE,
            ):
                break
            time.sleep(1.0)
        allure.attach(
            before_sleep_log or "<no scan policy log>",
            f"{summary}-before-screen-cycle.log",
            allure.attachment_type.TEXT,
        )
        assert_scan_backoff_policy(
            before_sleep_log,
            interface="wlan1",
            summary=f"{summary}/before-screen-cycle",
            expected_intervals_sec=(80,),
            require_low_traffic=False,
        )

        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(3.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")
        deadline = time.monotonic() + reset_observation_sec
        after_wake_log = ""
        while time.monotonic() < deadline:
            after_wake_log = _read_scan_policy_log(wifi.adb)
            if re.search(
                r"schedulePeriodicScanTimer\s+intervalMs\s+160000",
                after_wake_log,
                flags=re.IGNORECASE,
            ):
                break
            time.sleep(1.0)
        allure.attach(
            after_wake_log or "<no scan policy log>",
            f"{summary}-after-screen-cycle.log",
            allure.attachment_type.TEXT,
        )
        assert_scan_backoff_sequence(
            after_wake_log,
            interface="wlan1",
            summary=f"{summary}/after-screen-cycle",
        )
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: HyperWiFi disconnected during observation")
        print(
            f"[{summary}] wlan1 reached 80-second backoff, then screen wake "
            "reset scanning to 20/40/80/160 seconds"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify the disconnected radio follows screen-on scan backoff")
def run_screen_on_single_link_disconnected_radio_scan_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 170.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    traditional, hyper = dual_link_legs(primary_backup_entry(wifi_yaml))
    stages = (
        ("traditional-only", traditional, hyper, "wlan1"),
        ("hyper-only", hyper, traditional, "wlan0"),
    )

    try:
        for stage, target, absent, scan_interface in stages:
            if not wifi.disconnect_all(
                settle_sec=1.0,
                max_rounds=2,
                post_wait_sec=2.0,
            ):
                pytest.fail(f"{summary}: failed to disconnect before {stage}")
            wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
            wifi.adb.shell_line("logcat -c")
            target_ssid = str(target.get("ssid") or "")
            absent_ssid = str(absent.get("ssid") or "")
            if not wifi.connect_wifi_block(target):
                pytest.fail(f"{summary}: failed to connect {target_ssid!r}")

            deadline = time.monotonic() + 35.0
            found: list[str] = []
            missing: list[str] = []
            while time.monotonic() < deadline:
                found, missing = wifi.match_associated_ssids(
                    [target_ssid, absent_ssid],
                    use_dumpsys_for_missing=True,
                )
                if target_ssid in found and absent_ssid in missing:
                    break
                time.sleep(1.0)
            else:
                pytest.fail(
                    f"{summary}: {stage} precondition failed; "
                    f"found={found!r}, missing={missing!r}"
                )

            wifi.adb.keyevent("KEYCODE_HOME")
            time.sleep(1.0)
            initial_policy_log = _read_scan_policy_log(wifi.adb)
            initial_schedule_log = "\n".join(
                line
                for line in initial_policy_log.splitlines()
                if "schedulePeriodicScanTimer" in line
            )
            wifi.adb.shell_line("logcat -c")
            deadline = time.monotonic() + observation_sec
            observed_policy_log = ""
            while time.monotonic() < deadline:
                observed_policy_log = _read_scan_policy_log(wifi.adb)
                if len(
                    parse_interface_scan_offsets(
                        observed_policy_log,
                        scan_interface,
                    )
                ) >= 4:
                    break
                time.sleep(1.0)
            policy_log = "\n".join(
                part
                for part in (initial_schedule_log, observed_policy_log)
                if part
            )
            allure.attach(
                policy_log or "<no scan policy log>",
                f"{summary}-{stage}-scan-backoff.log",
                allure.attachment_type.TEXT,
            )
            assert_scan_backoff_sequence(
                policy_log,
                interface=scan_interface,
                summary=f"{summary}/{stage}",
            )
            found, missing = wifi.match_associated_ssids(
                [target_ssid, absent_ssid],
                use_dumpsys_for_missing=True,
            )
            if target_ssid not in found or absent_ssid not in missing:
                pytest.fail(
                    f"{summary}: {stage} changed during observation; "
                    f"found={found!r}, missing={missing!r}"
                )
            print(
                f"[{summary}] {stage}: {scan_interface} followed "
                "20/40/80/160-second backoff"
            )
    finally:
        wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify sufficient traditional WiFi skips candidate nomination")
def run_candidate_skip_wifi_rssi_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    expected_band: str,
    threshold_rssi: int,
    observation_sec: float = 35.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    configured_bssids = entry.get("bssids")
    if not isinstance(configured_bssids, Mapping):
        pytest.skip(f"{summary}: traditional WiFi profile has no band BSSIDs")
    target_bssid = str(configured_bssids.get(expected_band) or "").lower()
    if not target_bssid:
        pytest.skip(f"{summary}: no BSSID is configured for {expected_band}")

    channel = attenuator.channel_for(hyper=False, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    interface = "wlan0"

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        ssid = str(entry.get("ssid") or "")
        network_id = wifi.find_network_id_by_ssid(ssid)
        if network_id:
            wifi.forget_network(network_id)
        if not wifi.connect_wifi_block({**entry, "bssid": target_bssid}):
            pytest.fail(f"{summary}: failed to connect BSSID {target_bssid}")
        wait_for_link_bssid(summary, run_shell_cmd, interface, target_bssid)

        def read_rssi() -> int | None:
            measured_rssi, _frequency = link_radio_metrics(
                run_shell_cmd("cmd wifi status"),
                interface,
            )
            return measured_rssi

        _target_attenuation, measured_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            threshold_rssi + 5,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
        )
        if measured_rssi is None or measured_rssi <= threshold_rssi:
            pytest.fail(
                f"{summary}: sufficient RSSI precondition failed: "
                f"{measured_rssi} dBm"
            )

        wifi.open_wifi_settings()
        wifi.adb.shell_line("logcat -c")
        scan_log = _wait_for_interface_scans(
            wifi.adb,
            interface,
            minimum_scans=2,
            timeout_sec=observation_sec,
        )
        policy_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            policy_log or scan_log or "<no scan policy log>",
            f"{summary}-candidate-skip-policy.log",
            allure.attachment_type.TEXT,
        )
        assert_periodic_scan_interval(
            scan_log,
            interface=interface,
            summary=summary,
            expected_interval_sec=10.0,
        )
        assert_network_selection_skipped_for_sufficient_link(
            policy_log,
            interface=interface,
            summary=summary,
        )
        wait_for_link_bssid(summary, run_shell_cmd, interface, target_bssid)
        print(
            f"[{summary}] {expected_band} RSSI={measured_rssi} dBm; "
            "periodic scans skipped candidate nomination"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify sufficient HyperWiFi skips candidate nomination")
def run_candidate_skip_hyper_rssi_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int = -80,
    observation_sec: float = 35.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=True)
    channel = attenuator.channel_for(hyper=True, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: HyperWiFi association timed out")

        _target_attenuation, measured_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=4.0,
            tolerance_db=2,
        )
        if measured_rssi is None or measured_rssi <= -86:
            pytest.fail(
                f"{summary}: sufficient HyperWiFi RSSI precondition failed: "
                f"{measured_rssi} dBm"
            )

        wifi.open_wifi_settings()
        wifi.adb.shell_line("logcat -c")
        scan_log = _wait_for_interface_scans(
            wifi.adb,
            "wlan1",
            minimum_scans=2,
            timeout_sec=observation_sec,
        )
        policy_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            policy_log or scan_log or "<no scan policy log>",
            f"{summary}-candidate-skip-policy.log",
            allure.attachment_type.TEXT,
        )
        assert_periodic_scan_interval(
            scan_log,
            interface="wlan1",
            summary=summary,
            expected_interval_sec=10.0,
        )
        assert_network_selection_skipped_for_sufficient_link(
            policy_log,
            interface="wlan1",
            summary=summary,
        )
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: HyperWiFi disconnected during observation")
        print(
            f"[{summary}] HyperWiFi RSSI={measured_rssi} dBm; "
            "periodic scans skipped candidate nomination"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify active HyperWiFi traffic skips candidate nomination")
def run_candidate_skip_hyper_traffic_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int = -70,
    traffic_packets_per_sec: int = 20,
    traffic_duration_sec: int = 30,
    low_rssi: int = -88,
    settings_page: bool = True,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=True)
    channel = attenuator.channel_for(hyper=True, ap_index=ap_index)
    current = dict(attenuator.read_attenuations())
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    target_ssid = str(entry.get("ssid") or "")
    scan_interface = "wlan1"

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: HyperWiFi association timed out")

        target_attenuation, measured_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=4.0,
            tolerance_db=2,
        )
        if measured_rssi is None or abs(measured_rssi - target_rssi) > 2:
            pytest.fail(f"{summary}: RSSI calibration failed: {measured_rssi} dBm")

        _code, route_out, route_err = wifi.adb.shell_line(
            "ip route show table all"
        )
        route_text = "\n".join(part for part in (route_out, route_err) if part)
        active_route = parse_active_default_route(route_text)
        if active_route is None:
            pytest.skip(f"{summary}: HyperWiFi has no routed data path")
        gateway, data_interface = active_route

        if settings_page:
            wifi.open_wifi_settings()
        else:
            wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        packet_count = traffic_packets_per_sec * traffic_duration_sec
        ping_interval = 1.0 / traffic_packets_per_sec
        ping_command = (
            f"ping -I {data_interface} -c {packet_count} "
            f"-i {ping_interval:.3f} "
            f"-W 2 {gateway}"
        )
        with ThreadPoolExecutor(max_workers=1) as executor:
            ping_future = executor.submit(
                wifi.adb.shell_line,
                ping_command,
                timeout_sec=traffic_duration_sec + 10.0,
            )
            if settings_page:
                scan_log = _wait_for_interface_scans(
                    wifi.adb,
                    scan_interface,
                    minimum_scans=2,
                    timeout_sec=traffic_duration_sec - 2.0,
                )
            else:
                time.sleep(traffic_duration_sec - 2.0)
                scan_log = _read_interface_scan_log(wifi.adb, scan_interface)
            ping_code, ping_out, ping_err = ping_future.result()
        ping_text = "\n".join(part for part in (ping_out, ping_err) if part)
        allure.attach(
            ping_text or "<no ping output>",
            f"{summary}-active-stream-ping.log",
            allure.attachment_type.TEXT,
        )
        if ping_code != 0:
            pytest.fail(f"{summary}: traffic generation failed: {ping_text!r}")

        active_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            active_log or scan_log or "<no active-stream policy log>",
            f"{summary}-active-stream-policy.log",
            allure.attachment_type.TEXT,
        )
        if settings_page:
            assert_periodic_scan_interval(
                scan_log,
                interface=scan_interface,
                summary=f"{summary}/active-stream",
                expected_interval_sec=10.0,
            )
        else:
            assert_no_interface_scan(
                scan_log,
                interface=scan_interface,
                summary=f"{summary}/active-stream",
            )
        assert_active_stream_policy(active_log, summary=summary)

        wifi.adb.shell_line("logcat -c")
        low_attenuation = min(
            float(attenuator.max_attenuation_db),
            target_attenuation + abs(low_rssi - target_rssi),
        )
        attenuation = target_attenuation
        while attenuation < low_attenuation:
            attenuation = min(attenuation + 1.0, low_attenuation)
            attenuator.set_attenuation(channel, attenuation)
            time.sleep(1.0)
        low_measured_rssi = _hyper_rssi_reader(run_shell_cmd)()
        if low_measured_rssi is None or low_measured_rssi > low_rssi + 3:
            pytest.fail(
                f"{summary}: low-RSSI precondition failed: "
                f"{low_measured_rssi} dBm"
            )
        low_log = ""
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            low_log = _read_scan_policy_log(wifi.adb)
            if "low ongoing traffic" in low_log.lower():
                break
            time.sleep(1.0)
        allure.attach(
            low_log or "<no low-traffic policy log>",
            f"{summary}-low-traffic-policy.log",
            allure.attachment_type.TEXT,
        )
        assert_low_traffic_policy(low_log, summary=summary)
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if not found:
            pytest.fail(f"{summary}: HyperWiFi disconnected during observation")
        print(
            f"[{summary}] wlan1 generated {traffic_packets_per_sec} packets/s "
            f"at {measured_rssi} dBm, then reached {low_measured_rssi} dBm "
            "with low traffic"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify active HyperWiFi traffic suppresses periodic scans")
def run_autoscan_skip_hyper_traffic_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
) -> None:
    run_candidate_skip_hyper_traffic_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator,
        settings_page=False,
    )


@allure.step("Verify dual-link network selection runs independently")
def run_dual_link_network_selection_independence_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    target_rssi: int = -88,
    observation_sec: float = 65.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry = primary_backup_entry(wifi_yaml)
    traditional, hyper = dual_link_legs(entry)
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = dict(attenuator.read_attenuations())
    if any(channel not in original for channel in channels.values()):
        pytest.fail(
            f"{summary}: attenuator query omitted target channels; "
            f"channels={channels!r}, state={original!r}"
        )

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: dual-link connection failed; "
                f"found={found!r}, missing={missing!r}"
            )
        calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"wifi": target_rssi, "hyper": target_rssi},
            settle_sec=4.0,
            links=("hyper", "wifi"),
        )
        for link, (_attenuation, measured_rssi) in calibrated.items():
            if measured_rssi is None or abs(measured_rssi - target_rssi) > 2:
                pytest.fail(
                    f"{summary}: {link} RSSI calibration failed: "
                    f"{measured_rssi} dBm"
                )

        targets = [
            str(traditional.get("ssid") or ""),
            str(hyper.get("ssid") or ""),
        ]
        found, missing = wifi.match_associated_ssids(
            targets,
            use_dumpsys_for_missing=True,
        )
        if missing:
            pytest.fail(
                f"{summary}: dual links disconnected during RSSI calibration; "
                f"found={found!r}, missing={missing!r}"
            )

        wifi.adb.keyevent("KEYCODE_HOME")
        wifi.adb.shell_line("logcat -c")
        time.sleep(observation_sec)
        policy_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            policy_log or "<no scan policy log>",
            f"{summary}-dual-link-selection-policy.log",
            allure.attachment_type.TEXT,
        )
        assert_independent_link_network_selection(policy_log, summary=summary)
        found, missing = wifi.match_associated_ssids(
            targets,
            use_dumpsys_for_missing=True,
        )
        if missing:
            pytest.fail(
                f"{summary}: dual links did not remain connected; "
                f"found={found!r}, missing={missing!r}"
            )
        print(
            f"[{summary}] independent scans confirmed for wlan0/wlan1; "
            f"RSSI={calibrated!r}"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify an immediate scan after WLAN is re-enabled")
def run_autoscan_after_wlan_toggle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    max_latency_sec: float = 6.0,
    duplicate_window_sec: float = 1.5,
) -> None:
    """Verify one autonomous selection scan after a WLAN disable/enable cycle."""
    attach_wifi_status(summary, run_shell_cmd)
    original_wifi_enabled = wifi.is_wifi_enabled()
    try:
        if not wifi.set_wifi_enabled(False):
            pytest.fail(f"{summary}: failed to disable WLAN")

        def enable_wlan() -> None:
            if not wifi.set_wifi_enabled(True):
                pytest.fail(f"{summary}: failed to enable WLAN")

        _observe_single_scan_after_action(
            summary,
            wifi.adb,
            enable_wlan,
            max_latency_sec=max_latency_sec,
            duplicate_window_sec=duplicate_window_sec,
        )
    finally:
        wifi.set_wifi_enabled(original_wifi_enabled)


@allure.step("Verify an immediate scan after the current connection disconnects")
def run_autoscan_after_disconnect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    settings_page: bool = False,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd)
    if settings_page:
        wifi.open_wifi_settings()
    else:
        wifi.adb.keyevent("KEYCODE_HOME")

    def disconnect() -> None:
        if not wifi.disconnect_all(settle_sec=0.5, post_wait_sec=2.0):
            pytest.fail(f"{summary}: failed to disconnect the current network")

    _observe_single_scan_after_action(
        summary,
        wifi.adb,
        disconnect,
        max_latency_sec=6.0,
        duplicate_window_sec=1.5,
    )


@allure.step("Verify an immediate scan after airplane mode is disabled")
def run_autoscan_after_airplane_cycle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    original_airplane = run_shell_cmd(
        "settings get global airplane_mode_on"
    ).strip()
    try:
        if original_airplane == "1":
            _set_airplane_mode(run_shell_cmd, False)
        _set_airplane_mode(run_shell_cmd, True)
        _observe_single_scan_after_action(
            summary,
            wifi.adb,
            lambda: _set_airplane_mode(run_shell_cmd, False),
            max_latency_sec=6.0,
            duplicate_window_sec=1.5,
        )
    finally:
        _set_airplane_mode(run_shell_cmd, original_airplane == "1")


@allure.step("Verify an immediate scan after an unconnected device wakes")
def run_autoscan_after_screen_wake_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if not wifi.disconnect_all(settle_sec=0.5, post_wait_sec=2.0):
        pytest.fail(f"{summary}: failed to reach the unconnected precondition")
    wifi.adb.keyevent("KEYCODE_HOME")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    time.sleep(1.0)

    def wake() -> None:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")

    _observe_single_scan_after_action(
        summary,
        wifi.adb,
        wake,
        max_latency_sec=6.0,
        duplicate_window_sec=1.5,
    )


@allure.step("Verify an immediate scan after weak signal disconnects WLAN")
def run_autoscan_after_weak_signal_disconnect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channel = attenuator.channel_for(hyper=False, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)

        def weaken_until_disconnected() -> None:
            attenuator.set_attenuation(channel, attenuator.max_attenuation_db)
            if not wifi.wait_until_disconnected(timeout=20.0, interval=0.5):
                pytest.fail(
                    f"{summary}: WLAN remained connected at maximum attenuation"
                )

        _observe_single_scan_after_action(
            summary,
            wifi.adb,
            weaken_until_disconnected,
            max_latency_sec=25.0,
            duplicate_window_sec=1.5,
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)


@allure.step("Verify RSSI sufficiency suppresses periodic WLAN scans")
def run_autoscan_skip_wifi_rssi_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    expected_band: str,
    threshold_rssi: int,
    high_observation_sec: float = 22.0,
    low_observation_sec: float = 65.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    configured_bssids = entry.get("bssids")
    if not isinstance(configured_bssids, Mapping):
        pytest.skip(f"{summary}: traditional WiFi profile has no band BSSIDs")
    target_bssid = str(configured_bssids.get(expected_band) or "").lower()
    if not target_bssid:
        pytest.skip(f"{summary}: no BSSID is configured for {expected_band}")

    channel = attenuator.channel_for(hyper=False, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    interface = "wlan0"

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        ssid = str(entry.get("ssid") or "")
        network_id = wifi.find_network_id_by_ssid(ssid)
        if network_id:
            wifi.forget_network(network_id)
        if not wifi.connect_wifi_block({**entry, "bssid": target_bssid}):
            pytest.fail(f"{summary}: failed to connect BSSID {target_bssid}")
        wait_for_link_bssid(summary, run_shell_cmd, interface, target_bssid)

        def read_rssi() -> int | None:
            measured_rssi, _frequency = link_radio_metrics(
                run_shell_cmd("cmd wifi status"),
                interface,
            )
            return measured_rssi

        _high_attenuation, high_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            threshold_rssi + 5,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
        )
        if high_rssi is None or high_rssi <= threshold_rssi:
            pytest.fail(
                f"{summary}: high RSSI precondition failed: {high_rssi} dBm"
            )
        wifi.adb.shell_line("logcat -c")
        time.sleep(high_observation_sec)
        high_log = _read_interface_scan_log(wifi.adb, interface)
        allure.attach(
            high_log or "<no interface scan>",
            f"{summary}-high-rssi-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_no_interface_scan(
            high_log,
            interface=interface,
            summary=summary,
        )

        _low_attenuation, low_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            threshold_rssi - 5,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
        )
        if low_rssi is None or low_rssi >= threshold_rssi:
            pytest.fail(
                f"{summary}: low RSSI precondition failed: {low_rssi} dBm"
            )
        wifi.adb.shell_line("logcat -c")
        time.sleep(low_observation_sec)
        low_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            low_log or "<no interface scan>",
            f"{summary}-low-rssi-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_scan_backoff_policy(
            low_log,
            interface=interface,
            summary=summary,
        )
        print(
            f"[{summary}] {expected_band}: high={high_rssi} dBm no scan; "
            f"low={low_rssi} dBm periodic scan resumed"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)


@allure.step("Verify HyperWiFi RSSI sufficiency suppresses periodic scans")
def run_autoscan_skip_hyper_rssi_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    threshold_rssi: int = -86,
    high_observation_sec: float = 22.0,
    low_observation_sec: float = 65.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    entry, ap_index = signal_level_entry(wifi_yaml, hyper=True)
    channel = attenuator.channel_for(hyper=True, ap_index=ap_index)
    current = attenuator.read_attenuations()
    if channel not in current:
        pytest.fail(f"{summary}: attenuator channel {channel} is unavailable")
    original_attenuation = current[channel]
    interface = "wlan1"

    try:
        attenuator.set_attenuation(channel, 0)
        time.sleep(3.0)
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        target_ssid = str(entry.get("ssid") or "")
        deadline = time.monotonic() + 35.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target_ssid])
            if found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: HyperWiFi connection timed out")

        read_rssi = _hyper_rssi_reader(run_shell_cmd)
        _high_attenuation, high_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            threshold_rssi + 5,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
        )
        if high_rssi is None or high_rssi <= threshold_rssi:
            pytest.fail(
                f"{summary}: high RSSI precondition failed: {high_rssi} dBm"
            )
        wifi.adb.shell_line("logcat -c")
        time.sleep(high_observation_sec)
        high_log = _read_interface_scan_log(wifi.adb, interface)
        allure.attach(
            high_log or "<no interface scan>",
            f"{summary}-high-rssi-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_no_interface_scan(
            high_log,
            interface=interface,
            summary=summary,
        )

        _low_attenuation, low_rssi = tune_attenuation_for_rssi(
            attenuator,
            channel,
            threshold_rssi - 5,
            read_rssi,
            settle_sec=4.0,
            tolerance_db=2,
            allow_missing=True,
        )
        if low_rssi is not None and low_rssi >= threshold_rssi:
            pytest.fail(
                f"{summary}: low RSSI precondition failed: {low_rssi} dBm"
            )
        wifi.adb.shell_line("logcat -c")
        time.sleep(low_observation_sec)
        low_log = _read_scan_policy_log(wifi.adb)
        allure.attach(
            low_log or "<no scan policy log>",
            f"{summary}-low-rssi-scan.log",
            allure.attachment_type.TEXT,
        )
        assert_scan_backoff_policy(
            low_log,
            interface=interface,
            summary=summary,
        )
        print(
            f"[{summary}] HyperWiFi: high={high_rssi} dBm no scan; "
            f"low={low_rssi} dBm periodic scan resumed"
        )
    finally:
        attenuator.set_attenuation(channel, original_attenuation)


@allure.step("Verify HyperWiFi candidate scoring and RSSI selection")
def run_score_hyper_candidates_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    stronger_entry_id: str = "hyperwifi_lab_miniap1",
    weaker_entry_id: str = "hyperwifi_lab_miniap2",
    stronger_target_rssi: int = -60,
    weaker_target_rssi: int = -70,
    expected_rssi_scores: tuple[int, int] | None = None,
    require_equal_final_scores: bool = False,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    stronger = get_wifi_list_entry(wifi_yaml, entry_id=stronger_entry_id)
    weaker = get_wifi_list_entry(wifi_yaml, entry_id=weaker_entry_id)
    if not stronger or not weaker:
        pytest.skip(f"{summary}: miniAP1/miniAP2 WiFi profiles are missing")

    stronger_ssid = str(stronger.get("ssid") or "")
    weaker_ssid = str(weaker.get("ssid") or "")
    channels = {
        stronger_ssid: attenuator.channel_for(hyper=True, ap_index=1),
        weaker_ssid: attenuator.channel_for(hyper=True, ap_index=2),
    }
    original_attenuations = dict(attenuator.read_attenuations())
    original_saved = set(wifi.list_saved_networks())

    def scan_rssi_reader(ssid: str) -> Callable[[], int | None]:
        def read() -> int | None:
            run_shell_cmd("cmd wifi start-scan")
            time.sleep(2.0)
            values = scan_result_rssis(
                run_shell_cmd("cmd wifi list-scan-results"),
                ssid,
            )
            return max(values) if values else None

        return read

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 20)
        time.sleep(4.0)
        for entry, ssid in ((weaker, weaker_ssid), (stronger, stronger_ssid)):
            if not wifi.connect_wifi_block(cast(WiFiEntry, entry)):
                pytest.fail(f"{summary}: failed to save/connect {ssid!r}")
            deadline = time.monotonic() + 25.0
            while time.monotonic() < deadline:
                found, _missing = wifi.match_associated_ssids([ssid])
                if found:
                    break
                time.sleep(1.0)
            else:
                pytest.fail(f"{summary}: association timed out for {ssid!r}")

        _stronger_attenuation, stronger_rssi = tune_attenuation_for_rssi(
            attenuator,
            channels[stronger_ssid],
            stronger_target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=3.0,
            tolerance_db=2,
        )
        _weaker_attenuation, weaker_rssi = tune_attenuation_for_rssi(
            attenuator,
            channels[weaker_ssid],
            weaker_target_rssi,
            scan_rssi_reader(weaker_ssid),
            settle_sec=3.0,
            tolerance_db=2,
        )
        score_log = ""
        selected = ""
        for attempt in range(1, 4):
            run_shell_cmd("cmd wifi start-scan")
            time.sleep(3.0)
            wifi.adb.shell_line("logcat -c")
            if not wifi.set_wifi_enabled(False, settle_sec=1.0):
                pytest.fail(f"{summary}: failed to disable WLAN")
            time.sleep(3.0)
            if not wifi.set_wifi_enabled(True, settle_sec=1.0):
                pytest.fail(f"{summary}: failed to enable WLAN")

            deadline = time.monotonic() + 30.0
            selected = ""
            while time.monotonic() < deadline:
                found, _missing = wifi.match_associated_ssids(
                    [stronger_ssid, weaker_ssid],
                    use_dumpsys_for_missing=True,
                )
                if found:
                    selected = found[0]
                    break
                time.sleep(1.0)
            _code, score_out, score_err = wifi.adb.shell_line(
                "logcat -d -v threadtime | grep -i -E "
                "'final score|candidate|rssi score|turbolink'"
            )
            score_log = "\n".join(
                part for part in (score_out, score_err) if part
            ).strip()
            scores = parse_candidate_scores(score_log)
            if selected == stronger_ssid and all(
                ssid in scores for ssid in (stronger_ssid, weaker_ssid)
            ):
                break
            print(
                f"[{summary}] selection attempt {attempt}/3 incomplete: "
                f"selected={selected!r}, scores={sorted(scores)!r}"
            )
        if selected != stronger_ssid:
            pytest.fail(
                f"{summary}: selected {selected!r}, expected stronger "
                f"candidate {stronger_ssid!r}"
            )
        allure.attach(
            score_log or "<no score log>",
            f"{summary}-candidate-score.log",
            allure.attachment_type.TEXT,
        )
        assert_candidate_score_selection(
            score_log,
            stronger_ssid=stronger_ssid,
            weaker_ssid=weaker_ssid,
            summary=summary,
            expected_rssi_scores=expected_rssi_scores,
            require_equal_final_scores=require_equal_final_scores,
        )
        print(
            f"[{summary}] selected {stronger_ssid!r}; "
            f"RSSI={stronger_rssi}/{weaker_rssi} dBm with equal final scores"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original_attenuations[channel])
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        for ssid in (stronger_ssid, weaker_ssid):
            if ssid not in original_saved:
                network_id = wifi.find_network_id_by_ssid(ssid)
                if network_id:
                    wifi.forget_network(network_id)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify a WLAN restart within 10 seconds skips network selection")
def run_autoscan_recent_selection_skip_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    current_entry_id: str = "hyperwifi_lab_miniap1",
    candidate_entry_id: str = "hyperwifi_lab_miniap2",
    current_target_rssi: int = -70,
    candidate_target_rssi: int = -65,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: attenuator_device is not configured")
    current_entry = get_wifi_list_entry(wifi_yaml, entry_id=current_entry_id)
    candidate_entry = get_wifi_list_entry(wifi_yaml, entry_id=candidate_entry_id)
    if not current_entry or not candidate_entry:
        pytest.skip(f"{summary}: miniAP1/miniAP2 WiFi profiles are missing")

    current_ssid = str(current_entry.get("ssid") or "")
    candidate_ssid = str(candidate_entry.get("ssid") or "")
    current_channel = attenuator.channel_for(hyper=True, ap_index=1)
    candidate_channel = attenuator.channel_for(hyper=True, ap_index=2)
    original_attenuations = dict(attenuator.read_attenuations())
    original_saved = set(wifi.list_saved_networks())

    def candidate_rssi() -> int | None:
        run_shell_cmd("cmd wifi start-scan")
        time.sleep(2.0)
        values = scan_result_rssis(
            run_shell_cmd("cmd wifi list-scan-results"),
            candidate_ssid,
        )
        return max(values) if values else None

    try:
        attenuator.set_attenuation(current_channel, 20)
        attenuator.set_attenuation(candidate_channel, 20)
        time.sleep(4.0)
        for entry, ssid in (
            (candidate_entry, candidate_ssid),
            (current_entry, current_ssid),
        ):
            if not wifi.ensure_wifi_connected(
                cast(WiFiEntry, entry),
                max_attempts=3,
                settle_sec=2.0,
            ):
                pytest.fail(f"{summary}: failed to save/connect {ssid!r}")

        _current_attenuation, current_rssi = tune_attenuation_for_rssi(
            attenuator,
            current_channel,
            current_target_rssi,
            _hyper_rssi_reader(run_shell_cmd),
            settle_sec=3.0,
            tolerance_db=2,
        )
        _candidate_attenuation, candidate_rssi_value = tune_attenuation_for_rssi(
            attenuator,
            candidate_channel,
            candidate_target_rssi,
            candidate_rssi,
            settle_sec=3.0,
            tolerance_db=2,
        )
        if (
            current_rssi is None
            or candidate_rssi_value is None
            or candidate_rssi_value <= current_rssi
            or candidate_rssi_value < -70
        ):
            pytest.fail(
                f"{summary}: RSSI precondition failed: current={current_rssi}, "
                f"candidate={candidate_rssi_value} dBm"
            )

        wifi.open_wifi_settings()
        wifi.adb.shell_line("logcat -c")
        if not wifi.set_wifi_enabled(False, settle_sec=1.0):
            pytest.fail(f"{summary}: failed to disable WLAN")
        time.sleep(3.0)
        if not wifi.set_wifi_enabled(True, settle_sec=1.0):
            pytest.fail(f"{summary}: failed to enable WLAN")

        deadline = time.monotonic() + 30.0
        selected = ""
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids(
                [current_ssid, candidate_ssid],
                use_dumpsys_for_missing=True,
            )
            if found:
                selected = found[0]
                break
            time.sleep(1.0)
        _code, log_out, log_err = wifi.adb.shell_line(
            "logcat -d -v threadtime | grep -i -E "
            "'Too short since last network selection|network selection|candidate'"
        )
        selection_log = "\n".join(
            part for part in (log_out, log_err) if part
        ).strip()
        allure.attach(
            selection_log or "<no network-selection log>",
            f"{summary}-recent-selection-skip.log",
            allure.attachment_type.TEXT,
        )
        if selected != current_ssid:
            pytest.fail(
                f"{summary}: selected {selected!r}, expected current network "
                f"{current_ssid!r}"
            )
        assert_recent_network_selection_skipped(
            selection_log,
            interface="wlan1",
            summary=summary,
        )
        print(
            f"[{summary}] retained {current_ssid!r}; "
            f"RSSI={current_rssi}/{candidate_rssi_value} dBm"
        )
    finally:
        attenuator.set_attenuation(
            current_channel,
            original_attenuations[current_channel],
        )
        attenuator.set_attenuation(
            candidate_channel,
            original_attenuations[candidate_channel],
        )
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        for ssid in (current_ssid, candidate_ssid):
            if ssid not in original_saved:
                network_id = wifi.find_network_id_by_ssid(ssid)
                if network_id:
                    wifi.forget_network(network_id)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("Verify scan and reconnect when WLAN is enabled in airplane mode")
def run_autoscan_airplane_wlan_enable_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    target = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd)
    original_airplane = run_shell_cmd(
        "settings get global airplane_mode_on"
    ).strip()
    try:
        if original_airplane == "1":
            _set_airplane_mode(run_shell_cmd, False)
        _set_airplane_mode(run_shell_cmd, True)
        if not wifi.set_wifi_enabled(False):
            pytest.fail(f"{summary}: failed to disable WLAN in airplane mode")

        def enable_wlan() -> None:
            if not wifi.set_wifi_enabled(True):
                pytest.fail(f"{summary}: failed to enable WLAN in airplane mode")

        _observe_single_scan_after_action(
            summary,
            wifi.adb,
            enable_wlan,
            max_latency_sec=6.0,
            duplicate_window_sec=1.5,
        )
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids([target])
            if found:
                return
            time.sleep(0.5)
        pytest.fail(f"{summary}: scan completed but WLAN did not reconnect to {target!r}")
    finally:
        _set_airplane_mode(run_shell_cmd, original_airplane == "1")
