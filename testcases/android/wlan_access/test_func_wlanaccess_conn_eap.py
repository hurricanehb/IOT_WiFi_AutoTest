"""WiFi 连接 — Func_WlanAccess_Conn_EAP（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_007")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_CA证书-不验证方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网 2、金融系列因安全性原因未导入该选项",
)
def test_Func_WlanAccess_Conn_EAP_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_001")
@pytest.mark.wifi_case(
    title="STA选择PWD方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_002")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_CA证书_首次使用时信任方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_003")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_CA证书_安装证书方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_004")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_已有CA证书_不验证证书在线状态方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_005")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_已有CA证书_需要证书状态（非强制）方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_006")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_已有CA证书_需要证书状态式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_008")
@pytest.mark.wifi_case(
    title="STA选择PEAP_GTC方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_009")
@pytest.mark.wifi_case(
    title="STA选择PEAP_SIM方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_010")
@pytest.mark.wifi_case(
    title="STA选择PEAP_AKA方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_011")
@pytest.mark.wifi_case(
    title="STA选择PEAP_AKA'方式连接WiFi",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_012")
@pytest.mark.wifi_case(
    title="STA选择TLS_方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_013")
@pytest.mark.wifi_case(
    title="STA选择TTLS_PAP方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_014")
@pytest.mark.wifi_case(
    title="STA选择TTLS_MSCHAP方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_015")
@pytest.mark.wifi_case(
    title="STA选择TTLS_MSCHAPV2方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_016")
@pytest.mark.wifi_case(
    title="STA选择TTLS_GTC方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网",
)
def test_Func_WlanAccess_Conn_EAP_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_001")
@pytest.mark.wifi_case(
    title="WEP/WPA系列密码错误",
    pre="无",
)
def test_Func_WlanAccess_Conn_EAP_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_002")
@pytest.mark.wifi_case(
    title="802.1X认证失败-错误的用户名、密码",
    pre="1. 已配置好企业级WiFi网络",
)
def test_Func_WlanAccess_Conn_EAP_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_003")
@pytest.mark.wifi_case(
    title="802.1X认证失败-客户端证书不匹配",
    pre="1. 已配置好企业级WiFi网络",
)
def test_Func_WlanAccess_Conn_EAP_Excp_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_004")
@pytest.mark.wifi_case(
    title="802.1X认证失败-CA证书过期",
    pre="1. 已配置好企业级WiFi网络",
)
def test_Func_WlanAccess_Conn_EAP_Excp_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_005")
@pytest.mark.wifi_case(
    title="802.1X认证失败-CA证书不匹配",
    pre="1. 已配置好企业级WiFi网络",
)
def test_Func_WlanAccess_Conn_EAP_Excp_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_006")
@pytest.mark.wifi_case(
    title="802.1X认证失败-域名不匹配",
    pre="1. 已配置好企业级WiFi网络",
)
def test_Func_WlanAccess_Conn_EAP_Excp_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_007")
@pytest.mark.wifi_case(
    title="802.1X认证失败-radius服务器交互异常（无响应、超时、拒绝等）",
    pre="1. 已配置好企业级WiFi网络，server端禁用服务器",
)
def test_Func_WlanAccess_Conn_EAP_Excp_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Excp_008")
@pytest.mark.wifi_case(
    title="802.1X认证失败-eap方式不匹配",
    pre="1. 已配置好企业级WiFi网络，server端禁用PWD认证方式",
)
def test_Func_WlanAccess_Conn_EAP_Excp_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

