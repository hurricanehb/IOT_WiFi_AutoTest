"""WiFi 连接 — Func_WlanAccess_PriBakLink_CfgIndep（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_001")
@pytest.mark.wifi_case(
    title="新接入HyperWiFi网络，不影响已连的WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_002")
@pytest.mark.wifi_case(
    title="断开HyperWiFi网络，不影响已连的WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_003")
@pytest.mark.wifi_case(
    title="删除HyperWiFi网络，不影响已连的WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_004")
@pytest.mark.wifi_case(
    title="切换HyperWiFi网络，不影响已连的WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP1、miniAP2分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_005")
@pytest.mark.wifi_case(
    title="修改HyperWiFi配置（ip设置、隐私），不影响已连的WiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_006")
@pytest.mark.wifi_case(
    title="新接入WiFi网络，不影响已连的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_007")
@pytest.mark.wifi_case(
    title="断开WiFi网络，不影响已连的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_008")
@pytest.mark.wifi_case(
    title="删除WiFi网络，不影响已连的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_009")
@pytest.mark.wifi_case(
    title="切换WiFi网络，不影响已连的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由1和路由器2、miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_010")
@pytest.mark.wifi_case(
    title="连接新HyperWiFi（密码错误）失败，不影响已连接的双WiFi",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP1、miniAP2分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_011")
@pytest.mark.wifi_case(
    title="连接新WiFi（密码错误）失败，不影响已连接的双WiFi",
    pre="1、测试环境：办公室 2、拓扑：陪测路由1和路由器2、miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_CfgIndep_Vali_012")
@pytest.mark.wifi_case(
    title="修改WiFi配置（高级设置项），不影响已连的HyperWiFi网络",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_WlanAccess_PriBakLink_CfgIndep_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

