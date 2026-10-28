from unittest.mock import Mock

import pytest

from core.libs.android.systemui_pages import quick_settings_page
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.libs.android.wifi_scenarios.systemui.navigation import _assert_open_latency
from core.libs.android.wifi_scenarios.advanced_settings.energy_save import (
    _toggle_wlan_from_quick_settings,
)


def test_open_latency_accepts_one_second() -> None:
    _assert_open_latency("case", 1.0)


def test_open_latency_rejects_more_than_one_second() -> None:
    with pytest.raises(pytest.fail.Exception, match="要求 <=1s"):
        _assert_open_latency("case", 1.001, cycle=2)


class _RetryDevice:
    def __init__(self) -> None:
        self.expand_count = 0

    def press(self, key: str) -> None:
        pass

    def shell(self, command: str) -> None:
        if command == "cmd statusbar expand-settings":
            self.expand_count += 1

    def dump_hierarchy(self) -> str:
        if self.expand_count >= 3:
            return 'resource-id="com.android.systemui:id/qs_frame"'
        return 'package="com.android.launcher3"'

class _RetrySettingsUI:
    def __init__(self) -> None:
        self.device = _RetryDevice()
        self.reset_count = 0

    def reset_uiautomator(self) -> None:
        self.reset_count += 1

    def fail_with_artifacts(self, message: str) -> None:
        raise AssertionError(message)


def test_open_quick_settings_retries_shell_command_on_final_attempt(monkeypatch) -> None:
    settings_ui = _RetrySettingsUI()
    monkeypatch.setattr(quick_settings_page.time, "sleep", lambda _seconds: None)

    quick_settings_page.open_quick_settings(settings_ui)

    assert settings_ui.device.expand_count == 3
    assert settings_ui.reset_count == 1


def test_click_control_uses_adb_bounds_right_side_entry() -> None:
    settings_ui = Mock()
    control = Mock()
    control.info = {
        "bounds": {"left": 100, "top": 200, "right": 500, "bottom": 400}
    }

    quick_settings_page._click_control(settings_ui, control)

    settings_ui.device.shell.assert_called_once_with("input tap 450 300")
    control.click.assert_not_called()


def test_internet_tile_excludes_non_clickable_status_icon() -> None:
    settings_ui = Mock()
    selector = Mock()
    selector.wait.return_value = True
    settings_ui.device.return_value = selector

    assert quick_settings_page.internet_tile(settings_ui) is selector
    settings_ui.device.assert_called_once_with(
        descriptionMatches=quick_settings_page.INTERNET_TILE_PATTERN,
        clickable=True,
    )


def test_open_all_wifi_networks_falls_back_to_text_selector() -> None:
    settings_ui = Mock()
    resource_selector = Mock()
    resource_selector.click_exists.return_value = False
    text_selector = Mock()
    text_selector.click_exists.return_value = True
    settings_ui.device.side_effect = [resource_selector, text_selector]

    quick_settings_page.open_all_wifi_networks(settings_ui)

    settings_ui.device.assert_any_call(
        resourceId="com.android.systemui:id/see_all_layout"
    )
    settings_ui.device.assert_any_call(textMatches=quick_settings_page.SEE_ALL_PATTERN)


@pytest.mark.parametrize("initial_enabled", [False, True])
def test_energy_save_quick_settings_toggle_uses_fixture_class(
    monkeypatch, initial_enabled
) -> None:
    settings_ui = AndroidSettingsUI.__new__(AndroidSettingsUI)
    settings_ui.device = Mock()
    settings_ui.fail_with_artifacts = Mock(side_effect=AssertionError("UI failure"))
    opened = Mock()
    monkeypatch.setattr(quick_settings_page, "open_internet_dialog", opened)
    toggle = Mock()
    toggle.info = {
        "checked": initial_enabled,
        "bounds": {"left": 500, "top": 200, "right": 600, "bottom": 300},
    }
    done = Mock()
    done.info = {"bounds": {"left": 400, "top": 800, "right": 600, "bottom": 900}}
    settings_ui.device.side_effect = lambda **criteria: (
        toggle if criteria.get("resourceId", "").endswith("/wifi_toggle") else done
    )
    settings_ui.device.window_size.return_value = (720, 1600)
    settings_ui.device.dump_hierarchy.return_value = '<hierarchy package="launcher"/>'
    states = []

    def tap(command) -> None:
        if command == "input tap 550 250":
            toggle.info["checked"] = not toggle.info["checked"]
            states.append(toggle.info["checked"])

    settings_ui.device.shell.side_effect = tap

    _toggle_wlan_from_quick_settings(settings_ui)

    assert states == ([False, True] if initial_enabled else [True])
    assert toggle.info["checked"] is True
    assert opened.call_count == 2
    assert all(arguments.kwargs == {"capture": False} for arguments in opened.call_args_list)
    assert done.wait_gone.call_count == 2
    assert sum(
        arguments.args == ("input swipe 360 1440 360 320 300",)
        for arguments in settings_ui.device.shell.call_args_list
    ) == 2
    assert sum(
        arguments.args == ("input tap 575 850",)
        for arguments in settings_ui.device.shell.call_args_list
    ) == 2
    settings_ui.fail_with_artifacts.assert_not_called()


