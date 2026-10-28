"""WiFi 连接 — Func_Components_Settings_WifiSec（SP 半自动交互场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.wifi_security import (
    run_sp_wifi_security_case,
)

pytestmark = pytest.mark.no_wifi_lifecycle

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_001")
@pytest.mark.wifi_case(
    title="WiFi安全开关",
    pre="1、dut出厂状态",
)
def test_Func_Components_Settings_WifiSec_Vali_001(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_002")
@pytest.mark.wifi_case(
    title="禁止显示/连接加密方式为WEP网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_002(
    run_shell_cmd, wifi, settings_ui,
wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_003")
@pytest.mark.wifi_case(
    title="禁止显示/连接加密方式为Open",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_003(
    run_shell_cmd, wifi, settings_ui,
wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_004")
@pytest.mark.wifi_case(
    title="禁止显示/连接开放型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_004(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_005")
@pytest.mark.wifi_case(
    title="禁止显示/连接密码认证型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_005(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_006")
@pytest.mark.wifi_case(
    title="禁止显示/连接短信认证型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_006(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_007")
@pytest.mark.wifi_case(
    title="禁止显示/连接mac接入网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_007(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_008")
@pytest.mark.wifi_case(
    title="禁止显示/连接MAC优先Portal认证型网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_008(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_009")
@pytest.mark.wifi_case(
    title="手动添加网络安全性无“WEP”选项",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_009(
    run_shell_cmd, wifi, settings_ui,
wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_010")
@pytest.mark.wifi_case(
    title="手动添加网络安全性无“Open”选项",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_010(
    run_shell_cmd, wifi, settings_ui,
wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_011")
@pytest.mark.wifi_case(
    title="禁止扫码/添加加密方式为WEP的无线",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_011(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_012")
@pytest.mark.wifi_case(
    title="禁止扫码/添加加密方式为Open的无线",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_012(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_013")
@pytest.mark.wifi_case(
    title="禁止扫码/添加AP设置开放型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_013(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_014")
@pytest.mark.wifi_case(
    title="禁止扫码/添加AP设置密码认证型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_014(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_015")
@pytest.mark.wifi_case(
    title="禁止扫码/添加AP设置短信认证型Portal网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_015(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_016")
@pytest.mark.wifi_case(
    title="禁止扫码/添加AP设置mac接入网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_016(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiSec_Vali_017")
@pytest.mark.wifi_case(
    title="禁止扫码/添加MAC优先Portal认证型网络",
    pre="1、dut启用WiFi安全",
)
def test_Func_Components_Settings_WifiSec_Vali_017(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_WifiSec_UI_001")
@pytest.mark.wifi_case(
    title="SystemUI无线列表显示一致性",
    pre="无",
)
def test_Func_Components_Settings_WifiSec_UI_001(run_shell_cmd, wifi, settings_ui, wifi_case):
    run_sp_wifi_security_case(wifi_case, run_shell_cmd, wifi, settings_ui)
