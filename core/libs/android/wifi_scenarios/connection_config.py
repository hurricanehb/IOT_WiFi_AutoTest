"""Shared WiFi connection-dialog scenarios."""
from __future__ import annotations

import time
from typing import Callable, cast

import allure
import pytest

from core.libs.android.settings_pages.connection_config_page import WiFiConnectionConfigUI
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.testdata_loader import get_dual_wifi_entry


def connection_config_entry(
    wifi_yaml: dict, *, encrypted: bool, hyper: bool = False
) -> WiFiEntry:
    for entry in wifi_yaml.get("wifi_list") or []:
        is_encrypted = (entry.get("encrypt") or "").upper() != "OPEN"
        is_hyper = (entry.get("type") or "").lower() == "hyperwifi"
        if is_encrypted == encrypted and is_hyper == hyper and entry.get("expect") == "connected":
            return cast(WiFiEntry, entry)
    kind = "HyperWiFi 加密" if hyper else ("加密" if encrypted else "开放")
    pytest.skip(f"ConnCfg: wifi_ssid.yaml 无可用{kind}网络配置")
    raise AssertionError("pytest.skip should not return")


@allure.step("执行 WLAN 连接配置验证")
def run_connection_config_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    *,
    operation: str,
    hyper: bool = False,
    open_networks: Callable[[], None] | None = None,
) -> None:
    """ConnCfg：扫描列表连接配置框的可观测行为。"""
    attach_wifi_status(summary, run_shell_cmd)
    config_ui = WiFiConnectionConfigUI(settings_ui)
    if operation == "hyperwifi_intro":
        dual_entry = get_dual_wifi_entry(
            wifi_yaml,
            entry_id="dual_wifi_24g_hyperwifi_us",
        )
        hyper_entry = dual_entry.get("hyper_wifi") or {}
        ssid = str(hyper_entry.get("ssid") or "")
        if not ssid:
            pytest.skip(f"{summary}: 双 WiFi 配置缺少 miniAP HyperWiFi SSID")
        config_ui.open_hyperwifi_intro(ssid, open_networks)
        config_ui.close_hyperwifi_intro()
        return

    encrypted = operation != "open_no_dialog"
    entry = connection_config_entry(wifi_yaml, encrypted=encrypted, hyper=hyper)
    ssid = str(entry.get("ssid") or "")
    if not ssid:
        pytest.skip(f"{summary}: wifi_ssid.yaml 连接配置缺少 SSID")
    password = str(entry.get("pwd") or "")
    wifi.clear_saved_networks()
    config_ui.open_for_ssid(ssid, open_networks)

    if operation == "open_no_dialog":
        if config_ui.dialog_exists():
            config_ui.cancel()
            pytest.fail(f"{summary}: 开放网络不应弹出连接配置框")
        if not wifi.match_associated_ssids([ssid])[0]:
            pytest.fail(f"{summary}: 点击开放网络后未自动连接 {ssid!r}")
        return

    config_ui.require_dialog(ssid)
    try:
        if operation == "dialog":
            return
        if operation == "dialog_info":
            if config_ui.title() != ssid or not config_ui.password_field().exists:
                pytest.fail(f"{summary}: 配置框未正确显示 SSID 或密码输入框")
        elif operation == "empty_password":
            config_ui.set_password("")
            if config_ui.save_enabled():
                pytest.fail(f"{summary}: 空密码时连接按钮应不可用")
        elif operation == "min_password":
            config_ui.set_password(password[:7])
            if config_ui.save_enabled():
                pytest.fail(f"{summary}: 少于 8 位密码时连接按钮应不可用")
            config_ui.set_password(password)
            config_ui.save()
            assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        elif operation == "max_password":
            actual = config_ui.set_password("x" * (33 if hyper else 65))
            limit = 32 if hyper else 64
            if len(actual) > limit:
                pytest.fail(f"{summary}: 密码长度应限制为 {limit}，实际={len(actual)}")
        elif operation == "chinese_password":
            actual = config_ui.set_password("中文字符")
            if actual and config_ui.save_enabled():
                pytest.fail(f"{summary}: 中文密码字符不应允许保存")
        elif operation == "visibility":
            config_ui.set_password(password)
            first = config_ui.toggle_password_visibility()
            second = config_ui.toggle_password_visibility()
            if first == second:
                pytest.fail(f"{summary}: 密码明文/密文切换状态未恢复")
        elif operation == "clear":
            config_ui.set_password(password)
            if config_ui.set_password(""):
                pytest.fail(f"{summary}: 清空密码后输入框仍有内容")
        elif operation == "cancel":
            config_ui.cancel()
            if config_ui.dialog_exists():
                pytest.fail(f"{summary}: 取消后连接配置框仍显示")
            return
        elif operation == "connect":
            config_ui.set_password(password)
            config_ui.save()
            assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
            return
        elif operation == "advanced":
            config_ui.open_advanced_options()
            if config_ui.ip_mode().upper() != "DHCP":
                pytest.fail(f"{summary}: IP 设置默认值应为 DHCP")
            config_ui.select_ip_mode("Static")
            if config_ui.ip_mode().lower() not in ("static", "静态"):
                pytest.fail(f"{summary}: IP 设置未切换为静态")
            config_ui.select_ip_mode("DHCP")
            if config_ui.ip_mode().upper() != "DHCP":
                pytest.fail(f"{summary}: IP 设置未切换回 DHCP")
        elif operation == "wrong_password_reopen":
            config_ui.set_password("wrong_pwd_00000")
            config_ui.save()
            time.sleep(10.0)
            config_ui.open_for_ssid(ssid, open_networks)
            config_ui.require_dialog(ssid)
        else:
            raise ValueError(f"未知 ConnCfg 操作: {operation!r}")
    finally:
        if config_ui.dialog_exists():
            config_ui.cancel()