"""WiFi 连接 — Func_HalowLP_DoubleWifi_ScreenOff（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_001")
@pytest.mark.wifi_case(
    title="息屏，未连接HyperWiFi（无保存网络），WiFi进行PNO扫描，HyperWiFi低功耗模式不变",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_002")
@pytest.mark.wifi_case(
    title="息屏，未连接HyperWiFi（已保存网络）且未进行PNO扫描，WiFi进行PNO扫描，HyperWiFi退出低功耗模式",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_003")
@pytest.mark.wifi_case(
    title="息屏，已连接HyperWiFi（PowerSave模式），断开WiFi网络，HyperWiFi低功耗模式不变",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_004")
@pytest.mark.wifi_case(
    title="息屏，已连接HyperWiFi（PowerSave模式），WiFi发起PNO扫描连接，HyperWiFi低功耗模式不变",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_005")
@pytest.mark.wifi_case(
    title="息屏，WiFi保持连接，接入HyperWiFi且有流量（业务时），HyperWiFi退出功耗模式",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_006")
@pytest.mark.wifi_case(
    title="息屏，WiFi保持连接，断开HyperWiFi后发起pno扫描，退出低功耗（唤醒状态）",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_007")
@pytest.mark.wifi_case(
    title="息屏，WiFi保持连接，断开HyperWiFi后pno扫描不到目标网络，进入低功耗（idle状态）",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOff_Vali_008")
@pytest.mark.wifi_case(
    title="息屏，已连接双WiFi，HyperWiFi（PowerSave模式），WiFi进行DHCP续约，HyperWiFi低功耗模式不变",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOff_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
