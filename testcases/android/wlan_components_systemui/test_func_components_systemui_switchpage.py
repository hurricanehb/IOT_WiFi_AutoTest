"""WiFi 连接 — Func_Components_SystemUI_SwitchPage（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_switch_page_case

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_SwitchPage_UI_001")
@pytest.mark.wifi_case(
    title="systemUI WLAN页面切换--WLAN、有线网络、移动数据",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_SwitchPage_UI_001(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_switch_page_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_SwitchPage_UI_002")
@pytest.mark.wifi_case(
    title="反复操作点开systemWlan列表 20次",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_SwitchPage_UI_002(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_switch_page_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_SwitchPage_UI_003")
@pytest.mark.wifi_case(
    title="点开systemWLAN列表后，锁屏后亮屏",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_SwitchPage_UI_003(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_switch_page_case(wifi_case["case_id"], run_shell_cmd, settings_ui)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_SystemUI_SwitchPage_UI_004")
@pytest.mark.wifi_case(
    title="systemUI WLAN页面放置自刷新-5min",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_SwitchPage_UI_004(run_shell_cmd, settings_ui, wifi_case):
    run_systemui_switch_page_case(wifi_case["case_id"], run_shell_cmd, settings_ui)
