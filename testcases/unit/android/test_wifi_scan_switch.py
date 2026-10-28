from unittest.mock import Mock, call

from core.libs.android.wifi_scenarios.settings import wifi_scan_switch as scenarios


def test_wifi_scan_default_case_restores_explicit_value(monkeypatch) -> None:
    monkeypatch.setattr(scenarios, "attach_wifi_status", Mock())
    monkeypatch.setattr(scenarios, "_wifi_scan_switch_checked", Mock(return_value=False))
    shell = Mock(side_effect=["1", "", "null", ""])
    settings_ui = Mock()

    scenarios.run_wifi_scan_default_case("case", shell, settings_ui)

    assert shell.call_args_list == [
        call("settings get global wifi_scan_always_enabled"),
        call("settings delete global wifi_scan_always_enabled"),
        call("settings get global wifi_scan_always_enabled"),
        call("settings put global wifi_scan_always_enabled 1"),
    ]
    settings_ui.device.press.assert_called_once_with("home")


def test_wifi_scan_toggle_case_checks_wifi_on_and_off(monkeypatch) -> None:
    monkeypatch.setattr(scenarios, "attach_wifi_status", Mock())
    monkeypatch.setattr(
        scenarios,
        "visible_ssids",
        Mock(side_effect=[["Lab_AP"], ["Lab_AP"]]),
    )
    monkeypatch.setattr(
        scenarios,
        "wlan_list_blob",
        Mock(side_effect=["Lab_AP", "Lab_AP"]),
    )
    shell = Mock(side_effect=["0", "", "1", ""])
    wifi = Mock()
    wifi.is_wifi_enabled.return_value = True
    wifi.set_wifi_enabled.return_value = True

    scenarios.run_wifi_scan_toggle_case(
        "case", shell, wifi, Mock(), scan_wait_sec=0
    )

    assert wifi.set_wifi_enabled.call_args_list == [call(True), call(False), call(True)]
    assert scenarios.visible_ssids.call_count == 2
    assert scenarios.wlan_list_blob.call_count == 2