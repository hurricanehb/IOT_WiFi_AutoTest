"""WiFi performance scenario runners."""
from __future__ import annotations

import csv
import json
import re
import socket
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Optional, Tuple

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import (
    bssid_from_wifi_status,
    frequency_from_wifi_status,
    ssid_match,
)
from core.libs.android.wifi_scenarios.ip_configuration import wait_for_wifi_ipv4
from core.libs.android.wifi_scenarios.signal_level import (
    _hyper_rssi_reader,
    _traditional_rssi_reader,
    tune_attenuation_for_rssi,
)
from core.testdata_loader.android.wifi_data import get_wifi_list_entry
from core.utils.config_loader import get_settings
from core.utils.report_utils import perf_report_dir


_IPERF_SERVER_PORT = 5201
_IPERF_SERVER_START_TIMEOUT_SEC = 5.0


@dataclass(frozen=True)
class PatBaselinePoint:
    rssi_dbm: int
    min_tx_mbps: float
    min_rx_mbps: float
    max_drop_pct: Optional[float] = None


@dataclass(frozen=True)
class PatProfile:
    wifi_entry_id: str
    ap_index: int
    min_disconnect_rssi_dbm: int
    inflection_rssi_dbm: int
    inflection_drop_pct: float
    points: Tuple[PatBaselinePoint, ...]


def pat_profile(case_id: str, wifi_yaml: dict) -> Optional[PatProfile]:
    profiles = wifi_yaml.get("performance_pat") or {}
    raw = profiles.get(case_id) if isinstance(profiles, dict) else None
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"performance_pat.{case_id} 必须为映射")

    wifi_entry_id = str(raw.get("wifi_entry_id") or "").strip()
    raw_points = raw.get("points")
    if not wifi_entry_id or not isinstance(raw_points, list) or len(raw_points) < 2:
        raise ValueError(f"performance_pat.{case_id} 必须配置 wifi_entry_id 和至少两个 points")

    points = tuple(
        PatBaselinePoint(
            rssi_dbm=int(point["rssi_dbm"]),
            min_tx_mbps=float(point["min_tx_mbps"]),
            min_rx_mbps=float(point["min_rx_mbps"]),
            max_drop_pct=(
                float(point["max_drop_pct"])
                if point.get("max_drop_pct") is not None
                else None
            ),
        )
        for point in raw_points
    )
    if any(current.rssi_dbm <= following.rssi_dbm for current, following in zip(points, points[1:])):
        raise ValueError(f"performance_pat.{case_id}.points 必须按 RSSI 从强到弱排列")
    if any(
        point.min_tx_mbps < 0
        or point.min_rx_mbps < 0
        or (point.max_drop_pct is not None and not 0 <= point.max_drop_pct <= 100)
        for point in points
    ):
        raise ValueError(f"performance_pat.{case_id} 吞吐量和下降率阈值无效")

    inflection_rssi_dbm = int(raw["inflection_rssi_dbm"])
    inflection_drop_pct = float(raw["inflection_drop_pct"])
    if not 0 < inflection_drop_pct <= 100:
        raise ValueError(f"performance_pat.{case_id}.inflection_drop_pct 必须在 (0, 100] 内")
    return PatProfile(
        wifi_entry_id=wifi_entry_id,
        ap_index=int(raw.get("ap_index", 1)),
        min_disconnect_rssi_dbm=int(raw["min_disconnect_rssi_dbm"]),
        inflection_rssi_dbm=inflection_rssi_dbm,
        inflection_drop_pct=inflection_drop_pct,
        points=points,
    )


