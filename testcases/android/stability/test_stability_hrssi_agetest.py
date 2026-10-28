"""WiFi 连接 — Stability_HRssi_AgeTest（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Stability_HRssi_AgeTest_001")
@pytest.mark.wifi_case(
    title="12小时5G WIFI大流量稳定性测试（WIFI为主网络）",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3",
)
def test_Stability_HRssi_AgeTest_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_HRssi_AgeTest_002")
@pytest.mark.wifi_case(
    title="12小时HyperWiFi大流量稳定性测试（HyperWiFi为主网络）",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3",
)
def test_Stability_HRssi_AgeTest_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_AgeTest_003")
@pytest.mark.wifi_case(
    title="5*24小时息屏-亮屏-双WiFi连接稳定性（每隔24小时检查）",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：办公室",
)
def test_Stability_HRssi_AgeTest_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
