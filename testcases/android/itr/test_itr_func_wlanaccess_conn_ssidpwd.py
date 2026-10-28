"""WiFi 连接 — Func_WlanAccess_Conn_SsidPwd（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_009")
@pytest.mark.wifi_case(
    title="SSID GBK 1位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_SsidPwd_Vali_010")
@pytest.mark.wifi_case(
    title="SSID GBK 16位“中文字符”正常连接",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_SsidPwd_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
