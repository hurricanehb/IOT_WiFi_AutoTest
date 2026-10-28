"""WiFi 连接 — Func_WlanAccess_Conn_Channel（信道遍历等可 ADB 半自动）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.channel_plan import run_channel_automation_case

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_001")
@pytest.mark.wifi_case(
    title="Sub 1G-US国家码全信道遍历",
    pre="1、miniAP配置US国家码 2、miniAP支持的信道列表：",
)
def test_Func_WlanAccess_Conn_Channel_Vali_001(run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "miniAP",
            "country": "US",
            "wifi_entry_id": "hyperwifi_us",
            "bandwidths": [
                {"mhz": 1, "channels": {"start": 3, "end": 49, "step": 2}},
                {"mhz": 2, "channels": {"start": 6, "end": 46, "step": 4}},
                {"mhz": 4, "channels": {"start": 8, "end": 40, "step": 8}},
            ],
        },
        miniap_action=miniap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_002")
@pytest.mark.wifi_case(
    title="Sub 1G-EU国家码800MHz频段全信道遍历",
    pre="1、miniAP配置EU国家码 2、miniAP支持的信道列表：",
)
def test_Func_WlanAccess_Conn_Channel_Vali_002(run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "miniAP",
            "country": "EU",
            "band": "800MHz",
            "wifi_entry_id": "hyperwifi_eu",
            "bandwidths": [{"mhz": 1, "channels": [1, 3, 5, 7, 9]}],
        },
        miniap_action=miniap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_003")
@pytest.mark.wifi_case(
    title="Sub 1G-EU国家码900MHz频段全信道遍历",
    pre="1、miniAP配置EU国家码 2、miniAP支持的信道列表：",
)
def test_Func_WlanAccess_Conn_Channel_Vali_003(run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "miniAP",
            "country": "EU",
            "band": "900MHz",
            "wifi_entry_id": "hyperwifi_eu",
            "bandwidths": [{"mhz": 1, "channels": [31, 33, 35]}],
        },
        miniap_action=miniap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_004")
@pytest.mark.wifi_case(
    title="2.4G 全信道遍历",
    pre="1、AP配置JP国家码 2、AP支持的信道列表：1~13",
)
def test_Func_WlanAccess_Conn_Channel_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional, wifi_case
):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "ap",
            "band": "2g",
            "country": "JP",
            "wifi_entry_id": "wifi_ap_ssid_default",
            "configured_ssid": "PyAutoTest_Channel",
            "bandwidth_mhz": 20,
            "channels": {"start": 1, "end": 13},
        },
        wifi_ap_action=wifi_ap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_005")
@pytest.mark.wifi_case(
    title="5G 全信道遍历",
    pre="1、AP配置US国家码 2、AP支持的信道列表： 5.2GHz频段：36, 40, 44, 48 DFS频段：52, 56, 60, 64，100, 104, ..., 140, 144 5.8GHz频段：149, 153, 157, 161, 165",
)
def test_Func_WlanAccess_Conn_Channel_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional, wifi_case
):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "ap",
            "band": "5g",
            "country": "US",
            "configure_wifi": True,
            "wifi_entry_id": "wifi_ap_ssid_default",
            "configured_ssid": "PyAutoTest_Channel",
            "bandwidth_mhz": 20,
            "channels": [
                {"start": 36, "end": 48, "step": 4},
                {"start": 52, "end": 64, "step": 4},
                {"start": 149, "end": 165, "step": 4},
            ],
        },
        wifi_ap_action=wifi_ap_action_optional,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Channel_Vali_006")
@pytest.mark.wifi_case(
    title="wifi6E扩展频段全信道遍历",
    pre="1. Wi-Fi 6E AP（接入点）覆盖所有扩展频段信道（信道132-220）",
)
def test_Func_WlanAccess_Conn_Channel_Vali_006(
    run_shell_cmd, wifi, wifi_yaml, wifi_ap_action_optional, wifi_case
):
    run_channel_automation_case(
        wifi_case, run_shell_cmd, wifi, wifi_yaml,
        plan={
            "driver": "ap",
            "band": "6g",
            "bandwidth_mhz": 20,
            "channels": {"start": 132, "end": 220, "step": 4},
        },
        wifi_ap_action=wifi_ap_action_optional,
    )
