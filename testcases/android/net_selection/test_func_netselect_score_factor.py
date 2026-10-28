"""WiFi 连接 — Func_NetSelect_Score_Factor（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_score_hyper_candidates_case,
)
from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_001")
@pytest.mark.wifi_case(
    title="RSSI 评分阈值-2.4GWiFi（-80dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1(2MHz)、miniAP2(2MHz) 3、DUT已保存陪测设备的网络 4、RSSI阈值-80dBm",
)
def test_Func_NetSelect_Score_Factor_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_002")
@pytest.mark.wifi_case(
    title="RSSI 评分阈值-5GWiFi（-77dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1(2MHz)、miniAP2(2MHz) 3、DUT已保存陪测设备的网络 4、RSSI阈值-80dBm",
)
def test_Func_NetSelect_Score_Factor_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_003")
@pytest.mark.wifi_case(
    title="RSSI 评分阈值-HyperWiFi（-80dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1(2MHz)、miniAP2(2MHz) 3、DUT已保存陪测设备的网络 4、RSSI阈值-80dBm",
)
def test_Func_NetSelect_Score_Factor_Vali_003(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_score_hyper_candidates_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        stronger_target_rssi=-79,
        weaker_target_rssi=-81,
        expected_rssi_scores=(60, 56),
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_004")
@pytest.mark.wifi_case(
    title="基于频宽的吞吐量评分",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1、miniAP2 3、DUT已保存陪测设备的网络",
)
def test_Func_NetSelect_Score_Factor_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_005")
@pytest.mark.wifi_case(
    title="当前网络加分，有无外网加分平等",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Score_Factor_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_006")
@pytest.mark.wifi_case(
    title="当前网络有外网时，候选网络有无外网加分平等",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Score_Factor_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_007")
@pytest.mark.wifi_case(
    title="安全网络加分",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1（WPA2）、AP2（WPA3）、AP3（open），频宽相同 3、DUT已保存陪测设备的网络",
)
def test_Func_NetSelect_Score_Factor_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_008")
@pytest.mark.wifi_case(
    title="已保存网络得分高于推荐网络",
    pre="测试条件不好构造",
)
def test_Func_NetSelect_Score_Factor_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_009")
@pytest.mark.wifi_case(
    title="免费网络得分高于付费网络",
    pre="测试条件不好构造",
)
def test_Func_NetSelect_Score_Factor_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_010")
@pytest.mark.wifi_case(
    title="不受信任的网络得分低于其他网络",
    pre="测试条件不好构造",
)
def test_Func_NetSelect_Score_Factor_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_011")
@pytest.mark.wifi_case(
    title="评分相同下，选择rssi较优的网络连接",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1(2MHz)、miniAP2(2MHz) 3、DUT已保存陪测设备的网络",
)
def test_Func_NetSelect_Score_Factor_Vali_011(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_score_hyper_candidates_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        require_equal_final_scores=True,
    )

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_012")
@pytest.mark.wifi_case(
    title="同一环境下，信噪比（干扰环境）的信号评分测试（仅WiFi）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Score_Factor_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_Score_Factor_Vali_013")
@pytest.mark.wifi_case(
    title="保护主动连接评分测试",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP1、miniAP2可联网",
)
def test_Func_NetSelect_Score_Factor_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
