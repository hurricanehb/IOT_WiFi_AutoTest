"""WiFi 连接 — Stability_LinRssi_Thput（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Stability_LinRssi_Thput_001")
@pytest.mark.wifi_case(
    title="rssi动态变化-WiFi吞吐量稳定性测试",
    pre="1、拓扑：AC--多AP/多miniAP--STA 2、压测脚本（正弦调整rssi） 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）",
)
def test_Stability_LinRssi_Thput_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_LinRssi_Thput_002")
@pytest.mark.wifi_case(
    title="rssi动态变化-HyperWiFi吞吐量稳定性测试",
    pre="1、拓扑：AC--多AP/多miniAP--STA 2、压测脚本（正弦调整rssi） 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）",
)
def test_Stability_LinRssi_Thput_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
