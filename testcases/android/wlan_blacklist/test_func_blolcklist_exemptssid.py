"""WiFi 连接 — Func_BlolckList_ExemptSSID（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_001")
@pytest.mark.wifi_case(
    title="身份验证失败（即非密码错误或 EAP 失败）",
    pre="1、测试环境：办公室工位 2、陪测AP配置802.1x认证接入",
)
def test_Func_BlolckList_ExemptSSID_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_002")
@pytest.mark.wifi_case(
    title="ip获取失败",
    pre="1、测试环境：办公室工位 2、关闭陪测AP的DHCP",
)
def test_Func_BlolckList_ExemptSSID_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_003")
@pytest.mark.wifi_case(
    title="没外网（临时-网络验证失败，但用户表示他们希望将来始终连接到此网络）",
    pre="1、测试环境：办公室工位 2、陪测AP无互联网",
)
def test_Func_BlolckList_ExemptSSID_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_004")
@pytest.mark.wifi_case(
    title="没外网（永久）",
    pre="1、测试环境：办公室工位 2、陪测AP无互联网",
)
def test_Func_BlolckList_ExemptSSID_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_005")
@pytest.mark.wifi_case(
    title="网络连接连续失败五次或超过五次",
    pre="1、测试环境：办公室工位 2、关闭陪测AP的DHCP",
)
def test_Func_BlolckList_ExemptSSID_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_BlolckList_ExemptSSID_Vali_006")
@pytest.mark.wifi_case(
    title="请求方在扫描结果中未找到与框架请求连接的网络（包括网络功能）匹配的网络",
    pre="/",
)
def test_Func_BlolckList_ExemptSSID_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
