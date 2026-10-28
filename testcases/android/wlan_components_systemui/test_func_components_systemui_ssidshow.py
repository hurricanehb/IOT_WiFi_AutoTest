"""WiFi 连接 — Func_Components_SystemUI_SsidShow（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import (
    run_systemui_ssid_display_case,
    run_systemui_ssid_order_case,
)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_001")
@pytest.mark.wifi_case(
    title="WiFi-SSID UTF-8编码中文字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_001(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_002")
@pytest.mark.wifi_case(
    title="WiFi-SSID GBK编码中文字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_002(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_003")
@pytest.mark.wifi_case(
    title="WiFi-SSID CP949编码韩文字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_003(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_004")
@pytest.mark.wifi_case(
    title="WiFi-SSID Shift_JIS编码日文字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_004(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_005")
@pytest.mark.wifi_case(
    title="SSID含特殊字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_005(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_006")
@pytest.mark.wifi_case(
    title="SSID含英文字符正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_006(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_007")
@pytest.mark.wifi_case(
    title="SSID含数字正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_007(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_008")
@pytest.mark.wifi_case(
    title="SSID含小表情正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_008(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_009")
@pytest.mark.wifi_case(
    title="SSID32位正常显示",
    pre="1、设备恢复出厂 2、陪测试设备为AP 3、拓扑：AP有线连接上级路由器",
)
def test_Func_Components_SystemUI_SsidShow_UI_009(
    run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_ssid_display_case(
        wifi_case["case_id"], run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_SsidShow_UI_010")
@pytest.mark.wifi_case(
    title="SSID排序检查",
    pre="1、测试环境：办公室",
)
def test_Func_Components_SystemUI_SsidShow_UI_010(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_ssid_order_case(wifi_case["case_id"], run_shell_cmd, settings_ui)
