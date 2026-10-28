"""WiFi 连接 — Func_WiFiLP_Apf（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_001")
@pytest.mark.wifi_case(
    title="APF规则下发与生效",
    pre="亮屏连接，配置APF规则（如过滤ICMP）",
)
def test_Func_WiFiLP_Apf_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_002")
@pytest.mark.wifi_case(
    title="息屏APF过滤效果",
    pre="息屏连接，配置APF过滤ICMP",
)
def test_Func_WiFiLP_Apf_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_003")
@pytest.mark.wifi_case(
    title="APF规则更新",
    pre="亮屏连接，初始无过滤规则",
)
def test_Func_WiFiLP_Apf_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_004")
@pytest.mark.wifi_case(
    title="APF计数器读取",
    pre="亮屏连接，有APF规则",
)
def test_Func_WiFiLP_Apf_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_005")
@pytest.mark.wifi_case(
    title="切换网络APF重置",
    pre="连接AP1，配置特定APF规则",
)
def test_Func_WiFiLP_Apf_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Apf_Vali_006")
@pytest.mark.wifi_case(
    title="复杂APF规则压力",
    pre="构造超长/复杂APF字节码",
)
def test_Func_WiFiLP_Apf_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
