"""HyperWiFi low-power state scenario runners."""
from __future__ import annotations

import re
import time
import os
from typing import Callable

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.dual_link import dual_link_legs, wait_for_link_ssid
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.testdata_loader.android.wifi_data import (
    get_dual_wifi_entry,
    get_wifi_list_entry,
)


def _hyper_entry(wifi_yaml: dict, summary: str) -> dict:
    entry = get_wifi_list_entry(wifi_yaml, entry_id="hyperwifi_lab_miniap1")
    if not entry:
        pytest.skip(f"{summary}: missing hyperwifi_lab_miniap1 profile")
    return entry


def _dual_entry(wifi_yaml: dict, summary: str) -> dict:
    entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
    if not entry:
        pytest.skip(f"{summary}: missing dual_wifi_24g_hyperwifi_us profile")
    return entry


def _shell_text(wifi: WiFiControl, command: str) -> str:
    _code, out, err = wifi.adb.shell_line(command)
    return "\n".join(part for part in (out, err) if part).strip()


def _power_snapshot(wifi: WiFiControl) -> tuple[str, str]:
    return (
        _shell_text(wifi, "cli_app show ps_status"),
        _shell_text(wifi, "cli_app show idle_mode"),
    )


def _assert_contains(
    summary: str,
    value: str,
    patterns: tuple[str, ...],
    label: str,
) -> None:
    lower = value.lower()
    if not any(re.search(pattern, lower) for pattern in patterns):
        pytest.fail(f"{summary}: {label} missing {patterns!r}; actual={value!r}")


def _assert_idle_state(summary: str, wifi: WiFiControl) -> None:
    ps_status, idle_mode = _power_snapshot(wifi)
    _assert_contains(summary, ps_status, (r"sleep",), "ps_status idle state")
    _assert_contains(summary, idle_mode, (r"idle",), "idle_mode")


def _assert_active_state(summary: str, wifi: WiFiControl) -> None:
    ps_status, idle_mode = _power_snapshot(wifi)
    _assert_contains(summary, ps_status, (r"wake",), "ps_status active state")
    _assert_contains(summary, idle_mode, (r"no.?idle|active|wake"), "idle_mode")


def _wait_for_power_state(
    summary: str,
    wifi: WiFiControl,
    *,
    idle: bool,
    timeout: float = 12.0,
) -> None:
    deadline = time.monotonic() + timeout
    last_snapshot = ("", "")
    while time.monotonic() < deadline:
        last_snapshot = _power_snapshot(wifi)
        ps_status, idle_mode = (value.lower() for value in last_snapshot)
        if idle and "sleep" in ps_status and "idle" in idle_mode:
            return
        if not idle and "wake" in ps_status and re.search(
            r"no.?idle|active|wake", idle_mode
        ):
            return
        time.sleep(0.5)
    expected = "sleep/idle" if idle else "wake/active"
    pytest.fail(
        f"{summary}: power state did not reach {expected}; actual={last_snapshot!r}"
    )


def _set_airplane_power_state(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    enabled: bool,
) -> None:
    if enabled and not wifi.set_wifi_enabled(False, settle_sec=2.0):
        pytest.fail(f"{summary}: failed to disable WLAN before airplane mode")
    run_shell_cmd(
        f"cmd connectivity airplane-mode {'enable' if enabled else 'disable'}"
    )
    actual = run_shell_cmd("settings get global airplane_mode_on").strip()
    expected = "1" if enabled else "0"
    if actual != expected:
        pytest.fail(
            f"{summary}: airplane mode expected {expected}, actual={actual!r}"
        )
    if not enabled and not wifi.set_wifi_enabled(True, settle_sec=2.0):
        pytest.fail(f"{summary}: failed to enable WLAN after airplane mode")


