"""Android hotspot stability scenarios."""
from __future__ import annotations

from core.libs.android.softap_control import SoftAPControl
from core.libs.android.wifi_scenarios.hotspot._helpers import _write_uncaptured_line


_SOFTAP_TOGGLE_STRESS_CYCLES = 20


_SOFTAP_FAST_TOGGLE_POLL_INTERVAL_SECONDS = 0.1


def run_hotspot_toggle_stability_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    try:
        softap.toggle_hotspot_cycles(
            _SOFTAP_TOGGLE_STRESS_CYCLES,
            on_progress=lambda cycle, operation: _write_uncaptured_line(
                capsys, f"第{cycle}次{operation}WLAN热点开关正常"
            ),
        )
    except AssertionError as error:
        _write_uncaptured_line(capsys, str(error))
        raise

    _write_uncaptured_line(
        capsys,
        "设备热点执行开关操作"
        f"{_SOFTAP_TOGGLE_STRESS_CYCLES}次（次数可自行设置，默认20次），状态正常，"
        "后续请关注本机热点连接使用的具体功能是否正常",
    )


def run_hotspot_fast_toggle_stability_case(adb, capsys) -> None:
    softap = SoftAPControl(adb)
    softap.open_settings()
    try:
        softap.toggle_hotspot_cycles(
            _SOFTAP_TOGGLE_STRESS_CYCLES,
            on_progress=lambda cycle, operation: _write_uncaptured_line(
                capsys, f"第{cycle}次{operation}WLAN热点开关正常"
            ),
            poll_interval_seconds=_SOFTAP_FAST_TOGGLE_POLL_INTERVAL_SECONDS,
            cache_main_switch_bounds=True,
        )
    except AssertionError as error:
        _write_uncaptured_line(capsys, str(error))
        raise

    _write_uncaptured_line(
        capsys,
        f"设备热点执行{_SOFTAP_TOGGLE_STRESS_CYCLES}次快速开关，状态正常，"
        "后续请关注本机热点连接使用的具体功能是否正常",
    )
