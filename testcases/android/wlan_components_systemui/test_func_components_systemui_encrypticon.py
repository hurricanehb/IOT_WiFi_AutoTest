"""WiFi 连接 — Func_Components_SystemUI_EncryptIcon（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_encrypt_icon_case

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_EncryptIcon_UI_001")
@pytest.mark.wifi_case(
    title="加密型网络（WPA/WPA2/WPA3/802.1x认证）“锁”图标显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为传统 WiFi AP",
)
def test_Func_Components_SystemUI_EncryptIcon_UI_001(
    run_shell_cmd, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_encrypt_icon_case(
        wifi_case["case_id"], run_shell_cmd, settings_ui, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_EncryptIcon_UI_002")
@pytest.mark.wifi_case(
    title="开放型网络（open/owe、mac、portal认证）“无锁”显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为传统 WiFi AP",
)
def test_Func_Components_SystemUI_EncryptIcon_UI_002(
    run_shell_cmd, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_encrypt_icon_case(
        wifi_case["case_id"], run_shell_cmd, settings_ui, wifi_ap_action_optional
    )
