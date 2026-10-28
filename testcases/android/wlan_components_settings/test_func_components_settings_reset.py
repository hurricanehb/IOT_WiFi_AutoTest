"""WiFi 连接 — Func_Components_Settings_Reset（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_Reset_Vali_001")
@pytest.mark.wifi_case(
    title="恢复出厂设置",
    pre="1、DUT已连接ap wifi",
)
def test_Func_Components_Settings_Reset_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_Reset_Vali_002")
@pytest.mark.wifi_case(
    title="重置网络设置",
    pre="1、DUT已连接ap wifi",
)
def test_Func_Components_Settings_Reset_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
