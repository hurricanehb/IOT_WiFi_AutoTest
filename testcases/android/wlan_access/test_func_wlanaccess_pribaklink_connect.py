"""WiFi 连接 — Func_WlanAccess_PriBakLink_Connect（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_003")
@pytest.mark.wifi_case(
    title="连接usb外设后启用WiFi并连接",
    pre="1、dut禁用WLAN",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_004")
@pytest.mark.wifi_case(
    title="已连接WiFi，插拔usb外设",
    pre="无",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_001")
@pytest.mark.wifi_case(
    title="接入共网关下WiFi网络/HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接同一上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_002")
@pytest.mark.wifi_case(
    title="接入不共网关下WiFi网络/HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接不同上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_003")
@pytest.mark.wifi_case(
    title="依次连接WiFi、HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_004")
@pytest.mark.wifi_case(
    title="依次连接HyperWiFi、WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_005")
@pytest.mark.wifi_case(
    title="wpa/wpa2 WiFi+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_006")
@pytest.mark.wifi_case(
    title="wpa2/wpa3 WiFi+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_007")
@pytest.mark.wifi_case(
    title="wpa3 WiFi+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_008")
@pytest.mark.wifi_case(
    title="portal认证网络+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_009")
@pytest.mark.wifi_case(
    title="wpa2+802.1x网络+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_010")
@pytest.mark.wifi_case(
    title="wpa2+802.1x+证书网络+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_011")
@pytest.mark.wifi_case(
    title="wpa3+802.1x网络+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_012")
@pytest.mark.wifi_case(
    title="wpa3+802.1x+证书网络+HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_013")
@pytest.mark.wifi_case(
    title="双WiFi接入后，手动切换新的WIFI网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Vali_014")
@pytest.mark.wifi_case(
    title="双WiFi接入后，手动切换新的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_001")
@pytest.mark.wifi_case(
    title="连接双WiFi后启用热点",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_002")
@pytest.mark.wifi_case(
    title="启用热点后连接双WiFi",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

