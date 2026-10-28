"""WiFi 连接 — Stability_LRssi_CellInt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_001")
@pytest.mark.wifi_case(
    title="近距离（-60dBm）自身蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-60dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA插上SIM卡，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_002")
@pytest.mark.wifi_case(
    title="远距离（-86dBm）自身蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-86dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA插上SIM卡，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_003")
@pytest.mark.wifi_case(
    title="近距离（-60dBm）外界蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-60dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA不插SIM卡，且配置频点在1GHz以下 6、干扰源插SIM，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_004")
@pytest.mark.wifi_case(
    title="远距离（-86dBm）外界蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-86dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA不插SIM卡，且配置频点在1GHz以下 6、干扰源插SIM，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_005")
@pytest.mark.wifi_case(
    title="近距离（-60dBm）自身&外界蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-60dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA、干扰源插SIM卡，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LRssi_CellInt_006")
@pytest.mark.wifi_case(
    title="远距离（-86dBm）自身&外界蜂窝&HyperWiFi干扰稳定性测试",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAP rssi控制在-86dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、STA、干扰源插上SIM卡，且配置频点在1GHz以下",
)
def test_Stability_LRssi_CellInt_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
