from types import SimpleNamespace
from typing import cast

import pytest

from core.libs.access_points import miniap
from core.libs.access_points.miniap import MiniAPAction
from core.utils.config_loader import Settings
from core.utils.telnet_session import TelnetSession


class _RecordingSession:
    def __init__(self) -> None:
        self.commands = []

    def execute_command(self, command: str) -> str:
        self.commands.append(command)
        return ""

    def close(self) -> None:
        pass


def test_uci_set_quotes_shell_special_characters() -> None:
    session = _RecordingSession()
    settings = SimpleNamespace(
        miniAP_config=SimpleNamespace(),
        ap_config=SimpleNamespace(),
    )
    action = MiniAPAction(
        settings=cast(Settings, settings),
        session=cast(TelnetSession, session),
    )

    getattr(action, "_uci_set")("halow.ap.ssid", "lab's test; reboot")

    assert session.commands == [
        "uci set halow.ap.ssid='lab'\"'\"'s test; reboot'"
    ]


def test_wait_for_miniap_ready_retries_until_login_succeeds(monkeypatch) -> None:
    class RetryingSession:
        def __init__(self) -> None:
            self.login_calls = 0

        def login(self, *args) -> None:
            self.login_calls += 1
            if self.login_calls < 3:
                raise ConnectionError("miniAP is rebooting")

    session = RetryingSession()
    settings = SimpleNamespace(
        miniAP_config=SimpleNamespace(
            miniAP_ip="192.0.2.10",
            miniAP_root="root",
            miniAP_login_password="password",
            miniAP_flag="#",
        ),
        ap_config=SimpleNamespace(),
    )
    action = MiniAPAction(
        settings=cast(Settings, settings),
        session=cast(TelnetSession, session),
    )
    sleeps = []
    monkeypatch.setattr(miniap.time, "sleep", sleeps.append)

    getattr(action, "_wait_for_miniap_ready")(timeout_sec=1, interval_sec=0.1)

    assert session.login_calls == 3
    assert sleeps == [0.1, 0.1]


@pytest.mark.parametrize(
    "region,special_id",
    [("JP", "46434300"), ("US", "not-a-country-id")],
)
def test_set_countrycode_rejects_invalid_device_values(region, special_id) -> None:
    settings = SimpleNamespace(
        miniAP_config=SimpleNamespace(),
        ap_config=SimpleNamespace(),
    )
    action = MiniAPAction(
        settings=cast(Settings, settings),
        session=cast(TelnetSession, _RecordingSession()),
    )

    with pytest.raises(ValueError):
        action.set_countrycode(region, special_id, "ssid", "password")


def test_set_channel_rejects_non_positive_value() -> None:
    settings = SimpleNamespace(
        miniAP_config=SimpleNamespace(),
        ap_config=SimpleNamespace(),
    )
    action = MiniAPAction(
        settings=cast(Settings, settings),
        session=cast(TelnetSession, _RecordingSession()),
    )

    with pytest.raises(ValueError):
        action.set_channel("1; reboot")