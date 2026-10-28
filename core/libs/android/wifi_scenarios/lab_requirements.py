"""Shared environment gates for Android laboratory scenarios."""
from __future__ import annotations

import os

import pytest

_ENABLED_VALUES = frozenset(("1", "true", "yes", "on"))


def env_value(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip().lower()


def env_enabled(name: str, default: str = "0") -> bool:
    return env_value(name, default) in _ENABLED_VALUES


def require_env_value(
    name: str,
    expected: str,
    summary: str,
    *,
    hint: str = "",
) -> None:
    want = (expected or "").strip().lower()
    got = env_value(name)
    if got == want:
        return
    extra = f"；{hint}" if hint else ""
    pytest.skip(f"{summary}: 需 {name}={want!r}，当前={got!r}{extra}")


def require_lab_flag(flag: str, summary: str, *, hint: str) -> None:
    if env_enabled(flag):
        return
    pytest.skip(f"{summary}: 需设置 {flag}=1；{hint}")