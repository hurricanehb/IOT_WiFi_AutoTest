"""WiFi 连接 — Func_PriBakLink_Service_SameSide（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Service_SameSide_Stb_001")
@pytest.mark.wifi_case(
    title="WiFi与HyperWiFi互切-持续跑流测试",
    pre="1、拓扑：AP与miniAP分别有线连接同一上级网关，AP---上级网关---miniAP 2、AP与miniAP放置在同一位置上（如同一个工位上）",
)
def test_Func_PriBakLink_Service_SameSide_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Service_SameSide_Stb_002")
@pytest.mark.wifi_case(
    title="WiFi与HyperWiFi互切-持续ping测试",
    pre="1、拓扑：AP与miniAP分别有线连接同一上级网关，AP---上级网关---miniAP 2、AP与miniAP放置在同一位置上（如同一个工位上）",
)
def test_Func_PriBakLink_Service_SameSide_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Service_SameSide_Stb_003")
@pytest.mark.wifi_case(
    title="WiFi与HyperWiFi互切-云端在线检查",
    pre="1、拓扑：AP与miniAP分别有线连接同一上级网关，AP---上级网关---miniAP 2、AP与miniAP放置在同一位置上（如同一个工位上）",
)
def test_Func_PriBakLink_Service_SameSide_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
