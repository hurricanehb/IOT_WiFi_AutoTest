"""WiFi 连接 — Func_WlanAccess_Conn_IPCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder
from core.libs.android.wifi_scenarios.ip_configuration import (
    run_default_ip_mode_ui_case,
    run_ip_mode_options_ui_case,
    run_static_field_input_ui_case,
    run_static_fields_ui_case,
)
from core.libs.android.wifi_scenarios.ip_configuration import (
    run_dhcp_acquisition_case,
    run_dhcp_renewal_case,
    run_dhcp_switch_case,
    run_ip_configuration_reboot_case,
    run_static_configuration_case,
)
from core.libs.android.wifi_scenarios.ip_configuration import (
    collect_wifi_ipv4_info,
)


def static_ip_ui_case(*, overrides, expect_save_enabled, expect_values=False):
    """Replace a generated placeholder body with the shared UI field flow."""
    def decorate(original):
        def automated(run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui, wifi_case):
            print(f"[{original.__name__}] UI 输入={overrides!r}")
            run_static_field_input_ui_case(
                wifi,
                wifi_yaml,
                run_shell_cmd,
                wifi_ip_settings_ui,
                overrides=overrides,
                expect_save_enabled=expect_save_enabled,
                expect_values=expect_values,
            )

        automated.__name__ = original.__name__
        automated.__module__ = original.__module__
        return automated

    return decorate

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_001")
@pytest.mark.wifi_case(
    title="DHCP获取IP",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    print(f"[{wifi_case['case_id']}] 连接 AP，校验 DHCP 地址、网关、前缀、DNS 和网关连通性")
    run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_002")
@pytest.mark.wifi_case(
    title="DHCP IP续约",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，租期2min；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    print(f"[{wifi_case['case_id']}] 连接 AP，跨过租约检查窗口后校验 IP 保持不变")
    run_dhcp_renewal_case(wifi, wifi_yaml, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_003")
@pytest.mark.wifi_case(
    title="DHCP ip更新有效性",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP1已运行DHCP服务器，IP pool：192.168.1/10~20； 3. AP2已运行DHCP服务器，IP pool：192.168.2/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):

    print(f"[{wifi_case['case_id']}] 依次连接 AP1/AP2，校验 DHCP 地址和网关随子网更新")
    run_dhcp_switch_case(wifi, wifi_yaml, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_004")
@pytest.mark.wifi_case(
    title="静态IP，与AP同网段",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 保存同网段静态配置，检查网络详情和网关连通性")
    run_static_configuration_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_005")
@pytest.mark.wifi_case(
    title="静态IP，与AP不同网段",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 保存异网段静态配置，检查配置生效且网关不可达")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        different_subnet=True,
        expect_gateway_reachable=False,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_006")
@pytest.mark.wifi_case(
    title="DNS默认配置有效性",
    pre="1. 搭建网络拓扑：Internet--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_006(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 保存默认静态 DNS，检查 DNS 和域名联网")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        expect_internet=True,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_007")
@pytest.mark.wifi_case(
    title="DNS配置为网关ip有效性",
    pre="1. 搭建网络拓扑：Internet--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_007(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    info = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    gateway = str(info.gateway)
    print(f"[{wifi_case['case_id']}] DNS1/DNS2 配置为网关 {gateway}，检查域名联网")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        dns_servers=(gateway, gateway),
        expect_internet=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_008")
@pytest.mark.wifi_case(
    title="DNS1正确+DNS2错误配置有效性",
    pre="1. 搭建网络拓扑：Internet--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_008(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    info = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    working_dns = str(info.dns_servers[0])
    print(f"[{wifi_case['case_id']}] 配置正确 DNS1={working_dns} 和错误 DNS2，检查解析")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        dns_servers=(working_dns, "192.0.2.1"),
        expect_internet=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_009")
@pytest.mark.wifi_case(
    title="DNS1错误+DNS2正确配置有效性",
    pre="1. 搭建网络拓扑：Internet--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_009(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    info = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    working_dns = str(info.dns_servers[0])
    print(f"[{wifi_case['case_id']}] 配置错误 DNS1 和正确 DNS2={working_dns}，检查解析")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        dns_servers=("192.0.2.1", working_dns),
        expect_internet=True,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Vali_010")
@pytest.mark.wifi_case(
    title="DNS1错误+DNS2错误配置有效性",
    pre="1. 搭建网络拓扑：Internet--AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Vali_010(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 配置两个错误 DNS，检查域名无法解析")
    run_static_configuration_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        dns_servers=("192.0.2.1", "198.51.100.1"),
        expect_internet=False,
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Excp_001")
@pytest.mark.wifi_case(
    title="IP配置下电保存",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Excp_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 重启验证 DHCP/静态配置持久性，结束后恢复 DHCP")
    run_ip_configuration_reboot_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_Excp_002")
@pytest.mark.wifi_case(
    title="已连接网络，静态和DHCP互相切换",
    pre="1. 搭建网络拓扑：AP--STA； 2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；",
)
def test_Func_WlanAccess_Conn_IPCfg_Excp_002(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] DHCP 切换静态并校验，再恢复 DHCP")
    run_static_configuration_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_001")
@pytest.mark.wifi_case(
    title="默认配置检查",
    pre="1、DUT出厂状态",
)
def test_Func_WlanAccess_Conn_IPCfg_UI_001(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 打开已连接网络高级选项，检查默认 IP 设置")
    run_default_ip_mode_ui_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_002")
@pytest.mark.wifi_case(
    title="可选IP配置项检查",
    pre="1、DUT出厂状态",
)
def test_Func_WlanAccess_Conn_IPCfg_UI_002(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 检查 IP 设置下拉选项")
    run_ip_mode_options_ui_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_003")
@pytest.mark.wifi_case(
    title="静态IP可配置项检查",
    pre="1、DUT出厂状态",
)
def test_Func_WlanAccess_Conn_IPCfg_UI_003(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 切换静态 IP，检查五个可配置字段")
    run_static_fields_ui_case(
        wifi, wifi_yaml, run_shell_cmd, wifi_ip_settings_ui
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_004")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：ip正常格式输入",
    pre="无",
)
@static_ip_ui_case(overrides={}, expect_save_enabled=True)
def test_Func_WlanAccess_Conn_IPCfg_UI_004(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 输入同网段静态 IP，检查输入值和保存按钮")
    run_static_field_input_ui_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        overrides={},
        expect_save_enabled=True,
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_005")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：静态ip-IP地址配置特殊字符输入",
    pre="无",
)
@static_ip_ui_case(overrides={"ip_address": "~!"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_005(
    run_shell_cmd, wifi, wifi_yaml, wifi_ip_settings_ui,
wifi_case):

    print(f"[{wifi_case['case_id']}] 输入特殊字符，检查保存按钮不可用")
    run_static_field_input_ui_case(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        wifi_ip_settings_ui,
        overrides={"ip_address": "~!"},
        expect_save_enabled=False,
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_006")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：静态ip-IP地址配置中文输入",
    pre="无",
)
@static_ip_ui_case(overrides={"ip_address": "中文"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_007")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：英文字母输入",
    pre="无",
)
@static_ip_ui_case(overrides={"ip_address": "zxccxzc"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_008")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：输入为空",
    pre="无",
)
@static_ip_ui_case(overrides={"ip_address": ""}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_009")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：ip正常格式输入",
    pre="无",
)
@static_ip_ui_case(
    overrides={"gateway": "192.168.50.1"},
    expect_save_enabled=True,
    expect_values=True,
)
def test_Func_WlanAccess_Conn_IPCfg_UI_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_010")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：特殊字符输入",
    pre="无",
)
@static_ip_ui_case(overrides={"gateway": "~!"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_011")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：中文输入",
    pre="无",
)
@static_ip_ui_case(overrides={"gateway": "中文"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_012")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：英文字母输入",
    pre="无",
)
@static_ip_ui_case(overrides={"gateway": "zxccxzc"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_013")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：输入为空",
    pre="无",
)
@static_ip_ui_case(overrides={"gateway": ""}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_014")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：正常格式输入",
    pre="无",
)
@static_ip_ui_case(
    overrides={"prefix_length": "24"},
    expect_save_enabled=True,
    expect_values=True,
)
def test_Func_WlanAccess_Conn_IPCfg_UI_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_015")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：特殊字符输入",
    pre="无",
)
@static_ip_ui_case(overrides={"prefix_length": "~!"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_016")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：中文输入",
    pre="无",
)
@static_ip_ui_case(overrides={"prefix_length": "中文"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_017")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：英文字母输入",
    pre="无",
)
@static_ip_ui_case(overrides={"prefix_length": "zxccxzc"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_018")
@pytest.mark.wifi_case(
    title="静态ip-ip和网关不在同一网段",
    pre="无",
)
@static_ip_ui_case(
    overrides={
        "ip_address": "192.168.0.10",
        "gateway": "192.168.2.1",
        "prefix_length": "31",
    },
    expect_save_enabled=False,
)
def test_Func_WlanAccess_Conn_IPCfg_UI_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_019")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：正常格式输入",
    pre="无",
)
@static_ip_ui_case(
    overrides={"dns1": "223.5.5.5"},
    expect_save_enabled=True,
    expect_values=True,
)
def test_Func_WlanAccess_Conn_IPCfg_UI_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_020")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：特殊字符输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns1": "~!"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_021")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：中文输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns1": "中文"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_022")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：英文字母输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns1": "zxccxzc"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_023")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：输入为空",
    pre="无",
)
@static_ip_ui_case(overrides={"dns1": ""}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_023(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_024")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：正常格式输入",
    pre="无",
)
@static_ip_ui_case(
    overrides={"dns2": "223.5.5.5"},
    expect_save_enabled=True,
    expect_values=True,
)
def test_Func_WlanAccess_Conn_IPCfg_UI_024(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_025")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：特殊字符输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns2": "~!"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_025(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_026")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：中文输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns2": "中文"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_026(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_027")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：英文字母输入",
    pre="无",
)
@static_ip_ui_case(overrides={"dns2": "zxccxzc"}, expect_save_enabled=False)
def test_Func_WlanAccess_Conn_IPCfg_UI_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_IPCfg_UI_028")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：输入为空",
    pre="无",
)
@static_ip_ui_case(overrides={"dns2": ""}, expect_save_enabled=True)
def test_Func_WlanAccess_Conn_IPCfg_UI_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

