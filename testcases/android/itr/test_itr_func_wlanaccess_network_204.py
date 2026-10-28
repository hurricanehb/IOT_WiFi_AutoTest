"""WiFi 连接 — Func_WlanAccess_Network_204（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_003")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-LAN/WLAN/蜂窝检测独立性",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_005")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常-LAN/WLAN/蜂窝检测周期验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_007")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-LAN/WLAN/蜂窝检测独立性",
    pre="LAN、WiFi、HyperWiFi蜂窝均无外网",
)
def test_Func_WlanAccess_Network_204_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_009")
@pytest.mark.wifi_case(
    title="204开关开启，外网异常-LAN/WLAN/蜂窝检测周期验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均无外网",
)
def test_Func_WlanAccess_Network_204_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_011")
@pytest.mark.wifi_case(
    title="204开关开启，外网正常与异常互切-LAN/WLAN/蜂窝网络连通性验证",
    pre="无",
)
def test_Func_WlanAccess_Network_204_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_Network_204_Vali_014")
@pytest.mark.wifi_case(
    title="204开关关闭，LAN/WLAN/蜂窝网络连通性验证",
    pre="LAN、WiFi、HyperWiFi蜂窝均可访问外网",
)
def test_Func_WlanAccess_Network_204_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
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
