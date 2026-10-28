"""WiFi 连接 — Func_Components_Welcome_ScanList_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder, wifi_case

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ScanList_User_001")
@pytest.mark.wifi_case(
    title="未连接网络时上下滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Welcome_ScanList_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ScanList_User_002")
@pytest.mark.wifi_case(
    title="单WiFi连接过程中上下滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Welcome_ScanList_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ScanList_User_003")
@pytest.mark.wifi_case(
    title="双WiFi依次连接过程中上下滑动WLAN列表",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Welcome_ScanList_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ScanList_User_004")
@pytest.mark.wifi_case(
    title="双WIFi依次断开过程中-上行滑动WLAN列表不卡顿",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Welcome_ScanList_User_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_ScanList_User_005")
@pytest.mark.wifi_case(
    title="删除网络的过程中-上下滑动无线列表",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Welcome_ScanList_User_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

