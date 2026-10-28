"""WiFi 连接 — Func_Components_Settings_ConnStat（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.connection_status import (
    run_conn_status_connected_case,
    run_conn_status_disconnect_case,
    run_conn_status_no_internet_case,
    run_conn_status_wrong_password_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_001")
@pytest.mark.wifi_case(
    title="“已连接-互联网正常”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_conn_status_connected_case(
        wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_002")
@pytest.mark.wifi_case(
    title="“已连接-互联网异常”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_conn_status_no_internet_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_003")
@pytest.mark.wifi_case(
    title="已连接-互联网正常与异常互切，网络状态显示更新检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_004")
@pytest.mark.wifi_case(
    title="“密码错误”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_conn_status_wrong_password_case(
        wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_005")
@pytest.mark.wifi_case(
    title="“获取ip失败”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_006")
@pytest.mark.wifi_case(
    title="“已连接（互联网正常）再断开”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_006(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_conn_status_disconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wan="up"
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_007")
@pytest.mark.wifi_case(
    title="“已连接（互联网异常）再断开”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_007(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_conn_status_disconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wan="down"
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_008")
@pytest.mark.wifi_case(
    title="“Portal认证接入”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_ConnStat_UI_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ConnStat_UI_009")
@pytest.mark.wifi_case(
    title="“未联网重定向跳转”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为小米路由器AX3000",
)
def test_Func_Components_Settings_ConnStat_UI_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
