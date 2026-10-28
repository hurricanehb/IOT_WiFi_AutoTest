"""Shared helpers for Android Settings WiFi scenarios."""
from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from typing import cast

import pytest

from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import scan_result_ssids
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_expected_connected_ssids, get_wifi_list_entry
from core.utils.log_handler import get_logger

log = get_logger(__name__)


def wlan_list_blob(settings_ui: AndroidSettingsUI, *, settle_sec: float = 3.0) -> str:
    settings_ui.open_wifi_settings()
    time.sleep(settle_sec)
    return settings_ui.device.dump_hierarchy()


def find_status_text(blob: str, candidates: Sequence[str]) -> str:
    lower = (blob or "").lower()
    for text in candidates:
        if text.lower() in lower:
            return text
    return ""


def assert_status_text_present(
    blob: str,
    candidates: Sequence[str],
    *,
    summary: str,
    label: str,
) -> str:
    hit = find_status_text(blob, candidates)
    if not hit:
        pytest.fail(
            f"{summary}: WLAN 列表未显示{label}；候选文案={list(candidates)!r}"
        )
    log.info("%s: WLAN 列表命中%s文案 %r", summary, label, hit)
    return hit


def assert_status_text_absent(
    blob: str,
    candidates: Sequence[str],
    *,
    summary: str,
    label: str,
) -> None:
    hit = find_status_text(blob, candidates)
    if hit:
        pytest.fail(f"{summary}: WLAN 列表不应显示{label}，实际命中 {hit!r}")


def visible_ssids(
    run_shell_cmd: Callable[[str], str],
    *,
    scan_wait_sec: float = 6.0,
) -> list[str]:
    run_shell_cmd("cmd wifi start-scan")
    time.sleep(scan_wait_sec)
    return scan_result_ssids(run_shell_cmd("cmd wifi list-scan-results"))


def resolve_entry(
    wifi_yaml: dict,
    *,
    index: int | None,
    ssid: str | None,
    summary: str,
    run_shell_cmd: Callable[[str], str] | None = None,
) -> WiFiEntry:
    """Select a configured and currently visible AP when none is explicit."""
    if ssid is None and index is None and run_shell_cmd is not None:
        available = {name.lower() for name in visible_ssids(run_shell_cmd)}
        for name in get_expected_connected_ssids(wifi_yaml):
            if name.lower() in available:
                ssid = name
                break
        else:
            pytest.skip(
                f"{summary}: wifi_ssid.yaml 中 expect=connected 的 AP 均未扫描到，"
                f"可见 SSID={sorted(available)!r}"
            )

    entry = cast(
        WiFiEntry | None,
        get_wifi_list_entry(wifi_yaml, index=index, ssid=ssid),
    )
    if not entry or not (entry.get("ssid") or "").strip():
        pytest.skip(f"{summary}: wifi_ssid.yaml 无可用 AP 配置")
    log.info("%s: 选定目标 AP %r", summary, entry.get("ssid"))
    return entry
