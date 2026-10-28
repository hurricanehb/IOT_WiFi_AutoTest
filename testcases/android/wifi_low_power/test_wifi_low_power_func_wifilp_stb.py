"""WiFi 连接 — Func_WiFiLP_Stb（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stb_Vali_001")
@pytest.mark.wifi_case(
    title="长时间待机-已连接",
    pre="息屏连接，静置24小时，每小时记录",
)
def test_Func_WiFiLP_Stb_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stb_Vali_002")
@pytest.mark.wifi_case(
    title="长时间待机-未连接有保存网络",
    pre="息屏断网有保存网络，静置24小时",
)
def test_Func_WiFiLP_Stb_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stb_Vali_003")
@pytest.mark.wifi_case(
    title="长时间待机-无保存网络",
    pre="无",
)
def test_Func_WiFiLP_Stb_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stb_Vali_004")
@pytest.mark.wifi_case(
    title="长时间大流量下载",
    pre="亮屏连续下载4小时",
)
def test_Func_WiFiLP_Stb_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WiFiLP_Stb_Vali_005")
@pytest.mark.wifi_case(
    title="弱信号保持",
    pre="无",
)
def test_Func_WiFiLP_Stb_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
