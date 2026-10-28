"""WiFi 连接 — Func_Components_Settings_WifiNotify（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_Settings_WifiNotify_Vali_001")
@pytest.mark.wifi_case(
    title="附近有公共网络时发出通知",
    pre="1、陪测AP（设置公共无线）",
)
def test_Func_Components_Settings_WifiNotify_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
