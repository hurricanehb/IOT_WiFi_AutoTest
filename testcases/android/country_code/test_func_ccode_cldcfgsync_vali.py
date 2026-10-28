"""WiFi 连接 — Func_Ccode_CldCfgSync_Vali（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.country_code import (
    simulate_cloud_country_code,
    simulate_cloud_country_code_sequence,
)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_001")
@pytest.mark.wifi_case(
    title="设备在线，云端立即下发配置并生效",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "EU", case_id = wifi_case["case_id"])

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_002")
@pytest.mark.wifi_case(
    title="设备离线，云端下发配置，不生效",
    pre="1、设备离线",
)
def test_Func_Ccode_CldCfgSync_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_003")
@pytest.mark.wifi_case(
    title="切换渠道，主动推送",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_004")
@pytest.mark.wifi_case(
    title="云端修改，主动推送",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code_sequence(run_shell_cmd, ["EU", "US"], case_id = wifi_case["case_id"])

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_005")
@pytest.mark.wifi_case(
    title="批量推送-国家码配置",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_006")
@pytest.mark.wifi_case(
    title="批量推送  -国家码配置取消",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_007")
@pytest.mark.wifi_case(
    title="批量推送  -占空比配置：开启",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_008")
@pytest.mark.wifi_case(
    title="批量推送  -占空比配置：关闭",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_009")
@pytest.mark.wifi_case(
    title="批量推送  -占空比配置：取消",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CldCfgSync_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CldCfgSync_Vali_010")
@pytest.mark.wifi_case(
    title="设备重启，重新拉取云端配置",
    pre="1、设备联网在线 注：非激活的设备，即工厂模式设备，重启不会重新拉取",
)
def test_Func_Ccode_CldCfgSync_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
