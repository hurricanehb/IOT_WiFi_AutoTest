from core.libs.android.wifi_scenarios.settings.scan_list import (
    row_rssi,
    scan_list_user_dual_entry,
    settings_scan_rows,
)


def test_settings_scan_rows_extracts_only_wifi_entries() -> None:
    hierarchy = """
<hierarchy><node>
  <node clickable="true" bounds="[0,168][720,284]" content-desc="">
    <node text="WLAN" resource-id="android:id/title" />
  </node>
  <node clickable="true" bounds="[0,286][720,431]" content-desc="Lab_AP,[{aa=2412,-55,Wi-Fi 6,0s}],WLAN 信号满格。,安全网络">
    <node text="Lab_AP" resource-id="android:id/title" />
    <node resource-id="android:id/icon" />
  </node>
  <node clickable="true" bounds="[0,431][720,576]" content-desc="Open_AP,[{bb=2412,-70,Wi-Fi 5,0s}],WLAN 信号强度为三格。">
    <node text="Open_AP" resource-id="android:id/title" />
  </node>
</node></hierarchy>
"""

    rows = settings_scan_rows(hierarchy)

    assert [row.ssid for row in rows] == ["Lab_AP", "Open_AP"]
    assert [row_rssi(row) for row in rows] == [-55, -70]


def test_scan_list_user_dual_entry_uses_declared_dual_wifi_profile() -> None:
    wifi_yaml = {
        "dual_wifi_list": [
            {
                "id": "dual_wifi_24g_hyperwifi_us",
                "traditional_wifi": {"ssid": "Lab_HW_AutoTest"},
                "hyper_wifi": {"ssid": "Lab_AT1_HyperWiFi_test_1"},
            }
        ]
    }

    entry = scan_list_user_dual_entry(wifi_yaml)

    assert entry["traditional_wifi"]["ssid"] == "Lab_HW_AutoTest"
    assert entry["hyper_wifi"]["ssid"] == "Lab_AT1_HyperWiFi_test_1"
