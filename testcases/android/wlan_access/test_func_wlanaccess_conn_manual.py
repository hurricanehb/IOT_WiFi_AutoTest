"""WiFi 连接 — Func_WlanAccess_Conn_Manual（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.ap_configuration import (
    run_hidden_network_reboot_stress_case,
    run_wifi_ap_manual_add_security_case,
)
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    run_add_network_connection_case,
    run_add_network_field_case,
    run_add_network_switch_case,
    run_manual_network_connect_case,
)
from core.libs.android.wifi_scenarios.ip_configuration import (
    run_dhcp_acquisition_case,
    run_mac_privacy_case,
    run_static_configuration_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_001")
@pytest.mark.wifi_case(
    title="手动添加网络配置：(SSID 1位+密码8位) “英文字符”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_ascii_min_password_min"
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_002")
@pytest.mark.wifi_case(
    title="手动添加网络配置：(SSID +密码)16位 “组合字符”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_mixed_chars_16"
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_003")
@pytest.mark.wifi_case(
    title="手动添加网络配置：(SSID +密码)32位 “特殊字符”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_special_chars_32"
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_004")
@pytest.mark.wifi_case(
    title="手动添加网络配置：(32位SSID +64位密码) “数字字符”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_numeric_32_password_64"
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_005")
@pytest.mark.wifi_case(
    title="手动添加网络配置：SSID  “小表情符号”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_symbol_mixed_32_password_64"
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_006")
@pytest.mark.wifi_case(
    title="手动添加网络配置：(SSID+密码)首中尾包含空格",
    pre="1、DUT出厂状态 2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2",
)
def test_Func_WlanAccess_Conn_Manual_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_space_padded"
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_007")
@pytest.mark.wifi_case(
    title="手动添加网络配置：AP SSID UTF-8编码10个“中文字符”",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_Manual_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, entry_id="ssid_utf8_chinese_10"
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_008")
@pytest.mark.wifi_case(
    title="手动添加网络配置：AP SSID GBK编码16个“中文字符”",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_Manual_Vali_008_手动添加网络配置_AP_SSID_GBK(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="ssid_gbk_chinese_16",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_009")
@pytest.mark.wifi_case(
    title="手动添加网络配置：AP SSID  Shift_JIS编码16个日文字符",
    pre="1、AP配置ssid为Shift_JIS编码的16个日文字符",
)
def test_Func_WlanAccess_Conn_Manual_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="ssid_shift_jis_japanese_16",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_010")
@pytest.mark.wifi_case(
    title="手动添加网络配置：AP SSID CP949编码韩文字符",
    pre="1、AP配置ssid为CP949编码韩文字符",
)
def test_Func_WlanAccess_Conn_Manual_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="ssid_cp949_korean",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_011")
@pytest.mark.wifi_case(
    title="添加不存在的SSID",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_011(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_connection_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_add_network_ui,
        entry_id="ssid_nonexistent",
        expect_connected=False,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_012")
@pytest.mark.wifi_case(
    title="未连接状态，手动添加网络",
    pre="1、dut处于未连接状态",
)
def test_Func_WlanAccess_Conn_Manual_Vali_012(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_connection_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_013")
@pytest.mark.wifi_case(
    title="已连接状态，手动添加网络",
    pre="1、环境中存在同类型网络ap1、ap2或miniAP1、miniAP2 2、DUT已连接ap1",
)
def test_Func_WlanAccess_Conn_Manual_Vali_013(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_switch_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_014")
@pytest.mark.wifi_case(
    title="安全性选择“无”",
    pre="1、华三设置无线加密方式为Open",
)
def test_Func_WlanAccess_Conn_Manual_Vali_014(
    run_shell_cmd,
    wifi,
    wifi_yaml,
    wifi_add_network_ui,
    wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_add_network_ui,
        wifi_ap_action_optional,
        security="open",
        ui_security="open",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_015")
@pytest.mark.wifi_case(
    title="安全性选择“WEP”",
    pre="1、华三设置无线加密为WEP方式：12345",
)
def test_Func_WlanAccess_Conn_Manual_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_016")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2/WPA3-Enterprise”",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_017")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-TKIP",
    pre="1、华三设置无线加密为WPA-TKIP方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_017(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa-tkip", ui_security="personal",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_018")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-AES",
    pre="1、华三设置无线加密为WPA-AES方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_018(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa-aes", ui_security="personal",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_019")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-TKIP/AES",
    pre="1、华三设置无线加密为WPA-TKIP/AES方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_019(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa-aes-tkip", ui_security="personal",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_020")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-TKIP",
    pre="1、华三设置无线加密为WPA2-TKIP方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_020(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa2-tkip", ui_security="personal",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_021")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-AES",
    pre="1、华三设置无线加密为WPA2-AES方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_021(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa2-aes", ui_security="personal",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_022")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-TKIP/AES",
    pre="1、华三设置无线加密为WPA2-TKIP/AES方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_022(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa2-aes-tkip", ui_security="personal",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_023")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA/WPA2-混合",
    pre="1、华三设置无线加密为WPA/WPA2-混合方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_023(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa-wpa2-aes", ui_security="personal",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_024")
@pytest.mark.wifi_case(
    title="安全性选择“WPA3-Personal”，AP设置无线加密方式为WPA3-Personal",
    pre="1、华三设置无线加密为WPA3-Personal方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_024(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa3-aes", ui_security="wpa3",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_025")
@pytest.mark.wifi_case(
    title="安全性选择“WPA3-Personal”，AP设置无线加密方式为WPA3-SAE",
    pre="1、华三设置无线加密为WPA3-SAE方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_025(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa3-aes", ui_security="wpa3",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_026")
@pytest.mark.wifi_case(
    title="安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2/WPA3-混合",
    pre="1、华三设置无线加密为WPA2/WPA3-混合方式：24681357",
)
def test_Func_WlanAccess_Conn_Manual_Vali_026(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    for ui_security in ("personal", "wpa3"):
        run_wifi_ap_manual_add_security_case(
            wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
            wifi_ap_action_optional, security="wpa2-wpa3-aes",
            ui_security=ui_security,
        )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_027")
@pytest.mark.wifi_case(
    title="安全性选择“Enhanced Open”，手机热点设置无线加密方式为“开放”",
    pre="1、手机热点安全设置为“Enhanced Open”",
)
def test_Func_WlanAccess_Conn_Manual_Vali_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_028")
@pytest.mark.wifi_case(
    title="高级选项-隐藏的网络，选择是",
    pre="1. 锐捷R730-L AP配置隐藏 SSID，编码方式gbk,，不加密； 2、DUT wifi处于未连接状态 3、A9以前才有，A11后选项入口被删除",
)
def test_Func_WlanAccess_Conn_Manual_Vali_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_029")
@pytest.mark.wifi_case(
    title="高级选项-隐藏的网络，选择是，GBK Encoding选择是",
    pre="1. 锐捷R730-L AP配置隐藏 SSID，编码方式gbk,，不加密； 2、DUT wifi处于未连接状态 3、A9以前才有，A11后选项入口被删除",
)
def test_Func_WlanAccess_Conn_Manual_Vali_029(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_030")
@pytest.mark.wifi_case(
    title="高级选项-隐藏的网络，选择是，GBK Encoding选择否",
    pre="1. 锐捷R730-L AP配置隐藏 SSID，编码方式utf-8,，不加密； 2、DUT wifi处于未连接状态 3、A9以前才有，A11后选项入口被删除",
)
def test_Func_WlanAccess_Conn_Manual_Vali_030(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_031")
@pytest.mark.wifi_case(
    title="高级选项-隐藏的网络，选择否",
    pre="1. AP配置隐藏 SSID，不加密； 2、DUT wifi处于未连接状态",
)
def test_Func_WlanAccess_Conn_Manual_Vali_031(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_add_network_ui,
        wifi_ap_action_optional,
        security="open",
        ui_security="open",
        hidden=True,
        ui_hidden=False,
        expect_connected=False,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_032")
@pytest.mark.wifi_case(
    title="ip设置-DHCP获取IP有效性",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置不加密网络；",
)
def test_Func_WlanAccess_Conn_Manual_Vali_032(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    info = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    print(f"[{wifi_case['case_id']}] DHCP 网络信息：{info}")

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_033")
@pytest.mark.wifi_case(
    title="ip设置-静态ip设置有效性",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP配置不加密网络；",
)
def test_Func_WlanAccess_Conn_Manual_Vali_033(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    info = run_static_configuration_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )
    print(f"[{wifi_case['case_id']}] 静态网络信息：{info}")

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_034")
@pytest.mark.wifi_case(
    title="ip设置-默认本机MAC有效性",
    pre="DUT为出厂状态",
)
def test_Func_WlanAccess_Conn_Manual_Vali_034(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    run_mac_privacy_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui, mode="device"
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_035")
@pytest.mark.wifi_case(
    title="ip设置-随机MAC有效性",
    pre="DUT为出厂状态",
)
def test_Func_WlanAccess_Conn_Manual_Vali_035(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    run_mac_privacy_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui, mode="randomized"
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Excp_001")
@pytest.mark.wifi_case(
    title="手动添加网络配置：SSID密码含单引号",
    pre="1、AP的SSID为：'1234'5678'，密码：'1234'5678'",
)
def test_Func_WlanAccess_Conn_Manual_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="ssid_mixed_chars_16",
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Excp_002")
@pytest.mark.wifi_case(
    title="手动添加网络配置：SSID密码含双引号",
    pre="1、AP的SSID为：\"1234\"5678\"，密码：\"1234\"5678\"",
)
def test_Func_WlanAccess_Conn_Manual_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    run_manual_network_connect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id="ssid_special_chars_escaped",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Excp_003")
@pytest.mark.wifi_case(
    title="手动添加网络配置：安全性选择与AP配置不匹配",
    pre="1、AP无线配置WPA3-Personal加密",
)
def test_Func_WlanAccess_Conn_Manual_Excp_003(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_ap_manual_add_security_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
        wifi_ap_action_optional, security="wpa3-aes", ui_security="personal",
        expect_connected=False,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_001")
@pytest.mark.wifi_case(
    title="SSID长度>32位报错",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_field_case(
        wifi_add_network_ui,
        ssid="a" * 33,
        expect_save_enabled=False,
        expect_save_rejected=True,
        wifi=wifi,
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_002")
@pytest.mark.wifi_case(
    title="SSID （UTF-8 编码）超长中文字符输入报错（不可选编码，未知最大长度限制）",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_003")
@pytest.mark.wifi_case(
    title="SSID （GBK 编码）超长中文字符输入报错（不可选，未知最大长度限制）",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_004")
@pytest.mark.wifi_case(
    title="SSID  （Shift_JIS编码）超长日文字符输入报错（不可选，未知最大长度限制）",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_005")
@pytest.mark.wifi_case(
    title="SSID （CP949编码）超长韩文字符输入报错（不可选，未知最大长度限制）",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_006")
@pytest.mark.wifi_case(
    title="密码输入为空，“连接按键”置灰",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_006(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_field_case(
        wifi_add_network_ui,
        ssid="PyAutoTest_Empty_Password",
        password="",
        expect_save_enabled=False,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_007")
@pytest.mark.wifi_case(
    title="密码长度<8位报错",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_007(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_field_case(
        wifi_add_network_ui,
        ssid="PyAutoTest_Short_Password",
        password="1234567",
        expect_save_enabled=False,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_008")
@pytest.mark.wifi_case(
    title="密码长度>32位报错",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_009")
@pytest.mark.wifi_case(
    title="密码长度>64位报错",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_009(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_field_case(
        wifi_add_network_ui,
        ssid="PyAutoTest_Long_Password",
        password="a" * 65,
        expect_save_enabled=False,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_UI_010")
@pytest.mark.wifi_case(
    title="密码输入中文字符",
    pre="无",
)
def test_Func_WlanAccess_Conn_Manual_UI_010(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui,
wifi_case):

    run_add_network_field_case(
        wifi_add_network_ui,
        ssid="PyAutoTest_Chinese_Password",
        password="中文密码字符",
        expect_save_enabled=False,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Stb_001")
@pytest.mark.wifi_case(
    title="隐藏网络STA重启重连",
    pre="1、AP配置隐藏网络 2、dut已保存网络列表只有目标隐藏网络",
)
def test_Func_WlanAccess_Conn_Manual_Stb_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_add_network_ui, wifi_ap_action_optional,
wifi_case):

    run_hidden_network_reboot_stress_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_add_network_ui,
        wifi_ap_action_optional,
    )

