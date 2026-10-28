import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    assert_active_stream_policy,
    assert_candidate_score_selection,
    assert_equal_score_prefers_stronger_candidate,
    assert_interface_scan_started,
    assert_independent_link_network_selection,
    assert_low_traffic_policy,
    assert_no_pno_scan,
    assert_pno_scan_started,
    assert_no_interface_scan,
    assert_network_selection_skipped_for_sufficient_link,
    assert_periodic_scan_interval,
    assert_recent_network_selection_skipped,
    assert_scan_backoff_policy,
    assert_scan_backoff_sequence,
    assert_scan_backoff_started,
    assert_single_immediate_scan,
    parse_pno_scan_events,
    parse_interface_scan_offsets,
    parse_active_default_route,
    parse_candidate_scores,
    parse_network_selection_scan_cycles,
    parse_network_selection_scan_events,
    parse_recent_selection_skips,
)


SCORE_LOG = "\n".join(
    (
        'ThroughputScorer: Score for candidate: SSID: '
        '"Lab_AT1_HyperWiFi_test_2" BSSID: aa:bb rssiScore: 60 '
        'rssi: -71 final score: 3610',
        'ThroughputScorer: Score for candidate: SSID: '
        '"Lab_AT1_HyperWiFi_test_1" BSSID: cc:dd rssiScore: 60 '
        'rssi: -58 final score: 3610',
        'WifiConnectivityManager: turbolink candidate: '
        '"Lab_AT1_HyperWiFi_test_1" turbolinkCandidate.networkId :66',
    )
)


def test_equal_score_prefers_stronger_candidate() -> None:
    assert parse_candidate_scores(SCORE_LOG) == {
        "Lab_AT1_HyperWiFi_test_2": (60, -71, 3610),
        "Lab_AT1_HyperWiFi_test_1": (60, -58, 3610),
    }
    assert_equal_score_prefers_stronger_candidate(
        SCORE_LOG,
        stronger_ssid="Lab_AT1_HyperWiFi_test_1",
        weaker_ssid="Lab_AT1_HyperWiFi_test_2",
        summary="case",
    )


def test_equal_score_candidate_assertion_rejects_unequal_scores() -> None:
    with pytest.raises(pytest.fail.Exception, match="final scores differ"):
        assert_equal_score_prefers_stronger_candidate(
            SCORE_LOG.replace("final score: 3610", "final score: 3600", 1),
            stronger_ssid="Lab_AT1_HyperWiFi_test_1",
            weaker_ssid="Lab_AT1_HyperWiFi_test_2",
            summary="case",
        )


def test_traffic_policy_assertions_require_exact_evidence() -> None:
    log_text = (
        "WifiConnectivityManager: hasActiveStream:true\n"
        "WifiNetworkSelector: Current network link quality is not sufficient "
        "and has low ongoing traffic"
    )

    assert_active_stream_policy(log_text, summary="case")
    assert_low_traffic_policy(log_text, summary="case")
    with pytest.raises(pytest.fail.Exception, match="hasActiveStream:true"):
        assert_active_stream_policy("hasActiveStream:false", summary="case")
    with pytest.raises(pytest.fail.Exception, match="low ongoing traffic"):
        assert_low_traffic_policy("hasActiveStream:true", summary="case")


def test_parse_active_default_route_ignores_dummy_network() -> None:
    route_text = "\n".join(
        (
            "default dev dummy0 table dummy0 proto static scope link",
            "default via 192.168.3.1 dev bond0 table 1030 proto static",
        )
    )

    assert parse_active_default_route(route_text) == ("192.168.3.1", "bond0")
    assert parse_active_default_route("default dev dummy0") is None


def test_parse_pno_scan_events_is_case_insensitive() -> None:
    log_text = "\n".join(
        (
            "09-14 00:00:01.000 WifiScanner: Pno scan started",
            "09-14 00:00:02.000 WifiScanner: unrelated",
            "09-14 00:00:03.000 WifiScanner: PNO SCAN STARTED",
        )
    )

    assert len(parse_pno_scan_events(log_text)) == 2


