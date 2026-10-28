"""WLAN 热点用例共享前置条件。"""
from __future__ import annotations

import pytest

from core.libs.android.bluetooth_wlan_reset_control import BluetoothWlanResetControl
from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger

log = get_logger(__name__)


@pytest.fixture(autouse=True)
def reset_bluetooth_and_wlan_before_hotspot_case(adb: AdbHelper) -> None:
    """每条热点用例执行前恢复 WLAN 和蓝牙的初始状态。"""
    BluetoothWlanResetControl(adb).reset_bluetooth_and_wlan()
    log.info("热点用例前置：已重置蓝牙和 WLAN 状态")