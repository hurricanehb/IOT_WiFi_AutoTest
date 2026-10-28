"""WiFi 连接 — Func_Components_SystemUI_ScanList_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_User_001")
@pytest.mark.wifi_case(
    title="未连接网络时上下滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_User_002")
@pytest.mark.wifi_case(
    title="单WifFi-连接WiFi过程中-上下滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_User_003")
@pytest.mark.wifi_case(
    title="单WifFi-连接HyperWiFi过程中-上下滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_User_004")
@pytest.mark.wifi_case(
    title="双WiFi-已连接WiFi再连接HyperWiFi过程中-上下滑动WLAN列表",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_User_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
