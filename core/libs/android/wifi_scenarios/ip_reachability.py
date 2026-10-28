"""IpReachabilityMonitor 网关可达性检测场景。"""
from __future__ import annotations

import re
import time
from typing import Callable, List, Optional, Set

import allure
import pytest

from core.libs.android.wifi_scenarios.lab_requirements import (
    env_value as _env,
    require_env_value,
    require_lab_flag,
)
from core.libs.android.logcat_parsers import parse_logcat_event_offsets
from core.libs.android.wifi_control.connection_chk import assert_dual_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger

log = get_logger(__name__)

DEFAULT_DUAL_WIFI_ENTRY_ID = "dual_wifi_24g_hyperwifi_us"

_MONITOR_RE = re.compile(r"IpReachabilityMonitor", re.IGNORECASE)
_IF_NUM_RE = re.compile(r"\bif=(\d+)\b")
_IFACE_NAME_RE = re.compile(r"\b(wlan\d+|bond\d+)\b", re.IGNORECASE)
_NUD_FAILED_RE = re.compile(r"NUD_FAILED", re.IGNORECASE)
_LOST_PROV_RE = re.compile(r"LOST_PROVISIONING", re.IGNORECASE)
_IPV6_NEIGH_RE = re.compile(
    r"RTM_NEWNEIGH.*?(?:[0-9a-f]{0,4}:){2,}[0-9a-f:]+",
    re.IGNORECASE,
)
_EVENT_HINTS = (
    "ipreachabilitymonitor",
    "rtm_newneigh",
    "neighbor",
    "nud_",
    "lost_provisioning",
)
_NS_INTERVAL_MS = 750
_PERIOD_PROBE_COUNT = 10
_ROAM_PROBE_COUNT = 5


def require_ip_mode(expected: str, summary: str) -> None:
    """静态 IP 场景需 IPREACH_IP_MODE=static，且 DUT 已在设置中配好静态地址。"""
    want = (expected or "dhcp").strip().lower()
    got = _env("IPREACH_IP_MODE", "dhcp")
    if got == want:
        return
    pytest.skip(
        f"{summary}: 需 IP 模式={want!r}，当前 IPREACH_IP_MODE={got!r}；"
        f"请在 DUT 设置中配置后设置 IPREACH_IP_MODE={want}"
    )


def require_gateway_state(expected: str, summary: str) -> None:
    """不可达/恢复场景：IPREACH_GATEWAY=reachable|unreachable。"""
    want = (expected or "reachable").strip().lower()
    got = _env("IPREACH_GATEWAY", "reachable")
    if got == want:
        return
    pytest.skip(
        f"{summary}: 需网关状态={want!r}，当前 IPREACH_GATEWAY={got!r}；"
        f"请配置 Router/miniAP 后设置 IPREACH_GATEWAY={want}"
    )


def capture_ipreach_log(adb: AdbHelper, duration_sec: float = 45.0) -> str:
    """清空 logcat，等待检测，抓取 IpReachabilityMonitor 日志。"""
    adb.shell_line("logcat -c")
    time.sleep(2.0)
    wait = max(10.0, float(duration_sec))
    log.info("采集 IpReachabilityMonitor 日志，等待 %.0fs…", wait)
    time.sleep(wait)
    _code, out, err = adb.shell_line(
        "logcat -d | grep -i -E 'IpReachabilityMonitor|IpReachable'"
    )
    text = ((out or "") + "\n" + (err or "")).strip()
    if not text:
        _code, out, err = adb.shell_line("logcat -d | grep -i newneigh")
        text = ((out or "") + "\n" + (err or "")).strip()
    return text


def parse_monitor_iface_keys(log_text: str) -> Set[str]:
    """从日志提取接口标识（if=N 或 wlan/bond 名）。"""
    keys: Set[str] = set()
    for line in (log_text or "").splitlines():
        if not _MONITOR_RE.search(line) and "newneigh" not in line.lower():
            continue
        for match in _IF_NUM_RE.finditer(line):
            keys.add(f"if={match.group(1)}")
        for match in _IFACE_NAME_RE.finditer(line):
            keys.add(match.group(1).lower())
    return keys


