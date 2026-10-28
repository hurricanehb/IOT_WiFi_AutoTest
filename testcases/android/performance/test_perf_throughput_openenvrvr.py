"""WiFi 连接 — Perf_ThroughPut_OpenEnvRVR（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_001")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-HyperWiFi -US-TCP",
    pre="1. 测试拓扑：Router-PC1-LAN-miniAP )) (( STA;",
)
def test_Perf_ThroughPut_OpenEnvRVR_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_002")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-HyperWiFi -EUS-TCP",
    pre="1. 测试拓扑：Router-PC1-LAN-miniAP )) (( STA;",
)
def test_Perf_ThroughPut_OpenEnvRVR_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_003")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-HyperWiFi -US-UDP",
    pre="1. 测试拓扑：Router-PC1-LAN-miniAP )) (( STA;",
)
def test_Perf_ThroughPut_OpenEnvRVR_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_004")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-HyperWiFi -EUS-UDP",
    pre="1. 测试拓扑：Router-PC1-LAN-miniAP )) (( STA;",
)
def test_Perf_ThroughPut_OpenEnvRVR_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_005")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-2.4G-TCP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_006")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-5G-TCP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_007")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-6G-TCP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_008")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-2.4G-UDP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_009")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-5G-UDP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_OpenEnvRVR_010")
@pytest.mark.wifi_case(
    title="开放环境RVR测试-WiFi-6G-UDP",
    pre="1.测试拓扑：PC---AP ))) ((( DUT",
)
def test_Perf_ThroughPut_OpenEnvRVR_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
