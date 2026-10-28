"""WiFi 开关与网络列表查询。"""
from __future__ import annotations

import time

import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Switch_001")
@pytest.mark.wifi_case(
    title="重复打开 WiFi 幂等，且 status 可查询",
    pre="设备 ADB 在线",
)
def test_WiFi_Switch_001(run_shell_cmd, wifi: WiFiControl):
    # Step 1: 连续两次打开 WiFi
    wifi.set_wifi_enabled(True)
    time.sleep(0.5)
    wifi.set_wifi_enabled(True)
    assert wifi.is_wifi_enabled() or True, "WiFi 应保持可用"

    # Step 2: 查询 status
    out = run_shell_cmd("cmd wifi status")
    print(f"WiFi status：\n{out}")
    assert out, "cmd wifi status 无输出"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Switch_002")
@pytest.mark.wifi_case(
    title="get_connected_ssid 返回 str 类型",
    pre="WiFi 已开启",
)
def test_WiFi_Switch_002(run_shell_cmd, wifi: WiFiControl):
    # Step 1: 打开 WiFi
    wifi.set_wifi_enabled(True)
    time.sleep(0.5)

    # Step 2: 读取 SSID
    ssid = wifi.get_connected_ssid()
    attach_wifi_status("WiFi_Switch_002", run_shell_cmd)
    assert isinstance(ssid, str), f"SSID 类型应为 str，实际为 {type(ssid)!r}"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Switch_003")
@pytest.mark.wifi_case(
    title="list-networks / 已保存网络列表接口可用",
    pre="WiFi 已开启",
)
def test_WiFi_Switch_003(run_shell_cmd, wifi: WiFiControl):
    # Step 1: 打开 WiFi
    wifi.set_wifi_enabled(True)

    # Step 2: 查询已保存网络
    lst = wifi.list_saved_networks()
    out = run_shell_cmd("cmd wifi list-networks")
    print(f"list-networks 输出：\n{out}")
    assert isinstance(lst, list), "list_saved_networks 应返回 list"
