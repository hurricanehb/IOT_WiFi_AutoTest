"""WiFi 连接 — Func_AdvWlanSet_EnergySave（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.energy_save import (
    run_wlan_energy_save_airplane_toggle_persistence_case,
    run_wlan_energy_save_default_case,
    run_wlan_energy_save_display_case,
    run_wlan_energy_save_quick_settings_toggle_persistence_case,
    run_wlan_energy_save_reboot_persistence_case,
    run_wlan_energy_save_settings_toggle_persistence_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_UI_001")
@pytest.mark.wifi_case(
    title="默认配置“省电模式”UI检查",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_UI_002")
@pytest.mark.wifi_case(
    title="切换为“性能模式”UI检查",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_display_case(settings_ui, capsys, '性能模式')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Vali_001")
@pytest.mark.wifi_case(
    title="连接AP后亮屏-“省电模式”有效性",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Vali_002")
@pytest.mark.wifi_case(
    title="连接AP后息屏-“省电模式”有效性",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Vali_003")
@pytest.mark.wifi_case(
    title="连接AP后亮屏-“性能模式”有效性",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Vali_004")
@pytest.mark.wifi_case(
    title="连接AP后息屏-“性能模式”有效性",
    pre="1、测试环境：干扰环境下，如办公室",
)
def test_Func_AdvWlanSet_EnergySave_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配省电模式有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_EnergySave_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Int_001")
@pytest.mark.wifi_case(
    title="大流量（满载）功耗验证",
    pre="1、测试环境：硬件实验室",
)
def test_Func_AdvWlanSet_EnergySave_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Int_002")
@pytest.mark.wifi_case(
    title="小流量（ping包）功耗验证",
    pre="1、测试环境：硬件实验室",
)
def test_Func_AdvWlanSet_EnergySave_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Stb_001")
@pytest.mark.wifi_case(
    title="关机重启-WLAN省电配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_EnergySave_Stb_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_reboot_persistence_case(wifi, settings_ui, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Stb_002")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-WLAN省电配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_EnergySave_Stb_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Stb_003")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-WLAN省电配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_EnergySave_Stb_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_quick_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_EnergySave_Stb_004")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-WLAN省电配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_EnergySave_Stb_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_energy_save_airplane_toggle_persistence_case(settings_ui, capsys)
