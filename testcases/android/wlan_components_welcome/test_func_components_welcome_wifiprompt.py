"""WiFi 连接 — Func_Components_Welcome_WifiPrompt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder, wifi_case

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_WifiPrompt_UI_001")
@pytest.mark.wifi_case(
    title="HyperWiFi网络引导接入提示语检查",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_Components_Welcome_WifiPrompt_UI_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_WifiPrompt_UI_002")
@pytest.mark.wifi_case(
    title="WiFi网络引导接入提示语检查",
    pre="1、测试环境：办公室 2、拓扑：陪测路由和miniAP分别有线连接上级路由器 3、miniAP加密方式为WPA3",
)
def test_Func_Components_Welcome_WifiPrompt_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

