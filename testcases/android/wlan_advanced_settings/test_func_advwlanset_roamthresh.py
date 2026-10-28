"""WiFi 连接 — Func_AdvWlanSet_RoamThresh（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.roam_threshold import (
    run_wlan_roam_threshold_airplane_toggle_persistence_case,
    run_wlan_roam_threshold_custom_dialog_case,
    run_wlan_roam_threshold_custom_value_cannot_save_case,
    run_wlan_roam_threshold_custom_value_case,
    run_wlan_roam_threshold_cycle_case,
    run_wlan_roam_threshold_default_case,
    run_wlan_roam_threshold_display_case,
    run_wlan_roam_threshold_illegal_value_cannot_input_case,
    run_wlan_roam_threshold_options_case,
    run_wlan_roam_threshold_quick_settings_toggle_persistence_case,
    run_wlan_roam_threshold_reboot_persistence_case,
    run_wlan_roam_threshold_settings_toggle_persistence_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_001")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值默认值检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_002")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值可选项检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_options_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_003")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“高”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_display_case(settings_ui, capsys, '高')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_004")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“中”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_display_case(settings_ui, capsys, '中')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_005")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“低”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_display_case(settings_ui, capsys, '低')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_006")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_dialog_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_007")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”为“50”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_case(settings_ui, capsys, '50', '-50dBm')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_008")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”为“90”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_case(settings_ui, capsys, '90', '-90dBm')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_009")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”为“60”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_case(settings_ui, capsys, '60', '高')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_010")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”为“65”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_010(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_case(settings_ui, capsys, '65', '中')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_011")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”为“70”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_case(settings_ui, capsys, '70', '低')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_012")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值超出范围：“49”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_012(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_cannot_save_case(settings_ui, capsys, '49')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_013")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值超出范围：“91”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_013(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_custom_value_cannot_save_case(settings_ui, capsys, '91')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_014")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值非法：“小数”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_014(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_illegal_value_cannot_input_case(settings_ui, capsys, '70.2', '小数')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_015")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值非法：“中文”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_016")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值非法：“字母”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_UI_017")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值设置“自定义”值非法：“特殊字符”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_UI_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_001")
@pytest.mark.wifi_case(
    title="WLAN漫游默认阈值“中”，2.4g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_002")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“高”，2.4g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_003")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“低”，2.4g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_004")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-55dBm”，2.4g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_005")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-75dBm”，2.4g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_006")
@pytest.mark.wifi_case(
    title="WLAN漫游默认阈值“中”，5g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_007")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“高”，5g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_008")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“低”，5g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_009")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-55dBm”，5g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_010")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-75dBm”，5g频段切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP1、AP2（关闭双频合一）：设置同样的SSID-2.4G、SSID-5G 3、AP1、AP2在同一直线摆放，信号有重叠，两者的相对信号差：8~100dB，建议放在-90dBm处",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_011")
@pytest.mark.wifi_case(
    title="WLAN漫游默认阈值“中”，双频合一漫游切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP：开启双频合一",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_012")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“高”，双频合一漫游切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP：开启双频合一",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_013")
@pytest.mark.wifi_case(
    title="WLAN漫游阈值“低”，双频合一漫游切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP：开启双频合一",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_014")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-55dBm”，双频合一漫游切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP：开启双频合一",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Vali_015")
@pytest.mark.wifi_case(
    title="WLAN漫游自定义阈值“-75dBm”，双频合一漫游切换检查",
    pre="1、灵敏度默认“8dB” 2、陪测试AP：开启双频合一",
)
def test_Func_AdvWlanSet_RoamThresh_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配漫游阈值有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_RoamThresh_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Stb_001")
@pytest.mark.wifi_case(
    title="关机重启-漫游阈值配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_Stb_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_reboot_persistence_case(wifi, settings_ui, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Stb_002")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-漫游阈值配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_Stb_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Stb_003")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-漫游阈值配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_Stb_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_quick_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Stb_004")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-漫游阈值配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_Stb_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_airplane_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamThresh_Stb_005")
@pytest.mark.wifi_case(
    title="多次切换配置一致性",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamThresh_Stb_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_threshold_cycle_case(settings_ui, run_shell_cmd, capsys)
