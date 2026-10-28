"""Traditional WiFi AP-backed scenario runners."""
from __future__ import annotations

import re
import time
from typing import Any, Callable, Dict, Optional, Sequence, Tuple, cast

import allure
import pytest

from core.testdata_loader import get_ssid_pwd_entry, get_wifi_list_entry
from .ssidpwd_connection import (
    assert_gateway_ping,
    assert_ssid_visible_in_scan,
    run_add_network_connection_case,
)
from core.libs.android.wifi_control.connection_chk import (
    assert_wifi_connected,
)
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import scan_result_capabilities, ssid_match
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI
from core.libs.android.wifi_scenarios.lab_requirements import env_value, require_lab_flag
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.utils.log_handler import get_logger

log = get_logger(__name__)


SECURITY_EXPECTED = {
    "open": "OPEN",
    "wep40": "WEP",
    "wep104": "WEP",
    "wep128": "WEP",
    "wpa-aes": "WPA",
    "wpa-tkip": "WPA",
    "wpa-aes-tkip": "WPA",
    "wpa2-aes": "WPA2",
    "wpa2-tkip": "WPA2",
    "wpa2-aes-tkip": "WPA2",
    "wpa2-aes-pmf-optional": "WPA2",
    "wpa2-aes-pmf-mandatory": "WPA2",
    "wpa-wpa2-aes": "WPA2",
    "wpa-wpa2-tkip": "WPA2",
    "wpa-wpa2-aes-tkip": "WPA2",
    "wpa-wpa2-aes-pmf-optional": "WPA2",
    "wpa-wpa2-aes-pmf-mandatory": "WPA2",
    "wpa2-wpa3-aes": "WPA3",
    "wpa2-wpa3-aes-pmf-mandatory": "WPA3",
    "wpa3-aes": "WPA3",
    "enhanced-open": "OWE",
    "wapi-psk": "WAPI",
}


def _case_ssid(summary: str, security: str) -> str:
    suffix = re.sub(r"[^A-Za-z0-9]", "", security)[:12]
    case_number = (summary or "").rsplit("_", 1)[-1]
    return f"PyAutoTest_{case_number}_{suffix}"[:32]


def run_wifi_ap_security_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    security: str,
    password: str = "24681357",
    band: str = "5g",
    settle_sec: float = 5.0,
) -> None:
    """Configure one security mode and verify scan, association and gateway."""
    summary = case["case_id"]
    attach_wifi_status(summary, run_shell_cmd)
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    key = (security or "").strip().lower()
    if key not in SECURITY_EXPECTED:
        pytest.skip(f"{summary}: 未映射传统 WiFi AP 加密方式 {security!r}")

    ssid = _case_ssid(summary, key)
    secret = "" if key in ("open", "enhanced-open") else password
    with allure.step(f"配置 AP：{key}，频段：{band}"):
        wifi_ap_action.configure_wifi(
            ssid=ssid,
            password=secret,
            security=key,
            band=band,
            verify=True,
        )
        if settle_sec > 0:
            time.sleep(settle_sec)
    with allure.step(f"扫描并确认目标 SSID：{ssid}"):
        assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
    with allure.step(f"连接目标网络：{ssid}"):
        connected = assert_wifi_connected(
            wifi,
            wifi_yaml,
            run_shell_cmd,
            entry={
                "ssid": ssid,
                "pwd": secret,
                "encrypt": SECURITY_EXPECTED[key],
                "type": "normal",
                "expect": "connected",
            },
        )
    print(f"[{summary}] 传统 WiFi AP 加密验证连接成功：{connected!r} security={key}")
    with allure.step("验证网关连通性"):
        assert_gateway_ping(wifi, summary=summary, optional=True)


