"""WiFi 连接 — Perf_Latency_Ping（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.performance import run_ping_latency_case

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Latency_Ping_001")
@pytest.mark.wifi_case(
    title="HyperWiFi ，ping大包测试",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Latency_Ping_002")
@pytest.mark.wifi_case(
    title="HyperWiFi ，ping小包测试",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Latency_Ping_003")
@pytest.mark.wifi_case(
    title="WiFi ，ping大包测试",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Latency_Ping_004")
@pytest.mark.wifi_case(
    title="WiFi ，ping小包测试",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Latency_Ping_005")
@pytest.mark.wifi_case(
    title="HyperWiFi ，ping大包测试-12h小时",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Latency_Ping_006")
@pytest.mark.wifi_case(
    title="HyperWiFi ，ping小包测试-12小时",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Latency_Ping_007")
@pytest.mark.wifi_case(
    title="WiFi ，ping大包测试-12h小时",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Latency_Ping_008")
@pytest.mark.wifi_case(
    title="WiFi ，ping小包测试-12小时",
    pre="1.测试环境：屏蔽箱 2.拓扑：AP---上级网关---miniAP 3.陪测AP，信道/频宽为auto，WPA/WPA2 4.陪测miniAP，加密方式WPA3.自动信道",
)
def test_Perf_Latency_Ping_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_ping_latency_case(wifi_case, run_shell_cmd, wifi, wifi_yaml)
