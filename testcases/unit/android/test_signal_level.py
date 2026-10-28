from types import SimpleNamespace
from typing import cast

import pytest
from PIL import Image

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios import signal_level
from core.libs.android.wifi_scenarios.signal_level import (
    run_signal_level_case,
    signal_bars_for_ssid,
    signal_bars_from_icon,
    signal_level_entry,
    signal_level_spec,
    tune_attenuation_for_rssi,
    wifi_icon_bounds_for_ssid,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


class _FakeAttenuator:
    def __init__(self, original: float = 12.0) -> None:
        self.max_attenuation_db = 122.0
        self.original = original
        self.values: list[tuple[int, float]] = []

    def channel_for(self, *, hyper: bool, ap_index: int = 1) -> int:
        return 13 if hyper else 14

    def read_attenuations(self) -> dict[int, float]:
        return {13: self.original, 14: self.original}

    def set_attenuation(self, channel: int, attenuation_db: float) -> float:
        self.values.append((channel, attenuation_db))
        return attenuation_db


def test_signal_level_specs_use_terminal_half_open_boundaries() -> None:
    wifi = signal_level_spec("Func_Components_Settings_SignalLevel_UI_004")
    hyper = signal_level_spec("Func_Components_SystemUI_SignalLevel_UI_008")
    hyper_weak = signal_level_spec("Func_Components_SystemUI_SignalLevel_UI_009")

    assert (wifi.hyper, wifi.expected_bars, wifi.target_rssis) == (
        False,
        1,
        (-84, -86),
    )
    assert (hyper.hyper, hyper.expected_bars, hyper.target_rssis) == (
        True,
        2,
        (-88, -92),
    )
    assert (hyper_weak.hyper, hyper_weak.expected_bars, hyper_weak.target_rssis) == (
        True,
        1,
        (-95, -97),
    )


def test_signal_level_entry_resolves_explicit_lab_mapping() -> None:
    data = {
        "wifi_list": [{"id": "traditional", "ssid": "WiFi"}],
        "dual_wifi_list": [
            {"id": "pair", "hyper_wifi": {"ssid": "HyperWiFi"}}
        ],
        "signal_level_lab": {
            "traditional_entry_id": "traditional",
            "hyper_dual_entry_id": "pair",
            "ap_index": 2,
        },
    }

    assert signal_level_entry(data, hyper=False) == (
        {"id": "traditional", "ssid": "WiFi"},
        2,
    )
    assert signal_level_entry(data, hyper=True) == (
        {"ssid": "HyperWiFi"},
        2,
    )


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("Lab_AP,[...],WLAN 信号满格。,安全网络", 4),
        ("Lab_AP,[...],WLAN 信号强度为三格。,安全网络", 3),
        ("Lab_AP,[...],WLAN 信号强度为两格。,安全网络", 2),
        ("Lab_AP,[...],WLAN 信号强度为一格。,安全网络", 1),
        ("Lab_AP,[...],WLAN 信号强度为零格。,安全网络", 0),
    ],
)
def test_signal_bars_for_settings_description(
    description: str, expected: int
) -> None:
    hierarchy = f'<hierarchy><node content-desc="{description}" /></hierarchy>'

    assert signal_bars_for_ssid(hierarchy, "Lab_AP") == expected


def test_signal_bars_for_systemui_row() -> None:
    hierarchy = """
<hierarchy><node content-desc="">
  <node text="Lab_AP" resource-id="com.android.systemui:id/wifi_title" />
  <node content-desc="WLAN 信号强度为两格。" resource-id="com.android.systemui:id/wifi_icon" />
</node></hierarchy>
"""

    assert signal_bars_for_ssid(hierarchy, "Lab_AP") == 2


def test_wifi_icon_bounds_for_connected_ssid() -> None:
    hierarchy = """
<hierarchy><node>
  <node text="Lab_AP" resource-id="com.android.systemui:id/wifi_connected_title" />
  <node resource-id="com.android.systemui:id/wifi_connected_icon" bounds="[596,627][636,667]" />
</node></hierarchy>
"""

    assert wifi_icon_bounds_for_ssid(hierarchy, "Lab_AP") == (596, 627, 636, 667)


@pytest.mark.parametrize(("bars", "top_arc"), [(4, 4), (3, 7), (2, 10), (1, 13)])
def test_signal_bars_from_icon_uses_top_visible_arc(bars: int, top_arc: int) -> None:
    icon = Image.new("L", (20, 20), 255)
    for x in range(6, 14):
        icon.putpixel((x, top_arc), 100)

    assert signal_bars_from_icon(icon) == bars


def test_signal_bars_from_blank_icon_is_zero() -> None:
    assert signal_bars_from_icon(Image.new("L", (20, 20), 255)) == 0


def test_tune_attenuation_uses_monotonic_rssi_feedback() -> None:
    attenuator = _FakeAttenuator()

    attenuation, measured = tune_attenuation_for_rssi(
        cast(AttenuatorRig, attenuator),
        14,
        -70,
        lambda: -40 - int(attenuator.values[-1][1]),
        settle_sec=0,
    )

    assert measured == -70
    assert attenuation == 30


