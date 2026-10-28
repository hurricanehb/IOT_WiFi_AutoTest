"""WiFi 连接 — Perf_Conn_AssocTime（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.performance import run_connection_latency_case

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AssocTime_001")
@pytest.mark.wifi_case(
    title="连接耗时-HyperWIFI",
    pre="1. 测试拓扑：Router-LAN-miniAP )) (( STA;",
)
def test_Perf_Conn_AssocTime_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_connection_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AssocTime_002")
@pytest.mark.wifi_case(
    title="连接耗时-WIFI 2.4G",
    pre="1. 测试拓扑：Router )) (( STA;",
)
def test_Perf_Conn_AssocTime_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_connection_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AssocTime_003")
@pytest.mark.wifi_case(
    title="连接耗时-WIFI 5G",
    pre="1. 测试拓扑：Router )) (( STA;",
)
def test_Perf_Conn_AssocTime_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_connection_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AssocTime_004")
@pytest.mark.wifi_case(
    title="连接耗时-WIFI 6G",
    pre="1. 测试拓扑：Router )) (( STA;",
)
def test_Perf_Conn_AssocTime_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_connection_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)
