"""Android Welcome WLAN connection config scenarios."""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome._helpers import (
    _wait_for_wifi_connection,
    _wait_for_wifi_disconnection,
)
from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI
from core.testdata_loader import get_wifi_list_entry
from core.utils.log_handler import get_logger


WELCOME_ENCRYPTED_ENTRY_ID = "welcome_connection_wpa2"


WELCOME_OPEN_ENTRY_ID = "welcome_connection_open"


log = get_logger(__name__)


WELCOME_CONN_CFG_017_WRONG_PASSWORD = "87654321"


WELCOME_CONN_CFG_017_ERROR_STATUS_TEXTS = ("请检查密码", "密码不正确", "已保存")


def _welcome_wifi_entry(wifi_yaml: dict, entry_id: str) -> tuple[str, str]:
    entry = get_wifi_list_entry(wifi_yaml, entry_id=entry_id)
    ssid = str(entry.get("ssid") or "").strip()
    if not ssid:
        pytest.skip(f"wifi_ssid.yaml 缺少 {entry_id!r} 的 SSID")
    return ssid, str(entry.get("pwd") or "")


def _open_config_and_verify_password(
    welcome_wlan_ui: WelcomeWlanUI, ssid: str, password: str, capsys, success_message: str
) -> None:
    log.info("打开 Welcome 网络 %s 的连接配置框", ssid)
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        message = f"{success_message}异常"
        log.info("%s", message)
        with capsys.disabled():
            print(f"\n{message}")
        welcome_wlan_ui.fail_with_artifacts(message)
    welcome_wlan_ui.cancel_network_config()
    log.info("%s", success_message)
    with capsys.disabled():
        print(f"\n{success_message}")


def _fail_with_result(
    welcome_wlan_ui: WelcomeWlanUI, capsys, message: str
) -> None:
    log.info("%s", message)
    with capsys.disabled():
        print(f"\n{message}")
    welcome_wlan_ui.fail_with_artifacts(message)


