"""WiFi 连接 — Func_Components_Welcome_Button（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome.navigation import (
    run_welcome_expand_networks_case,
)


@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_Components_Welcome_Button_UI_001")
@pytest.mark.wifi_case(
    title="“展开全部”/大屏滚动显示更多 SSID 检查",
    pre="1、测试环境：办公室",
)
def test_Func_Components_Welcome_Button_UI_001(
    run_shell_cmd, wifi, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_case,
):
    run_welcome_expand_networks_case(settings_ui, tmp_path, capsys)
