"""WiFi 连接 — Func_Components_Welcome_Version（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome.version import (
    run_welcome_version_case,
)


@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_Version_Vali_001")
@pytest.mark.wifi_case(
    title="Welcome组件版本检查",
    pre="1、设备恢复出厂",
)
def test_Func_Components_Welcome_Version_Vali_001(run_shell_cmd, wifi, wifi_yaml, capsys, wifi_case):
    run_welcome_version_case(run_shell_cmd, capsys)