def test_assert_no_pno_scan_rejects_scan_event() -> None:
    with pytest.raises(pytest.fail.Exception, match="unexpectedly started 1 PNO"):
        assert_no_pno_scan("WifiScanner: Pno scan started", summary="case")


def test_assert_pno_scan_started_requires_event() -> None:
    with pytest.raises(pytest.fail.Exception, match="PNO scan did not start"):
        assert_pno_scan_started("WifiScanner: unrelated", summary="case")


def test_assert_interface_scan_started_requires_target_interface() -> None:
    log_text = "09-14 00:00:01.000 WifiScanningService: startSingleScan on real: wlan1"

    with pytest.raises(pytest.fail.Exception, match="wlan0 did not start a scan"):
        assert_interface_scan_started(log_text, interface="wlan0", summary="case")


SCAN_EVENT = (
    "09-13 23:38:54.309  1423  1757 V WifiConnectivityManager: "
    "AllSingleScanListener onResults: start network selection"
)


def test_parse_network_selection_scan_events_ignores_listener_duplicates() -> None:
    log_text = "\n".join(
        (
            "09-13 23:38:54.300 I WifiScanningService: singleScanResults: listener=1",
            "09-13 23:38:54.301 I WifiScanningService: singleScanResults: listener=2",
            SCAN_EVENT,
        )
    )

    assert parse_network_selection_scan_events(log_text) == [SCAN_EVENT]


def test_assert_single_immediate_scan_accepts_one_prompt_event() -> None:
    assert_single_immediate_scan(
        SCAN_EVENT,
        elapsed_sec=1.3,
        summary="case",
    )


def test_scan_callbacks_from_two_radios_form_one_cycle() -> None:
    second_radio_event = SCAN_EVENT.replace("54.309", "55.609")

    assert parse_network_selection_scan_cycles(
        f"{SCAN_EVENT}\n{second_radio_event}"
    ) == [0.0]
    assert_single_immediate_scan(
        f"{SCAN_EVENT}\n{second_radio_event}",
        elapsed_sec=1.3,
        summary="case",
    )


def test_parse_interface_scan_offsets_filters_other_radio() -> None:
    log_text = "\n".join(
        (
            "09-13 23:51:44.342 I WifiScanningService: startSingleScan on real: wlan0",
            "09-13 23:51:44.350 I WifiScanningService: startSingleScan on real: wlan1",
            "09-13 23:52:04.365 I WifiScanningService: startSingleScan on real: wlan0",
        )
    )

    assert parse_interface_scan_offsets(log_text, "wlan0") == [0.0, 20.023]
    assert_no_interface_scan(log_text, interface="hyper0", summary="case")
    assert_scan_backoff_started(log_text, interface="wlan0", summary="case")


def test_interface_scan_assertions_reject_wrong_behavior() -> None:
    one_scan = (
        "09-13 23:51:44.342 I WifiScanningService: "
        "startSingleScan on real: wlan0"
    )
    with pytest.raises(pytest.fail.Exception, match="unexpectedly started 1"):
        assert_no_interface_scan(one_scan, interface="wlan0", summary="case")
    with pytest.raises(pytest.fail.Exception, match="fewer than two"):
        assert_scan_backoff_started(one_scan, interface="wlan0", summary="case")


def test_periodic_scan_interval_accepts_two_ten_second_scans() -> None:
    log_text = "\n".join(
        (
            "09-13 23:51:44.342 I WifiScanningService: startSingleScan on real: wlan1",
            "09-13 23:51:54.365 I WifiScanningService: startSingleScan on real: wlan1",
        )
    )

    assert_periodic_scan_interval(
        log_text,
        interface="wlan1",
        summary="case",
        expected_interval_sec=10.0,
    )


