"""WiFi 连接 — Func_Components_Settings_ProxyCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ProxyCfg_Vali_001")
@pytest.mark.wifi_case(
    title="http proxy代理设置-手动",
    pre="1、拓扑：PC和DUT在同一局域网 2、PC安装CCproxy工具并正确配置",
)
def test_Func_Components_Settings_ProxyCfg_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Settings_ProxyCfg_Vali_002")
@pytest.mark.wifi_case(
    title="http proxy代理设置-自动配置（PAC）",
    pre="1、拓扑：PC和DUT在同一局域网 2、PC安装CCproxy工具并正确配置",
)
def test_Func_Components_Settings_ProxyCfg_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
