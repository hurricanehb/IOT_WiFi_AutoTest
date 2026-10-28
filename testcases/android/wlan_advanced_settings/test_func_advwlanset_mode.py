"""WiFi 连接 — Func_AdvWlanSet_Mode（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.mode import (
    run_wlan_mode_default_case,
    run_wlan_mode_display_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_001")
@pytest.mark.wifi_case(
    title="配置默认选项检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_002")
@pytest.mark.wifi_case(
    title="设置“802.11a/b/g”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 ABG')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_003")
@pytest.mark.wifi_case(
    title="设置“802.11b”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 B')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_004")
@pytest.mark.wifi_case(
    title="设置“802.11g”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 G')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_005")
@pytest.mark.wifi_case(
    title="设置“802.11 N”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 N')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_006")
@pytest.mark.wifi_case(
    title="设置“802.11b only”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 B only')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_007")
@pytest.mark.wifi_case(
    title="设置“802.11 G only”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 G only')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_008")
@pytest.mark.wifi_case(
    title="设置“802.11 N only”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 N only')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_009")
@pytest.mark.wifi_case(
    title="设置“802.11 AC only”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 AC only')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_010")
@pytest.mark.wifi_case(
    title="设置“802.11g/n”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_011")
@pytest.mark.wifi_case(
    title="设置“802.11ac”菜单显示检查",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_mode_display_case(settings_ui, capsys, '802.11 AC')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_UI_012")
@pytest.mark.wifi_case(
    title="设置弹窗“取消”按钮",
    pre="DUT出厂状态",
)
def test_Func_AdvWlanSet_Mode_UI_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_001")
@pytest.mark.wifi_case(
    title="WLAN模式默认值有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式）：频宽、信道自动 腾达AC1200M（AC9）、WIFI6路由器 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_002")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 a/b/g有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_003")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 b/g有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_004")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 g有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_005")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 a有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_006")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 b有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_007")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 a/b/g/n有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_008")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 b/g/n有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_009")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 a/n有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_010")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 g/n有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_011")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 ac有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_012")
@pytest.mark.wifi_case(
    title="WLAN模式设置802.11 anac有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Vali_013")
@pytest.mark.wifi_case(
    title="WLAN关闭情况下设置模式有效性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配WLAN模式有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_Mode_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Int_001")
@pytest.mark.wifi_case(
    title="2.4G频段-WLAN模式选项自适应",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Int_002")
@pytest.mark.wifi_case(
    title="5G频段-WLAN模式选项自适应",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Int_003")
@pytest.mark.wifi_case(
    title="自适应频段-WLAN模式选项自适应",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Stb_001")
@pytest.mark.wifi_case(
    title="关机重启-WLAN模式配置不变",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Stb_002")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-WLAN模式配置不变",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Stb_003")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-WLAN模式配置不变",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Stb_004")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-WLAN模式配置不变",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Stb_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_Mode_Stb_005")
@pytest.mark.wifi_case(
    title="多次切换配置一致性",
    pre="1. STA恢复出厂设置 2. 陪测AP（可设置无线协议模式） 3、屏蔽房或近距离无干扰环境",
)
def test_Func_AdvWlanSet_Mode_Stb_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
