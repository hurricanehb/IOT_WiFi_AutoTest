"""Android hotspot auto shutdown scenarios."""
from __future__ import annotations

import pytest

from core.libs.android.softap_control import SoftAPControl
from core.libs.android.wifi_scenarios.hotspot._helpers import _write_uncaptured_line


_SOFTAP_AUTO_SHUTDOWN_TARGET_SECONDS = 10 * 60


_SOFTAP_AUTO_SHUTDOWN_TOLERANCE_SECONDS = 30


_SOFTAP_AUTO_SHUTDOWN_EARLIEST_SECONDS = (
    _SOFTAP_AUTO_SHUTDOWN_TARGET_SECONDS - _SOFTAP_AUTO_SHUTDOWN_TOLERANCE_SECONDS
)


_SOFTAP_AUTO_SHUTDOWN_LATEST_SECONDS = (
    _SOFTAP_AUTO_SHUTDOWN_TARGET_SECONDS + _SOFTAP_AUTO_SHUTDOWN_TOLERANCE_SECONDS
)


_SOFTAP_AUTO_SHUTDOWN_DISABLED_OBSERVE_SECONDS = 12 * 60


def run_hotspot_auto_shutdown_enabled_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    softap.enable_auto_shutdown()

    # Step 2: 开启 WLAN 热点开关，保持无热点客户端连接
    softap.enable_hotspot()
    assert softap.is_hotspot_enabled(), "WLAN热点开关未成功开启"
    if softap.connected_client_count() > 0:
        message = "热点开启后已有其他设备连接本机热点，测试条件不满足，测试跳过"
        _write_uncaptured_line(capsys, message)
        pytest.skip(message)

    with capsys.disabled():
        client_connected = softap.wait_for_auto_shutdown_window(
            earliest_shutdown_seconds=_SOFTAP_AUTO_SHUTDOWN_EARLIEST_SECONDS,
            latest_shutdown_seconds=_SOFTAP_AUTO_SHUTDOWN_LATEST_SECONDS,
            on_progress=lambda remaining: _write_uncaptured_line(
                capsys,
                "等待中，热点自动关闭观察倒计时："
                f"{remaining // 60:02d}:{remaining % 60:02d}"
                "（目标10:00，允许09:30-10:30）",
            ),
        )
    if client_connected:
        message = "有其他设备连接本机热点，测试条件不满足，测试跳过"
        _write_uncaptured_line(capsys, message)
        pytest.skip(message)

    # Step 3: 通过 Wi-Fi 服务状态校验，监控阶段不依赖 WLAN 热点页面
    hotspot_enabled = softap.is_hotspot_active()
    _write_uncaptured_line(
        capsys, f"WLAN热点开关{'未关闭' if hotspot_enabled else '已关闭'}"
    )
    assert not hotspot_enabled, "WLAN热点开关未在 09:30-10:30 无客户端连接窗口内自动关闭"


def run_hotspot_auto_shutdown_disabled_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    softap.disable_auto_shutdown()

    # Step 2: 开启 WLAN 热点开关，保持无热点客户端连接
    softap.enable_hotspot()
    with capsys.disabled():
        client_connected = softap.wait_for_no_client_window(
            _SOFTAP_AUTO_SHUTDOWN_DISABLED_OBSERVE_SECONDS,
            on_progress=lambda remaining: _write_uncaptured_line(
                capsys,
                f"等待中，热点无客户端连接倒计时：{remaining // 60:02d}:{remaining % 60:02d}",
            ),
            expected_hotspot_enabled=True,
            expected_auto_shutdown_enabled=False,
        )
    if client_connected:
        message = "有其他设备连接本机热点，测试条件不满足，测试跳过"
        _write_uncaptured_line(capsys, message)
        pytest.skip(message)

    # Step 3: 12 分钟后校验 WLAN 热点开关保持开启
    hotspot_enabled = softap.is_hotspot_enabled()
    _write_uncaptured_line(
        capsys, f"WLAN热点开关{'保持开启' if hotspot_enabled else '未保持开启'}"
    )
    assert hotspot_enabled, "WLAN热点开关在 12 分钟无客户端连接后未保持开启"
