"""WiFi 连接 — Func_Components_SystemUI_ScanList（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import (
    run_systemui_scan_list_case,
    run_systemui_scan_list_default_case,
)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_001")
@pytest.mark.wifi_case(
    title="默认信息展示",
    pre="1、测试环境：办公室",
)
def test_Func_Components_SystemUI_ScanList_UI_001(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_scan_list_default_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_002")
@pytest.mark.wifi_case(
    title="列表每10s刷新（周期10s扫描）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_003")
@pytest.mark.wifi_case(
    title="新增AP-SSID条目更新检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_004")
@pytest.mark.wifi_case(
    title="减少AP-SSID条目更新检查",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_005")
@pytest.mark.wifi_case(
    title="切换ssid连接wlan列表更新检查（5s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_006")
@pytest.mark.wifi_case(
    title="手动断开无线连接后-wlan列表更新检查（5s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_007")
@pytest.mark.wifi_case(
    title="关闭AP无线后-WiFi断开-wlan列表更新检查（10s内更新）",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_Components_SystemUI_ScanList_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_008")
@pytest.mark.wifi_case(
    title="点击加密的SSID",
    pre="1、测试环境：办公室 2、陪测AP，wpa/wpa2混合加密",
)
def test_Func_Components_SystemUI_ScanList_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_009")
@pytest.mark.wifi_case(
    title="点击不加密的SSID",
    pre="1、测试环境：办公室 2、陪测AP，不加密",
)
def test_Func_Components_SystemUI_ScanList_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_010")
@pytest.mark.wifi_case(
    title="已连接无线，切换SSID连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2",
)
def test_Func_Components_SystemUI_ScanList_UI_010(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_011")
@pytest.mark.wifi_case(
    title="多AP同一个SSID扫描唯一性",
    pre="1、测试环境：办公室 2、陪测AP：支持SSID格式修改",
)
def test_Func_Components_SystemUI_ScanList_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_UI_012")
@pytest.mark.wifi_case(
    title="SSID排序检查",
    pre="1、测试环境：办公室",
)
def test_Func_Components_SystemUI_ScanList_UI_012(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Excp_001")
@pytest.mark.wifi_case(
    title="UTF-8编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置UTF-8编码方式中文SSID",
)
def test_Func_Components_SystemUI_ScanList_Excp_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Excp_002")
@pytest.mark.wifi_case(
    title="GBK编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置GBK编码方式中文SSID",
)
def test_Func_Components_SystemUI_ScanList_Excp_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Excp_003")
@pytest.mark.wifi_case(
    title="Shift_JIS编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置 Shift_JIS编码日文字符SSID",
)
def test_Func_Components_SystemUI_ScanList_Excp_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Excp_004")
@pytest.mark.wifi_case(
    title="CP949编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置CP949编码方式韩文字符SSID",
)
def test_Func_Components_SystemUI_ScanList_Excp_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_001")
@pytest.mark.wifi_case(
    title="金融安全属性",
    pre="周围存在弱加密网络（open、owe、mac、portal认证等）",
)
def test_Func_Components_SystemUI_ScanList_Int_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_002")
@pytest.mark.wifi_case(
    title="settings依次接入WiFi、HyperWiFi，systemUI-wlan列表条目检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_Int_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_003")
@pytest.mark.wifi_case(
    title="双WiFi-setting切换WiFi网络，systemUI-wlan列表条目检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_Int_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_004")
@pytest.mark.wifi_case(
    title="双WiFi-setting切换HyperWiFi网络，systemUI-wlan列表条目检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_Int_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_005")
@pytest.mark.wifi_case(
    title="双WiFi-setting断开WiFi网络，systemUI-wlan列表条目检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_Int_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Int_006")
@pytest.mark.wifi_case(
    title="双WiFi-setting断开HyperWiFi网络，systemUI-wlan列表条目检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ScanList_Int_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_scan_list_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )
