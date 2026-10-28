from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path
from unittest.mock import Mock, call

import pytest

from core.libs.android.softap_control import SoftAPControl
from core.libs.android.wifi_scenarios.advanced_settings import (
    band,
    energy_save,
    mode,
    priority,
    roam_sensitivity,
    roam_threshold,
    timeout_disconnect,
)
from core.libs.android.wifi_scenarios.hotspot import (
    auto_shutdown,
    defaults,
    stability,
)
from core.libs.android.wifi_ui.advanced_settings_page import WiFiAdvancedSettingsUI


_ANDROID_TESTS = Path(__file__).resolve().parents[2] / "android"
_FOLDERS = ("wlan_advanced_settings", "wlan_hotspot")
_FEATURES = (
    (band, "band"),
    (energy_save, "energy_save"),
    (mode, "mode"),
    (priority, "priority"),
    (roam_sensitivity, "roam_sensitivity"),
    (roam_threshold, "roam_threshold"),
    (timeout_disconnect, "timeout_disconnect"),
)
_PERSISTENT_FEATURES = tuple(
    (module, feature) for module, feature in _FEATURES
    if module not in (band, mode)
)


def _entry_call(function):
    node = ast.parse(inspect.getsource(function)).body[0]
    assert isinstance(node, ast.FunctionDef)
    assert len(node.body) == 1
    statement = node.body[0]
    assert isinstance(statement, ast.Expr)
    expression = statement.value
    assert isinstance(expression, ast.Call)
    assert isinstance(expression.func, ast.Name)
    return expression.func.id, expression


def _implemented_entries():
    entries = []
    for folder in _FOLDERS:
        for path in sorted((_ANDROID_TESTS / folder).glob("test_*.py")):
            module = importlib.import_module(
                f"testcases.android.{folder}.{path.stem}"
            )
            for name, function in vars(module).items():
                if name.startswith("test_") and inspect.isfunction(function):
                    runner_name, _ = _entry_call(function)
                    if runner_name != "run_manual_placeholder":
                        entries.append(pytest.param(module, function, id=name))
    return entries


def _argument_value(node, arguments):
    if isinstance(node, ast.Name):
        return arguments[node.id]
    return ast.literal_eval(node)


@pytest.mark.parametrize("module,function", _implemented_entries())
@pytest.mark.parametrize("failure", (False, True))
def test_entry_delegates_arguments_and_propagates_errors(
    monkeypatch, module, function, failure
) -> None:
    runner_name, expression = _entry_call(function)
    runner = getattr(module, runner_name)
    assert runner.__module__.startswith(
        "core.libs.android.wifi_scenarios."
        + ("hotspot." if "softap" in module.__name__ else "advanced_settings.")
    )
    arguments = {name: object() for name in inspect.signature(function).parameters}
    expected_args = [_argument_value(arg, arguments) for arg in expression.args]
    expected_kwargs = {}
    for keyword in expression.keywords:
        assert keyword.arg is not None
        expected_kwargs[keyword.arg] = _argument_value(keyword.value, arguments)
    inspect.signature(runner).bind(*expected_args, **expected_kwargs)
    error = RuntimeError("scenario failed")
    delegate = Mock(side_effect=error if failure else None)
    monkeypatch.setattr(module, runner_name, delegate)

    if failure:
        with pytest.raises(RuntimeError) as caught:
            function(**arguments)
        assert caught.value is error
    else:
        function(**arguments)

    delegate.assert_called_once_with(*expected_args, **expected_kwargs)


@pytest.mark.parametrize(
    "folder,total,manual", (
        ("wlan_advanced_settings", 184, 100),
        ("wlan_hotspot", 78, 66),
    ),
)
def test_case_identity_and_manual_inventory(folder, total, manual) -> None:
    functions = []
    identifiers = []
    placeholders = 0
    for path in (_ANDROID_TESTS / folder).glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                assert node.name.startswith("test_")
                functions.append(node)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Attribute) and node.func.attr == "case_id":
                identifiers.append(ast.literal_eval(node.args[0]))
            elif isinstance(node.func, ast.Name) and node.func.id == "run_manual_placeholder":
                placeholders += 1
    assert len(functions) == len(identifiers) == len(set(identifiers)) == total
    assert placeholders == manual
    assert len(_implemented_entries()) == 96


