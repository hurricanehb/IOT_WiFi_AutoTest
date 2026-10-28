"""SSID、密码与手动连接场景。"""
from __future__ import annotations

import os
import re
import time
from typing import Callable, Dict, List, Optional, Tuple, cast

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.ip_configuration import (
    assert_gateway_reachable,
    wait_for_wifi_ipv4,
)

from core.testdata_loader import get_ssid_pwd_entry, get_wifi_list_entry
from core.libs.access_points import MiniAPAction
from core.libs.android.wifi_scenarios.lab_requirements import (
    env_enabled as _env_bool,
    env_value as _env,
    require_lab_flag,
)
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.entries import WiFiEntry
from core.libs.android.wifi_control.ssid_parsers import scan_result_ssids, ssid_match
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI
from core.utils.config_loader import get_settings
from core.utils.log_handler import get_logger

log = get_logger(__name__)

_GATEWAY_RE = re.compile(r"default\s+via\s+(\d+\.\d+\.\d+\.\d+)")


def _resolve_entry(
    wifi_yaml: dict,
    *,
    entry_id: Optional[str] = None,
    profile: Optional[Dict[str, str]] = None,
    summary: str,
) -> dict:
    if profile:
        return dict(profile)
    if entry_id:
        entry = get_ssid_pwd_entry(wifi_yaml, entry_id=entry_id)
        if entry:
            return entry
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 SSID/密码 profile id={entry_id!r}")
    pytest.fail(f"{summary}: 需传入 entry_id 或 profile")


def _apply_miniap_profile_if_enabled(summary: str, entry: dict) -> dict:
    """可选：按 wifi_ssid.yaml 条目自动下发 miniAP SSID/密码/加密。"""
    if not _env_bool("SSIDPWD_MINIAP_AUTOCFG", "0"):
        return entry

    entry = dict(entry)

    settings = get_settings()
    cfg = settings.miniAP_config
    if not (cfg.miniAP_ip or "").strip():
        pytest.skip(f"{summary}: SSIDPWD_MINIAP_AUTOCFG=1 但未配置 miniAP_ip")
    if not (cfg.miniAP_login_password or "").strip():
        pytest.skip(
            f"{summary}: SSIDPWD_MINIAP_AUTOCFG=1 但未配置环境变量 MINIAP_LOGIN_PASSWORD"
        )

    ssid = (entry.get("ssid") or "").strip()
    password = (entry.get("password") or "").strip()
    security = (entry.get("security") or "WPA2").strip()
    miniap_encrypt = security
    if security.lower() not in ("open", "none"):
        miniap_encrypt = "WPA3"
    if not ssid:
        pytest.skip(f"{summary}: 自动下发 miniAP 时 SSID 不能为空")

    action = MiniAPAction(settings=settings)
    try:
        log.info(
            "%s: 自动下发 miniAP 配置 ssid=%r encrypt=%r (source=%r)",
            summary,
            ssid,
            miniap_encrypt,
            security,
        )
        action.set_wifi_profile(ssid=ssid, pwd=password, encryption=miniap_encrypt)
        applied = action.read_wifi_profile_summary()
        if applied:
            log.info("%s: miniAP 当前配置:\n%s", summary, applied)
        entry["security"] = miniap_encrypt
    except Exception as exc:
        pytest.fail(f"{summary}: miniAP 自动配置失败: {exc}")
    finally:
        action.close()

    return entry


