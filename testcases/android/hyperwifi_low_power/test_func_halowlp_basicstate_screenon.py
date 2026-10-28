"""WiFi 连接 — Func_HalowLP_BasicState_ScreenOn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.hyperwifi_low_power import (
    run_hyperwifi_airplane_cycle_case,
    run_hyperwifi_airplane_cycle_stability_case,
    run_hyperwifi_disconnect_screen_on_active_case,
    run_hyperwifi_screen_on_active_case,
    run_hyperwifi_unconnected_screen_on_active_case,
    run_hyperwifi_unconnected_wlan_off_idle_case,
    run_hyperwifi_wlan_cycle_stability_case,
    run_hyperwifi_wlan_off_idle_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏，出厂启用WLAN但不连接，不进入低功耗模式（IDLE）",
    pre="1、默认设备已恢复出厂设置；确认设备处于出厂后的亮屏状态",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_unconnected_screen_on_active_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏，WLAN已连接但无业务，不进入低功耗模式（PowerSave）",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_on_active_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_003")
@pytest.mark.wifi_case(
    title="亮屏，WLAN断开且不扫描，不进入低功耗模式（IDLE）",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_disconnect_screen_on_active_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_004")
@pytest.mark.wifi_case(
    title="亮屏，出厂关闭WLAN，为低功耗模式（IDLE）",
    pre="1、默认设备已恢复出厂设置；备注：MTK系列（SP01、SP10等）WLAN默认关闭，高通系列（V3MIX等）WLAN默认开启",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_005")
@pytest.mark.wifi_case(
    title="亮屏，无连接状态下关闭WLAN，进入低功耗模式（IDLE）",
    pre="1、未连接HyperWiFi网络",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_unconnected_wlan_off_idle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_006")
@pytest.mark.wifi_case(
    title="亮屏，已连接状态下关闭WLAN，进入低功耗模式（IDLE）",
    pre="1、已连接HyperWiFi网络",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_wlan_off_idle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Vali_007")
@pytest.mark.wifi_case(
    title="亮屏，开启飞行模式，进入低功耗模式（IDLE）",
    pre="1、已连接HyperWiFi网络",
)
def test_Func_HalowLP_BasicState_ScreenOn_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_airplane_cycle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Stb_001")
@pytest.mark.wifi_case(
    title="亮屏状态下低功耗模式切换--禁用启用Wlan开关",
    pre="1、环境拓扑：上级网关--AP/miniAP 2、测试环境：办公位或者实验室 3、已连接WiFi",
)
def test_Func_HalowLP_BasicState_ScreenOn_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_wlan_cycle_stability_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOn_Stb_002")
@pytest.mark.wifi_case(
    title="亮屏状态下低功耗模式切换--禁用启用飞行模式",
    pre="无",
)
def test_Func_HalowLP_BasicState_ScreenOn_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_airplane_cycle_stability_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )
