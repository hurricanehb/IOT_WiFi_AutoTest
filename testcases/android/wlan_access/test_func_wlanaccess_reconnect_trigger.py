"""WiFi 连接 — Func_WlanAccess_Reconnect_Trigger（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_001")
@pytest.mark.wifi_case(
    title="Beacon Timeout 断连",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_002")
@pytest.mark.wifi_case(
    title="密码错误",
    pre="1、AP、miniAP配置wpa3加密",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_003")
@pytest.mark.wifi_case(
    title="认证超时",
    pre="/",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_004")
@pytest.mark.wifi_case(
    title="认证失败",
    pre="/",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_005")
@pytest.mark.wifi_case(
    title="关联失败",
    pre="1、接入点满载",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_006")
@pytest.mark.wifi_case(
    title="dhcp失败",
    pre="1、AP、miniAP关闭DHCP服务器",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Vali_007")
@pytest.mark.wifi_case(
    title="网关不可达主动断连",
    pre="1、AP、miniAP配置防ping或sta配置与AP、miniAP不同网段",
)
def test_Func_WlanAccess_Reconnect_Trigger_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Int_001")
@pytest.mark.wifi_case(
    title="不自动重连黑名单内ap",
    pre="1、测试环境：办公室工位 2、AC+AP拓扑，关闭陪测AP、miniAP的dhcp服务器",
)
def test_Func_WlanAccess_Reconnect_Trigger_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Int_002")
@pytest.mark.wifi_case(
    title="自动重连无外网ap",
    pre="1、陪测AP、miniAP无外网",
)
def test_Func_WlanAccess_Reconnect_Trigger_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_Trigger_Int_003")
@pytest.mark.wifi_case(
    title="连续 7 次失败（认证、关联、dhcp）触发 Watchdog",
    pre="1、陪测AP、miniAP关闭DHCPs",
)
def test_Func_WlanAccess_Reconnect_Trigger_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

