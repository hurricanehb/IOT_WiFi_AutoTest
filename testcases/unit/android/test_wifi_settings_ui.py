from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest
from uiautomator2.exceptions import UiObjectNotFoundError

from core.libs.android.wifi_scenarios.settings.wifi_security import (
    run_wifi_security_filter_case,
    run_wifi_security_option_absent_case,
)
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    run_add_network_field_case,
)
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI
from core.libs.android.settings_pages.ip_settings_page import WiFiIPSettingsUI
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from testcases import conftest as case_fixtures
from core.libs.android.wifi_scenarios.advanced_settings.energy_save import (
    _toggle_wlan_from_settings,
)


@pytest.mark.parametrize(
    "resource_id",
    ["com.android.settings:id/switchWidget", "android:id/switch_widget"],
)
def test_energy_save_wlan_toggle_uses_fixture_settings_api(resource_id) -> None:
    settings = AndroidSettingsUI.__new__(AndroidSettingsUI)
    settings.device = Mock()
    settings.open_wifi_settings = Mock()
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("missing switch"))
    switch = settings.device.return_value
    switch.info = {"checked": True}
    missing_switch = Mock()
    missing_switch.wait.return_value = False
    settings.device.side_effect = lambda **criteria: (
        switch
        if criteria.get("resourceId") == resource_id
        or re.fullmatch(criteria.get("resourceIdMatches", r"(?!)"), resource_id)
        else missing_switch
    )
    states = []

    def toggle_switch() -> None:
        switch.info["checked"] = not switch.info["checked"]
        states.append(switch.info["checked"])

    switch.click.side_effect = toggle_switch

    _toggle_wlan_from_settings(settings)

    assert states == [False, True]
    assert settings.open_wifi_settings.call_count == 2
    assert switch.click.call_count == 2


@pytest.mark.parametrize(
    ("module", "should_prepare"),
    [
        ("wlan_components_welcome", False),
        ("wlan_hotspot", False),
        ("wlan_advanced_settings", False),
        ("wlan_access", True),
    ],
)
def test_settings_ui_keeps_existing_wlan_case_initialization(
    monkeypatch, tmp_path, module, should_prepare
) -> None:
    settings = Mock()
    factory = Mock(return_value=settings)
    monkeypatch.setattr(case_fixtures, "AndroidSettingsUI", factory)
    request = SimpleNamespace(
        node=SimpleNamespace(path=tmp_path / "testcases" / "android" / module / "test_case.py"),
        getfixturevalue=Mock(),
    )

    actual = case_fixtures.settings_ui.__wrapped__("serial", tmp_path, request)

    assert actual is settings
    factory.assert_called_once_with("serial", tmp_path / "settings-ui")
    assert request.getfixturevalue.call_count == int(should_prepare)
    if should_prepare:
        settings.prepare.assert_called_once_with()
    else:
        settings.prepare.assert_not_called()


def test_prepare_reconnects_after_initial_jsonrpc_failure(monkeypatch) -> None:
    stale_device = Mock()
    stale_device.settings = {}
    stale_device.screen_on.side_effect = ConnectionError("connection refused")
    recovered_device = Mock()
    recovered_device.settings = {}
    connect = Mock(side_effect=[stale_device, recovered_device])
    monkeypatch.setattr(
        "core.libs.android.settings_pages.settings_page.u2.connect", connect
    )
    monkeypatch.setattr(
        "core.libs.android.settings_pages.settings_page.time.sleep", Mock()
    )
    settings = AndroidSettingsUI("serial", Path("artifacts"))

    settings.prepare()

    assert connect.call_args_list == [call("serial"), call("serial")]
    recovered_device.reset_uiautomator.assert_called_once_with()
    recovered_device.screen_on.assert_called_once_with()
    recovered_device.press.assert_called_once_with("home")


