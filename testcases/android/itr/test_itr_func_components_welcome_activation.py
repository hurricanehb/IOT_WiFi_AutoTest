"""WiFi 连接 — Func_Components_Welcome_Activation（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_Activation_Int_004")
@pytest.mark.wifi_case(
    title="离线激活-连接双WiFi激活",
    pre="DUT恢复出厂设置，选择离线激活",
)
def test_Func_Components_Welcome_Activation_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_Activation_Int_005")
@pytest.mark.wifi_case(
    title="离线激活-连接单WiFi激活",
    pre="DUT恢复出厂设置，选择离线激活",
)
def test_Func_Components_Welcome_Activation_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
