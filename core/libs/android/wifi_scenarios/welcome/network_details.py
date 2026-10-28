"""Android Welcome WLAN network details scenarios."""
from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.welcome._helpers import (
    _wait_for_wifi_connection,
    _wait_for_wifi_disconnection,
)
from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI
from core.testdata_loader import get_wifi_list_entry, load_wifi_ssid
from core.utils.log_handler import get_logger


_WELCOME_CONNECTION_ENTRY_ID = "welcome_connection_wpa2"


DEFAULT_REQUIRED_STATIC_IP_ADDRESS = "10.210.105.100"


def _welcome_connection_entry(wifi_yaml: dict | None = None) -> tuple[str, str]:
    data = wifi_yaml if wifi_yaml is not None else load_wifi_ssid()
    entry = get_wifi_list_entry(data, entry_id=_WELCOME_CONNECTION_ENTRY_ID)
    ssid = str(entry.get("ssid") or "").strip()
    if not ssid:
        pytest.skip(
            f"wifi_ssid.yaml 缺少 {_WELCOME_CONNECTION_ENTRY_ID!r} 测试数据"
        )
    return ssid, str(entry.get("pwd") or "")


def _open_static_ip_config(settings_ui, tmp_path) -> WelcomeWlanUI:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    ssid, _ = _welcome_connection_entry()
    get_logger(__name__).info("打开 Welcome 网络 %r 的静态 IP 配置", ssid)
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    welcome_wlan_ui.open_advanced_options()
    welcome_wlan_ui.select_ip_mode("静态")
    return welcome_wlan_ui


def _open_static_ip_config_with_defaults(settings_ui, tmp_path) -> WelcomeWlanUI:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    if not welcome_wlan_ui.is_network_config_open():
        ssid, password = _welcome_connection_entry()
        welcome_wlan_ui.open_encrypted_network_config(ssid)
        if not welcome_wlan_ui.enter_password(password):
            welcome_wlan_ui.fail_with_artifacts(
                f"指定 WiFi {ssid!r} 的密码未正确填写"
            )
        welcome_wlan_ui.dismiss_keyboard()
    welcome_wlan_ui.open_advanced_options()
    if welcome_wlan_ui.current_ip_mode() != "静态":
        welcome_wlan_ui.select_ip_mode("静态")
    actual = welcome_wlan_ui.set_static_field(
        "ip_address", DEFAULT_REQUIRED_STATIC_IP_ADDRESS
    )
    if actual != DEFAULT_REQUIRED_STATIC_IP_ADDRESS:
        welcome_wlan_ui.fail_with_artifacts(
            "静态 IP 地址未正确输入 "
            f"{DEFAULT_REQUIRED_STATIC_IP_ADDRESS!r}，实际={actual!r}"
        )
    return welcome_wlan_ui


def _fail_with_artifacts(welcome_wlan_ui: WelcomeWlanUI, capsys, message: str) -> None:
    get_logger(__name__).info("%s", message)
    with capsys.disabled():
        print(f"\n{message}")
    welcome_wlan_ui.fail_with_artifacts(message)


def run_welcome_static_field_input_case(
    settings_ui, tmp_path, capsys, field: str, value: str, initial_value: str | None = None
) -> None:
    welcome_wlan_ui = _open_static_ip_config(settings_ui, tmp_path)
    if initial_value is not None:
        initial_actual = welcome_wlan_ui.set_static_field(field, initial_value)
        if initial_actual != initial_value:
            _fail_with_artifacts(
                welcome_wlan_ui,
                capsys,
                f"静态 IP 字段 {field!r} 未正确输入 {initial_value!r}，实际={initial_actual!r}",
            )
    actual = welcome_wlan_ui.set_static_field(field, value)
    if actual != value:
        _fail_with_artifacts(
            welcome_wlan_ui, capsys, f"静态 IP 字段 {field!r} 未正确输入 {value!r}，实际={actual!r}"
        )
    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，静态 IP 字段 %r 正确输入 %r", field, value)
    with capsys.disabled():
        print(f"\nwelcomeUI，静态 IP 字段 {field!r} 正确输入 {value!r}")


def run_welcome_static_field_rejection_case(
    settings_ui, tmp_path, capsys, field: str, value: str
) -> None:
    welcome_wlan_ui = _open_static_ip_config_with_defaults(settings_ui, tmp_path)
    if not welcome_wlan_ui.is_connect_enabled():
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            "填写默认 IP 地址后，连接按钮仍不可点击",
        )
    welcome_wlan_ui.set_static_field(field, value, verify_readback=False)
    if welcome_wlan_ui.is_connect_enabled():
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            f"静态 IP 字段 {field!r} 输入非法值 {value!r} 后，连接按钮未置灰",
        )
    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，静态 IP 字段 %r 输入非法值 %r 后连接按钮已置灰", field, value)
    with capsys.disabled():
        print(f"\nwelcomeUI，静态 IP 字段 {field!r} 输入非法值 {value!r} 后连接按钮已置灰")


