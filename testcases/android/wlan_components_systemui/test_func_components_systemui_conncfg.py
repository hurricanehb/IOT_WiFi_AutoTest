"""WiFi 连接 — Func_Components_SystemUI_ConnCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_connection_config_case

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_001")
@pytest.mark.wifi_case(
    title="点击HyperWiFi-logo跳转界面检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="hyperwifi_intro", hyper=True)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_002")
@pytest.mark.wifi_case(
    title="open网络连接无“配置框”弹出检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="open_no_dialog")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_003")
@pytest.mark.wifi_case(
    title="加密网络连接“配置框”弹出检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="dialog")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_004")
@pytest.mark.wifi_case(
    title="加密网络连接“配置框”信息检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="dialog_info")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_005")
@pytest.mark.wifi_case(
    title="密码输入为空，“连接按键”置灰",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="empty_password")

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_006")
@pytest.mark.wifi_case(
    title="密码长度<8位报错",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_006(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="min_password", hyper=True)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_007")
@pytest.mark.wifi_case(
    title="密码长度>32位报错-HyperWiFi",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_007(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="max_password", hyper=True)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_008")
@pytest.mark.wifi_case(
    title="密码长度>64位输入-WiFi",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_008(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="max_password")

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_009")
@pytest.mark.wifi_case(
    title="密码输入中文字符",
    pre="无",
)
def test_Func_Components_SystemUI_ConnCfg_UI_009(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="chinese_password")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_010")
@pytest.mark.wifi_case(
    title="密码输入框明文/密文切换按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_010(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="visibility")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_011")
@pytest.mark.wifi_case(
    title="密码输入框“删除”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_011(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="clear")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_012")
@pytest.mark.wifi_case(
    title="密码输入框“取消”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_012(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="cancel")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_013")
@pytest.mark.wifi_case(
    title="密码输入框“连接”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_013(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="connect")

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_014")
@pytest.mark.wifi_case(
    title="高级选项-IP设置",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_014(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="advanced")

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnCfg_UI_015")
@pytest.mark.wifi_case(
    title="再次点击“密码错误”提示的无线-配置框自动弹出",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnCfg_UI_015(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_connection_config_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, operation="wrong_password_reopen")
