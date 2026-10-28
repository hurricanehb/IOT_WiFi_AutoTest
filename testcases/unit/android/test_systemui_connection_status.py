from unittest.mock import Mock

from core.libs.android.wifi_scenarios.systemui import connection_status


def test_connected_state_requires_connected_layout(monkeypatch) -> None:
    hierarchy = (
        '<node resource-id="com.android.systemui:id/wifi_connected_layout">'
        '<node text="Lab_AP" /></node>'
    )
    monkeypatch.setattr(connection_status, "open_internet_dialog", Mock())
    monkeypatch.setattr(
        connection_status,
        "capture_systemui",
        Mock(return_value=hierarchy),
    )

    result = connection_status.assert_systemui_connected_state(
        "case", Mock(), ["Lab_AP"], internet=True
    )

    assert result == hierarchy


def test_connected_case_dispatches_to_systemui_assertion(monkeypatch) -> None:
    assert_connected = Mock(return_value="Lab_AP")
    assert_systemui = Mock()
    monkeypatch.setattr(connection_status, "assert_wifi_connected", assert_connected)
    monkeypatch.setattr(
        connection_status, "assert_systemui_connected_state", assert_systemui
    )
    monkeypatch.setattr(
        connection_status,
        "scan_profile_entry",
        Mock(return_value={"ssid": "Lab_AP", "pwd": "24681357"}),
    )
    monkeypatch.setattr(connection_status, "configure_scan_ap", Mock())
    monkeypatch.setattr(connection_status, "assert_ssid_visible_in_scan", Mock())
    wifi_ap_action = Mock()

    connection_status.run_systemui_conn_status_case(
        "Func_Components_SystemUI_ConnStat_UI_001",
        Mock(),
        Mock(),
        {},
        Mock(),
        wifi_ap_action,
    )

    assert_connected.assert_called_once()
    assert_systemui.assert_called_once()
    wifi_ap_action.teardown_wifi.assert_called_once_with()
