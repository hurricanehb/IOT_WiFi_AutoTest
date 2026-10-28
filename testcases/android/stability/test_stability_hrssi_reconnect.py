"""WiFi 连接 — Stability_HRssi_Reconnect（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_003")
@pytest.mark.wifi_case(
    title="STA 重启-双WiFi重连测试--300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_008")
@pytest.mark.wifi_case(
    title="STA 反复移动断开-双WiFi重连测试--500次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_001")
@pytest.mark.wifi_case(
    title="禁用启用WLAN开关-双WiFi重连测试--500次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_002")
@pytest.mark.wifi_case(
    title="禁用/启用飞行模式--双WiFi重连测试--300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_004")
@pytest.mark.wifi_case(
    title="STA 息屏-PNO扫描-双WIFI重连测试--300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_005")
@pytest.mark.wifi_case(
    title="AP/miniAP重启-双WiFi重连测试（AP端行为）-300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Stability_HRssi_Reconnect_006")
@pytest.mark.wifi_case(
    title="miniAP踢客户端-HyperWiFi重连测试（AP端行为）--300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Stability_HRssi_Reconnect_007")
@pytest.mark.wifi_case(
    title="AP/miniAP无线初始化（改信道、频宽等）-双WiFi重连测试--300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、miniAPrssi控制在-45dBm左右 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、配置好压测脚本",
)
def test_Stability_HRssi_Reconnect_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