def _connect_dual_with_active_checks(
    summary: str,
    wifi: WiFiControl,
    entry: dict,
    order: tuple[str, str],
) -> tuple[dict, dict]:
    traditional, hyper = dual_link_legs(entry)
    legs = {"wifi": traditional, "hyper": hyper}
    wifi.forget_dual_wifi_entry(entry)
    for link in order:
        block = legs[link]
        ssid = str(block.get("ssid") or "")
        if not wifi.connect_wifi_block(block):
            pytest.fail(f"{summary}: failed to connect {link} SSID {ssid!r}")
        wait_for_link_ssid(wifi, ssid)
        _assert_active_state(summary, wifi)
    ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=45.0)
    if not ok:
        pytest.fail(f"{summary}: dual-link setup failed found={found!r} missing={missing!r}")
    return traditional, hyper


def _forget_link(
    summary: str,
    wifi: WiFiControl,
    target: dict,
    remaining: dict,
) -> None:
    target_ssid = str(target.get("ssid") or "")
    remaining_ssid = str(remaining.get("ssid") or "")
    network_id = wifi.find_network_id_by_ssid(target_ssid)
    if not network_id or not wifi.forget_network(network_id):
        pytest.fail(f"{summary}: failed to forget {target_ssid!r}")
    deadline = time.monotonic() + 15.0
    while time.monotonic() < deadline:
        found, _missing = wifi.match_associated_ssids([target_ssid, remaining_ssid])
        if target_ssid not in found and remaining_ssid in found:
            return
        time.sleep(0.5)
    pytest.fail(
        f"{summary}: link state did not settle after forgetting {target_ssid!r}"
    )


@allure.step("Verify HyperWiFi stays active during dual-WiFi screen-on operations")
def run_hyperwifi_dual_screen_on_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    operation: str,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    entry = _dual_entry(wifi_yaml, summary)
    order = ("hyper", "wifi") if operation == "connect_hyper_first" else ("wifi", "hyper")
    traditional, hyper = _connect_dual_with_active_checks(summary, wifi, entry, order)
    if operation == "disconnect_wifi":
        _forget_link(summary, wifi, traditional, hyper)
    elif operation == "disconnect_hyper":
        _forget_link(summary, wifi, hyper, traditional)
    elif operation not in {"connect_wifi_first", "connect_hyper_first", "observe"}:
        raise ValueError(f"unsupported dual screen-on operation: {operation!r}")
    time.sleep(3.0)
    _assert_active_state(summary, wifi)


def _assert_screen_off_mode(
    summary: str,
    wifi: WiFiControl,
    *,
    powersave: bool,
    expected_ssids: list[str],
    observation_sec: float = 20.0,
) -> None:
    wifi.adb.keyevent("KEYCODE_HOME")
    wifi.adb.shell_line("dmesg -c")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    deadline = time.monotonic() + observation_sec
    dmesg = ""
    while time.monotonic() < deadline:
        dmesg = _shell_text(
            wifi, "dmesg | grep -iE 'setting ps state|ps mode|ps state'"
        )
        ps_status, idle_mode = _power_snapshot(wifi)
        if powersave:
            reached = "sleep" in ps_status.lower() and bool(
                re.search(r"deep(?:sleep[_ ]|[_ ])tim", dmesg.lower())
            )
        else:
            reached = (
                "sleep" in ps_status.lower()
                and "idle" in idle_mode.lower()
                and bool(re.search(r"deep(?:sleep)?[_ ]nontim", dmesg.lower()))
            )
        if reached:
            break
        time.sleep(1.0)
    allure.attach(dmesg or "<empty>", f"{summary}-dmesg.txt", allure.attachment_type.TEXT)
    if powersave:
        _assert_contains(summary, ps_status, (r"sleep",), "ps_status sleep state")
        _assert_contains(
            summary,
            dmesg,
            (r"deep(?:sleep[_ ]|[_ ])tim",),
            "dmesg PowerSave mode",
        )
    else:
        _assert_idle_state(summary, wifi)
        _assert_contains(
            summary,
            dmesg,
            (r"deep(?:sleep)?[_ ]nontim",),
            "dmesg IDLE mode",
        )
    found, missing = wifi.match_associated_ssids(expected_ssids)
    if missing:
        pytest.fail(
            f"{summary}: expected links disconnected while screen off; "
            f"found={found!r} missing={missing!r}"
        )