def assert_pat_curve(
    case_id: str,
    profile: PatProfile,
    samples: Mapping[int, Tuple[float, float]],
) -> None:
    for direction, value_index in (("TX", 0), ("RX", 1)):
        observed_inflection: Optional[int] = None
        previous: Optional[Tuple[int, float]] = None
        for point in profile.points:
            if point.rssi_dbm not in samples:
                pytest.fail(f"{case_id}: 缺少 RSSI {point.rssi_dbm} dBm 的吞吐量数据")
            observed = samples[point.rssi_dbm][value_index]
            minimum = point.min_tx_mbps if direction == "TX" else point.min_rx_mbps
            assert observed >= minimum, (
                f"{case_id}: {direction} 在 {point.rssi_dbm} dBm 低于基线，"
                f"observed={observed:.2f} Mbps, baseline={minimum:.2f} Mbps"
            )
            if previous is not None and previous[1] > 0:
                drop_pct = max(0.0, (previous[1] - observed) / previous[1] * 100.0)
                if point.max_drop_pct is not None:
                    assert drop_pct <= point.max_drop_pct, (
                        f"{case_id}: {direction} 在 {point.rssi_dbm} dBm 吞吐量下降过快，"
                        f"drop={drop_pct:.2f}%, max={point.max_drop_pct:.2f}%"
                    )
                if observed_inflection is None and drop_pct >= profile.inflection_drop_pct:
                    observed_inflection = point.rssi_dbm
            previous = (point.rssi_dbm, observed)

        if observed_inflection is not None:
            assert observed_inflection <= profile.inflection_rssi_dbm, (
                f"{case_id}: {direction} 吞吐量拐点过早，observed={observed_inflection} dBm, "
                f"baseline={profile.inflection_rssi_dbm} dBm"
            )


