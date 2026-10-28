"""Fixtures owned exclusively by WLAN advanced-settings tests."""
from pathlib import Path

import pytest

from core.libs.android.wifi_ui.advanced_settings_support import AdvancedSettingsSupportUI


@pytest.fixture
def settings_ui(device_serial: str, tmp_path: Path) -> AdvancedSettingsSupportUI:
    return AdvancedSettingsSupportUI(device_serial, tmp_path / "advanced-settings-ui")