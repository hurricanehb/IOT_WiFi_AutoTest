"""WiFi 连接 — Func_WlanAccess_Conn_AP（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    run_nrc_miniap_compatibility_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_001")
@pytest.mark.wifi_case(
    title="STA连接高通方案的AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_002")
@pytest.mark.wifi_case(
    title="STA连接博通方案的AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_003")
@pytest.mark.wifi_case(
    title="STA连接MTK方案的AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_004")
@pytest.mark.wifi_case(
    title="STA连接realtek方案的AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_005")
@pytest.mark.wifi_case(
    title="STA连接NRC方案的miniAP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_005(
    run_shell_cmd, wifi, wifi_yaml, miniap_action_optional,
wifi_case):
    run_nrc_miniap_compatibility_case(
        wifi_case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        miniap_action_optional,
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_006")
@pytest.mark.wifi_case(
    title="STA连接Morse方案的miniAP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_007")
@pytest.mark.wifi_case(
    title="STA连接android10版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_008")
@pytest.mark.wifi_case(
    title="STA连接android11版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_009")
@pytest.mark.wifi_case(
    title="STA连接android12版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_010")
@pytest.mark.wifi_case(
    title="STA连接android13版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_011")
@pytest.mark.wifi_case(
    title="STA连接android14版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_012")
@pytest.mark.wifi_case(
    title="STA连接android15版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_013")
@pytest.mark.wifi_case(
    title="STA连接android16版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_014")
@pytest.mark.wifi_case(
    title="STA连接IOS14版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_015")
@pytest.mark.wifi_case(
    title="STA连接IOS15版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_016")
@pytest.mark.wifi_case(
    title="STA连接IOS16版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_017")
@pytest.mark.wifi_case(
    title="STA连接IOS17版本手机热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_018")
@pytest.mark.wifi_case(
    title="STA连接IOS系统平板热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_019")
@pytest.mark.wifi_case(
    title="STA连接安卓系统平板热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_020")
@pytest.mark.wifi_case(
    title="STA连接windows系统平板热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_021")
@pytest.mark.wifi_case(
    title="STA连接windows7系统PC热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_022")
@pytest.mark.wifi_case(
    title="STA连接windows10系统PC热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_023")
@pytest.mark.wifi_case(
    title="STA连接windows11系统PC热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_023(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_024")
@pytest.mark.wifi_case(
    title="STA连接macbook热点",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_024(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_025")
@pytest.mark.wifi_case(
    title="wifi4安全网络AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_025(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_026")
@pytest.mark.wifi_case(
    title="wifi5安全网络AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_026(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_027")
@pytest.mark.wifi_case(
    title="wifi6安全网络AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_AP_Comp_028")
@pytest.mark.wifi_case(
    title="wifi7安全网络AP",
    pre="AP外网可达",
)
def test_Func_WlanAccess_Conn_AP_Comp_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
