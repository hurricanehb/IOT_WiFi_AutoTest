from unittest.mock import Mock, call

from PIL import Image

from core.libs.android.wifi_scenarios.dual_link import (
    connect_dual_link_in_order,
    primary_link_from_status,
)
from core.libs.android.wifi_scenarios.dual_link_failover import (
    assert_backup_score_leads,
    candidate_final_scores,
    link_bssid_from_status,
    link_radio_metrics,
    parse_link_roles,
)
from core.libs.android.wifi_scenarios.settings.primary_backup_icon import (
    has_orange_highlight,
    settings_ssid_rows,
    ssid_title_bounds,
)


def test_primary_link_from_status_supports_real_hyper_interface() -> None:
    status = """
==== ClientModeManager instance: ConcreteClientModeManager{id=1 iface=hyper0 role=ROLE_CLIENT_PRIMARY} ====
==== ClientModeManager instance: ConcreteClientModeManager{id=2 iface=wlan0 role=ROLE_CLIENT_SECONDARY_LONG_LIVED} ====
"""

    assert primary_link_from_status(status) == "hyper"


def test_failover_log_roles_support_real_hyper_interface() -> None:
    log_text = """
setrole ifname
hyper0 role: ROLE_CLIENT_PRIMARY
wlan0 role: ROLE_CLIENT_SECONDARY_LONG_LIVED
"""

    assert parse_link_roles(log_text) == {
        "hyper0": "ROLE_CLIENT_PRIMARY",
        "wlan0": "ROLE_CLIENT_SECONDARY_LONG_LIVED",
    }


def test_link_radio_metrics_reads_only_requested_interface() -> None:
    status = """
==== ClientModeManager instance: ConcreteClientModeManager{id=1 iface=wlan0 role=ROLE_CLIENT_PRIMARY} ====
WifiInfo: RSSI: -71, Frequency: 5180MHz
==== ClientModeManager instance: ConcreteClientModeManager{id=2 iface=hyper0 role=ROLE_CLIENT_SECONDARY_LONG_LIVED} ====
WifiInfo: RSSI: -60, Frequency: 925MHz
"""

    assert link_radio_metrics(status, "wlan0") == (-71, 5180)
    assert link_radio_metrics(status, "hyper0") == (-60, 925)
    assert link_bssid_from_status(
        status.replace("RSSI: -71", "BSSID: 54:f6:e2:e9:4a:57, RSSI: -71"),
        "wlan0",
    ) == "54:f6:e2:e9:4a:57"


def test_backup_score_lead_uses_latest_score_per_candidate() -> None:
    log_text = """
ThroughputScorer: Score for candidate: SSID: "WiFi" rssi: -73 final score: 3500
ThroughputScorer: Score for candidate: SSID: "Hyper" rssi: -70 final score: 3610
ThroughputScorer: Score for candidate: SSID: "Hyper" rssi: -70 final score: 3610
"""

    assert candidate_final_scores(log_text) == {"WiFi": 3500, "Hyper": 3610}
    assert assert_backup_score_leads(
        log_text,
        primary_ssid="WiFi",
        backup_ssid="Hyper",
        summary="case",
    ) == (3500, 3610)


def test_connect_dual_link_in_requested_order() -> None:
    wifi = Mock()
    wifi.match_associated_ssids.side_effect = lambda ssids, **_kwargs: (ssids, [])
    wifi.ensure_dual_wifi_connected.return_value = (
        True,
        ["Traditional", "Hyper"],
        [],
    )
    entry = {
        "traditional_wifi": {"ssid": "Traditional", "encrypt": "OPEN"},
        "hyper_wifi": {"ssid": "Hyper", "encrypt": "OPEN"},
    }

    connect_dual_link_in_order("case", wifi, entry, ("hyper", "wifi"))

    assert wifi.connect_wifi_block.call_args_list == [
        call(entry["hyper_wifi"]),
        call(entry["traditional_wifi"]),
    ]
    wifi.forget_dual_wifi_entry.assert_called_once_with(entry)


def test_settings_ssid_rows_uses_clickable_container_bounds() -> None:
    hierarchy = """
<hierarchy><node>
  <node clickable="true" bounds="[0,286][720,431]">
    <node text="Primary" bounds="[40,318][250,361]" />
  </node>
  <node clickable="true" bounds="[0,431][720,576]">
    <node text="Backup" bounds="[40,463][250,506]" />
  </node>
</node></hierarchy>
"""

    assert settings_ssid_rows(hierarchy, ("Primary", "Backup")) == {
        "Primary": 286,
        "Backup": 431,
    }
    assert ssid_title_bounds(hierarchy, "Primary") == (40, 318, 250, 361)


def test_has_orange_highlight_detects_primary_title_color() -> None:
    image = Image.new("RGB", (20, 10), "white")
    for x in range(4):
        image.putpixel((x, 0), (230, 110, 30))

    assert has_orange_highlight(image, (0, 0, 20, 10))
    assert not has_orange_highlight(
        Image.new("RGB", (20, 10), (40, 40, 40)),
        (0, 0, 20, 10),
    )