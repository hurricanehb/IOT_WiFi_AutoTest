"""WiFi 连接 — Func_Components_Settings_PriBakIcon（衰减器自动化场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.primary_backup_icon import (
    run_primary_backup_icon_case,
)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_Settings_PriBakIcon_UI_001")
@pytest.mark.wifi_case(
    title="首次连接WiFi为主网络-HyperWiFi为备用网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_Settings_PriBakIcon_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_primary_backup_icon_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_Settings_PriBakIcon_UI_002")
@pytest.mark.wifi_case(
    title="首次连接HyperWiFi为主网络-WiFi为备用网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-80dBm）、miniAP（-50dBm）",
)
def test_Func_Components_Settings_PriBakIcon_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_primary_backup_icon_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_Settings_PriBakIcon_UI_003")
@pytest.mark.wifi_case(
    title="主备网络发生切换",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_Settings_PriBakIcon_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_primary_backup_icon_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_Settings_PriBakIcon_UI_004")
@pytest.mark.wifi_case(
    title="断开主网络，备用网络切换为主网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_Settings_PriBakIcon_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_primary_backup_icon_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional)
