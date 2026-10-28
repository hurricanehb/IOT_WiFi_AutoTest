"""204 / NetworkMonitor 检测场景。"""
from __future__ import annotations

import re
import time
from typing import Callable, List, Optional

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status

from core.libs.android.wifi_scenarios.lab_requirements import env_value
from core.libs.android.logcat_parsers import parse_logcat_event_offsets
from core.libs.android.wifi_control.connection_chk import assert_dual_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger

log = get_logger(__name__)

# NetworkMonitor 探测域名（各链路共用）
PROBE_HOSTS = [
    "www.qualcomm.cn",
    "connectivitycheck.gstatic.com",
    "connect.rom.miui.com",
    "www.google.com",
    "connectivitycheck.platform.hicloud.com",
]

DEFAULT_DUAL_WIFI_ENTRY_ID = "dual_wifi_24g_hyperwifi_us"

_CAPTIVE_SUCCESS_RE = re.compile(r"isSuccessful\(\)\s*=\s*(true|false)", re.IGNORECASE)
_CAPTIVE_DISABLED_RE = re.compile(
    r"isCaptivePortalDetectionEnabled:\s*false",
    re.IGNORECASE,
)
_CAPTIVE_ENABLED_RE = re.compile(
    r"isCaptivePortalDetectionEnabled:\s*true",
    re.IGNORECASE,
)
_PROBE_EVENT_HINTS = (
    "issuccessful",
    "captiveportal",
    "networkmonitor",
    "validation",
    "probe",
)
_NO_INTERNET_MARKERS = (
    "cannot provide internet",
    "no internet",
    "无法提供互联网",
    "不能提供互联网",
)
_BACKOFF_EXPECTED_SEC = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 600)


def _wan_env() -> str:
    return env_value("NETWORK_204_WAN", "up")


def _switch_env() -> str:
    return env_value("NETWORK_204_SWITCH", "on")


def require_wan_state(expected: str, summary: str) -> None:
    """校验实验室外网状态；外网异常用例需 NETWORK_204_WAN=down。"""
    want = (expected or "up").strip().lower()
    got = _wan_env()
    if got == want:
        return
    pytest.skip(
        f"{summary}: 需实验室外网={want!r}，当前 NETWORK_204_WAN={got!r}；"
        f"请设置 NETWORK_204_WAN={want}"
    )


def require_204_switch(expected: str, summary: str) -> None:
    """校验 204 开关状态；关闭场景需 NETWORK_204_SWITCH=off。"""
    want = (expected or "on").strip().lower()
    got = _switch_env()
    if got == want:
        return
    pytest.skip(
        f"{summary}: 需 204 开关={want!r}，当前 NETWORK_204_SWITCH={got!r}；"
        f"请在设置中切换后设置 NETWORK_204_SWITCH={want}"
    )


def capture_networkmonitor_log(adb: AdbHelper, duration_sec: float = 90.0) -> str:
    """清空 logcat，等待检测周期，抓取 NetworkMonitor 相关日志。"""
    adb.shell_line("logcat -c")
    time.sleep(2.0)
    wait = max(15.0, float(duration_sec))
    log.info("采集 NetworkMonitor 日志，等待 %.0fs…", wait)
    time.sleep(wait)
    _code, out, err = adb.shell_line(
        "logcat -d | grep -i -E 'networkmonitor|NetworkMonitor|CaptivePortal'"
    )
    text = ((out or "") + "\n" + (err or "")).strip()
    if not text:
        _code, out, err = adb.shell_line("logcat -d | grep -i captive")
        text = ((out or "") + "\n" + (err or "")).strip()
    return text


def parse_captive_success_flags(log_text: str) -> List[bool]:
    flags: List[bool] = []
    for match in _CAPTIVE_SUCCESS_RE.finditer(log_text or ""):
        flags.append(match.group(1).lower() == "true")
    return flags


def parse_probe_hosts_found(log_text: str, hosts: List[str]) -> List[str]:
    blob = (log_text or "").lower()
    found: List[str] = []
    for host in hosts:
        key = (host or "").strip().lower()
        if key and key in blob and key not in found:
            found.append(host)
    return found


def parse_probe_event_epochs(log_text: str) -> List[float]:
    """从 logcat 行提取探测事件时间戳（相对首次事件的秒数）。"""
    return parse_logcat_event_offsets(log_text, _PROBE_EVENT_HINTS)


