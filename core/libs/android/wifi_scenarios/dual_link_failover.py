"""双链路主备切换（PriBakLink）场景 runner。

覆盖《双链路主备切换管理.md》中 beacon loss 触发主备切换的用例：
- 连接双 WiFi（复用 connection_chk.assert_dual_wifi_connected）
- 清空 logcat 后由人工执行物理操作（衰减器调 RSSI / AP 断电），
  设置 DUAL_LINK_MANUAL_CONFIRM=1 时逐条确认（实验室联调模式）
- 抓取 logcat，断言 BEACON LOSS 事件与 setrole 主备角色切换
"""
from __future__ import annotations

import re
import time
from collections.abc import Mapping
from typing import Callable, List, Optional

import allure
import pytest

from core.contracts.attenuator import AttenuatorRig
from core.libs.android.wifi_scenarios.dual_link import (
    connect_dual_link_in_order,
    dual_link_legs,
    primary_backup_entry,
    primary_link_from_status,
    tune_dual_link_rssi,
    wait_for_link_ssid,
    wait_for_primary_link,
)
from core.libs.android.wifi_scenarios.signal_level import signal_level_entry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.testdata_loader.android.wifi_data import get_dual_wifi_entry

from core.libs.android.wifi_scenarios.lab_requirements import env_enabled
from core.libs.android.wifi_control.connection_chk import assert_dual_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger

log = get_logger(__name__)

DEFAULT_DUAL_WIFI_ENTRY_ID = "dual_wifi_24g_hyperwifi_us"

_BEACON_LOSS_RE = re.compile(r"beacon[\s_]*loss|BEACON LOSS", re.IGNORECASE)
_SETROLE_RE = re.compile(r"setrole\s+ifname", re.IGNORECASE)
_ROLE_LINE_RE = re.compile(
    r"((?:wlan|hyper)\d+)\s+role:\s*(ROLE_CLIENT_\w+)",
    re.IGNORECASE,
)
_FINAL_SCORE_RE = re.compile(
    r'Score for candidate:\s+SSID:\s+"(?P<ssid>[^"\r\n]+)"'
    r".*?final score:\s*(?P<score>-?\d+)",
    re.IGNORECASE,
)

_WIFI_IFACE = "wlan0"
_HYPER_IFACE = "hyper0"
_ROLE_PRIMARY = "ROLE_CLIENT_PRIMARY"
_ROLE_SECONDARY = "ROLE_CLIENT_SECONDARY_LONG_LIVED"


def link_radio_metrics(status: str, iface: str) -> tuple[int | None, int | None]:
    """Return RSSI and frequency from one ClientModeManager status block."""
    block_match = re.search(
        rf"iface={re.escape(iface)}\b.*?(?=\n==== ClientModeManager|\Z)",
        status or "",
        re.DOTALL | re.IGNORECASE,
    )
    if block_match is None:
        return None, None
    block = block_match.group(0)
    rssi_match = re.search(r"\bRSSI:\s*(-?\d+)\b", block)
    frequency_match = re.search(r"\bFrequency:\s*(\d+)MHz\b", block)
    return (
        int(rssi_match.group(1)) if rssi_match else None,
        int(frequency_match.group(1)) if frequency_match else None,
    )


def link_bssid_from_status(status: str, iface: str) -> str:
    block_match = re.search(
        rf"iface={re.escape(iface)}\b.*?(?=\n==== ClientModeManager|\Z)",
        status or "",
        re.DOTALL | re.IGNORECASE,
    )
    if block_match is None:
        return ""
    match = re.search(
        r"\bBSSID:\s*([0-9a-f]{2}(?::[0-9a-f]{2}){5})\b",
        block_match.group(0),
        re.IGNORECASE,
    )
    return match.group(1).lower() if match else ""