def run_wifi_ap_manual_add_security_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    add_network_ui: WiFiAddNetworkUI,
    wifi_ap_action: Any,
    *,
    security: str,
    ui_security: str,
    password: str = "24681357",
    band: str = "5g",
    hidden: bool = False,
    ui_hidden: Optional[bool] = None,
    expect_connected: bool = True,
    settle_sec: float = 5.0,
) -> None:
    """Configure AP security and connect through Android's add-network UI."""
    summary = case["case_id"]
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    key = (security or "").strip().lower()
    if key not in SECURITY_EXPECTED:
        pytest.skip(f"{summary}: 未映射传统 WiFi AP 加密方式 {security!r}")

    ssid = _case_ssid(summary, key)
    secret = "" if key in ("open", "enhanced-open") else password
    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=secret,
        security=key,
        band=band,
        hidden=hidden,
        verify=True,
    )
    if settle_sec > 0:
        time.sleep(settle_sec)
    if not hidden:
        assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
    run_add_network_connection_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        add_network_ui,
        profile={
            "ssid": ssid,
            "password": secret,
            "encrypt": SECURITY_EXPECTED[key],
            "type": "normal",
            "expect": "connected" if expect_connected else "auth_fail",
        },
        security=ui_security,
        hidden=ui_hidden,
        expect_connected=expect_connected,
    )


def run_hidden_network_reboot_stress_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    add_network_ui: WiFiAddNetworkUI,
    wifi_ap_action: Any,
) -> None:
    summary = case["case_id"]
    require_lab_flag(
        "HIDDEN_NETWORK_STRESS",
        summary,
        hint="设置 HIDDEN_NETWORK_STRESS=1 后执行隐藏网络重启压力测试",
    )
    duration_sec = float(env_value("HIDDEN_NETWORK_STRESS_DURATION_SEC", "7200"))
    if duration_sec <= 0:
        pytest.fail("HIDDEN_NETWORK_STRESS_DURATION_SEC 必须大于 0")
    run_wifi_ap_manual_add_security_case(
        case,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        add_network_ui,
        wifi_ap_action,
        security="wpa2-aes",
        ui_security="personal",
        hidden=True,
        ui_hidden=True,
    )
    ssid = _case_ssid(summary, "wpa2-aes")
    entry = _connection_entry(ssid, "24681357", "wpa2-aes")
    deadline = time.monotonic() + duration_sec
    attempts = 0
    from .ip_configuration import reboot_and_wait

    while time.monotonic() < deadline:
        reboot_and_wait(wifi)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        assert_gateway_ping(wifi, summary=summary, optional=True)
        attempts += 1
    assert attempts > 0


def run_preconfigured_wifi_security_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    entry_id: str,
    expected_capabilities: Sequence[str] = (),
    ping_gateway: bool = True,
) -> str:
    """Connect to a lab-provisioned SSID and verify its advertised security."""
    summary = case["case_id"]
    entry = get_wifi_list_entry(wifi_yaml, entry_id=entry_id)
    if not entry:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无预置网络 id={entry_id!r}")

    lab_flag = str(entry.get("lab_flag") or "").strip()
    if lab_flag:
        require_lab_flag(
            lab_flag,
            summary,
            hint=f"确认预置网络 {entry_id!r} 可用后设置 {lab_flag}=1",
        )

    ssid = str(entry.get("ssid") or "")
    if not ssid:
        pytest.fail(f"{summary}: 预置网络 {entry_id!r} 的 SSID 不能为空")
    password_env = str(entry.get("password_env") or "").strip()
    if password_env and not str(entry.get("pwd") or "") and not env_value(password_env):
        pytest.skip(f"{summary}: 需通过环境变量 {password_env} 提供预置网络凭据")

    assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
    if expected_capabilities:
        scan = run_shell_cmd("cmd wifi list-scan-results")
        capabilities = scan_result_capabilities(scan, ssid)
        missing = [
            expected
            for expected in expected_capabilities
            if not any(expected.lower() in actual.lower() for actual in capabilities)
        ]
        if missing:
            pytest.fail(
                f"{summary}: SSID={ssid!r} 未广播预期安全能力 {missing!r}，"
                f"实际={capabilities!r}"
            )

    connected = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=cast(WiFiEntry, entry),
    )
    if ping_gateway:
        assert_gateway_ping(wifi, summary=summary, optional=True)
    print(
        f"[{summary}] 预置网络安全验证成功：SSID={connected!r} "
        f"capabilities={list(expected_capabilities)!r}"
    )
    return connected


