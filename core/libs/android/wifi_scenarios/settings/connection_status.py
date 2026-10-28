"""SettingsUI scenarios for WiFi connection status presentation."""
from __future__ import annotations

import time
from collections.abc import Callable

import allure
import pytest

from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.network_204 import require_wan_state
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.settings._helpers import (
    assert_status_text_absent,
    assert_status_text_present,
    resolve_entry,
    wlan_list_blob,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI

CONNECTED_TEXTS = ("已连接", "Connected")
NO_INTERNET_TEXTS = (
    "无法提供互联网连接",
    "无法访问互联网",
    "无法连接到互联网",
    "No internet access",
    "no internet",
)
WRONG_PASSWORD_TEXTS = (
    "请检查密码",
    "密码不正确",
    "身份验证出现问题",
    "Check password",
    "Authentication problem",
)
SAVED_TEXTS = ("已保存", "Saved")

_VALIDATION_SETTLE_SEC = 10.0


@allure.step("执行已连接状态验证")
def run_conn_status_connected_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    *,
    index: int | None = None,
    ssid: str | None = None,
    wan: str = "up",
) -> None:
    """ConnStat_UI_001：互联网正常时 WLAN 列表显示“已连接”。"""
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    entry = resolve_entry(
        wifi_yaml, index=index, ssid=ssid, summary=summary, run_shell_cmd=run_shell_cmd
    )

    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    time.sleep(_VALIDATION_SETTLE_SEC)

    blob = wlan_list_blob(settings_ui)
    assert_status_text_present(
        blob, CONNECTED_TEXTS, summary=summary, label="“已连接”"
    )
    assert_status_text_absent(
        blob, NO_INTERNET_TEXTS, summary=summary, label="无互联网提示"
    )


@allure.step("执行无互联网状态验证")
def run_conn_status_no_internet_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state("down", summary)
    entry = resolve_entry(
        wifi_yaml,
        index=None,
        ssid=None,
        summary=summary,
        run_shell_cmd=run_shell_cmd,
    )
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    time.sleep(_VALIDATION_SETTLE_SEC)

    blob = wlan_list_blob(settings_ui)
    assert_status_text_present(
        blob, NO_INTERNET_TEXTS, summary=summary, label="无互联网提示"
    )


@allure.step("执行断开后的保存状态验证")
def run_conn_status_disconnect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    *,
    wan: str,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    entry = resolve_entry(
        wifi_yaml,
        index=None,
        ssid=None,
        summary=summary,
        run_shell_cmd=run_shell_cmd,
    )
    target = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    time.sleep(_VALIDATION_SETTLE_SEC)

    if wan == "down":
        blob = wlan_list_blob(settings_ui)
        assert_status_text_present(
            blob, NO_INTERNET_TEXTS, summary=summary, label="无互联网提示"
        )

    if not wifi.disconnect_all(post_wait_sec=2.0):
        pytest.fail(f"{summary}: 无法断开当前 WLAN")
    if not wifi.wait_until_disconnected(timeout=10.0):
        pytest.fail(f"{summary}: 断开操作后 WLAN 仍保持连接")
    if not any(target.casefold() == saved.casefold() for saved in wifi.list_saved_networks()):
        pytest.fail(f"{summary}: 断开后网络未保留在保存列表: {target!r}")

    blob = wlan_list_blob(settings_ui)
    assert_status_text_present(blob, SAVED_TEXTS, summary=summary, label="已保存")


@allure.step("执行密码错误状态验证")
def run_conn_status_wrong_password_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    *,
    index: int | None = None,
    ssid: str | None = None,
    wrong_password: str = "wrong_pwd_00000",
    settle_sec: float = 20.0,
) -> None:
    """ConnStat_UI_004：错误密码连接后显示“已保存/请检查密码是否正确”。"""
    attach_wifi_status(summary, run_shell_cmd)
    entry = resolve_entry(
        wifi_yaml, index=index, ssid=ssid, summary=summary, run_shell_cmd=run_shell_cmd
    )
    target = str(entry.get("ssid") or "")

    if not wifi.set_wifi_enabled(True):
        pytest.fail(f"{summary}: 无法打开 WiFi 射频")
    wifi.clear_saved_networks()

    try:
        wifi.connect_wpa2(target, wrong_password)
        time.sleep(settle_sec)

        status = run_shell_cmd("cmd wifi status")
        print(f"[{summary}] 错误密码连接后 cmd wifi status:\n{status}")
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if any(name.lower() == target.lower() for name in connected):
            pytest.fail(f"{summary}: 使用错误密码却关联成功，当前={connected!r}")

        blob = wlan_list_blob(settings_ui)
        assert_status_text_present(
            blob,
            WRONG_PASSWORD_TEXTS + SAVED_TEXTS,
            summary=summary,
            label="“已保存/请检查密码是否正确”",
        )
    finally:
        wifi.clear_saved_networks()
