"""SystemUI status-bar WiFi icon scenarios."""
from __future__ import annotations

import time
from collections.abc import Callable
from typing import cast

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.dual_link import (
    primary_backup_entry,
    primary_link_from_status,
    tune_dual_link_rssi,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.systemui_pages.quick_settings_page import capture_systemui
from core.libs.android.wifi_scenarios.systemui.parsers import (
    SystemUIStatusBarWifiIcon,
    systemui_status_bar_wifi_icons,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry


def _wait_for_status_bar_links(
    summary: str,
    settings_ui: AndroidSettingsUI,
    expected: set[str],
    stage: str,
    *,
    timeout: float = 20.0,
    expected_order: tuple[str, ...] | None = None,
) -> tuple[SystemUIStatusBarWifiIcon, ...]:
    settings_ui.device.press("home")
    deadline = time.monotonic() + timeout
    icons: tuple[SystemUIStatusBarWifiIcon, ...] = ()
    while time.monotonic() < deadline:
        hierarchy = settings_ui.device.dump_hierarchy()
        icons = systemui_status_bar_wifi_icons(hierarchy)
        actual_order = tuple(icon.link for icon in icons)
        if (
            {icon.link for icon in icons} == expected
            and len(icons) == len(expected)
            and (expected_order is None or actual_order == expected_order)
        ):
            capture_systemui(settings_ui, stage)
            print(
                f"[{summary}] 状态栏 {stage}: "
                f"{[(icon.link, icon.bounds) for icon in icons]!r}"
            )
            return icons
        time.sleep(0.5)
    settings_ui.fail_with_artifacts(
        f"{summary}: 状态栏 {stage} 图标不匹配，期望={sorted(expected)!r}，"
        f"期望顺序={expected_order!r}，"
        f"实际={[(icon.link, icon.bounds) for icon in icons]!r}"
    )
    raise AssertionError("unreachable")


def _forget_connected_ssid(wifi: WiFiControl, ssid: str) -> None:
    targets = wifi.forget_targets_for_connected_ssids([ssid])
    if not targets:
        pytest.fail(f"未找到已连接网络 {ssid!r} 的 network id")
    for network_id, _ in targets:
        if not wifi.forget_network(network_id):
            pytest.fail(f"断开网络 {ssid!r} 失败，network id={network_id!r}")


def _wait_for_status_primary(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    expected: str,
    *,
    timeout: float = 30.0,
) -> None:
    deadline = time.monotonic() + timeout
    status = ""
    while time.monotonic() < deadline:
        status = run_shell_cmd("cmd wifi status")
        if primary_link_from_status(status) == expected:
            allure.attach(status, "cmd wifi status - primary", allure.attachment_type.TEXT)
            return
        time.sleep(1.0)
    pytest.fail(
        f"{summary}: 等待 {expected} 成为 primary 超时，"
        f"实际={primary_link_from_status(status)!r}\n{status[:1200]}"
    )


@allure.step("执行 SystemUI 状态栏 WLAN 图标验证")
def run_systemui_status_bar_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    attenuator: AttenuatorRig | None = None,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
    if not entry:
        pytest.skip(f"{summary}: 缺少 dual_wifi_24g_hyperwifi_us 配置")
    if summary.endswith(("UI_005", "Int_005")):
        entry = primary_backup_entry(wifi_yaml)
    traditional = entry.get("traditional_wifi")
    hyper = entry.get("hyper_wifi")
    if not isinstance(traditional, dict) or not isinstance(hyper, dict):
        pytest.skip(f"{summary}: 双 WiFi 配置缺少传统或 Hyper 链路")
    traditional_ssid = str(traditional.get("ssid") or "")
    hyper_ssid = str(hyper.get("ssid") or "")
    original_attenuations: dict[int, float] | None = None

    def connect(block: dict, expected: set[str], stage: str) -> None:
        ssid = str(block.get("ssid") or "")
        if not ssid or not wifi.connect_wifi_block(cast(WiFiEntry, block)):
            pytest.fail(f"{summary}: 无法连接目标网络 {ssid!r}")
        _wait_for_status_bar_links(summary, settings_ui, expected, stage)

    try:
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        if summary.endswith("UI_002"):
            connect(hyper, {"hyper"}, "hyper_only")
        elif summary.endswith("UI_004"):
            ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=60.0)
            if not ok:
                pytest.fail(f"{summary}: 双链路连接失败 found={found!r} missing={missing!r}")
            _wait_for_status_primary(summary, run_shell_cmd, "wifi")
            _wait_for_status_bar_links(
                summary,
                settings_ui,
                {"wifi", "hyper"},
                "wifi_primary",
                expected_order=("wifi", "hyper"),
            )
        elif summary.endswith(("UI_005", "Int_005")):
            if attenuator is None:
                pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")
            ap_index = int(wifi_yaml.get("signal_level_lab", {}).get("ap_index", 1))
            channels = {
                "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
                "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
            }
            current_attenuations = attenuator.read_attenuations()
            if any(channel not in current_attenuations for channel in channels.values()):
                pytest.fail(
                    f"{summary}: 衰减器查询缺少目标通道，"
                    f"channels={channels!r}, state={current_attenuations!r}"
                )
            original_attenuations = {
                channel: current_attenuations[channel] for channel in channels.values()
            }
            for channel in channels.values():
                attenuator.set_attenuation(channel, 0)
            ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
            if not ok:
                pytest.fail(f"{summary}: 双链路连接失败 found={found!r} missing={missing!r}")

            initial_targets = (
                {"wifi": -80, "hyper": -50}
                if summary.endswith("UI_005")
                else {"wifi": -60, "hyper": -60}
            )
            tune_dual_link_rssi(
                run_shell_cmd,
                attenuator,
                channels,
                entry,
                initial_targets,
                settle_sec=4.0,
            )
            wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
            wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
            if summary.endswith("UI_005"):
                connect(hyper, {"hyper"}, "hyper_only")
                connect(traditional, {"wifi", "hyper"}, "dual_hyper_primary")
                _wait_for_status_primary(summary, run_shell_cmd, "hyper")
                _wait_for_status_bar_links(
                    summary,
                    settings_ui,
                    {"wifi", "hyper"},
                    "hyper_primary",
                    expected_order=("hyper", "wifi"),
                )
            else:
                connect(traditional, {"wifi"}, "wifi_only")
                connect(hyper, {"wifi", "hyper"}, "dual_wifi_primary")
                _wait_for_status_primary(summary, run_shell_cmd, "wifi")
                _wait_for_status_bar_links(
                    summary,
                    settings_ui,
                    {"wifi", "hyper"},
                    "wifi_primary",
                    expected_order=("wifi", "hyper"),
                )
                tune_dual_link_rssi(
                    run_shell_cmd,
                    attenuator,
                    channels,
                    entry,
                    {"wifi": -80, "hyper": -70},
                    settle_sec=4.0,
                )
                _wait_for_status_primary(summary, run_shell_cmd, "hyper")
                expected_ssids = [traditional_ssid, hyper_ssid]
                found, missing = wifi.match_associated_ssids(
                    expected_ssids, use_dumpsys_for_missing=True
                )
                if missing:
                    pytest.fail(
                        f"{summary}: primary 切换后未保持双链路，"
                        f"found={found!r} missing={missing!r}"
                    )
                _wait_for_status_bar_links(
                    summary,
                    settings_ui,
                    {"wifi", "hyper"},
                    "hyper_primary_after_switch",
                    timeout=45.0,
                    expected_order=("hyper", "wifi"),
                )
        elif summary.endswith("Int_001"):
            connect(traditional, {"wifi"}, "wifi_only")
            connect(hyper, {"wifi", "hyper"}, "dual_after_hyper")
        elif summary.endswith("Int_002"):
            connect(hyper, {"hyper"}, "hyper_only")
            connect(traditional, {"wifi", "hyper"}, "dual_after_wifi")
        elif summary.endswith("Int_003"):
            ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=60.0)
            if not ok:
                pytest.fail(f"{summary}: 双链路连接失败 found={found!r} missing={missing!r}")
            _wait_for_status_bar_links(summary, settings_ui, {"wifi", "hyper"}, "dual")
            _forget_connected_ssid(wifi, traditional_ssid)
            _wait_for_status_bar_links(summary, settings_ui, {"hyper"}, "after_wifi_disconnect")
        elif summary.endswith("Int_004"):
            ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=60.0)
            if not ok:
                pytest.fail(f"{summary}: 双链路连接失败 found={found!r} missing={missing!r}")
            _wait_for_status_bar_links(summary, settings_ui, {"wifi", "hyper"}, "dual")
            _forget_connected_ssid(wifi, hyper_ssid)
            _wait_for_status_bar_links(summary, settings_ui, {"wifi"}, "after_hyper_disconnect")
        else:
            raise ValueError(f"未知 SystemUI StatBar 用例: {summary}")
    finally:
        if attenuator is not None and original_attenuations is not None:
            for channel, value in original_attenuations.items():
                attenuator.set_attenuation(channel, value)
        wifi.disconnect_all(settle_sec=1.0, max_rounds=2, post_wait_sec=1.0)
        wifi.clear_saved_networks(max_rounds=2, settle_sec=0.2)
        settings_ui.device.press("home")
