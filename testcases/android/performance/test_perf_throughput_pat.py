"""WiFi 连接 — Perf_ThroughPut_PAT（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.performance import run_pat_throughput_case

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_001")
@pytest.mark.wifi_case(
    title="PAT测试-HyperWiFi-US-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_002")
@pytest.mark.wifi_case(
    title="PAT测试-HyperWiFi-EUS-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_002(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_003")
@pytest.mark.wifi_case(
    title="PAT测试-HyperWiFi-US-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_003(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_004")
@pytest.mark.wifi_case(
    title="PAT测试-HyperWiFi-EUS-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_004(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_005")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-2.4G-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_005(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_006")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-5G-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_006(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_007")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-6G-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_007(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_008")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-2.4G-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_008(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_009")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-5G-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_009(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_PAT_010")
@pytest.mark.wifi_case(
    title="PAT测试-WiFi-6G-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---AP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_PAT_010(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pat_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml, attenuator_optional)