def assert_exponential_probe_intervals(
    relative_times: List[float],
    *,
    summary: str,
    min_pairs: int = 3,
) -> None:
    """校验探测间隔近似 1/2/4/8s 指数退避。"""
    if len(relative_times) < min_pairs + 1:
        pytest.fail(
            f"{summary}: 探测事件不足（需要>={min_pairs + 1} 个时间点，"
            f"实际={len(relative_times)}）"
        )
    intervals = [
        relative_times[index + 1] - relative_times[index]
        for index in range(len(relative_times) - 1)
    ]
    print(f"[{summary}] 探测间隔(s): {[round(v, 2) for v in intervals[:8]]}")

    checks = min(min_pairs, len(intervals), len(_BACKOFF_EXPECTED_SEC))
    for index in range(checks):
        expected = _BACKOFF_EXPECTED_SEC[index]
        actual = intervals[index]
        low = expected * 0.4
        high = expected * 2.5
        if actual < low or actual > high:
            pytest.fail(
                f"{summary}: 第 {index + 1} 个探测间隔 {actual:.1f}s "
                f"不在预期 {expected}s 附近（允许 {low:.1f}~{high:.1f}s）"
            )
    log.info("%s: 指数退避间隔校验通过 intervals=%r", summary, intervals[:checks])


def _connect_dual_wifi(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
) -> None:
    region = (hyper_region or "US").strip().upper()
    entry_id = (dual_wifi_entry_id or DEFAULT_DUAL_WIFI_ENTRY_ID).strip() or None
    print(f"[{summary}] 双 WiFi 204 检测：region={region} entry={entry_id}")
    assert_dual_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        hyper_region=region,
        entry_id=entry_id,
        failure_label=summary,
    )


def _assert_wifi_status(
    run_shell_cmd: Callable[[str], str],
    *,
    expect_internet: bool,
    expect_no_internet: bool,
) -> str:
    status = run_shell_cmd("cmd wifi status")
    lower = status.lower()
    has_connected = "wifi is connected" in lower or "connected to" in lower
    has_no_inet = any(marker in lower for marker in _NO_INTERNET_MARKERS)

    if expect_internet:
        assert has_connected, f"cmd wifi status 未显示已连接：\n{status[:600]}"
    if expect_no_internet:
        if not has_no_inet:
            log.warning("cmd wifi status 未出现无外网文案（可能仅 UI 展示）")
    return status


def assert_network_204_log(
    log_text: str,
    *,
    probe_hosts: List[str],
    min_probe_hosts: int,
    expect_captive_success: bool,
    summary: str,
) -> None:
    if _CAPTIVE_DISABLED_RE.search(log_text or ""):
        pytest.fail(f"{summary}: 204 检测开关为关闭状态（isCaptivePortalDetectionEnabled: false）")

    found_hosts = parse_probe_hosts_found(log_text, probe_hosts)
    if len(found_hosts) < max(1, min_probe_hosts):
        excerpt = (log_text or "")[:1200]
        pytest.fail(
            f"{summary}: NetworkMonitor 日志中探测域名不足 "
            f"(需要>={min_probe_hosts}，实际={found_hosts!r})\n{excerpt}"
        )

    flags = parse_captive_success_flags(log_text)
    if not flags:
        excerpt = (log_text or "")[:1200]
        pytest.fail(
            f"{summary}: 未找到 isSuccessful() 字段\n{excerpt}"
        )

    if expect_captive_success:
        if not any(flags):
            pytest.fail(f"{summary}: 期望 isSuccessful()=true，实际={flags!r}")
    elif all(flags):
        pytest.fail(f"{summary}: 期望存在 isSuccessful()=false，实际全部为 true")

    log.info(
        "%s: 204 日志校验通过 hosts=%r captive=%r",
        summary,
        found_hosts,
        flags,
    )


def assert_network_204_disabled_log(
    log_text: str,
    *,
    probe_hosts: List[str],
    summary: str,
) -> None:
    if not _CAPTIVE_DISABLED_RE.search(log_text or ""):
        excerpt = (log_text or "")[:1200]
        pytest.fail(
            f"{summary}: 未找到 isCaptivePortalDetectionEnabled: false\n{excerpt}"
        )
    found_hosts = parse_probe_hosts_found(log_text, probe_hosts)
    if found_hosts:
        pytest.fail(f"{summary}: 204 关闭时不应出现探测域名，实际={found_hosts!r}")
    if parse_captive_success_flags(log_text):
        pytest.fail(f"{summary}: 204 关闭时不应出现 isSuccessful() 探测结果")
    log.info("%s: 204 关闭日志校验通过", summary)


@allure.step("执行网络 204 默认配置验证")
def run_204_default_config_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    *,
    wan: str = "up",
) -> None:
    """Vali_001：204 开关默认开启。"""
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    require_204_switch("on", summary)

    if not wifi.set_wifi_enabled(True):
        pytest.fail(f"{summary}: 无法打开 WiFi 射频")

    dumpsys = run_shell_cmd("dumpsys connectivity | grep -i captive")
    print(f"[{summary}] dumpsys connectivity captive 摘录：\n{dumpsys[:800]}")

    log_text = capture_networkmonitor_log(wifi.adb, duration_sec=30)
    if _CAPTIVE_DISABLED_RE.search(log_text):
        pytest.fail(f"{summary}: 默认配置下 204 检测不应为关闭状态")
    if _CAPTIVE_ENABLED_RE.search(log_text) or _CAPTIVE_SUCCESS_RE.search(log_text):
        log.info("%s: 默认 204 检测已启用", summary)
        return
    if "captive" in dumpsys.lower() and "false" not in dumpsys.lower():
        log.info("%s: dumpsys 显示 Captive 检测可用", summary)
        return
    pytest.fail(
        f"{summary}: 无法确认 204 默认开启，请检查 dumpsys/logcat 输出"
    )


@allure.step("执行双 WiFi 204 网络验证")
def run_dual_wifi_204_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    wan: str = "up",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    log_duration_sec: float = 90,
    min_probe_hosts: int = 2,
    expect_captive_success: bool = True,
    expect_connected_status: bool = False,
    expect_no_internet_status: bool = False,
    probe_hosts: Optional[List[str]] = None,
) -> None:
    """双 WiFi 204 独立性：连接双路 → 采集 logcat → 校验探测与 isSuccessful。"""
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    require_204_switch("on", summary)

    hosts = probe_hosts if probe_hosts is not None else PROBE_HOSTS

    _connect_dual_wifi(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper_region=hyper_region,
        dual_wifi_entry_id=dual_wifi_entry_id,
    )

    log_text = capture_networkmonitor_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] NetworkMonitor 日志摘录（前 1500 字符）：\n{log_text[:1500]}")

    assert_network_204_log(
        log_text,
        probe_hosts=hosts,
        min_probe_hosts=min_probe_hosts,
        expect_captive_success=expect_captive_success,
        summary=summary,
    )

    status = _assert_wifi_status(
        run_shell_cmd,
        expect_internet=expect_connected_status,
        expect_no_internet=expect_no_internet_status,
    )
    print(f"[{summary}] cmd wifi status:\n{status}")


@allure.step("执行双 WiFi 204 周期验证")
def run_dual_wifi_204_period_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    wan: str = "down",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    log_duration_sec: float = 150,
    min_backoff_pairs: int = 3,
) -> None:
    """双 WiFi 204 检测周期：外网异常时校验 1/2/4/8s 指数退避。"""
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    require_204_switch("on", summary)

    _connect_dual_wifi(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper_region=hyper_region,
        dual_wifi_entry_id=dual_wifi_entry_id,
    )

    log_text = capture_networkmonitor_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] NetworkMonitor 周期日志摘录（前 2000 字符）：\n{log_text[:2000]}")

    relative_times = parse_probe_event_epochs(log_text)
    assert_exponential_probe_intervals(
        relative_times,
        summary=summary,
        min_pairs=min_backoff_pairs,
    )


@allure.step("执行双 WiFi 204 禁用验证")
def run_dual_wifi_204_disabled_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    wan: str = "up",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    log_duration_sec: float = 60,
    expect_connected_status: bool = True,
    probe_hosts: Optional[List[str]] = None,
) -> None:
    """204 开关关闭：不应发起 DNS 探测。"""
    attach_wifi_status(summary, run_shell_cmd)
    require_wan_state(wan, summary)
    require_204_switch("off", summary)

    hosts = probe_hosts if probe_hosts is not None else PROBE_HOSTS

    _connect_dual_wifi(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper_region=hyper_region,
        dual_wifi_entry_id=dual_wifi_entry_id,
    )

    log_text = capture_networkmonitor_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] NetworkMonitor 日志摘录（前 1500 字符）：\n{log_text[:1500]}")

    assert_network_204_disabled_log(
        log_text,
        probe_hosts=hosts,
        summary=summary,
    )

    status = _assert_wifi_status(
        run_shell_cmd,
        expect_internet=expect_connected_status,
        expect_no_internet=False,
    )
    print(f"[{summary}] cmd wifi status:\n{status}")
