"""WiFi 连接 — Func_WiFiLP_ScreenOn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_autoscan_after_airplane_cycle_case,
    run_autoscan_after_weak_signal_disconnect_case,
    run_autoscan_after_wlan_toggle_case,
    run_screen_on_settings_periodic_scan_case,
)
from core.libs.android.wifi_scenarios.low_power import (
    run_screen_on_disconnected_scan_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏-已连接-无流量（非设置界面）",
    pre="连接至AP，无数据收发",
)
def test_Func_WiFiLP_ScreenOn_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏-已连接-无流量（Wi-Fi设置界面）",
    pre="连接至AP，无数据收发",
)
def test_Func_WiFiLP_ScreenOn_Vali_002(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_screen_on_settings_periodic_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        hyper=False,
        target_rssi=None,
    )

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_003")
@pytest.mark.wifi_case(
    title="亮屏-已连接-有下行流量",
    pre="连接至AP，AP侧持续ping设备",
)
def test_Func_WiFiLP_ScreenOn_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_004")
@pytest.mark.wifi_case(
    title="亮屏-已连接-有上行流量",
    pre="连接至AP，应用主动上传数据",
)
def test_Func_WiFiLP_ScreenOn_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_005")
@pytest.mark.wifi_case(
    title="亮屏-未连接-无保存网络",
    pre="清除所有已保存网络，Wi-Fi开启",
)
def test_Func_WiFiLP_ScreenOn_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_screen_on_disconnected_scan_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, keep_saved_network=False
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_006")
@pytest.mark.wifi_case(
    title="亮屏-未连接-有保存网络",
    pre="保存一个已知网络（未连接），Wi-Fi开启",
)
def test_Func_WiFiLP_ScreenOn_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_screen_on_disconnected_scan_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, keep_saved_network=True
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_007")
@pytest.mark.wifi_case(
    title="亮屏-飞行模式切换",
    pre="亮屏已连接",
)
def test_Func_WiFiLP_ScreenOn_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_airplane_cycle_case(
        wifi_case["case_id"], run_shell_cmd, wifi
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_008")
@pytest.mark.wifi_case(
    title="亮屏-Wi-Fi开关切换",
    pre="亮屏已连接",
)
def test_Func_WiFiLP_ScreenOn_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_wlan_toggle_case(
        wifi_case["case_id"], run_shell_cmd, wifi
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_009")
@pytest.mark.wifi_case(
    title="亮屏-已连接-漫游触发",
    pre="漫游环境",
)
def test_Func_WiFiLP_ScreenOn_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_010")
@pytest.mark.wifi_case(
    title="亮屏-漫游中丢包率",
    pre="亮屏连接，持续ping网关",
)
def test_Func_WiFiLP_ScreenOn_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOn_Vali_011")
@pytest.mark.wifi_case(
    title="亮屏-弱信号触发扫描",
    pre="无",
)
def test_Func_WiFiLP_ScreenOn_Vali_011(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_autoscan_after_weak_signal_disconnect_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )
