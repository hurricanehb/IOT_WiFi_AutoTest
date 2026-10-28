"""WiFi 连接 — Func_WlanAccess_Conn_Manual（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Manual_Vali_008")
@pytest.mark.wifi_case(
    title="手动添加网络配置：AP SSID GBK编码16个“中文字符”",
    pre="1、陪测试设备为锐捷AP720-A",
)
def test_Func_WlanAccess_Conn_Manual_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
