from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from core.libs.android.wifi_scenarios import performance


def _ping_config(**overrides) -> SimpleNamespace:
    values = {
        "ping_host": "192.168.1.1",
        "ping_count": 3,
        "ping_big_size": 1200,
        "ping_small_size": 128,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_connection_latency_case_resets_and_connects_target(monkeypatch) -> None:
    entry = {"ssid": "Lab WiFi", "security": "WPA2", "password": "password"}
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock(return_value=(entry, "")))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monotonic = Mock(side_effect=(10.0, 11.0))
    monkeypatch.setattr(performance.time, "monotonic", monotonic)
    wifi = Mock()
    wifi.get_connected_ssid.return_value = '"Lab WiFi"'
    run_shell_cmd = Mock(return_value="Wi-Fi is enabled")

    performance.run_connection_latency_case(
        {"case_id": "Perf_Conn_AssocTime_002", "title": "WiFi"},
        run_shell_cmd,
        wifi,
        {"wifi_list": [entry]},
    )

    run_shell_cmd.assert_called_once_with("cmd wifi status")
    wifi.set_wifi_enabled.assert_called_once_with(True)
    wifi.disconnect_all.assert_called_once_with(
        max_rounds=2,
        settle_sec=1.0,
        post_wait_sec=2.0,
    )
    performance.connect_by_entry.assert_called_once_with(wifi, entry)


def test_ping_latency_case_runs_configured_ping(monkeypatch) -> None:
    entry = {"ssid": "Lab WiFi"}
    monkeypatch.setattr(
        performance,
        "get_settings",
        Mock(return_value=SimpleNamespace(performance=_ping_config())),
    )
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock(return_value=(entry, "")))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "wait_for_wifi_ipv4", Mock())
    monkeypatch.setattr(
        performance,
        "parse_ping_metrics",
        Mock(return_value=(5.0, 0.0, 1.0)),
    )
    run_shell_cmd = Mock(return_value="ping output")
    wifi = Mock()

    performance.run_ping_latency_case(
        {"case_id": "Perf_Latency_Ping_004", "title": "小包"},
        run_shell_cmd,
        wifi,
        {"wifi_list": [entry]},
    )

    assert run_shell_cmd.call_args_list == [
        call("cmd wifi status"),
        call("ping -c 3 -s 128 192.168.1.1"),
    ]
    performance.connect_by_entry.assert_called_once_with(wifi, entry)
    performance.parse_ping_metrics.assert_called_once_with("ping output")


def test_ping_latency_case_relaxes_thresholds_for_long_run_title(monkeypatch) -> None:
    entry = {"ssid": "Lab WiFi"}
    monkeypatch.setattr(
        performance,
        "get_settings",
        Mock(return_value=SimpleNamespace(performance=_ping_config())),
    )
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock(return_value=(entry, "")))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "wait_for_wifi_ipv4", Mock())
    monkeypatch.setattr(
        performance,
        "parse_ping_metrics",
        Mock(return_value=(50.0, 0.5, 40.0)),
    )

    performance.run_ping_latency_case(
        {"case_id": "Perf_Latency_Ping_006", "title": "HyperWiFi ，ping小包测试-12小时"},
        Mock(return_value="ping output"),
        Mock(),
        {"wifi_list": [entry]},
    )


def test_throughput_protocols_prefers_case_title(monkeypatch) -> None:
    assert performance.throughput_protocols({"title": "WiFi-TCP"}, "udp") == (
        "tcp",
    )


def test_throughput_parallel_streams_uses_traditional_override() -> None:
    config = SimpleNamespace(
        iperf_parallel_streams=1,
        traditional_iperf_parallel_streams=16,
    )

    assert performance.throughput_parallel_streams(
        {"case_id": "Perf_ThroughPut_PAT_005", "title": "PAT测试-WiFi-2.4G-TCP"},
        config,
    ) == 16
    assert performance.throughput_parallel_streams(
        {"case_id": "Perf_ThroughPut_PAT_001", "title": "PAT测试-HyperWiFi-US-TCP"},
        config,
    ) == 1


