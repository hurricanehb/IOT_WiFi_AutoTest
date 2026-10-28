"""WiFi 连接 — Func_WlanAccess_Conn_SsidPwd（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.ap_configuration import run_wifi_ap_ssid_case

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_009")
@pytest.mark.wifi_case(
    title="SSID GBK 1位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_009(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_gbk_chinese_min",
    )

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_010")
@pytest.mark.wifi_case(
    title="SSID GBK 16位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_010(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_gbk_chinese_16",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_001")
@pytest.mark.wifi_case(
    title="(SSID 1位+密码8位) “数字”正常连接",
    pre="1、陪测试设备为锐捷AP720-A/miniAP",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_numeric_min",
    )

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_002")
@pytest.mark.wifi_case(
    title="(SSID +密码)16位 \"组合字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A/miniAP",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_002(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_mixed_chars_16_alt",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_003")
@pytest.mark.wifi_case(
    title="(SSID +密码)32位 “特殊字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A/miniAP",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_003(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_special_chars_escaped",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_004")
@pytest.mark.wifi_case(
    title="(SSID 32位+密码64位) “英文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_ascii_max_password_max",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_005")
@pytest.mark.wifi_case(
    title="SSID  “小表情符号”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_cjk_phrase",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_006")
@pytest.mark.wifi_case(
    title="SSID全空格正常连接",
    pre="1、陪测试设备为锐捷AP720-A/miniAP",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_007")
@pytest.mark.wifi_case(
    title="SSID UTF-8 1位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_007(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_utf8_chinese_min",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_008")
@pytest.mark.wifi_case(
    title="SSID UTF-8 10位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_008(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_utf8_chinese_10",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_011")
@pytest.mark.wifi_case(
    title="SSID  Shift_JIS编码（日文）1个字符正常连接",
    pre="暂无AP设备支持配置",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_011(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_shift_jis_japanese_min",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_012")
@pytest.mark.wifi_case(
    title="SSID  Shift_JIS编码（日文）16个字符正常连接",
    pre="暂无AP设备支持配置",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_012(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_shift_jis_japanese_16",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_013")
@pytest.mark.wifi_case(
    title="SSID  CP949编码（韩文）1个字符正常连接",
    pre="暂无AP设备支持配置",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_013(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_cp949_korean_min",
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_014")
@pytest.mark.wifi_case(
    title="SSID  CP949编码（韩文）16个字符正常连接",
    pre="暂无AP设备支持配置",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_014(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
        entry_id="ssid_cp949_korean",
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_001")
@pytest.mark.wifi_case(
    title="中文SSID字符编码格式变化",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_002")
@pytest.mark.wifi_case(
    title="UTF-8编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置UTF-8编码方式中文SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_003")
@pytest.mark.wifi_case(
    title="GBK编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置GBK编码方式中文SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_004")
@pytest.mark.wifi_case(
    title="Shift_JIS编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置 Shift_JIS编码日文字符SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_005")
@pytest.mark.wifi_case(
    title="CP949编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置CP949编码方式韩文字符SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_006")
@pytest.mark.wifi_case(
    title="网络详情-UTF-8编码SSID“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP，并配置UTF-8编码方式中文SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_007")
@pytest.mark.wifi_case(
    title="网络详情-GBK编码SSID“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP，并配置GBK编码方式中文SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_008")
@pytest.mark.wifi_case(
    title="网络详情- Shift_JIS编码SSID“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP，并配置 Shift_JIS编码日文字符SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Excp_009")
@pytest.mark.wifi_case(
    title="网络详情-CP949编码SSID“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP，并配置CP949编码方式韩文字符SSID",
)
def test_Func_WlanAccess_Conn_SsidPwd_Excp_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

