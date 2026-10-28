"""WiFi 连接 — Func_Components_SystemUI_SignalLevel（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.signal_level import run_signal_level_case

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_001")
@pytest.mark.wifi_case(
    title="WiFi信号格数-满格（>-65dBm）检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为华三AP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_001(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_002")
@pytest.mark.wifi_case(
    title="WiFi信号格数-三格[-75,-65]dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为华三AP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_002(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_003")
@pytest.mark.wifi_case(
    title="WiFi信号格数-两格[-82,-75)dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为华三AP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_003(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_004")
@pytest.mark.wifi_case(
    title="WiFi信号格数-一格[-88,-82)dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为华三AP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_004(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_005")
@pytest.mark.wifi_case(
    title="WiFi信号格数-无（<-88）检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为华三AP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_005(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_006")
@pytest.mark.wifi_case(
    title="HyperWiFi信号格数-满格（>-73dBm）检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_006(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_007")
@pytest.mark.wifi_case(
    title="HyperWiFi信号格数-三格[-86,-73]dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_007(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_008")
@pytest.mark.wifi_case(
    title="HyperWiFi信号格数-两格[-93,-86)dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_008(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_009")
@pytest.mark.wifi_case(
    title="HyperWiFi信号格数-一格[-98,-93)dBm检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_009(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_SystemUI_SignalLevel_UI_010")
@pytest.mark.wifi_case(
    title="HyperWiFi信号格数-无（<-98）检查",
    pre="1、屏蔽箱（漫游测试环境） 2、陪测试设备为miniAP",
)
def test_Func_Components_SystemUI_SignalLevel_UI_010(run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, wifi_case):
    run_signal_level_case(wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator_optional, surface="systemui")