def wait_for_link_bssid(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    iface: str,
    expected_bssid: str,
    *,
    timeout: float = 35.0,
) -> str:
    deadline = time.monotonic() + timeout
    last_status = ""
    while time.monotonic() < deadline:
        last_status = run_shell_cmd("cmd wifi status")
        if link_bssid_from_status(last_status, iface) == expected_bssid.lower():
            return last_status
        time.sleep(1.0)
    pytest.fail(
        f"{summary}: 等待 {iface} 关联 BSSID {expected_bssid} 超时；"
        f"实际={link_bssid_from_status(last_status, iface)!r}\n{last_status[:1200]}"
    )


@allure.step("执行首次连接顺序触发主备选择验证")
def run_connection_state_change_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    order: tuple[str, str],
    targets: dict[str, int],
    expected_primary: str,
    settle_sec: float = 4.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")

    entry = primary_backup_entry(wifi_yaml)
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = attenuator.read_attenuations()
    if any(channel not in original for channel in channels.values()):
        pytest.fail(
            f"{summary}: 衰减器查询缺少目标通道，"
            f"channels={channels!r}, state={original!r}"
        )

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: RSSI 校准前双链路连接失败 "
                f"found={found!r} missing={missing!r}"
            )
        tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            targets,
            settle_sec=settle_sec,
        )
        wifi.adb.shell_line("logcat -c")
        connect_dual_link_in_order(summary, wifi, entry, order)
        status = wait_for_primary_link(summary, run_shell_cmd, expected_primary)
        _code, out, err = wifi.adb.shell_line(
            "logcat -d | grep -i -E 'setrole|final score'"
        )
        role_log = ((out or "") + "\n" + (err or "")).strip()
        allure.attach(role_log, "setrole and final score log", allure.attachment_type.TEXT)
        print(
            f"[{summary}] order={order!r} targets={targets!r} "
            f"primary={expected_primary}\n{status[:1200]}"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])


