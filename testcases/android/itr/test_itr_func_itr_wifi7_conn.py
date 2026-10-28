"""WiFi 连接 — Func_ITR_WiFi7_Conn（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_ITR_WiFi7_Conn_Vali_001")
@pytest.mark.wifi_case(
    title="连接WiFi7 AP（按兼容性矩阵扩充：）",
    pre="AP外网可达",
)
def test_Func_ITR_WiFi7_Conn_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
