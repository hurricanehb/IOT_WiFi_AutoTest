"""WiFi 连接 — Func_Components_Welcome_ConnCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome.connection_config import (
    run_welcome_cancel_config_case,
    run_welcome_clear_password_case,
    run_welcome_connect_button_case,
    run_welcome_empty_password_case,
    run_welcome_encrypted_config_case,
    run_welcome_hyperwifi_intro_case,
    run_welcome_ip_mode_switch_case,
    run_welcome_open_network_case,
    run_welcome_password_input_case,
    run_welcome_password_length_case,
    run_welcome_password_visibility_case,
    run_welcome_wrong_password_reopen_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_001")
@pytest.mark.wifi_case(
    title="点击HyperWiFi-logo跳转界面检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_Welcome_ConnCfg_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_hyperwifi_intro_case(settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_002")
@pytest.mark.wifi_case(
    title="open网络连接无“配置框”弹出检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_open_network_case(wifi, wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_003")
@pytest.mark.wifi_case(
    title="加密网络连接“配置框”弹出检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_encrypted_config_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.parametrize(
    ("ssid_password", "success_message"),
    (
        pytest.param(
            '~!@#$%^&*()_+-={}|[]\\:";\'<>?,./', "密码输入框特殊字符输入正常",
            id="Func_Components_Welcome_ConnCfg_UI_004",
            marks=[pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_004"), pytest.mark.wifi_case(title="密码输入框“特殊字符”正常输入", pre="1、设备恢复出厂 2、陪测试设备为AP")],
        ),
        pytest.param(
            "1008610086", "密码输入框数字输入正常",
            id="Func_Components_Welcome_ConnCfg_UI_005",
            marks=[pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_005"), pytest.mark.wifi_case(title="密码输入框“数字”正常输入", pre="1、设备恢复出厂 2、陪测试设备为AP")],
        ),
        pytest.param(
            "helloworld", "密码输入框英文字符输入正常",
            id="Func_Components_Welcome_ConnCfg_UI_006",
            marks=[pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_006"), pytest.mark.wifi_case(title="密码输入框“英文字符”正常输入", pre="1、设备恢复出厂 2、陪测试设备为AP")],
        ),
    ),
)
@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
def test_welcome_password_input(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case, ssid_password: str, success_message: str,
):
    run_welcome_password_input_case(
        wifi_yaml,
        settings_ui,
        tmp_path,
        capsys,
        ssid_password,
        success_message,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_007")
@pytest.mark.wifi_case(
    title="密码输入为空，“连接按键”置灰",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_empty_password_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_008")
@pytest.mark.wifi_case(
    title="最小密码长度8位验证",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys, wifi_case,
):
    run_welcome_password_length_case(wifi, wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_009")
@pytest.mark.wifi_case(
    title="允许最大密码长度32位输入-HyperWiFi",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_Welcome_ConnCfg_UI_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_010")
@pytest.mark.wifi_case(
    title="允许最大密码长度64位输入-WiFi",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_011")
@pytest.mark.wifi_case(
    title="密码输入中文字符",
    pre="无",
)
def test_Func_Components_Welcome_ConnCfg_UI_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_012")
@pytest.mark.wifi_case(
    title="密码输入框明文/密文切换按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_012(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_password_visibility_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_013")
@pytest.mark.wifi_case(
    title="密码输入框“删除”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_013(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_clear_password_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_014")
@pytest.mark.wifi_case(
    title="密码输入框“取消”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_014(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_cancel_config_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_015")
@pytest.mark.wifi_case(
    title="密码输入框“连接”按钮有效",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_015(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys, wifi_case,
):
    run_welcome_connect_button_case(wifi, wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_016")
@pytest.mark.wifi_case(
    title="高级选项-IP设置",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_016(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_ip_mode_switch_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ConnCfg_UI_017")
@pytest.mark.wifi_case(
    title="再次点击“密码错误”提示的无线-配置框自动弹出",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Welcome_ConnCfg_UI_017(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys, wifi_case,
):
    run_welcome_wrong_password_reopen_case(wifi_yaml, settings_ui, tmp_path, capsys)