def run_welcome_ip_mode_default_case(settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config()
    welcome_wlan_ui.open_advanced_options()
    if welcome_wlan_ui.current_ip_mode() != "DHCP":
        _fail_with_artifacts(welcome_wlan_ui, capsys, "IP 设置默认不是 DHCP")
    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，IP 设置默认选中 DHCP 正常")
    with capsys.disabled():
        print("\nwelcomeUI，IP 设置默认选中 DHCP 正常")


def run_welcome_ip_mode_options_case(settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config()
    welcome_wlan_ui.open_advanced_options()
    if welcome_wlan_ui.ip_mode_options() != {"DHCP", "静态"}:
        _fail_with_artifacts(welcome_wlan_ui, capsys, "IP 设置选项不是 DHCP 和静态")
    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，IP 设置仅提供 DHCP 和静态选项正常")
    with capsys.disabled():
        print("\nwelcomeUI，IP 设置仅提供 DHCP 和静态选项正常")


def run_welcome_static_fields_case(settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = _open_static_ip_config(settings_ui, tmp_path)
    if welcome_wlan_ui.static_field_labels() != {
        "ip_address", "gateway", "prefix_length", "dns1", "dns2"
    }:
        _fail_with_artifacts(welcome_wlan_ui, capsys, "静态 IP 可配置项不完整")
    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，静态 IP 可配置项显示完整正常")
    with capsys.disabled():
        print("\nwelcomeUI，静态 IP 可配置项显示完整正常")


def run_welcome_delete_network_case(
    wifi, wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, password = _welcome_connection_entry(wifi_yaml)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    welcome_wlan_ui.open_encrypted_network_config(ssid)
    if not welcome_wlan_ui.enter_password(password):
        _fail_with_artifacts(welcome_wlan_ui, capsys, "指定 WiFi 的密码未正确填写")
    if not welcome_wlan_ui.is_connect_enabled():
        _fail_with_artifacts(welcome_wlan_ui, capsys, "指定 WiFi 的连接按钮未启用")
    welcome_wlan_ui.connect_network()
    if not _wait_for_wifi_connection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            f"未连接到 {ssid!r}，当前={connected_ssids!r}",
        )

    welcome_wlan_ui.open_connected_network_details(ssid)
    welcome_wlan_ui.delete_network_from_details()

    if not _wait_for_wifi_disconnection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            f"点击删除此网络后仍连接 {ssid!r}，当前={connected_ssids!r}",
        )
    get_logger(__name__).info("welcomeUI，删除 %r 后网络已断开", ssid)
    with capsys.disabled():
        print(f"\nwelcomeUI，删除 {ssid!r} 后网络已断开")


def run_welcome_cancel_static_config_case(
    wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, _ = _welcome_connection_entry(wifi_yaml)
    welcome_wlan_ui = _open_static_ip_config_with_defaults(settings_ui, tmp_path)
    if not welcome_wlan_ui.is_connect_enabled():
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            "填写指定 WiFi 的密码和 IP 地址后，连接按钮仍不可点击",
        )

    welcome_wlan_ui.cancel_network_config()
    get_logger(__name__).info("welcomeUI，取消 %r 的静态 IP 配置后已返回 WLAN 列表", ssid)
    with capsys.disabled():
        print(f"\nwelcomeUI，取消 {ssid!r} 的静态 IP 配置后已返回 WLAN 列表")


def run_welcome_save_static_config_case(
    wifi, wifi_yaml, settings_ui, tmp_path, capsys
) -> None:
    ssid, _ = _welcome_connection_entry(wifi_yaml)
    welcome_wlan_ui = _open_static_ip_config_with_defaults(settings_ui, tmp_path)
    if not welcome_wlan_ui.is_connect_enabled():
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            "填写指定 WiFi 的密码和 IP 地址后，连接按钮仍不可点击",
        )

    welcome_wlan_ui.connect_network()
    if not _wait_for_wifi_connection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            f"点击连接后未连接到 {ssid!r}，当前={connected_ssids!r}",
        )
    get_logger(__name__).info("welcomeUI，点击连接后已关联 %r", ssid)
    with capsys.disabled():
        print(f"\nwelcomeUI，点击连接后已关联 {ssid!r}")

    welcome_wlan_ui.open_connected_network_details(ssid)
    welcome_wlan_ui.delete_network_from_details()
    if not _wait_for_wifi_disconnection(wifi, ssid):
        connected_ssids = wifi.list_connected_ssids(trust_status_fallback=True)
        _fail_with_artifacts(
            welcome_wlan_ui,
            capsys,
            f"删除网络后仍连接 {ssid!r}，当前={connected_ssids!r}",
        )
    get_logger(__name__).info("welcomeUI，删除 %r 后网络已断开", ssid)
    with capsys.disabled():
        print(f"\nwelcomeUI，删除 {ssid!r} 后网络已断开")
