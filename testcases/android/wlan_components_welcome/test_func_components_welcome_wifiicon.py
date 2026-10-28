"""WiFi 连接 — Func_Components_Welcome_WifiIcon（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome.wifi_icon import (
    run_welcome_hyperwifi_icon_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Welcome_WifiIcon_UI_001")
@pytest.mark.wifi_case(
    title="WiFi网络标准4/5/6/7图标检查",
    pre="1、设备恢复出厂 2、周围存在WiFi4/5/6/7的路由器",
)
def test_Func_Components_Welcome_WifiIcon_UI_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_WifiIcon_UI_002")
@pytest.mark.wifi_case(
    title="HyperWiFi网络标识“HYPER Wi-Fi”检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_Welcome_WifiIcon_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_hyperwifi_icon_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_WifiIcon_UI_003")
@pytest.mark.wifi_case(
    title="HyperWiFi网络标准“H”图标检查",
    pre="1、设备恢复出厂 2、陪测试设备为miniAP",
)
def test_Func_Components_Welcome_WifiIcon_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
