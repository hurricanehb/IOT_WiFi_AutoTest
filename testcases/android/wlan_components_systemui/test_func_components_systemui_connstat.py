"""WiFi 连接 — Func_Components_SystemUI_ConnStat（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui import run_systemui_conn_status_case
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_001")
@pytest.mark.wifi_case(
    title="“已连接-互联网正常”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_002")
@pytest.mark.wifi_case(
    title="“已连接-互联网异常”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_003")
@pytest.mark.wifi_case(
    title="已连接-互联网正常与异常互切，网络状态显示更新检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_004")
@pytest.mark.wifi_case(
    title="“密码错误”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_005")
@pytest.mark.wifi_case(
    title="“获取ip失败”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_006")
@pytest.mark.wifi_case(
    title="“已连接（互联网正常）再断开”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui,
        wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_007")
@pytest.mark.wifi_case(
    title="“已连接（互联网异常）再断开”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_008")
@pytest.mark.wifi_case(
    title="“Portal认证接入”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_SystemUI_ConnStat_UI_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_UI_009")
@pytest.mark.wifi_case(
    title="“未联网重定向跳转”网络状态显示检查",
    pre="1、设备恢复出厂 2、陪测试设备为小米路由器AX3000",
)
def test_Func_Components_SystemUI_ConnStat_UI_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_001")
@pytest.mark.wifi_case(
    title="settings接入双WiFi(互联网异常)，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_002")
@pytest.mark.wifi_case(
    title="settings接入双WiFi(互联网正常)，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_003")
@pytest.mark.wifi_case(
    title="settings接入双WiFi-断开WiFi，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_004")
@pytest.mark.wifi_case(
    title="settings接入双WiFi-取消保存WiFi，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_005")
@pytest.mark.wifi_case(
    title="settings接入双WiFi-断开HyperWiFi，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_ConnStat_Int_006")
@pytest.mark.wifi_case(
    title="settings接入双WiFi-取消保存HyperWiFi，systemUI-wlan列表状态一致性检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP1、miniAP",
)
def test_Func_Components_SystemUI_ConnStat_Int_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui,
wifi_case):
    run_systemui_conn_status_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, settings_ui
    )
