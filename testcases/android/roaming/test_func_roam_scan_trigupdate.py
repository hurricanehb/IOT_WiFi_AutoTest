"""WiFi 连接 — Func_Roam_Scan_TrigUpdate（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_001")
@pytest.mark.wifi_case(
    title="漫游失败后则更新为“阈值 -5”",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_002")
@pytest.mark.wifi_case(
    title="漫游成功后阈值重置（判断-75dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、当前已连接miniAP1，漫游阈值为-80dBm",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_003")
@pytest.mark.wifi_case(
    title="远近移动断连回连后+阈值更新测试（判断强弱信号）",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_004")
@pytest.mark.wifi_case(
    title="cur_rssi>-75dBm=漫游阈值时阈值不变（-75dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、陪测miniAP1处于强信号下",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_005")
@pytest.mark.wifi_case(
    title="强信号下“阈值+5<cur_rssi≤-75dBm”则更新为“cur_rssi - 5”",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、陪测miniAP1处于强信号下",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_006")
@pytest.mark.wifi_case(
    title="强信号下“cur_rssi同时>阈值+5和-75dBm”则更新为 “-75dBm”",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、陪测miniAP1处于强信号下",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Roam_Scan_TrigUpdate_Vali_007")
@pytest.mark.wifi_case(
    title="强信号下漫游阈值更新老化时间2分钟有效验证",
    pre="1、测试环境：实验室屏蔽箱 2、测试拓扑：AC（可联网）+1AP/3miniAP(同ssid/密码)---衰减器---STA 3、陪测miniAP1处于强信号下",
)
def test_Func_Roam_Scan_TrigUpdate_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
