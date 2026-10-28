from types import SimpleNamespace
from typing import cast

from core.libs.access_points.miniap import MiniAPAction
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios import channel_plan as wifi_channel_scenarios


def test_miniap_radio_controls_use_halow_service() -> None:
    action = object.__new__(MiniAPAction)
    commands = []
    action._login_miniap = lambda: None
    action._cmd = lambda command: commands.append(command) or ""

    action.stop_radio()
    action.start_radio(wait_sec=0)

    assert commands == [
        "/etc/init.d/halow stop",
        "/etc/init.d/halow start",
    ]


def test_wait_for_miniap_ready_requires_consecutive_logins() -> None:
    action = object.__new__(MiniAPAction)
    outcomes = iter((None, ConnectionError("restarting"), None, None))
    calls = []

    def login() -> None:
        calls.append(None)
        outcome = next(outcomes)
        if outcome is not None:
            raise outcome

    action._login_miniap = login

    action._wait_for_miniap_ready(timeout_sec=1, interval_sec=0)

    assert len(calls) == 4


def test_us_channel_case_synchronizes_miniap_wifi_profile() -> None:
    class RecordingAction:
        def __init__(self) -> None:
            self.profiles = []
            self.channels = []

        def set_wifi_profile(self, **kwargs) -> None:
            self.profiles.append(kwargs)

        def set_bandwidth_channel(self, bandwidth, channel) -> None:
            self.channels.append((bandwidth, channel))

    action = RecordingAction()
    original_assert = wifi_channel_scenarios.assert_wifi_connected
    wifi_channel_scenarios.assert_wifi_connected = lambda *args, **kwargs: None
    try:
        wifi_channel_scenarios.run_channel_automation_case(
            {"case_id": "halow-us", "title": "Sub 1G-US", "tag": "HyperWiFi"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {
                "wifi_list": [
                    {
                        "ssid": "HyperWi-Fi_US",
                        "pwd": "24681357",
                        "encrypt": "WPA3",
                        "type": "hyperwifi",
                        "region": "US",
                    }
                ]
            },
            plan={
                "driver": "miniAP",
                "country": "US",
                "bandwidths": [{"mhz": 1, "channels": [3]}],
            },
            miniap_action=action,
        )
    finally:
        wifi_channel_scenarios.assert_wifi_connected = original_assert

    assert action.profiles == [
        {"ssid": "HyperWi-Fi_US", "pwd": "24681357", "encryption": "WPA3"}
    ]
    assert action.channels == [(1, 3)]
