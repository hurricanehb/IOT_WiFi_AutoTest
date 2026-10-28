"""WiFi 连接 — Func_Components_SystemUI_WiFiPrompt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_WiFiPrompt_UI_001")
@pytest.mark.wifi_case(
    title="首次连接WiFi为主网络-HyperWiFi为备用网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_WiFiPrompt_UI_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_WiFiPrompt_UI_002")
@pytest.mark.wifi_case(
    title="首次连接HyperWiFi为主网络-WiFi为备用网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-80dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_WiFiPrompt_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_WiFiPrompt_UI_003")
@pytest.mark.wifi_case(
    title="主备网络发生切换",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_WiFiPrompt_UI_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.dualwifi
@pytest.mark.case_id("Func_Components_SystemUI_WiFiPrompt_UI_004")
@pytest.mark.wifi_case(
    title="断开主网络，备用网络切换为主网络",
    pre="1、测试环境：实验室漫游测试屏蔽箱 2、陪测试设备为AP（-50dBm）、miniAP（-50dBm）",
)
def test_Func_Components_SystemUI_WiFiPrompt_UI_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
