from unittest.mock import Mock

from core.libs.android.wifi_scenarios.systemui import ssid_display


def test_ssid_display_configures_and_restores_ap(monkeypatch) -> None:
    monkeypatch.setattr(ssid_display.time, "sleep", Mock())
    monkeypatch.setattr(
        ssid_display,
        "get_ssid_pwd_entry",
        lambda *args, **kwargs: {
            "ssid": "测试网络",
            "password": "24681357",
            "ssid_encoding": "utf-8",
        },
    )
    monkeypatch.setattr(ssid_display, "assert_ssid_visible_in_scan", Mock())
    monkeypatch.setattr(ssid_display, "open_internet_dialog", Mock())
    monkeypatch.setattr(
        ssid_display, "visible_systemui_ssids", lambda ui: ("测试网络",)
    )
    monkeypatch.setattr(ssid_display, "capture_systemui", Mock())
    wifi_ap_action = Mock()

    ssid_display.run_systemui_ssid_display_case(
        "Func_Components_SystemUI_SsidShow_UI_001",
        Mock(return_value="scan"),
        {},
        Mock(),
        wifi_ap_action,
        settle_sec=0,
    )

    wifi_ap_action.configure_wifi.assert_called_once_with(
        ssid="测试网络",
        password="24681357",
        security="wpa2-aes",
        band="5g",
        ssid_encoding="utf-8",
        verify=True,
    )
    wifi_ap_action.teardown_wifi.assert_called_once_with()