def run_welcome_hyperwifi_intro_case(settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    label = welcome_wlan_ui.find_hyperwifi_label()
    if label is None:
        message = '\nwelcomeUI，点击HyperWiFi-logo跳转失败'
        log.info("%s", message.strip())
        with capsys.disabled():
            print(message)
        welcome_wlan_ui.fail_with_artifacts(message)

    if not welcome_wlan_ui.click_hyperwifi_label_and_wait_for_intro(label):
        message = '\nwelcomeUI，点击HyperWiFi-logo跳转失败'
        log.info("%s", message.strip())
        with capsys.disabled():
            print(message)
        welcome_wlan_ui.fail_with_artifacts(message)

    welcome_wlan_ui.close_hyperwifi_intro()
    log.info("welcomeUI，点击HyperWiFi-logo跳转成功")
    with capsys.disabled():
        print('\nwelcomeUI，点击HyperWiFi-logo跳转成功')


def run_welcome_open_network_case(
    wifi, wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_OPEN_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.connect_open_network(ssid)

    if not _wait_for_wifi_connection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_result(
            welcome_wlan_ui,
            capsys,
            f"点击开放 WiFi 后未连接到 {ssid!r}，当前={connected_ssids!r}",
        )

    welcome_wlan_ui.open_connected_network_details(ssid)
    welcome_wlan_ui.delete_network_from_details()
    if not _wait_for_wifi_disconnection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_result(
            welcome_wlan_ui,
            capsys,
            f"点击删除此网络后仍连接 {ssid!r}，当前={connected_ssids!r}",
        )
    log.info("点击开放 WiFi %r 后未弹出配置框，连接后删除成功", ssid)
    with capsys.disabled():
        print(f"\nwelcomeUI，点击开放 WiFi {ssid!r} 后未弹出配置框，连接后删除成功")


def run_welcome_encrypted_config_case(
    wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    try:
        ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
        welcome_wlan_ui.open_encrypted_network_config(ssid)
    except AssertionError:
        log.info("加密网络连接配置框弹出异常")
        with capsys.disabled():
            print("\n加密网络连接配置框弹出异常")
        raise
    welcome_wlan_ui.cancel_network_config()
    log.info("加密网络连接配置框正常")
    with capsys.disabled():
        print("\n加密网络连接配置框正常")


def run_welcome_empty_password_case(wifi_yaml, settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    welcome_wlan_ui.clear_password()
    if welcome_wlan_ui.is_connect_enabled():
        _fail_with_result(welcome_wlan_ui, capsys, "空密码时连接按钮未置灰")
    welcome_wlan_ui.cancel_network_config()
    log.info("空密码时连接按钮置灰正常")
    with capsys.disabled():
        print("\n空密码时连接按钮置灰正常")


def run_welcome_password_length_case(
    wifi, wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, password = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    log.info("校验 %r 的 7 位与 8 位密码连接状态", ssid)
    if not welcome_wlan_ui.enter_password("1234567"):
        _fail_with_result(welcome_wlan_ui, capsys, "7位密码输入异常")
    if welcome_wlan_ui.is_connect_enabled():
        _fail_with_result(welcome_wlan_ui, capsys, "7位密码时连接按钮未置灰")
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_result(welcome_wlan_ui, capsys, "8位密码输入异常")
    if not welcome_wlan_ui.is_connect_enabled():
        _fail_with_result(welcome_wlan_ui, capsys, "8位密码时连接按钮未启用")
    welcome_wlan_ui.connect_network()
    if not _wait_for_wifi_connection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_result(
            welcome_wlan_ui, capsys,
            f"8位密码后未连接到 {ssid}，当前={connected_ssids!r}",
        )
    welcome_wlan_ui.open_connected_network_details(ssid)
    welcome_wlan_ui.delete_network_from_details()
    if not _wait_for_wifi_disconnection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_result(
            welcome_wlan_ui, capsys,
            f"点击删除此网络后仍连接 {ssid!r}，当前={connected_ssids!r}",
        )
    log.info("最小8位密码校验正常，删除 %r 后网络已断开", ssid)
    with capsys.disabled():
        print(f"\n最小8位密码校验正常，删除 {ssid!r} 后网络已断开")


def run_welcome_password_visibility_case(
    wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, password = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_result(welcome_wlan_ui, capsys, "密码输入异常")
    if not welcome_wlan_ui.is_password_masked():
        _fail_with_result(welcome_wlan_ui, capsys, "密码输入框默认未密文显示")
    welcome_wlan_ui.toggle_password_visibility()
    if welcome_wlan_ui.is_password_masked():
        _fail_with_result(welcome_wlan_ui, capsys, "点击眼睛按钮后密码未明文显示")
    welcome_wlan_ui.toggle_password_visibility()
    if not welcome_wlan_ui.is_password_masked():
        _fail_with_result(welcome_wlan_ui, capsys, "再次点击眼睛按钮后密码未密文显示")
    welcome_wlan_ui.cancel_network_config()
    log.info("密码输入框明文/密文切换正常")
    with capsys.disabled():
        print("\n密码输入框明文/密文切换正常")


def run_welcome_clear_password_case(wifi_yaml, settings_ui, tmp_path, capsys) -> None:
    ssid, password = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_result(welcome_wlan_ui, capsys, "密码输入异常")
    welcome_wlan_ui.clear_password_with_button()
    welcome_wlan_ui.cancel_network_config()
    log.info("密码输入框删除按钮有效")
    with capsys.disabled():
        print("\n密码输入框删除按钮有效")


def run_welcome_cancel_config_case(wifi_yaml, settings_ui, tmp_path, capsys) -> None:
    ssid, password = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_result(welcome_wlan_ui, capsys, "密码输入异常")
    welcome_wlan_ui.cancel_network_config()
    log.info("密码输入框取消按钮有效")
    with capsys.disabled():
        print("\n密码输入框取消按钮有效")


def run_welcome_connect_button_case(
    wifi, wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, password = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_result(welcome_wlan_ui, capsys, "正确密码输入异常")
    welcome_wlan_ui.connect_network()

    if not _wait_for_wifi_connection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_result(
            welcome_wlan_ui,
            capsys,
            f"正确密码后未连接到 {ssid}，当前={connected_ssids!r}",
        )
    log.info("密码输入框连接按钮连接 %r 成功", ssid)
    with capsys.disabled():
        print("\n密码输入框连接按钮连接成功")


def run_welcome_ip_mode_switch_case(wifi_yaml, settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    welcome_wlan_ui.open_advanced_options()
    if welcome_wlan_ui.current_ip_mode() != "DHCP":
        _fail_with_result(welcome_wlan_ui, capsys, "高级选项 IP 设置默认不是 DHCP")
    welcome_wlan_ui.select_ip_mode("静态")
    welcome_wlan_ui.select_ip_mode("DHCP")
    welcome_wlan_ui.cancel_network_config()
    log.info("高级选项 IP 设置切换正常")
    with capsys.disabled():
        print("\n高级选项 IP 设置切换正常")


def run_welcome_wrong_password_reopen_case(
    wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(WELCOME_CONN_CFG_017_WRONG_PASSWORD):
        _fail_with_result(welcome_wlan_ui, capsys, "错误密码输入异常")
    welcome_wlan_ui.connect_network()

    if not welcome_wlan_ui.wait_for_network_status(
        ssid, WELCOME_CONN_CFG_017_ERROR_STATUS_TEXTS
    ):
        _fail_with_result(welcome_wlan_ui, capsys, "错误密码后目标 WiFi 未显示已保存或密码错误提示")
    if not welcome_wlan_ui.wait_for_ssid(ssid):
        _fail_with_result(welcome_wlan_ui, capsys, "错误密码后等待目标 WiFi 刷新出现超时")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    log.info("密码错误提示的 WiFi %r 再次点击后配置框弹出正常", ssid)
    with capsys.disabled():
        print("\n密码错误提示的 WiFi 再次点击后配置框弹出正常")


def run_welcome_password_input_case(
    wifi_yaml, settings_ui, tmp_path, capsys,
    ssid_password: str, success_message: str,
) -> None:
    ssid, _ = _welcome_wifi_entry(wifi_yaml, WELCOME_ENCRYPTED_ENTRY_ID)
    _open_config_and_verify_password(
        WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui"),
        ssid, ssid_password, capsys, success_message,
    )