def test_tune_attenuation_reaches_weak_rssi_beyond_twelve_steps() -> None:
    attenuator = _FakeAttenuator()

    attenuation, measured = tune_attenuation_for_rssi(
        cast(AttenuatorRig, attenuator),
        13,
        -93,
        lambda: -22 - int(attenuator.values[-1][1]),
        settle_sec=0,
    )

    assert measured == -92
    assert attenuation == 70


def test_tune_attenuation_limits_adjustment_in_weak_signal_region() -> None:
    attenuator = _FakeAttenuator()

    tune_attenuation_for_rssi(
        cast(AttenuatorRig, attenuator),
        13,
        -95,
        lambda: -22 - int(attenuator.values[-1][1]),
        settle_sec=0,
    )

    values = [value for _, value in attenuator.values]
    weak_index = values.index(66)
    assert all(
        later - earlier <= 2
        for earlier, later in zip(values[weak_index:], values[weak_index + 1 :])
    )


def test_tune_attenuation_ignores_one_transient_missing_read() -> None:
    attenuator = _FakeAttenuator()
    readings = iter((-60, None, -72, None, None))

    attenuation, measured = tune_attenuation_for_rssi(
        cast(AttenuatorRig, attenuator),
        13,
        -99,
        lambda: next(readings),
        settle_sec=0,
        allow_missing=True,
    )

    assert measured is None
    assert attenuation == 12
    assert [value for _, value in attenuator.values] == [0, 6, 6, 12, 12]


def test_tune_attenuation_does_not_accept_missing_for_nonzero_bars() -> None:
    attenuator = _FakeAttenuator()

    with pytest.raises(pytest.fail.Exception, match="无法达到目标 RSSI"):
        tune_attenuation_for_rssi(
            cast(AttenuatorRig, attenuator),
            13,
            -93,
            lambda: -90 if attenuator.values[-1][1] <= 79 else None,
            settle_sec=0,
        )


def test_tune_attenuation_never_sets_negative_value_when_rssi_is_missing() -> None:
    attenuator = _FakeAttenuator()

    with pytest.raises(pytest.fail.Exception, match="无法读取 RSSI"):
        tune_attenuation_for_rssi(
            cast(AttenuatorRig, attenuator),
            14,
            -60,
            lambda: None,
            settle_sec=0,
        )

    assert attenuator.values
    assert all(value >= 0 for _, value in attenuator.values)


def test_traditional_rssi_reader_falls_back_to_connected_status() -> None:
    commands: list[str] = []

    def run_shell(command: str) -> str:
        commands.append(command)
        return (
            'Wifi is connected to "Lab_AP"\n'
            'WifiInfo: SSID: "Lab_AP", BSSID: 00:11:22:33:44:55, RSSI: -61, '
            'Frequency: 2412MHz'
        )

    read_rssi = signal_level._traditional_rssi_reader(run_shell, "Lab_AP")

    assert read_rssi() == -61
    assert commands == [
        "cmd wifi start-scan",
        "cmd wifi list-scan-results",
        "cmd wifi status",
    ]


def test_traditional_rssi_reader_tracks_connected_bssid() -> None:
    def run_shell(command: str) -> str:
        if command == "cmd wifi list-scan-results":
            return """\
54:f6:e2:e9:4a:40 2412 -72(0:-72) 1s Lab_AP [WPA2-PSK-CCMP][ESS]
54:f6:e2:e9:5a:40 2412 -48(0:-48) 1s Lab_AP [WPA2-PSK-CCMP][ESS]
"""
        return ""

    read_rssi = signal_level._traditional_rssi_reader(
        run_shell,
        "Lab_AP",
        "54:f6:e2:e9:4a:40",
    )

    assert read_rssi() == -72


def test_run_signal_level_case_restores_original_attenuation(monkeypatch) -> None:
    attenuator = _FakeAttenuator(original=17)
    monkeypatch.setattr(
        signal_level,
        "signal_level_entry",
        lambda *args, **kwargs: (
            {"ssid": "Lab_AP", "pwd": "24681357", "type": "normal"},
            1,
        ),
    )
    monkeypatch.setattr(signal_level, "assert_wifi_connected", lambda *args, **kwargs: None)
    monkeypatch.setattr(signal_level, "_traditional_rssi_reader", lambda *args: lambda: -66)
    monkeypatch.setattr(
        signal_level,
        "tune_attenuation_for_rssi",
        lambda *args, **kwargs: (25.0, -66),
    )
    monkeypatch.setattr(
        signal_level,
        "_assert_ui_bars",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("UI mismatch")),
    )
    with pytest.raises(AssertionError, match="UI mismatch"):
        run_signal_level_case(
            "Func_Components_Settings_SignalLevel_UI_002",
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            cast(AndroidSettingsUI, SimpleNamespace()),
            cast(AttenuatorRig, attenuator),
            surface="settings",
            settle_sec=0,
        )

    assert attenuator.values[0] == (14, 0)
    assert attenuator.values[-1] == (14, 17)