@allure.step("执行 RSSI 阈值触发主备切换验证")
def run_rssi_threshold_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    threshold_rssi: int = -73,
    expected_band: str = "5g",
    settle_sec: float = 4.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")

    entry = primary_backup_entry(wifi_yaml)
    traditional, hyper = dual_link_legs(entry)
    configured_bssids = traditional.get("bssids")
    if not isinstance(configured_bssids, Mapping):
        pytest.skip(f"{summary}: 传统 WiFi profile 未配置分频段 BSSID")
    target_bssid = str(configured_bssids.get(expected_band) or "").strip().lower()
    if not target_bssid:
        pytest.skip(f"{summary}: 传统 WiFi profile 未配置 {expected_band} BSSID")
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = attenuator.read_attenuations()
    if any(channel not in original for channel in channels.values()):
        pytest.fail(
            f"{summary}: 衰减器查询缺少目标通道，"
            f"channels={channels!r}, state={original!r}"
        )

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: RSSI 校准前双链路连接失败 "
                f"found={found!r} missing={missing!r}"
            )
        calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"hyper": -40},
            settle_sec=settle_sec,
            links=("hyper",),
        )
        current_status = run_shell_cmd("cmd wifi status")
        if link_bssid_from_status(current_status, _WIFI_IFACE) != target_bssid:
            traditional_ssid = str(traditional.get("ssid") or "")
            network_id = wifi.find_network_id_by_ssid(traditional_ssid)
            if network_id and not wifi.forget_network(network_id):
                pytest.fail(
                    f"{summary}: 无法清除传统 WiFi network id={network_id}"
                )
        targeted_entry = {**traditional, "bssid": target_bssid}
        if not wifi.connect_wifi_block(targeted_entry):
            pytest.fail(f"{summary}: 无法连接目标 BSSID {target_bssid}")
        wait_for_link_bssid(
            summary,
            run_shell_cmd,
            _WIFI_IFACE,
            target_bssid,
        )
        targets = [
            str(traditional.get("ssid") or ""),
            str(hyper.get("ssid") or ""),
        ]
        found, missing = wifi.match_associated_ssids(
            targets,
            use_dumpsys_for_missing=True,
        )
        if missing:
            pytest.fail(
                f"{summary}: 锁定传统 BSSID 后双链路不完整 "
                f"found={found!r} missing={missing!r}"
            )
        wifi_target = -50 if expected_band == "2g" else -60
        calibrated.update(tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"wifi": wifi_target},
            settle_sec=settle_sec,
            traditional_bssid=target_bssid,
            links=("wifi",),
        ))
        status = wait_for_primary_link(summary, run_shell_cmd, "wifi")
        live_rssi, frequency = link_radio_metrics(status, _WIFI_IFACE)
        band_matches = (
            expected_band == "2g" and frequency is not None and frequency < 3000
        ) or (
            expected_band == "5g" and frequency is not None and 4900 <= frequency < 5900
        )
        if not band_matches:
            pytest.skip(
                f"{summary}: 当前传统 WiFi 频率={frequency or '未知'}MHz，"
                f"不满足 {expected_band} 用例前置"
            )
        wifi.adb.shell_line("logcat -c")

        start_attenuation, calibrated_rssi = calibrated["wifi"]
        start_rssi = live_rssi if live_rssi is not None else calibrated_rssi
        if start_rssi is None or start_rssi <= threshold_rssi:
            pytest.fail(
                f"{summary}: 初始 WiFi RSSI 不高于阈值，"
                f"start_rssi={start_rssi}, threshold={threshold_rssi}"
            )
        reached_rssi: int | None = None
        max_steps = min(60, int(attenuator.max_attenuation_db - start_attenuation))
        for step in range(1, max_steps + 1):
            attenuator.set_attenuation(channels["wifi"], start_attenuation + step)
            time.sleep(1.0)
            status = run_shell_cmd("cmd wifi status")
            measured_rssi, _ = link_radio_metrics(status, _WIFI_IFACE)
            if measured_rssi is None:
                continue
            if measured_rssi <= threshold_rssi:
                reached_rssi = measured_rssi
                break
            actual = primary_link_from_status(status)
            if actual != "wifi":
                pytest.fail(
                    f"{summary}: WiFi RSSI 达到阈值前提前切换，"
                    f"step={step}, rssi={measured_rssi}, primary={actual!r}\n"
                    f"{status[:1200]}"
                )

        if reached_rssi is None:
            pytest.fail(
                f"{summary}: 以 1 dB/s 增加衰减后仍未达到 "
                f"RSSI {threshold_rssi} dBm"
            )

        status = wait_for_primary_link(summary, run_shell_cmd, "hyper", timeout=60.0)
        _code, out, err = wifi.adb.shell_line(
            "logcat -d | grep -i -E 'setrole|final score'"
        )
        role_log = ((out or "") + "\n" + (err or "")).strip()
        allure.attach(role_log, "RSSI failover log", allure.attachment_type.TEXT)
        print(
            f"[{summary}] WiFi RSSI 从 {start_rssi} dBm 以 1 dB/s "
            f"下降至 {reached_rssi} dBm，primary=hyper\n{status[:1200]}"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])


def parse_link_roles(log_text: str) -> dict[str, str]:
    """从 logcat 提取最近一次各接口角色：{iface: role}（后出现的覆盖先出现的）。"""
    roles: dict[str, str] = {}
    for match in _ROLE_LINE_RE.finditer(log_text or ""):
        roles[match.group(1).lower()] = match.group(2).upper()
    return roles


def candidate_final_scores(log_text: str) -> dict[str, int]:
    """Return the latest final score for each candidate in one selection window."""
    scores: dict[str, int] = {}
    for line in (log_text or "").splitlines():
        match = _FINAL_SCORE_RE.search(line)
        if match:
            scores[match.group("ssid")] = int(match.group("score"))
    return scores


def assert_backup_score_leads(
    log_text: str,
    *,
    primary_ssid: str,
    backup_ssid: str,
    summary: str,
) -> tuple[int, int]:
    scores = candidate_final_scores(log_text)
    missing = [ssid for ssid in (primary_ssid, backup_ssid) if ssid not in scores]
    if missing:
        pytest.fail(f"{summary}: 候选评分日志缺少 {missing!r}")
    primary_score = scores[primary_ssid]
    backup_score = scores[backup_ssid]
    if backup_score <= primary_score:
        pytest.fail(
            f"{summary}: 备链路评分未高于主链路，"
            f"primary={primary_score}, backup={backup_score}"
        )
    return primary_score, backup_score


