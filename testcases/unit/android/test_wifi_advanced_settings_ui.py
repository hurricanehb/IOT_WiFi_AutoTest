from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import Mock, call, patch

import pytest

from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI
from core.libs.android.wifi_ui.advanced_settings_support import AdvancedSettingsSupportUI
from core.libs.android.wifi_scenarios.advanced_settings.energy_save import (
    _toggle_airplane_mode_from_settings,
    _toggle_wlan_from_settings,
)


@pytest.mark.parametrize("scroll_to_end", [True, False])
def test_network_preferences_click_waits_for_row_to_stop_moving(
    monkeypatch, scroll_to_end
) -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    settings.device = Mock()
    page = WiFiAdvancedSettingsUI(settings)
    label = page.NETWORK_PREFERENCE_LABELS[0]
    page._find_entry = Mock(side_effect=[settings.device.return_value] if scroll_to_end
                            else [None, settings.device.return_value])
    snapshots = [
        f'<hierarchy><node clickable="true" bounds="[0,{top}][720,{top + 120}]">'
        f'<node text="{label}" bounds="[40,{top + 20}][400,{top + 60}]"/>'
        '</node></hierarchy>'
        for top in (1200, 1400, 1400)
    ]
    settings.device.dump_hierarchy.side_effect = snapshots
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_page.time.sleep", Mock()
    )

    page._click_entry(
        page.NETWORK_PREFERENCE_LABELS, scroll_to_end_before_search=scroll_to_end
    )

    settings.device.click.assert_called_once_with(360, 1460)
    assert settings.device.dump_hierarchy.call_count == 3
    settings.device.return_value.click_exists.assert_not_called()
    if scroll_to_end:
        settings.device.return_value.scroll.toEnd.assert_called_once_with()
    else:
        settings.device.return_value.scroll.to.assert_called_once_with(text=label)


def test_network_preferences_never_clicks_when_row_keeps_moving(monkeypatch) -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.fail_with_artifacts.side_effect = AssertionError("row did not settle")
    page = WiFiAdvancedSettingsUI(settings)
    page._entry_row_bounds_from_hierarchy = Mock(side_effect=[
        (0, 1200, 720, 1320), (0, 1400, 720, 1520), (0, 1300, 720, 1420)
    ])
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_page.time.monotonic",
        Mock(side_effect=[0.0, 0.1, 1.0, 2.0, 6.0]),
    )
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_page.time.sleep", Mock()
    )

    with pytest.raises(AssertionError, match="row did not settle"):
        page._click_entry(page.NETWORK_PREFERENCE_LABELS, scroll_to_end_before_search=True)

    settings.device.click.assert_not_called()
    settings.device.return_value.click_exists.assert_not_called()


@pytest.mark.parametrize("row_attributes", [
    'bounds="[0,1480][720,1600]"',
    'bounds="[0,1400][0,1520]"',
    'bounds="[0,1400][720,1520]" enabled="false"',
])
def test_network_preferences_rejects_clipped_empty_or_disabled_row(
    row_attributes: str,
) -> None:
    label = WiFiAdvancedSettingsUI.NETWORK_PREFERENCE_LABELS[0]
    hierarchy = (
        '<hierarchy><node scrollable="true" bounds="[0,200][720,1500]">'
        f'<node clickable="true" {row_attributes}><node text="{label}"/></node>'
        '</node></hierarchy>'
    )

    assert WiFiAdvancedSettingsUI._entry_row_bounds_from_hierarchy(
        hierarchy, (label,)
    ) is None


def test_network_preferences_does_not_fall_back_to_unverified_title_click() -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.device.dump_hierarchy.return_value = '<hierarchy/>'
    settings.device.return_value.scroll.to.return_value = False
    settings.fail_with_artifacts.side_effect = AssertionError("entry unavailable")
    page = WiFiAdvancedSettingsUI(settings)

    with pytest.raises(AssertionError, match="entry unavailable"):
        page._click_entry(page.NETWORK_PREFERENCE_LABELS, scroll_to_end_before_search=True)

    settings.device.click.assert_not_called()
    settings.device.return_value.click_exists.assert_not_called()


@pytest.mark.parametrize("successful_attempt", [1, 2, None])
def test_open_waits_for_network_preferences_and_retries_missed_click(
    monkeypatch, successful_attempt
) -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.fail_with_artifacts.side_effect = AssertionError("preferences did not open")
    page = WiFiAdvancedSettingsUI(settings)
    page._single_choice_dialog_is_open = Mock(return_value=False)
    page._advanced_setting_row = Mock(return_value=None)
    page._advanced_setting_row_required = Mock()
    attempts = 0
    polls = 0
    preferences_open = False

    def click_entry(labels, **_kwargs) -> None:
        nonlocal attempts, polls
        if labels == page.NETWORK_PREFERENCE_LABELS:
            attempts += 1
            polls = 0
        elif not preferences_open:
            raise AssertionError("advanced entry searched before navigation completed")

    def find_entry(labels):
        nonlocal polls, preferences_open
        if labels == page.ADVANCED_SETTINGS_LABELS and attempts:
            polls += 1
            preferences_open = attempts == successful_attempt and polls >= 2
            if preferences_open:
                return settings.device.return_value
        return None

    page._click_entry = Mock(side_effect=click_entry)
    page._find_entry = Mock(side_effect=find_entry)
    clock = iter(range(100))
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_page.time.monotonic",
        lambda: next(clock),
    )
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_page.time.sleep", Mock()
    )

    if successful_attempt is None:
        with pytest.raises(AssertionError, match="preferences did not open"):
            page.open()
        assert attempts == 3
        page._advanced_setting_row_required.assert_not_called()
    else:
        page.open()
        assert attempts == successful_attempt
        page._advanced_setting_row_required.assert_called_once_with()
        settings.fail_with_artifacts.assert_not_called()
    settings.open_wifi_settings.assert_called_once_with()


def test_advanced_settings_fixture_uses_its_own_support(monkeypatch, tmp_path) -> None:
    from testcases.android.wlan_advanced_settings import conftest as advanced_fixtures
    from testcases import conftest as shared_fixtures

    factory = Mock(spec=AdvancedSettingsSupportUI)
    monkeypatch.setattr(advanced_fixtures, "AdvancedSettingsSupportUI", factory)

    actual = advanced_fixtures.settings_ui.__wrapped__("serial", tmp_path)

    assert actual is factory.return_value
    factory.assert_called_once_with("serial", tmp_path / "advanced-settings-ui")
    assert AdvancedSettingsSupportUI.__name__ != "AndroidSettingsUI"
    assert not issubclass(AdvancedSettingsSupportUI, shared_fixtures.AndroidSettingsUI)
    assert not hasattr(shared_fixtures.AndroidSettingsUI, "set_airplane_mode_from_settings")


@pytest.mark.parametrize(
    ("toggle", "open_method", "initial_state"),
    [
        (_toggle_airplane_mode_from_settings, "open_airplane_mode_settings", False),
        (_toggle_wlan_from_settings, "open_wifi_settings", True),
    ],
)
@pytest.mark.parametrize(
    "resource_id",
    ["com.android.settings:id/switchWidget", "android:id/switch_widget"],
)
def test_energy_save_radio_toggle_uses_advanced_settings_api(
    resource_id, toggle, open_method, initial_state
) -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    open_page = Mock()
    setattr(settings, open_method, open_page)
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("missing switch"))
    switch = settings.device.return_value
    missing_switch = Mock()
    missing_switch.wait.return_value = False
    settings.device.side_effect = lambda **criteria: (
        switch
        if criteria.get("resourceId") == resource_id
        or re.fullmatch(criteria.get("resourceIdMatches", r"(?!)"), resource_id)
        else missing_switch
    )
    switch.info = {
        "checked": initial_state,
        "bounds": {"left": 100, "right": 200, "top": 300, "bottom": 400},
    }
    states = []

    def toggle_switch(*coordinates) -> None:
        switch.info["checked"] = not switch.info["checked"]
        states.append(switch.info["checked"])

    settings.device.click.side_effect = toggle_switch

    toggle(settings)

    assert states == [not initial_state, initial_state]
    assert open_page.call_count == 2
    assert settings.device.click.call_args_list == [call(150, 350), call(150, 350)]


@pytest.mark.parametrize("enabled", [False, True])
def test_advanced_settings_owns_quick_settings_toggle_and_close(enabled) -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    toggle = Mock(info={
        "checked": not enabled,
        "bounds": {"left": 585, "top": 643, "right": 659, "bottom": 724},
    })
    settings.device = Mock(return_value=toggle)
    settings.device.shell.side_effect = lambda _command: toggle.info.update(checked=enabled)
    settings._close_quick_settings_internet_panel = Mock()

    with patch(
        "core.libs.android.systemui_pages.quick_settings_page.open_internet_dialog"
    ) as open_internet_dialog:
        settings.set_quick_settings_wifi_enabled(enabled)

    open_internet_dialog.assert_called_once_with(settings, capture=False)
    settings.device.shell.assert_called_once_with("input tap 622 683")
    settings._close_quick_settings_internet_panel.assert_called_once_with()