def parse_ipv6_neighbor_events(log_text: str) -> int:
    return len(_IPV6_NEIGH_RE.findall(log_text or ""))


def has_monitor_failure(log_text: str) -> bool:
    blob = log_text or ""
    return bool(_NUD_FAILED_RE.search(blob) or _LOST_PROV_RE.search(blob))


def parse_neighbor_event_epochs(log_text: str) -> List[float]:
    """提取邻居探测事件时间戳（相对首次事件的秒数）。"""
    return parse_logcat_event_offsets(log_text, _EVENT_HINTS)


def assert_dual_independent_monitor(
    log_text: str,
    *,
    summary: str,
    min_ifaces: int = 2,
    min_events: int = 2,
) -> None:
    if not _MONITOR_RE.search(log_text or ""):
        excerpt = (log_text or "")[:1200]
        pytest.fail(f"{summary}: 未找到 IpReachabilityMonitor 日志\n{excerpt}")

    ifaces = parse_monitor_iface_keys(log_text)
    events = len(_MONITOR_RE.findall(log_text or ""))
    print(f"[{summary}] 监控接口={sorted(ifaces)!r} 事件数={events}")

    if len(ifaces) < min_ifaces and events < min_events + 1:
        excerpt = (log_text or "")[:1500]
        pytest.fail(
            f"{summary}: 双 WiFi 未分别触发检测 "
            f"(接口>={min_ifaces} 或事件>={min_events + 1}，"
            f"实际接口={len(ifaces)} 事件={events})\n{excerpt}"
        )
    log.info("%s: 双路独立检测校验通过 ifaces=%r", summary, ifaces)


def assert_monitor_outcome(
    log_text: str,
    *,
    summary: str,
    expect_failure: bool,
) -> None:
    failed = has_monitor_failure(log_text)
    if expect_failure:
        if not failed:
            excerpt = (log_text or "")[:1500]
            pytest.fail(
                f"{summary}: 期望 NUD_FAILED/LOST_PROVISIONING，日志中未找到\n{excerpt}"
            )
    elif failed:
        pytest.fail(f"{summary}: 期望网关可达，但日志含失败标记")
    log.info("%s: 可达性结果校验通过 expect_failure=%s", summary, expect_failure)


def assert_ns_probe_intervals(
    relative_times: List[float],
    *,
    summary: str,
    max_probes: int,
    interval_ms: int = _NS_INTERVAL_MS,
    tolerance: float = 0.45,
) -> None:
    """校验 NS 探测间隔约 750ms。"""
    if len(relative_times) < 3:
        pytest.fail(
            f"{summary}: 邻居探测事件不足（需要>=3，实际={len(relative_times)}）"
        )
    intervals = [
        relative_times[i + 1] - relative_times[i]
        for i in range(len(relative_times) - 1)
    ]
    expected = interval_ms / 1000.0
    print(f"[{summary}] NS 探测间隔(s): {[round(v, 3) for v in intervals[:max_probes]]}")

    checks = min(max_probes - 1, len(intervals))
    for index in range(checks):
        actual = intervals[index]
        low = expected * (1.0 - tolerance)
        high = expected * (1.0 + tolerance) * 2.5
        if actual < low or actual > high:
            pytest.fail(
                f"{summary}: 第 {index + 1} 个 NS 间隔 {actual:.3f}s "
                f"不在 {expected}s 附近（允许 {low:.3f}~{high:.3f}s）"
            )
    log.info("%s: NS 间隔校验通过 checks=%d", summary, checks)


def _connect_dual_wifi(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
) -> None:
    entry_id = (dual_wifi_entry_id or DEFAULT_DUAL_WIFI_ENTRY_ID).strip() or None
    print(f"[{summary}] 双 WiFi 网关可达检测：region={hyper_region}")
    assert_dual_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        hyper_region=hyper_region,
        entry_id=entry_id,
        failure_label=summary,
    )


