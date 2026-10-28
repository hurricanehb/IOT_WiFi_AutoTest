"""WiFi channel automation helpers with legacy case API exports."""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeAlias, TypedDict, cast

import allure
import pytest

from core.testdata_loader import get_wifi_list_entry
from core.testdata_loader.miniap import (
    count_channel_steps,
    iter_channel_steps,
    load_halow_frequency_tables,
    special_id as halow_special_id,
)
from core.libs.android.wifi_control.connection_chk import (
    assert_wifi_connected,
)
from core.libs.android.wifi_scenarios.country_code import (
    force_country_and_restart_wifi,
    require_cli_app,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import frequency_from_wifi_status
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status


class ChannelRange(TypedDict, total=False):
    start: int
    end: int
    step: int


ChannelSpec: TypeAlias = int | list[int | ChannelRange] | ChannelRange


class BandwidthPlan(TypedDict, total=False):
    mhz: int
    channels: ChannelSpec


class ChannelPlan(TypedDict, total=False):
    driver: str
    band: str
    country: str
    android_country_code: str
    country_code: str
    special_id: str
    wifi_entry_id: str
    wifi_entry_ssid: str
    configured_ssid: str
    configure_wifi: bool
    bandwidth_mhz: int
    settle_sec: float
    ap_id: int
    channels: ChannelSpec
    bandwidths: list[BandwidthPlan]


_ANDROID_CC_BY_HALOW_REGION = {
    "US": "US",
    "EU": "DE",
}
_DEFAULT_HALOW_REGION = "US"
_DEFAULT_DFS_SETTLE_SEC = 65.0


def _wifi_channel_frequency_mhz(band: str, channel: int) -> int:
    if band == "2g":
        return 2484 if channel == 14 else 2407 + 5 * channel
    if band == "5g":
        return 5000 + 5 * channel
    raise ValueError(f"不支持的 WiFi 频段: {band!r}")


def channel_settle_sec(band: str, channel: int, configured_sec: float) -> float:
    settle_sec = max(0.0, float(configured_sec))
    if band == "5g" and 52 <= int(channel) <= 144:
        return max(settle_sec, _DEFAULT_DFS_SETTLE_SEC)
    return settle_sec


def assert_dut_channel(
    run_shell_cmd: Callable[[str], str],
    *,
    band: str,
    channel: int,
    summary: str,
    attempts: int = 10,
    interval_sec: float = 2.0,
) -> None:
    expected_frequency = _wifi_channel_frequency_mhz(band, channel)
    total_attempts = max(1, int(attempts))
    status = ""
    actual_frequency: Optional[int] = None
    for attempt in range(1, total_attempts + 1):
        status = run_shell_cmd("cmd wifi status")
        actual_frequency = frequency_from_wifi_status(status)
        if actual_frequency == expected_frequency:
            print(
                f"[{summary}] DUT channel={channel} "
                f"frequency={actual_frequency}MHz 校验成功"
            )
            return
        if attempt < total_attempts and interval_sec > 0:
            time.sleep(interval_sec)
    pytest.fail(
        f"{summary}: DUT 信道校验失败，AP 目标={band}/{channel} "
        f"({expected_frequency}MHz)，DUT 实际={actual_frequency or '未知'}MHz，"
        f"连续校验={total_attempts}次\ncmd wifi status:\n{status[:800]}"
    )


def _infer_hyperwifi_region_from_title(title: str) -> str:
    t = (title or "").upper()
    if "EU" in t:
        return "EU"
    if "US" in t:
        return "US"
    return "US"


def _normalized_product_tag(case: Dict[str, str]) -> str:
    title = (case.get("title") or "").lower()
    summary = (case.get("case_id") or "").lower()
    raw = (case.get("tag") or "").lower()

    if "hyperwifi" in raw or "hyperwifi" in title or "hyperwifi" in summary:
        return "hyperwifi"
    if raw == "common" or "common" in raw:
        return "common"
    if "wifi" in raw or "wifi" in title or "wifi" in summary:
        return "wifi"
    return raw or "common"


def halow_frequency_mhz(plan: ChannelPlan, bandwidth: Optional[int], channel: int) -> str:
    tables = load_halow_frequency_tables()
    country = (plan.get("country") or "").strip().upper()
    band = (plan.get("band") or "").strip().lower()
    region = tables.get(country) or {}
    keys: List[str] = []

    if country == "US" and bandwidth is not None:
        keys.append(f"bandwidth_{bandwidth}mhz")
    elif country == "EU":
        if "800" in band:
            keys.append("band_800mhz_1mhz")
        elif "900" in band:
            keys.append("band_900mhz_1mhz")
    keys.append("full")

    for key in keys:
        freq_map = region.get(key) or {}
        for freq, ch in freq_map.items():
            if int(ch) == int(channel):
                return f"{int(freq) / 10:.1f}MHz"
    return "N/A"


def pick_wifi_yaml_entry(case: Dict[str, str], wifi_yaml: dict) -> Tuple[Optional[dict], str]:
    wifi_list = wifi_yaml.get("wifi_list") or []
    title = (case.get("title") or "").upper()
    tag = _normalized_product_tag(case).upper()

    if tag == "HYPERWIFI" or "HYPERWIFI" in tag:
        region = _infer_hyperwifi_region_from_title(title)
        if "US" not in title and "EU" not in title:
            print(
                f"[{case.get('case_id') or 'wifi_case'}] "
                f"HyperWiFi 标题未显式包含 US/EU，默认按 US 区域选网"
            )
        for entry in wifi_list:
            if (entry.get("type") or "").lower() != "hyperwifi":
                continue
            if (entry.get("region") or "").upper() == region:
                return entry, ""
        return None, f"wifi_list 无 HyperWiFi region={region} 配置"

    if "2.4" in title:
        for entry in wifi_list:
            if "2.4" in (entry.get("ssid") or ""):
                return entry, ""
    if "5G" in title and "6E" not in title:
        for entry in wifi_list:
            ssid = entry.get("ssid") or ""
            if "5G" in ssid and "6" not in ssid.replace("5G", "", 1):
                return entry, ""
    if "6E" in title or "6G" in title:
        for entry in wifi_list:
            if "6" in (entry.get("ssid") or "").upper():
                return entry, ""

    for entry in wifi_list:
        if (entry.get("type") or "").lower() != "hyperwifi":
            return entry, ""
    return None, "wifi_list 无可用传统 WiFi 配置"


def _hyperwifi_entry_by_region(wifi_yaml: dict, region: str) -> Optional[dict]:
    want = (region or "").strip().upper()
    for entry in wifi_yaml.get("wifi_list") or []:
        if (entry.get("type") or "").lower() != "hyperwifi":
            continue
        if (entry.get("expect") or "").strip().lower() == "auth_fail":
            continue
        if (entry.get("region") or "").strip().upper() == want:
            return entry
    return None


def setup_halow_region_country(
    plan: ChannelPlan,
    *,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    miniap_action: Any,
    entry: WiFiEntry,
    summary: str,
) -> None:
    """按 plan 的 country 同步 Android 与 miniAP 的 Halow 国家码。"""
    region = (plan.get("country") or "").strip().upper()
    if region not in _ANDROID_CC_BY_HALOW_REGION:
        return

    android_cc = (
        plan.get("android_country_code") or _ANDROID_CC_BY_HALOW_REGION[region]
    ).strip().upper()
    require_cli_app(run_shell_cmd)
    print(f"[{summary}] 设置 Android 国家码 {android_cc}（Halow {region}）")
    force_country_and_restart_wifi(
        run_shell_cmd,
        wifi,
        country_code=android_cc,
        wait_after_enable=3.0,
    )

    sid = (
        plan.get("special_id")
        or plan.get("country_code")
        or halow_special_id(region)
    ).strip()
    ssid = (entry.get("ssid") or "").strip()
    pwd = (entry.get("pwd") or "").strip()
    if not sid or not ssid:
        pytest.fail(f"{summary}: miniAP SPECIAL_ID 或 HyperWiFi SSID 配置不完整")

    print(
        f"[{summary}] 设置 miniAP 国家码："
        f"dwrite SPECIAL_ID={sid},COUNTRY_ID={region} ssid={ssid!r}"
    )
    miniap_action.set_countrycode(region, sid, ssid, pwd)


def restore_halow_us_default(
    *,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    miniap_action: Any,
    wifi_yaml: dict,
    summary: str,
) -> None:
    """EU 用例结束后恢复 Android 与 miniAP 到默认 US 配置。"""
    us_entry = _hyperwifi_entry_by_region(wifi_yaml, _DEFAULT_HALOW_REGION)
    if not us_entry:
        print(f"[{summary}] 跳过恢复 US：wifi_yaml 无 US HyperWiFi 配置")
        return

    require_cli_app(run_shell_cmd)
    print(f"[{summary}] 恢复 Android 默认国家码 US")
    force_country_and_restart_wifi(
        run_shell_cmd,
        wifi,
        country_code=_DEFAULT_HALOW_REGION,
        wait_after_enable=3.0,
    )

    if miniap_action is None:
        return

    sid = halow_special_id(_DEFAULT_HALOW_REGION).strip()
    ssid = (us_entry.get("ssid") or "").strip()
    pwd = (us_entry.get("pwd") or "").strip()
    if not sid or not ssid:
        print(f"[{summary}] 跳过恢复 miniAP US：SPECIAL_ID 或 SSID 不完整")
        return

    print(
        f"[{summary}] 恢复 miniAP 默认 US："
        f"dwrite SPECIAL_ID={sid},COUNTRY_ID=US ssid={ssid!r}"
    )
    miniap_action.set_countrycode(_DEFAULT_HALOW_REGION, sid, ssid, pwd)


@allure.step("执行 AP 信道遍历验证")
def run_channel_automation_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    plan: ChannelPlan,
    miniap_action: Any = None,
    wifi_ap_action: Any = None,
) -> None:
    """遍历 AP 信道并校验 DUT 始终关联到目标网络。"""
    summary = case["case_id"]
    attach_wifi_status(summary, run_shell_cmd)
    if not plan:
        pytest.skip(f"{summary}: 未提供信道 plan")
    steps: List[Tuple[Optional[int], int]] = list(iter_channel_steps(plan))
    if not steps:
        pytest.skip(f"{summary}: 信道计划为空")

    wifi_entry_id = str(plan.get("wifi_entry_id") or "").strip()
    wifi_entry_ssid = str(plan.get("wifi_entry_ssid") or "").strip()
    if wifi_entry_id:
        entry = get_wifi_list_entry(wifi_yaml, entry_id=wifi_entry_id)
        reason = f"wifi_list 无 id={wifi_entry_id!r} 的配置"
    elif wifi_entry_ssid:
        entry = get_wifi_list_entry(wifi_yaml, ssid=wifi_entry_ssid)
        reason = f"wifi_list 无 ssid={wifi_entry_ssid!r} 的配置"
    else:
        entry, reason = pick_wifi_yaml_entry(case, wifi_yaml)
    if not entry:
        pytest.skip(reason)
    entry = cast(WiFiEntry, dict(entry))

    configured_ssid = str(plan.get("configured_ssid") or "").strip()
    if configured_ssid:
        entry["ssid"] = configured_ssid

    ssid = (entry.get("ssid") or "").strip()
    driver = (plan.get("driver") or "miniAP").lower()
    total = count_channel_steps(plan)
    if driver == "miniap":
        if miniap_action is None:
            pytest.skip(f"{summary}: miniAP 信道遍历需 MINIAP_LAB=1 且配置 miniAP_ip")
        region = (plan.get("country") or "").strip().upper()
        try:
            if region == "EU":
                setup_halow_region_country(
                    plan,
                    run_shell_cmd=run_shell_cmd,
                    wifi=wifi,
                    miniap_action=miniap_action,
                    entry=entry,
                    summary=summary,
                )
            else:
                miniap_action.set_wifi_profile(
                    ssid=ssid,
                    pwd=(entry.get("pwd") or entry.get("password") or "").strip(),
                    encryption=(entry.get("encrypt") or "WPA3").strip(),
                )
            for bandwidth, channel in steps:
                miniap_action.set_bandwidth_channel(bandwidth, channel)
                print(
                    f"[{summary}] miniAP bandwidth={bandwidth}MHz channel={channel} "
                    f"frequency={halow_frequency_mhz(plan, bandwidth, channel)}"
                )
                assert_wifi_connected(
                    wifi,
                    wifi_yaml,
                    run_shell_cmd,
                    ssid=ssid,
                    allow_any_configured=False,
                )
        finally:
            if region == "EU":
                restore_halow_us_default(
                    run_shell_cmd=run_shell_cmd,
                    wifi=wifi,
                    miniap_action=miniap_action,
                    wifi_yaml=wifi_yaml,
                    summary=summary,
                )
        print(f"[{summary}] 完成 {total} 个信道，关联成功：{ssid!r}")
        return

    if driver != "ap":
        pytest.skip(f"{summary}: 不支持的信道驱动 {driver!r}")
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 传统 WiFi AP 信道遍历需配置 ap_config")
    band = (plan.get("band") or "").strip().lower()
    if band not in ("2g", "5g"):
        pytest.skip(f"{summary}: 当前传统 WiFi AP 不支持 {band or '未指定'} 射频信道自动化")
    security = (entry.get("encrypt") or entry.get("security") or "WPA2").strip().lower()
    security_map = {
        "open": "open",
        "none": "open",
        "wpa": "wpa-aes",
        "wpa2": "wpa2-aes",
        "wpa3": "wpa3-aes",
        "wpa/wpa2": "wpa-wpa2-aes",
        "wpa2/wpa3": "wpa2-wpa3-aes",
    }
    if security not in security_map:
        pytest.skip(f"{summary}: 传统 WiFi AP 暂不支持 YAML 加密方式 {security!r}")
    bandwidth_mhz = int(plan.get("bandwidth_mhz") or 20)
    settle_sec = float(plan.get("settle_sec", 5.0))
    ap_id = plan.get("ap_id")
    original_channel = wifi_ap_action.current_channel(band, ap_id=ap_id)
    try:
        if plan.get("configure_wifi", True):
            wifi_ap_action.configure_wifi(
                ssid=ssid,
                password=(entry.get("pwd") or entry.get("password") or "").strip(),
                security=security_map[security],
                band=band,
            )
        for _, channel in steps:
            wifi_ap_action.set_channel(
                band,
                channel,
                bandwidth_mhz=bandwidth_mhz,
                ap_id=ap_id,
                verify=True,
            )
            current_settle_sec = channel_settle_sec(band, channel, settle_sec)
            if current_settle_sec > 0:
                time.sleep(current_settle_sec)
            if not wifi.disconnect_all():
                pytest.fail(f"{summary}: AP 切换到信道 {channel} 后 DUT 断开 WiFi 失败")
            assert_wifi_connected(
                wifi,
                wifi_yaml,
                run_shell_cmd,
                entry=entry,
                allow_any_configured=False,
            )
            assert_dut_channel(
                run_shell_cmd,
                band=band,
                channel=channel,
                summary=summary,
            )
    finally:
        wifi_ap_action.set_channel(
            band,
            original_channel,
            bandwidth_mhz=bandwidth_mhz,
            ap_id=ap_id,
            verify=True,
        )
    print(f"[{summary}] 完成 {total} 个传统 WiFi AP 信道，关联成功：{ssid!r}")


