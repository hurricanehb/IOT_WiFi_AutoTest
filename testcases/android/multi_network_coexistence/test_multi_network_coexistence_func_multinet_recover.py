"""WiFi 连接 — Func_MultiNet_Recover（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_001")
@pytest.mark.wifi_case(
    title="三网均无网，仅LAN恢复",
    pre="三网均无互联网（LAN、WLAN、蜂窝都无外网）",
)
def test_Func_MultiNet_Recover_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_002")
@pytest.mark.wifi_case(
    title="三网均无网，仅WiFi恢复",
    pre="三网均无互联网（LAN、WLAN、蜂窝都无外网）",
)
def test_Func_MultiNet_Recover_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_003")
@pytest.mark.wifi_case(
    title="三网均无网，仅HyperWiFi恢复",
    pre="三网均无互联网（LAN、WLAN、HyperWiFi均无外网）",
)
def test_Func_MultiNet_Recover_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_004")
@pytest.mark.wifi_case(
    title="当前使用LAN，LAN恢复",
    pre="当前默认网络为WLAN或蜂窝（LAN断开或无网），LAN已恢复有网",
)
def test_Func_MultiNet_Recover_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_005")
@pytest.mark.wifi_case(
    title="当前使用LAN，WLAN/蜂窝恢复",
    pre="设备使用LAN上网，WLAN和/或蜂窝之前无网或断开，现准备恢复",
)
def test_Func_MultiNet_Recover_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_006")
@pytest.mark.wifi_case(
    title="当前使用WLAN，LAN恢复",
    pre="设备使用WLAN上网，LAN断开或无网，现LAN恢复有网",
)
def test_Func_MultiNet_Recover_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_007")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN恢复",
    pre="当前默认网络为蜂窝，WLAN之前无网或断开，现WLAN恢复有网",
)
def test_Func_MultiNet_Recover_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_008")
@pytest.mark.wifi_case(
    title="当前使用WLAN，蜂窝恢复",
    pre="设备使用WLAN上网，蜂窝无网或断开",
)
def test_Func_MultiNet_Recover_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_009")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，LAN恢复",
    pre="设备使用蜂窝上网，LAN断开或无网，现LAN恢复有网",
)
def test_Func_MultiNet_Recover_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_010")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，WLAN恢复",
    pre="设备使用蜂窝上网，WLAN无网或断开，现WLAN恢复有网",
)
def test_Func_MultiNet_Recover_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_011")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，蜂窝恢复",
    pre="设备使用WLAN上网（或当前默认非蜂窝），蜂窝无网或断开",
)
def test_Func_MultiNet_Recover_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_012")
@pytest.mark.wifi_case(
    title="禁用204开关后网络切换？？",
    pre="设备已连接WLAN和蜂窝网络，204开关当前处于开启状态",
)
def test_Func_MultiNet_Recover_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_Recover_Vali_013")
@pytest.mark.wifi_case(
    title="WLAN长时间断网后恢复",
    pre="设备使用蜂窝上网，WLAN无网或断开，现WLAN恢复有网",
)
def test_Func_MultiNet_Recover_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
