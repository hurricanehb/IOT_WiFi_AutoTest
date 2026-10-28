from unittest.mock import Mock

from core.libs.android.wifi_scenarios.systemui import scan_list


def test_scan_list_adds_ap_and_restores_it(monkeypatch) -> None:
    monkeypatch.setattr(scan_list.time, "sleep", Mock())
    monkeypatch.setattr(
        scan_list,
        "scan_profile_entry",
        lambda *args: {"ssid": "ScanTarget", "pwd": "24681357"},
    )
    monkeypatch.setattr(scan_list, "open_internet_dialog", Mock())
    wait_for_ssid = Mock(return_value=("ScanTarget",))
    monkeypatch.setattr(scan_list, "wait_systemui_ssid", wait_for_ssid)
    monkeypatch.setattr(scan_list, "assert_ssid_visible_in_scan", Mock())
    wifi_ap_action = Mock()
    run_shell_cmd = Mock(return_value="Wi-Fi is enabled")

    scan_list.run_systemui_scan_list_case(
        "Func_Components_SystemUI_ScanList_UI_003",
        run_shell_cmd,
        Mock(),
        {},
        Mock(),
        wifi_ap_action,
    )

    wifi_ap_action.configure_wifi.assert_called_once()
    wait_for_ssid.assert_called_once()
    wifi_ap_action.teardown_wifi.assert_called_once_with()
    run_shell_cmd.assert_any_call("cmd wifi status")


def test_scan_list_disconnects_only_requested_dual_link(monkeypatch) -> None:
    entry = {
        "traditional_wifi": {"ssid": "WiFi"},
        "hyper_wifi": {"ssid": "HyperWiFi"},
    }
    monkeypatch.setattr(scan_list.time, "sleep", Mock())
    monkeypatch.setattr(
        scan_list,
        "assert_dual_rows",
        Mock(return_value=(entry, ["WiFi", "HyperWiFi"])),
    )
    monkeypatch.setattr(scan_list, "open_internet_dialog", Mock())
    wifi = Mock()
    wifi.forget_targets_for_connected_ssids.return_value = [("7", "WiFi")]
    wifi.list_connected_ssids.return_value = ["HyperWiFi"]

    scan_list.run_systemui_scan_list_case(
        "Func_Components_SystemUI_ScanList_Int_005", Mock(), wifi, {}, Mock()
    )

    wifi.forget_targets_for_connected_ssids.assert_called_once_with(["WiFi"])
    wifi.forget_network.assert_called_once_with("7")
