"""WiFi 连接 — Func_PriBakLink_Scenario_Roam（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_001")
@pytest.mark.wifi_case(
    title="2.4G WIFI漫游与主备切换同时触发",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_002")
@pytest.mark.wifi_case(
    title="5G WIFI漫游与主备切换同时触发",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_003")
@pytest.mark.wifi_case(
    title="HyperWiFi漫游与主备切换同时触发",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_004")
@pytest.mark.wifi_case(
    title="WiFi切换为HyperWiFi网络后再触发漫游",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_005")
@pytest.mark.wifi_case(
    title="无WIFI漫游，2.4G WIFI网络与HyperWiFi（多miniAP）网络选择后主备切换",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_006")
@pytest.mark.wifi_case(
    title="无WIFI漫游，5G WIFI网络与HyperWiFi（多miniAP）网络互切",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Scenario_Roam_Int_007")
@pytest.mark.wifi_case(
    title="无WIFI漫游，HyperWiFi网络切换HyperWiFi（多miniAP）网络",
    pre="无",
)
def test_Func_PriBakLink_Scenario_Roam_Int_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
