"""WiFi 连接 — Func_Components_Settings_WifiAutoOn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.wifi_auto_on import (
    run_wifi_auto_on_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_UI_001")
@pytest.mark.wifi_case(
    title="默认配置UI检查",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_WifiAutoOn_UI_001(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_UI_002")
@pytest.mark.wifi_case(
    title="开启“自动开启WLAN”UI检查",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_WifiAutoOn_UI_002(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Vali_001")
@pytest.mark.wifi_case(
    title="开启“自动开启WLAN”",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_WifiAutoOn_Vali_001(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Vali_002")
@pytest.mark.wifi_case(
    title="关闭“自动开启WLAN”",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_WifiAutoOn_Vali_002(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Vali_003")
@pytest.mark.wifi_case(
    title="WLAN扫描功能弹窗“取消”按钮",
    pre="无",
)
def test_Func_Components_Settings_WifiAutoOn_Vali_003(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Vali_004")
@pytest.mark.wifi_case(
    title="WLAN扫描功能弹窗“开启”按钮",
    pre="无",
)
def test_Func_Components_Settings_WifiAutoOn_Vali_004(run_shell_cmd, settings_ui, wifi_case):
    run_wifi_auto_on_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Int_001")
@pytest.mark.wifi_case(
    title="开关开启+网络已保存",
    pre="无",
)
def test_Func_Components_Settings_WifiAutoOn_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Int_002")
@pytest.mark.wifi_case(
    title="开关关闭+网络已保存",
    pre="无",
)
def test_Func_Components_Settings_WifiAutoOn_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiAutoOn_Int_003")
@pytest.mark.wifi_case(
    title="开关开启+网络已取消保存",
    pre="无",
)
def test_Func_Components_Settings_WifiAutoOn_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