def pat_collection_rssis(initial_rssi_dbm: int) -> Tuple[int, ...]:
    start_rssi = min(-30, initial_rssi_dbm // 5 * 5)
    return tuple(range(start_rssi, -111, -5))


def _iperf_server_available(host: str, port: int = _IPERF_SERVER_PORT) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def _ensure_local_iperf_server(host: str) -> None:
    """Start the bundled Windows server when the configured host is not listening."""
    if _iperf_server_available(host):
        return

    executable = Path(__file__).resolve().parents[4] / "tools" / "bin" / "iperf3" / "iperf3.exe"
    if not executable.is_file():
        pytest.fail(f"iperf3 服务端未启动且找不到本地程序：{executable}")

    creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    process = None
    try:
        process = subprocess.Popen(
            [str(executable), "-s"],
            cwd=str(executable.parent),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            creationflags=creationflags,
        )
    except OSError as exc:
        pytest.fail(f"无法启动本地 iperf3 服务端：{executable} ({exc})")

    deadline = time.monotonic() + _IPERF_SERVER_START_TIMEOUT_SEC
    while time.monotonic() < deadline:
        if _iperf_server_available(host):
            print(f"[iperf3] 已启动本地服务端：{executable} -s")
            return
        time.sleep(0.2)
    if process is not None:
        process.terminate()
    pytest.fail(f"iperf3 服务端启动后端口 {_IPERF_SERVER_PORT} 仍不可用：{host}")


def normalized_tag(case: Dict[str, str]) -> str:
    title = (case.get("title") or "").lower()
    summary = (case.get("case_id") or "").lower()
    raw = (case.get("tag") or "").lower()
    if "hyperwifi" in title or "hyperwifi" in summary:
        return "hyperwifi"
    if "wifi" in title or "wifi" in summary:
        return "wifi"
    return raw or "common"


def is_stress_case(case: Dict[str, str]) -> bool:
    summary = case.get("case_id") or ""
    title = case.get("title") or ""
    return summary.startswith("Perf_Stress_") or any(
        token in title for token in ("30min", "12h", "12小时", "1小时", "压测")
    )


def is_throughput_tcp_udp_case(summary: str) -> bool:
    return bool(re.match(r"^Perf_(HyperWiFi|WiFi)_ThroughPut_(TCP|UDP)_\d{3}$", summary or ""))


def is_ping_latency_case(summary: str) -> bool:
    return "_Ping_Latency_" in (summary or "")


def is_connection_latency_case(summary: str) -> bool:
    return "_Conn_Latency_" in (summary or "") and "_Roam_" not in (summary or "")


def _infer_hyperwifi_region_from_title(title: str) -> str:
    upper_title = (title or "").upper()
    if "EU" in upper_title:
        return "EU"
    return "US"


def wifi_band_from_title(title: str) -> str:
    upper_title = (title or "").upper()
    for token, band in (("2.4G", "2g"), ("5G", "5g"), ("6G", "6g")):
        if token in upper_title:
            return band
    return ""


def assert_pat_link_band(
    case_id: str,
    status: str,
    target_band: str,
    target_bssid: str,
) -> str:
    connected_bssid = bssid_from_wifi_status(status)
    frequency_mhz = frequency_from_wifi_status(status)
    frequency_matches = {
        "2g": 2400 <= frequency_mhz < 2500,
        "5g": 4900 <= frequency_mhz < 5925,
        "6g": 5925 <= frequency_mhz <= 7125,
    }.get(target_band, True)
    if target_bssid and connected_bssid != target_bssid:
        pytest.fail(
            f"{case_id}: 关联 BSSID 不符，目标 {target_band}/{target_bssid}，"
            f"实际 BSSID={connected_bssid or 'unknown'}"
        )
    if target_band and not frequency_matches:
        pytest.fail(
            f"{case_id}: 关联频段不符，目标 {target_band}，"
            f"实际 Frequency={frequency_mhz or 'unknown'} MHz"
        )
    return connected_bssid


def pick_wifi_entry(case: Dict[str, str], wifi_yaml: dict) -> Tuple[Optional[dict], str]:
    wifi_list = wifi_yaml.get("wifi_list") or []
    title = (case.get("title") or "").upper()
    tag = normalized_tag(case).upper()
    if "HYPERWIFI" in tag:
        target_region = _infer_hyperwifi_region_from_title(title)
        if "US" not in title and "EU" not in title:
            print(
                f"[{case.get('case_id') or 'perf_case'}] "
                "HyperWiFi 标题未显式包含 US/EU，默认按 US 区域选网"
            )
        for entry in wifi_list:
            if (entry.get("type") or "").lower() == "hyperwifi" and (
                entry.get("region") or ""
            ).upper() == target_region:
                return entry, ""
        return None, f"未在 wifi_list 中找到 HyperWiFi {target_region} 配置"
    if "WIFI" in tag:
        target_band = wifi_band_from_title(title)
        if target_band:
            for entry in wifi_list:
                bssids = entry.get("bssids") or {}
                if (entry.get("type") or "").lower() == "normal" and bssids.get(target_band):
                    return entry, ""
            return None, f"未在 wifi_list 中找到传统 WiFi {target_band} BSSID 配置"
        for entry in wifi_list:
            if (entry.get("type") or "").lower() == "normal":
                return entry, ""
        return None, "未在 wifi_list 中找到普通 WiFi 配置"
    return None, f"不支持的标签类型: {case.get('tag')}"


def connect_by_entry(wifi: WiFiControl, entry: dict) -> bool:
    ssid = (entry.get("ssid") or "").strip()
    if not ssid:
        return False
    if (entry.get("bssid") or "").strip():
        return wifi.connect_wifi_block(entry)
    encrypt = (entry.get("encrypt") or entry.get("security") or "OPEN").upper()
    password = (entry.get("pwd") or "").strip()
    if not password and entry.get("password_env"):
        password = wifi.resolve_password(str(entry.get("password_env") or ""))
    if encrypt == "OPEN" and not password:
        return wifi.connect_open(ssid)
    if encrypt in {"WPA3", "SAE"}:
        return wifi.connect_wpa3(ssid, password)
    return wifi.connect_wpa2(ssid, password)


def parse_iperf_mbps(output: str) -> Tuple[Optional[float], Optional[float]]:
    text = output or ""
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(text[start : end + 1])
            received = data.get("end", {}).get("sum_received", {}).get("bits_per_second")
            sent = data.get("end", {}).get("sum_sent", {}).get("bits_per_second")
            return (
                float(sent) / 1_000_000.0 if sent else None,
                float(received) / 1_000_000.0 if received else None,
            )
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
    values = [float(value) for value in re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*Mbits/sec", text)]
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], values[0]
    return values[-2], values[-1]


def parse_iperf_udp_metrics(output: str) -> Tuple[Optional[float], Optional[float]]:
    text = output or ""
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(text[start : end + 1])
            summary = data.get("end", {}).get("sum_received") or data.get("end", {}).get("sum") or {}
            loss = summary.get("lost_percent")
            jitter = summary.get("jitter_ms")
            return (
                float(loss) if loss is not None else None,
                float(jitter) if jitter is not None else None,
            )
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
    match = re.search(r"([0-9.]+)\s*ms\s+\d+/\d+\s+\(([0-9.]+)%\)", text)
    return (float(match.group(2)), float(match.group(1))) if match else (None, None)


def throughput_protocols(case: Dict[str, str], default: str) -> Tuple[str, ...]:
    title = (case.get("title") or "").upper()
    if "-TCP" in title:
        return ("tcp",)
    if "-UDP" in title:
        return ("udp",)
    protocols = tuple(part.strip() for part in default.lower().split(",") if part.strip())
    if not protocols or any(protocol not in ("tcp", "udp") for protocol in protocols):
        raise ValueError("performance.iperf_protocols 只能配置 tcp、udp 或 tcp,udp")
    return protocols


def throughput_parallel_streams(case: Dict[str, str], config: object) -> int:
    default = int(getattr(config, "iperf_parallel_streams"))
    if normalized_tag(case) == "wifi":
        return int(getattr(config, "traditional_iperf_parallel_streams", default))
    return default


def throughput_summary(values: List[float]) -> str:
    return "avg={:.2f} Mbps, min={:.2f}, max={:.2f}, samples={}".format(
        sum(values) / len(values),
        min(values),
        max(values),
        ", ".join("{:.2f}".format(value) for value in values),
    )


def parse_ping_metrics(output: str) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    text = output or ""
    loss_match = re.search(r"(\d+(?:\.\d+)?)%\s*packet loss", text)
    average_match = re.search(
        r"(?:min/avg/max(?:/mdev)?|round-trip min/avg/max(?:/stddev)?)\s*=\s*"
        r"[0-9.]+/([0-9.]+)/[0-9.]+(?:/([0-9.]+))?",
        text,
    )
    return (
        float(average_match.group(1)) if average_match else None,
        float(loss_match.group(1)) if loss_match else None,
        float(average_match.group(2)) if average_match and average_match.group(2) else None,
    )


@allure.step("执行 WiFi 关联耗时测试")
def run_connection_latency_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(case["case_id"], run_shell_cmd)
    entry, reason = pick_wifi_entry(case, wifi_yaml)
    if not entry:
        pytest.skip(reason)
    ssid = (entry.get("ssid") or "").strip()
    if not ssid:
        pytest.skip("目标 SSID 为空，无法执行连接耗时测试。")

    wifi.set_wifi_enabled(True)
    wifi.disconnect_all(max_rounds=2, settle_sec=1.0, post_wait_sec=2.0)

    start = time.monotonic()
    ok = connect_by_entry(wifi, entry)
    elapsed = time.monotonic() - start
    print(f"[{case['case_id']}] connect elapsed={elapsed:.2f}s, target={ssid!r}")

    if not ok:
        pytest.xfail(f"连接目标网络失败：{ssid}")

    current = wifi.get_connected_ssid()
    assert ssid_match(ssid, current), f"关联 SSID 不符：预期 {ssid!r}，实际 {current!r}"
    assert elapsed < 8.0, f"连接成功耗时超标：elapsed={elapsed:.2f}s，阈值=8.00s"


@allure.step("执行 WiFi 时延测试")
def run_ping_latency_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
) -> None:
    attach_wifi_status(case["case_id"], run_shell_cmd)
    config = get_settings().performance
    host = config.ping_host
    if not host:
        pytest.skip("缺少 performance.ping_host 或 PERF_PING_HOST，无法执行 ping 时延实测。")

    entry, reason = pick_wifi_entry(case, wifi_yaml)
    if not entry:
        pytest.skip(reason)
    ssid = (entry.get("ssid") or "").strip()

    connect_ok = connect_by_entry(wifi, entry)
    if not connect_ok:
        pytest.xfail(f"连接目标网络失败：{ssid}")

    # 关联成功不代表 DHCP/路由已就绪，直接 ping 会得到 Network is unreachable
    wait_for_wifi_ipv4(run_shell_cmd)

    big_packet = "大包" in (case.get("title") or "")
    packet_size = config.ping_big_size if big_packet else config.ping_small_size
    cmd = f"ping -c {config.ping_count} -s {packet_size} {host}"
    out = run_shell_cmd(cmd)
    print(f"[{case['case_id']}] ping command={cmd}")
    print(f"[{case['case_id']}] raw output:\n{out}")

    avg_ms, loss_pct, jitter_ms = parse_ping_metrics(out)
    assert avg_ms is not None, "未能从 ping 输出解析平均时延"

    is_stress = is_stress_case(case)
    max_avg_ms = 100.0 if is_stress else 10.0
    max_loss_pct = 1.0 if is_stress else 0.0
    max_jitter_ms = None if is_stress else 30.0

    assert avg_ms <= max_avg_ms, f"平均时延超标：avg={avg_ms:.2f} ms，阈值={max_avg_ms:.2f} ms"
    if loss_pct is not None:
        assert loss_pct <= max_loss_pct, f"丢包率超标：loss={loss_pct:.2f}% ，阈值={max_loss_pct:.2f}%"
    if max_jitter_ms is not None and jitter_ms is not None:
        assert jitter_ms < max_jitter_ms, f"抖动超标：jitter={jitter_ms:.2f} ms，阈值={max_jitter_ms:.2f} ms"


