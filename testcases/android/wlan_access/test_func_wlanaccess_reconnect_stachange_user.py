"""WiFi 连接 — Func_WlanAccess_Reconnect_StaChange_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_User_001")
@pytest.mark.wifi_case(
    title="STA远近移动拉断回连",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_StaChange_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_User_002")
@pytest.mark.wifi_case(
    title="断开当前网络，自动重连另一个已保存的网络",
    pre="1. 搭建网络拓扑：AP1/AP2--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，AP开启WiFi； 3. AP和STA放置于强干扰环境，如办公室 4. STA已安装wifi魔盒",
)
def test_Func_WlanAccess_Reconnect_StaChange_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_User_003")
@pytest.mark.wifi_case(
    title="取消保存当前网络，自动重连另一个已保存的网络",
    pre="1. 搭建网络拓扑：AP1/AP2--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，AP开启WiFi； 3. AP和STA放置于强干扰环境，如办公室 4. STA已安装wifi魔盒",
)
def test_Func_WlanAccess_Reconnect_StaChange_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

