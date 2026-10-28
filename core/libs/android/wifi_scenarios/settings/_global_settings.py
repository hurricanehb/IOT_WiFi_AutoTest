"""Helpers for reading, mutating, and restoring Android global settings."""
from __future__ import annotations

from collections.abc import Callable


def global_setting(run_shell_cmd: Callable[[str], str], key: str) -> str:
    return run_shell_cmd(f"settings get global {key}").strip()


def set_global_setting(
    run_shell_cmd: Callable[[str], str],
    key: str,
    value: str,
) -> None:
    run_shell_cmd(f"settings put global {key} {value}")


def restore_global_setting(
    run_shell_cmd: Callable[[str], str],
    key: str,
    value: str,
) -> None:
    if value in ("", "null"):
        run_shell_cmd(f"settings delete global {key}")
    else:
        set_global_setting(run_shell_cmd, key, value)