def test_save_enabled_recovers_when_scrollable_disappears() -> None:
    settings = Mock()
    device = settings.device
    scrollable = Mock()
    scrollable.exists = True
    scrollable.scroll.toEnd.side_effect = UiObjectNotFoundError(
        {"code": -32001, "message": "redrawn"}, method="scrollToEnd"
    )
    button_missing = Mock()
    button_missing.exists = False
    button_visible = Mock()
    button_visible.exists = True
    button_visible.info = {"enabled": True}
    device.return_value = scrollable
    page = WiFiAddNetworkUI(settings)
    page._save_button = Mock(side_effect=[button_missing, button_visible])

    enabled = page.save_enabled()

    assert enabled is True
    scrollable.scroll.toEnd.assert_called_once_with()
    settings.reset_uiautomator.assert_not_called()


def test_current_ip_mode_reads_spinner_child_text() -> None:
    settings = Mock()
    spinner = Mock()
    spinner.exists = True
    spinner.get_text.return_value = "IP 设置\nDHCP"
    settings.device.return_value = spinner
    page = WiFiIPSettingsUI(settings)

    assert page.current_ip_mode() == "DHCP"

    settings.device.assert_called_once_with(resourceId="com.android.settings:id/ip_settings")


def test_open_network_editor_uses_native_tap_when_landscape_click_is_ignored() -> None:
    settings = Mock()
    edit = Mock()
    edit.exists = True
    edit.info = {
        "bounds": {"left": 1828, "right": 1882, "top": 63, "bottom": 117}
    }
    title = Mock()
    title.wait.side_effect = [False, True]
    title.exists = True
    spinner = Mock()
    spinner.exists = True
    spinner.wait.return_value = True
    settings.device.window_size.return_value = (1920, 1080)

    def select(**kwargs):
        if kwargs.get("description") == "修改":
            return edit
        if kwargs.get("resourceId") == "com.android.settings:id/password":
            return Mock(exists=False)
        if kwargs.get("resourceId") == "com.android.settings:id/alertTitle":
            return title
        if kwargs.get("resourceId") == "com.android.settings:id/ip_settings":
            return spinner
        return Mock()

    settings.device.side_effect = select

    WiFiIPSettingsUI(settings).open_network_editor("Lab_HW_AutoTest")

    settings.device.shell.assert_called_once_with("input tap 1855 90")
    settings.click_description.assert_not_called()
    title.wait.assert_called_once_with(timeout=3.0)
    title.click.assert_not_called()


def test_open_network_editor_does_not_native_tap_in_portrait() -> None:
    settings = Mock()
    edit = Mock()
    edit.exists = True
    title = Mock()
    title.wait.return_value = False
    title.exists = False
    spinner = Mock()
    spinner.exists = True
    spinner.wait.return_value = True
    settings.device.window_size.return_value = (720, 1600)

    def select(**kwargs):
        if kwargs.get("description") == "修改":
            return edit
        if kwargs.get("resourceId") == "com.android.settings:id/password":
            return Mock(exists=False)
        if kwargs.get("resourceId") == "com.android.settings:id/alertTitle":
            return title
        if kwargs.get("resourceId") == "com.android.settings:id/ip_settings":
            return spinner
        return Mock()

    settings.device.side_effect = select

    settings.fail_with_artifacts.side_effect = AssertionError(
        "未打开 WiFi 修改对话框"
    )

    with pytest.raises(AssertionError, match="未打开 WiFi 修改对话框"):
        WiFiIPSettingsUI(settings).open_network_editor("Lab_HW_AutoTest")

    settings.device.shell.assert_not_called()
    settings.click_description.assert_called_once_with("修改")


def test_open_network_editor_native_taps_advanced_toggle_in_landscape() -> None:
    settings = Mock()
    edit = Mock()
    edit.exists = True
    edit.info = {
        "bounds": {"left": 1828, "right": 1882, "top": 63, "bottom": 117}
    }
    title = Mock()
    title.wait.return_value = True
    spinner = Mock()
    spinner.exists = False
    spinner.wait.return_value = True
    toggle = Mock()
    toggle.wait.return_value = True
    toggle.info = {
        "bounds": {"left": 800, "right": 1840, "top": 600, "bottom": 680}
    }
    settings.device.window_size.return_value = (1920, 1080)

    def select(**kwargs):
        if kwargs.get("description") == "修改":
            return edit
        if kwargs.get("resourceId") == "com.android.settings:id/password":
            return Mock(exists=False)
        if kwargs.get("resourceId") == "com.android.settings:id/alertTitle":
            return title
        if kwargs.get("resourceId") == "com.android.settings:id/ip_settings":
            return spinner
        if kwargs.get("resourceId") == "com.android.settings:id/wifi_advanced_togglebox":
            return toggle
        return Mock()

    settings.device.side_effect = select

    WiFiIPSettingsUI(settings).open_network_editor("Lab_HW_AutoTest")

    assert settings.device.shell.call_args_list == [
        call("input tap 1855 90"),
        call("input tap 1320 640"),
    ]
    toggle.click.assert_not_called()


