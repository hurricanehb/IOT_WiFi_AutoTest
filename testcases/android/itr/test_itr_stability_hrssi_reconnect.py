"""WiFi 连接 — Stability_HRssi_Reconnect（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
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
