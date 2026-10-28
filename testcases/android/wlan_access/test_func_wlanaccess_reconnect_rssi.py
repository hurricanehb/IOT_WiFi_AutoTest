"""WiFi 连接 — Func_WlanAccess_Reconnect_RSSI（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.reconnect_rssi import (
    run_reconnect_rssi_threshold_case,
)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_RSSI_Vali_001")
@pytest.mark.wifi_case(
    title="2.4G回连阈值（-80dbm）",
    pre="1、屏蔽环境 2、设备亮屏，WiFi断开连接",
)
def test_Func_WlanAccess_Reconnect_RSSI_Vali_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_reconnect_rssi_threshold_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        hyper=False, expected_band="2g", no_reconnect_rssi=-80,
        reconnect_rssi=-79,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_RSSI_Vali_002")
@pytest.mark.wifi_case(
    title="5G回连阈值（-77dBm）",
    pre="1、屏蔽环境 2、设备亮屏，WiFi断开连接",
)
def test_Func_WlanAccess_Reconnect_RSSI_Vali_002(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_reconnect_rssi_threshold_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        hyper=False, expected_band="5g", no_reconnect_rssi=-78,
        reconnect_rssi=-77,
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_RSSI_Vali_003")
@pytest.mark.wifi_case(
    title="HyperWiFi回连阈值（-93dBm）",
    pre="1、屏蔽环境 2、设备亮屏，HyperWIFI断开连接",
)
def test_Func_WlanAccess_Reconnect_RSSI_Vali_003(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_reconnect_rssi_threshold_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        hyper=True, no_reconnect_rssi=-94, reconnect_rssi=-93,
    )