def test_quick_settings_relocates_done_after_wifi_dialog_resizes(monkeypatch) -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("dialog still open"))
    toggle = Mock(info={"checked": False})
    done = Mock()
    done.info = {"bounds": {"left": 61, "top": 1200, "right": 659, "bottom": 1281}}
    dialog = Mock()
    closed = False

    def tap(command) -> None:
        nonlocal closed
        if command == "input tap 360 960":
            closed = True
        if command.startswith("input tap"):
            done.info = {"bounds": {"left": 61, "top": 920, "right": 659, "bottom": 1001}}

    def select(**criteria):
        return {
            "com.android.systemui:id/wifi_toggle": toggle,
            "com.android.systemui:id/done_button": done,
            "com.android.systemui:id/internet_dialog_title": dialog,
        }[criteria["resourceId"]]

    settings.device.side_effect = select
    settings.device.shell.side_effect = tap
    settings.device.window_size.return_value = (720, 1600)
    settings.device.dump_hierarchy.return_value = "<hierarchy/>"
    dialog.wait_gone.side_effect = lambda **_kwargs: closed
    monkeypatch.setattr(
        "core.libs.android.systemui_pages.quick_settings_page.open_internet_dialog", Mock()
    )

    settings.set_quick_settings_wifi_enabled(False)

    assert [
        arguments.args[0]
        for arguments in settings.device.shell.call_args_list
        if arguments.args[0].startswith("input tap")
    ] == ["input tap 360 1240", "input tap 360 960"]
    settings.fail_with_artifacts.assert_not_called()


def test_quick_settings_done_retry_is_bounded_and_does_not_hide_failure() -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.device.return_value.info = {
        "bounds": {"left": 61, "top": 920, "right": 659, "bottom": 1001}
    }
    settings.device.return_value.wait_gone.return_value = False
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("dialog still open"))
    settings._dismiss_quick_settings = Mock()

    with pytest.raises(AssertionError, match="dialog still open"):
        settings._close_quick_settings_internet_panel()

    assert settings.device.shell.call_args_list == [call("input tap 360 960")] * 3
    settings._dismiss_quick_settings.assert_not_called()


def test_quick_settings_done_requires_clickable_enabled_button() -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.device.return_value.wait.return_value = False
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("missing done"))

    with pytest.raises(AssertionError, match="missing done"):
        settings._close_quick_settings_internet_panel()

    settings.device.assert_called_once_with(
        resourceId="com.android.systemui:id/done_button", enabled=True, clickable=True
    )
    settings.device.shell.assert_not_called()


@pytest.mark.parametrize("enabled", [False, True])
def test_airplane_mode_does_not_click_when_already_in_target_state(enabled) -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.open_airplane_mode_settings = Mock()
    settings.device.return_value.info = {"checked": enabled}

    settings.set_airplane_mode_from_settings(enabled)

    settings.device.click.assert_not_called()


def test_airplane_mode_fails_when_switch_does_not_change(monkeypatch) -> None:
    settings = AdvancedSettingsSupportUI.__new__(AdvancedSettingsSupportUI)
    settings.device = Mock()
    settings.open_airplane_mode_settings = Mock()
    settings.fail_with_artifacts = Mock(side_effect=AssertionError("unchanged"))
    settings.device.return_value.info = {
        "checked": False,
        "bounds": {"left": 100, "right": 200, "top": 300, "bottom": 400},
    }
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_support.time.monotonic",
        Mock(side_effect=[0.0, 0.1, 9.0]),
    )
    monkeypatch.setattr(
        "core.libs.android.wifi_ui.advanced_settings_support.time.sleep", Mock()
    )

    with pytest.raises(AssertionError, match="unchanged"):
        settings.set_airplane_mode_from_settings(True)

    settings.fail_with_artifacts.assert_called_once_with(
        "飞行模式设置页的开关未切换为 开启"
    )


def test_energy_save_airplane_toggle_disables_mode_after_enable_failure() -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    settings.set_airplane_mode_from_settings.side_effect = [
        AssertionError("enable failed"), None
    ]

    with pytest.raises(AssertionError, match="enable failed"):
        _toggle_airplane_mode_from_settings(settings)

    assert settings.set_airplane_mode_from_settings.call_args_list == [
        call(True), call(False)
    ]


def test_custom_input_field_requires_one_edit_text() -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    device = Mock()
    field = Mock()
    field.count = 1
    field.exists = True
    device.return_value = field
    settings.device = device
    page = WiFiAdvancedSettingsUI(settings)

    assert page._custom_input_field("WLAN 漫游阈值") is field
    device.assert_called_once_with(className="android.widget.EditText")