def test_periodic_scan_interval_rejects_wrong_period() -> None:
    log_text = "\n".join(
        (
            "09-13 23:51:44.342 I WifiScanningService: startSingleScan on real: wlan1",
            "09-13 23:52:04.365 I WifiScanningService: startSingleScan on real: wlan1",
            "09-13 23:52:24.350 I WifiScanningService: startSingleScan on real: wlan1",
        )
    )

    with pytest.raises(pytest.fail.Exception, match="scan intervals"):
        assert_periodic_scan_interval(
            log_text,
            interface="wlan1",
            summary="case",
            expected_interval_sec=10.0,
        )


def test_sufficient_link_skip_requires_interface_and_decision() -> None:
    log_text = (
        "WifiNetworkSelector: wlan0: Current connected network already "
        "sufficient. Skip network selection."
    )

    assert_network_selection_skipped_for_sufficient_link(
        log_text,
        interface="wlan0",
        summary="case",
    )
    with pytest.raises(pytest.fail.Exception, match="missing sufficient-link"):
        assert_network_selection_skipped_for_sufficient_link(
            log_text,
            interface="wlan1",
            summary="case",
        )


def test_independent_link_network_selection_requires_both_interfaces() -> None:
    log_text = "\n".join(
        (
            "09-14 00:00:01.000 WifiScanningService: startSingleScan on real: wlan0",
            "09-14 00:00:01.100 WifiNetworkSelector: wlan0: Current connected network is not sufficient.",
            "09-14 00:00:02.000 WifiScanningService: startSingleScan on real: wlan1",
            "09-14 00:00:02.100 WifiNetworkSelector: wlan1: Current connected network is not sufficient.",
        )
    )

    assert_independent_link_network_selection(log_text, summary="case")
    with pytest.raises(pytest.fail.Exception, match=r"missing_scans=\['wlan1'\]"):
        assert_independent_link_network_selection(
            "\n".join(log_text.splitlines()[:2]),
            summary="case",
        )


def test_scan_backoff_policy_accepts_current_backoff_state() -> None:
    log_text = "\n".join(
        (
            "09-14 00:27:56.631 V WifiConnectivityManager: "
            "schedulePeriodicScanTimer intervalMs 80000",
            "09-14 00:27:56.634 D WifiNetworkSelector: Current network link "
            "quality is not sufficient and has low ongoing traffic",
            "09-14 00:27:56.648 I WifiScanningService: "
            "startSingleScan on real: wlan0",
        )
    )

    assert_scan_backoff_policy(log_text, interface="wlan0", summary="case")


def test_scan_backoff_policy_accepts_hyper_without_traffic_log() -> None:
    log_text = "\n".join(
        (
            "09-14 00:27:56.631 V WifiConnectivityManager: "
            "schedulePeriodicScanTimer intervalMs 80000",
            "09-14 00:27:56.634 D WifiNetworkSelector: wlan1: "
            "Current connected network is not sufficient.",
            "09-14 00:27:56.648 I WifiScanningService: "
            "startSingleScan on real: wlan1",
        )
    )

    assert_scan_backoff_policy(
        log_text,
        interface="wlan1",
        summary="case",
        require_low_traffic=False,
    )


def test_scan_backoff_sequence_requires_full_ordered_policy() -> None:
    log_text = "\n".join(
        (
            "09-14 00:00:00.000 V WifiConnectivityManager: schedulePeriodicScanTimer intervalMs 20000",
            "09-14 00:00:00.010 I WifiScanningService: startSingleScan on real: wlan1",
            "09-14 00:00:20.000 I WifiScanningService: startSingleScan on real: wlan1",
            "09-14 00:00:20.010 V WifiConnectivityManager: schedulePeriodicScanTimer intervalMs 40000",
            "09-14 00:01:00.000 I WifiScanningService: startSingleScan on real: wlan1",
            "09-14 00:01:00.010 V WifiConnectivityManager: schedulePeriodicScanTimer intervalMs 80000",
            "09-14 00:02:20.000 I WifiScanningService: startSingleScan on real: wlan1",
            "09-14 00:02:20.010 V WifiConnectivityManager: schedulePeriodicScanTimer intervalMs 160000",
        )
    )

    assert_scan_backoff_sequence(log_text, interface="wlan1", summary="case")
    immediate_scan = (
        "09-14 00:00:00.005 I WifiScanningService: "
        "startSingleScan on real: wlan1"
    )
    assert_scan_backoff_sequence(
        f"{immediate_scan}\n{log_text}",
        interface="wlan1",
        summary="case",
    )
    with pytest.raises(pytest.fail.Exception, match="ordered sequence"):
        assert_scan_backoff_sequence(
            log_text.replace("intervalMs 80000", "intervalMs 60000"),
            interface="wlan1",
            summary="case",
        )


