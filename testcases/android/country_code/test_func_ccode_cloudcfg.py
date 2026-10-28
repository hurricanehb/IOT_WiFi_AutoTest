"""WiFi 连接 — Func_Ccode_CloudCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.country_code import simulate_cloud_country_code

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_001")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置占空比为空",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_002")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置占空比为关闭",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_003")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置占空比为开启",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_004")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置eus 异常值",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_005")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置占空比为空",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_006")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置占空比为关闭",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_007")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置占空比为开启",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_008")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置eus 异常值",
    pre="1、设备联网在线 2、云端未配置强制国家码",
)
def test_Func_Ccode_CloudCfg_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_009")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置下发国家码-EU",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "EU", case_id = wifi_case["case_id"])

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_010")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置下发国家码-EUS",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "EUS", case_id = wifi_case["case_id"])

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_011")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置下发国家码-US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "US", case_id = wifi_case["case_id"])

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_012")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置下发国家码-EU",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "EU", case_id = wifi_case["case_id"])

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_013")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置下发国家码-EUS",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "EUS", case_id = wifi_case["case_id"])

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_014")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置下发国家码-US",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    simulate_cloud_country_code(run_shell_cmd, "US", case_id = wifi_case["case_id"])

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_015")
@pytest.mark.wifi_case(
    title="设备国家码EU，云端配置下发国家码-异常值EU00，取消配置",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Vali_016")
@pytest.mark.wifi_case(
    title="设备国家码US，云端配置下发国家码-异常值EU00，取消配置",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_001")
@pytest.mark.wifi_case(
    title="单传统WIFI已连接，下发配置，检查网络连通性",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_002")
@pytest.mark.wifi_case(
    title="单HyperWIFI已连接，下发配置，跟随配置生效",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_003")
@pytest.mark.wifi_case(
    title="双WIFI已连接，下发配置，检查网络连通性",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_004")
@pytest.mark.wifi_case(
    title="有线网络已连接，下发配置，不影响已有网络连通性",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_005")
@pytest.mark.wifi_case(
    title="移动蜂窝数据已连接，下发配置，不影响已有网络连通性",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_006")
@pytest.mark.wifi_case(
    title="下发配置后，已保存的SSID自动重连",
    pre="1、设备联网在线",
)
def test_Func_Ccode_CloudCfg_Int_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_CloudCfg_Int_007")
@pytest.mark.wifi_case(
    title="息屏状态，下发配置成功且生效",
    pre="1、设备联网在线，息屏",
)
def test_Func_Ccode_CloudCfg_Int_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
