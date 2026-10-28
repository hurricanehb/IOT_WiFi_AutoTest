"""WiFi association orchestration and validation helpers."""
from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, List, Optional, cast

import pytest

from core.testdata_loader import (
    dual_wifi_ssids,
    get_dual_wifi_entry,
    get_dual_wifi_entry_by_region,
    get_expected_connected_ssids,
    get_wifi_list_entry,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import DualWiFiEntry, WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import ssid_match
from core.utils.device_log_export import export_device_packlogs
from core.utils.log_handler import get_logger

log = get_logger(__name__)


def any_configured_ap_connected(wifi: WiFiControl, wifi_yaml: dict) -> bool:
    """Return True when any expect=connected SSID in wifi_ssid.yaml is associated."""
    names = get_expected_connected_ssids(wifi_yaml)
    if not names:
        return False
    found, _ = wifi.match_associated_ssids(names, use_dumpsys_for_missing=False)
    if found:
        return True
    found, _ = wifi.match_associated_ssids(names, use_dumpsys_for_missing=True)
    return bool(found)


def assert_dual_wifi_connected(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    *,
    hyper_region: str,
    entry_id: Optional[str] = None,
    failure_label: str = "",
    export_logs_on_fail: bool = True,
) -> list[str]:
    """Ensure and verify both traditional_wifi and hyper_wifi are associated."""
    entry = cast(
        Optional[DualWiFiEntry],
        get_dual_wifi_entry(wifi_yaml, entry_id=entry_id)
        if entry_id
        else get_dual_wifi_entry_by_region(wifi_yaml, region=hyper_region),
    )
    if not entry:
        reason = (
            f"wifi_ssid.yaml 无 region={hyper_region!r} 的双 WiFi 配置"
            + (f" / id={entry_id!r}" if entry_id else "")
        )
        pytest.skip(reason)

    targets = dual_wifi_ssids(entry)
    if len(targets) < 2:
        pytest.fail(
            f"双 WiFi 配置不完整 id={entry.get('id')!r} targets={targets!r}"
        )
    if not wifi.set_wifi_enabled(True):
        pytest.fail("无法打开 WiFi 射频")
    time.sleep(0.5)

    found, missing = wifi.match_associated_ssids(
        targets, use_dumpsys_for_missing=True
    )
    if not missing:
        log.info("双 WiFi 已连接：%r（配置 id=%r）", found, entry.get("id"))
        return found

    ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
    if ok:
        log.info("双 WiFi 连接完成：%r（配置 id=%r）", found, entry.get("id"))
        return found

    status = run_shell_cmd("cmd wifi status")
    networks = wifi.list_networks_blob()
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    log_path: Optional[Path] = None
    if export_logs_on_fail:
        log_path = export_device_packlogs(
            wifi.adb,
            reason="dual_wifi_reconnect_failed",
            label=failure_label or f"dual_wifi_{hyper_region}",
        )

    message = (
        f"双 WiFi 未全部连接：需要 {targets!r}，已识别 {found!r}，缺失 {missing!r}；"
        f"list_connected={connected!r}\n"
        f"cmd wifi status:\n{status}\n"
        f"list-networks:\n{networks[:800]}"
    )
    if log_path:
        message += f"\n设备日志已导出：{log_path}"
    pytest.fail(message)


def assert_wifi_connected(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    *,
    index: Optional[int] = None,
    ssid: Optional[str] = None,
    entry: Optional[WiFiEntry] = None,
    allow_any_configured: bool = False,
) -> str:
    """Connect to a target AP from wifi_ssid.yaml and validate association."""
    if entry is None:
        entry = cast(
            Optional[WiFiEntry],
            get_wifi_list_entry(wifi_yaml, index=index, ssid=ssid),
        )
    if not entry:
        pytest.skip("wifi_ssid.yaml 无可用 AP 配置")
    target = str(entry.get("ssid") or "")

    if not wifi.set_wifi_enabled(True):
        pytest.fail("无法打开 WiFi 射频")
    time.sleep(0.5)
    configured = get_expected_connected_ssids(wifi_yaml)
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    current = connected[0] if connected else ""

    if allow_any_configured and any_configured_ap_connected(wifi, wifi_yaml):
        log.info(
            "WiFi 已联网：当前 SSID=%r，配置内 AP=%r，跳过 connect-network",
            current,
            configured,
        )
        return current or target

    if not wifi.ensure_wifi_connected(entry):
        status = run_shell_cmd("cmd wifi status")
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        current = connected[0] if connected else ""
        attempts = (
            wifi.last_connect_attempts()
            if hasattr(wifi, "last_connect_attempts")
            else []
        )
        log.info("cmd wifi status：\n%s", status)
        pytest.fail(
            f"未能关联到 AP {target!r}（已尝试断开并连接，当前={current!r}）。"
            f"配置 AP：{configured!r}\n"
            f"connect-network 尝试：{attempts!r}\n"
            f"cmd wifi status:\n{status[:800]}"
        )

    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    current = connected[0] if connected else ""
    status = run_shell_cmd("cmd wifi status")
    log.info("WiFi 连接校验：目标 SSID=%r，当前 SSID=%r", target, current)
    log.info("cmd wifi status：\n%s", status)
    if allow_any_configured and any_configured_ap_connected(wifi, wifi_yaml):
        return current or target

    found, _ = wifi.match_associated_ssids([target], use_dumpsys_for_missing=True)
    if not found and not ssid_match(target, current):
        pytest.fail(f"WiFi 未连接成功：预期 SSID={target!r}，实际={current!r}")
    if status and "disabled" in status.lower() and target.lower() not in status.lower():
        pytest.fail(f"WiFi status 显示关闭但已关联 {target!r}：\n{status[:400]}")
    return (found[0] if found else current) or target