"""WiFi 连接 — Func_WlanAccess_Network_204（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.network_204 import (
    run_204_default_config_case,
    run_dual_wifi_204_case,
    run_dual_wifi_204_disabled_case,
    run_dual_wifi_204_period_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_001")
@pytest.mark.wifi_case(
    title="204检测默认配置检查",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_204_default_config_case(wifi_case['case_id'], run_shell_cmd, wifi)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_002")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-双WiFi网络检测独立性",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_dual_wifi_204_case(wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_003")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-LAN/WLAN/蜂窝检测独立性",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_004")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-双WiFi网络连通性检测周期验证",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_005")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-LAN/WLAN/蜂窝检测周期验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_006")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-双WiFi网络检测独立性",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_dual_wifi_204_case(
        wifi_case['case_id'],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        wan='down',
        expect_captive_success=False,
    )

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_007")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-LAN/WLAN/蜂窝检测独立性",
    pre="LAN、WiFi、HyperWiFi蜂窝均无外网",
)
def test_Func_WlanAccess_Network_204_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_008")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-双WiFi网络连通性检测周期验证",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_dual_wifi_204_period_case(wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_009")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-LAN/WLAN/蜂窝检测周期验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均无外网",
)
def test_Func_WlanAccess_Network_204_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_010")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常与异常互切-双WiFi网络连通性验证",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_011")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常与异常互切-LAN/WLAN/蜂窝网络连通性验证",
    pre="无",
)
def test_Func_WlanAccess_Network_204_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_012")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常与异常：一条正常、一条不正常",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_013")
@pytest.mark.wifi_case(
    title="204开关关闭，双WiFi网络连通性验证",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_dual_wifi_204_disabled_case(wifi_case['case_id'], run_shell_cmd, wifi, wifi_yaml)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_014")
@pytest.mark.wifi_case(
    title="204开关关闭，LAN/WLAN/蜂窝网络连通性验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Excp_001")
@pytest.mark.wifi_case(
    title="sta收到非正常的dns解析ip",
    pre="1、陪测AP、miniAP 2、router具有DNS劫持功能，如腾达路由器",
)
def test_Func_WlanAccess_Network_204_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Excp_002")
@pytest.mark.wifi_case(
    title="单网络断网恢复",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Excp_003")
@pytest.mark.wifi_case(
    title="LAN<->WLAN网络断网恢复",
    pre="1、LAN连接router1，WLAN连接Router2&minIAP",
)
def test_Func_WlanAccess_Network_204_Excp_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Excp_004")
@pytest.mark.wifi_case(
    title="WLAN<->蜂窝网络断网恢复",
    pre="1、WLAN连接Router2&minIAP",
)
def test_Func_WlanAccess_Network_204_Excp_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Excp_005")
@pytest.mark.wifi_case(
    title="关闭204，连接无外网网络再启用204",
    pre="1、AP、miniAP无外网",
)
def test_Func_WlanAccess_Network_204_Excp_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Int_001")
@pytest.mark.wifi_case(
    title="portal网络识别",
    pre="1、AP外网正常 2、sta启用204",
)
def test_Func_WlanAccess_Network_204_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Int_002")
@pytest.mark.wifi_case(
    title="设备休眠 / 锁屏后状态下的 204 检测",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP 3、sta启用204",
)
def test_Func_WlanAccess_Network_204_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Int_003")
@pytest.mark.wifi_case(
    title="双WiFi接入，主备链路切换后重新检测",
    pre="1、测试环境：屏蔽箱 2、陪测试设备为AP、miniAP 3、sta启用204",
)
def test_Func_WlanAccess_Network_204_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_WlanAccess_Network_204_Int_004")
@pytest.mark.wifi_case(
    title="网络重选后重新检测",
    pre="1、测试环境：屏蔽箱 2、陪测试设备为AP1、AP2、miniAP1、miniAP2 3、sta启用204",
)
def test_Func_WlanAccess_Network_204_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_WlanAccess_Network_204_Stb_001")
@pytest.mark.wifi_case(
    title="204开关反复开启/关闭测试",
    pre="1、测试环境：办公室工位 2、陪测试设备为AP、miniAP",
)
def test_Func_WlanAccess_Network_204_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

