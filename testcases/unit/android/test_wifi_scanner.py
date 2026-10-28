from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from core.libs.android.wifi_scenarios.qr_scanner import (
    WifiQrDisplay,
    wifi_qr_payload,
    _wait_for_scanner_connection,
    run_wifi_scanner_case,
)


def test_wifi_qr_payload_escapes_delimiters() -> None:
    assert wifi_qr_payload('a;b\\c', 'p:q,"') == (
        'WIFI:T:WPA;S:a\\;b\\\\c;P:p\\:q\\,\\";;'
    )


def test_wifi_qr_payload_open_network_omits_password() -> None:
    assert wifi_qr_payload("Guest", "ignored", "open") == (
        "WIFI:T:nopass;S:Guest;;"
    )


def test_wifi_qr_payload_rejects_unsupported_security() -> None:
    with pytest.raises(ValueError, match="不支持"):
        wifi_qr_payload("Lab", "secret", "WEP")


def test_wifi_qr_display_close_terminates_live_process() -> None:
    display = WifiQrDisplay("payload")
    process = Mock()
    process.is_alive.return_value = True
    display._process = process

    display.close()

    process.terminate.assert_called_once_with()
    process.join.assert_called_once_with(timeout=3.0)
    assert display._process is None


def test_wait_for_scanner_connection_requires_connected_and_saved() -> None:
    wifi = SimpleNamespace(
        list_connected_ssids=lambda **kwargs: ["Lab_QR"],
        list_networks_blob=lambda: '0 "Lab_QR" [CURRENT]',
    )

    _wait_for_scanner_connection(wifi, "Lab_QR", timeout_sec=0.01)


def test_wait_for_scanner_connection_supports_whitespace_ssid() -> None:
    wifi = SimpleNamespace(
        list_connected_ssids=lambda **kwargs: [],
        list_networks_blob=lambda: '0 " " [CURRENT]',
        is_wifi_associated=lambda: True,
    )

    _wait_for_scanner_connection(wifi, " ", timeout_sec=0.01)


def test_scanner_case_skips_without_camera_lab_opt_in(monkeypatch) -> None:
    monkeypatch.delenv("WIFI_QR_LAB", raising=False)

    with pytest.raises(pytest.skip.Exception, match="WIFI_QR_LAB=1"):
        run_wifi_scanner_case(
            {"case_id": "scanner"},
            lambda command: "",
            SimpleNamespace(),
            {},
            SimpleNamespace(),
            None,
            entry_id="scanner_default",
        )
