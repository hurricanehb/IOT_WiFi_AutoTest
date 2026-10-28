from unittest.mock import Mock

import pytest

from core.libs.android.wifi_scenarios.systemui import encryption_icon
from core.libs.android.wifi_scenarios.systemui.encryption_icon import (
    assert_encryption_icon,
)


def test_encryption_icon_matches_lock_resource() -> None:
    settings_ui = Mock()
    settings_ui.device.dump_hierarchy.return_value = """
        <hierarchy><node resource-id="com.android.systemui:id/wifi_list">
          <node resource-id="com.android.systemui:id/wifi_title" text="Secure_AP" />
          <node resource-id="com.android.systemui:id/wifi_end_icon" />
        </node></hierarchy>
    """
    scan_blob = "aa:bb:cc:dd:ee:ff 5180 -50 0 Secure_AP [WPA2-PSK-CCMP][ESS]"

    assert_encryption_icon("case", settings_ui, scan_blob, "Secure_AP", encrypted=True)


def test_encryption_icon_rejects_lock_for_open_network() -> None:
    settings_ui = Mock()
    settings_ui.device.dump_hierarchy.return_value = """
        <hierarchy><node resource-id="com.android.systemui:id/wifi_list">
          <node resource-id="com.android.systemui:id/wifi_title" text="Open_AP" />
          <node resource-id="com.android.systemui:id/wifi_end_icon" />
        </node></hierarchy>
    """

    with pytest.raises(pytest.fail.Exception, match="锁图标"):
        assert_encryption_icon("case", settings_ui, "", "Open_AP", encrypted=False)


def test_encrypt_icon_runs_supported_encrypted_matrix(monkeypatch) -> None:
    monkeypatch.setattr(encryption_icon, "assert_ssid_visible_in_scan", Mock())
    monkeypatch.setattr(
        encryption_icon,
        "scan_result_capabilities",
        lambda blob, ssid: [
            "SAE"
            if ssid.endswith("WPA3")
            else "WPA2-PSK"
            if ssid.endswith("WPA2")
            else "WPA-PSK"
        ],
    )
    monkeypatch.setattr(encryption_icon, "open_internet_dialog", Mock())
    monkeypatch.setattr(
        encryption_icon,
        "visible_systemui_ssids",
        lambda ui: ("PyAutoTest_WPA", "PyAutoTest_WPA2", "PyAutoTest_WPA3"),
    )
    monkeypatch.setattr(encryption_icon, "assert_encryption_icon", Mock())
    monkeypatch.setattr(encryption_icon, "capture_systemui", Mock())
    wifi_ap_action = Mock()

    encryption_icon.run_systemui_encrypt_icon_case(
        "Func_Components_SystemUI_EncryptIcon_UI_001",
        Mock(return_value="scan"),
        Mock(),
        wifi_ap_action,
    )

    assert [
        item.kwargs["security"]
        for item in wifi_ap_action.configure_wifi.call_args_list
    ] == ["wpa-aes", "wpa2-aes", "wpa3-aes"]
    wifi_ap_action.teardown_wifi.assert_called_once_with()