@allure.step("执行双 WiFi 网关可达性验证")
def run_dual_wifi_ipreach_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    ip_mode: str = "dhcp",
    gateway: str = "reachable",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    log_duration_sec: float = 45,
    min_ifaces: int = 2,
    expect_failure: bool = False,
) -> None:
    """双 WiFi 连接 → 采集 IpReachabilityMonitor → 校验独立检测与结果。"""
    require_ip_mode(ip_mode, summary)
    require_gateway_state(gateway, summary)

    _connect_dual_wifi(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper_region=hyper_region,
        dual_wifi_entry_id=dual_wifi_entry_id,
    )

    attach_wifi_status(summary, run_shell_cmd)

    log_text = capture_ipreach_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] IpReachabilityMonitor 摘录（前 2000 字符）：\n{log_text[:2000]}")

    assert_dual_independent_monitor(
        log_text, summary=summary, min_ifaces=min_ifaces
    )
    assert_monitor_outcome(
        log_text, summary=summary, expect_failure=expect_failure
    )


def run_dual_wifi_ipreach_ipv6_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    ip_mode: str = "dhcp",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    log_duration_sec: float = 45,
    min_ipv6_events: int = 1,
) -> None:
    """Vali_002：DHCP 双 WiFi，日志中应出现 IPv6 邻居探测。"""
    require_ip_mode(ip_mode, summary)
    require_gateway_state("reachable", summary)

    _connect_dual_wifi(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        hyper_region=hyper_region,
        dual_wifi_entry_id=dual_wifi_entry_id,
    )

    log_text = capture_ipreach_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] IpReachabilityMonitor IPv6 摘录（前 2000 字符）：\n{log_text[:2000]}")

    assert_dual_independent_monitor(log_text, summary=summary)
    ipv6_count = parse_ipv6_neighbor_events(log_text)
    if ipv6_count < min_ipv6_events:
        log.warning(
            "%s: 未明确解析到 IPv6 RTM_NEWNEIGH（count=%d），"
            "若实验室无 IPv6 可忽略",
            summary,
            ipv6_count,
        )
    log.info("%s: IPv6 邻居事件 count=%d", summary, ipv6_count)


def run_ipreach_period_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    ip_mode: str = "static",
    gateway: str = "unreachable",
    log_duration_sec: float = 12,
    max_probes: int = _PERIOD_PROBE_COUNT,
) -> None:
    """Vali_004：错误静态网关，约 7.5s 内 10 次 NS 探测（750ms 间隔）。"""
    require_ip_mode(ip_mode, summary)
    require_gateway_state(gateway, summary)

    _connect_dual_wifi(summary, run_shell_cmd, wifi, wifi_yaml)

    log_text = capture_ipreach_log(wifi.adb, duration_sec=log_duration_sec)
    print(f"[{summary}] 周期检测日志摘录（前 2500 字符）：\n{log_text[:2500]}")

    relative_times = parse_neighbor_event_epochs(log_text)
    assert_ns_probe_intervals(
        relative_times,
        summary=summary,
        max_probes=max_probes,
    )
    assert_monitor_outcome(log_text, summary=summary, expect_failure=True)


def run_ipreach_recovery_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    ip_mode: str = "static",
) -> None:
    """Excp_002：先不可达后恢复（两阶段，靠环境变量切换）。"""
    phase = _env("IPREACH_GATEWAY_PHASE", "fail")
    if phase == "fail":
        require_ip_mode(ip_mode, summary)
        require_gateway_state("unreachable", summary)
        _connect_dual_wifi(summary, run_shell_cmd, wifi, wifi_yaml)
        log_text = capture_ipreach_log(wifi.adb, duration_sec=12)
        print(f"[{summary}] 阶段1（不可达）日志摘录：\n{log_text[:2000]}")
        assert_dual_independent_monitor(log_text, summary=summary)
        assert_monitor_outcome(log_text, summary=summary, expect_failure=True)
        pytest.skip(
            f"{summary}: 阶段1 完成；请 Router 改配 DHCP 192.168.2.1/24 后 "
            f"设置 IPREACH_GATEWAY=reachable IPREACH_GATEWAY_PHASE=recover 重跑"
        )

    require_gateway_state("reachable", summary)
    _connect_dual_wifi(summary, run_shell_cmd, wifi, wifi_yaml)
    log_text = capture_ipreach_log(wifi.adb, duration_sec=45)
    print(f"[{summary}] 阶段2（恢复）日志摘录：\n{log_text[:2000]}")
    assert_dual_independent_monitor(log_text, summary=summary)
    assert_monitor_outcome(log_text, summary=summary, expect_failure=False)


