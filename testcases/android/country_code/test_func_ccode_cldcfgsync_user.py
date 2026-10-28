"""WiFi 连接 — Func_Ccode_CldCfgSync_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.country_code import simulate_cloud_country_code_sequence

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_001")
@pytest.mark.wifi_case(
    title="批量推送-分组内存在部分欧盟区、部分非欧盟区的设备",
    pre="1、设备联网在线 确认分组是否存在不同区域的设备场景？",
)
def test_Func_Ccode_CldCfgSync_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_002")
@pytest.mark.wifi_case(
    title="批量推送-设备部分在线、部分离线",
    pre="1、部分设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_003")
@pytest.mark.wifi_case(
    title="批量推送-离线设备，依次重启后，均收到配置信息",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_004")
@pytest.mark.wifi_case(
    title="单台设备，同一国家码反复推送：US->US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["US", "US"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_005")
@pytest.mark.wifi_case(
    title="单台设备，同一国家码反复推送：EU->EU",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "EU"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_006")
@pytest.mark.wifi_case(
    title="单台设备，不同国家码反复推送：EU<->US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "US", "EU"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_007")
@pytest.mark.wifi_case(
    title="单台设备，占空比开关反复互切：EU<->EUS",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "EUS", "EU"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_008")
@pytest.mark.wifi_case(
    title="分组设备，同一国家码反复推送：US->US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["US", "US"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_009")
@pytest.mark.wifi_case(
    title="分组设备，同一国家码反复推送：EU->EU",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "EU"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_010")
@pytest.mark.wifi_case(
    title="分组设备，不同国家码反复推送：EU<->US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "US", "EU"], case_id = wifi_case["case_id"])

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_User_011")
@pytest.mark.wifi_case(
    title="分组设备，占空比开关反复互切：EU<->EUS",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_User_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "EUS", "EU"], case_id = wifi_case["case_id"])
