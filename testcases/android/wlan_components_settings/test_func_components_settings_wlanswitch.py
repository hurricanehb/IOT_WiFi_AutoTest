"""WiFi 连接 — Func_Components_Settings_WlanSwitch（自动化/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.settings.wlan_switch import (
    run_airplane_wlan_switch_case,
    run_cross_component_wlan_switch_case,
    run_hotspot_wlan_switch_case,
    run_wlan_list_scroll_stability_case,
    run_wlan_switch_off_case,
    run_wlan_switch_on_case,
    run_wlan_toggle_stability_case,
    run_wrong_password_reconnect_stability_case,
)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Vali_001")
@pytest.mark.wifi_case(
    title="无线开关开启",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WlanSwitch_Vali_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_case):
    run_wlan_switch_on_case(wifi_case['case_id'], run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Vali_002")
@pytest.mark.wifi_case(
    title="无线开关关闭",
    pre="1、DUT恢复出厂状态 2、PC安装adb环境",
)
def test_Func_Components_Settings_WlanSwitch_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_wlan_switch_off_case(wifi_case['case_id'], run_shell_cmd, wifi)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Int_001")
@pytest.mark.wifi_case(
    title="热点与WLAN开关",
    pre="无",
)
def test_Func_Components_Settings_WlanSwitch_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_hotspot_wlan_switch_case(wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Int_002")
@pytest.mark.wifi_case(
    title="飞行模式与WLAN开关",
    pre="无",
)
def test_Func_Components_Settings_WlanSwitch_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_airplane_wlan_switch_case(wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Int_003")
@pytest.mark.wifi_case(
    title="跨组件状态一致性",
    pre="无",
)
def test_Func_Components_Settings_WlanSwitch_Int_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_cross_component_wlan_switch_case(
        wifi_case['case_id'], run_shell_cmd, wifi, settings_ui
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.stress
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Stb_001")
@pytest.mark.wifi_case(
    title="快速关闭/开启wlan开关（20次）-不闪退",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Settings_WlanSwitch_Stb_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_wlan_toggle_stability_case(
        wifi_case['case_id'], run_shell_cmd, wifi, settings_ui, cycles=20
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.stress
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Stb_002")
@pytest.mark.wifi_case(
    title="快速上下滑动wlan列表（20次）-不闪退",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Settings_WlanSwitch_Stb_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_wlan_list_scroll_stability_case(
        wifi_case['case_id'], run_shell_cmd, settings_ui, cycles=20
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.stress
@pytest.mark.case_id("Func_Components_Settings_WlanSwitch_Stb_003")
@pytest.mark.wifi_case(
    title="错误密码断开后多次操作再连接（20次）-不闪退",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_Settings_WlanSwitch_Stb_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_wrong_password_reconnect_stability_case(
        wifi_case['case_id'],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        settings_ui,
        wifi_ap_action_optional,
        cycles=20,
    )
