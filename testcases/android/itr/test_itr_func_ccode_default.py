"""WiFi 连接 — Func_Ccode_Default（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_Default_Vali_001")
@pytest.mark.wifi_case(
    title="初始未联网，WiFi默认国家码检查",
    pre="1、设备恢复出厂设置",
)
def test_Func_Ccode_Default_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
