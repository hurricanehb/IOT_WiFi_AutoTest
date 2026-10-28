"""WiFi 连接 — Func_Roam_SWiFi_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Roam_SWiFi_User_001")
@pytest.mark.wifi_case(
    title="3台同ssid之间进行漫游（rssi优先）",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA",
)
def test_Func_Roam_SWiFi_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Roam_SWiFi_User_002")
@pytest.mark.wifi_case(
    title="2台同ssid+1台不同ssid+漫游优先",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_SWiFi_User_003")
@pytest.mark.wifi_case(
    title="2台同ssid+1台不同ssid+不可漫游后进行弱信号网络切换",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Roam_SWiFi_User_004")
@pytest.mark.wifi_case(
    title="2台同ssid+1台不同ssid+漫游与网络选择并行",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_SWiFi_User_005")
@pytest.mark.wifi_case(
    title="HyperWiFi漫游切换ping包验证",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_SWiFi_User_006")
@pytest.mark.wifi_case(
    title="HyperWiFi漫游切换跑流验证",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_SWiFi_User_007")
@pytest.mark.wifi_case(
    title="pno连接亮屏后rssi≥阈值（差值＜5）立即触发漫游扫描",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、miniAP1和miniAP2同ssid",
)
def test_Func_Roam_SWiFi_User_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
