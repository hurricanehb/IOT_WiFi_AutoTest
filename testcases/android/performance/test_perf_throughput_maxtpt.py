"""WiFi 连接 — Perf_ThroughPut_MaxTpt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.performance import run_throughput_case

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_001")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-US-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_002")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-EUS-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_003")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-EU-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_004")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-TH-TCP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_005")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-2.4G-TCP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_006")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-5G-TCP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_007")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-6G-TCP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_008")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-US-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_009")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-EUS-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_010")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-EU-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_011")
@pytest.mark.wifi_case(
    title="极限吞吐量-HyperWiFi-EH-UDP",
    pre="1.测试环境：屏蔽箱 2.拓扑：PC---上级网关---miniAP --程控衰减 --DUT",
)
def test_Perf_ThroughPut_MaxTpt_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_012")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-2.4G-UDP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_013")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-5G-UDP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_014")
@pytest.mark.wifi_case(
    title="极限吞吐量-WiFi-6G-UDP",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_015")
@pytest.mark.wifi_case(
    title="不同加密方式(Open/WPA3)下的吞吐量",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_ThroughPut_MaxTpt_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        wifi_entry_id="hyperwifi_us",
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_016")
@pytest.mark.wifi_case(
    title="双WIFI网络，HyperWiFi为主网络吞吐量",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_ThroughPut_MaxTpt_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_017")
@pytest.mark.wifi_case(
    title="双WIFI网络，WiFi为主网络（2.4G/5G/6G）吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---AP))) ((( STA",
)
def test_Perf_ThroughPut_MaxTpt_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_018")
@pytest.mark.wifi_case(
    title="HyperWiFi抖动测试-30min",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---AP",
)
def test_Perf_ThroughPut_MaxTpt_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_ThroughPut_MaxTpt_019")
@pytest.mark.wifi_case(
    title="WIFI抖动测试-30min",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---AP",
)
def test_Perf_ThroughPut_MaxTpt_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_throughput_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)
