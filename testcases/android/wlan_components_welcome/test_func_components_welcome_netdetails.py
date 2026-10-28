"""WiFi 连接 — Func_Components_Welcome_NetDetails（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome.network_details import (
    run_welcome_cancel_static_config_case,
    run_welcome_delete_network_case,
    run_welcome_ip_mode_default_case,
    run_welcome_ip_mode_options_case,
    run_welcome_save_static_config_case,
    run_welcome_static_field_input_case,
    run_welcome_static_field_rejection_case,
    run_welcome_static_fields_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_Vali_001")
@pytest.mark.wifi_case(
    title="bonding模式-网络详情检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_Vali_002")
@pytest.mark.wifi_case(
    title="双STA模式-WiFi网络详情-MAC地址检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_Vali_003")
@pytest.mark.wifi_case(
    title="双STA模式-HyperWiFi网络详情-IP地址检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_001")
@pytest.mark.wifi_case(
    title="IP设置默认配置检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_ip_mode_default_case(settings_ui, tmp_path, capsys)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_002")
@pytest.mark.wifi_case(
    title="IP设置可选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_002(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_ip_mode_options_case(settings_ui, tmp_path, capsys)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_003")
@pytest.mark.wifi_case(
    title="静态IP可配置项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_003(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_fields_case(settings_ui, tmp_path, capsys)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_004")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：ip正常格式输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_004(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_input_case(
        settings_ui,
        tmp_path,
        capsys,
        'ip_address',
        '192.168.1.100',
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_005")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：静态ip-IP地址配置特殊字符输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_005(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'ip_address', '~!')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_006")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：静态ip-IP地址配置中文输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_006(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'ip_address', '中华人民共和国')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_007")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：英文字母输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_007(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'ip_address', 'zxccxzc')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_008")
@pytest.mark.wifi_case(
    title="静态ip-IP地址配置：输入为空",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_008(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'ip_address', '')

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_009")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：ip正常格式输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_009(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_input_case(settings_ui, tmp_path, capsys, 'gateway', '192.168.1.1')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_010")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：特殊字符输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_010(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'gateway', '~!')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_011")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：中文输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_011(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'gateway', '中华人民共和国')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_012")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：英文字母输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_012(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'gateway', 'zxccxzc')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_013")
@pytest.mark.wifi_case(
    title="静态ip-网关配置：输入为空",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_013(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'gateway', '')

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_014")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：正常格式输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_014(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_input_case(settings_ui, tmp_path, capsys, 'prefix_length', '24')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_015")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：特殊字符输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_015(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'prefix_length', '~!')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_016")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：中文输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_016(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(
        settings_ui,
        tmp_path,
        capsys,
        'prefix_length',
        '中华人民共和国',
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_017")
@pytest.mark.wifi_case(
    title="静态ip-网络前缀长度配置：英文字母输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_017(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(
        settings_ui,
        tmp_path,
        capsys,
        'prefix_length',
        'zxccxzc',
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_018")
@pytest.mark.wifi_case(
    title="静态ip-ip和网关不在同一网段",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_019")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：正常格式输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_019(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_input_case(settings_ui, tmp_path, capsys, 'dns1', '223.5.5.5')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_020")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：特殊字符输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_020(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns1', '~!')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_021")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：中文输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_021(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns1', '中华人民共和国')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_022")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：英文字母输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_022(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns1', 'zxccxzc')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_023")
@pytest.mark.wifi_case(
    title="静态ip-DNS1配置：输入为空",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_023(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns1', '')

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_024")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：正常格式输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_024(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_input_case(settings_ui, tmp_path, capsys, 'dns2', '223.5.5.5')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_025")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：特殊字符输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_025(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns2', '~!')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_026")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：中文输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_026(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns2', '中华人民共和国')

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_027")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：英文字母输入",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_027(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_static_field_rejection_case(settings_ui, tmp_path, capsys, 'dns2', 'zxccxzc')

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_028")
@pytest.mark.wifi_case(
    title="静态ip-DNS2配置：输入为空",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_029")
@pytest.mark.wifi_case(
    title="静态配置输入框“X”按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_029(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_030")
@pytest.mark.wifi_case(
    title="“删除此网络”按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_030(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_delete_network_case(wifi, wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_031")
@pytest.mark.wifi_case(
    title="“取消”按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_031(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_cancel_static_config_case(wifi_yaml, settings_ui, tmp_path, capsys)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.no_wifi_lifecycle
@pytest.mark.case_id("Func_Components_Welcome_NetDetails_UI_032")
@pytest.mark.wifi_case(
    title="“保存”按钮",
    pre="1、设备恢复出厂 2、陪测试设备为AP、miniAP",
)
def test_Func_Components_Welcome_NetDetails_UI_032(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_save_static_config_case(wifi, wifi_yaml, settings_ui, tmp_path, capsys)
