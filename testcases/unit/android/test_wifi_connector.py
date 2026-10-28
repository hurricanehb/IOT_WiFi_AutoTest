from __future__ import annotations

from unittest.mock import Mock, call, patch

from core.libs.android.wifi_control.connector import WiFiConnector
from core.libs.android.wifi_control.state import WiFiState
from core.utils.adb_helper import AdbHelper


def _connector(adb, state, *, disconnect_all=None) -> WiFiConnector:
    return WiFiConnector(
        adb,
        state=state,
        set_wifi_enabled=lambda enabled: enabled,
        disconnect_all=disconnect_all or Mock(return_value=True),
        logger=Mock(),
    )


def test_connect_wifi_block_preserves_credential_whitespace() -> None:
    adb = Mock(spec=AdbHelper)
    adb.shell.return_value = (0, "Connection initiated", "")
    ssid = " Test Network "
    password = " Password 123 "
    state = Mock(spec=WiFiState)
    state.get_connected_ssid.return_value = ssid
    state.match_associated_ssids.return_value = ([ssid], [])
    connector = _connector(adb, state)

    connected = connector.connect_wifi_block(
        {"ssid": ssid, "pwd": password, "encrypt": "WPA2"}
    )

    assert connected is True
    adb.shell.assert_called_once_with(
        "cmd",
        "wifi",
        "connect-network",
        ssid,
        "wpa2",
        password,
    )


def test_connect_wifi_block_targets_configured_bssid() -> None:
    adb = Mock(spec=AdbHelper)
    adb.shell.return_value = (0, "Connection initiated", "")
    state = Mock(spec=WiFiState)
    state.get_connected_ssid.return_value = "Lab_AP"
    state.match_associated_ssids.return_value = (["Lab_AP"], [])
    connector = _connector(adb, state)

    connected = connector.connect_wifi_block(
        {
            "ssid": "Lab_AP",
            "pwd": "24681357",
            "encrypt": "WPA2",
            "bssid": "54:f6:e2:e9:4a:57",
        }
    )

    assert connected is True
    adb.shell.assert_called_once_with(
        "cmd",
        "wifi",
        "connect-network",
        "Lab_AP",
        "wpa2",
        "24681357",
        "-b",
        "54:f6:e2:e9:4a:57",
        "-r",
        "none",
    )


def test_connect_wifi_block_uses_native_wep_security() -> None:
    adb = Mock(spec=AdbHelper)
    adb.shell.return_value = (0, "Connection initiated", "")
    state = Mock(spec=WiFiState)
    state.get_connected_ssid.return_value = "Lab_WEP"
    state.match_associated_ssids.return_value = (["Lab_WEP"], [])

    connected = _connector(adb, state).connect_wifi_block(
        {"ssid": "Lab_WEP", "pwd": "12345", "encrypt": "WEP"}
    )

    assert connected is True
    adb.shell.assert_called_once_with(
        "cmd", "wifi", "connect-network", "Lab_WEP", "wep", "12345"
    )


def test_connect_wifi_block_uses_native_owe_without_credential() -> None:
    adb = Mock(spec=AdbHelper)
    adb.shell.return_value = (0, "Connection initiated", "")
    state = Mock(spec=WiFiState)
    state.get_connected_ssid.return_value = "Lab_OWE"
    state.match_associated_ssids.return_value = (["Lab_OWE"], [])

    connected = _connector(adb, state).connect_wifi_block(
        {"ssid": "Lab_OWE", "pwd": "", "encrypt": "OWE"}
    )

    assert connected is True
    adb.shell.assert_called_once_with(
        "cmd", "wifi", "connect-network", "Lab_OWE", "owe"
    )


def test_connect_wpa3_falls_back_to_sae_when_command_is_unsupported() -> None:
    adb = Mock(spec=AdbHelper)
    adb.shell.side_effect = [
        (1, "", "unsupported security type"),
        (0, "Connection initiated", ""),
    ]
    state = Mock(spec=WiFiState)
    state.get_connected_ssid.return_value = "Lab_WPA3"
    state.match_associated_ssids.return_value = (["Lab_WPA3"], [])

    connected = _connector(adb, state).connect_wpa3("Lab_WPA3", "24681357")

    assert connected is True
    assert adb.shell.call_args_list == [
        call("cmd", "wifi", "connect-network", "Lab_WPA3", "wpa3", "24681357"),
        call("cmd", "wifi", "connect-network", "Lab_WPA3", "sae", "24681357"),
    ]