def run_ipreach_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    """Int_002：不共网关 + 主网络断开后备升主，重新触发检测。"""
    require_env_value(
        "IPREACH_SHARED_GATEWAY",
        "0",
        summary,
        hint="AP 与 miniAP 须配置不同网关",
    )

    _connect_dual_wifi(summary, run_shell_cmd, wifi, wifi_yaml)
    log_before = capture_ipreach_log(wifi.adb, duration_sec=30)
    assert_dual_independent_monitor(log_before, summary=summary)

    if _env("IPREACH_PRIMARY_WIFI_DOWN") not in ("1", "true", "yes", "on"):
        pytest.skip(
            f"{summary}: 初始双路检测已通过；断开主 WiFi 后设置 "
            f"IPREACH_PRIMARY_WIFI_DOWN=1 重跑以校验 HyperWiFi 升主后重新检测"
        )

    print(f"[{summary}] 断开主 WiFi（cmd wifi disconnect）")
    run_shell_cmd("cmd wifi disconnect")
    time.sleep(5.0)
    log_after = capture_ipreach_log(wifi.adb, duration_sec=30)
    print(f"[{summary}] 主网络断开后日志摘录：\n{log_after[:2000]}")
    if not _MONITOR_RE.search(log_after):
        pytest.fail(f"{summary}: 主网络断开后未观察到新的 IpReachabilityMonitor 事件")
    log.info("%s:  failover 后检测事件已出现", summary)


def run_ipreach_roam_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    roam: bool = False,
) -> None:
    """Int_003/004：屏蔽箱衰减器切换或漫游（需人工操作后采集日志）。"""
    require_lab_flag(
        "IPREACH_ROAM_LAB",
        summary,
        hint="需屏蔽箱 AP1/AP2、miniAP1/miniAP2 与衰减器",
    )
    max_probes = _ROAM_PROBE_COUNT if roam else _PERIOD_PROBE_COUNT
    hint = "漫游" if roam else "切换 AP"

    if _env("IPREACH_ROAM_DONE") not in ("1", "true", "yes", "on"):
        pytest.skip(
            f"{summary}: 请人工调节衰减器完成{hint}后设置 "
            f"IPREACH_ROAM_DONE=1 重跑以采集日志"
        )

    log_text = capture_ipreach_log(wifi.adb, duration_sec=15)
    print(f"[{summary}] {hint}后日志摘录：\n{log_text[:2000]}")
    if not _MONITOR_RE.search(log_text):
        pytest.fail(f"{summary}: {hint}后未找到 IpReachabilityMonitor 日志")

    relative_times = parse_neighbor_event_epochs(log_text)
    if len(relative_times) >= 3:
        assert_ns_probe_intervals(
            relative_times,
            summary=summary,
            max_probes=max_probes,
        )


def run_ipreach_ip_mode_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    """Int_005：静态/DHCP 切换后重新检测（需在设置中切换 IP 模式）。"""
    mode = _env("IPREACH_IP_MODE", "")
    if mode not in ("static", "dhcp"):
        pytest.skip(
            f"{summary}: 请在 DUT 设置中切换 IP 模式后设置 "
            f"IPREACH_IP_MODE=static 或 dhcp 分别重跑"
        )

    _connect_dual_wifi(summary, run_shell_cmd, wifi, wifi_yaml)
    log_text = capture_ipreach_log(wifi.adb, duration_sec=30)
    print(f"[{summary}] IP 模式={mode} 日志摘录：\n{log_text[:2000]}")
    assert_dual_independent_monitor(log_text, summary=summary)
