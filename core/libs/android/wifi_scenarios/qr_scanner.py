"""Automation runner for WiFi QR scanner connection cases."""
from __future__ import annotations

import multiprocessing
import os
import time
from contextlib import AbstractContextManager
from typing import Any, Dict, Optional, Protocol, Type, cast

import pytest

from core.testdata_loader import get_ssid_pwd_entry
from core.libs.android.wifi_scenarios.lab_requirements import env_enabled
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    assert_gateway_ping,
    assert_ssid_visible_in_scan,
)
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.libs.android.wifi_control.ssid_parsers import saved_network_ssids, ssid_match


class _ReadyEvent(Protocol):
    def set(self) -> None: ...


def _escape_wifi_qr(value: str) -> str:
    escaped = str(value)
    for character in ("\\", ";", ",", ":", '"'):
        escaped = escaped.replace(character, f"\\{character}")
    return escaped


def wifi_qr_payload(ssid: str, password: str, security: str = "WPA2") -> str:
    """Build a payload conforming to the de-facto WiFi QR format."""
    qr_security = (security or "WPA2").strip().upper()
    if qr_security in ("OPEN", "NONE", "NOPASS"):
        qr_security = "nopass"
        password = ""
    elif qr_security in ("WPA", "WPA2", "WPA3", "WPA/WPA2"):
        qr_security = "WPA"
    else:
        raise ValueError(f"二维码不支持的 WiFi 加密方式: {security!r}")

    fields = [f"T:{qr_security}", f"S:{_escape_wifi_qr(ssid)}"]
    if password:
        fields.append(f"P:{_escape_wifi_qr(password)}")
    return f"WIFI:{';'.join(fields)};;"


def _show_qr_window(payload: str, ready: _ReadyEvent) -> None:
    import tkinter as tk

    import qrcode
    from PIL import Image, ImageTk

    image = cast(Image.Image, qrcode.make(payload)).convert("RGB")
    root = tk.Tk()
    root.configure(background="white")
    root.overrideredirect(True)

    geometry = (os.environ.get("WIFI_QR_DISPLAY_GEOMETRY") or "").strip()
    if geometry:
        root.geometry(geometry)
    else:
        root.attributes("-fullscreen", True)

    size = max(320, min(root.winfo_screenwidth(), root.winfo_screenheight()) - 120)
    image = image.resize((size, size))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=photo, background="white", borderwidth=0)
    label.pack(expand=True)
    root.after(100, ready.set)
    root.mainloop()


class WifiQrDisplay(AbstractContextManager["WifiQrDisplay"]):
    """Display a WiFi QR code until the scanner flow finishes."""

    def __init__(self, payload: str, *, ready_timeout: float = 10.0) -> None:
        self.payload = payload
        self.ready_timeout = ready_timeout
        self._process: Optional[multiprocessing.Process] = None

    def __enter__(self) -> "WifiQrDisplay":
        ready = multiprocessing.Event()
        self._process = multiprocessing.Process(
            target=_show_qr_window,
            args=(self.payload, ready),
            daemon=True,
        )
        self._process.start()
        if not ready.wait(self.ready_timeout):
            self.close()
            raise RuntimeError("宿主机二维码窗口未在预期时间内就绪")
        return self

    def close(self) -> None:
        if self._process is not None and self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=3.0)
        self._process = None

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: object,
    ) -> None:
        self.close()


def _wait_for_scanner_connection(
    wifi: WiFiControl,
    ssid: str,
    *,
    timeout_sec: float = 60.0,
) -> None:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        networks = wifi.list_networks_blob()
        if ssid.strip():
            connected = wifi.list_connected_ssids(trust_status_fallback=True)
            is_connected = any(ssid_match(ssid, current) for current in connected)
            is_saved = any(
                ssid_match(ssid, saved) for saved in saved_network_ssids(networks)
            )
        else:
            is_connected = wifi.is_wifi_associated()
            is_saved = f'"{ssid}"' in networks
        if is_connected and is_saved:
            return
        time.sleep(1.0)
    pytest.fail(
        f"扫码后未连接并保存目标网络 {ssid!r}；"
        f"当前={wifi.list_connected_ssids(trust_status_fallback=True)!r}\n"
        f"list-networks:\n{wifi.list_networks_blob()[:800]}"
    )


def _reboot_and_assert_reconnected(
    wifi: WiFiControl,
    ssid: str,
    *,
    summary: str,
) -> None:
    if not env_enabled("WIFI_QR_REBOOT_CHECK"):
        pytest.skip(
            f"{summary}: 扫码、连接和保存网络验证已通过；设置 "
            "WIFI_QR_REBOOT_CHECK=1 后执行重启重连阶段"
        )

    wifi.adb.shell("reboot")
    offline_deadline = time.monotonic() + 30.0
    while time.monotonic() < offline_deadline:
        code, _, _ = wifi.adb.run("get-state", shell=False)
        if code != 0:
            break
        time.sleep(1.0)
    if not wifi.adb.wait_for_device(total_sec=120.0):
        pytest.fail(f"{summary}: DUT 重启后 120 秒内未恢复 ADB")

    boot_deadline = time.monotonic() + 120.0
    while time.monotonic() < boot_deadline:
        code, output, _ = wifi.adb.shell("getprop", "sys.boot_completed")
        if code == 0 and output.strip() == "1":
            break
        time.sleep(2.0)
    else:
        pytest.fail(f"{summary}: DUT 重启后系统未完成启动")

    _wait_for_scanner_connection(wifi, ssid, timeout_sec=90.0)


def run_wifi_scanner_case(
    case: Dict[str, str],
    run_shell_cmd,
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any,
    *,
    entry_id: str,
    entry_point: str = "add_network_entry",
    ap_encoding: str = "utf-8",
    reboot_check: bool = False,
    settle_sec: float = 5.0,
) -> None:
    """Scan a host-displayed QR code and verify connection without ADB connecting."""
    summary = case["case_id"]
    if not env_enabled("WIFI_QR_LAB"):
        pytest.skip(
            f"{summary}: 需设置 WIFI_QR_LAB=1，并将 DUT 摄像头固定朝向二维码显示器"
        )

    entry = get_ssid_pwd_entry(wifi_yaml, entry_id=entry_id)
    if not entry:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 profile id={entry_id!r}")

    encoding = ap_encoding.strip().lower()
    if encoding == "utf-8":
        if wifi_ap_action is None:
            pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
        security = str(entry.get("security") or "WPA2").strip().lower()
        security_map = {"open": "open", "wpa": "wpa-aes", "wpa2": "wpa2-aes"}
        if security not in security_map:
            pytest.skip(f"{summary}: AP 自动配置不支持加密方式 {security!r}")
        wifi_ap_action.configure_wifi(
            ssid=str(entry.get("ssid") or ""),
            password=str(entry.get("password") or ""),
            security=security_map[security],
            band="5g",
        )
        time.sleep(settle_sec)
    elif not env_enabled("WIFI_QR_ENCODING_LAB"):
        pytest.skip(
            f"{summary}: {encoding} SSID 需实验室 AP 预配置，并设置 WIFI_QR_ENCODING_LAB=1"
        )

    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("password") or "")
    security = str(entry.get("security") or "WPA2")
    if ssid.strip():
        assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
    else:
        run_shell_cmd("cmd wifi start-scan")
        time.sleep(4.0)
        print(f"[{summary}] 空格 SSID 无法通过规范化扫描文本唯一识别，改由扫码后关联状态校验")

    payload = wifi_qr_payload(ssid, password, security)
    with WifiQrDisplay(payload):
        settings_ui.open_wifi_qr_scanner(entry_point)
        _wait_for_scanner_connection(wifi, ssid)

    print(f"[{summary}] 二维码扫码连接并保存成功：SSID={ssid!r}")
    assert_gateway_ping(wifi, summary=summary, optional=True)
    if reboot_check:
        _reboot_and_assert_reconnected(wifi, ssid, summary=summary)