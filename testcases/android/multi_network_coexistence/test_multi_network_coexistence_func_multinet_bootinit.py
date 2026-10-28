"""WiFi 连接 — Func_MultiNet_BootInit（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_001")
@pytest.mark.wifi_case(
    title="三网上电初始化，均有外网",
    pre="设备关机，连接LAN（已插网线且可上网），同时开启WLAN和蜂窝",
)
def test_Func_MultiNet_BootInit_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_002")
@pytest.mark.wifi_case(
    title="三网上电初始化，仅LAN有网",
    pre="设备关机，连接LAN（已插网线且可上网），同时开启WLAN和蜂窝（但WLAN和蜂窝无网络）",
)
def test_Func_MultiNet_BootInit_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_003")
@pytest.mark.wifi_case(
    title="三网上电初始化，仅WLAN有网",
    pre="设备关机，WLAN已连接且有网，同时开启蜂窝（无网），LAN线已插但上级无网",
)
def test_Func_MultiNet_BootInit_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_004")
@pytest.mark.wifi_case(
    title="三网上电初始化，仅蜂窝有网",
    pre="设备关机，蜂窝有网，WLAN开启但无网，LAN线已插但上级无网",
)
def test_Func_MultiNet_BootInit_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_005")
@pytest.mark.wifi_case(
    title="三网无网上电初始化",
    pre="设备关机，连接LAN（无外网），开启WLAN（无外网）和蜂窝（无信号或数据关闭）",
)
def test_Func_MultiNet_BootInit_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_BootInit_Vali_006")
@pytest.mark.wifi_case(
    title="无网络恢复初始化",
    pre="设备关机，连接LAN（已插网线且可上网），同时开启WLAN和蜂窝",
)
def test_Func_MultiNet_BootInit_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