@pytest.mark.parametrize("module,feature", _FEATURES)
@pytest.mark.parametrize("matches", (False, True))
def test_selected_setting_keeps_page_order_and_assertion(
    monkeypatch, module, feature, matches
) -> None:
    page = Mock(spec=WiFiAdvancedSettingsUI)
    monkeypatch.setattr(module, "WiFiAdvancedSettingsUI", Mock(return_value=page))
    monkeypatch.setattr(module, "_write_uncaptured_line", Mock())
    getattr(page, f"wlan_{feature}_summary").return_value = "selected"
    getattr(page, f"wlan_{feature}_matches").return_value = matches
    runner = getattr(module, f"run_wlan_{feature}_display_case")

    if matches:
        runner(Mock(), Mock(), "selected")
    else:
        with pytest.raises(pytest.fail.Exception):
            runner(Mock(), Mock(), "selected")

    assert page.mock_calls == [
        call.open(),
        getattr(call, f"open_wlan_{feature}_selector")(),
        getattr(call, f"select_wlan_{feature}")("selected"),
        getattr(call, f"confirm_wlan_{feature}_selection")(),
        getattr(call, f"wlan_{feature}_summary")(),
        getattr(call, f"wlan_{feature}_matches")("selected", "selected"),
    ]


@pytest.mark.parametrize("module,feature", _PERSISTENT_FEATURES)
@pytest.mark.parametrize(
    "action", ("reboot", "settings_toggle", "quick_settings_toggle", "airplane_toggle")
)
def test_persistence_runner_keeps_original_lifecycle_action(
    monkeypatch, module, feature, action
) -> None:
    capture = Mock()

    def execute_action(settings_ui, capsys, lifecycle_action, *messages):
        capture(settings_ui, capsys, *messages)
        lifecycle_action()

    monkeypatch.setattr(
        module, f"_assert_wlan_{feature}_persists", execute_action
    )
    reboot = Mock()
    monkeypatch.setattr(module, "reboot_and_wait", reboot)
    runner = getattr(module, f"run_wlan_{feature}_{action}_persistence_case")
    settings, wifi, output = Mock(), Mock(), Mock()
    arguments = {"settings_ui": settings, "wifi": wifi, "capsys": output}

    runner(**{name: arguments[name] for name in inspect.signature(runner).parameters})

    assert capture.call_args.args[:2] == (settings, output)
    if action == "reboot":
        reboot.assert_called_once_with(wifi)
        assert settings.mock_calls == []
    else:
        reboot.assert_not_called()
        method = {
            "settings_toggle": "set_wifi_switch"
            if module is energy_save else "set_wifi_enabled_from_settings",
            "quick_settings_toggle": "set_quick_settings_wifi_enabled",
            "airplane_toggle": "set_airplane_mode_from_settings",
        }[action]
        states = (True, False) if action == "airplane_toggle" else (False, True)
        assert settings.mock_calls == [
            getattr(call, method)(state) for state in states
        ]


@pytest.mark.parametrize("module,feature", _PERSISTENT_FEATURES)
def test_airplane_failure_keeps_existing_restoration_difference(module, feature) -> None:
    settings = Mock()
    error = RuntimeError("cannot enable airplane mode")
    settings.set_airplane_mode_from_settings.side_effect = [error, None]

    with pytest.raises(RuntimeError) as caught:
        module._toggle_airplane_mode_from_settings(settings)

    assert caught.value is error
    expected = [call(True), call(False)] if module is energy_save else [call(True)]
    assert settings.set_airplane_mode_from_settings.call_args_list == expected


@pytest.mark.parametrize(
    "module,feature,values,command",
    (
        (roam_threshold, "roam_threshold", ("60", "65", "70"),
         'getprop | grep -iE "persist.vendor.wifi.roam.value"'),
        (roam_sensitivity, "roam_sensitivity", ("5", "7", "9"),
         'getprop | grep -iE "persist.vendor.wifi.roam_delta"'),
    ),
)
@pytest.mark.parametrize("failure", (None, "summary", "property"))
def test_roaming_cycle_keeps_ten_cycles_and_backend_checks(
    monkeypatch, module, feature, values, command, failure
) -> None:
    page = Mock(spec=WiFiAdvancedSettingsUI)
    monkeypatch.setattr(module, "WiFiAdvancedSettingsUI", Mock(return_value=page))
    monkeypatch.setattr(module, "_write_uncaptured_line", Mock())
    getattr(page, f"wlan_{feature}_matches").return_value = failure != "summary"
    shell = Mock(side_effect=list(values) * 10)
    if failure == "property":
        shell.side_effect = None
        shell.return_value = "not-a-property-value"
    runner = getattr(module, f"run_wlan_{feature}_cycle_case")

    if failure is None:
        runner(Mock(), shell, Mock())
        assert shell.call_args_list == [call(command)] * 30
        assert getattr(page, f"select_wlan_{feature}").call_count == 30
    else:
        with pytest.raises(pytest.fail.Exception):
            runner(Mock(), shell, Mock())
        assert getattr(page, f"select_wlan_{feature}").call_count == 1
        assert shell.call_count == (0 if failure == "summary" else 1)


