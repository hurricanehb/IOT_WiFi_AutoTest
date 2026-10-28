"""WiFi 连接 — Func_PriBakLink_Trigger_RSSI（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.dual_link_failover import (
    run_rssi_threshold_failover_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_RSSI_Vali_001")
@pytest.mark.wifi_case(
    title="主网络WiFi，2.4G-WiFi的RSSI下降到阈值（-73dBm）后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Trigger_RSSI_Vali_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_RSSI_Vali_002")
@pytest.mark.wifi_case(
    title="主网络WiFi，5G-WiFi的RSSI下降到阈值（-73dBm）后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Trigger_RSSI_Vali_002(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_rssi_threshold_failover_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        expected_band="5g",
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_RSSI_Vali_003")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，2.4GWiFi的RSSI回升到阈值（-73dBm）后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Trigger_RSSI_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_RSSI_Vali_004")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，5GWiFi的RSSI回升到阈值（-73dBm）后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Trigger_RSSI_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_RSSI_Vali_005")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，HyperWiFi的RSSI下降到阈值（-84dBm）后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_PriBakLink_Trigger_RSSI_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
