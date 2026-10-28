"""WiFi 连接 — Func_WlanAccess_Conn_Encrypt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.ap_configuration import (
    run_preconfigured_wifi_security_case,
    run_wifi_ap_security_case,
)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_001")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-40",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_001(
    run_shell_cmd, wifi, wifi_yaml,
wifi_case):
    run_preconfigured_wifi_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        entry_id="wifi_wep40_lab", expected_capabilities=("WEP",),
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_002")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-104",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_002(
    run_shell_cmd, wifi, wifi_yaml,
wifi_case):
    run_preconfigured_wifi_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        entry_id="wifi_wep104_lab", expected_capabilities=("WEP",),
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_003")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-128",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_003(
    run_shell_cmd, wifi, wifi_yaml,
wifi_case):
    run_preconfigured_wifi_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        entry_id="wifi_wep128_lab", expected_capabilities=("WEP",),
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_004")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA-CCMP",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-aes",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_005")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA-TKIP/CCMP",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-aes-tkip",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_006")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_006(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-tkip",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_007")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_007(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-aes-pmf-mandatory",
    )

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_008")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，可选开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_008(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-aes-pmf-optional",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_009")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，关闭pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_009(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-aes",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_010")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_011")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，可选开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_012")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，关闭pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_012(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-aes-tkip",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_013")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，TKIP加密",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_013(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-wpa2-tkip",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_014")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_014(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-wpa2-aes-pmf-mandatory",
    )

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_015")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，可选开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_015(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-wpa2-aes-pmf-optional",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_016")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，关闭pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_016(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-wpa2-aes",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_017")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_018")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，可选开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_019")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，关闭pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_019(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa-wpa2-aes-tkip",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_020")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，可选启用pmf",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置可选pmf",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_020_WPA2_WPA3混合_可选启用pmf(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-wpa3-aes",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_021")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，强制启用pmf（暂无AP支持配置强制开启或关闭pmf）",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置强制启用pmf",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_021_WPA2_WPA3混合_强制启用pmf_(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-wpa3-aes-pmf-mandatory",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_022")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，强制关闭pmf（暂无AP支持配置强制开启或关闭pmf）",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置强制关闭pmf",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_023")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，禁用AE_PK，禁用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置禁用AE_PK，禁用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_023_AP设置无线加密方式为WPA3加密_禁用(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_024")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，禁用SAE_PK，启用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置禁用SAE_PK，启用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_024_AP设置无线加密方式为WPA3加密_禁用(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_025")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，启用SAE_PK，禁用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置启用SAE_PK，禁用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_025_AP设置无线加密方式为WPA3加密_启用(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_026")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，启用SAE_PK，启用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置启用SAE_PK，启用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_026_AP设置无线加密方式为WPA3加密_启用(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_027")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，可选开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网 3、备注：miniAP 采用的是CCMP加密方式",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_028")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，强制开启pmf",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、备注：miniAP 采用的是CCMP加密方式",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_028_AP设置无线加密方式为WPA3个人级_C(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa3-aes",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_029")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，强制关闭pmf",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、备注：miniAP 采用的是CCMP加密方式",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_029(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_030")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，AES256GCM加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_030_AP设置无线加密方式为WPA3个人级_A(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_031")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_031_AP设置无线加密方式为WPA3个人级过渡(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="wpa2-wpa3-aes-pmf-mandatory",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_032")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，关闭pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_032(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_033")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级过渡模式-CCMP",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_033(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_034")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级only模式-CCMP",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_034(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_035")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级-GCMP（无可配ACAP）",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_035(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_036")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级192bit模式-GCMP",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_036(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_037")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级192bit模式-CNSA（政府军用）",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_037(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_038")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级CCMP加密，可选开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_038(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_039")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级CCMP加密，关闭PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_039(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_040")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，强制开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_040(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_041")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，可选开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_041(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_042")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，关闭PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_042(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_043")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP加密",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_043(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_044")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，强制开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_044(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_045")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，可选开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_045(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_046")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，关闭PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_046(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_047")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，强制开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_047(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_048")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，可选开启PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_048(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_049")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，关闭PMF",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_049(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_050")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP加密",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_050(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_051")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA企业级TKIP加密",
    pre="1. DUT为出厂状态 2. 已配置好企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_051(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_052")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为Open",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：可联网，双频合一/频宽信道auto/密码无/加密方式不加密",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_052(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="open", password="",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_053")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为OWE",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：H3C WX2520X-LI 可联网，OWE网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_053(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        security="enhanced-open", password="",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_054")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为OWE过渡模式",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，OWE过渡模式网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_054(
    run_shell_cmd, wifi, wifi_yaml,
wifi_case):
    run_preconfigured_wifi_security_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="wifi_owe_transition",
        expected_capabilities=("OWE",),
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_055")
@pytest.mark.wifi_case(
    title="AP设置开放型Portal网络",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：商米W1s，可联网，Portal网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_055(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_056")
@pytest.mark.wifi_case(
    title="AP设置密码认证型Portal网络",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：商米W1s，可联网，Portal网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_056(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_057")
@pytest.mark.wifi_case(
    title="AP设置短信认证型Portal网络",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：商米W1s，可联网，Portal网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_057(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_058")
@pytest.mark.wifi_case(
    title="AP设置mac接入网络",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S，可联网，MAC认证网络已配置好",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_058(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_059")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WAPI-PSK",
    pre="1. DUT为出厂状态 2. 传统 WiFi AP已配置好WAPI-PSK WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_059(
    run_shell_cmd, wifi, wifi_yaml,
wifi_case):
    # cmd wifi connect-network 不支持 WAPI，需 UI 与厂商适配后手工验证。
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_060")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WAPI证书认证--终端未适配，缺测试环境",
    pre="1. DUT为出厂状态 2. 传统 WiFi AP已配置好WAPI证书认证网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_060(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_061")
@pytest.mark.wifi_case(
    title="AC+AP场景启用FT属性",
    pre="1. DUT为出厂状态 2. 传统 WiFi AP已配置好漫游环境，并启用FT属性，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_061(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