@pytest.mark.parametrize(
    "module,feature", (
        (roam_threshold, "roam_threshold"),
        (roam_sensitivity, "roam_sensitivity"),
        (timeout_disconnect, "timeout_disconnect"),
    ),
)
@pytest.mark.parametrize("save_enabled", (False, True))
def test_custom_value_keeps_original_save_button_expectation(
    monkeypatch, module, feature, save_enabled
) -> None:
    page = Mock(spec=WiFiAdvancedSettingsUI)
    monkeypatch.setattr(module, "WiFiAdvancedSettingsUI", Mock(return_value=page))
    monkeypatch.setattr(module, "_write_uncaptured_line", Mock())
    method = getattr(page, f"enter_wlan_{feature}_custom_value")
    method.return_value = ("21", save_enabled)
    runner = getattr(module, f"run_wlan_{feature}_custom_value_cannot_save_case")

    if save_enabled:
        with pytest.raises(pytest.fail.Exception):
            runner(Mock(), Mock(), "21")
    else:
        runner(Mock(), Mock(), "21")

    method.assert_called_once_with("21")


@pytest.fixture
def scenario_output(monkeypatch):
    outputs = {}
    for module in (auto_shutdown, defaults, stability):
        outputs[module] = Mock()
        monkeypatch.setattr(module, "_write_uncaptured_line", outputs[module])
    return outputs


@pytest.fixture
def softap(monkeypatch, scenario_output):
    control = Mock(spec=SoftAPControl)
    for module in (auto_shutdown, defaults, stability):
        monkeypatch.setattr(module, "SoftAPControl", Mock(return_value=control))
    return control


def test_auto_shutdown_keeps_exact_window_and_service_state(
    softap, scenario_output, capsys
) -> None:
    softap.is_hotspot_enabled.return_value = True
    softap.connected_client_count.return_value = 0
    softap.wait_for_auto_shutdown_window.return_value = False
    softap.is_hotspot_active.return_value = False

    auto_shutdown.run_hotspot_auto_shutdown_enabled_case(Mock(), capsys)

    assert softap.mock_calls[:5] == [
        call.open_settings(), call.enable_auto_shutdown(), call.enable_hotspot(),
        call.is_hotspot_enabled(), call.connected_client_count(),
    ]
    kwargs = softap.wait_for_auto_shutdown_window.call_args.kwargs
    assert kwargs["earliest_shutdown_seconds"] == 570
    assert kwargs["latest_shutdown_seconds"] == 630
    kwargs["on_progress"](600)
    assert "10:00" in scenario_output[auto_shutdown].call_args.args[1]
    softap.is_hotspot_active.assert_called_once_with()
    softap.is_hotspot_enabled.assert_called_once_with()


@pytest.mark.parametrize("connected_before_wait", (False, True))
def test_auto_shutdown_skips_on_client_without_final_state_check(
    softap, capsys, connected_before_wait
) -> None:
    softap.is_hotspot_enabled.return_value = True
    softap.connected_client_count.return_value = int(connected_before_wait)
    softap.wait_for_auto_shutdown_window.return_value = True

    with pytest.raises(pytest.skip.Exception, match="其他设备连接"):
        auto_shutdown.run_hotspot_auto_shutdown_enabled_case(Mock(), capsys)

    assert softap.wait_for_auto_shutdown_window.call_count == (0 if connected_before_wait else 1)
    softap.is_hotspot_active.assert_not_called()


def test_auto_shutdown_enabled_fails_when_hotspot_stays_active(softap, capsys) -> None:
    softap.is_hotspot_enabled.return_value = True
    softap.connected_client_count.return_value = 0
    softap.wait_for_auto_shutdown_window.return_value = False
    softap.is_hotspot_active.return_value = True

    with pytest.raises(AssertionError, match="09:30-10:30"):
        auto_shutdown.run_hotspot_auto_shutdown_enabled_case(Mock(), capsys)


