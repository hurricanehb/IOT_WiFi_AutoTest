"""WiFi 连接 — Func_NetSelect_AutoScan_StatChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_autoscan_after_airplane_cycle_case,
    run_autoscan_after_disconnect_case,
    run_autoscan_after_screen_wake_case,
    run_autoscan_after_weak_signal_disconnect_case,
    run_autoscan_after_wlan_toggle_case,
    run_autoscan_airplane_wlan_enable_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_001")
@pytest.mark.wifi_case(
    title="处于Settings页面，连接断开后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_disconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        settings_page=True,
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_002")
@pytest.mark.wifi_case(
    title="处于非Settings页面，连接断开后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_disconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_003")
@pytest.mark.wifi_case(
    title="禁用-启用wlan开关后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_wlan_toggle_case(
        wifi_case["case_id"], run_shell_cmd, wifi
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_004")
@pytest.mark.wifi_case(
    title="启用-禁用飞行模式开关后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_airplane_cycle_case(
        wifi_case["case_id"], run_shell_cmd, wifi
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_005")
@pytest.mark.wifi_case(
    title="未连接状态下息屏再亮屏后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_after_screen_wake_case(
        wifi_case["case_id"], run_shell_cmd, wifi
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Vali_006")
@pytest.mark.wifi_case(
    title="远近移动（RSSI弱）断开连接后立即发起单次扫描",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Vali_006(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_autoscan_after_weak_signal_disconnect_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml,
        attenuator_optional,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_StatChange_Excp_001")
@pytest.mark.wifi_case(
    title="飞行模式下启用WLAN开关立即发起扫描连接",
    pre="测试环境：实验室屏蔽箱",
)
def test_Func_NetSelect_AutoScan_StatChange_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_autoscan_airplane_wlan_enable_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml
    )