def _restore_miniap_profile_if_enabled(summary: str, wifi_yaml: dict, applied: bool) -> None:
    """用例结束后恢复 miniAP 默认 SSID/密码/加密。"""
    if not applied:
        return
    if not (
        _env_bool("SSIDPWD_MINIAP_AUTOCFG", "0")
        or _env_bool("SSIDPWD_MINIAP_RESTORE", "0")
    ):
        return

    restore_id = (os.environ.get("SSIDPWD_MINIAP_RESTORE_ID") or "").strip()
    if restore_id:
        restore_entry = get_ssid_pwd_entry(wifi_yaml, entry_id=restore_id)
        restore_source = f"restore_id={restore_id}"
        if not restore_entry:
            log.warning(
                "%s: SSIDPWD_MINIAP_RESTORE_ID=%r 未在 wifi_ssid.yaml 找到，改用 US 默认恢复配置",
                summary,
                restore_id,
            )
    else:
        restore_entry = {}
        restore_source = "wifi_list US default"

    if not restore_entry:
        restore_entry = next(
            (
                entry
                for entry in wifi_yaml.get("wifi_list") or []
                if (entry.get("type") or "").strip().lower() == "hyperwifi"
                and (entry.get("region") or "").strip().upper() == "US"
                and (entry.get("expect") or "").strip().lower() == "connected"
            ),
            {},
        )
        restore_source = "wifi_list US default"

    if not restore_entry:
        log.warning("%s: 未找到 miniAP US 默认恢复配置，跳过恢复", summary)
        print(f"[{summary}] 跳过恢复环境：未找到 wifi_list 的 US HyperWiFi 条目")
        return

    settings = get_settings()
    if not (settings.miniAP_config.miniAP_login_password or "").strip():
        log.warning("%s: 未配置 MINIAP_LOGIN_PASSWORD，跳过 miniAP 环境恢复", summary)
        print(f"[{summary}] 跳过恢复环境：未配置环境变量 MINIAP_LOGIN_PASSWORD")
        return
    action = MiniAPAction(settings=settings)
    try:
        ssid = (restore_entry.get("ssid") or "").strip()
        password = (restore_entry.get("password") or restore_entry.get("pwd") or "").strip()
        security = (restore_entry.get("security") or restore_entry.get("encrypt") or "WPA2").strip()
        print(
            f"[{summary}] 恢复环境 SSID={ssid!r} "
            f"(source={restore_source}, security={security})"
        )
        action.set_wifi_profile(ssid=ssid, pwd=password, encryption=security)
        log.info(
            "%s: miniAP 已恢复默认配置 source=%s ssid=%r",
            summary,
            restore_source,
            ssid,
        )
        print(f"[{summary}] 恢复环境完成：SSID={ssid!r}")
    except Exception as exc:
        # 恢复失败仅记录，不覆盖用例主断言结果。
        log.warning("%s: miniAP 恢复默认配置失败: %s", summary, exc)
        print(f"[{summary}] 恢复环境失败: {exc}")
    finally:
        action.close()


def restore_miniap_default_if_enabled(wifi_yaml: dict, *, summary: str = "module_teardown") -> None:
    """供模块级 teardown 调用：恢复 miniAP 到默认 US HyperWiFi 配置。"""
    _restore_miniap_profile_if_enabled(summary, wifi_yaml, applied=True)


def _default_gateway(adb) -> Optional[str]:
    code, out, err = adb.shell("ip", "route", "show", "table", "all")
    text = ((out or "") + (err or "")).strip()
    if code != 0 or not text:
        return None
    match = _GATEWAY_RE.search(text)
    return match.group(1) if match else None


def _ping_gateway(adb, gateway: str) -> Tuple[int, str]:
    code, out, err = adb.shell("ping", "-c", "1", "-W", "3", gateway)
    return code, ((out or "") + (err or "")).strip()


def assert_gateway_ping(
    wifi: WiFiControl,
    *,
    summary: str,
    optional: bool = False,
) -> None:
    gateway = _default_gateway(wifi.adb)
    if not gateway:
        if optional:
            log.warning("%s: 未解析到默认网关，跳过 ping", summary)
            return
        pytest.fail(f"{summary}: 未解析到默认网关")
    code, blob = _ping_gateway(wifi.adb, gateway)
    print(f"[{summary}] ping {gateway}: exit={code}\n{blob[:300]}")
    if code != 0:
        pytest.fail(f"{summary}: ping 网关 {gateway} 失败：\n{blob[:400]}")