@pytest.mark.parametrize("client_connected,enabled", ((False, True), (False, False), (True, True)))
def test_auto_shutdown_disabled_keeps_twelve_minute_observation(
    softap, scenario_output, capsys, client_connected, enabled
) -> None:
    softap.wait_for_no_client_window.return_value = client_connected
    softap.is_hotspot_enabled.return_value = enabled

    if client_connected:
        with pytest.raises(pytest.skip.Exception, match="其他设备连接"):
            auto_shutdown.run_hotspot_auto_shutdown_disabled_case(Mock(), capsys)
        softap.is_hotspot_enabled.assert_not_called()
    elif not enabled:
        with pytest.raises(AssertionError, match="12 分钟"):
            auto_shutdown.run_hotspot_auto_shutdown_disabled_case(Mock(), capsys)
    else:
        auto_shutdown.run_hotspot_auto_shutdown_disabled_case(Mock(), capsys)
    assert softap.wait_for_no_client_window.call_args.args == (720,)
    kwargs = softap.wait_for_no_client_window.call_args.kwargs
    assert kwargs["expected_hotspot_enabled"] is True
    assert kwargs["expected_auto_shutdown_enabled"] is False
    kwargs["on_progress"](720)
    assert "12:00" in scenario_output[auto_shutdown].call_args.args[1]


@pytest.mark.parametrize("fast", (False, True))
@pytest.mark.parametrize("failure", (False, True))
def test_hotspot_toggle_keeps_cycles_parameters_and_exception(
    softap, scenario_output, capsys, fast, failure
) -> None:
    error = AssertionError("toggle failed")
    softap.toggle_hotspot_cycles.side_effect = error if failure else None
    runner = (
        stability.run_hotspot_fast_toggle_stability_case
        if fast else stability.run_hotspot_toggle_stability_case
    )
    if failure:
        with pytest.raises(AssertionError) as caught:
            runner(Mock(), capsys)
        assert caught.value is error
    else:
        runner(Mock(), capsys)
    assert softap.toggle_hotspot_cycles.call_args.args == (20,)
    kwargs = softap.toggle_hotspot_cycles.call_args.kwargs
    assert set(kwargs) == (
        {"on_progress", "poll_interval_seconds", "cache_main_switch_bounds"}
        if fast else {"on_progress"}
    )
    if fast:
        assert kwargs["poll_interval_seconds"] == 0.1
        assert kwargs["cache_main_switch_bounds"] is True
    kwargs["on_progress"](1, "打开")
    assert "第1次打开" in scenario_output[stability].call_args.args[1]


@pytest.mark.parametrize(
    "runner,method,value",
    (
        (defaults.run_hotspot_default_switch_case, "is_hotspot_enabled", False),
        (defaults.run_hotspot_default_security_case, "security_summary", "WPA2/WPA3-Personal"),
        (defaults.run_hotspot_default_band_case, "compatibility_summary", "2.4GHz"),
        (defaults.run_hotspot_default_auto_shutdown_case, "is_auto_shutdown_enabled", True),
        (defaults.run_hotspot_security_editor_default_case, "open_security_editor",
         ([], "WPA2/WPA3-Personal")),
        (defaults.run_hotspot_band_editor_default_case, "open_compatibility_editor",
         ([], "2.4GHz")),
    ),
)
def test_hotspot_default_checks_keep_expected_values(
    softap, capsys, runner, method, value
) -> None:
    softap.is_security_editor_open.return_value = False
    getattr(softap, method).return_value = value

    runner(Mock(), capsys)

    softap.open_settings.assert_called_once_with()
    getattr(softap, method).assert_called_once_with()


@pytest.mark.parametrize("security", (False, True))
@pytest.mark.parametrize("default_selected", (False, True))
def test_hotspot_options_keep_warning_only_for_nondefault_selection(
    softap, scenario_output, capsys, security, default_selected
) -> None:
    softap.is_security_editor_open.return_value = False
    options = (
        ["WPA3-Personal", "WPA2/WPA3-Personal", "WPA2-Personal", "无"]
        if security else ["2.4GHz", "5GHz"]
    )
    selected = ("WPA2/WPA3-Personal" if security else "2.4GHz") if default_selected else "other"
    method = softap.open_security_editor if security else softap.open_compatibility_editor
    method.return_value = (options, selected)
    runner = (
        defaults.run_hotspot_security_options_case
        if security else defaults.run_hotspot_band_options_case
    )

    runner(Mock(), capsys)

    message = scenario_output[defaults].call_args.args[1]
    assert ("请关注" in message) is not default_selected


@pytest.mark.parametrize("security", (False, True))
def test_hotspot_options_reject_wrong_order_or_missing_option(softap, capsys, security) -> None:
    softap.is_security_editor_open.return_value = False
    method = softap.open_security_editor if security else softap.open_compatibility_editor
    method.return_value = (["5GHz", "2.4GHz"], "2.4GHz")
    runner = (
        defaults.run_hotspot_security_options_case
        if security else defaults.run_hotspot_band_options_case
    )

    with pytest.raises(AssertionError, match="不符合用例预期"):
        runner(Mock(), capsys)