def test_save_enabled_does_not_press_enter_without_focused_input() -> None:
    settings = Mock()
    focused_input = Mock()
    focused_input.exists = True
    save_button = Mock()
    save_button.exists = True
    save_button.info = {"enabled": True}

    def select(**kwargs):
        if kwargs == {"className": "android.widget.EditText", "focused": True}:
            return focused_input
        if kwargs.get("resourceId") == "android:id/button1":
            return save_button
        return Mock(exists=False)

    settings.device.side_effect = select

    assert WiFiIPSettingsUI(settings).save_enabled() is True
    settings.device.press.assert_not_called()


def test_select_privacy_mode_uses_native_taps_in_landscape() -> None:
    settings = Mock()
    current = Mock()
    current.exists = True
    selector = Mock()
    selector.exists = True
    selector.get_text.return_value = "使用设备 MAC"
    selector.info = {
        "bounds": {"left": 1008, "right": 1632, "top": 400, "bottom": 480}
    }
    option = Mock()
    option.wait.return_value = True
    option.info = {
        "bounds": {"left": 1008, "right": 1632, "top": 500, "bottom": 580}
    }
    settings.device.window_size.return_value = (1920, 1080)

    def select(**kwargs):
        if kwargs.get("text") == "使用设备 MAC":
            return current
        if kwargs.get("text") == "使用随机 MAC":
            return option
        if kwargs.get("resourceId") == "com.android.settings:id/privacy_settings":
            return selector
        return Mock(exists=False)

    settings.device.side_effect = select

    WiFiIPSettingsUI(settings).select_privacy_mode("randomized")

    assert settings.device.shell.call_args_list == [
        call("input tap 1320 440"),
        call("input tap 1320 540"),
    ]
    selector.click.assert_not_called()
    option.click.assert_not_called()


def test_current_privacy_mode_reads_rom_randomized_label_from_spinner() -> None:
    settings = Mock()
    selector = Mock()
    selector.exists = True
    selector.get_text.return_value = "隐私\n使用随机分配的 MAC"
    settings.device.side_effect = lambda **kwargs: (
        selector
        if kwargs.get("resourceId") == "com.android.settings:id/privacy_settings"
        else Mock(exists=False)
    )

    assert WiFiIPSettingsUI(settings).current_privacy_mode() == "randomized"
    settings.device.assert_called_once_with(
        resourceId="com.android.settings:id/privacy_settings"
    )


def test_overlong_ssid_accepts_enabled_save_with_rejection_message() -> None:
    add_network_ui = Mock()
    wifi = Mock()
    wifi.list_networks_blob.return_value = "Network Id\tSSID\tSecurity type"
    add_network_ui.set_ssid.return_value = "a" * 33
    add_network_ui.set_password.return_value = "24681357"
    add_network_ui.save_enabled.return_value = True
    add_network_ui.save_rejection_message.return_value = "无法保存网络"

    run_add_network_field_case(
        add_network_ui,
        ssid="a" * 33,
        expect_save_enabled=False,
        expect_save_rejected=True,
        wifi=wifi,
    )

    add_network_ui.save_rejection_message.assert_called_once_with()
    add_network_ui.cancel.assert_called_once_with()


def test_save_rejection_message_reads_network_save_toast() -> None:
    settings = Mock()
    settings.device.toast.get_message.return_value = "无法保存网络"
    page = WiFiAddNetworkUI(settings)
    save_button = Mock()
    page.save_enabled = Mock(return_value=True)
    page._save_button = Mock(return_value=save_button)

    assert page.save_rejection_message(timeout=1.0) == "无法保存网络"

    save_button.click.assert_called_once_with()
    settings.device.toast.reset.assert_called_once_with()
    settings.device.toast.get_message.assert_called_once_with(
        wait_timeout=1.0,
        cache_timeout=10.0,
        default="",
    )


