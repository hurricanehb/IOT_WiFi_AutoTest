"""WiFi 连接 — Func_Components_Settings_SavedNet（自动化/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.saved_networks import (
    run_saved_hidden_network_case,
    run_saved_network_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_001")
@pytest.mark.wifi_case(
    title="未连接过网络",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_SavedNet_Vali_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_saved_network_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_002")
@pytest.mark.wifi_case(
    title="保存已连接-可联网的网络",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置不加密网络；",
)
def test_Func_Components_Settings_SavedNet_Vali_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_saved_network_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_003")
@pytest.mark.wifi_case(
    title="保存已连接-不可联网的网络",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置不加密网络；",
)
def test_Func_Components_Settings_SavedNet_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_004")
@pytest.mark.wifi_case(
    title="保存已连接-需认证的网络",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置不加密网络；",
)
def test_Func_Components_Settings_SavedNet_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_005")
@pytest.mark.wifi_case(
    title="保存未连接-密码错误的网络",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置加密网络；",
)
def test_Func_Components_Settings_SavedNet_Vali_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_saved_network_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_006")
@pytest.mark.wifi_case(
    title="保存添加的隐藏网络",
    pre="无",
)
def test_Func_Components_Settings_SavedNet_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional, wifi_case):
    run_saved_hidden_network_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_add_network_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_007")
@pytest.mark.wifi_case(
    title="“保存网络配置”路径下取消保存",
    pre="无",
)
def test_Func_Components_Settings_SavedNet_Vali_007(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_saved_network_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_SavedNet_Vali_008")
@pytest.mark.wifi_case(
    title="“在线列表网络详情”路径下取消保存",
    pre="无",
)
def test_Func_Components_Settings_SavedNet_Vali_008(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_saved_network_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui)
