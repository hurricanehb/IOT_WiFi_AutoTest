"""WiFi 连接 — Func_WlanAccess_PriBakLink_Connect（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_003")
@pytest.mark.wifi_case(
    title="连接usb外设后启用WiFi并连接",
    pre="1、dut禁用WLAN",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_WlanAccess_PriBakLink_Connect_Int_004")
@pytest.mark.wifi_case(
    title="已连接WiFi，插拔usb外设",
    pre="无",
)
def test_Func_WlanAccess_PriBakLink_Connect_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
