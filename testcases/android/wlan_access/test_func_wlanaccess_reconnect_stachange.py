"""WiFi 连接 — Func_WlanAccess_Reconnect_StaChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Excp_001")
@pytest.mark.wifi_case(
    title="STA开关机自动重连-超长GBK编码",
    pre="1. 陪测试设备为锐捷AP720-A 2. AP配置16位GBK编码SSBD 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Excp_002")
@pytest.mark.wifi_case(
    title="STA开关机自动重连-已保存多个GBK编码网络且共网关",
    pre="1. 搭建网络拓扑：AC+AP--STA； 2. AC已运行DHCP服务器，IP pool：192.168.1/10~20； 3. 创建n≥2个GBK编码 SSID",
)
def test_Func_WlanAccess_Reconnect_StaChange_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_001")
@pytest.mark.wifi_case(
    title="STA软重启自动重连",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_002")
@pytest.mark.wifi_case(
    title="STA开关机自动重连",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_003")
@pytest.mark.wifi_case(
    title="setting页面-wlan开关“禁用启用”自动重连",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_004")
@pytest.mark.wifi_case(
    title="systemUI组件-wlan开关“禁用启用”自动重连",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_005")
@pytest.mark.wifi_case(
    title="systemUI组件-飞行模式“禁用启用”自动重连",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_006")
@pytest.mark.wifi_case(
    title="网络详情切换隐私选项",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_007")
@pytest.mark.wifi_case(
    title="网络详情切换IP设置选项",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Vali_008")
@pytest.mark.wifi_case(
    title="改配WLAN高级设置选项",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

