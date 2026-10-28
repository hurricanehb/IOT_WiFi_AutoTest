"""WiFi 连接 — Func_MultiNet_Degrade（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_001")
@pytest.mark.wifi_case(
    title="当前使用LAN，LAN有网->无网，WLAN/蜂窝达标",
    pre="设备使用LAN上网，WLAN和蜂窝均有网且达标",
)
def test_Func_MultiNet_Degrade_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_002")
@pytest.mark.wifi_case(
    title="当前使用LAN，LAN有网->无网，WLAN/蜂窝不达标",
    pre="设备使用LAN上网，WLAN和蜂窝均无Internet（不达标）",
)
def test_Func_MultiNet_Degrade_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_003")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN有网->无网，蜂窝达标",
    pre="设备使用WLAN上网（有Internet），蜂窝有网且达标",
)
def test_Func_MultiNet_Degrade_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_004")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN有网->无网，蜂窝不达标",
    pre="设备使用WLAN上网（有Internet），蜂窝无Internet（不达标）",
)
def test_Func_MultiNet_Degrade_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_005")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN弱网",
    pre="WLAN+蜂窝均有网，WLAN为默认",
)
def test_Func_MultiNet_Degrade_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_006")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN信号减弱至临界值",
    pre="设备连接WLAN（信号良好），蜂窝可用",
)
def test_Func_MultiNet_Degrade_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_007")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，蜂窝有网->无网",
    pre="WLAN无Internet，蜂窝有网且为默认",
)
def test_Func_MultiNet_Degrade_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Degrade_Vali_008")
@pytest.mark.wifi_case(
    title="多网络外网依次断开",
    pre="三网均有网，以太网为默认",
)
def test_Func_MultiNet_Degrade_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
