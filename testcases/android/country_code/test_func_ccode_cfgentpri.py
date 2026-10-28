"""WiFi 连接 — Func_Ccode_CfgEntPri（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.country_code import (
    assert_cloud_country_code_precedes_shell,
    simulate_cloud_country_code,
    simulate_telephony_country_code,
)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_001")
@pytest.mark.wifi_case(
    title="有云端配置，设备插SIM卡，以云端配置为准",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_telephony_country_code(run_shell_cmd, "US", case_id = wifi_case["case_id"])
    simulate_cloud_country_code(run_shell_cmd, "EUS")

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_002")
@pytest.mark.wifi_case(
    title="有云端配置，手动shell命令配置不生效，以云端配置为准",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    assert_cloud_country_code_precedes_shell(
        run_shell_cmd,
        case_id=wifi_case["case_id"],
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_003")
@pytest.mark.wifi_case(
    title="无云端配置，设备插SIM卡，随telephone归属地自动映射",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_004")
@pytest.mark.wifi_case(
    title="无云端配置，手动shell命令配置，配置生效",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_005")
@pytest.mark.wifi_case(
    title="无云端配置，设备插SIM卡，shell命令配置后生效",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CfgEntPri_Vali_005")
@pytest.mark.wifi_case(
    title="无云端配置，设备插SIM卡，shell命令配置，重启设备后随telephone",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CfgEntPri_Vali_005_无云端配置_设备插SIM卡_shell命(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
