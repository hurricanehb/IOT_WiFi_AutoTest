"""WiFi 连接 — Func_SoftAP_Basic（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.hotspot.auto_shutdown import (
    run_hotspot_auto_shutdown_disabled_case,
    run_hotspot_auto_shutdown_enabled_case,
)
from core.libs.android.wifi_scenarios.hotspot.defaults import (
    run_hotspot_band_editor_default_case,
    run_hotspot_band_options_case,
    run_hotspot_default_auto_shutdown_case,
    run_hotspot_default_band_case,
    run_hotspot_default_security_case,
    run_hotspot_default_switch_case,
    run_hotspot_security_editor_default_case,
    run_hotspot_security_options_case,
)
from core.libs.android.wifi_scenarios.hotspot.stability import (
    run_hotspot_fast_toggle_stability_case,
    run_hotspot_toggle_stability_case,
)
from testcases.support.case_api import run_manual_placeholder


@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_001")
@pytest.mark.wifi_case(
    title="“WLAN热点开关”启用",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_002")
@pytest.mark.wifi_case(
    title="“WLAN热点开关”禁用",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_003")
@pytest.mark.wifi_case(
    title="连接默认WLAN热点有效性",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_004")
@pytest.mark.wifi_case(
    title="二维码连接WLAN热点有效性",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_005")
@pytest.mark.wifi_case(
    title="WLAN热点二维码信息检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_006")
@pytest.mark.wifi_case(
    title="加密方式：WPA2/WPA3-Personal",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_007")
@pytest.mark.wifi_case(
    title="加密方式：WPA3-Personal",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_008")
@pytest.mark.wifi_case(
    title="加密方式：WPA2-Personal",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_009")
@pytest.mark.wifi_case(
    title="无加密",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_010")
@pytest.mark.wifi_case(
    title="WLAN热点2.4GHz频段有效性",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_011")
@pytest.mark.wifi_case(
    title="WLAN热点5GHz频段有效性",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_012")
@pytest.mark.wifi_case(
    title="WLAN热点双频段有效性",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_013")
@pytest.mark.wifi_case(
    title="“自动关闭热点”开关启用",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_013(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_auto_shutdown_enabled_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_014")
@pytest.mark.wifi_case(
    title="“自动关闭热点”开关禁用",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_014(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_auto_shutdown_disabled_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_015")
@pytest.mark.wifi_case(
    title="“热点名称“配置：中文字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_016")
@pytest.mark.wifi_case(
    title="“热点名称“配置：特殊字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_017")
@pytest.mark.wifi_case(
    title="“热点名称“配置：英文字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_018")
@pytest.mark.wifi_case(
    title="“热点名称“配置：数字",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_019")
@pytest.mark.wifi_case(
    title="“热点名称“配置：空格",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_020")
@pytest.mark.wifi_case(
    title="“热点名称“配置：32位",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_021")
@pytest.mark.wifi_case(
    title="”热点密码”配置：数字字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_022")
@pytest.mark.wifi_case(
    title="”热点密码”配置：英文字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_023")
@pytest.mark.wifi_case(
    title="“热点密码“配置：特殊字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_023(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_024")
@pytest.mark.wifi_case(
    title="“热点密码“配置：空格",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_024(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_025")
@pytest.mark.wifi_case(
    title="”热点密码”配置：长度8",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_025(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_026")
@pytest.mark.wifi_case(
    title="”热点密码”配置：长度32",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_026(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Vali_027")
@pytest.mark.wifi_case(
    title="”热点密码”配置：长度64",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Vali_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Excp_001")
@pytest.mark.wifi_case(
    title="”热点密码”配置：中文字符",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Excp_002")
@pytest.mark.wifi_case(
    title="“热点名称“配置：单引号",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Excp_003")
@pytest.mark.wifi_case(
    title="“热点名称“配置：双引号",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Excp_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Excp_004")
@pytest.mark.wifi_case(
    title="“热点密码“配置：单引号",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Excp_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Excp_005")
@pytest.mark.wifi_case(
    title="“热点密码“配置：双引号",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Excp_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_001")
@pytest.mark.wifi_case(
    title="2.4GWiFi+2.4G热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_002")
@pytest.mark.wifi_case(
    title="2.4GWiFi+5G热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_003")
@pytest.mark.wifi_case(
    title="5GWiFi+2.4G热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_004")
@pytest.mark.wifi_case(
    title="5GWiFi+5G热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_005")
@pytest.mark.wifi_case(
    title="启用热点后开启飞行模式",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_006")
@pytest.mark.wifi_case(
    title="飞行模式下开启热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_007")
@pytest.mark.wifi_case(
    title="重置WLAN热点重置",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_008")
@pytest.mark.wifi_case(
    title="恢复出厂设置热点重置",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_009")
@pytest.mark.wifi_case(
    title="热点状态通知",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_010")
@pytest.mark.wifi_case(
    title="快速设置面板热点开关",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_011")
@pytest.mark.wifi_case(
    title="蜂窝关闭状态（无SIM卡，无数据等）开启热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_Int_012")
@pytest.mark.wifi_case(
    title="WLAN关闭状态开启热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Int_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_SoftAP_Basic_Stb_001")
@pytest.mark.wifi_case(
    title="反复开关WLAN热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Stb_001(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_toggle_stability_case(adb, capsys)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_SoftAP_Basic_Stb_002")
@pytest.mark.wifi_case(
    title="快速开关WLAN热点",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Stb_002(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_fast_toggle_stability_case(adb, capsys)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_SoftAP_Basic_Stb_003")
@pytest.mark.wifi_case(
    title="长时间运行WLAN热点--ping包",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.stress
@pytest.mark.case_id("Func_SoftAP_Basic_Stb_004")
@pytest.mark.wifi_case(
    title="长时间运行WLAN热点--打流",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_Stb_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_001")
@pytest.mark.wifi_case(
    title="“WLAN热点开关”默认关闭",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_001(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_default_switch_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_002")
@pytest.mark.wifi_case(
    title="默认热点名称检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_003")
@pytest.mark.wifi_case(
    title="默认安全性检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_003(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_default_security_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_004")
@pytest.mark.wifi_case(
    title="默认热点密码检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_005")
@pytest.mark.wifi_case(
    title="默认AP频段检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_005(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_default_band_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_006")
@pytest.mark.wifi_case(
    title="“自动关闭热点”默认开启",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_006(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_default_auto_shutdown_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_007")
@pytest.mark.wifi_case(
    title="“安全性”弹窗-点击“安全性“检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_007(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_security_editor_default_case(adb, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_008")
@pytest.mark.wifi_case(
    title="“安全性”弹窗-点击“安全性“检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_008(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_security_options_case(adb, capsys)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_009")
@pytest.mark.wifi_case(
    title="“热点名称”弹窗-点击“热点名称”检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_010")
@pytest.mark.wifi_case(
    title="“热点名称”弹窗-“取消”按键",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_011")
@pytest.mark.wifi_case(
    title="“热点名称”弹窗-“确定”按键",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_012")
@pytest.mark.wifi_case(
    title="“热点名称“非法长度：33位",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_013")
@pytest.mark.wifi_case(
    title="“热点名称“非法配置：为空",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_014")
@pytest.mark.wifi_case(
    title="”热点密码“弹窗-点击“热点密码“检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_015")
@pytest.mark.wifi_case(
    title="”热点密码“弹窗-“取消”按键",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_016")
@pytest.mark.wifi_case(
    title="”热点密码“弹窗-“确定”按键",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_017")
@pytest.mark.wifi_case(
    title="”热点密码”配置：为空",
    pre="1、DUT恢复出厂状态 2、安全为WPA2/WPA3-Personal",
)
def test_Func_SoftAP_Basic_UI_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_018")
@pytest.mark.wifi_case(
    title="”热点密码“非法长度：<8位",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_019")
@pytest.mark.wifi_case(
    title="”热点密码“非法长度：>64位",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_020")
@pytest.mark.wifi_case(
    title="“AP频段”弹窗-点击“AP频段“检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_020(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_band_editor_default_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_021")
@pytest.mark.wifi_case(
    title="“AP频段”弹窗-”AP频段“可选项检查",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_021(run_shell_cmd, adb, capsys, wifi_case):
    run_hotspot_band_options_case(adb, capsys)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_SoftAP_Basic_UI_022")
@pytest.mark.wifi_case(
    title="已连接设备显示",
    pre="DUT恢复出厂状态",
)
def test_Func_SoftAP_Basic_UI_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
