"""WiFi 连接 — Func_HalowLP_BasicState_ScreenOff（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.hyperwifi_low_power import (
    run_hyperwifi_no_saved_screen_off_idle_case,
    run_hyperwifi_screen_off_powersave_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOff_Vali_001")
@pytest.mark.wifi_case(
    title="息屏，出厂未连接状态下，进入IDLE模式验证",
    pre="1、默认设备已恢复出厂设置；未连接过HyperWiFi",
)
def test_Func_HalowLP_BasicState_ScreenOff_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_no_saved_screen_off_idle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOff_Vali_002")
@pytest.mark.wifi_case(
    title="息屏，PNO扫描不到目标网络，进入IDLE模式",
    pre="1、默认设备已恢复出厂设置；已连接HyperWiFi后目标网络下线",
)
def test_Func_HalowLP_BasicState_ScreenOff_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOff_Vali_003")
@pytest.mark.wifi_case(
    title="息屏，已连接状态但无流量，进入PowerSave模式验证",
    pre="无",
)
def test_Func_HalowLP_BasicState_ScreenOff_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_off_powersave_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_BasicState_ScreenOff_Vali_004")
@pytest.mark.wifi_case(
    title="息屏，PNO扫描成功后无流量或业务，进入powersave模式",
    pre="无",
)
def test_Func_HalowLP_BasicState_ScreenOff_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