def test_open_internet_dialog_accepts_disabled_wifi_toggle(monkeypatch) -> None:
    settings_ui = Mock()
    settings_ui.device.dump_hierarchy.return_value = (
        '<hierarchy><node resource-id="com.android.systemui:id/internet_dialog_title"/>'
        '<node resource-id="com.android.systemui:id/wifi_toggle" checked="false"/></hierarchy>'
    )
    monkeypatch.setattr(quick_settings_page, "open_quick_settings", Mock())
    monkeypatch.setattr(quick_settings_page, "internet_tile", Mock())
    monkeypatch.setattr(quick_settings_page, "_click_control", Mock())

    quick_settings_page.open_internet_dialog(settings_ui, capture=False)

    settings_ui.fail_with_artifacts.assert_not_called()


def test_quick_settings_wifi_toggle_reports_unchanged_state(monkeypatch) -> None:
    settings_ui = AndroidSettingsUI.__new__(AndroidSettingsUI)
    settings_ui.device = Mock()
    settings_ui.device.return_value.info = {
        "checked": True,
        "bounds": {"left": 500, "top": 200, "right": 600, "bottom": 300},
    }
    settings_ui.fail_with_artifacts = Mock(side_effect=AssertionError("未切换为 关闭"))
    monkeypatch.setattr(quick_settings_page, "open_internet_dialog", Mock())
    monkeypatch.setattr(quick_settings_page.time, "monotonic", Mock(side_effect=[0, 0, 6]))
    monkeypatch.setattr(quick_settings_page.time, "sleep", Mock())

    with pytest.raises(AssertionError, match="未切换为 关闭"):
        settings_ui.set_quick_settings_wifi_enabled(False)

    settings_ui.device.swipe.assert_not_called()


def test_quick_settings_waits_for_dialog_close_before_swipe(monkeypatch) -> None:
    settings_ui = AndroidSettingsUI.__new__(AndroidSettingsUI)
    settings_ui.device = Mock()
    settings_ui.device.return_value.info = {
        "checked": False,
        "bounds": {"left": 400, "top": 800, "right": 600, "bottom": 900},
    }
    settings_ui.device.return_value.wait_gone.return_value = False
    settings_ui.fail_with_artifacts = Mock(side_effect=AssertionError("互联网面板未关闭"))
    monkeypatch.setattr(quick_settings_page, "open_internet_dialog", Mock())

    with pytest.raises(AssertionError, match="互联网面板未关闭"):
        settings_ui.set_quick_settings_wifi_enabled(False)

    assert not any(
        arguments.args[0].startswith("input swipe")
        for arguments in settings_ui.device.shell.call_args_list
    )


@pytest.mark.parametrize("dismissal", ["second_swipe", "collapse", "stuck"])
def test_quick_settings_dismisses_notification_shade_after_first_swipe(
    monkeypatch, dismissal
) -> None:
    settings_ui = AndroidSettingsUI.__new__(AndroidSettingsUI)
    settings_ui.device = Mock()
    settings_ui.device.return_value.info = {
        "checked": False,
        "bounds": {"left": 400, "top": 800, "right": 600, "bottom": 900},
    }
    settings_ui.device.window_size.return_value = (720, 1600)
    settings_ui.device.dump_hierarchy.side_effect = [
        'resource-id="com.android.systemui:id/qs_frame"',
        '<hierarchy/>' if dismissal == "second_swipe" else 'resource-id="com.android.systemui:id/qs_frame"',
        'resource-id="com.android.systemui:id/qs_frame"' if dismissal == "stuck" else '<hierarchy/>',
    ]
    settings_ui.fail_with_artifacts = Mock(side_effect=AssertionError("快速设置栏未退出"))
    monkeypatch.setattr(quick_settings_page, "open_internet_dialog", Mock())
    monkeypatch.setattr(
        quick_settings_page.time, "monotonic", Mock(side_effect=[0, 0, 0, 0, 3, 3, 3, 6, 6, 6, 9])
    )
    monkeypatch.setattr(quick_settings_page.time, "sleep", Mock())

    if dismissal == "stuck":
        with pytest.raises(AssertionError, match="快速设置栏未退出"):
            settings_ui.set_quick_settings_wifi_enabled(False)
    else:
        settings_ui.set_quick_settings_wifi_enabled(False)
        settings_ui.fail_with_artifacts.assert_not_called()

    assert [
        arguments.args[0]
        for arguments in settings_ui.device.shell.call_args_list
        if arguments.args[0].startswith("input swipe")
    ] == ["input swipe 360 1440 360 320 300", "input swipe 360 900 360 160 300"]
    assert any(
        arguments.args == ("cmd statusbar collapse",)
        for arguments in settings_ui.device.shell.call_args_list
    ) == (dismissal != "second_swipe")
