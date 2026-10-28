"""WiFi 连接 — Func_WlanAccess_Conn_Scanner（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest
from core.libs.android.wifi_scenarios.qr_scanner import run_wifi_scanner_case

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_001")
@pytest.mark.wifi_case(
    title="+添加网络入口扫码连接测试",
    pre="1、DUT出厂状态 2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="scanner_default",
        entry_point="add_network_entry",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_002")
@pytest.mark.wifi_case(
    title="添加网络设置-扫码连接测试",
    pre="1、DUT出厂状态 2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="scanner_default",
        entry_point="ssid_editor",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_003")
@pytest.mark.wifi_case(
    title="扫码添加全特殊字符网络",
    pre="1、AP配置ssid为~!@#$%^&*()_+-={}|[]\\:\";'<>?,./，密码为~!@#$%^&*()_+-={}|[]\\:\";'<>?,./",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_special_chars_32",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_004")
@pytest.mark.wifi_case(
    title="扫码添加空格字符网络",
    pre="1、AP配置ssid为空格，密码为8个空格",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_spaces_only",
        reboot_check=True,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_005")
@pytest.mark.wifi_case(
    title="扫码添加组合字符网络",
    pre="1、AP配置SSID和密码包含中英文、空格及引号",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_mixed_chars_16",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_006")
@pytest.mark.wifi_case(
    title="扫码添加AP SSID UTF-8编码10个中文字符网络",
    pre="1、AP配置SSID为UTF-8编码格式的10个中文字符，密码为24681357",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_utf8_chinese_10",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_007")
@pytest.mark.wifi_case(
    title="扫码添加AP SSID GBK编码16个中文字符网络",
    pre="1、AP配置SSID为GBK编码格式的16个中文字符，密码为24681357",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_007_扫码添加AP_SSID_GBK编码16个(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_gbk_chinese_16",
        ap_encoding="gbk",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_008")
@pytest.mark.wifi_case(
    title="扫码添加AP SSID  Shift_JIS编码16个日文字符网络",
    pre="1、AP配置ssid为Shift_JIS编码的16个日文字符",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_shift_jis_japanese_16",
        ap_encoding="shift_jis",
        reboot_check=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_009")
@pytest.mark.wifi_case(
    title="扫码添加AP SSID CP949编码韩文字符网络",
    pre="1、AP配置ssid为CP949编码韩文字符",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
wifi_case):

    run_wifi_scanner_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action_optional,
        entry_id="ssid_cp949_korean",
        ap_encoding="cp949",
        reboot_check=True,
    )