_THROUGHPUT_CSV_HEADER = (
    "timestamp",
    "case",
    "ssid",
    "server",
    "protocol",
    "direction",
    "rssi_dbm",
    "run",
    "duration_sec",
    "streams",
    "mbps",
    "loss_pct",
    "jitter_ms",
)


def archive_iperf_run(row: Dict[str, object], raw_output: str) -> Path:
    """存档单次跑流：原始 JSON 落盘，并追加一行到汇总 CSV。"""
    base = perf_report_dir()
    case_dir = base / re.sub(r"[^\w\-]+", "_", str(row["case"]))
    case_dir.mkdir(parents=True, exist_ok=True)

    direction_tag = "rx" if str(row["direction"]).startswith("Server") else "tx"
    rssi_value = row.get("rssi_dbm", "")
    rssi_tag = f"_{rssi_value}dbm" if rssi_value != "" else ""
    raw_path = case_dir / (
        f"{row['protocol']}_{direction_tag}{rssi_tag}_run{row['run']}.json"
    )
    raw_path.write_text(raw_output or "", encoding="utf-8")

    csv_path = base / "throughput.csv"
    is_new = not csv_path.exists()
    with csv_path.open("a", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=_THROUGHPUT_CSV_HEADER)
        if is_new:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in _THROUGHPUT_CSV_HEADER})
    return raw_path


