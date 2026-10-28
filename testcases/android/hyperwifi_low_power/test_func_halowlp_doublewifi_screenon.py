"""WiFi 连接 — Func_HalowLP_DoubleWifi_ScreenOn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.hyperwifi_low_power import (
    run_hyperwifi_dual_screen_on_case,
)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOn_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏，先后连接WiFi、HyperWiFi的过程中，HyperWiFi仍为唤醒状态",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室",
)
def test_Func_HalowLP_DoubleWifi_ScreenOn_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_on_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="connect_wifi_first",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOn_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏，先后连接HyperiWiFi、WiFi的过程中，HyperWiFi仍为唤醒状态",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室",
)
def test_Func_HalowLP_DoubleWifi_ScreenOn_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_on_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="connect_hyper_first",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOn_Vali_003")
@pytest.mark.wifi_case(
    title="亮屏，已连接双WiFi，断开WiFi的过程中，HyperWiFi仍为唤醒状态",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接HyperWiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOn_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_on_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="disconnect_wifi",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOn_Vali_004")
@pytest.mark.wifi_case(
    title="亮屏，已连接双WiFi，断开HyperWiFi的过程中，HyperWiFi仍为唤醒状态",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接HyperWiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOn_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_on_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="disconnect_hyper",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScreenOn_Vali_005")
@pytest.mark.wifi_case(
    title="亮屏，连接双WiFi后-无业务或流量（无扫描）时，HyperWiFi仍为唤醒状态",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接HyperWiFi",
)
def test_Func_HalowLP_DoubleWifi_ScreenOn_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_on_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="observe",
    )
