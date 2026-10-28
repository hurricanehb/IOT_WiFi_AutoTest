"""WiFi 连接 — Func_WlanAccess_Network_IpReachMon（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Vali_001")
@pytest.mark.wifi_case(
    title="正常接入，网关可达-IPV4",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router启用DHCPs",
)
def test_Func_WlanAccess_Network_IpReachMon_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Vali_002")
@pytest.mark.wifi_case(
    title="正常接入，网关可达-IPV6",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router启用DHCPs",
)
def test_Func_WlanAccess_Network_IpReachMon_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Vali_003")
@pytest.mark.wifi_case(
    title="静态ip可达性检测",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router&miniAP禁用DHCPs",
)
def test_Func_WlanAccess_Network_IpReachMon_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Int_004")
@pytest.mark.wifi_case(
    title="漫游后触发检测",
    pre="1、测试环境：屏蔽箱环境 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_WlanAccess_Network_IpReachMon_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Excp_001")
@pytest.mark.wifi_case(
    title="连接WLAN，网关不可达",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router&miniAP禁用DHCPs：192.168.0.1/24",
)
def test_Func_WlanAccess_Network_IpReachMon_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Excp_002")
@pytest.mark.wifi_case(
    title="网关不可达，再恢复",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router&miniAP禁用DHCPs：192.168.0.1/24",
)
def test_Func_WlanAccess_Network_IpReachMon_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Vali_004")
@pytest.mark.wifi_case(
    title="周期性检测验证",
    pre="1、拓扑：Internet--Router（AP）--miniAP 2、Router&miniAP禁用DHCPs：192.168.0.1/24",
)
def test_Func_WlanAccess_Network_IpReachMon_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Int_001")
@pytest.mark.wifi_case(
    title="双WiFi接入独立检测",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_IpReachMon_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Int_002")
@pytest.mark.wifi_case(
    title="双WiFi不共网关，主网络断开后备链路变主链路重新触发检测",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP 3、AP和miniAP不共网关",
)
def test_Func_WlanAccess_Network_IpReachMon_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Int_003")
@pytest.mark.wifi_case(
    title="切换ap连接时重新检测",
    pre="1、测试环境：屏蔽箱环境 2、陪测试设备为AP1、AP2、miniAP1、miniAP2",
)
def test_Func_WlanAccess_Network_IpReachMon_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_IpReachMon_Int_005")
@pytest.mark.wifi_case(
    title="dhcp和静态ip切换后重新检测",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_IpReachMon_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

