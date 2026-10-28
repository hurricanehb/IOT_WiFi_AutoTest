"""Configuration and control for the laboratory attenuator."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
import re
import time
from typing import Protocol

from core.utils.telnet_helper import TelnetClient


_ATT_RESPONSE_RE = re.compile(
    r"^ATT\s+(?P<channel>\d+)\s+(?P<value>\d+(?:\.\d+)?)$",
    re.IGNORECASE,
)
_ATT_PAIR_RE = re.compile(r"^(?P<channel>\d+)\s+(?P<value>\d+(?:\.\d+)?)$")
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


@dataclass(frozen=True)
class AttenuatorDeviceConfig:
    host: str = ""
    port: int = 50000
    timeout_sec: float = 5.0
    max_attenuation_db: float = 122.0


@dataclass(frozen=True)
class AttenuatorChannelMap:
    mini_ap_1: int = 13
    traditional_ap_1: int = 14
    mini_ap_2: int = 15
    traditional_ap_2: int = 16


class AttenuatorProtocolError(RuntimeError):
    """Raised when the attenuator returns an invalid or rejected response."""


class _LineClient(Protocol):
    @property
    def connected(self) -> bool: ...

    def connect(self) -> None: ...

    def close(self) -> None: ...

    def write_line(self, line: str, end: str | None = None) -> None: ...

    def read_until(
        self, pattern: str | bytes, timeout_sec: float | None = None
    ) -> bytes: ...


ClientFactory = Callable[..., _LineClient]


class HJRadioRack:
    """Control one HJ Radio Rack; all endpoint values are supplied by callers."""

    def __init__(
        self,
        host: str,
        port: int,
        timeout_sec: float,
        max_attenuation_db: float,
        client_factory: ClientFactory = TelnetClient,
    ) -> None:
        if not host.strip():
            raise ValueError("host must not be empty")
        if not 1 <= port <= 65535:
            raise ValueError("port must be between 1 and 65535")
        if timeout_sec <= 0:
            raise ValueError("timeout_sec must be positive")
        if max_attenuation_db <= 0:
            raise ValueError("max_attenuation_db must be positive")

        self.host = host.strip()
        self.port = port
        self.timeout_sec = timeout_sec
        self.max_attenuation_db = float(max_attenuation_db)
        self._client = client_factory(
            self.host,
            port=self.port,
            timeout_sec=self.timeout_sec,
            newline="\r\n",
            encoding="ascii",
        )

    @property
    def connected(self) -> bool:
        return self._client.connected

    def connect(self) -> None:
        self._client.connect()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HJRadioRack:
        self.connect()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def read_attenuations(self) -> dict[int, float]:
        return self._parse_multi_response(self._request("ATT"))

    def set_attenuation(self, channel: int, attenuation_db: float) -> float:
        channel_number = self._validated_channel(channel)
        expected = self._validated_value(attenuation_db)
        response = self._request(
            f"ATT {channel_number} {self._format_db(expected)}"
        )
        actual = self._parse_single_response(response, channel_number)
        if actual != expected:
            raise AttenuatorProtocolError(
                f"channel {channel_number} returned {actual:g} dB, "
                f"expected {expected:g} dB"
            )
        return actual

    def set_attenuations(self, values: Mapping[int, float]) -> dict[int, float]:
        if not values:
            raise ValueError("values must not be empty")
        expected = {
            self._validated_channel(channel): self._validated_value(value)
            for channel, value in values.items()
        }
        assignments = ";".join(
            f"{channel} {self._format_db(value)}"
            for channel, value in expected.items()
        )
        actual = self._parse_multi_response(self._request(f"ATT {assignments}"))
        if actual != expected:
            raise AttenuatorProtocolError(
                f"device returned {actual!r}, expected {expected!r}"
            )
        return actual

    def set_socket_timeout(self, minutes: int) -> None:
        if minutes < 0:
            raise ValueError("minutes must be zero or positive")
        response = self._request(f"TIMEOUT {minutes}")
        if response.upper() != "OK":
            raise AttenuatorProtocolError(
                f"TIMEOUT command rejected by {self.host}: {response!r}"
            )

    def _request(self, command: str) -> str:
        if not self.connected:
            raise ConnectionError("attenuator is not connected")
        self._client.write_line(command)
        deadline = time.monotonic() + self.timeout_sec
        while (remaining := deadline - time.monotonic()) > 0:
            raw = self._client.read_until(b"\n", timeout_sec=remaining)
            if not raw:
                break
            for line in raw.decode("ascii", errors="replace").splitlines():
                response = _ANSI_ESCAPE_RE.sub("", line).strip()
                if response:
                    return response
        raise AttenuatorProtocolError(
            f"no response from {self.host} for command {command!r}"
        )

    @staticmethod
    def _validated_channel(channel: int) -> int:
        if isinstance(channel, bool) or not isinstance(channel, int) or channel <= 0:
            raise ValueError("channel must be a positive integer")
        return channel

    def _validated_value(self, attenuation_db: float) -> float:
        value = float(attenuation_db)
        if not 0 <= value <= self.max_attenuation_db:
            raise ValueError(
                f"attenuation_db must be between 0 and {self.max_attenuation_db:g}"
            )
        return value

    @staticmethod
    def _format_db(value: float) -> str:
        return f"{value:g}"

    @staticmethod
    def _parse_single_response(response: str, channel: int) -> float:
        match = _ATT_RESPONSE_RE.fullmatch(response.rstrip(";").strip())
        if match is None or int(match.group("channel")) != channel:
            raise AttenuatorProtocolError(f"invalid ATT response: {response!r}")
        return float(match.group("value"))

    @staticmethod
    def _parse_multi_response(response: str) -> dict[int, float]:
        result: dict[int, float] = {}
        for index, item in enumerate(response.split(";")):
            text = item.strip()
            if not text:
                continue
            match = (
                _ATT_RESPONSE_RE.fullmatch(text)
                if index == 0
                else _ATT_PAIR_RE.fullmatch(text) or _ATT_RESPONSE_RE.fullmatch(text)
            )
            if match is None:
                raise AttenuatorProtocolError(f"invalid ATT response: {response!r}")
            result[int(match.group("channel"))] = float(match.group("value"))
        if not result:
            raise AttenuatorProtocolError(f"invalid ATT response: {response!r}")
        return result


class ConfiguredAttenuatorRig:
    """Map laboratory AP roles to physical attenuator channels."""

    def __init__(
        self,
        driver: HJRadioRack,
        channels: AttenuatorChannelMap,
    ) -> None:
        self._driver = driver
        self._channels = channels

    @property
    def max_attenuation_db(self) -> float:
        return self._driver.max_attenuation_db

    def channel_for(self, *, hyper: bool, ap_index: int = 1) -> int:
        if ap_index not in (1, 2):
            raise ValueError("ap_index must be 1 or 2")
        prefix = "mini_ap" if hyper else "traditional_ap"
        return int(getattr(self._channels, f"{prefix}_{ap_index}"))

    def read_attenuations(self) -> dict[int, float]:
        return self._driver.read_attenuations()

    def set_attenuation(self, channel: int, attenuation_db: float) -> float:
        return self._driver.set_attenuation(channel, attenuation_db)