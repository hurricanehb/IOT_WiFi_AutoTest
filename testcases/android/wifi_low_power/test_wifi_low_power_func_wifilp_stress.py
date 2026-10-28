"""WiFi 连接 — Func_WiFiLP_Stress（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.low_power import (
    run_connect_disconnect_stress_case,
    run_screen_cycle_stress_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_001")
@pytest.mark.wifi_case(
    title="频繁亮灭屏切换",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_screen_cycle_stress_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_002")
@pytest.mark.wifi_case(
    title="频繁连接/断开",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_connect_disconnect_stress_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_003")
@pytest.mark.wifi_case(
    title="大量保存网络",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_004")
@pytest.mark.wifi_case(
    title="高密度AP环境",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_005")
@pytest.mark.wifi_case(
    title="弱信号反复漫游",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_006")
@pytest.mark.wifi_case(
    title="息屏PNO与数据收发并发",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_007")
@pytest.mark.wifi_case(
    title="屏幕状态快速变化+网络切换",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_008")
@pytest.mark.wifi_case(
    title="路由器重启恢复",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stress_Vali_009")
@pytest.mark.wifi_case(
    title="休眠唤醒反复测试",
    pre="无",
)
def test_Func_WiFiLP_Stress_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
