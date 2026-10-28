"""冒烟：不连设备，校验工程与核心模块可导入。"""
from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = [
    pytest.mark.smoke,
]


@pytest.mark.p3
@pytest.mark.case_id("SMOKE-WIFI-IMPORT-001")
def test_core_imports():
    """【用例ID】SMOKE-WIFI-IMPORT-001\n核心路径与配置可加载。"""
    from core.utils.config_loader import ROOT, android_data_path, get_settings

    assert ROOT.is_dir()
    assert get_settings() is not None
    assert isinstance(android_data_path("wifi_ssid.yaml"), Path)
