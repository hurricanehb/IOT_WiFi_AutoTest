"""WiFi 连接 — Func_NetSelect_Candicate_Skip（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_candidate_skip_hyper_traffic_case,
    run_candidate_skip_hyper_rssi_case,
    run_candidate_skip_wifi_rssi_case,
)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Candicate_Skip_Vali_001")
@pytest.mark.wifi_case(
    title="当前网络流量高于阈值（16数据包/秒）时跳过提名（仅WiFi）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Candicate_Skip_Vali_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_candidate_skip_hyper_traffic_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Candicate_Skip_Vali_002")
@pytest.mark.wifi_case(
    title="当前网络RSSI高于阈值时跳过提名-2.4G  WiFi（-73dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Candicate_Skip_Vali_002(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_candidate_skip_wifi_rssi_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        expected_band="2g",
        threshold_rssi=-73,
    )

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_NetSelect_Candicate_Skip_Vali_003")
@pytest.mark.wifi_case(
    title="当前网络RSSI高于阈值时跳过提名-5G  WiFi（-70dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Candicate_Skip_Vali_003(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_candidate_skip_wifi_rssi_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
        expected_band="5g",
        threshold_rssi=-70,
    )

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_NetSelect_Candicate_Skip_Vali_004")
@pytest.mark.wifi_case(
    title="当前网络RSSI高于阈值时跳过提名-HyperWiFi（-86dBm）",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP、miniAP可联网",
)
def test_Func_NetSelect_Candicate_Skip_Vali_004(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_candidate_skip_hyper_rssi_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )
