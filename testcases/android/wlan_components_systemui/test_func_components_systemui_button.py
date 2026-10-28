"""WiFi 连接 — Func_Components_SystemUI_Button（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_button_case

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_Button_UI_001")
@pytest.mark.wifi_case(
    title="“WLAN设置”按键跳转检查",
    pre="无",
)
def test_Func_Components_SystemUI_Button_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_button_case(wifi_case["case_id"], run_shell_cmd, wifi, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_Button_UI_002")
@pytest.mark.wifi_case(
    title="“WLAN开关”/“互联网”开关按键跳转检查",
    pre="1、开关图标可能为WLAN或互联网",
)
def test_Func_Components_SystemUI_Button_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_button_case(wifi_case["case_id"], run_shell_cmd, wifi, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_Button_UI_003")
@pytest.mark.wifi_case(
    title="“查看全部”开关按键跳转检查",
    pre="无",
)
def test_Func_Components_SystemUI_Button_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_button_case(wifi_case["case_id"], run_shell_cmd, wifi, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_Button_UI_004")
@pytest.mark.wifi_case(
    title="“网络详情”图标跳转",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_Button_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_systemui_button_case(wifi_case["case_id"], run_shell_cmd, wifi, settings_ui)