def test_ensure_wifi_connected_disconnects_unrelated_network_and_retries() -> None:
    adb = Mock(spec=AdbHelper)
    state = Mock(spec=WiFiState)
    state.list_connected_ssids.return_value = ["Other_AP"]
    state.match_associated_ssids.side_effect = [
        ([], ["Target_AP"]),
        ([], ["Target_AP"]),
        (["Target_AP"], []),
    ]
    disconnect_all = Mock(return_value=True)
    connector = _connector(adb, state, disconnect_all=disconnect_all)
    connector.connect_wifi_block = Mock(return_value=True)
    entry = {"ssid": "Target_AP", "pwd": "24681357", "encrypt": "WPA2"}

    with patch("core.libs.android.wifi_control.connector.time.sleep"):
        connected = connector.ensure_wifi_connected(entry, settle_sec=0)

    assert connected is True
    disconnect_all.assert_called_once_with(
        settle_sec=1.5,
        max_rounds=2,
        post_wait_sec=2.0,
    )
    assert connector.connect_wifi_block.call_count == 2


def test_ensure_dual_wifi_connected_uses_monotonic_deadline() -> None:
    adb = Mock(spec=AdbHelper)
    state = Mock(spec=WiFiState)
    state.match_associated_ssids.side_effect = [
        ([], ["Traditional", "Hyper"]),
        (["Traditional"], ["Hyper"]),
        (["Traditional"], ["Hyper"]),
    ]
    connector = _connector(adb, state)
    connector.connect_wifi_block = Mock(return_value=True)
    entry = {
        "traditional_wifi": {
            "ssid": "Traditional",
            "pwd": "24681357",
            "encrypt": "WPA2",
        },
        "hyper_wifi": {
            "ssid": "Hyper",
            "pwd": "24681357",
            "encrypt": "WPA3",
        },
    }

    with (
        patch(
            "core.libs.android.wifi_control.connector.time.monotonic",
            side_effect=[100.0, 100.0, 111.0],
        ) as monotonic,
        patch("core.libs.android.wifi_control.connector.time.sleep"),
    ):
        connected, found, missing = connector.ensure_dual_wifi_connected(
            entry,
            timeout=0,
            interval=0,
            settle_after_connect=0,
        )

    assert connected is False
    assert found == ["Traditional"]
    assert missing == ["Hyper"]
    assert monotonic.call_count == 3


def test_dual_wifi_timeout_starts_before_connection_attempts(monkeypatch) -> None:
    adb = Mock(spec=AdbHelper)
    state = Mock(spec=WiFiState)
    state.match_associated_ssids.side_effect = [
        ([], ["Traditional", "Hyper"]),
        ([], ["Traditional", "Hyper"]),
    ]
    connector = _connector(adb, state)
    connector.connect_wifi_block = Mock(return_value=False)
    entry = {
        "traditional_wifi": {
            "ssid": "Traditional",
            "pwd": "24681357",
            "encrypt": "WPA2",
        },
        "hyper_wifi": {
            "ssid": "Hyper",
            "pwd": "24681357",
            "encrypt": "WPA3",
        },
    }

    clock = Mock()
    clock.side_effect = [0.0, 0.0, 1.0, 1.0, 11.0, 11.0, 11.0]
    monkeypatch.setattr("core.libs.android.wifi_control.connector.time.monotonic", clock)
    monkeypatch.setattr("core.libs.android.wifi_control.connector.time.sleep", Mock())

    ok, _, missing = connector.ensure_dual_wifi_connected(entry, timeout=10.0)

    assert ok is False
    assert missing == ["Traditional", "Hyper"]
    assert connector.connect_wifi_block.call_count == 1
    assert all(
        call.kwargs["use_dumpsys_for_missing"] is False
        for call in state.match_associated_ssids.call_args_list
    )
