"""WiFi 连接 — Func_HalowLP_DoubleWifi_ScrChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.hyperwifi_low_power import (
    run_hyperwifi_dual_screen_transition_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScrChange_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏连接双WiFi-断开WiFi后息屏，HyperWiFi（无流量等）进入低功耗PowerSave模式",
    pre="1、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScrChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_transition_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="disconnect_wifi_then_sleep",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScrChange_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏连接双WiFi-断开HyperWiFi后息屏，HyperWiFi（无扫描等）进入低功耗IDLE模式",
    pre="1、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScrChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_transition_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="disconnect_hyper_then_sleep",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScrChange_Vali_003")
@pytest.mark.wifi_case(
    title="息屏连接双WiFi（HyperWiFi为PS）-亮屏后HyperWiFi切换为唤醒状态",
    pre="1、已连接双WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScrChange_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_transition_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="dual_sleep_wake",
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScrChange_Vali_004")
@pytest.mark.wifi_case(
    title="息屏只连接WiFi（HyperWiFi为IDLE）-亮屏后HyperWiFi切换为唤醒状态",
    pre="1、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScrChange_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_dual_screen_transition_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        operation="wifi_only_sleep_wake",
    )

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_DoubleWifi_ScrChange_Int_001")
@pytest.mark.wifi_case(
    title="整机低功耗休眠唤醒HyperWiFi",
    pre="1、已连接WiFi",
)
def test_Func_HalowLP_DoubleWifi_ScrChange_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
