"""WiFi 连接 — Func_Components_SystemUI_WlanSwitch（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.wlan_switch import (
    run_wlan_switch_off_case,
    run_wlan_switch_on_case,
)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_WlanSwitch_Vali_001")
@pytest.mark.wifi_case(
    title="wlan开启检查",
    pre="1、开关图标可能为WLAN或互联网",
)
def test_Func_Components_SystemUI_WlanSwitch_Vali_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_wlan_switch_on_case(wifi_case["case_id"], run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_WlanSwitch_Vali_002")
@pytest.mark.wifi_case(
    title="wlan关闭检查",
    pre="1、开关图标可能为WLAN或互联网",
)
def test_Func_Components_SystemUI_WlanSwitch_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_wlan_switch_off_case(wifi_case["case_id"], run_shell_cmd, wifi)
