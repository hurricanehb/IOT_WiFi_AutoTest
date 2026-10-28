"""WiFi 连接 — Func_WlanAccess_Conn_Scanner（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Scanner_Vali_007")
@pytest.mark.wifi_case(
    title="扫码添加AP SSID GBK编码16个中文字符网络",
    pre="1、AP配置为GBK编码格式的中文字符，密码为\"123 'test'  //\\\\\"",
)
def test_Func_WlanAccess_Conn_Scanner_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