def _wait_for_candidate_score_window(
    wifi: WiFiControl,
    primary_ssid: str,
    backup_ssid: str,
    *,
    timeout: float = 25.0,
) -> str:
    wifi.adb.shell_line("logcat -c")
    deadline = time.monotonic() + timeout
    latest = ""
    while time.monotonic() < deadline:
        _code, out, err = wifi.adb.shell_line(
            "logcat -d | grep -i -E 'start network selection|final score|setrole'"
        )
        latest = ((out or "") + "\n" + (err or "")).strip()
        scores = candidate_final_scores(latest)
        if primary_ssid in scores and backup_ssid in scores:
            return latest
        time.sleep(1.0)
    return latest


@allure.step("验证备链路连续5次评分领先后的主备切换去抖")
def run_score_debounce_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    initial_wifi_rssi: int = -65,
    weak_wifi_rssi: int = -73,
    hyper_rssi: int = -70,
    required_leads: int = 5,
    settle_sec: float = 4.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")

    entry = primary_backup_entry(wifi_yaml)
    traditional, hyper = dual_link_legs(entry)
    primary_ssid = str(traditional.get("ssid") or "")
    backup_ssid = str(hyper.get("ssid") or "")
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = dict(attenuator.read_attenuations())
    if any(channel not in original for channel in channels.values()):
        pytest.fail(
            f"{summary}: 衰减器查询缺少目标通道，"
            f"channels={channels!r}, state={original!r}"
        )

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: RSSI校准前双链路连接失败 "
                f"found={found!r} missing={missing!r}"
            )

        calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"hyper": hyper_rssi, "wifi": weak_wifi_rssi},
            settle_sec=settle_sec,
            links=("hyper", "wifi"),
        )
        weak_attenuation, measured_weak = calibrated["wifi"]
        if measured_weak is None or abs(measured_weak - weak_wifi_rssi) > 2:
            pytest.fail(
                f"{summary}: WiFi弱信号校准失败，"
                f"target={weak_wifi_rssi}, measured={measured_weak}"
            )

        attenuator.set_attenuation(channels["wifi"], 0)
        connect_dual_link_in_order(summary, wifi, entry, ("hyper", "wifi"))
        wait_for_primary_link(summary, run_shell_cmd, "wifi")
        initial_calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"wifi": initial_wifi_rssi},
            settle_sec=settle_sec,
            links=("wifi",),
        )
        _initial_attenuation, measured_initial = initial_calibrated["wifi"]
        if measured_initial is None or abs(measured_initial - initial_wifi_rssi) > 2:
            pytest.fail(
                f"{summary}: WiFi强信号校准失败，"
                f"target={initial_wifi_rssi}, measured={measured_initial}"
            )
        wait_for_primary_link(summary, run_shell_cmd, "wifi")
        wifi.open_wifi_settings()
        wifi.adb.shell_line("logcat -c")

        attenuator.set_attenuation(channels["wifi"], weak_attenuation)
        time.sleep(3.0)
        immediate_status = run_shell_cmd("cmd wifi status")
        allure.attach(
            immediate_status,
            "cmd wifi status - immediate debounce check",
            allure.attachment_type.TEXT,
        )
        if primary_link_from_status(immediate_status) != "wifi":
            pytest.fail(f"{summary}: WiFi降至阈值后立即发生主备切换")

        samples: list[tuple[int, int]] = []
        for index in range(1, required_leads + 1):
            score_log = _wait_for_candidate_score_window(
                wifi,
                primary_ssid,
                backup_ssid,
            )
            scores = assert_backup_score_leads(
                score_log,
                primary_ssid=primary_ssid,
                backup_ssid=backup_ssid,
                summary=f"{summary} 第{index}次评分",
            )
            samples.append(scores)
            allure.attach(
                score_log or "<no score log>",
                f"debounce-score-{index}",
                allure.attachment_type.TEXT,
            )
            if index < required_leads:
                status = run_shell_cmd("cmd wifi status")
                if primary_link_from_status(status) != "wifi":
                    pytest.fail(
                        f"{summary}: 备链路仅连续领先{index}次时提前切换"
                    )

        status = wait_for_primary_link(summary, run_shell_cmd, "hyper", timeout=30.0)
        print(
            f"[{summary}] backup score leads={samples!r}; primary=hyper\n"
            f"{status[:1200]}"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


@allure.step("验证息屏后目标链路PNO重连并恢复主链路")
def _run_screen_off_pno_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
    *,
    reconnect_link: str,
    wifi_rssi: int = -75,
    initial_hyper_rssi: int = -70,
    reconnect_rssi: int = -65,
    settle_sec: float = 4.0,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if attenuator is None:
        pytest.skip(f"{summary}: 未配置可调衰减器 attenuator_device")
    if reconnect_link not in {"wifi", "hyper"}:
        raise ValueError(f"无效的PNO重连链路: {reconnect_link!r}")

    entry = get_dual_wifi_entry(
        wifi_yaml,
        entry_id=DEFAULT_DUAL_WIFI_ENTRY_ID,
    )
    traditional, hyper = dual_link_legs(entry)
    traditional_ssid = str(traditional.get("ssid") or "")
    hyper_ssid = str(hyper.get("ssid") or "")
    ssids = {"wifi": traditional_ssid, "hyper": hyper_ssid}
    remaining_link = "wifi" if reconnect_link == "hyper" else "hyper"
    _, ap_index = signal_level_entry(wifi_yaml, hyper=False)
    channels = {
        "wifi": attenuator.channel_for(hyper=False, ap_index=ap_index),
        "hyper": attenuator.channel_for(hyper=True, ap_index=ap_index),
    }
    original = dict(attenuator.read_attenuations())
    if any(channel not in original for channel in channels.values()):
        pytest.fail(
            f"{summary}: 衰减器查询缺少目标通道，"
            f"channels={channels!r}, state={original!r}"
        )

    try:
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        ok, found, missing = wifi.ensure_dual_wifi_connected(entry, timeout=90.0)
        if not ok:
            pytest.fail(
                f"{summary}: RSSI校准前双链路连接失败 "
                f"found={found!r} missing={missing!r}"
            )
        reconnect_calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {reconnect_link: reconnect_rssi},
            settle_sec=settle_sec,
            links=(reconnect_link,),
        )
        reconnect_attenuation, reconnect_measured = reconnect_calibrated[reconnect_link]
        initial_calibrated = tune_dual_link_rssi(
            run_shell_cmd,
            attenuator,
            channels,
            entry,
            {"hyper": initial_hyper_rssi, "wifi": wifi_rssi},
            settle_sec=settle_sec,
            links=("hyper", "wifi"),
        )
        for channel in channels.values():
            attenuator.set_attenuation(channel, 0)
        connect_dual_link_in_order(summary, wifi, entry, (remaining_link, reconnect_link))
        for link, (attenuation, _measured) in initial_calibrated.items():
            attenuator.set_attenuation(channels[link], attenuation)
        time.sleep(settle_sec)
        wait_for_primary_link(summary, run_shell_cmd, reconnect_link)

        attenuator.set_attenuation(
            channels[reconnect_link],
            attenuator.max_attenuation_db,
        )
        deadline = time.monotonic() + 45.0
        while time.monotonic() < deadline:
            found, _missing = wifi.match_associated_ssids(
                [ssids[reconnect_link]],
                use_dumpsys_for_missing=True,
            )
            if not found:
                break
            time.sleep(1.0)
        else:
            pytest.fail(f"{summary}: {reconnect_link}加至最大衰减后未断开")
        found, missing = wifi.match_associated_ssids(
            [ssids[remaining_link]],
            use_dumpsys_for_missing=True,
        )
        if missing:
            pytest.fail(
                f"{summary}: {reconnect_link}断开后{remaining_link}未保持连接"
            )

        wifi.adb.shell_line("logcat -c")
        wifi.adb.keyevent("KEYCODE_SLEEP")
        time.sleep(2.0)
        attenuator.set_attenuation(channels[reconnect_link], reconnect_attenuation)
        try:
            wait_for_link_ssid(wifi, ssids[reconnect_link], timeout=90.0)
        finally:
            _code, out, err = wifi.adb.shell_line(
                "logcat -d | grep -i -E 'pno|final score|setrole'"
            )
            reconnect_log = ((out or "") + "\n" + (err or "")).strip()
            allure.attach(
                reconnect_log or "<no PNO/failover log>",
                f"screen-off {reconnect_link} reconnect log",
                allure.attachment_type.TEXT,
            )
        if "pno scan started" not in reconnect_log.lower():
            pytest.fail(f"{summary}: {reconnect_link}重连前未检测到PNO扫描")
        status = wait_for_primary_link(
            summary,
            run_shell_cmd,
            reconnect_link,
            timeout=45.0,
        )
        print(
            f"[{summary}] {reconnect_link} reconnected at "
            f"{reconnect_measured} dBm; initial={initial_calibrated!r}; "
            f"primary={reconnect_link}\n{status[:1200]}"
        )
    finally:
        for channel in channels.values():
            attenuator.set_attenuation(channel, original[channel])
        wifi.set_wifi_enabled(True, settle_sec=1.0)
        wifi.adb.keyevent("KEYCODE_WAKEUP")
        wifi.adb.shell("wm", "dismiss-keyguard")
        wifi.adb.keyevent("KEYCODE_HOME")


