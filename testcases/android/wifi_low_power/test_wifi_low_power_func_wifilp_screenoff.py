"""WiFi 连接 — Func_WiFiLP_ScreenOff（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_pno_disconnected_screen_off_case,
    run_pno_no_saved_network_screen_off_case,
    run_screen_off_wifi_roaming_scan_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_001")
@pytest.mark.wifi_case(
    title="息屏-已连接-无流量-进入省电",
    pre="亮屏连接，无流量",
)
def test_Func_WiFiLP_ScreenOff_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_002")
@pytest.mark.wifi_case(
    title="息屏-已连接-无流量-保持省电",
    pre="息屏连接，无流量，AP配置DTIM=2",
)
def test_Func_WiFiLP_ScreenOff_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_003")
@pytest.mark.wifi_case(
    title="息屏-已连接-单播接收",
    pre="息屏连接，无流量，AP发送1个ICMP包",
)
def test_Func_WiFiLP_ScreenOff_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_004")
@pytest.mark.wifi_case(
    title="息屏-已连接-组播接收（DTIM周期内）",
    pre="息屏连接，无流量，AP DTIM=3",
)
def test_Func_WiFiLP_ScreenOff_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_005")
@pytest.mark.wifi_case(
    title="息屏-已连接-广播接收",
    pre="息屏连接，无流量，AP发送广播ARP请求",
)
def test_Func_WiFiLP_ScreenOff_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_006")
@pytest.mark.wifi_case(
    title="息屏-已连接-持续下行流量",
    pre="息屏连接，AP持续ping设备",
)
def test_Func_WiFiLP_ScreenOff_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_007")
@pytest.mark.wifi_case(
    title="息屏-已连接-上行流量",
    pre="息屏连接，应用后台发送数据（如消息推送）",
)
def test_Func_WiFiLP_ScreenOff_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_008")
@pytest.mark.wifi_case(
    title="息屏-未连接-有保存网络（PNO）",
    pre="息屏，Wi-Fi断开，已保存至少一个网络",
)
def test_Func_WiFiLP_ScreenOff_Vali_008(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_pno_disconnected_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        hyper=False,
        verify_reconnect=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_009")
@pytest.mark.wifi_case(
    title="息屏-未连接-无保存网络",
    pre="清除所有保存网络，Wi-Fi开启",
)
def test_Func_WiFiLP_ScreenOff_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_pno_no_saved_network_screen_off_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper=False,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_010")
@pytest.mark.wifi_case(
    title="息屏-漫游触发",
    pre="息屏连接AP1，信号逐渐减弱，AP2信号增强",
)
def test_Func_WiFiLP_ScreenOff_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_011")
@pytest.mark.wifi_case(
    title="息屏-漫游后恢复省电",
    pre="息屏连接，完成漫游后无流量",
)
def test_Func_WiFiLP_ScreenOff_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WiFiLP_ScreenOff_Vali_012")
@pytest.mark.wifi_case(
    title="息屏-信号变弱触发扫描",
    pre="息屏连接，信号逐渐减弱至-75dBm以下",
)
def test_Func_WiFiLP_ScreenOff_Vali_012(
    run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case
):
    run_screen_off_wifi_roaming_scan_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )
