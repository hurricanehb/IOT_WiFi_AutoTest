"""Country-code scenario runners."""
from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple, cast

import allure
import pytest

from core.testdata_loader import get_wifi_list_entry
from core.libs.android.wifi_control.connection_chk import (
    assert_dual_wifi_connected,
    assert_wifi_connected,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.ip_configuration import (
    assert_gateway_reachable,
    wait_for_wifi_ipv4,
)
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.utils.adb_helper import AdbDeviceUnavailableError
from core.utils.device_log_export import export_device_packlogs
from core.utils.log_handler import get_logger

log = get_logger(__name__)

_SIMULATED_COUNTRY_CODES = ("EU", "EUS", "US")
_HALOW_FAIL_MARKERS = (
    "FAIL",
    "INVALID ARGUMENT",
    "RECEIVE ERROR",
    "NOT FOUND",
    "NO SUCH FILE",
)


def require_cli_app(run_shell_cmd: Callable[[str], str]) -> None:
    probe = run_shell_cmd("cli_app show config")
    if "not found" in probe.lower() or "no such file" in probe.lower():
        pytest.skip("cli_app 不可用")


@allure.step("模拟电话国家码")
def simulate_telephony_country_code(
    run_shell_cmd: Callable[[str], str],
    country_code: str,
    *,
    case_id: str | None = None,
    expected_country_code: str | None = None,
) -> None:
    """模拟电话国家码，并确认 WiFi 服务已采用该值。"""
    if case_id:
        attach_wifi_status(case_id, run_shell_cmd)
    _simulate_country_code_source(
        run_shell_cmd,
        command="force-telephony_country-code",
        country_code=country_code,
        source_name="电话国家码",
        expected_country_code=expected_country_code,
    )


@allure.step("模拟远程配置国家码")
def simulate_cloud_country_code(
    run_shell_cmd: Callable[[str], str],
    country_code: str,
    *,
    case_id: str | None = None,
) -> None:
    """模拟远程配置国家码，并确认 WiFi 服务已采用该值。"""
    if case_id:
        attach_wifi_status(case_id, run_shell_cmd)
    code = (country_code or "").strip().upper()
    if code in ("EU", "EUS"):
        _simulate_country_code_source(
            run_shell_cmd,
            command="force-country-code-sunmi",
            country_code="EU",
            source_name="远程配置国家码",
        )
        set_eus_duty_cycle(run_shell_cmd, duty_cycle_off=code == "EUS")
        return
    _simulate_country_code_source(
        run_shell_cmd,
        command="force-country-code-sunmi",
        country_code=code,
        source_name="远程配置国家码",
    )


@allure.step("模拟远程国家码下发序列")
def simulate_cloud_country_code_sequence(
    run_shell_cmd: Callable[[str], str],
    country_codes: List[str],
    *,
    case_id: str | None = None,
) -> None:
    """按顺序模拟多次远程国家码下发，并逐次验证生效结果。"""
    if case_id:
        attach_wifi_status(case_id, run_shell_cmd)
    if not country_codes:
        pytest.fail("远程配置国家码序列不能为空")
    for country_code in country_codes:
        simulate_cloud_country_code(run_shell_cmd, country_code)


@allure.step("验证云端国家码优先于手动 shell 配置")
def assert_cloud_country_code_precedes_shell(
    run_shell_cmd: Callable[[str], str],
    *,
    case_id: str | None = None,
) -> None:
    if case_id:
        attach_wifi_status(case_id, run_shell_cmd)
    _simulate_country_code_source(
        run_shell_cmd,
        command="force-country-code-sunmi",
        country_code="EU",
        source_name="远程配置国家码",
    )

    result = run_shell_cmd("cmd wifi force-country-code enabled US")
    if any(marker in (result or "").upper() for marker in _HALOW_FAIL_MARKERS):
        pytest.fail(f"手动配置传统 WiFi 国家码失败：{result!r}")
    wifi_code = run_shell_cmd("cmd wifi get-country-code")
    if "US" not in (wifi_code or "").upper():
        pytest.fail(f"传统 WiFi 国家码应切换为 US，实际={wifi_code!r}")

    halow_code = run_shell_cmd("cli_app show config | grep -i country")
    if not re.search(r"\bEU\b", (halow_code or "").upper()):
        pytest.fail(f"Halow 国家码应保持云端 EU 配置，实际={halow_code!r}")

    eus_result = run_shell_cmd("cmd wifi set-eus 1")
    rejection = (eus_result or "").lower()
    if "remotely configured" not in rejection and "remote eus" not in rejection:
        pytest.fail(f"远程配置存在时 set-eus 1 应被拒绝，实际={eus_result!r}")


def _simulate_country_code_source(
    run_shell_cmd: Callable[[str], str],
    *,
    command: str,
    country_code: str,
    source_name: str,
    expected_country_code: str | None = None,
) -> None:
    code = (country_code or "").strip().upper()
    if code not in _SIMULATED_COUNTRY_CODES:
        pytest.fail(
            f"{source_name}仅支持 {_SIMULATED_COUNTRY_CODES!r}，实际={country_code!r}"
        )
    result = run_shell_cmd(f"cmd wifi {command} enabled {code}")
    if any(marker in (result or "").upper() for marker in _HALOW_FAIL_MARKERS):
        pytest.fail(f"设置{source_name}失败：{result!r}")
    expected = (expected_country_code or code).strip().upper()
    actual = run_shell_cmd("cmd wifi get-country-code")
    assert expected in (actual or "").upper(), (
        f"{source_name}下发后国家码应为 {expected!r}，实际={actual!r}"
    )


def set_eus_duty_cycle(
    run_shell_cmd: Callable[[str], str], duty_cycle_off: bool
) -> None:
    """设置 EUS：1 表示关闭占空比，0 表示开启占空比。"""
    expected = "1" if duty_cycle_off else "0"
    result = run_shell_cmd(f"cmd wifi set-eus {expected}")
    print(f"cmd wifi set-eus {expected}:\n{result}")
    if any(marker in (result or "").upper() for marker in _HALOW_FAIL_MARKERS):
        pytest.fail(f"设置 EUS 占空比失败：{result!r}")
    assert_eus_duty_cycle(run_shell_cmd, duty_cycle_off)


def assert_eus_duty_cycle(
    run_shell_cmd: Callable[[str], str],
    duty_cycle_off: bool,
    timeout: float = 10.0,
) -> None:
    """通过 get-eus 与 cli_app show duty 回读校验 EUS 占空比。"""
    expected = "1" if duty_cycle_off else "0"
    actual = run_shell_cmd("cmd wifi get-eus")
    print(f"cmd wifi get-eus:\n{actual}")
    if not re.search(rf"(?<!\d){expected}(?!\d)", actual or ""):
        pytest.fail(f"EUS 占空比应为 {expected}，实际={actual!r}")
    deadline = time.monotonic() + timeout
    while True:
        duty = run_shell_cmd("cli_app show duty")
        print(f"cli_app show duty:\n{duty}")
        is_off = "off" in (duty or "").lower()
        if is_off == duty_cycle_off:
            return
        if time.monotonic() >= deadline:
            expected_state = "off" if duty_cycle_off else "on"
            pytest.fail(f"Duty cycle 应为 {expected_state}，实际={duty!r}")
        time.sleep(1.0)


def _wait_for_wifi_country_code(
    run_shell_cmd: Callable[[str], str],
    *,
    expected: str,
    timeout: float,
) -> None:
    deadline = time.monotonic() + max(0.0, timeout)
    actual = ""
    while True:
        actual = run_shell_cmd("cmd wifi get-country-code")
        if re.search(rf"(?<![A-Z]){re.escape(expected)}(?![A-Z])", (actual or "").upper()):
            return
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            pytest.fail(
                f"WiFi 国家码未在 {timeout:.1f}s 内收敛到 {expected!r}，实际={actual!r}"
            )
        time.sleep(min(1.0, remaining))


def force_country_and_restart_wifi(
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    country_code: str,
    wait_after_enable: float,
    country_code_timeout: float = 20.0,
) -> None:
    run_shell_cmd(f"cmd wifi force-country-code enabled {country_code}")
    expected = (country_code or "").strip().upper()
    _wait_for_wifi_country_code(
        run_shell_cmd, expected=expected, timeout=country_code_timeout
    )
    wifi.set_wifi_enabled(False)
    time.sleep(1.0)
    wifi.set_wifi_enabled(True)
    time.sleep(wait_after_enable)
    _wait_for_wifi_country_code(
        run_shell_cmd, expected=expected, timeout=country_code_timeout
    )


def _emit_stress_progress(message: str) -> None:
    stream = sys.__stdout__
    if stream is not None:
        try:
            print(message, file=stream, flush=True)
            return
        except (OSError, ValueError):
            pass
    print(message, file=sys.stdout, flush=True)


def _read_halow_country_and_duty(
    run_shell_cmd: Callable[[str], str],
) -> Tuple[str, str]:
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    duty_info = run_shell_cmd("cli_app show duty")
    return country_info, duty_info


def _halow_output_ready(country_info: str, duty_info: str) -> bool:
    country = (country_info or "").strip()
    duty = (duty_info or "").strip()
    if not country or not duty:
        return False
    blob = f"{country}\n{duty}".upper()
    return not any(marker in blob for marker in _HALOW_FAIL_MARKERS) and (
        "COUNTRY" in country.upper() and "DUTY" in duty.upper()
    )


def _wait_halow_country_and_duty(
    run_shell_cmd: Callable[[str], str],
    *,
    expected_halow: str,
    timeout: float = 30.0,
    poll_interval: float = 2.0,
) -> Tuple[str, str]:
    """国家码切换后轮询，直至 Halow 国家码和占空比均收敛到期望状态。"""
    deadline = time.monotonic() + max(0.0, timeout)
    poll_interval = max(0.5, poll_interval)
    expected = (expected_halow or "").strip().upper()
    last = ("", "")

    while time.monotonic() <= deadline:
        last = _read_halow_country_and_duty(run_shell_cmd)
        country_info, duty_info = last
        country_matches = bool(re.search(rf"\b{re.escape(expected)}\b", country_info.upper()))
        duty_matches = "off" in duty_info.lower()
        if _halow_output_ready(*last) and country_matches and duty_matches:
            return last
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        sleep_sec = min(poll_interval, remaining)
        log.info(
            "Halow 状态未收敛到 country=%s/duty=off，%.1fs 后重试：country=%r duty=%r",
            expected,
            sleep_sec,
            country_info,
            duty_info,
        )
        time.sleep(sleep_sec)

    return last


def assert_country_and_duty(
    run_shell_cmd: Callable[[str], str],
    *,
    country_code: str,
    expected_halow: str,
    halow_ready_timeout: float = 30.0,
) -> None:
    wifi_code = run_shell_cmd("cmd wifi get-country-code")
    country_info, duty_info = _wait_halow_country_and_duty(
        run_shell_cmd,
        expected_halow=expected_halow,
        timeout=halow_ready_timeout,
    )
    log.info("[%s] WiFi 国家码输出：\n%s", country_code, wifi_code)
    log.info("[%s] Halow 国家码：\n%s", country_code, country_info)
    log.info("[%s] 占空比：\n%s", country_code, duty_info)
    assert country_code in (wifi_code or "").upper(), (
        f"WiFi 国家码应含 {country_code!r}，实际={wifi_code!r}"
    )
    assert expected_halow in (country_info or "").upper(), (
        f"Halow 国家码应为 {expected_halow}，country={country_info!r}"
    )
    assert "off" in (duty_info or "").lower() and "duty" in (duty_info or "").lower(), (
        f"占空比应为 off，duty={duty_info!r}"
    )


def run_adapt_country_mapping(
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    country_code: str,
    *,
    expected_halow: str,
) -> None:
    """Run the shared country-code mapping verification flow."""
    code = (country_code or "").strip().upper()
    if not re.fullmatch(r"[A-Z]{2}", code):
        pytest.fail(f"非法国家码: {country_code!r}")
    halow = (expected_halow or "").strip().upper()
    if halow not in ("US", "EU"):
        pytest.fail(f"expected_halow 须为 US 或 EU，实际={expected_halow!r}")
    require_cli_app(run_shell_cmd)
    wifi.set_wifi_enabled(True)
    force_country_and_restart_wifi(
        run_shell_cmd, wifi, country_code=code, wait_after_enable=1.0
    )
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, allow_any_configured=True)
    assert_country_and_duty(
        run_shell_cmd, country_code=code, expected_halow=halow
    )


@dataclass
class CountryCodeStressResult:
    """国家码压测的完整执行结果。"""

    total_cycles: int
    passed_cycles: int = 0
    failed_cycles: int = 0
    failures: List[str] = field(default_factory=list)

    def summary(self) -> str:
        details = "; ".join(self.failures) if self.failures else "无"
        return (
            f"总轮次={self.total_cycles}, 成功={self.passed_cycles}, "
            f"失败={self.failed_cycles}, 失败详情={details}"
        )


def run_country_table_case(
    country_code: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    capability: str,
    expected_halow: str,
) -> None:
    """按 DUT 能力执行表驱动的国家码和联网校验。"""
    code = (country_code or "").strip().upper()
    halow = (expected_halow or "").strip().upper()
    dut_capability = (capability or "").strip().lower()
    if dut_capability not in ("wifi", "hyperwifi", "dualwifi"):
        pytest.fail(f"不支持的 DUT_WIFI_CAPABILITY={capability!r}")

    if dut_capability != "wifi":
        require_cli_app(run_shell_cmd)
    force_country_and_restart_wifi(
        run_shell_cmd, wifi, country_code=code, wait_after_enable=0.0
    )

    if dut_capability == "dualwifi":
        assert_dual_wifi_connected(
            wifi, wifi_yaml, run_shell_cmd, hyper_region=halow
        )
    else:
        entry_id = (
            "wifi_ap_ssid_default"
            if dut_capability == "wifi"
            else f"hyperwifi_{halow.lower()}"
        )
        entry = get_wifi_list_entry(wifi_yaml, entry_id=entry_id)
        if not entry:
            pytest.skip(f"wifi_ssid.yaml 缺少国家码遍历配置 id={entry_id!r}")
        assert_wifi_connected(
            wifi,
            wifi_yaml,
            run_shell_cmd,
            entry=cast(WiFiEntry, entry),
            allow_any_configured=False,
        )

    ipv4 = wait_for_wifi_ipv4(run_shell_cmd)
    assert_gateway_reachable(run_shell_cmd, ipv4.gateway)

    if dut_capability == "wifi":
        _wait_for_wifi_country_code(run_shell_cmd, expected=code, timeout=20.0)
    else:
        assert_country_and_duty(
            run_shell_cmd, country_code=code, expected_halow=halow
        )