def run_screen_off_wifi_pno_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
) -> None:
    _run_screen_off_pno_failover_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator,
        reconnect_link="wifi",
        wifi_rssi=-65,
        initial_hyper_rssi=-70,
    )


def run_screen_off_hyper_pno_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    attenuator: AttenuatorRig | None,
) -> None:
    _run_screen_off_pno_failover_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        attenuator,
        reconnect_link="hyper",
        wifi_rssi=-75,
        initial_hyper_rssi=-70,
    )


def _manual_steps(summary: str, steps: List[str]) -> None:
    """打印需人工执行的物理操作步骤；联调模式下逐条等待回车确认。"""
    print(f"[{summary}] 请在实验台上执行以下操作：")
    for index, step in enumerate(steps, start=1):
        print(f"    {index}. {step}")
    if env_enabled("DUAL_LINK_MANUAL_CONFIRM", "0"):
        for index, step in enumerate(steps, start=1):
            input(f"[{summary}] 完成步骤 {index}（{step}）后回车继续…")
    else:
        wait_sec = 20.0
        print(f"[{summary}] 非确认模式，等待 {wait_sec:.0f}s 供执行上述操作…")
        time.sleep(wait_sec)


def capture_failover_log(adb: AdbHelper, duration_sec: float = 45.0) -> str:
    """清空 logcat，等待切换发生，抓取主备切换相关日志。"""
    adb.shell_line("logcat -c")
    time.sleep(2.0)
    wait = max(10.0, float(duration_sec))
    log.info("采集主备切换日志，等待 %.0fs…", wait)
    time.sleep(wait)
    _code, out, err = adb.shell_line(
        "logcat -d | grep -i -E 'beacon|setrole|final score'"
    )
    return ((out or "") + "\n" + (err or "")).strip()


