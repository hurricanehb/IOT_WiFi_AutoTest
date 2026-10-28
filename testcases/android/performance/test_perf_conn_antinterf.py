"""WiFi 连接 — Perf_Conn_AntInterf（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_001")
@pytest.mark.wifi_case(
    title="HyperWiFi同频干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_002")
@pytest.mark.wifi_case(
    title="HyperWiFi邻频干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_003")
@pytest.mark.wifi_case(
    title="WIFI同频干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC--AP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_004")
@pytest.mark.wifi_case(
    title="WIFI邻频干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC--AP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_005")
@pytest.mark.wifi_case(
    title="蜂窝干扰下吞吐量测试（自身和外界的蜂窝干扰、不同band）",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_006")
@pytest.mark.wifi_case(
    title="蓝牙干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_007")
@pytest.mark.wifi_case(
    title="RFID干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_008")
@pytest.mark.wifi_case(
    title="微波干扰下吞吐量测试",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_009")
@pytest.mark.wifi_case(
    title="穿墙干扰（嘉善环境）",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP 3.陪测试miniAP，加密方式WPA3",
)
def test_Perf_Conn_AntInterf_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_010")
@pytest.mark.wifi_case(
    title="竞争干扰-同类型设备同时跑流竞争-HyperWiFi",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_011")
@pytest.mark.wifi_case(
    title="竞争干扰-不同类型设备同时跑流竞争-HyperWiFi",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_012")
@pytest.mark.wifi_case(
    title="竞争干扰-同类型设备同时跑流竞争-WiFi 2.4G",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_013")
@pytest.mark.wifi_case(
    title="竞争干扰-不同类型设备同时跑流竞争-WiFi 2.4G",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_014")
@pytest.mark.wifi_case(
    title="竞争干扰-同类型设备同时跑流竞争-WiFi 5G",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Perf_Conn_AntInterf_015")
@pytest.mark.wifi_case(
    title="竞争干扰-不同类型设备同时跑流竞争-WiFi 5G",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_016")
@pytest.mark.wifi_case(
    title="竞争干扰-HyperWiFi性能测试-限1/2背景流量ping包",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Perf_Conn_AntInterf_017")
@pytest.mark.wifi_case(
    title="竞争干扰-WiFi性能测试-限1/2背景流量ping包",
    pre="1.测试环境：屏蔽房 2.拓扑：PC---上级网关---miniAP",
)
def test_Perf_Conn_AntInterf_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