@allure.step("执行 miniAP 兼容性验证")
def run_nrc_miniap_compatibility_case(
    case: Dict[str, str],
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    miniap_action: Optional[MiniAPAction],
) -> str:
    """Configure the NRC miniAP and verify DUT association and gateway access."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    require_lab_flag(
        "MINIAP_LAB",
        summary,
        hint="需连接 config/test_config.json 中配置的 NRC miniAP",
    )
    if miniap_action is None:
        pytest.skip(f"{summary}: 未配置 miniAP_ip")

    entry = get_wifi_list_entry(
        wifi_yaml,
        wifi_type="hyperwifi",
        expect="connected",
    )
    if not entry:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无可用 HyperWiFi 配置")

    ssid = str(entry.get("ssid") or "").strip()
    password = str(entry.get("password") or entry.get("pwd") or "").strip()
    security = str(entry.get("security") or entry.get("encrypt") or "WPA3").strip()
    if not ssid:
        pytest.fail(f"{summary}: HyperWiFi SSID 不能为空")

    try:
        miniap_action.set_wifi_profile(
            ssid=ssid,
            pwd=password,
            encryption=security,
        )
    except (TimeoutError, ConnectionError, OSError) as exc:
        pytest.skip(f"{summary}: NRC miniAP Telnet 不可达：{exc}")
    connected = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=cast(WiFiEntry, entry),
    )
    assert_gateway_ping(wifi, summary=summary)
    print(f"[{summary}] NRC miniAP 兼容性验证成功：SSID={connected!r}")
    return connected


def assert_ssid_visible_in_scan(
    run_shell_cmd: Callable[[str], str],
    ssid: str,
    *,
    summary: str,
    attempts: int = 3,
    scan_wait_sec: float = 6.0,
) -> None:
    total_attempts = max(1, int(attempts))
    scan = ""
    for attempt in range(1, total_attempts + 1):
        run_shell_cmd("cmd wifi start-scan")
        if scan_wait_sec > 0:
            time.sleep(scan_wait_sec)
        scan = run_shell_cmd("cmd wifi list-scan-results")
        print(
            f"[{summary}] scan attempt {attempt}/{total_attempts} "
            f"results 摘录（前 800 字符）：\n{scan[:800]}"
        )
        if any(ssid_match(ssid, candidate) for candidate in scan_result_ssids(scan)):
            return
    pytest.fail(
        f"{summary}: 连续扫描 {total_attempts} 次未找到 SSID={ssid!r}"
    )


def run_ssidpwd_connect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    entry_id: Optional[str] = None,
    profile: Optional[Dict[str, str]] = None,
    ping_gateway: bool = True,
    check_scan: bool = False,
    reboot_check: bool = False,
) -> str:
    """连接指定 SSID/密码，校验关联与 ping 网关。"""
    entry = _resolve_entry(
        wifi_yaml, entry_id=entry_id, profile=profile, summary=summary
    )
    entry = _apply_miniap_profile_if_enabled(summary, entry)
    if _env_bool("SSIDPWD_MINIAP_AUTOCFG", "0"):
        # miniAP 改配后重启 DUT WiFi，减少旧关联/缓存状态干扰。
        wifi.set_wifi_enabled(False)
        time.sleep(1.0)
        wifi.set_wifi_enabled(True)
        time.sleep(3.0)

    target = str(entry.get("ssid") or "")
    if check_scan:
        assert_ssid_visible_in_scan(run_shell_cmd, target, summary=summary)

    connected = assert_wifi_connected(
        wifi,
        wifi_yaml,
        run_shell_cmd,
        entry=cast(
            WiFiEntry,
            {
                **entry,
                "pwd": entry.get("password", ""),
                "encrypt": entry.get("security", "WPA2"),
            },
        ),
    )
    print(f"[{summary}] 已连接 SSID={connected!r}")

    if ping_gateway:
        require_gateway = _env_bool("SSIDPWD_REQUIRE_GATEWAY", "0")
        assert_gateway_ping(
            wifi,
            summary=summary,
            optional=not require_gateway,
        )

    if reboot_check and _env_bool("SSIDPWD_REBOOT_CHECK", "0"):
        print(f"[{summary}] 重启后重连校验（SSIDPWD_REBOOT_CHECK=1）")
        run_shell_cmd("reboot")
        pytest.skip(f"{summary}: 已触发 reboot，请设备上线后手动重跑验证自动重连")

    return connected


def run_ssidpwd_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    ap1_id: str,
    ap2_id: str,
    ping_gateway: bool = True,
) -> None:
    """依次连接 AP1/AP2，再切回 AP1。"""
    run_ssidpwd_connect_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id=ap1_id,
        ping_gateway=ping_gateway,
    )
    run_ssidpwd_connect_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id=ap2_id,
        ping_gateway=ping_gateway,
    )
    run_ssidpwd_connect_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id=ap1_id,
        ping_gateway=ping_gateway,
    )
    log.info("%s: AP1→AP2→AP1 切换连接完成", summary)


def run_ssidpwd_qr_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    entry_id: str,
) -> None:
    """连接后校验已保存网络；分享二维码步骤需 UI 或第二终端。"""
    entry = _resolve_entry(wifi_yaml, entry_id=entry_id, summary=summary)
    target = (entry.get("ssid") or "").strip()

    run_ssidpwd_connect_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id=entry_id,
        ping_gateway=False,
    )

    networks = wifi.list_networks_blob()
    print(f"[{summary}] list-networks 摘录：\n{networks[:800]}")
    if target and not ssid_match(target, networks):
        pytest.fail(f"{summary}: 已保存网络列表中未找到 SSID={target!r}")

    if _env("SSIDPWD_QR_SCAN_DONE") not in ("1", "true", "yes", "on"):
        pytest.skip(
            f"{summary}: 连接与保存网络已通过；请在网络详情点击「分享二维码」并由其他终端扫码后 "
            f"设置 SSIDPWD_QR_SCAN_DONE=1 重跑完成步骤3"
        )
    log.info("%s: 二维码分享流程已由实验室确认", summary)


def run_ssidpwd_encoding_change_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    entry_id: str,
) -> None:
    """Excp_001：AP UTF-8/GBK 编码切换需陪测 AP 改配。"""
    require_lab_flag(
        "SSIDPWD_ENCODING_LAB",
        summary,
        hint="请先在 AP 上完成 UTF-8→GBK→UTF-8 改配",
    )
    phase = _env("SSIDPWD_ENCODING_PHASE", "utf8")
    if phase == "utf8":
        run_ssidpwd_connect_case(
            summary,
            run_shell_cmd,
            wifi,
            wifi_yaml,
            entry_id=entry_id,
        )
        pytest.skip(
            f"{summary}: UTF-8 连接已通过；请 AP 改 GBK（SSID 不变）后 "
            f"设置 SSIDPWD_ENCODING_PHASE=gbk 重跑"
        )
    if phase == "gbk":
        status = run_shell_cmd("cmd wifi status")
        print(f"[{summary}] GBK 改配后 status:\n{status}")
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if not connected:
            pytest.fail(f"{summary}: GBK 改配后未保持连接，当前={connected!r}")
        pytest.skip(
            f"{summary}: GBK 阶段连接状态已采集；请 AP 改回 UTF-8 后 "
            f"设置 SSIDPWD_ENCODING_PHASE=utf8_restore 重跑"
        )
    if phase == "utf8_restore":
        run_ssidpwd_connect_case(
            summary,
            run_shell_cmd,
            wifi,
            wifi_yaml,
            entry_id=entry_id,
        )
        return
    pytest.skip(
        f"{summary}: 未知 SSIDPWD_ENCODING_PHASE={phase!r}，"
        f"可用 utf8|gbk|utf8_restore"
    )


def run_manual_network_connect_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    *,
    entry_id: str,
    reboot_check: bool = False,
) -> str:
    """连接实验室中按配置手动准备的 WiFi 网络。"""
    if not _env_bool("SSIDPWD_MINIAP_AUTOCFG"):
        require_lab_flag(
            "MANUAL_WIFI_LAB",
            summary,
            hint="请按 wifi_ssid.yaml 对应 manual_* 条目配置陪测 AP",
        )
    connected = run_ssidpwd_connect_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        entry_id=entry_id,
        check_scan=True,
        reboot_check=reboot_check,
    )
    if reboot_check and not _env_bool("SSIDPWD_REBOOT_CHECK"):
        pytest.skip(
            f"{summary}: 连接、扫描和网关验证已通过；设置 "
            "SSIDPWD_REBOOT_CHECK=1 后执行重启重连阶段"
        )
    return connected


def run_add_network_field_case(
    add_network_ui: WiFiAddNetworkUI,
    *,
    ssid: str,
    password: str = "24681357",
    security: str = "personal",
    expect_save_enabled: bool,
    expect_save_rejected: bool = False,
    wifi: WiFiControl | None = None,
) -> None:
    add_network_ui.open()
    try:
        actual_ssid = add_network_ui.set_ssid(ssid)
        add_network_ui.select_security(security)
        actual_password = ""
        if security != "open":
            actual_password = add_network_ui.set_password(password)
        rejected = actual_ssid != ssid or (
            security != "open" and actual_password != password
        )
        enabled = add_network_ui.save_enabled()
        if expect_save_rejected and not rejected and enabled:
            message = add_network_ui.save_rejection_message()
            if wifi is None:
                pytest.fail("校验保存失败结果需要 WiFiControl")
            saved = wifi.list_networks_blob()
            if ssid_match(ssid, saved):
                pytest.fail(f"超长 SSID {ssid!r} 不应保存，list-networks={saved!r}")
            if message:
                log.info("超长 SSID 保存失败提示：%s", message)
            else:
                log.info("超长 SSID 未保存；ROM 瞬时提示未被 UI 自动化捕获")
            return
        assert enabled is expect_save_enabled or (
            not expect_save_enabled and rejected
        ), (
            f"添加网络字段校验不符合预期: save_enabled={enabled}, "
            f"ssid={actual_ssid!r}, password={actual_password!r}"
        )
    finally:
        add_network_ui.cancel()


def run_add_network_connection_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    add_network_ui: WiFiAddNetworkUI,
    *,
    entry_id: Optional[str] = None,
    profile: Optional[Dict[str, str]] = None,
    security: str = "personal",
    hidden: Optional[bool] = None,
    expect_connected: bool = True,
) -> None:
    if entry_id or profile:
        entry = _resolve_entry(
            wifi_yaml, entry_id=entry_id, profile=profile, summary=summary
        )
    else:
        entry = get_wifi_list_entry(
            wifi_yaml, wifi_type="normal", expect="connected"
        )
        if not entry:
            pytest.skip(f"{summary}: wifi_list 无可用普通 WiFi 配置")
    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("password") or entry.get("pwd") or "")
    wifi.set_wifi_enabled(False)
    wifi.set_wifi_enabled(True)
    add_network_ui.open()
    add_network_ui.set_ssid(ssid)
    add_network_ui.select_security(security)
    if security != "open":
        add_network_ui.set_password(password)
    if hidden is not None:
        add_network_ui.select_hidden(hidden)
    add_network_ui.save()
    deadline = time.monotonic() + (45.0 if hidden else 20.0)
    saved = ""
    connected: List[str] = []
    while time.monotonic() < deadline:
        saved = wifi.list_networks_blob()
        connected = wifi.list_connected_ssids(trust_status_fallback=True)
        if ssid_match(ssid, saved) or any(
            ssid_match(ssid, current) for current in connected
        ):
            break
        time.sleep(1.0)
    assert ssid_match(ssid, saved) or any(
        ssid_match(ssid, current) for current in connected
    ), f"{summary}: 添加网络后未保存或连接 SSID={ssid!r}"
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    matched = any(ssid_match(ssid, value) for value in connected)
    if expect_connected:
        if not matched:
            assert_wifi_connected(
                wifi,
                wifi_yaml,
                run_shell_cmd,
                entry=cast(WiFiEntry, {**entry, "pwd": password}),
            )
        info = wait_for_wifi_ipv4(run_shell_cmd)
        assert_gateway_reachable(run_shell_cmd, info.gateway)
    else:
        assert not matched, (
            f"{summary}: 不存在或安全性不匹配的网络不应连接，实际={connected!r}"
        )


def run_add_network_switch_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    wifi_yaml: dict,
    add_network_ui: WiFiAddNetworkUI,
) -> None:
    entries = [
        entry
        for entry in wifi_yaml.get("wifi_list") or []
        if (entry.get("type") or "normal").lower() == "normal"
        and (entry.get("expect") or "connected").lower() == "connected"
        and (entry.get("encrypt") or "").upper() != "OPEN"
    ]
    if len(entries) < 2:
        pytest.skip(f"{summary}: 需要 wifi_list 中至少两个可连接普通 WiFi")
    first, second = entries[:2]
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=first)
    run_add_network_connection_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        add_network_ui,
        profile=second,
    )
