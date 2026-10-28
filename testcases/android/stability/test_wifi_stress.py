"""WiFi 压力：快速开关（短轮次默认）。"""
from __future__ import annotations

import time

import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.config_loader import get_settings


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.parametrize("cycles", [3])
@pytest.mark.case_id("WiFi_Stress_Toggle_001")
@pytest.mark.wifi_case(
    title="快速开关 WiFi 若干轮后子系统仍可用",
    pre="设备 ADB 在线",
)
def test_WiFi_Stress_Toggle_001(run_shell_cmd, wifi: WiFiControl, cycles: int):
    for i in range(cycles):
        # Step: 开 → 关
        wifi.set_wifi_enabled(True)
        time.sleep(0.4)
        wifi.set_wifi_enabled(False)
        time.sleep(0.4)
        print(f"第 {i + 1}/{cycles} 轮开关完成")

    # Step: 恢复开启并查 status
    wifi.set_wifi_enabled(True)
    out = run_shell_cmd("cmd wifi status")
    assert out, "压力轮次结束后 cmd wifi status 应可查询"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("WiFi_Stress_Env_001")
@pytest.mark.wifi_case(
    title="多轮开启 WiFi 后状态仍可用",
    pre="可通过 WIFI_STRESS_CYCLES 环境变量调节轮次",
)
def test_WiFi_Stress_Env_001(run_shell_cmd, wifi: WiFiControl):
    n = max(1, min(get_settings().scenario_tuning.wifi_stress_cycles, 50))
    for i in range(n):
        wifi.set_wifi_enabled(True)
        time.sleep(0.2)
    out = run_shell_cmd("cmd wifi status")
    print(f"共 {n} 轮开启后 status：\n{out}")
    assert wifi.is_wifi_enabled() or out, "压力测试后 WiFi 应可用或 status 有输出"
