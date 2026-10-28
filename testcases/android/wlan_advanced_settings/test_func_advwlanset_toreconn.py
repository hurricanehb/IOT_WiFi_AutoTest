"""WiFi 连接 — Func_AdvWlanSet_ToReconn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.advanced_settings.timeout_disconnect import (
    run_wlan_timeout_disconnect_airplane_toggle_persistence_case,
    run_wlan_timeout_disconnect_custom_dialog_case,
    run_wlan_timeout_disconnect_custom_value_cannot_save_case,
    run_wlan_timeout_disconnect_custom_value_case,
    run_wlan_timeout_disconnect_default_case,
    run_wlan_timeout_disconnect_display_case,
    run_wlan_timeout_disconnect_illegal_value_cannot_input_case,
    run_wlan_timeout_disconnect_options_case,
    run_wlan_timeout_disconnect_quick_settings_toggle_persistence_case,
    run_wlan_timeout_disconnect_reboot_persistence_case,
    run_wlan_timeout_disconnect_settings_toggle_persistence_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_001")
@pytest.mark.wifi_case(
    title="默认UI配置页面检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_options_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_002")
@pytest.mark.wifi_case(
    title="UI默认配置值检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_default_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_003")
@pytest.mark.wifi_case(
    title="超时断连设置3秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_display_case(settings_ui, capsys, '3秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_004")
@pytest.mark.wifi_case(
    title="超时断连设置5秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_display_case(settings_ui, capsys, '5秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_005")
@pytest.mark.wifi_case(
    title="超时断连设置8秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_display_case(settings_ui, capsys, '8秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_006")
@pytest.mark.wifi_case(
    title="超时断连设置12秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_display_case(settings_ui, capsys, '12秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_007")
@pytest.mark.wifi_case(
    title="超时断连设置16秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_display_case(settings_ui, capsys, '16秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_008")
@pytest.mark.wifi_case(
    title="超时断连设置自定义弹窗检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_dialog_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_009")
@pytest.mark.wifi_case(
    title="超时断连设置自定义3秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_case(settings_ui, capsys, '3', '3秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_010")
@pytest.mark.wifi_case(
    title="超时断连设置自定义11秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_010(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_case(settings_ui, capsys, '11', '11秒')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_011")
@pytest.mark.wifi_case(
    title="超时断连设置自定义20秒检查",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_case(settings_ui, capsys, '20', '20秒')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_012")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置数值超出范围：小于3",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_012(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_cannot_save_case(settings_ui, capsys, '2')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_013")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置数值超出范围：大于20",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_013(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_cannot_save_case(settings_ui, capsys, '21')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_014")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置非法：小数",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_014(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_illegal_value_cannot_input_case(settings_ui, capsys, '10.2', '小数')

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_015")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置非法：中文",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_016")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置非法：特殊字符",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_017")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置非法：英文字母",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_UI_018")
@pytest.mark.wifi_case(
    title="超时断连设置：自定义设置非法：空",
    pre="STA出厂状态",
)
def test_Func_AdvWlanSet_ToReconn_UI_018(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_custom_value_cannot_save_case(settings_ui, capsys, '')

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_001")
@pytest.mark.wifi_case(
    title="超时断连设置3秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_002")
@pytest.mark.wifi_case(
    title="超时断连设置5秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_003")
@pytest.mark.wifi_case(
    title="超时断连设置8秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_004")
@pytest.mark.wifi_case(
    title="超时断连设置12秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_005")
@pytest.mark.wifi_case(
    title="超时断连设置16秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_006")
@pytest.mark.wifi_case(
    title="超时断连设置自定义20秒有效性测试",
    pre="1、测试环境：屏蔽房 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Vali_007")
@pytest.mark.wifi_case(
    title="时效内重新接受AP的beacon包，规则不生效",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Excp_001")
@pytest.mark.wifi_case(
    title="WLAN关闭状态下改配超时断连设置有效",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_AdvWlanSet_ToReconn_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Stb_001")
@pytest.mark.wifi_case(
    title="时效内反复接收到AP的beacon包",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Stb_002")
@pytest.mark.wifi_case(
    title="关机重启-WLAN超时配置不变",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Stb_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_reboot_persistence_case(wifi, settings_ui, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Stb_003")
@pytest.mark.wifi_case(
    title="WLAN开关启用/禁用-WLAN超时配置不变",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Stb_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Stb_004")
@pytest.mark.wifi_case(
    title="快速设置栏禁用/启用-WLAN超时配置不变",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Stb_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_quick_settings_toggle_persistence_case(settings_ui, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_AdvWlanSet_ToReconn_Stb_005")
@pytest.mark.wifi_case(
    title="飞行模式禁用/启用-WLAN超时配置不变",
    pre="1、测试环境：屏蔽房、屏蔽箱 2、陪测设备：台式PC、AP（设置好无线配置）、无线网卡 3、辅助工具：抓包软件omnipeek",
)
def test_Func_AdvWlanSet_ToReconn_Stb_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, capsys
,
    wifi_case):
    run_wlan_timeout_disconnect_airplane_toggle_persistence_case(settings_ui, capsys)
