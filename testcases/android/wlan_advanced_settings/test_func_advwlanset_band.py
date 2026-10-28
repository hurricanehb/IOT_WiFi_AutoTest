"""WiFi 连接 — Func_AdvWlanSet_Band（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.band import (
    run_wlan_band_default_case,
    run_wlan_band_display_case,
    run_wlan_band_reboot_persistence_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_UI_001")
@pytest.mark.wifi_case(
    title="配置默认选项检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Band_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_band_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_UI_002")
@pytest.mark.wifi_case(
    title="设置2.4G 显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Band_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_band_display_case(settings_ui, capsys, '2.4GHz')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_UI_003")
@pytest.mark.wifi_case(
    title="设置5G 显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Band_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_band_display_case(settings_ui, capsys, '5GHz')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_UI_004")
@pytest.mark.wifi_case(
    title="设置弹窗“取消”按钮",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Band_UI_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_Vali_001")
@pytest.mark.wifi_case(
    title="频段默认设置-自动选择",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Band_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_Vali_002")
@pytest.mark.wifi_case(
    title="频段设置2.4GHz",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Band_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_Vali_003")
@pytest.mark.wifi_case(
    title="频段设置5GHz",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Band_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_Vali_004")
@pytest.mark.wifi_case(
    title="频段设置6GHz",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Band_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Band_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配频段有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Band_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_001")
@pytest.mark.wifi_case(
    title="自动与2.4GHz反复切换配置有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_002")
@pytest.mark.wifi_case(
    title="2.4GHz与5GHz反复切换配置有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_003")
@pytest.mark.wifi_case(
    title="5GHz与2.4GHz反复切换配置有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_004")
@pytest.mark.wifi_case(
    title="关机重启-WLAN频段配置不变",
    pre="无",
)
def test_Func_AdvWlanSet_Band_Stb_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_band_reboot_persistence_case(wifi, settings_ui, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_005")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-WLAN频段配置不变",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_006")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-WLAN频段配置不变",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Band_Stb_007")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-WLAN频段配置不变",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP启用WIFI，关闭双频合一；",
)
def test_Func_AdvWlanSet_Band_Stb_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
