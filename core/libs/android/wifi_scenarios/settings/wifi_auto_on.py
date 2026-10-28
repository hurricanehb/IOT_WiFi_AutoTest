"""Settings automation for the WiFi auto-on preference."""
from __future__ import annotations

import time
from collections.abc import Callable

import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.settings._global_settings import (
    global_setting,
    restore_global_setting,
    set_global_setting,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI

AUTO_ON_TITLE = "自动开启 WLAN"
AUTO_ON_SUMMARY = "自动重新开启 WLAN"
AUTO_OFF_SUMMARY = "不自动重新开启 WLAN"
PREFERENCES_TITLE = "网络偏好设置"
SCAN_DIALOG_TITLE = "要开启 WLAN 扫描功能吗？"
WIFI_SCAN_KEY = "wifi_scan_always_enabled"
WIFI_WAKEUP_KEY = "wifi_wakeup_enabled"


def _wait_global_setting(
    run_shell_cmd: Callable[[str], str],
    key: str,
    expected: str,
    *,
    timeout: float = 5.0,
) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if global_setting(run_shell_cmd, key) == expected:
            return True
        time.sleep(0.2)
    return False


def _open_wifi_preferences(settings_ui: AndroidSettingsUI) -> None:
    settings_ui.open_wifi_settings()
    settings_ui.scroll_to_text(PREFERENCES_TITLE)
    settings_ui.click_text(PREFERENCES_TITLE)
    settings_ui.require_text(AUTO_ON_TITLE)


def _auto_on_switch_checked(settings_ui: AndroidSettingsUI) -> bool:
    switch = settings_ui.device(
        resourceId="com.android.settings:id/switchWidget",
        instance=0,
    )
    if not switch.wait(timeout=5.0):
        settings_ui.fail_with_artifacts("WLAN 偏好设置页未找到自动开启开关")
    return bool(switch.info.get("checked"))


def _require_scan_dialog(settings_ui: AndroidSettingsUI) -> None:
    settings_ui.require_text(SCAN_DIALOG_TITLE)
    settings_ui.require_text("取消")
    settings_ui.require_text("开启")


def _assert_setting(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    key: str,
    expected: str,
) -> None:
    actual = global_setting(run_shell_cmd, key)
    if actual != expected:
        pytest.fail(f"{summary}: {key} 期望={expected!r}，实际={actual!r}")


def run_wifi_auto_on_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    settings_ui: AndroidSettingsUI,
) -> None:
    """Run WiFi auto-on UI and validation cases against the real Settings UI."""
    attach_wifi_status(summary, run_shell_cmd)
    original_wakeup = global_setting(run_shell_cmd, WIFI_WAKEUP_KEY)
    original_scan = global_setting(run_shell_cmd, WIFI_SCAN_KEY)
    try:
        if summary.endswith("UI_001"):
            if original_wakeup != "0":
                pytest.skip(
                    f"{summary}: 前置要求出厂默认状态，"
                    f"当前 {WIFI_WAKEUP_KEY}={original_wakeup!r}"
                )
            _open_wifi_preferences(settings_ui)
            if _auto_on_switch_checked(settings_ui):
                pytest.fail(f"{summary}: 自动开启 WLAN 默认应关闭")
            settings_ui.press_back()
            settings_ui.require_text(AUTO_OFF_SUMMARY)
            return

        if not summary.endswith(
            ("UI_002", "Vali_001", "Vali_002", "Vali_003", "Vali_004")
        ):
            raise ValueError(f"未知 WifiAutoOn 自动化用例: {summary}")

        if summary.endswith("Vali_002"):
            set_global_setting(run_shell_cmd, WIFI_WAKEUP_KEY, "1")
            set_global_setting(run_shell_cmd, WIFI_SCAN_KEY, "1")
            settings_ui.device.shell("am force-stop com.android.settings")
            _open_wifi_preferences(settings_ui)
            if not _auto_on_switch_checked(settings_ui):
                pytest.fail(f"{summary}: 自动开启 WLAN 前置未开启")
            settings_ui.click_text(AUTO_ON_TITLE)
            if not _wait_global_setting(run_shell_cmd, WIFI_WAKEUP_KEY, "0"):
                pytest.fail(f"{summary}: 点击关闭后自动开启 WLAN 未关闭")
            if _auto_on_switch_checked(settings_ui):
                pytest.fail(f"{summary}: 关闭后 UI 开关仍为开启")
            return

        set_global_setting(run_shell_cmd, WIFI_WAKEUP_KEY, "0")
        set_global_setting(run_shell_cmd, WIFI_SCAN_KEY, "0")
        settings_ui.device.shell("am force-stop com.android.settings")
        _open_wifi_preferences(settings_ui)
        if _auto_on_switch_checked(settings_ui):
            pytest.fail(f"{summary}: 自动开启 WLAN 前置未关闭")

        settings_ui.click_text(AUTO_ON_TITLE)
        _require_scan_dialog(settings_ui)

        if summary.endswith("Vali_003"):
            settings_ui.click_text("取消")
            settings_ui.require_text(AUTO_ON_TITLE)
            _assert_setting(summary, run_shell_cmd, WIFI_WAKEUP_KEY, "0")
            _assert_setting(summary, run_shell_cmd, WIFI_SCAN_KEY, "0")
            if _auto_on_switch_checked(settings_ui):
                pytest.fail(f"{summary}: 取消后自动开启 WLAN 不应生效")
            return

        settings_ui.click_text("开启")
        if not _wait_global_setting(run_shell_cmd, WIFI_WAKEUP_KEY, "1"):
            pytest.fail(f"{summary}: 点击开启后自动开启 WLAN 未生效")
        _assert_setting(summary, run_shell_cmd, WIFI_SCAN_KEY, "1")
        settings_ui.open_wifi_settings()
        settings_ui.scroll_to_text(PREFERENCES_TITLE)
        settings_ui.require_text(AUTO_ON_SUMMARY)
        _open_wifi_preferences(settings_ui)
        if not _auto_on_switch_checked(settings_ui):
            pytest.fail(f"{summary}: 重新进入偏好设置后 UI 开关仍为关闭")
        if summary.endswith(("UI_002", "Vali_001")):
            settings_ui.press_back()
            settings_ui.require_text(AUTO_ON_SUMMARY)
    finally:
        restore_global_setting(
            run_shell_cmd,
            WIFI_WAKEUP_KEY,
            original_wakeup,
        )
        restore_global_setting(
            run_shell_cmd,
            WIFI_SCAN_KEY,
            original_scan,
        )