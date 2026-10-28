"""Android Welcome WLAN ssid display scenarios."""
from __future__ import annotations

import time
from typing import Any, Callable

import allure
import pytest

from core.libs.android.wifi_scenarios.ssidpwd_connection import assert_ssid_visible_in_scan
from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI
from core.testdata_loader import get_ssid_pwd_entry
from core.utils.log_handler import get_logger


WELCOME_SSID_PROFILE_BY_CASE = {
    "Func_Components_Welcome_SsidShow_UI_001": "ssid_utf8_chinese_10",
    "Func_Components_Welcome_SsidShow_UI_002": "ssid_gbk_chinese_16",
    "Func_Components_Welcome_SsidShow_UI_003": "ssid_cp949_korean",
    "Func_Components_Welcome_SsidShow_UI_004": "ssid_shift_jis_japanese_16",
    "Func_Components_Welcome_SsidShow_UI_005": "ssid_special_chars_32",
    "Func_Components_Welcome_SsidShow_UI_006": "welcome_ssid_ascii_display",
    "Func_Components_Welcome_SsidShow_UI_007": "welcome_ssid_numeric_display",
    "Func_Components_Welcome_SsidShow_UI_009": "ssid_numeric_32_password_64",
}


def run_welcome_encoded_ssid_display_case(
    case_id, run_shell_cmd, wifi_yaml, settings_ui, tmp_path, capsys,
    wifi_ap_action,
) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    with capsys.disabled():
        run_welcome_ssid_display_case(
            case_id, run_shell_cmd, wifi_yaml, welcome_wlan_ui, wifi_ap_action,
            entry_id=WELCOME_SSID_PROFILE_BY_CASE[case_id],
        )


def _welcome_ssid_for_case(wifi_yaml: dict, case_id: str) -> str:
    profile_id = WELCOME_SSID_PROFILE_BY_CASE[case_id]
    entry = get_ssid_pwd_entry(wifi_yaml, entry_id=profile_id)
    ssid = str(entry.get("ssid") or "")
    if not ssid:
        pytest.skip(f"wifi_ssid.yaml 缺少 {profile_id!r} 测试数据")
    return ssid


def _assert_welcome_ssid_visible(target_ssid, settings_ui, tmp_path, capsys) -> None:
    # Step 3: 创建 Welcome WLAN 页面对象，保存失败时的截图和页面层级。
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")

    # Step 4: 从 WLAN 列表顶部向下查找目标 SSID；遇到“展开全部”自动展开后继续。
    if welcome_wlan_ui.find_ssid(target_ssid):
        message = f"AP的SSID设置为\"{target_ssid}\"，设备welcome组件WLAN列表显示对应SSID正常"
        get_logger(__name__).info("%s", message)

    # Step 5: 绕过 pytest 输出捕获，在终端单独输出本条成功结果。
        with capsys.disabled():
            print()
            print(message, flush=True)
        return

    # Step 5: 列表已滑到底仍未找到目标 SSID，输出失败原因并保存失败产物。
    message = (
        f"AP的SSID设置为\"{target_ssid}\"，设备welcome组件WLAN列表没有发现对应SSID，"
        "请确认环境中是否有对应SSID的AP"
    )
    get_logger(__name__).info("%s", message)
    with capsys.disabled():
        print()
        print(message, flush=True)
    welcome_wlan_ui.fail_with_artifacts(message)


def run_welcome_preconfigured_ssid_display_case(
    wifi_yaml, settings_ui, tmp_path, capsys, wifi_case
) -> None:
    target_ssid = _welcome_ssid_for_case(wifi_yaml, wifi_case["case_id"])
    _assert_welcome_ssid_visible(
        target_ssid,
        settings_ui,
        tmp_path,
        capsys,
    )


@allure.step("Verify encoded SSID display on Welcome WLAN")
def run_welcome_ssid_display_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi_yaml: dict,
    welcome_wlan_ui: WelcomeWlanUI,
    wifi_ap_action: Any,
    *,
    entry_id: str,
    settle_sec: float = 5.0,
) -> None:
    if wifi_ap_action is None:
        pytest.skip(f"{summary}: traditional WiFi AP ap_config is required")
    entry = get_ssid_pwd_entry(wifi_yaml, entry_id=entry_id)
    ssid = str(entry.get("ssid") or "")
    if not ssid:
        pytest.skip(f"{summary}: missing SSID profile {entry_id!r}")

    password = str(entry.get("password") or "24681357")
    encoding = str(entry.get("ssid_encoding") or "utf-8")
    attach_wifi_status(summary, run_shell_cmd)
    try:
        with allure.step(f"Configure AP SSID {ssid!r} using {encoding}"):
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
        with allure.step("Wait for the exact SSID on the Welcome WLAN list"):
            if not welcome_wlan_ui.wait_for_ssid(ssid):
                welcome_wlan_ui.fail_with_artifacts(
                    f"{summary}: Welcome WLAN did not display SSID {ssid!r}, "
                    f"encoding={encoding!r}, although the device scan found it"
                )
        message = (
            f"[{summary}] Welcome WLAN displayed SSID={ssid!r}, "
            f"encoding={encoding!r}"
        )
        get_logger(__name__).info("%s", message)
        print(message, flush=True)
    finally:
        with allure.step("Stop broadcasting the automation VAP"):
            wifi_ap_action.teardown_wifi()
