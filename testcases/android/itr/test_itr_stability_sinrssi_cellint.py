"""WiFi 连接 — Stability_SinRssi_CellInt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Stability_SinRssi_CellInt_002")
@pytest.mark.wifi_case(
    title="AP/miniAP重启-双WiFi重连测试（多STA竞争接入）-300次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、压测脚本（正弦调整rssi） 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）",
)
def test_Stability_SinRssi_CellInt_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Stability_SinRssi_CellInt_001")
@pytest.mark.wifi_case(
    title="禁用启用WLAN开关-双WiFi重连测试--500次",
    pre="1、拓扑：AC--AP/miniAP--STA 2、压测脚本（正弦调整rssi） 3、测试环境：实验室屏蔽箱 4、测试软件：Ixchariot或iperf3 5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）",
)
def test_Stability_SinRssi_CellInt_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
