"""WiFi 连接 — Func_Components_Settings_WifiScanSw（自动化实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.wifi_scan_switch import (
    run_wifi_scan_always_case,
    run_wifi_scan_default_case,
    run_wifi_scan_toggle_case,
)


@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiScanSw_UI_001")
@pytest.mark.wifi_case(
    title="WLAN扫描设置默认配置检查",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WifiScanSw_UI_001(
    run_shell_cmd, settings_ui, wifi_case
):
    run_wifi_scan_default_case(wifi_case["case_id"], run_shell_cmd, settings_ui)


@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiScanSw_Vali_001")
@pytest.mark.wifi_case(
    title="WLAN扫描设置设置开启",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WifiScanSw_Vali_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_case
):
    run_wifi_scan_always_case(
        wifi_case["case_id"], run_shell_cmd, wifi, enabled=True
    )


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiScanSw_Vali_002")
@pytest.mark.wifi_case(
    title="WLAN扫描设置设置关闭",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WifiScanSw_Vali_002(
    run_shell_cmd, wifi, wifi_yaml, wifi_case
):
    run_wifi_scan_always_case(
        wifi_case["case_id"], run_shell_cmd, wifi, enabled=False
    )


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiScanSw_Vali_003")
@pytest.mark.wifi_case(
    title="WLAN开关开启/禁用，扫描设置开启",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WifiScanSw_Vali_003(
    run_shell_cmd, wifi, settings_ui, wifi_case
):
    run_wifi_scan_toggle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, settings_ui
    )
