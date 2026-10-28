"""WiFi 连接 — Func_PriBakLink_Score_RSSI（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏状态评分周期",
    pre="1、测试环境：办公室工位 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_002")
@pytest.mark.wifi_case(
    title="息屏状态不发起轮询评分",
    pre="1、测试环境：办公室工位 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_003")
@pytest.mark.wifi_case(
    title="2.4G信号评分-rssi大于阈值（-70dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_004")
@pytest.mark.wifi_case(
    title="2.4G信号评分-rssi小于阈值（-70dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_005")
@pytest.mark.wifi_case(
    title="5G信号评分-rssi大于阈值（-70dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_006")
@pytest.mark.wifi_case(
    title="5G信号评分-rssi小于阈值（-70dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_007")
@pytest.mark.wifi_case(
    title="sub-1G信号评分-rssi大于阈值（-80dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Score_RSSI_Vali_008")
@pytest.mark.wifi_case(
    title="sub-1G信号评分-rssi小于阈值（-80dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Score_RSSI_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
