"""WiFi 连接 — Func_WlanAccess_Reconnect_StaChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Excp_001")
@pytest.mark.wifi_case(
    title="STA开关机自动重连-超长GBK编码",
    pre="1. 陪测试设备为锐捷AP720-A 2. AP配置16位GBK编码SSBD 3. STA已经连接AP；",
)
def test_Func_WlanAccess_Reconnect_StaChange_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Reconnect_StaChange_Excp_002")
@pytest.mark.wifi_case(
    title="STA开关机自动重连-已保存多个GBK编码网络且共网关",
    pre="1. 搭建网络拓扑：AC+AP--STA； 2. AC已运行DHCP服务器，IP pool：192.168.1/10~20； 3. 创建n≥2个GBK编码 SSID",
)
def test_Func_WlanAccess_Reconnect_StaChange_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
