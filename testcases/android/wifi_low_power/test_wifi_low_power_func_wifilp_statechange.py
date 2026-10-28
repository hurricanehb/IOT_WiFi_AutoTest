"""WiFi 连接 — Func_WiFiLP_StateChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_pno_disconnected_screen_off_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏→息屏（无流量）",
    pre="亮屏连接，无流量",
)
def test_Func_WiFiLP_StateChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_002")
@pytest.mark.wifi_case(
    title="息屏→亮屏（无流量）",
    pre="息屏连接，无流量",
)
def test_Func_WiFiLP_StateChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_003")
@pytest.mark.wifi_case(
    title="连接→断开（息屏）",
    pre="息屏连接，无流量",
)
def test_Func_WiFiLP_StateChange_Vali_003(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_pno_disconnected_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        hyper=False,
        screen_off_before_disconnect=True,
        verify_reconnect=False,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_004")
@pytest.mark.wifi_case(
    title="断开→连接（息屏）",
    pre="息屏断网，PNO扫描中",
)
def test_Func_WiFiLP_StateChange_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_pno_disconnected_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        hyper=False,
        screen_off_before_disconnect=True,
        verify_reconnect=True,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_005")
@pytest.mark.wifi_case(
    title="无流量→有流量（息屏）",
    pre="息屏连接，无流量",
)
def test_Func_WiFiLP_StateChange_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_StateChange_Vali_006")
@pytest.mark.wifi_case(
    title="有流量→无流量（息屏）",
    pre="息屏连接，持续ping",
)
def test_Func_WiFiLP_StateChange_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
