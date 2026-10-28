"""WiFi 连接 — Func_Components_Settings_ScanListOps（自动化/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.scan_list_ops import (
    run_settings_scan_list_ops_case,
)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_001")
@pytest.mark.wifi_case(
    title="已连接网络快捷菜单",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_002")
@pytest.mark.wifi_case(
    title="未连接网络快捷菜单",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_003")
@pytest.mark.wifi_case(
    title="已保存未连接网络快捷菜单",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_004")
@pytest.mark.wifi_case(
    title="已连接网络-分享按钮",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_005")
@pytest.mark.wifi_case(
    title="已连接网络-取消保存按钮",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_006")
@pytest.mark.wifi_case(
    title="已连接网络-断开连接按钮",
    pre="1、无线已连接",
)
def test_Func_Components_Settings_ScanListOps_UI_006(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_007")
@pytest.mark.wifi_case(
    title="已保存未连接-连接按钮",
    pre="1、DUT已保存网络但未连接",
)
def test_Func_Components_Settings_ScanListOps_UI_007(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_008")
@pytest.mark.wifi_case(
    title="已保存未连接-修改按钮",
    pre="1、DUT已保存网络但未连接",
)
def test_Func_Components_Settings_ScanListOps_UI_008(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_009")
@pytest.mark.wifi_case(
    title="已保存未连接-取消保存按钮",
    pre="1、DUT已保存网络但未连接",
)
def test_Func_Components_Settings_ScanListOps_UI_009(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanListOps_UI_010")
@pytest.mark.wifi_case(
    title="未保存未连接网络-连接按钮",
    pre="1、DUT 未保存未连接无线网络",
)
def test_Func_Components_Settings_ScanListOps_UI_010(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_ops_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)
