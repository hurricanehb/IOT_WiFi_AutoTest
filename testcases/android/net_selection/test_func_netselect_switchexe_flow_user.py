"""WiFi 连接 — Func_NetSelect_SwitchExe_Flow_User（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_001")
@pytest.mark.wifi_case(
    title="禁用启用WLAN开关网络重选",
    pre="1、测试环境：办公室环境 2、2个陪测nimiap，miniap1有网络，miniap2无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_002")
@pytest.mark.wifi_case(
    title="禁用启用飞行模式网络重选",
    pre="1、测试环境：办公室环境 2、2个陪测nimiap，miniap1有网络，miniap2无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_003")
@pytest.mark.wifi_case(
    title="系统重启后网络重选",
    pre="1、测试环境：办公室环境 2、2个陪测nimiap，miniap1有网络，miniap2无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_004")
@pytest.mark.wifi_case(
    title="连接断开后网络重选",
    pre="1、测试环境：办公室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_005")
@pytest.mark.wifi_case(
    title="取消保存网络后网络重选",
    pre="1、测试环境：办公室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_006")
@pytest.mark.wifi_case(
    title="setting页面，弱信号下网络重选",
    pre="1、测试环境：办公室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_007")
@pytest.mark.wifi_case(
    title="home页面，弱信号下后网络重选",
    pre="1、测试环境：办公室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_008")
@pytest.mark.wifi_case(
    title="从上级断开无线连接后网络重选",
    pre="1、测试环境：实验室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_User_009")
@pytest.mark.wifi_case(
    title="远近移动（RSSI弱）断开连接网络重选",
    pre="1、测试环境：实验室环境 2、3个陪测nimiap，miniap1、2有网络，miniap3无网络",
)
def test_Func_NetSelect_SwitchExe_Flow_User_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
