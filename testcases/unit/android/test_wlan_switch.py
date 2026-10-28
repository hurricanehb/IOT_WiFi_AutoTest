from unittest.mock import Mock, call

from core.libs.android.wifi_scenarios.settings import wlan_switch as scenarios


def test_set_airplane_mode_updates_setting_and_broadcasts(monkeypatch):
    shell = Mock(side_effect=["", "1"])
    monkeypatch.setattr(scenarios.time, "sleep", Mock())

    scenarios._set_airplane_mode(shell, True, settle_sec=0)

    assert shell.call_args_list == [
        call("cmd connectivity airplane-mode enable"),
        call("settings get global airplane_mode_on"),
    ]


def test_airplane_wlan_case_restores_original_state(monkeypatch):
    entry = {"ssid": "target", "pwd": "password", "encrypt": "WPA2"}
    monkeypatch.setattr(scenarios, "_resolve_entry", Mock(return_value=entry))
    monkeypatch.setattr(
        scenarios,
        "assert_wifi_connected",
        Mock(side_effect=["target", "target", "target"]),
    )
    airplane_values = iter(["0", "0"])
    monkeypatch.setattr(
        scenarios, "_airplane_mode_value", lambda run_shell_cmd: next(airplane_values)
    )
    set_airplane = Mock()
    monkeypatch.setattr(scenarios, "_set_airplane_mode", set_airplane)
    wifi = Mock()
    wifi.is_wifi_enabled.side_effect = [True, False]
    wifi.set_wifi_enabled.return_value = True
    shell = Mock()

    scenarios.run_airplane_wlan_switch_case(
        "case", shell, wifi, {}, settle_sec=0
    )

    assert set_airplane.call_args_list == [
        call(shell, True, settle_sec=0),
        call(shell, False, settle_sec=0),
    ]
    assert wifi.set_wifi_enabled.call_args_list == [
        call(True, settle_sec=0),
        call(False, settle_sec=0),
        call(True, settle_sec=0),
        call(True, settle_sec=0),
    ]


def test_toggle_stability_runs_requested_cycles_and_restores(monkeypatch):
    wifi = Mock()
    wifi.is_wifi_enabled.return_value = True
    wifi.set_wifi_enabled.return_value = True
    settings_ui = Mock()
    shell = Mock(side_effect=["Wi-Fi is enabled", "", "1234", ""])

    scenarios.run_wlan_toggle_stability_case(
        "case", shell, wifi, settings_ui, cycles=3, settle_sec=0
    )

    assert wifi.set_wifi_enabled.call_args_list == [
        call(False, settle_sec=0), call(True, settle_sec=0),
        call(False, settle_sec=0), call(True, settle_sec=0),
        call(False, settle_sec=0), call(True, settle_sec=0),
        call(True),
    ]
    settings_ui.open_wifi_settings.assert_called_once_with()


def test_scroll_stability_runs_two_swipes_per_cycle():
    settings_ui = Mock()
    settings_ui.device.window_size.return_value = (1000, 2000)
    settings_ui.device.dump_hierarchy.return_value = (
        '<node package="com.android.settings" />'
    )
    shell = Mock(side_effect=["Wi-Fi is enabled", "", "1234", ""])

    scenarios.run_wlan_list_scroll_stability_case(
        "case", shell, settings_ui, cycles=3
    )

    assert settings_ui.device.swipe.call_count == 6
    settings_ui.open_wifi_settings.assert_called_once_with()


def test_hotspot_case_always_stops_softap(monkeypatch):
    monkeypatch.setattr(scenarios, "_resolve_entry", Mock(return_value={"ssid": "target"}))
    monkeypatch.setattr(scenarios, "assert_wifi_connected", Mock(side_effect=["target", "target"]))
    monkeypatch.setattr(scenarios.time, "sleep", Mock())
    shell = Mock(side_effect=["Wi-Fi is enabled", "", "wlan1: <UP> state UP", ""])
    wifi = Mock()
    wifi.list_connected_ssids.return_value = ["target"]
    wifi.set_wifi_enabled.return_value = True

    scenarios.run_hotspot_wlan_switch_case(
        "case", shell, wifi, {}, settle_sec=0
    )

    assert shell.call_args_list[-1] == call("cmd wifi stop-softap")


def test_cross_component_case_checks_both_directions(monkeypatch):
    monkeypatch.setattr(scenarios.time, "sleep", Mock())
    monkeypatch.setattr(scenarios, "open_internet_dialog", Mock())
    tile = Mock()
    tile.info = {"checked": False}
    monkeypatch.setattr(scenarios, "systemui_wifi_toggle", Mock(return_value=tile))
    wifi = Mock()
    wifi.is_wifi_enabled.side_effect = [True, False, True, True]
    settings_ui = Mock()
    settings_ui.wifi_switch_checked.return_value = True
    shell = Mock(return_value="Wi-Fi is enabled")

    scenarios.run_cross_component_wlan_switch_case(
        "case", shell, wifi, settings_ui, settle_sec=0
    )

    shell.assert_called_once_with("cmd wifi status")
    assert settings_ui.set_wifi_switch.call_args_list == [call(False), call(False), call(True)]
    tile.click.assert_called_once_with()
    wifi.set_wifi_enabled.assert_called_once_with(True)


def test_wrong_password_stability_rejects_then_reconnects(monkeypatch):
    monkeypatch.setattr(scenarios.time, "sleep", Mock())
    connected = Mock(return_value="target")
    monkeypatch.setattr(scenarios, "assert_wifi_connected", connected)
    shell = Mock(side_effect=["Wi-Fi is enabled", "", "1234", ""])
    wifi = Mock()
    wifi.list_connected_ssids.return_value = []
    settings_ui = Mock()
    wifi_ap_action = Mock()

    scenarios.run_wrong_password_reconnect_stability_case(
        "case", shell, wifi, {}, settings_ui, wifi_ap_action,
        cycles=3, settle_sec=0,
    )

    assert wifi.connect_wpa2.call_count == 3
    assert connected.call_count == 3
    assert wifi.clear_saved_networks.call_count == 4
    wifi_ap_action.configure_wifi.assert_called_once_with(
        ssid="PyAutoTest_WlanStability",
        password="24681357",
        security="wpa2-aes",
        band="5g",
        verify=True,
    )