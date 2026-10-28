"""WiFi 连接 — Func_Components_Settings_ScanList（自动化/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.scan_list import (
    run_settings_scan_list_case,
    run_settings_scan_list_toggle_stability_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_001")
@pytest.mark.wifi_case(
    title="默认信息展示",
    pre="1、测试环境：办公室",
)
def test_Func_Components_Settings_ScanList_Vali_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_002")
@pytest.mark.wifi_case(
    title="列表每10s刷新（周期10s扫描）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_003")
@pytest.mark.wifi_case(
    title="新增AP-SSID条目更新检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_004")
@pytest.mark.wifi_case(
    title="减少AP-SSID条目更新检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_005")
@pytest.mark.wifi_case(
    title="切换ssid连接-wlan列表更新检查（5s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_006")
@pytest.mark.wifi_case(
    title="手动断开无线连接后-wlan列表更新检查（5s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_007")
@pytest.mark.wifi_case(
    title="AP下电无线连接断开-wlan列表更新检查（20s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_Settings_ScanList_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_008")
@pytest.mark.wifi_case(
    title="点击加密的SSID",
    pre="1、测试环境：办公室 2、陪测AP，wpa/wpa2混合加密",
)
def test_Func_Components_Settings_ScanList_Vali_008(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_009")
@pytest.mark.wifi_case(
    title="点击不加密的SSID",
    pre="1、测试环境：办公室 2、陪测AP，不加密",
)
def test_Func_Components_Settings_ScanList_Vali_009(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_010")
@pytest.mark.wifi_case(
    title="已连接无线，切换SSID连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2",
)
def test_Func_Components_Settings_ScanList_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_011")
@pytest.mark.wifi_case(
    title="不同网络类型多AP相同SSID扫描显示",
    pre="1、测试环境：办公室 2、陪测AP，miniAP",
)
def test_Func_Components_Settings_ScanList_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_012")
@pytest.mark.wifi_case(
    title="同类型多AP相同加密方式SSID扫描显示",
    pre="1、测试环境：办公室 2、陪测AP，miniAP",
)
def test_Func_Components_Settings_ScanList_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_013")
@pytest.mark.wifi_case(
    title="同类型多AP不同加密方式SSID扫描显示",
    pre="1、测试环境：办公室 2、陪测AP，miniAP",
)
def test_Func_Components_Settings_ScanList_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_014")
@pytest.mark.wifi_case(
    title="SSID排序检查",
    pre="1、测试环境：办公室",
)
def test_Func_Components_Settings_ScanList_Vali_014(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Vali_015")
@pytest.mark.wifi_case(
    title="手动WLAN刷新扫描有效性（o控件）",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态",
)
def test_Func_Components_Settings_ScanList_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Excp_001")
@pytest.mark.wifi_case(
    title="同名SSID场景",
    pre="/",
)
def test_Func_Components_Settings_ScanList_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Int_001")
@pytest.mark.wifi_case(
    title="HOME页面->setting WLAN，查看列表刷新耗时",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Int_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Int_002")
@pytest.mark.wifi_case(
    title="settings WLAN页面，锁屏->亮屏",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Int_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Int_003")
@pytest.mark.wifi_case(
    title="后台进程切换，切换到settingWLAN界面",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Int_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_settings_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ScanList_Int_004")
@pytest.mark.wifi_case(
    title="杀死setting进程后，打开setting ，切换到WLAN界面",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Int_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional, wifi_case):
    run_settings_scan_list_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.stress
@pytest.mark.case_id("Func_Components_Settings_ScanList_Stb_001")
@pytest.mark.wifi_case(
    title="反复操作WLAN开关 20次，查看列表刷新耗时",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Stb_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_settings_scan_list_toggle_stability_case(
        wifi_case["case_id"], run_shell_cmd, wifi, settings_ui
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.stress
@pytest.mark.case_id("Func_Components_Settings_ScanList_Stb_002")
@pytest.mark.wifi_case(
    title="反复操作重置互联网界面  20次，查看列表刷新耗时",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Settings_ScanList_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
