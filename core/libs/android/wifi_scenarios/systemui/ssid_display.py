"""SystemUI SSID display scenarios."""
from __future__ import annotations

import re
import time
from typing import Any, Callable
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    assert_ssid_visible_in_scan,
)
from core.libs.android.systemui_pages.quick_settings_page import (
    capture_systemui,
    open_all_wifi_networks,
    open_internet_dialog,
)
from core.libs.android.wifi_scenarios.systemui.scan_assertions import (
    visible_systemui_ssids,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_ssid_pwd_entry


_SSID_SHOW_PROFILES = {
    1: "ssid_utf8_chinese_10",
    2: "ssid_gbk_chinese_16",
    3: "ssid_cp949_korean",
    4: "ssid_shift_jis_japanese_16",
    5: "ssid_special_chars_32",
    6: "ssid_ascii_min_password_min",
    7: "ssid_numeric_min",
    8: "ssid_cjk_phrase",
    9: "ssid_numeric_32_password_64",
}


@allure.step("执行 SystemUI SSID 显示验证")
def run_systemui_ssid_display_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    wifi_ap_action: Any,
    *,
    settle_sec: float = 5.0,
) -> None:
    """Configure one SSID profile and assert its exact SystemUI rendering."""
    attach_wifi_status(summary, run_shell_cmd)
    match = re.search(r"SsidShow_UI_(\d{3})$", summary)
    number = int(match.group(1)) if match else 0
    profile_id = _SSID_SHOW_PROFILES.get(number)
    if profile_id is None:
        raise ValueError(f"未知 SystemUI SsidShow 用例: {summary}")
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: 需配置传统 WiFi AP ap_config")
    entry = get_ssid_pwd_entry(wifi_yaml, entry_id=profile_id)
    if not entry:
        pytest.skip(f"{summary}: wifi_ssid.yaml 无 profile id={profile_id!r}")

    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("password") or "24681357")
    encoding = str(entry.get("ssid_encoding") or "utf-8")
    try:
        wifi_ap_action.configure_wifi(
            ssid=ssid,
            password=password,
            security="wpa2-aes",
            band="5g",
            ssid_encoding=encoding,
            verify=True,
        )
        if settle_sec > 0:
            time.sleep(settle_sec)
        assert_ssid_visible_in_scan(run_shell_cmd, ssid, summary=summary)
        open_internet_dialog(settings_ui, capture=False)
        deadline = time.monotonic() + 10.0
        visible: tuple[str, ...] = ()
        while time.monotonic() < deadline:
            visible = visible_systemui_ssids(settings_ui)
            if ssid in visible:
                capture_systemui(settings_ui, f"ssid_show_{number:03d}")
                print(
                    f"[{summary}] SystemUI 已精确显示 SSID={ssid!r}, "
                    f"encoding={encoding!r}"
                )
                return
            time.sleep(1.0)
        open_all_wifi_networks(settings_ui)
        target = settings_ui.device(packageName="com.android.settings", text=ssid)
        if not target.wait(timeout=10.0):
            settings_ui.fail_with_artifacts(
                f"{summary}: SystemUI 首屏及查看全部列表均未精确显示 "
                f"SSID {ssid!r}，首屏可见={visible!r}"
            )
        hierarchy = capture_systemui(settings_ui, f"ssid_show_{number:03d}_all")
        root = ElementTree.fromstring(hierarchy)
        exact_matches = [
            node for node in root.iter("node") if node.get("text", "") == ssid
        ]
        if len(exact_matches) != 1:
            pytest.fail(
                f"{summary}: 查看全部列表应精确显示一次 SSID {ssid!r}，"
                f"实际次数={len(exact_matches)}"
            )
        print(
            f"[{summary}] SystemUI 查看全部已精确显示 SSID={ssid!r}, "
            f"encoding={encoding!r}"
        )
    finally:
        wifi_ap_action.teardown_wifi()