@pytest.mark.parametrize(
    ("log_text", "message"),
    [
        (
            "09-14 00:27:56.631 V WifiConnectivityManager: "
            "schedulePeriodicScanTimer intervalMs 80000",
            "did not start",
        ),
        (
            "09-14 00:27:56.648 I WifiScanningService: "
            "startSingleScan on real: wlan0",
            "missing low-quality",
        ),
    ],
)
def test_scan_backoff_policy_rejects_missing_evidence(
    log_text: str,
    message: str,
) -> None:
    with pytest.raises(pytest.fail.Exception, match=message):
        assert_scan_backoff_policy(log_text, interface="wlan0", summary="case")


@pytest.mark.parametrize(
    ("log_text", "elapsed_sec", "message"),
    [
        ("", 1.0, "found 0"),
        (
            f"{SCAN_EVENT}\n{SCAN_EVENT.replace('54.309', '57.309')}",
            1.0,
            "found 2",
        ),
        (SCAN_EVENT, 6.1, "scan completed after 6.1s"),
    ],
)
def test_assert_single_immediate_scan_rejects_invalid_evidence(
    log_text: str,
    elapsed_sec: float,
    message: str,
) -> None:
    with pytest.raises(pytest.fail.Exception, match=message):
        assert_single_immediate_scan(
            log_text,
            elapsed_sec=elapsed_sec,
            summary="case",
        )


def test_parse_candidate_scores_does_not_cross_log_lines() -> None:
    noisy_log = 'WifiScoreCard: SSID: "unrelated" details\n' + SCORE_LOG

    assert "unrelated" not in parse_candidate_scores(noisy_log)


def test_candidate_score_selection_requires_expected_rssi_scores() -> None:
    threshold_log = SCORE_LOG.replace(
        '"Lab_AT1_HyperWiFi_test_2" BSSID: aa:bb rssiScore: 60',
        '"Lab_AT1_HyperWiFi_test_2" BSSID: aa:bb rssiScore: 56',
    )

    assert_candidate_score_selection(
        threshold_log,
        stronger_ssid="Lab_AT1_HyperWiFi_test_1",
        weaker_ssid="Lab_AT1_HyperWiFi_test_2",
        summary="case",
        expected_rssi_scores=(60, 56),
    )
    with pytest.raises(pytest.fail.Exception, match="RSSI scores were"):
        assert_candidate_score_selection(
            threshold_log,
            stronger_ssid="Lab_AT1_HyperWiFi_test_1",
            weaker_ssid="Lab_AT1_HyperWiFi_test_2",
            summary="case",
            expected_rssi_scores=(56, 60),
        )


def test_recent_network_selection_skip_requires_interface_and_timing() -> None:
    log_text = (
        "WifiNetworkSelector: wlan1: Too short since last network selection: "
        "8512 ms. Skip network selection"
    )

    assert parse_recent_selection_skips(log_text) == [("wlan1", 8512)]
    assert_recent_network_selection_skipped(
        log_text,
        interface="wlan1",
        summary="case",
    )
    with pytest.raises(pytest.fail.Exception, match="missing recent-selection"):
        assert_recent_network_selection_skipped(
            log_text,
            interface="wlan0",
            summary="case",
        )
    with pytest.raises(pytest.fail.Exception, match="expected <8000"):
        assert_recent_network_selection_skipped(
            log_text,
            interface="wlan1",
            summary="case",
            maximum_elapsed_ms=8000,
        )