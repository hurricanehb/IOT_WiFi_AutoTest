"""WiFi 连接 — Func_BlolckList_Exempt_BSSID（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Vali_001")
@pytest.mark.wifi_case(
    title="没外网",
    pre="1、测试环境：办公室工位 2、陪测AP无互联网 3、AC+AP网络无外网，可触发",
)
def test_Func_BlolckList_Exempt_BSSID_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Vali_002")
@pytest.mark.wifi_case(
    title="ip获取失败",
    pre="1、测试环境：办公室工位 2、关闭陪测AP的DHCP 3、AC+AP网络关闭DHCP，可触发",
)
def test_Func_BlolckList_Exempt_BSSID_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Vali_003")
@pytest.mark.wifi_case(
    title="连AP过程中出现非本地断开",
    pre="/",
)
def test_Func_BlolckList_Exempt_BSSID_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Vali_004")
@pytest.mark.wifi_case(
    title="连接超时",
    pre="/",
)
def test_Func_BlolckList_Exempt_BSSID_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Vali_005")
@pytest.mark.wifi_case(
    title="认证失败",
    pre="/",
)
def test_Func_BlolckList_Exempt_BSSID_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Int_001")
@pytest.mark.wifi_case(
    title="同一SSID下不同BSSID的独立黑名单机制",
    pre="1、AP1、AP2相同SSID",
)
def test_Func_BlolckList_Exempt_BSSID_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_Exempt_BSSID_Int_002")
@pytest.mark.wifi_case(
    title="BSSID黑名单+漫游",
    pre="1、漫游环境",
)
def test_Func_BlolckList_Exempt_BSSID_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
