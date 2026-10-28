"""WiFi 连接 — Func_NetSelect_AutoScan_ScreenOn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_screen_on_disconnected_hyper_scan_case,
    run_screen_on_hyper_rssi_scan_case,
    run_screen_on_scan_backoff_reset_case,
    run_screen_on_single_link_disconnected_radio_scan_case,
    run_screen_on_settings_periodic_scan_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_001")
@pytest.mark.wifi_case(
    title="亮屏，任意连接状态，处于Settings页面周期性扫描（10s）",
    pre="1、测试环境：实验室屏蔽箱 2、任意连接状态：已连接、已连接弱信号、未连接等",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_screen_on_settings_periodic_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_002")
@pytest.mark.wifi_case(
    title="亮屏，WLAN未连接，处于非Settings页面周期性扫描（WiFi和HyperWiFi通用 5/5/8/10.。。。。s）",
    pre="测试环境：实验室屏蔽箱 1、V3MIX为20s 2、P3H 5/5/8/10.。。。。 3、原生传统WiFi 20/40/80/160 --原生周期基于手机（蜂窝为主），PDA以WiFi为主，可考量调整周期 4、不同产品存在差异，需明确 ---非setting页面扫描周期调整，具体数值待开发确定",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_002(run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case):
    run_screen_on_disconnected_hyper_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        miniap_action_optional,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_003")
@pytest.mark.wifi_case(
    title="单链路连接时，未连接的链路周期检查",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_screen_on_single_link_disconnected_radio_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_004")
@pytest.mark.wifi_case(
    title="亮屏，已连接网络且RSSI低于阈值，处于非Settings页面周期性扫描",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP，信号为-70dBm 3、阈值：RSSI>-73dBm(2.4G)/-70dBm(5G/6G)/-86dBm(sub-1G",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_004(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_screen_on_hyper_rssi_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        target_rssi=-88,
        expect_scan=True,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_005")
@pytest.mark.wifi_case(
    title="亮屏，已连接网络且RSSI高于阈值，处于非Settings页面不触发扫描",
    pre="1、测试环境：实验室屏蔽箱 2、阈值： RSSI>-73dBm(2.4G)/-70dBm(5G/6G)/-86dBm(sub-1G)",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_005(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_screen_on_hyper_rssi_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        target_rssi=-55,
        expect_scan=False,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_ScreenOn_Vali_006")
@pytest.mark.wifi_case(
    title="弱信号下屏幕状态变化，扫描周期重置",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_ScreenOn_Vali_006(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_screen_on_scan_backoff_reset_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )
