"""WiFi 连接 — Func_Components_Settings_NetDetails（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.network_details import (
    run_network_details_advanced_case,
    run_network_details_disconnect_reconnect_case,
    run_network_details_edit_password_case,
    run_network_details_forget_case,
    run_network_details_status_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_001")
@pytest.mark.wifi_case(
    title="网络详情-连接状态检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_network_details_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_002")
@pytest.mark.wifi_case(
    title="网络详情-高级网络详情",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_network_details_advanced_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_003")
@pytest.mark.wifi_case(
    title="网络详情-修改密码“铅笔图标”检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_network_details_edit_password_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_004")
@pytest.mark.wifi_case(
    title="网络详情-“取消保存”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_network_details_forget_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_005")
@pytest.mark.wifi_case(
    title="网络详情-“断开连接”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_network_details_disconnect_reconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_006")
@pytest.mark.wifi_case(
    title="网络详情-“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_007")
@pytest.mark.wifi_case(
    title="网络详情-“登录”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_008")
@pytest.mark.wifi_case(
    title="网络详情-“自动连接”开关",
    pre="1、DUT已成功连接AP 2、屏蔽房或干扰少的环境",
)
def test_Func_Components_Settings_NetDetails_UI_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