def test_open_wifi_settings_uses_hard_recovery_after_repeated_misses(
    monkeypatch,
) -> None:
    device = Mock()
    device.settings = {}
    title = Mock()
    title.wait.side_effect = [False, False, True]
    device.return_value = title
    monkeypatch.setattr(
        "core.libs.android.settings_pages.settings_page.u2.connect",
        Mock(return_value=device),
    )
    monkeypatch.setattr(
        "core.libs.android.settings_pages.settings_page.time.sleep", Mock()
    )
    settings = AndroidSettingsUI("serial", Path("artifacts"))

    settings.open_wifi_settings()

    device.assert_any_call(
        packageName="com.android.settings",
        textMatches=r"(?i)^(WLAN|Wi-?Fi)$",
    )
    assert device.reset_uiautomator.call_count == 2
    device.screen_on.assert_called_once_with()
    device.press.assert_called_once_with("home")
    assert device.shell.call_args_list == [
        call("wm dismiss-keyguard"),
        call("am start -W -a android.settings.WIFI_SETTINGS -f 0x10008000"),
        call("am start -W -a android.settings.WIFI_SETTINGS -f 0x10008000"),
        call("am force-stop com.android.settings"),
        call("am start -W -a android.settings.WIFI_SETTINGS -f 0x10008000"),
    ]


def test_add_network_security_options_reads_visible_dropdown_items() -> None:
    settings = Mock()
    device = settings.device
    spinner = Mock()
    spinner.exists = True
    device.return_value = spinner
    device.dump_hierarchy.return_value = (
        '<hierarchy><node text="无"/><node text="WPA/WPA2-Personal"/>'
        '<node text="WPA3-Personal"/></hierarchy>'
    )

    options = WiFiAddNetworkUI(settings).security_options()

    assert options == ("无", "WPA/WPA2-Personal", "WPA3-Personal")
    spinner.click.assert_called_once_with()
    device.press.assert_called_once_with("back")


def test_wifi_security_filter_hides_weak_network_then_shows_wpa2(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "core.libs.android.wifi_scenarios.settings.wifi_security.time.sleep", Mock()
    )
    scans = iter([[], ["PyAutoTest_WifiSec_WEP"]])
    monkeypatch.setattr(
        "core.libs.android.wifi_scenarios.settings.wifi_security.visible_ssids",
        lambda *args, **kwargs: next(scans),
    )
    wifi = Mock()
    wifi.set_wifi_enabled.return_value = True
    wifi_ap_action = Mock()

    run_wifi_security_filter_case(
        "case",
        Mock(),
        wifi,
        wifi_ap_action,
        insecure_security="wep40",
        settle_sec=0,
    )

    assert wifi_ap_action.configure_wifi.call_args_list == [
        call(
            ssid="PyAutoTest_WifiSec_WEP",
            password="12345",
            security="wep40",
            band="5g",
            verify=True,
        ),
        call(
            ssid="PyAutoTest_WifiSec_WEP",
            password="24681357",
            security="wpa2-aes",
            band="5g",
            verify=True,
        ),
    ]


def test_wifi_security_option_absent_fails_when_forbidden_option_exists(
) -> None:
    add_network_ui = Mock()
    add_network_ui.security_options.return_value = ("None", "WPA2-Personal")

    with pytest.raises(pytest.fail.Exception, match="不应包含弱安全选项"):
        run_wifi_security_option_absent_case(
            "case", add_network_ui, forbidden_options=("Open", "None", "无")
        )

    add_network_ui.open.assert_called_once_with()
    add_network_ui.cancel.assert_called_once_with()


def test_wifi_security_option_absent_fails_when_options_are_empty() -> None:
    add_network_ui = Mock()
    add_network_ui.security_options.return_value = ()

    with pytest.raises(pytest.fail.Exception, match="未读取到任何"):
        run_wifi_security_option_absent_case(
            "case", add_network_ui, forbidden_options=("WEP",)
        )

    add_network_ui.cancel.assert_called_once_with()