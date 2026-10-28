"""WiFi 连接 — Func_NetSelect_AutoScan_PNO（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_pno_connected_screen_off_case,
    run_pno_disconnected_screen_off_case,
    run_pno_miniap_reboot_screen_off_case,
    run_pno_no_saved_network_screen_off_case,
    run_screen_off_wifi_roaming_scan_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_001")
@pytest.mark.wifi_case(
    title="息屏，连接未断开，不发起PNO扫描",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1/miniAP2可联网",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_pno_connected_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
    )

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_002")
@pytest.mark.wifi_case(
    title="息屏，拉远无线断开，发起PNO扫描",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1/miniAP2可联网",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_003")
@pytest.mark.wifi_case(
    title="息屏，重启miniAP，发起PNO扫描",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_003(run_shell_cmd, wifi, wifi_yaml, miniap_action_optional, wifi_case):
    run_pno_miniap_reboot_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        miniap_action_optional,
    )

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_004")
@pytest.mark.wifi_case(
    title="连接断开后息屏，发起PNO扫描",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1可联网",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_004(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_pno_disconnected_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_005")
@pytest.mark.wifi_case(
    title="取消保存后（无保存网络）息屏，不发起PNO扫描",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1可联网",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_pno_no_saved_network_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_006")
@pytest.mark.wifi_case(
    title="无候选网络状态息屏，检查PNO扫描周期",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_007")
@pytest.mark.wifi_case(
    title="亮息屏切换，PNO扫描周期更新（60s->20s）",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_008")
@pytest.mark.wifi_case(
    title="PNO全信道扫描机制",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_AutoScan_PNO_Vali_009")
@pytest.mark.wifi_case(
    title="息屏有连接状态，漫游扫描（WiFi）",
    pre="1、测试环境：实验室屏蔽箱/办公室 2、陪测AP、miniAP1",
)
def test_Func_NetSelect_AutoScan_PNO_Vali_009(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_screen_off_wifi_roaming_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )
