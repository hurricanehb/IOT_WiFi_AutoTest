"""WiFi 连接 — Func_HalowLP_StateChange_ScrChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.hyperwifi_low_power import (
    run_hyperwifi_disconnected_screen_off_idle_case,
    run_hyperwifi_screen_cycle_stability_case,
    run_hyperwifi_unconnected_screen_wake_case,
    run_hyperwifi_screen_wake_active_case,
    run_hyperwifi_screen_off_powersave_case,
)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Vali_001")
@pytest.mark.wifi_case(
    title="已连接状态亮屏->息屏（无业务或流量等），进入低功耗PowerSave模式",
    pre="无",
)
def test_Func_HalowLP_StateChange_ScrChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_off_powersave_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏状态断开连接->息屏（无扫描等），进入低功耗IDLE模式",
    pre="无",
)
def test_Func_HalowLP_StateChange_ScrChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_disconnected_screen_off_idle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, clear_saved=False
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Vali_003")
@pytest.mark.wifi_case(
    title="亮屏状态取消保存网络（无保存网络）->息屏（无扫描等），进入低功耗IDLE模式",
    pre="无",
)
def test_Func_HalowLP_StateChange_ScrChange_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_disconnected_screen_off_idle_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, clear_saved=True
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Vali_004")
@pytest.mark.wifi_case(
    title="未连接息屏，再亮屏，立即退出IDLE模式",
    pre="1、未连接HyperWiFi",
)
def test_Func_HalowLP_StateChange_ScrChange_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_unconnected_screen_wake_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Vali_005")
@pytest.mark.wifi_case(
    title="已连接息屏，再亮屏，立即退出PowerSave模式",
    pre="无",
)
def test_Func_HalowLP_StateChange_ScrChange_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_wake_active_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Stb_001")
@pytest.mark.wifi_case(
    title="未连接状态，亮屏息屏互切低功耗状态检查",
    pre="1、未连接HyperWiFi",
)
def test_Func_HalowLP_StateChange_ScrChange_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_cycle_stability_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, connected=False
    )

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_HalowLP_StateChange_ScrChange_Stb_002")
@pytest.mark.wifi_case(
    title="已连接状态，亮屏息屏互切低功耗状态检查",
    pre="1、已连接HyperWiFi",
)
def test_Func_HalowLP_StateChange_ScrChange_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hyperwifi_screen_cycle_stability_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, connected=True
    )
