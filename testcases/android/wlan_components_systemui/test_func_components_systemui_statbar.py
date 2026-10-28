"""WiFi 连接 — Func_Components_SystemUI_StatBar（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_status_bar_case
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_001")
@pytest.mark.wifi_case(
    title="连接传统WiFi无线图标左下角显示检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_002")
@pytest.mark.wifi_case(
    title="连接HyperWiFi无线图标左下角显示检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_003")
@pytest.mark.wifi_case(
    title="单WiFi连接-无线图标右下角流量标志",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_004")
@pytest.mark.wifi_case(
    title="双WiFi连接-WiFi为主网络-WiFi图标在前，HyperWiFi图标在后",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_005")
@pytest.mark.wifi_case(
    title="双WiFi连接-HyperWiFi为主网络-HyperWiFi图标在前，WiFi图标在后",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-80dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_systemui_status_bar_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional
    )

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_UI_006")
@pytest.mark.wifi_case(
    title="双WiFi连接-主网络无线图标右下角流量标志",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_StatBar_UI_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_Int_001")
@pytest.mark.wifi_case(
    title="settings依次接入WiFi、HyperWiFi，systemUI-状态栏无线图标检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_StatBar_Int_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_Int_002")
@pytest.mark.wifi_case(
    title="settings依次接入HyperWiFi、WiFi，systemUI-状态栏无线图标检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_StatBar_Int_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_Int_003")
@pytest.mark.wifi_case(
    title="双WiFi-settings断开WiFi网络，systemUI-状态栏检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_StatBar_Int_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_Int_004")
@pytest.mark.wifi_case(
    title="双WiFi-settings断开HyperWiFi网络，systemUI-状态栏检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_StatBar_Int_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_status_bar_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_StatBar_Int_005")
@pytest.mark.wifi_case(
    title="主备网络切换-system-状态栏检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_StatBar_Int_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_systemui_status_bar_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional
    )