@allure.step("执行 AP SSID 与密码验证")
def run_wifi_ap_ssid_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    entry_id: str,
    band: str = "5g",
    settle_sec: float = 5.0,
) -> None:
    """Apply one document-backed SSID/password profile and verify connection."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    entry = get_ssid_pwd_entry(wifi_yaml, entry_id=entry_id)
    if not entry:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 profile id={entry_id!r}")
    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("password") or "")
    security = str(entry.get("security") or "WPA2").strip().lower()
    ssid_encoding = str(entry.get("ssid_encoding") or "utf-8").strip().lower()
    security_map = {
        "open": "open",
        "wpa": "wpa-aes",
        "wpa2": "wpa2-aes",
        "wpa3": "wpa3-aes",
    }
    if security not in security_map:
        pytest.skip(f"{summary}: 不支持的 SSID profile 加密方式 {security!r}")

    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=password,
        security=security_map[security],
        band=band,
        ssid_encoding=ssid_encoding,
        verify=True,
    )
    if settle_sec > 0:
        time.sleep(settle_sec)
    assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
    connected = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=cast(
            WiFiEntry,
            {
                **entry,
                "pwd": password,
                "encrypt": security.upper(),
                "type": "normal",
                "expect": "connected",
            },
        ),
    )
    print(f"[{summary}] 传统 WiFi AP SSID/密码验证连接成功：{connected!r}")
    assert_gateway_ping(wifi, summary=summary, optional=True)


def _connection_entry(ssid: str, password: str, security: str) -> WiFiEntry:
    return {
        "ssid": ssid,
        "pwd": password,
        "encrypt": SECURITY_EXPECTED[security],
        "type": "normal",
        "expect": "connected",
    }


def _is_connected_to(wifi: WiFiControl, ssid: str) -> bool:
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    return any(ssid_match(ssid, current) for current in connected)


def _wait_for_connection_state(
    wifi: WiFiControl,
    ssid: str,
    *,
    connected: bool,
    timeout_sec: float,
    interval_sec: float = 0.5,
) -> bool:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if _is_connected_to(wifi, ssid) is connected:
            return True
        time.sleep(interval_sec)
    return _is_connected_to(wifi, ssid) is connected


def _assert_auto_reconnected(
    wifi: WiFiControl,
    ssid: str,
    *,
    summary: str,
    timeout_sec: float,
) -> None:
    if not _wait_for_connection_state(
        wifi, ssid, connected=True, timeout_sec=timeout_sec
    ):
        current = wifi.list_connected_ssids(trust_status_fallback=True)
        pytest.fail(f"{summary}: AP 改配后未自动重连 {ssid!r}，当前={current!r}")
    assert_gateway_ping(wifi, summary=summary, optional=True)


def _assert_stays_disconnected(
    wifi: WiFiControl,
    ssid: str,
    *,
    summary: str,
    disconnect_timeout_sec: float,
    observation_sec: float,
) -> None:
    if not _wait_for_connection_state(
        wifi, ssid, connected=False, timeout_sec=disconnect_timeout_sec
    ):
        pytest.fail(f"{summary}: AP 改配后仍连接 {ssid!r}")
    deadline = time.monotonic() + observation_sec
    while time.monotonic() < deadline:
        if _is_connected_to(wifi, ssid):
            pytest.fail(f"{summary}: AP 改配后意外自动重连 {ssid!r}")
        time.sleep(0.5)


def _require_ap(summary: str, wifi_ap_action: Any) -> None:
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")


def _configure_and_connect(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    ssid: str,
    password: str,
    security: str,
    band: str,
    settle_sec: float,
) -> None:
    wifi_ap_action.configure_wifi(
        ssid=ssid,
        password=password,
        security=security,
        band=band,
    )
    if settle_sec > 0:
        time.sleep(settle_sec)
    assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=_connection_entry(ssid, password, security),
    )
    assert_gateway_ping(wifi, summary=summary, optional=True)


@allure.step("执行 AP SSID 变更验证")
def run_wifi_ap_ssid_change_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    settle_sec: float = 5.0,
    reconnect_timeout_sec: float = 10.0,
) -> None:
    """Connect SSID1, connect SSID2, then verify automatic return to SSID1."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    _require_ap(summary, wifi_ap_action)
    ssid1 = "PyAutoTest_ApChange_1"
    ssid2 = "PyAutoTest_ApChange_2"
    password1 = "24681357"
    password2 = "87654321"
    security = "wpa2-aes"

    try:
        _configure_and_connect(
            summary, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action,
            ssid=ssid1, password=password1, security=security,
            band="5g", settle_sec=settle_sec,
        )
        _configure_and_connect(
            summary, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action,
            ssid=ssid2, password=password2, security=security,
            band="5g", settle_sec=settle_sec,
        )
        wifi_ap_action.configure_wifi(
            ssid=ssid1, password=password1, security=security, band="5g"
        )
        _assert_auto_reconnected(
            wifi, ssid1, summary=summary, timeout_sec=reconnect_timeout_sec
        )
    finally:
        wifi_ap_action.configure_wifi(
            ssid=ssid1, password=password1, security=security, band="5g"
        )


