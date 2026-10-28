"""WiFi 连接 — Func_AdvWlanSet_RoamSens（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.roam_sensitivity import (
    run_wlan_roam_sensitivity_airplane_toggle_persistence_case,
    run_wlan_roam_sensitivity_custom_dialog_case,
    run_wlan_roam_sensitivity_custom_value_cannot_save_case,
    run_wlan_roam_sensitivity_custom_value_case,
    run_wlan_roam_sensitivity_cycle_case,
    run_wlan_roam_sensitivity_default_case,
    run_wlan_roam_sensitivity_display_case,
    run_wlan_roam_sensitivity_illegal_value_cannot_input_case,
    run_wlan_roam_sensitivity_options_case,
    run_wlan_roam_sensitivity_quick_settings_toggle_persistence_case,
    run_wlan_roam_sensitivity_reboot_persistence_case,
    run_wlan_roam_sensitivity_settings_toggle_persistence_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_001")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度默认值检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_002")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度可选项检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_options_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_003")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“5dB”检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_display_case(settings_ui, capsys, '5dB')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_004")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“7dB”检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_display_case(settings_ui, capsys, '7dB')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_005")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“9dB”检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_display_case(settings_ui, capsys, '9dB')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_006")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_custom_dialog_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_007")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”为“1”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_custom_value_case(settings_ui, capsys, '1', '1dB')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_008")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”为“20”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_custom_value_case(settings_ui, capsys, '20', '20dB')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_009")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值超出范围：“0”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_custom_value_cannot_save_case(settings_ui, capsys, '0')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_010")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值超出范围：“21”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_010(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_custom_value_cannot_save_case(settings_ui, capsys, '21')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_011")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值非法：“小数”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_illegal_value_cannot_input_case(settings_ui, capsys, '19.9', '小数')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_012")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值非法：“中文”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_013")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值非法：“字母”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_UI_014")
@pytest.mark.wifi_case(
    title="WLAN漫游灵敏度设置“自定义”值非法：“特殊字符”",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_UI_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_001")
@pytest.mark.wifi_case(
    title="灵敏度“8dB”，2.4g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_002")
@pytest.mark.wifi_case(
    title="灵敏度“5dB”，2.4g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_003")
@pytest.mark.wifi_case(
    title="灵敏度“10dB”，2.4g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_004")
@pytest.mark.wifi_case(
    title="灵敏度自定义“20dB”，2.4g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_005")
@pytest.mark.wifi_case(
    title="灵敏度自定义“1dB”，2.4g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_006")
@pytest.mark.wifi_case(
    title="灵敏度“8dB”，5g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_007")
@pytest.mark.wifi_case(
    title="灵敏度“5dB”，5g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_008")
@pytest.mark.wifi_case(
    title="灵敏度“10dB”，5g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_009")
@pytest.mark.wifi_case(
    title="灵敏度自定义“20dB”，5g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_010")
@pytest.mark.wifi_case(
    title="灵敏度自定义“1dB”，5g频段切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_011")
@pytest.mark.wifi_case(
    title="灵敏度“8dB”，双频合一漫游切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_012")
@pytest.mark.wifi_case(
    title="灵敏度“5dB”，双屏合一漫游切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_013")
@pytest.mark.wifi_case(
    title="灵敏度“10dB”，双屏合一漫游切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_014")
@pytest.mark.wifi_case(
    title="灵敏度自定义“20dB”，双屏合一漫游切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Vali_015")
@pytest.mark.wifi_case(
    title="灵敏度自定义“1dB”，双屏合一漫游切换检查",
    pre="1、DUT的WLAN漫游阈值为“中”，即-65dBm 2、AP1、AP2在同一直线上，信号重叠，初始位置分别位于DUT -65dBm处",
)
def test_Func_AdvWlanSet_RoamSens_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配漫游灵敏度有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_RoamSens_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Stb_001")
@pytest.mark.wifi_case(
    title="关机重启-漫游灵敏度配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_Stb_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_reboot_persistence_case(wifi, settings_ui, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Stb_002")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-漫游灵敏度配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_Stb_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Stb_003")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-漫游灵敏度配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_Stb_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_quick_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Stb_004")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-漫游灵敏度配置不变",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_Stb_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_airplane_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_RoamSens_Stb_005")
@pytest.mark.wifi_case(
    title="多次切换配置一致性",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_RoamSens_Stb_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_roam_sensitivity_cycle_case(settings_ui, run_shell_cmd, capsys)
