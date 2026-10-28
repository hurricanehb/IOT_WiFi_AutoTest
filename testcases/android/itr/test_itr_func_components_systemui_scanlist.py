"""WiFi 连接 — Func_Components_SystemUI_ScanList（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_Components_SystemUI_ScanList_Excp_002")
@pytest.mark.wifi_case(
    title="GBK编码SSID切换连接",
    pre="1、测试环境：办公室 2、陪测AP1、AP2，并配置GBK编码方式中文SSID",
)
def test_Func_Components_SystemUI_ScanList_Excp_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
