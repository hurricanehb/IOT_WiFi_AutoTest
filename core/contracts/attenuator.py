"""Contracts exposed by laboratory attenuation equipment."""

from __future__ import annotations

from typing import Protocol


class AttenuatorRig(Protocol):
    """Signal-scenario view of an attenuator and its laboratory wiring."""

    @property
    def max_attenuation_db(self) -> float: ...

    def channel_for(self, *, hyper: bool, ap_index: int = 1) -> int: ...

    def read_attenuations(self) -> dict[int, float]: ...

    def set_attenuation(self, channel: int, attenuation_db: float) -> float: ...