def _run_pat_direction(
    case_id: str,
    run_shell_cmd: Callable[..., str],
    config: object,
    *,
    ssid: str,
    protocol: str,
    reverse: bool,
    rssi_dbm: int,
    runs: int = 2,
    streams: Optional[int] = None,
) -> float:
    duration = int(getattr(config, "iperf_duration_sec"))
    streams = streams or int(getattr(config, "iperf_parallel_streams"))
    server = str(getattr(config, "iperf_server"))
    protocol_args = f"-u -b {getattr(config, 'udp_bandwidth')}" if protocol == "udp" else ""
    direction = "Server->DUT" if reverse else "DUT->Server"
    samples: List[float] = []

    for run_number in range(1, runs + 1):
        reverse_flag = "-R" if reverse else ""
        command = " ".join(
            f"iperf3 -c {server} -t {duration} -P {streams} "
            f"{protocol_args} {reverse_flag} -J".split()
        )
        output = run_shell_cmd(command, timeout_sec=duration + 30)
        tx_mbps, rx_mbps = parse_iperf_mbps(output)
        observed = rx_mbps if reverse else tx_mbps
        if observed is None:
            observed = tx_mbps if reverse else rx_mbps
        assert observed is not None, (
            f"{case_id}: 未能解析 {rssi_dbm} dBm {protocol.upper()} {direction} 吞吐量"
        )
        samples.append(observed)
        loss_pct = jitter_ms = None
        if protocol == "udp":
            loss_pct, jitter_ms = parse_iperf_udp_metrics(output)
        archive_iperf_run(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "case": case_id,
                "ssid": ssid,
                "server": server,
                "protocol": protocol,
                "direction": direction,
                "rssi_dbm": rssi_dbm,
                "run": run_number,
                "duration_sec": duration,
                "streams": streams,
                "mbps": f"{observed:.2f}",
                "loss_pct": "" if loss_pct is None else f"{loss_pct:.2f}",
                "jitter_ms": "" if jitter_ms is None else f"{jitter_ms:.2f}",
            },
            output,
        )
    average = sum(samples) / len(samples)
    print(
        f"[{case_id}] RSSI={rssi_dbm} dBm {protocol.upper()} {direction}: "
        f"{throughput_summary(samples)}"
    )
    return average