def run_country_code_switch_stress(
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    cycles: int = 1000,
    us_code: str = "US",
    eu_code: str = "DE",
    wait_after_enable: float = 5.0,
    halow_ready_timeout: float = 30.0,
    log_every: int = 50,
    max_failure_log_exports: int = 3,
    progress_callback: Optional[Callable[[str], None]] = None,
) -> CountryCodeStressResult:
    """交替切换 US/EU 国家码，记录单轮失败并继续执行。"""
    require_cli_app(run_shell_cmd)
    total = max(1, int(cycles))
    log_every = max(1, int(log_every))
    max_failure_log_exports = max(0, int(max_failure_log_exports))
    us = (us_code or "US").strip().upper()
    eu = (eu_code or "DE").strip().upper()
    if not re.fullmatch(r"[A-Z]{2}", us) or not re.fullmatch(r"[A-Z]{2}", eu):
        pytest.fail(f"非法国家码: us={us_code!r}, eu={eu_code!r}")

    result = CountryCodeStressResult(total_cycles=total)
    exported_failure_logs = 0
    wifi.set_wifi_enabled(True)
    for index in range(total):
        code, expected_halow = ((us, "US"), (eu, "EU"))[index % 2]
        cycle = index + 1
        start_message = (
            f"[Ccode Stress] {cycle}/{total} 开始："
            f"WiFi 国家码={code}，期望 Halow={expected_halow}"
        )
        _emit_stress_progress(start_message)
        if progress_callback:
            progress_callback(start_message)
        try:
            force_country_and_restart_wifi(
                run_shell_cmd,
                wifi,
                country_code=code,
                wait_after_enable=wait_after_enable,
            )
            assert_country_and_duty(
                run_shell_cmd,
                country_code=code,
                expected_halow=expected_halow,
                halow_ready_timeout=halow_ready_timeout,
            )
            assert_dual_wifi_connected(
                wifi,
                wifi_yaml,
                run_shell_cmd,
                hyper_region=expected_halow,
                failure_label=f"ccode_stress_{cycle}_{code}",
                export_logs_on_fail=False,
            )
        except AdbDeviceUnavailableError as exc:
            summary = result.summary()
            message = f"{exc}; 国家码压测已中止，截止统计：{summary}"
            log.error(message)
            _emit_stress_progress(f"[Ccode Stress] 硬件不可用：{message}")
            if progress_callback:
                progress_callback(f"[Ccode Stress] 硬件不可用：{message}")
            raise AdbDeviceUnavailableError(message, statistics=summary) from exc
        except BaseException as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit, pytest.skip.Exception)):
                raise
            result.failed_cycles += 1
            message = " ".join(str(exc).split())[:500]
            detail = f"轮次={cycle}, 国家码={code}, 原因={message or type(exc).__name__}"
            result.failures.append(detail)
            log.error("国家码压测单轮失败，继续下一轮：%s", detail)
            status = (
                f"[Ccode Stress] {cycle}/{total} 失败：{message or type(exc).__name__}；"
                f"累计成功={result.passed_cycles}，失败={result.failed_cycles}"
            )
            _emit_stress_progress(status)
            if progress_callback:
                progress_callback(status)
            if exported_failure_logs < max_failure_log_exports:
                exported_failure_logs += 1
                try:
                    export_device_packlogs(
                        wifi.adb,
                        reason="country_code_stress_cycle_failed",
                        label=f"ccode_stress_{cycle}_{code}",
                    )
                except Exception as export_exc:
                    export_message = (
                        f"[Ccode Stress] {cycle}/{total} 失败日志导出异常，继续下一轮："
                        f"{type(export_exc).__name__}: {export_exc}"
                    )
                    log.exception(export_message)
                    _emit_stress_progress(export_message)
                    if progress_callback:
                        progress_callback(export_message)
        else:
            result.passed_cycles += 1
            status = (
                f"[Ccode Stress] {cycle}/{total} 成功；"
                f"累计成功={result.passed_cycles}，失败={result.failed_cycles}"
            )
            _emit_stress_progress(status)
            if progress_callback:
                progress_callback(status)
        if cycle % log_every == 0 or cycle == total:
            log.info("国家码压测进度 %d/%d：%s", cycle, total, result.summary())
    complete_message = f"[Ccode Stress] 完成：{result.summary()}"
    _emit_stress_progress(complete_message)
    if progress_callback:
        progress_callback(complete_message)
    return result
