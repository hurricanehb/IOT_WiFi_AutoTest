from core.libs.android.wifi_scenarios.systemui import (
    systemui_connected_wifi_row,
    systemui_status_bar_wifi_icons,
)


def test_systemui_status_bar_wifi_icons_extracts_links_in_screen_order() -> None:
    hierarchy = """
    <hierarchy>
      <node resource-id="com.android.systemui:id/statusIcons">
        <node resource-id="com.android.systemui:id/sub_wifi_signal"
              content-desc="WLAN 信号满格。" bounds="[609,10][639,40]" />
        <node resource-id="com.android.systemui:id/wifi_signal"
              content-desc="WLAN 信号三格。" bounds="[575,10][605,40]" />
      </node>
    </hierarchy>
    """

    icons = systemui_status_bar_wifi_icons(hierarchy)

    assert [icon.link for icon in icons] == ["wifi", "hyper"]
    assert icons[0].bounds == (575, 10, 605, 40)
    assert icons[0].description == "WLAN 信号三格。"


def test_systemui_status_bar_wifi_icons_ignores_unrelated_icons() -> None:
    hierarchy = """
    <hierarchy>
      <node resource-id="com.android.systemui:id/mobile_signal" bounds="[1,2][3,4]" />
      <node resource-id="com.android.systemui:id/wifi_signal" bounds="invalid" />
    </hierarchy>
    """

    assert systemui_status_bar_wifi_icons(hierarchy) == ()


def test_systemui_connected_wifi_row_extracts_fixed_connected_row() -> None:
    hierarchy = """
    <hierarchy>
      <node resource-id="com.android.systemui:id/wifi_connected_layout">
        <node resource-id="com.android.systemui:id/wifi_connected_title" text="Lab_AP" />
        <node resource-id="com.android.systemui:id/wifi_connected_summary"
              text="已连接 standard = Wi‑Fi 6 rssi = -55" />
        <node resource-id="com.android.systemui:id/wifi_label" bounds="[479,627][540,667]" />
        <node resource-id="com.android.systemui:id/wifi_connected_icon" bounds="[596,627][636,667]" />
      </node>
    </hierarchy>
    """

    row = systemui_connected_wifi_row(hierarchy)

    assert row is not None
    assert row.ssid == "Lab_AP"
    assert "Wi‑Fi 6" in row.summary
    assert row.resources["com.android.systemui:id/wifi_label"] == (479, 627, 540, 667)
    assert row.resources["com.android.systemui:id/wifi_connected_icon"] == (
        596,
        627,
        636,
        667,
    )


def test_systemui_connected_wifi_row_returns_none_without_connected_layout() -> None:
    assert systemui_connected_wifi_row("<hierarchy />") is None