@allure.step("执行 AP 密码变更验证")
def run_wifi_ap_password_change_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    settle_sec: float = 5.0,
    reconnect_timeout_sec: float = 10.0,
) -> None:
    """Verify wrong AP password disconnects and restoring it reconnects."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    _require_ap(summary, wifi_ap_action)
    ssid = "PyAutoTest_ApChange_Pwd"
    password1 = "24681357"
    password2 = "87654321"
    security = "wpa2-aes"

    try:
        _configure_and_connect(
            summary, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action,
            ssid=ssid, password=password1, security=security,
            band="5g", settle_sec=settle_sec,
        )
        wifi_ap_action.configure_wifi(
            ssid=ssid, password=password2, security=security, band="5g"
        )
        _assert_stays_disconnected(
            wifi,
            ssid,
            summary=summary,
            disconnect_timeout_sec=reconnect_timeout_sec,
            observation_sec=3.0,
        )
        wifi_ap_action.configure_wifi(
            ssid=ssid, password=password1, security=security, band="5g"
        )
        _assert_auto_reconnected(
            wifi, ssid, summary=summary, timeout_sec=reconnect_timeout_sec
        )
    finally:
        wifi_ap_action.configure_wifi(
            ssid=ssid, password=password1, security=security, band="5g"
        )


@allure.step("执行 AP 加密变更验证")
def run_wifi_ap_security_change_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    initial_security: str,
    transitions: Sequence[Tuple[str, bool]],
    settle_sec: float = 5.0,
    reconnect_timeout_sec: float = 10.0,
) -> None:
    """Change security modes and verify expected automatic reconnect behavior."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    _require_ap(summary, wifi_ap_action)
    ssid = "PyAutoTest_ApChange_Security"
    password = "24681357"

    try:
        _configure_and_connect(
            summary, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action,
            ssid=ssid, password=password, security=initial_security,
            band="5g", settle_sec=settle_sec,
        )
        for security, expect_reconnect in transitions:
            secret = "" if security in ("open", "enhanced-open") else password
            wifi_ap_action.configure_wifi(
                ssid=ssid,
                password=secret,
                security=security,
                band="5g",
            )
            if expect_reconnect:
                _assert_auto_reconnected(
                    wifi,
                    ssid,
                    summary=summary,
                    timeout_sec=reconnect_timeout_sec,
                )
            else:
                _assert_stays_disconnected(
                    wifi,
                    ssid,
                    summary=summary,
                    disconnect_timeout_sec=reconnect_timeout_sec,
                    observation_sec=3.0,
                )
    finally:
        wifi_ap_action.configure_wifi(
            ssid=ssid,
            password=password,
            security=initial_security,
            band="5g",
        )


@allure.step("执行 AP 信道变更验证")
def run_wifi_ap_channel_change_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    wifi_ap_action: Any,
    *,
    settle_sec: float = 5.0,
    reconnect_timeout_sec: float = 10.0,
) -> None:
    """Change 5 GHz channel/bandwidth and verify the saved network reconnects."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    _require_ap(summary, wifi_ap_action)
    ssid = "PyAutoTest_ApChange_Channel"
    password = "24681357"
    security = "wpa2-aes"

    try:
        wifi_ap_action.set_channel("5g", 36, bandwidth_mhz=20, verify=True)
        _configure_and_connect(
            summary, run_shell_cmd, wifi, wifi_yaml, wifi_ap_action,
            ssid=ssid, password=password, security=security,
            band="5g", settle_sec=settle_sec,
        )
        wifi_ap_action.set_channel("5g", 149, bandwidth_mhz=80, verify=True)
        _assert_auto_reconnected(
            wifi, ssid, summary=summary, timeout_sec=reconnect_timeout_sec
        )
    finally:
        wifi_ap_action.set_channel("5g", 36, bandwidth_mhz=20, verify=True)