def test_pick_wifi_entry_uses_requested_band_bssid() -> None:
    entry = {
        "ssid": "Lab WiFi",
        "type": "normal",
        "bssids": {"2g": "00:11:22:33:44:55", "5g": "00:11:22:33:44:66"},
    }

    selected, reason = performance.pick_wifi_entry(
        {"case_id": "Perf_ThroughPut_PAT_005", "title": "PAT测试-WiFi-2.4G-TCP"},
        {"wifi_list": [{"ssid": "fallback", "type": "normal"}, entry]},
    )

    assert reason == ""
    assert selected is entry


def test_connect_by_entry_preserves_target_bssid() -> None:
    wifi = Mock()
    entry = {
        "ssid": "Lab WiFi",
        "pwd": "password",
        "encrypt": "WPA2",
        "bssid": "00:11:22:33:44:55",
    }

    assert performance.connect_by_entry(wifi, entry) is wifi.connect_wifi_block.return_value
    wifi.connect_wifi_block.assert_called_once_with(entry)


def test_assert_pat_link_band_checks_bssid_and_frequency() -> None:
    status = (
        "WifiInfo: SSID: \"Lab_HW_AutoTest\", BSSID: 54:f6:e2:e9:4a:4c, "
        "Frequency: 2412MHz"
    )

    assert performance.assert_pat_link_band(
        "Perf_ThroughPut_PAT_005",
        status,
        "2g",
        "54:f6:e2:e9:4a:4c",
    ) == "54:f6:e2:e9:4a:4c"
    with pytest.raises(pytest.fail.Exception, match="关联频段不符"):
        performance.assert_pat_link_band(
            "Perf_ThroughPut_PAT_005",
            status.replace("2412MHz", "5180MHz"),
            "2g",
            "54:f6:e2:e9:4a:4c",
        )
    assert performance.throughput_protocols({"title": "WiFi"}, "udp") == (
        "udp",
    )


def test_throughput_summary_formats_samples() -> None:
    assert performance.throughput_summary([10.0, 20.0]) == (
        "avg=15.00 Mbps, min=10.00, max=20.00, samples=10.00, 20.00"
    )


def test_pat_profile_and_curve_accept_valid_measurements() -> None:
    case_id = "Perf_ThroughPut_PAT_001"
    profile = performance.pat_profile(
        case_id,
        {
            "performance_pat": {
                case_id: {
                    "wifi_entry_id": "hyperwifi_us",
                    "min_disconnect_rssi_dbm": -90,
                    "inflection_rssi_dbm": -70,
                    "inflection_drop_pct": 30,
                    "points": [
                        {"rssi_dbm": -30, "min_tx_mbps": 80, "min_rx_mbps": 70},
                        {
                            "rssi_dbm": -70,
                            "min_tx_mbps": 40,
                            "min_rx_mbps": 35,
                            "max_drop_pct": 60,
                        },
                    ],
                }
            }
        },
    )

    assert profile is not None
    assert profile.wifi_entry_id == "hyperwifi_us"
    performance.assert_pat_curve(case_id, profile, {-30: (90, 80), -70: (50, 45)})


def test_pat_curve_rejects_early_inflection() -> None:
    profile = performance.PatProfile(
        wifi_entry_id="hyperwifi_us",
        ap_index=1,
        min_disconnect_rssi_dbm=-90,
        inflection_rssi_dbm=-70,
        inflection_drop_pct=30,
        points=(
            performance.PatBaselinePoint(-30, 1, 1),
            performance.PatBaselinePoint(-60, 1, 1),
            performance.PatBaselinePoint(-70, 1, 1),
        ),
    )

    with pytest.raises(AssertionError, match="拐点过早"):
        performance.assert_pat_curve(
            "Perf_ThroughPut_PAT_001",
            profile,
            {-30: (100, 100), -60: (60, 60), -70: (50, 50)},
        )


