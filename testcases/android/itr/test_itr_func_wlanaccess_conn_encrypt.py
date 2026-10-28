"""WiFi 连接 — Func_WlanAccess_Conn_Encrypt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_023")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，禁用AE_PK，禁用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置禁用AE_PK，禁用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_023(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_024")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，禁用SAE_PK，启用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置禁用SAE_PK，启用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_024(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_025")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，启用SAE_PK，禁用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置启用SAE_PK，禁用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_025(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_026")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3加密，启用SAE_PK，启用OCV（暂无AP支持配置）",
    pre="1. DUT为出厂状态 2. 陪测AP：Ruckus R770，已配置启用SAE_PK，启用OCV",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_026(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_020")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，可选启用pmf",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置可选pmf",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_021")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，强制启用pmf（暂无AP支持配置强制开启或关闭pmf）",
    pre="1、 网络拓扑：AP--STA； 2、DUT出厂状态 3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置强制启用pmf",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_028")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，强制开启pmf",
    pre="1、测试环境：办公室 2、拓扑：miniAP有线连接上级路由器 3、备注：miniAP 采用的是CCMP加密方式",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_030")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，AES256GCM加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_030(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_031")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，强制开启pmf",
    pre="1. DUT为出厂状态 2. 已配置好WiFI网络，可通外网",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_031(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
