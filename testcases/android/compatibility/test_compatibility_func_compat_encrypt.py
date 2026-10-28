"""WiFi 连接 — Func_Compat_Encrypt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Encrypt_Vali_001")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3-SAE-PK",
    pre="1. AP配置为WPA3-SAE-PK模式； 2. 已知SAE-PK密码； 3. DUT支持SAE-PK。",
)
def test_Func_Compat_Encrypt_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_Compat_Encrypt_Vali_002")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，配置OCV",
    pre="1. AP配置为WPA3-Personal，并启用OCV(Operating Channel Validation)； 2. 已知SAE密码； 3. DUT支持OCV。",
)
def test_Func_Compat_Encrypt_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
