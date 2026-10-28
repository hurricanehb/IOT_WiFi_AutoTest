from collections.abc import Iterable

import pytest

from core.utils.attenuator import (
    AttenuatorChannelMap,
    AttenuatorProtocolError,
    ConfiguredAttenuatorRig,
    HJRadioRack,
)


class _RecordingClient:
    def __init__(self, *args, responses: Iterable[bytes] = (), **kwargs) -> None:
        self.connected = False
        self.commands: list[str] = []
        self.responses = iter(responses)

    def connect(self) -> None:
        self.connected = True

    def close(self) -> None:
        self.connected = False

    def write_line(self, command: str) -> None:
        self.commands.append(command)

    def read_until(self, pattern, timeout_sec=None) -> bytes:
        return next(self.responses)


def _attenuator(*responses: bytes) -> tuple[HJRadioRack, _RecordingClient]:
    client = _RecordingClient(responses=responses)
    attenuator = HJRadioRack(
        host="192.0.2.1",
        port=50000,
        timeout_sec=5.0,
        max_attenuation_db=122.0,
        client_factory=lambda *args, **kwargs: client,
    )
    attenuator.connect()
    return attenuator, client


def test_read_attenuations_parses_documented_response() -> None:
    attenuator, client = _attenuator(b"ATT 1 56;ATT 2 10\r\n")

    values = attenuator.read_attenuations()

    assert client.commands == ["ATT"]
    assert values == {1: 56.0, 2: 10.0}


def test_read_attenuations_parses_live_device_response() -> None:
    attenuator, _ = _attenuator(
        b"\x1b[2J\x1b[0;0H\r\n",
        b"ATT 1 0;2 0;13 36;15 122;\r\n",
    )

    assert attenuator.read_attenuations() == {
        1: 0.0,
        2: 0.0,
        13: 36.0,
        15: 122.0,
    }


def test_set_attenuation_sends_single_channel_command() -> None:
    attenuator, client = _attenuator(b"ATT 1 56;\r\n")

    result = attenuator.set_attenuation(1, 56)

    assert client.commands == ["ATT 1 56"]
    assert result == 56.0


def test_set_attenuations_sends_documented_multi_channel_command() -> None:
    attenuator, client = _attenuator(
        b"ATT 15 56;ATT 1 11;ATT 3 34;ATT 4 56\r\n"
    )

    result = attenuator.set_attenuations({15: 56, 1: 11, 3: 34, 4: 56})

    assert client.commands == ["ATT 15 56;1 11;3 34;4 56"]
    assert result == {15: 56.0, 1: 11.0, 3: 34.0, 4: 56.0}


def test_set_socket_timeout_accepts_ok_response() -> None:
    attenuator, client = _attenuator(b"OK\r\n")

    attenuator.set_socket_timeout(10)

    assert client.commands == ["TIMEOUT 10"]


@pytest.mark.parametrize("channel", [0, -1, True])
def test_set_attenuation_rejects_invalid_channel(channel) -> None:
    attenuator, client = _attenuator()

    with pytest.raises(ValueError, match="positive integer"):
        attenuator.set_attenuation(channel, 10)

    assert client.commands == []


@pytest.mark.parametrize("attenuation_db", [-0.1, 122.1])
def test_set_attenuation_rejects_out_of_range_value(attenuation_db: float) -> None:
    attenuator, client = _attenuator()

    with pytest.raises(ValueError, match="between 0 and 122"):
        attenuator.set_attenuation(1, attenuation_db)

    assert client.commands == []


def test_set_attenuation_rejects_mismatched_response() -> None:
    attenuator, _ = _attenuator(b"ATT 2 56\r\n")

    with pytest.raises(AttenuatorProtocolError, match="invalid ATT response"):
        attenuator.set_attenuation(1, 56)


def test_context_manager_closes_connection() -> None:
    client = _RecordingClient()

    with HJRadioRack(
        host="192.0.2.1",
        port=50000,
        timeout_sec=5.0,
        max_attenuation_db=122.0,
        client_factory=lambda *args, **kwargs: client,
    ) as attenuator:
        assert attenuator.connected

    assert not client.connected


def test_lab_channel_mapping_matches_current_wiring() -> None:
    attenuator, _ = _attenuator()
    rig = ConfiguredAttenuatorRig(attenuator, AttenuatorChannelMap())

    assert rig.channel_for(hyper=True, ap_index=1) == 13
    assert rig.channel_for(hyper=False, ap_index=1) == 14
    assert rig.channel_for(hyper=True, ap_index=2) == 15
    assert rig.channel_for(hyper=False, ap_index=2) == 16