@allure.step("Verify HyperWiFi power state across dual-WiFi screen transitions")
def run_hyperwifi_dual_screen_transition_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    operation: str,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    entry = _dual_entry(wifi_yaml, summary)
    traditional, hyper = dual_link_legs(entry)
    traditional_ssid = str(traditional.get("ssid") or "")
    hyper_ssid = str(hyper.get("ssid") or "")

    try:
        if operation == "wifi_only_sleep_wake":
            wifi.forget_dual_wifi_entry(entry)
            if not wifi.connect_wifi_block(traditional):
                pytest.fail(f"{summary}: failed to connect traditional WiFi")
            wait_for_link_ssid(wifi, traditional_ssid)
            _assert_active_state(summary, wifi)
            _assert_screen_off_mode(
                summary, wifi, powersave=False, expected_ssids=[traditional_ssid]
            )
        else:
            traditional, hyper = _connect_dual_with_active_checks(
                summary, wifi, entry, ("wifi", "hyper")
            )
            if operation == "disconnect_wifi_then_sleep":
                _forget_link(summary, wifi, traditional, hyper)
                _assert_active_state(summary, wifi)
                _assert_screen_off_mode(
                    summary, wifi, powersave=True, expected_ssids=[hyper_ssid]
                )
            elif operation == "disconnect_hyper_then_sleep":
                _forget_link(summary, wifi, hyper, traditional)
                _assert_active_state(summary, wifi)
                _assert_screen_off_mode(
                    summary, wifi, powersave=False, expected_ssids=[traditional_ssid]
                )
            elif operation == "dual_sleep_wake":
                _assert_screen_off_mode(
                    summary,
                    wifi,
                    powersave=True,
                    expected_ssids=[traditional_ssid, hyper_ssid],
                )
            else:
                raise ValueError(f"unsupported dual screen operation: {operation!r}")

        if operation in {"dual_sleep_wake", "wifi_only_sleep_wake"}:
            wifi.adb.keyevent("KEYCODE_WAKEUP")
            wifi.adb.shell("wm", "dismiss-keyguard")
            _wait_for_power_state(summary, wifi, idle=False)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Run repeated HyperWiFi screen state cycles")
def run_hyperwifi_screen_cycle_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    connected: bool,
    cycles: int | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    total_cycles = cycles or int(os.getenv("HALOWLP_SCREEN_CYCLES", "20"))
    if total_cycles <= 0:
        pytest.fail(f"{summary}: HALOWLP_SCREEN_CYCLES must be positive")
    entry = _hyper_entry(wifi_yaml, summary)
    if connected:
        if not wifi.connect_wifi_block(entry):
            pytest.fail(f"{summary}: failed to connect HyperWiFi")
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    else:
        wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        wifi.set_wifi_enabled(True, settle_sec=1.0)

    try:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        for cycle in range(1, total_cycles + 1):
            wifi.adb.keyevent("KEYCODE_HOME")
            wifi.adb.keyevent("KEYCODE_SLEEP")
            time.sleep(1.0)
            wifi.adb.keyevent("KEYCODE_WAKEUP")
            wifi.adb.shell("wm", "dismiss-keyguard")
            time.sleep(1.0)
            if connected:
                found, _missing = wifi.match_associated_ssids(
                    [str(entry.get("ssid") or "")]
                )
                if not found:
                    pytest.fail(f"{summary}: HyperWiFi disconnected at cycle {cycle}")
            if cycle % 5 == 0:
                _assert_active_state(summary, wifi)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify connected HyperWiFi stays awake while the screen is on")