def test_custom_input_field_rejects_multiple_edit_texts() -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    device = Mock()
    field = Mock()
    field.count = 2
    field.exists = True
    device.return_value = field
    settings.device = device
    settings.fail_with_artifacts.side_effect = AssertionError("ambiguous")
    page = WiFiAdvancedSettingsUI(settings)

    try:
        page._custom_input_field("WLAN 漫游阈值")
    except AssertionError as error:
        assert str(error) == "ambiguous"
    else:
        raise AssertionError("expected ambiguous custom input to fail")


@pytest.mark.parametrize("separator", ("-", "~", "\uff5e"))
def test_timeout_custom_dialog_accepts_range_separator_variants(
    separator: str,
) -> None:
    prompt = WiFiAdvancedSettingsUI.WLAN_TIMEOUT_DISCONNECT_CUSTOM_PROMPT.replace(
        "3~20", f"3 {separator} 20 "
    )
    assert WiFiAdvancedSettingsUI.wlan_timeout_disconnect_custom_dialog_matches(
        prompt, WiFiAdvancedSettingsUI.WLAN_TIMEOUT_DISCONNECT_CUSTOM_INPUT_HINT
    )
    assert WiFiAdvancedSettingsUI._range_labels_match(
        WiFiAdvancedSettingsUI.WLAN_TIMEOUT_DISCONNECT_CUSTOM_PROMPT, prompt
    )


@pytest.mark.parametrize(
    ("prompt", "input_hint"),
    (
        ("请输入自定义超时断连时间（2 ～ 20 秒）", "允许填写的数值 3 ~ 20"),
        ("请输入自定义超时断连时间（3 ～ 21 秒）", "允许填写的数值 3 ~ 20"),
        ("请输入自定义超时断连时间（3 ～ 20 分钟）", "允许填写的数值 3 ~ 20"),
        ("请输入自定义漫游时间（3 ～ 20 秒）", "允许填写的数值 3 ~ 20"),
        ("请输入自定义超时断连时间（3 ～ 20 秒）", "允许填写的数值 3 ~ 21"),
    ),
)
def test_timeout_custom_dialog_rejects_incorrect_text(
    prompt: str, input_hint: str
) -> None:
    assert not WiFiAdvancedSettingsUI.wlan_timeout_disconnect_custom_dialog_matches(
        prompt, input_hint
    )


@pytest.mark.parametrize("save_enabled", (False, True))
def test_empty_timeout_checks_save_state_without_reading_hint(
    save_enabled: bool,
) -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    field = Mock(count=1, exists=True)
    field.get_text.return_value = "允许填写的数值 3 ~ 20"
    button = Mock(exists=True, info={"enabled": save_enabled})
    settings.device = Mock(side_effect=(field, button))
    page = WiFiAdvancedSettingsUI(settings)

    with patch.object(page, "open_wlan_timeout_disconnect_custom_dialog") as open_dialog:
        assert page.enter_wlan_timeout_disconnect_custom_value("") == (
            "", save_enabled
        )

    open_dialog.assert_called_once_with()
    field.click.assert_called_once_with()
    field.clear_text.assert_called_once_with()
    field.set_text.assert_not_called()
    field.get_text.assert_not_called()
    button.click.assert_not_called()
    settings.fail_with_artifacts.assert_not_called()
    assert settings.device.call_args_list[-1].kwargs == {
        "resourceId": "android:id/button1"
    }


@pytest.mark.parametrize("value", ("2", "21", "20"))
def test_nonempty_custom_value_still_verifies_readback(value: str) -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    field = Mock(count=1, exists=True)
    field.get_text.return_value = value
    settings.device = Mock(return_value=field)
    page = WiFiAdvancedSettingsUI(settings)

    assert page._enter_custom_value("WLAN 超时断连设置", value) == value

    field.set_text.assert_called_once_with(value)
    field.get_text.assert_called_once_with()
    settings.fail_with_artifacts.assert_not_called()


def test_nonempty_custom_value_rejects_hint_as_readback() -> None:
    settings = Mock(spec=AdvancedSettingsSupportUI)
    field = Mock(count=1, exists=True)
    field.get_text.return_value = "允许填写的数值 3 ~ 20"
    settings.device = Mock(return_value=field)
    settings.fail_with_artifacts.side_effect = AssertionError("readback mismatch")
    page = WiFiAdvancedSettingsUI(settings)

    with pytest.raises(AssertionError, match="readback mismatch"):
        page._enter_custom_value("WLAN 超时断连设置", "20")


def test_range_labels_preserve_negative_signs() -> None:
    assert WiFiAdvancedSettingsUI._range_labels_match(
        "-90 ～ -50 dBm", "-90 ~ -50 dBm"
    )
    assert not WiFiAdvancedSettingsUI._range_labels_match(
        "90 ～ 50 dBm", "-90 ~ -50 dBm"
    )