def assert_beacon_loss_and_failover(
    log_text: str,
    *,
    summary: str,
    expect_primary_iface: Optional[str],
) -> None:
    """断言出现 BEACON LOSS；expect_primary_iface 为 None 时断言未发生角色切换。"""
    if expect_primary_iface is not None:
        if not _BEACON_LOSS_RE.search(log_text or ""):
            excerpt = (log_text or "")[:1200]
            pytest.fail(
                f"{summary}: 未在 logcat 找到 BEACON LOSS 事件\n{excerpt}"
            )
    else:
        if _SETROLE_RE.search(log_text or ""):
            roles = parse_link_roles(log_text)
            pytest.fail(
                f"{summary}: 备用链路 beacon loss 不应触发主备切换，"
                f"但 logcat 出现 setrole：roles={roles!r}"
            )
        log.info("%s: 未出现 setrole，主备未切换（符合预期）", summary)
        return

    if not _SETROLE_RE.search(log_text or ""):
        excerpt = (log_text or "")[:1200]
        pytest.fail(
            f"{summary}: 未找到 setrole ifname 角色切换日志\n{excerpt}"
        )

    roles = parse_link_roles(log_text)
    print(f"[{summary}] 解析角色：{roles!r}")
    expect_iface = expect_primary_iface.lower()
    actual_role = roles.get(expect_iface, "")
    if actual_role != _ROLE_PRIMARY:
        pytest.fail(
            f"{summary}: 期望 {expect_iface}={_ROLE_PRIMARY}，"
            f"实际={actual_role or '未出现'}（roles={roles!r}）"
        )
    other = _HYPER_IFACE if expect_iface == _WIFI_IFACE else _WIFI_IFACE
    other_role = roles.get(other, "")
    if other_role and other_role != _ROLE_SECONDARY:
        log.warning(
            "%s: 对端 %s 角色=%s（预期 %s），请关注",
            summary, other, other_role, _ROLE_SECONDARY,
        )
    log.info("%s: 主备切换校验通过 primary=%s", summary, expect_iface)


