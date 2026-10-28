"""WiFi 连接 — Func_Components_SystemUI_WifiIcon（自动化实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_wifi_icon_case

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_WifiIcon_UI_001")
@pytest.mark.wifi_case(
    title="WiFi网络标准4/5/6/7图标检查",
    pre="1、设备恢复出厂 2、周围存在WiFi4/5/6/7的路由器",
)
def test_Func_Components_SystemUI_WifiIcon_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case
):
    run_systemui_wifi_icon_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_WifiIcon_UI_002")
@pytest.mark.wifi_case(
    title="HyperWiFi网络标识“HYPER Wi-Fi”检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_WifiIcon_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case
):
    run_systemui_wifi_icon_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_WifiIcon_UI_003")
@pytest.mark.wifi_case(
    title="HyperWiFi网络标准“H”图标检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_WifiIcon_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case
):
    run_systemui_wifi_icon_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )
