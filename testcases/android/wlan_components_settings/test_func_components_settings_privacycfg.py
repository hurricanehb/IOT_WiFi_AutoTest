"""WiFi 连接 — Func_Components_Settings_PrivacyCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_UI_001")
@pytest.mark.wifi_case(
    title="MAC默认显示检查",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_UI_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_UI_002")
@pytest.mark.wifi_case(
    title="MAC可选项检查",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_001")
@pytest.mark.wifi_case(
    title="无线连接时使用设备MAC",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_002")
@pytest.mark.wifi_case(
    title="已连接网络-随机MAC切换设备MAC",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_003")
@pytest.mark.wifi_case(
    title="切换AP连接，设备MAC规则失效",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_004")
@pytest.mark.wifi_case(
    title="wifi断开重连，设备MAC一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_005")
@pytest.mark.wifi_case(
    title="STA重启重连，设备MAC一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_006")
@pytest.mark.wifi_case(
    title="取消保存后重新连接，设备MAC规则失效",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_007")
@pytest.mark.wifi_case(
    title="无线连接时使用随机MAC",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_008")
@pytest.mark.wifi_case(
    title="已连接网络-设备MAC切换随机MAC",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_009")
@pytest.mark.wifi_case(
    title="wifi断开重连，随机MAC一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_010")
@pytest.mark.wifi_case(
    title="STA重启重连，随机MAC一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_011")
@pytest.mark.wifi_case(
    title="取消保存后重新连接，原随机mac一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_012")
@pytest.mark.wifi_case(
    title="切换AP连接，原随机mac一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_PrivacyCfg_Vali_013")
@pytest.mark.wifi_case(
    title="切换回原AP，原随机mac规则一致性",
    pre="DUT为出厂状态",
)
def test_Func_Components_Settings_PrivacyCfg_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
