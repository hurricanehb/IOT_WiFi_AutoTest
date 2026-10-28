"""Network-selection candidate filtering scenario runners."""
from __future__ import annotations

import time
from typing import Callable

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.testdata_loader.android.wifi_data import get_wifi_list_entry


def _require_entry(wifi_yaml: dict, entry_id: str, summary: str) -> dict:
    entry = get_wifi_list_entry(wifi_yaml, entry_id=entry_id)
    if not entry:
        pytest.skip(f"{summary}: missing WiFi profile {entry_id!r}")
    return entry


@allure.step("Verify user-disconnected SSIDs are not nominated again")
def run_user_disconnect_candidate_filter_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    first_entry_id: str = "hyperwifi_lab_miniap1",
    second_entry_id: str = "hyperwifi_lab_miniap2",
    observation_sec: float = 10.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    first = _require_entry(wifi_yaml, first_entry_id, summary)
    second = _require_entry(wifi_yaml, second_entry_id, summary)
    first_ssid = str(first.get("ssid") or "")
    second_ssid = str(second.get("ssid") or "")
    if not first_ssid or not second_ssid:
        pytest.fail(f"{summary}: candidate SSID is empty")

    try:
        for entry, ssid in ((first, first_ssid), (second, second_ssid)):
            if not wifi.connect_wifi_block(entry):
                pytest.fail(f"{summary}: failed to connect {ssid!r}")
            assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
            wifi.adb.shell_line("cmd wifi disconnect")
            if not wifi.wait_until_disconnected(timeout=10.0, interval=0.5):
                pytest.fail(f"{summary}: failed to user-disconnect {ssid!r}")

        wifi.adb.shell_line("logcat -c")
        time.sleep(observation_sec)
        found, _missing = wifi.match_associated_ssids(
            [first_ssid, second_ssid],
            use_dumpsys_for_missing=True,
        )
        if found:
            pytest.fail(
                f"{summary}: user-disconnected network was nominated again; "
                f"associated={found!r}"
            )
        _code, out, err = wifi.adb.shell_line(
            "logcat -d -v threadtime | grep -i -E 'candidate|network selection'"
        )
        log_text = "\n".join(part for part in (out, err) if part).strip()
        allure.attach(
            log_text or "<no candidate log>",
            f"{summary}-candidate-filter.log",
            allure.attachment_type.TEXT,
        )
    finally:
        wifi.adb.shell_line("cmd wifi disconnect")
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)