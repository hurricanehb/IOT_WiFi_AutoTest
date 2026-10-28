"""WiFi 连接 — Func_WlanAccess_Conn_EAP（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_EAP_Vali_007")
@pytest.mark.wifi_case(
    title="STA选择PEAP_MSCHAPV2_CA证书-不验证方式连接",
    pre="1. 已配置好WPA/WPA2企业级WiFi网络，可通外网 2、金融系列因安全性原因未导入该选项",
)
def test_Func_WlanAccess_Conn_EAP_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
