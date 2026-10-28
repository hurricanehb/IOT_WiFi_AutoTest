"""WiFi 连接 — Func_NetSelect_PriBakLink_Indep（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.net_selection import (
    run_dual_link_network_selection_independence_case,
)
from testcases.support.case_api import run_manual_placeholder
from testcases.support.skip import run_not_applicable

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_001")
@pytest.mark.wifi_case(
    title="双WiFi接入，网络选择独立性",
    pre="1、测试环境：实验室屏蔽箱 2、陪测AP1&miniAP1，信号为-70dBm 3、阈值：RSSI>-73dBm(2.4G)/-70dBm(5G/6G)/-86dBm(sub-1G",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_001(run_shell_cmd, wifi, wifi_yaml, attenuator_optional, wifi_case):
    run_dual_link_network_selection_independence_case(
        wifi_case["case_id"],
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator_optional,
    )

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_002")
@pytest.mark.wifi_case(
    title="双WiFi接入，WiFi发生网络重选",
    pre="1、测试环境：实验室环境 2、AP1、AP2、miniAP、miniAP2同一网关",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_003")
@pytest.mark.wifi_case(
    title="双WiFi接入，HyperWiFi发生网络重选",
    pre="1、测试环境：实验室环境 2、AP1、AP2、miniAP、miniAP2同一网关",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_004")
@pytest.mark.wifi_case(
    title="双WiFI接入，重选到不同网关的网络",
    pre="1、测试环境：office环境（传统 WiFi AC+AP，不同网关） 2、sta已保存AP1/miniAP1(网关1）、AP2/miniAP2(网关2）网络",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_005")
@pytest.mark.wifi_case(
    title="双WiFi接入，重选与主备切换同时发生",
    pre="主备切换模块已包含，这里删除",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_not_applicable(
        wifi_case,
        reason="需求已删除，覆盖已归属主备切换模块",
    )

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_PriBakLink_Indep_Int_006")
@pytest.mark.wifi_case(
    title="双WiFi接入，重选与漫游同时发生",
    pre="漫游模块已包含：这里删除 漫游与可连接切换判断测试",
)
def test_Func_NetSelect_PriBakLink_Indep_Int_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_not_applicable(
        wifi_case,
        reason="需求已删除，覆盖已归属漫游模块",
    )
