"""WiFi 连接 — Func_Compat_Hotspot_Android（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_001")
@pytest.mark.wifi_case(
    title="接入Android 11热点后正常访问网络",
    pre="1. Android 11手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_002")
@pytest.mark.wifi_case(
    title="接入Android 12热点后正常访问网络",
    pre="1. Android 12手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_003")
@pytest.mark.wifi_case(
    title="接入Android 13热点后正常访问网络",
    pre="1. Android 13手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_004")
@pytest.mark.wifi_case(
    title="接入Android 14热点后正常访问网络",
    pre="1. Android 14手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_005")
@pytest.mark.wifi_case(
    title="接入Android 15热点后正常访问网络",
    pre="1. Android 15手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Hotspot_Android_Vali_006")
@pytest.mark.wifi_case(
    title="接入Android 16热点后正常访问网络",
    pre="1. Android 16手机开启便携热点，安全类型设为“WPA2-Personal”，频段为Auto； 2. 已知热点密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_Compat_Hotspot_Android_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
