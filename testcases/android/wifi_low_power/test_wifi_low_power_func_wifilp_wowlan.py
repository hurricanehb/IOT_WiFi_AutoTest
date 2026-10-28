"""WiFi 连接 — Func_WiFiLP_Wowlan（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_001")
@pytest.mark.wifi_case(
    title="WoWLAN能力查询",
    pre="设备支持WoWLAN",
)
def test_Func_WiFiLP_Wowlan_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_002")
@pytest.mark.wifi_case(
    title="挂起进入WoWLAN",
    pre="设备连接，执行挂起",
)
def test_Func_WiFiLP_Wowlan_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_003")
@pytest.mark.wifi_case(
    title="Magic Packet唤醒",
    pre="挂起设备，配置magic包唤醒",
)
def test_Func_WiFiLP_Wowlan_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_004")
@pytest.mark.wifi_case(
    title="模式匹配唤醒",
    pre="挂起设备，配置特定模式（如UDP端口）",
)
def test_Func_WiFiLP_Wowlan_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_005")
@pytest.mark.wifi_case(
    title="普通包不唤醒",
    pre="挂起设备，未配置模式匹配",
)
def test_Func_WiFiLP_Wowlan_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_006")
@pytest.mark.wifi_case(
    title="挂起时AP断开再恢复",
    pre="挂起设备，关闭AP再开启",
)
def test_Func_WiFiLP_Wowlan_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_Wowlan_Vali_007")
@pytest.mark.wifi_case(
    title="挂起时漫游",
    pre="挂起设备，AP信号变弱，另一AP可用",
)
def test_Func_WiFiLP_Wowlan_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