def test_pat_throughput_case_sweeps_points_and_restores_attenuation(monkeypatch) -> None:
    case_id = "Perf_ThroughPut_PAT_001"
    profile = performance.PatProfile(
        wifi_entry_id="hyperwifi_us",
        ap_index=1,
        min_disconnect_rssi_dbm=-80,
        inflection_rssi_dbm=-70,
        inflection_drop_pct=50,
        points=(
            performance.PatBaselinePoint(-30, 50, 50),
            performance.PatBaselinePoint(-70, 20, 20, 70),
        ),
    )
    config = SimpleNamespace(
        iperf_server="192.168.1.2",
        iperf_protocols="tcp",
        iperf_parallel_streams=1,
        traditional_iperf_parallel_streams=16,
    )
    attenuator = Mock(max_attenuation_db=10)
    attenuator.channel_for.return_value = 13
    attenuator.read_attenuations.return_value = {13: 4.0}
    wifi = Mock()
    entry = {"ssid": "HyperWi-Fi_US", "type": "hyperwifi"}
    read_rssi = Mock(side_effect=(-85, None, None))

    monkeypatch.setattr(performance, "pat_profile", Mock(return_value=profile))
    monkeypatch.setattr(performance, "get_settings", Mock(return_value=SimpleNamespace(performance=config)))
    monkeypatch.setattr(performance, "get_wifi_list_entry", Mock(return_value=entry))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "wait_for_wifi_ipv4", Mock())
    monkeypatch.setattr(performance, "_ensure_local_iperf_server", Mock())
    monkeypatch.setattr(performance.time, "sleep", Mock())
    monkeypatch.setattr(performance, "_hyper_rssi_reader", Mock(return_value=read_rssi))
    monkeypatch.setattr(
        performance,
        "tune_attenuation_for_rssi",
        Mock(side_effect=((2.0, -30), (6.0, -70))),
    )
    measure = Mock(side_effect=(100.0, 90.0, 40.0, 35.0))
    monkeypatch.setattr(performance, "_run_pat_direction", measure)

    performance.run_pat_throughput_case(
        {"case_id": case_id, "title": "PAT测试-HyperWiFi-US-TCP"},
        Mock(return_value="iperf 3.0"),
        wifi,
        {},
        attenuator,
    )

    assert measure.call_count == 4
    attenuator.set_attenuation.assert_called_with(13, 4.0)


def test_pat_throughput_case_collects_without_baseline(monkeypatch) -> None:
    case_id = "Perf_ThroughPut_PAT_001"
    config = SimpleNamespace(
        iperf_server="192.168.1.2",
        iperf_protocols="tcp",
        iperf_parallel_streams=1,
        traditional_iperf_parallel_streams=16,
    )
    attenuator = Mock(max_attenuation_db=20)
    attenuator.channel_for.return_value = 13
    attenuator.read_attenuations.return_value = {13: 4.0}
    entry = {"ssid": "HyperWi-Fi_US", "type": "hyperwifi"}
    read_rssi = Mock(return_value=-37)

    monkeypatch.setattr(performance, "pat_profile", Mock(return_value=None))
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock(return_value=(entry, "")))
    monkeypatch.setattr(performance, "get_settings", Mock(return_value=SimpleNamespace(performance=config)))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "wait_for_wifi_ipv4", Mock())
    monkeypatch.setattr(performance, "_ensure_local_iperf_server", Mock())
    monkeypatch.setattr(performance, "_hyper_rssi_reader", Mock(return_value=read_rssi))
    monkeypatch.setattr(
        performance,
        "tune_attenuation_for_rssi",
        Mock(side_effect=((3.0, -40), (8.0, None))),
    )
    measure = Mock(side_effect=(80.0, 75.0))
    monkeypatch.setattr(performance, "_run_pat_direction", measure)

    performance.run_pat_throughput_case(
        {"case_id": case_id, "title": "PAT测试-HyperWiFi-US-TCP"},
        Mock(return_value="iperf 3.0"),
        Mock(),
        {},
        attenuator,
    )

    assert measure.call_count == 2
    assert performance.tune_attenuation_for_rssi.call_args_list[0].kwargs["allow_missing"] is True
    attenuator.set_attenuation.assert_called_with(13, 4.0)


