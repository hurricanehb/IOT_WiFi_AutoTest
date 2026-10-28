"""WiFi 连接 — Func_PriBakLink_Trigger_ConStatChg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.dual_link_failover import (
    run_connection_state_change_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_001")
@pytest.mark.wifi_case(
    title="首次顺序连接WiFi、HyperWiFi网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_connection_state_change_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        order=("wifi", "hyper"), targets={"wifi": -73, "hyper": -70},
        expected_primary="hyper",
    )

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_002")
@pytest.mark.wifi_case(
    title="首次顺序连接HyperWiFi、WiFi网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_002(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_connection_state_change_case(
        wifi_case["case_id"], run_shell_cmd, wifi, wifi_yaml, attenuator_optional,
        order=("hyper", "wifi"), targets={"wifi": -65, "hyper": -70},
        expected_primary="wifi",
    )

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_003")
@pytest.mark.wifi_case(
    title="主网络WiFi手动断开后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_004")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi手动断开后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_005")
@pytest.mark.wifi_case(
    title="主网络WiFi手动切换网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_006")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi手动切换网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_007")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，弱信号（-88dBm）自动切换新网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_008")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，2.4GWiFi弱信号（-73dBm）自动切换新网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Vali_009")
@pytest.mark.wifi_case(
    title="主网络HyperWiFi，5GWiFi弱信号（-70dBm）自动切换新网络后触发",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Excp_001")
@pytest.mark.wifi_case(
    title="主网络网络异常（如portal未认证），存在备网络--设计如此:WiFi仍为主网络，设备不能上网",
    pre="/",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Excp_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Stb_001")
@pytest.mark.wifi_case(
    title="首次依次连接HyperWiFi、WiFi后，主备链路切换",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Stb_002")
@pytest.mark.wifi_case(
    title="取消保存主网络（WiFi），备用网络（HyperWiFi）自动切换为主网络",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_PriBakLink_Trigger_ConStatChg_Stb_003")
@pytest.mark.wifi_case(
    title="取消保存主网络（HyperWiFi），备用网络（WiFi）自动切换为主网络",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1、AP2、miniAP1、miniAP2可联网",
)
def test_Func_PriBakLink_Trigger_ConStatChg_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