def run_hyperwifi_screen_on_active_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 5.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    target_ssid = str(entry.get("ssid") or "")
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    time.sleep(observation_sec)
    ps_status, idle_mode = _power_snapshot(wifi)
    dmesg = _shell_text(wifi, "dmesg | grep -iE 'ps mode|ps state|setting ps state'")
    allure.attach(ps_status or "<empty>", f"{summary}-ps_status.txt", allure.attachment_type.TEXT)
    allure.attach(idle_mode or "<empty>", f"{summary}-idle_mode.txt", allure.attachment_type.TEXT)
    allure.attach(dmesg or "<empty>", f"{summary}-dmesg.txt", allure.attachment_type.TEXT)
    _assert_contains(summary, ps_status, (r"wake",), "ps_status")
    _assert_contains(summary, dmesg, (r"active|wake",), "dmesg active state")
    _assert_contains(summary, idle_mode, (r"no.?idle|active|wake" ,), "idle_mode")
    found, _missing = wifi.match_associated_ssids([target_ssid])
    if target_ssid not in found:
        pytest.fail(f"{summary}: HyperWiFi disconnected during observation")


@allure.step("Verify an unconnected HyperWiFi device stays awake while screen is on")
def run_hyperwifi_unconnected_screen_on_active_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
    wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
    wifi.set_wifi_enabled(True, settle_sec=1.0)
    time.sleep(3.0)
    _assert_active_state(summary, wifi)


@allure.step("Verify a user-disconnected HyperWiFi device stays awake")
def run_hyperwifi_disconnect_screen_on_active_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.shell_line("cmd wifi disconnect")
    if not wifi.wait_until_disconnected(timeout=10.0, interval=0.5):
        pytest.fail(f"{summary}: failed to disconnect HyperWiFi")
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    time.sleep(3.0)
    _assert_active_state(summary, wifi)


@allure.step("Verify connected HyperWiFi enters PowerSave after screen off")
def run_hyperwifi_screen_off_powersave_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 20.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    target_ssid = str(entry.get("ssid") or "")
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    wifi.adb.keyevent("KEYCODE_HOME")
    time.sleep(2.0)
    wifi.adb.shell_line("dmesg -c")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    try:
        deadline = time.monotonic() + observation_sec
        dmesg = ""
        ps_status = ""
        idle_mode = ""
        while time.monotonic() < deadline:
            dmesg = _shell_text(wifi, "dmesg | grep -iE 'setting ps state|ps mode|ps state'")
            ps_status, idle_mode = _power_snapshot(wifi)
            if re.search(r"deep(?:sleep[_ ]|[_ ])tim", dmesg.lower()) and re.search(
                r"sleep", dmesg.lower()
            ):
                break
            time.sleep(1.0)
        allure.attach(dmesg or "<empty>", f"{summary}-dmesg.txt", allure.attachment_type.TEXT)
        allure.attach(ps_status or "<empty>", f"{summary}-ps_status.txt", allure.attachment_type.TEXT)
        allure.attach(idle_mode or "<empty>", f"{summary}-idle_mode.txt", allure.attachment_type.TEXT)
        _assert_contains(
            summary,
            dmesg,
            (r"deep(?:sleep[_ ]|[_ ])tim",),
            "dmesg PowerSave mode",
        )
        _assert_contains(summary, dmesg, (r"sleep",), "dmesg sleep state")
        found, _missing = wifi.match_associated_ssids([target_ssid])
        if target_ssid not in found:
            pytest.fail(f"{summary}: HyperWiFi disconnected while screen was off")
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify no-saved-network HyperWiFi enters IDLE after screen off")
def run_hyperwifi_no_saved_screen_off_idle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 20.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
    wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
    if wifi.has_saved_networks():
        pytest.fail(f"{summary}: saved networks remain before screen-off check")
    if not wifi.set_wifi_enabled(True, settle_sec=1.0):
        pytest.fail(f"{summary}: failed to enable WLAN")
    wifi.adb.keyevent("KEYCODE_HOME")
    wifi.adb.shell_line("dmesg -c")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    try:
        deadline = time.monotonic() + observation_sec
        dmesg = ""
        while time.monotonic() < deadline:
            dmesg = _shell_text(
                wifi, "dmesg | grep -iE 'setting ps state|ps mode|ps state'"
            )
            ps_status, idle_mode = _power_snapshot(wifi)
            if (
                "sleep" in ps_status.lower()
                and "idle" in idle_mode.lower()
                and re.search(r"deep(?:sleep)?[_ ]nontim", dmesg.lower())
            ):
                break
            time.sleep(1.0)
        allure.attach(dmesg or "<empty>", f"{summary}-dmesg.txt", allure.attachment_type.TEXT)
        _assert_idle_state(summary, wifi)
        _assert_contains(
            summary,
            dmesg,
            (r"deep(?:sleep)?[_ ]nontim",),
            "dmesg no-PNO idle mode",
        )
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify a disconnected HyperWiFi device enters idle after screen off")
def run_hyperwifi_disconnected_screen_off_idle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    clear_saved: bool,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.shell_line("cmd wifi disconnect")
    if not wifi.wait_until_disconnected(timeout=10.0, interval=0.5):
        pytest.fail(f"{summary}: failed to disconnect HyperWiFi")
    if clear_saved:
        network_id = wifi.find_network_id_by_ssid(str(entry.get("ssid") or ""))
        if network_id and not wifi.forget_network(network_id):
            pytest.fail(f"{summary}: failed to forget HyperWiFi network")
    wifi.adb.keyevent("KEYCODE_HOME")
    wifi.adb.shell_line("dmesg -c")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    try:
        deadline = time.monotonic() + 12.0
        while time.monotonic() < deadline:
            ps_status, idle_mode = _power_snapshot(wifi)
            if "sleep" in ps_status.lower() and "idle" in idle_mode.lower():
                break
            time.sleep(1.0)
        _assert_idle_state(summary, wifi)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify disabling WLAN enters HyperWiFi idle state")
