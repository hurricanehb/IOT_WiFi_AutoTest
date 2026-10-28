"""WiFi 连接 — Func_WlanAccess_Reconnect_ApChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.ap_configuration import (
    run_wifi_ap_channel_change_case,
    run_wifi_ap_password_change_case,
    run_wifi_ap_security_change_case,
    run_wifi_ap_ssid_change_case,
)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_001")
@pytest.mark.wifi_case(
    title="AP系统重启",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20； 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_002")
@pytest.mark.wifi_case(
    title="AP修改DHCP服务器配置",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_003")
@pytest.mark.wifi_case(
    title="AP修改无线SSID",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_003(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_ssid_change_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_004")
@pytest.mark.wifi_case(
    title="AP修改无线密码",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_password_change_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_005")
@pytest.mark.wifi_case(
    title="AP修改加密方式-WPA/WPA2/WPA3",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_change_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_ap_action_optional,
        initial_security="wpa2-aes",
        transitions=[
            ("wpa2-wpa3-aes", True),
            ("wpa3-aes", True),
        ],
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_006")
@pytest.mark.wifi_case(
    title="AP修改加密方式-open和加密互切",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_006(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_change_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_ap_action_optional,
        initial_security="wpa2-aes",
        transitions=[
            ("open", False),
            ("wpa-wpa2-aes", True),
        ],
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_007")
@pytest.mark.wifi_case(
    title="AP修改无线频宽/信道",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_007(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_channel_change_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_008")
@pytest.mark.wifi_case(
    title="AP修改无线模式",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Vali_009")
@pytest.mark.wifi_case(
    title="STA亮灭屏wifi重连",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Excp_001")
@pytest.mark.wifi_case(
    title="DHCP失败恢复",
    pre="无",
)
def test_Func_WlanAccess_Reconnect_ApChange_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Excp_002")
@pytest.mark.wifi_case(
    title="认证失败恢复",
    pre="无",
)
def test_Func_WlanAccess_Reconnect_ApChange_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Excp_003")
@pytest.mark.wifi_case(
    title="AP修改加密方式-WPA2和WPA3互切（含pmf配置）",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Excp_003(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_change_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_ap_action_optional,
        initial_security="wpa2-aes-pmf-mandatory",
        transitions=[("wpa3-aes", True)],
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_ApChange_Excp_004")
@pytest.mark.wifi_case(
    title="AP修改加密方式-WPA2和WPA2/WPA3互切（含pmf配置）",
    pre="1. 搭建网络拓扑：AC--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Reconnect_ApChange_Excp_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional,
wifi_case):
    run_wifi_ap_security_change_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wifi_ap_action_optional,
        initial_security="wpa2-aes-pmf-mandatory",
        transitions=[("wpa2-wpa3-aes-pmf-mandatory", True)],
    )

