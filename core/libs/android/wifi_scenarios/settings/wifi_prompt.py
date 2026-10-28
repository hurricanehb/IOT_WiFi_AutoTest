"""Settings guidance prompts shown for the alternate WiFi link type."""
from __future__ import annotations

import re
import time
from collections.abc import Callable
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry

HYPER_GUIDANCE = (
    "您可以再连接 Hyper Wi-Fi，提供超强网络覆盖范围，跨楼层的穿透能力。"
)
WIFI_GUIDANCE = (
    "Hyper Wi-Fi 技术可支持您再连接一个备选网络，获得更稳定的上网体验。"
)


def normalize_guidance(text: str) -> str:
    return re.sub(r"\s+", "", (text or "").replace("‑", "-")).casefold()


def hierarchy_has_guidance(hierarchy: str, expected: str) -> bool:
    wanted = normalize_guidance(expected)
    root = ElementTree.fromstring(hierarchy)
    return any(
        wanted in normalize_guidance(
            f"{node.get('text', '')} {node.get('content-desc', '')}"
        )
        for node in root.iter("node")
    )


def _dual_legs(wifi_yaml: dict) -> tuple[WiFiEntry, WiFiEntry]:
    entry = get_dual_wifi_entry(
        wifi_yaml,
        entry_id="dual_wifi_24g_hyperwifi_us",
    )
    traditional = entry.get("traditional_wifi")
    hyper = entry.get("hyper_wifi")
    if not isinstance(traditional, dict) or not isinstance(hyper, dict):
        pytest.skip("dual_wifi_24g_hyperwifi_us 缺少传统 WiFi 或 HyperWiFi 配置")
    return traditional, hyper


def _wait_for_guidance(
    settings_ui: AndroidSettingsUI,
    expected: str,
    target_ssid: str,
    *,
    timeout: float = 15.0,
) -> str:
    deadline = time.monotonic() + timeout
    hierarchy = ""
    settings_ui.open_wifi_settings()
    while time.monotonic() < deadline:
        hierarchy = settings_ui.device.dump_hierarchy()
        if hierarchy_has_guidance(hierarchy, expected) and target_ssid in hierarchy:
            return hierarchy
        settings_ui.device.shell("cmd wifi start-scan")
        time.sleep(1.0)
    settings_ui.fail_with_artifacts(f"WLAN 列表未显示引导提示 {expected!r}")
    return hierarchy


@allure.step("执行 Settings WLAN 引导接入提示语验证")
def run_settings_wifi_prompt_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    traditional, hyper = _dual_legs(wifi_yaml)
    if summary.endswith("UI_001"):
        source = traditional
        target = hyper
        expected = HYPER_GUIDANCE
    elif summary.endswith("UI_002"):
        source = hyper
        target = traditional
        expected = WIFI_GUIDANCE
    else:
        raise ValueError(f"未知 Settings WiFiPrompt 用例: {summary}")

    source_ssid = str(source.get("ssid") or "")
    target_ssid = str(target.get("ssid") or "")
    if not source_ssid or not target_ssid:
        pytest.skip(f"{summary}: 双链路测试数据缺少 SSID")

    try:
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        if not wifi.connect_wifi_block(source):
            pytest.fail(f"{summary}: 无法连接前置网络 {source_ssid!r}")
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if source_ssid not in connected:
            pytest.fail(
                f"{summary}: 前置网络未关联，期望={source_ssid!r}，实际={connected!r}"
            )

        _wait_for_guidance(settings_ui, expected, target_ssid)
        print(
            f"[{summary}] 已连接 {source_ssid!r}，"
            f"目标 {target_ssid!r} 引导提示正确: {expected}"
        )
    finally:
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)