def run_hyperwifi_wlan_off_idle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    try:
        if not wifi.set_wifi_enabled(False, settle_sec=2.0):
            pytest.fail(f"{summary}: failed to disable WLAN")
        _assert_idle_state(summary, wifi)
    finally:
        wifi.set_wifi_enabled(True, settle_sec=1.0)


@allure.step("Run repeated HyperWiFi WLAN power-state cycles")
def run_hyperwifi_wlan_cycle_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    cycles: int | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    total_cycles = cycles or int(os.getenv("HALOWLP_WLAN_CYCLES", "20"))
    if total_cycles <= 0:
        pytest.fail(f"{summary}: HALOWLP_WLAN_CYCLES must be positive")
    entry = _hyper_entry(wifi_yaml, summary)
    target_ssid = str(entry.get("ssid") or "")
    if not wifi.ensure_wifi_connected(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")

    try:
        for cycle in range(1, total_cycles + 1):
            if not wifi.set_wifi_enabled(False, settle_sec=2.0):
                pytest.fail(f"{summary}: failed to disable WLAN at cycle {cycle}")
            _assert_idle_state(summary, wifi)

            if not wifi.set_wifi_enabled(True, settle_sec=2.0):
                pytest.fail(f"{summary}: failed to enable WLAN at cycle {cycle}")
            deadline = time.monotonic() + 15.0
            while time.monotonic() < deadline:
                found, _missing = wifi.match_associated_ssids([target_ssid])
                if target_ssid in found:
                    break
                time.sleep(0.5)
            else:
                pytest.fail(f"{summary}: HyperWiFi did not reconnect at cycle {cycle}")
            _assert_active_state(summary, wifi)
    finally:
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify an unconnected device enters HyperWiFi idle after WLAN off")
def run_hyperwifi_unconnected_wlan_off_idle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
    wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
    wifi.set_wifi_enabled(True, settle_sec=1.0)
    try:
        if not wifi.set_wifi_enabled(False, settle_sec=2.0):
            pytest.fail(f"{summary}: failed to disable WLAN")
        _assert_idle_state(summary, wifi)
    finally:
        wifi.set_wifi_enabled(True, settle_sec=1.0)


@allure.step("Verify an unconnected HyperWiFi device exits idle after screen wake")
def run_hyperwifi_unconnected_screen_wake_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    observation_sec: float = 8.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")
    wifi.disconnect_all(settle_sec=0.5, max_rounds=2, post_wait_sec=2.0)
    wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
    wifi.set_wifi_enabled(True, settle_sec=1.0)
    wifi.adb.keyevent("KEYCODE_HOME")
    wifi.adb.shell_line("dmesg -c")
    wifi.adb.keyevent("KEYCODE_SLEEP")
    try:
        deadline = time.monotonic() + observation_sec
        dmesg = ""
        while time.monotonic() < deadline:
            dmesg = _shell_text(wifi, "dmesg | grep -iE 'setting ps state|ps mode|ps state'")
            ps_status, idle_mode = _power_snapshot(wifi)
            if re.search(r"sleep", ps_status.lower()) and re.search(
                r"idle", idle_mode.lower()
            ):
                break
            time.sleep(1.0)
        allure.attach(dmesg or "<empty>", f"{summary}-dmesg.txt", allure.attachment_type.TEXT)
        ps_status, idle_mode = _power_snapshot(wifi)
        allure.attach(ps_status or "<empty>", f"{summary}-ps_status.txt", allure.attachment_type.TEXT)
        allure.attach(idle_mode or "<empty>", f"{summary}-idle_mode.txt", allure.attachment_type.TEXT)
        _assert_contains(summary, ps_status, (r"sleep",), "ps_status idle state")
        _assert_contains(summary, idle_mode, (r"idle",), "idle_mode")

        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        time.sleep(2.0)
        _assert_active_state(summary, wifi)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify airplane mode enters and exits HyperWiFi idle state")
def run_hyperwifi_airplane_cycle_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    try:
        _set_airplane_power_state(summary, run_shell_cmd, wifi, enabled=True)
        _wait_for_power_state(summary, wifi, idle=True)
        _set_airplane_power_state(summary, run_shell_cmd, wifi, enabled=False)
        _wait_for_power_state(summary, wifi, idle=False)
    finally:
        run_shell_cmd("cmd connectivity airplane-mode disable")
        wifi.set_wifi_enabled(True, settle_sec=1.0)


@allure.step("Run repeated HyperWiFi airplane-mode power-state cycles")
def run_hyperwifi_airplane_cycle_stability_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    cycles: int | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    total_cycles = cycles or int(os.getenv("HALOWLP_AIRPLANE_CYCLES", "20"))
    if total_cycles <= 0:
        pytest.fail(f"{summary}: HALOWLP_AIRPLANE_CYCLES must be positive")
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.ensure_wifi_connected(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    wifi.adb.keyevent("KEYCODE_WAKEUP")
    wifi.adb.shell("wm", "dismiss-keyguard")

    try:
        for cycle in range(1, total_cycles + 1):
            _set_airplane_power_state(summary, run_shell_cmd, wifi, enabled=True)
            try:
                _wait_for_power_state(summary, wifi, idle=True)
            except pytest.fail.Exception as exc:
                pytest.fail(f"{summary}: airplane enable failed at cycle {cycle}: {exc}")

            _set_airplane_power_state(summary, run_shell_cmd, wifi, enabled=False)
            try:
                _wait_for_power_state(summary, wifi, idle=False)
            except pytest.fail.Exception as exc:
                pytest.fail(f"{summary}: airplane disable failed at cycle {cycle}: {exc}")
            if not wifi.ensure_wifi_connected(entry, max_attempts=2, settle_sec=2.0):
                pytest.fail(
                    f"{summary}: HyperWiFi did not reconnect after cycle {cycle}"
                )
    finally:
        run_shell_cmd("cmd connectivity airplane-mode disable")
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")


@allure.step("Verify screen wake exits HyperWiFi PowerSave")
def run_hyperwifi_screen_wake_active_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = _hyper_entry(wifi_yaml, summary)
    if not wifi.connect_wifi_block(entry):
        pytest.fail(f"{summary}: failed to connect HyperWiFi")
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    try:
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(3.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        time.sleep(2.0)
        _assert_active_state(summary, wifi)
    finally:
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")