@allure.step("执行 PAT 吞吐量随信号衰减测试")
def run_pat_throughput_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[..., str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: Optional[AttenuatorRig],
) -> None:
    case_id = case["case_id"]
    attach_wifi_status(case_id, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{case_id}: 未配置可调衰减器 attenuator_device")
    profile = pat_profile(case_id, wifi_yaml)

    config = get_settings().performance
    server = config.iperf_server
    if not server:
        pytest.skip("缺少 performance.iperf_server 或 PERF_IPERF_SERVER，无法执行 PAT 实测。")
    if profile is not None:
        entry = get_wifi_list_entry(wifi_yaml, entry_id=profile.wifi_entry_id)
        ap_index = profile.ap_index
    else:
        entry, reason = pick_wifi_entry(case, wifi_yaml)
        if not entry:
            pytest.skip(reason)
        ap_index = 1
        print(f"[{case_id}] 未配置产品基线，进入两组数据采集模式")
    ssid = (entry.get("ssid") or "").strip()
    hyper = (entry.get("type") or "").lower() == "hyperwifi"
    target_band = "" if hyper else wifi_band_from_title(case.get("title") or "")
    target_bssid = str((entry.get("bssids") or {}).get(target_band) or "").strip().lower()
    connect_entry = {**entry, **({"bssid": target_bssid} if target_bssid else {})}
    channel = attenuator.channel_for(hyper=hyper, ap_index=ap_index)
    current_attenuations = attenuator.read_attenuations()
    if channel not in current_attenuations:
        pytest.fail(f"{case_id}: 衰减器查询结果不包含通道 {channel}: {current_attenuations!r}")

    try:
        attenuator.set_attenuation(channel, 0)
        wifi.disconnect_all(max_rounds=2, settle_sec=1.0, post_wait_sec=2.0)
        if not connect_by_entry(wifi, connect_entry):
            pytest.xfail(f"连接 PAT 目标网络失败：{ssid}")
        wait_for_wifi_ipv4(run_shell_cmd)
        iperf_check = run_shell_cmd("iperf3 --version")
        if "iperf" not in (iperf_check or "").lower():
            pytest.skip("DUT 未检测到 iperf3，请先在设备侧部署 iperf3。")
        _ensure_local_iperf_server(server)

        connected_status = run_shell_cmd("cmd wifi status")
        connected_bssid = assert_pat_link_band(
            case_id,
            connected_status,
            target_band,
            target_bssid,
        )
        read_rssi = _hyper_rssi_reader(run_shell_cmd) if hyper else _traditional_rssi_reader(
            run_shell_cmd,
            ssid,
            connected_bssid,
        )
        protocol = throughput_protocols(case, config.iperf_protocols)[0]
        parallel_streams = throughput_parallel_streams(case, config)
        samples: Dict[int, Tuple[float, float]] = {}
        attenuation_db = 0.0
        last_connected_rssi: Optional[int] = None
        if profile is not None:
            target_rssis = tuple(point.rssi_dbm for point in profile.points)
        else:
            initial_rssi = read_rssi()
            if initial_rssi is None:
                pytest.fail(f"{case_id}: 连接后无法读取目标网络 RSSI")
            target_rssis = pat_collection_rssis(initial_rssi)

        for target_rssi in target_rssis:
            attenuation_db, measured_rssi = tune_attenuation_for_rssi(
                attenuator,
                channel,
                target_rssi,
                read_rssi,
                allow_missing=profile is None,
            )
            if measured_rssi is None:
                print(f"[{case_id}] RSSI 目标 {target_rssi} dBm 已断连，结束数据采集")
                break
            last_connected_rssi = measured_rssi
            assert_pat_link_band(
                case_id,
                run_shell_cmd("cmd wifi status"),
                target_band,
                target_bssid,
            )
            tx_mbps = _run_pat_direction(
                case_id,
                run_shell_cmd,
                config,
                ssid=ssid,
                protocol=protocol,
                reverse=False,
                rssi_dbm=measured_rssi,
                streams=parallel_streams,
            )
            assert_pat_link_band(
                case_id,
                run_shell_cmd("cmd wifi status"),
                target_band,
                target_bssid,
            )
            rx_mbps = _run_pat_direction(
                case_id,
                run_shell_cmd,
                config,
                ssid=ssid,
                protocol=protocol,
                reverse=True,
                rssi_dbm=measured_rssi,
                streams=parallel_streams,
            )
            assert_pat_link_band(
                case_id,
                run_shell_cmd("cmd wifi status"),
                target_band,
                target_bssid,
            )
            samples[target_rssi] = (tx_mbps, rx_mbps)

        if profile is None:
            assert samples, f"{case_id}: 未采集到任何 PAT 吞吐量数据"
            print(f"[{case_id}] 数据采集完成，共 {len(samples)} 个 RSSI 点，每方向 2 组")
            return

        assert_pat_curve(case_id, profile, samples)
        consecutive_missing = 0
        while True:
            if attenuation_db < attenuator.max_attenuation_db:
                attenuation_db = min(attenuator.max_attenuation_db, attenuation_db + 2.0)
                attenuator.set_attenuation(channel, attenuation_db)
            time.sleep(2.0)
            measured_rssi = read_rssi()
            if measured_rssi is None:
                consecutive_missing += 1
                if consecutive_missing >= 2:
                    break
                continue
            consecutive_missing = 0
            last_connected_rssi = measured_rssi
            if attenuation_db >= attenuator.max_attenuation_db:
                pytest.fail(f"{case_id}: 达到最大衰减仍未断开 PAT 目标网络")
        assert last_connected_rssi is not None
        assert last_connected_rssi <= profile.min_disconnect_rssi_dbm, (
            f"{case_id}: 断连过早，最后连接 RSSI={last_connected_rssi} dBm, "
            f"基线={profile.min_disconnect_rssi_dbm} dBm"
        )
    finally:
        attenuator.set_attenuation(channel, current_attenuations[channel])


@allure.step("执行 WiFi 吞吐量测试")
def run_throughput_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[..., str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    wifi_entry_id: Optional[str] = None,
) -> None:
    attach_wifi_status(case["case_id"], run_shell_cmd)
    config = get_settings().performance
    server = config.iperf_server
    if not server:
        pytest.skip("缺少 performance.iperf_server 或 PERF_IPERF_SERVER，无法执行吞吐量实测。")

    if wifi_entry_id:
        entry = get_wifi_list_entry(wifi_yaml, entry_id=wifi_entry_id)
        reason = f"未在 wifi_list 中找到 id={wifi_entry_id!r} 的配置"
    else:
        entry, reason = pick_wifi_entry(case, wifi_yaml)
    if not entry:
        pytest.skip(reason)
    ssid = (entry.get("ssid") or "").strip()
    if not connect_by_entry(wifi, entry):
        pytest.xfail(f"连接目标网络失败：{ssid}")

    current = wifi.get_connected_ssid()
    print(f"[{case['case_id']}] connected_ssid={current!r}, target={ssid!r}")

    # 版本横幅形如 "iperf 3.6+ (cJSON 1.7.13)"，不含 "iperf3" 字面量
    iperf_check = run_shell_cmd("iperf3 --version")
    if "iperf" not in (iperf_check or "").lower():
        pytest.skip("DUT 未检测到 iperf3，请先在设备侧部署 iperf3。")
    _ensure_local_iperf_server(server)

    duration = config.iperf_duration_sec
    runs = config.iperf_runs
    streams = throughput_parallel_streams(case, config)
    udp_bw = config.udp_bandwidth
    min_mbps = config.min_mbps
    protocols = throughput_protocols(case, config.iperf_protocols)
    print(
        f"[{case['case_id']}] iperf3 server={server}, duration={duration}s, "
        f"runs={runs}, streams={streams}, protocols={','.join(protocols)}"
    )

    for protocol in protocols:
        protocol_args = f"-u -b {udp_bw}" if protocol == "udp" else ""
        for direction, reverse in (("DUT->Server", False), ("Server->DUT", True)):
            samples: List[float] = []
            udp_losses: List[float] = []
            udp_jitters: List[float] = []

            for run_number in range(1, runs + 1):
                reverse_flag = "-R" if reverse else ""
                cmd = (
                    f"iperf3 -c {server} -t {duration} -P {streams} "
                    f"{protocol_args} {reverse_flag} -J"
                )
                cmd = " ".join(cmd.split())
                # adb 默认超时（30s）短于跑流时长，必须按 duration 放宽
                out = run_shell_cmd(cmd, timeout_sec=duration + 30)
                tx_mbps, rx_mbps = parse_iperf_mbps(out)
                observed = rx_mbps if reverse else tx_mbps
                if observed is None:
                    observed = tx_mbps if reverse else rx_mbps
                assert observed is not None, (
                    "未能从 iperf3 输出解析到吞吐量，请检查 server/网络/iperf3 输出格式\n"
                    f"cmd: {cmd}\nraw output:\n{out}"
                )
                samples.append(observed)
                print(
                    f"[{case['case_id']}] {protocol.upper()} {direction} "
                    f"run={run_number}/{runs}, throughput={observed:.2f} Mbps"
                )

                loss_pct = jitter_ms = None
                if protocol == "udp":
                    loss_pct, jitter_ms = parse_iperf_udp_metrics(out)
                    if loss_pct is not None:
                        udp_losses.append(loss_pct)
                    if jitter_ms is not None:
                        udp_jitters.append(jitter_ms)

                archive_iperf_run(
                    {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "case": case["case_id"],
                        "ssid": ssid,
                        "server": server,
                        "protocol": protocol,
                        "direction": direction,
                        "run": run_number,
                        "duration_sec": duration,
                        "streams": streams,
                        "mbps": f"{observed:.2f}",
                        "loss_pct": "" if loss_pct is None else f"{loss_pct:.2f}",
                        "jitter_ms": "" if jitter_ms is None else f"{jitter_ms:.2f}",
                    },
                    out,
                )

            average_mbps = sum(samples) / len(samples)
            print(
                f"[{case['case_id']}] {protocol.upper()} {direction} "
                f"throughput: {throughput_summary(samples)}"
            )
            if protocol == "udp":
                if udp_losses:
                    print(
                        f"[{case['case_id']}] UDP {direction} "
                        f"loss_avg={sum(udp_losses) / len(udp_losses):.2f}%"
                    )
                if udp_jitters:
                    print(
                        f"[{case['case_id']}] UDP {direction} "
                        f"jitter_avg={sum(udp_jitters) / len(udp_jitters):.2f} ms"
                    )
            assert average_mbps >= min_mbps, (
                f"平均吞吐量低于阈值: average={average_mbps:.2f} Mbps, "
                f"min={min_mbps:.2f} Mbps, protocol={protocol}, direction={direction}, "
                f"case={case['case_id']}"
            )