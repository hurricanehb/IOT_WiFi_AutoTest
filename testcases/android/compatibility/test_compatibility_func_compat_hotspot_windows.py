"""WiFi 连接 — Func_Compat_Hotspot_Windows（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Windows_Vali_001")
@pytest.mark.wifi_case(
    title="接入Windows 10热点后正常访问网络",
    pre="1. Windows 10笔记本开启“移动热点”功能，频段选“任何可用”，加密WPA2； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Windows_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Windows_Vali_002")
@pytest.mark.wifi_case(
    title="接入Windows 11热点后正常访问网络",
    pre="1. Windows 11笔记本开启“移动热点”功能，频段选“任何可用”，加密WPA2； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Windows_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