def test_run_pat_direction_archives_exactly_two_groups(monkeypatch) -> None:
    config = SimpleNamespace(
        iperf_server="192.168.1.2",
        iperf_duration_sec=1,
        iperf_parallel_streams=1,
        udp_bandwidth="10M",
    )
    run_shell_cmd = Mock(return_value="{}")
    monkeypatch.setattr(performance, "parse_iperf_mbps", Mock(return_value=(80.0, 75.0)))
    archive = Mock()
    monkeypatch.setattr(performance, "archive_iperf_run", archive)

    average = performance._run_pat_direction(
        "Perf_ThroughPut_PAT_001",
        run_shell_cmd,
        config,
        ssid="HyperWi-Fi_US",
        protocol="tcp",
        reverse=False,
        rssi_dbm=-40,
    )

    assert average == 80.0
    assert run_shell_cmd.call_count == 2
    assert archive.call_count == 2
    assert [item.args[0]["run"] for item in archive.call_args_list] == [1, 2]
    assert all(item.args[0]["rssi_dbm"] == -40 for item in archive.call_args_list)


def test_throughput_case_runs_both_tcp_directions(monkeypatch) -> None:
    entry = {"ssid": "Lab WiFi"}
    config = SimpleNamespace(
        iperf_server="192.168.1.2",
        iperf_duration_sec=1,
        iperf_runs=1,
        iperf_parallel_streams=1,
        udp_bandwidth="10M",
        min_mbps=50.0,
        iperf_protocols="tcp",
    )
    monkeypatch.setattr(
        performance,
        "get_settings",
        Mock(return_value=SimpleNamespace(performance=config)),
    )
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock(return_value=(entry, "")))
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "_ensure_local_iperf_server", Mock())
    monkeypatch.setattr(
        performance,
        "parse_iperf_mbps",
        Mock(return_value=(100.0, 100.0)),
    )
    run_shell_cmd = Mock(
        side_effect=lambda command, **_: "iperf3 3.0" if command == "iperf3 --version" else "{}"
    )
    wifi = Mock()
    wifi.get_connected_ssid.return_value = "Lab WiFi"

    performance.run_throughput_case(
        {"case_id": "Perf_ThroughPut_MaxTpt_005", "title": "WiFi-TCP"},
        run_shell_cmd,
        wifi,
        {"wifi_list": [entry]},
    )

    run_shell_cmd.assert_any_call("iperf3 -c 192.168.1.2 -t 1 -P 1 -J", timeout_sec=31)
    run_shell_cmd.assert_any_call("iperf3 -c 192.168.1.2 -t 1 -P 1 -R -J", timeout_sec=31)
    assert performance.parse_iperf_mbps.call_count == 2


def test_throughput_case_prefers_explicit_wifi_entry_id(monkeypatch) -> None:
    entry = {"id": "hyperwifi_us", "ssid": "HyperWi-Fi_US"}
    config = SimpleNamespace(
        iperf_server="192.168.1.2",
        iperf_duration_sec=1,
        iperf_runs=1,
        iperf_parallel_streams=1,
        udp_bandwidth="10M",
        min_mbps=50.0,
        iperf_protocols="tcp",
    )
    monkeypatch.setattr(
        performance,
        "get_settings",
        Mock(return_value=SimpleNamespace(performance=config)),
    )
    monkeypatch.setattr(performance, "pick_wifi_entry", Mock())
    monkeypatch.setattr(performance, "connect_by_entry", Mock(return_value=True))
    monkeypatch.setattr(performance, "_ensure_local_iperf_server", Mock())
    monkeypatch.setattr(
        performance,
        "parse_iperf_mbps",
        Mock(return_value=(100.0, 100.0)),
    )
    run_shell_cmd = Mock(
        side_effect=lambda command, **_: "iperf3 3.0" if command == "iperf3 --version" else "{}"
    )
    wifi = Mock()
    wifi.get_connected_ssid.return_value = "HyperWi-Fi_US"

    performance.run_throughput_case(
        {"case_id": "Perf_ThroughPut_MaxTpt_015", "title": "不同加密方式"},
        run_shell_cmd,
        wifi,
        {"wifi_list": [entry]},
        wifi_entry_id="hyperwifi_us",
    )

    performance.pick_wifi_entry.assert_not_called()
    performance.connect_by_entry.assert_called_once_with(wifi, entry)