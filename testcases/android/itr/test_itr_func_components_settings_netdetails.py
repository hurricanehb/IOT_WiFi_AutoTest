"""WiFi 连接 — Func_Components_Settings_NetDetails（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_NetDetails_UI_006")
@pytest.mark.wifi_case(
    title="网络详情-GBK编码SSID“分享二维码”选项检查",
    pre="1、设备恢复出厂 2、陪测试设备为AP",
)
def test_Func_Components_Settings_NetDetails_UI_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
