import pytest

from core.libs.android.wifi_scenarios.ip_reachability import (
    parse_neighbor_event_epochs,
)
from core.libs.android.wifi_scenarios.network_204 import (
    parse_probe_event_epochs,
)
from core.libs.android.wifi_control.ssid_parsers import (
    bssid_from_wifi_status,
    scan_result_rssi_for_bssid,
    scan_result_rssis,
    scan_result_ssids,
    ssid_match,
)


def test_ssid_match_requires_exact_normalized_value() -> None:
    assert ssid_match('"Lab WiFi"', "Lab WiFi")
    assert not ssid_match("Lab", "LabGuest")


def test_scan_result_ssids_extracts_single_character_and_spaced_names() -> None:
        scan = """BSSID Frequency RSSI Age(sec) SSID Flags
    54:f6:e2:e9:4a:f7 5180 -27(0:-27) 6.600 0 [WPA2-PSK-CCMP-128][ESS]
    3c:a3:7e:4c:31:a4 5300 -77(0:-77) 2.291 Lab WiFi [RSN-PSK-CCMP-128][ESS]
"""

        assert scan_result_ssids(scan) == ["0", "Lab WiFi"]


def test_scan_result_rssis_returns_all_matching_radios() -> None:
    scan = """\
54:f6:e2:e9:4a:40 2412 -66(0:-66) 1s Lab WiFi [WPA2-PSK-CCMP][ESS]
54:f6:e2:e9:4a:50 5180 -74 2s Lab WiFi [WPA2-PSK-CCMP][ESS]
54:f6:e2:e9:4a:60 5200 -50 1s Other [ESS]
"""

    assert scan_result_rssis(scan, "Lab WiFi") == [-66, -74]


def test_bssid_helpers_track_one_radio() -> None:
    status = 'WifiInfo: SSID: "Lab WiFi", BSSID: 54:F6:E2:E9:4A:40, RSSI: -66'
    scan = """\
54:f6:e2:e9:4a:40 2412 -78(0:-78) 1s Lab WiFi [WPA2-PSK-CCMP][ESS]
54:f6:e2:e9:5a:40 2412 -50(0:-50) 1s Lab WiFi [WPA2-PSK-CCMP][ESS]
"""

    bssid = bssid_from_wifi_status(status)

    assert bssid == "54:f6:e2:e9:4a:40"
    assert scan_result_rssi_for_bssid(scan, bssid) == -78


@pytest.mark.parametrize(
    ("parser", "event"),
    [
        (parse_neighbor_event_epochs, "IpReachabilityMonitor probe"),
        (parse_probe_event_epochs, "NetworkMonitor probe"),
    ],
)
def test_logcat_event_epochs_handle_year_rollover(parser, event: str) -> None:
    log_text = (
        f"12-31 23:59:59.000  100  100 I Test: {event}\n"
        f"01-01 00:00:01.000  100  100 I Test: {event}"
    )

    assert parser(log_text) == [0.0, 2.0]