@allure.step("执行 Beacon 丢失倒换验证")
def run_beacon_loss_failover_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    loss_target: str,
    expect_failover: bool = True,
    expect_primary: str = "wifi",
    hyper_region: str = "US",
    dual_wifi_entry_id: Optional[str] = None,
    settle_sec: float = 45.0,
) -> None:
    """beacon loss 触发主备切换。

    loss_target: "wifi"=AP 断电（WiFi 链路 beacon loss）、
                 "hyper"=miniAP 断电（HyperWiFi 链路 beacon loss）。
    expect_primary: "wifi" → wlan0 为主；"hyper" → hyper0 为主。
    expect_failover=False 时断言未发生角色切换（备用链路 beacon loss 场景）。
    """
    attach_wifi_status(summary, run_shell_cmd)
    entry_id = (dual_wifi_entry_id or DEFAULT_DUAL_WIFI_ENTRY_ID).strip() or None
    print(
        f"[{summary}] 双链路 beacon loss：loss_target={loss_target} "
        f"expect_failover={expect_failover} expect_primary={expect_primary} "
        f"entry={entry_id}"
    )
    assert_dual_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        hyper_region=hyper_region,
        entry_id=entry_id,
        failure_label=summary,
    )

    # 清 logcat 在前，人工操作在后，保证抓到的就是操作后的切换日志
    wifi.adb.shell_line("logcat -c")
    time.sleep(2.0)

    if loss_target == "wifi":
        steps = [
            "通过衰减器调节 AP 与 miniAP 信号至正常（如 AP -65dBm / miniAP -70dBm）",
            "确认 WiFi 为主网络（cmd wifi status / 设置页）",
            "将主网络 WiFi 侧 AP 下电（或衰减器拉断触发 beacon loss）",
        ]
    else:
        steps = [
            "通过衰减器调节 AP 与 miniAP 信号（如 AP -75dBm / miniAP -65dBm）",
            "确认 HyperWiFi 为主网络",
            "将 HyperWiFi 侧 miniAP 下电（或衰减器拉断触发 beacon loss）",
        ]
    if not expect_failover:
        steps[-1] = steps[-1].replace("主网络", "备用网络")
    _manual_steps(summary, steps)

    log_text = capture_failover_log(wifi.adb, duration_sec=settle_sec)
    print(f"[{summary}] 主备切换日志摘录（前 1500 字符）：\n{log_text[:1500]}")

    if expect_failover:
        expect_iface = _WIFI_IFACE if expect_primary == "wifi" else _HYPER_IFACE
    else:
        expect_iface = None
    assert_beacon_loss_and_failover(
        log_text,
        summary=summary,
        expect_primary_iface=expect_iface,
    )
