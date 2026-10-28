from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path
from unittest.mock import Mock, call

import pytest

from core.libs.android.wifi_scenarios.welcome import (
    _helpers,
    connection_config,
    navigation,
    network_details,
    ssid_display,
    version,
    wifi_icon,
)
from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI


_CASE_DIRECTORY = Path(__file__).resolve().parents[2] / "android" / "wlan_components_welcome"
_IMPLEMENTED_MODULES = ("button", "conncfg", "netdetails", "ssidshow", "version", "wifiicon")


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
    for suffix in _IMPLEMENTED_MODULES:
        module = importlib.import_module(
            "testcases.android.wlan_components_welcome."
            f"test_func_components_welcome_{suffix}"
        )
        for name, function in vars(module).items():
            if not name.startswith("test_") or not inspect.isfunction(function):
                continue
            runner_name, _ = _entry_call(function)
            if runner_name != "run_manual_placeholder":
                entries.append(pytest.param(module, function, id=name))
    return entries


def _argument_value(node, arguments):
    if isinstance(node, ast.Name):
        return arguments[node.id]
    if isinstance(node, ast.Subscript):
        assert isinstance(node.value, ast.Name)
        return arguments[node.value.id][ast.literal_eval(node.slice)]
    return ast.literal_eval(node)


@pytest.mark.parametrize("module,function", _implemented_entries())
def test_welcome_entry_delegates_to_one_scenario(monkeypatch, module, function) -> None:
    runner_name, expression = _entry_call(function)
    runner = getattr(module, runner_name)
    assert runner.__module__.startswith("core.libs.android.wifi_scenarios.welcome.")
    arguments = {name: object() for name in inspect.signature(function).parameters}
    arguments["wifi_case"] = {"case_id": "welcome-case"}
    expected_args = [_argument_value(arg, arguments) for arg in expression.args]
    expected_kwargs = {}
    for keyword in expression.keywords:
        assert keyword.arg is not None
        expected_kwargs[keyword.arg] = _argument_value(keyword.value, arguments)
    inspect.signature(runner).bind(*expected_args, **expected_kwargs)
    delegate = Mock()
    monkeypatch.setattr(module, runner_name, delegate)

    function(**arguments)

    delegate.assert_called_once_with(*expected_args, **expected_kwargs)


def test_welcome_case_and_placeholder_inventory_is_unchanged() -> None:
    identifiers = []
    functions = []
    placeholders = 0
    for path in _CASE_DIRECTORY.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert all(
            not isinstance(node, ast.FunctionDef) or node.name.startswith("test_")
            for node in tree.body
        )
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == "case_id":
                    identifiers.append(ast.literal_eval(node.args[0]))
                elif isinstance(node.func, ast.Name) and node.func.id == "run_manual_placeholder":
                    placeholders += 1
    assert len(functions) == 126
    assert len(identifiers) == len(set(identifiers)) == 128
    assert placeholders == 74
    assert len(_implemented_entries()) == 52


@pytest.fixture
def welcome_page(monkeypatch):
    page = Mock(spec=WelcomeWlanUI)
    page.fail_with_artifacts.side_effect = AssertionError("page failure")
    for module in (connection_config, navigation, network_details, ssid_display, wifi_icon):
        monkeypatch.setattr(module, "WelcomeWlanUI", Mock(return_value=page))
    return page


@pytest.fixture
def network_entry(monkeypatch):
    entry = {"ssid": "lab-network", "pwd": "24681357"}
    for module in (connection_config, network_details, wifi_icon):
        monkeypatch.setattr(module, "get_wifi_list_entry", Mock(return_value=entry))
    monkeypatch.setattr(network_details, "load_wifi_ssid", Mock(return_value={}))
    return entry


@pytest.mark.parametrize(
    "helper,matched,expected",
    (
        (_helpers._wait_for_wifi_connection, ["lab-network"], True),
        (_helpers._wait_for_wifi_connection, [], False),
        (_helpers._wait_for_wifi_disconnection, [], True),
        (_helpers._wait_for_wifi_disconnection, ["lab-network"], False),
    ),
)
def test_association_wait_keeps_final_target_specific_probe(helper, matched, expected) -> None:
    wifi = Mock()
    wifi.match_associated_ssids.return_value = (matched, [])

    assert helper(wifi, "lab-network", timeout=0) is expected

    wifi.match_associated_ssids.assert_called_once_with(
        ["lab-network"], use_dumpsys_for_missing=True
    )


@pytest.mark.parametrize(
    "helper,states",
    (
        (_helpers._wait_for_wifi_connection, [([], []), (["lab-network"], [])]),
        (_helpers._wait_for_wifi_disconnection, [(["lab-network"], []), ([], [])]),
    ),
)
def test_association_wait_preserves_poll_interval(monkeypatch, helper, states) -> None:
    wifi = Mock()
    wifi.match_associated_ssids.side_effect = states
    sleep = Mock()
    monkeypatch.setattr(_helpers.time, "sleep", sleep)

    assert helper(wifi, "lab-network")

    assert wifi.match_associated_ssids.call_count == 2
    sleep.assert_called_once_with(0.5)


def test_open_network_connects_then_deletes(
    monkeypatch, welcome_page, network_entry, tmp_path, capsys
) -> None:
    factory = Mock(return_value=welcome_page)
    monkeypatch.setattr(connection_config, "WelcomeWlanUI", factory)
    events = Mock()
    events.attach_mock(welcome_page, "page")
    events.wifi.match_associated_ssids.side_effect = [
        ([network_entry["ssid"]], []), ([], [])
    ]
    settings = Mock()

    connection_config.run_welcome_open_network_case(
        events.wifi, {}, settings, tmp_path, capsys
    )

    ssid = network_entry["ssid"]
    assert events.mock_calls == [
        call.page.connect_open_network(ssid),
        call.wifi.match_associated_ssids([ssid], use_dumpsys_for_missing=True),
        call.page.open_connected_network_details(ssid),
        call.page.delete_network_from_details(),
        call.wifi.match_associated_ssids([ssid], use_dumpsys_for_missing=True),
    ]
    factory.assert_called_once_with(
        settings.device, tmp_path / "welcome-wlan-ui"
    )
    assert settings.mock_calls == []


def test_open_network_connection_failure_keeps_artifacts(
    monkeypatch, welcome_page, network_entry, tmp_path, capsys
) -> None:
    monkeypatch.setattr(connection_config, "_wait_for_wifi_connection", Mock(return_value=False))
    wifi = Mock()
    wifi.list_connected_ssids.return_value = ["other-network"]

    with pytest.raises(AssertionError, match="page failure"):
        connection_config.run_welcome_open_network_case(wifi, {}, Mock(), tmp_path, capsys)

    assert network_entry["ssid"] in welcome_page.fail_with_artifacts.call_args.args[0]
    assert "other-network" in welcome_page.fail_with_artifacts.call_args.args[0]
    welcome_page.delete_network_from_details.assert_not_called()


def test_password_length_checks_seven_then_eight_and_cleans_up(
    welcome_page, network_entry, tmp_path, capsys
) -> None:
    wifi = Mock()
    wifi.match_associated_ssids.side_effect = [([network_entry["ssid"]], []), ([], [])]
    welcome_page.enter_password.return_value = True
    welcome_page.is_connect_enabled.side_effect = [False, True]

    connection_config.run_welcome_password_length_case(wifi, {}, Mock(), tmp_path, capsys)

    assert welcome_page.enter_password.call_args_list == [
        call("1234567"), call(network_entry["pwd"])
    ]
    welcome_page.connect_network.assert_called_once_with()
    welcome_page.delete_network_from_details.assert_called_once_with()
    assert wifi.match_associated_ssids.call_count == 2


def test_password_visibility_checks_both_toggle_directions(
    welcome_page, network_entry, tmp_path, capsys
) -> None:
    welcome_page.enter_password.return_value = True
    welcome_page.is_password_masked.side_effect = [True, False, True]

    connection_config.run_welcome_password_visibility_case({}, Mock(), tmp_path, capsys)

    assert welcome_page.toggle_password_visibility.call_count == 2
    welcome_page.cancel_network_config.assert_called_once_with()
    welcome_page.fail_with_artifacts.assert_not_called()


@pytest.mark.parametrize("masked", ([False], [True, True], [True, False, False]))
def test_password_visibility_failure_is_not_swallowed(
    welcome_page, network_entry, tmp_path, capsys, masked
) -> None:
    welcome_page.enter_password.return_value = True
    welcome_page.is_password_masked.side_effect = masked

    with pytest.raises(AssertionError, match="page failure"):
        connection_config.run_welcome_password_visibility_case({}, Mock(), tmp_path, capsys)

    welcome_page.cancel_network_config.assert_not_called()


@pytest.mark.parametrize(
    "field,value,initial",
    (("ip_address", "192.168.1.100", None), ("gateway", "192.168.1.1", "192.168.0.1")),
)
def test_static_field_input_preserves_readback_and_cancel(
    welcome_page, network_entry, tmp_path, capsys, field, value, initial
) -> None:
    welcome_page.set_static_field.side_effect = lambda name, text: text

    network_details.run_welcome_static_field_input_case(
        Mock(), tmp_path, capsys, field, value, initial_value=initial
    )

    expected = [call(field, value)]
    if initial is not None:
        expected.insert(0, call(field, initial))
    assert welcome_page.set_static_field.call_args_list == expected
    welcome_page.select_ip_mode.assert_called_once_with("静态")
    welcome_page.cancel_network_config.assert_called_once_with()


@pytest.mark.parametrize("already_open", (False, True))
def test_static_rejection_preserves_defaults_keyboard_and_disabled_button(
    welcome_page, network_entry, tmp_path, capsys, already_open
) -> None:
    welcome_page.is_network_config_open.return_value = already_open
    welcome_page.current_ip_mode.return_value = "静态" if already_open else "DHCP"
    welcome_page.enter_password.return_value = True
    welcome_page.set_static_field.side_effect = lambda name, text, **kwargs: text
    welcome_page.is_connect_enabled.side_effect = [True, False]

    network_details.run_welcome_static_field_rejection_case(
        Mock(), tmp_path, capsys, "ip_address", ""
    )

    assert welcome_page.set_static_field.call_args_list == [
        call("ip_address", network_details.DEFAULT_REQUIRED_STATIC_IP_ADDRESS),
        call("ip_address", "", verify_readback=False),
    ]
    welcome_page.cancel_network_config.assert_called_once_with()
    if already_open:
        welcome_page.open_encrypted_network_config.assert_not_called()
        welcome_page.enter_password.assert_not_called()
        welcome_page.dismiss_keyboard.assert_not_called()
        welcome_page.select_ip_mode.assert_not_called()
    else:
        welcome_page.open_encrypted_network_config.assert_called_once_with(network_entry["ssid"])
        welcome_page.enter_password.assert_called_once_with(network_entry["pwd"])
        welcome_page.dismiss_keyboard.assert_called_once_with()
        welcome_page.select_ip_mode.assert_called_once_with("静态")


def test_static_rejection_requires_enabled_baseline(
    welcome_page, network_entry, tmp_path, capsys
) -> None:
    welcome_page.is_network_config_open.return_value = True
    welcome_page.current_ip_mode.return_value = "静态"
    welcome_page.set_static_field.side_effect = lambda name, text: text
    welcome_page.is_connect_enabled.return_value = False

    with pytest.raises(AssertionError, match="page failure"):
        network_details.run_welcome_static_field_rejection_case(
            Mock(), tmp_path, capsys, "gateway", "~!"
        )

    welcome_page.set_static_field.assert_called_once_with(
        "ip_address", network_details.DEFAULT_REQUIRED_STATIC_IP_ADDRESS
    )
    welcome_page.cancel_network_config.assert_not_called()


@pytest.mark.parametrize("number", (1, 2, 3, 4))
def test_encoded_ssid_entry_keeps_ap_backed_runner(
    monkeypatch, welcome_page, tmp_path, capsys, number
) -> None:
    delegate = Mock()
    monkeypatch.setattr(ssid_display, "run_welcome_ssid_display_case", delegate)
    settings = Mock()
    shell, data, ap = Mock(), {}, Mock()
    case_id = f"Func_Components_Welcome_SsidShow_UI_{number:03d}"

    ssid_display.run_welcome_encoded_ssid_display_case(
        case_id, shell, data, settings, tmp_path, capsys, ap
    )

    delegate.assert_called_once_with(
        case_id, shell, data, welcome_page, ap,
        entry_id=ssid_display.WELCOME_SSID_PROFILE_BY_CASE[case_id],
    )


@pytest.mark.parametrize("number", (5, 6, 7, 9))
def test_preconfigured_ssid_does_not_configure_ap(
    monkeypatch, welcome_page, tmp_path, capsys, number
) -> None:
    delegate = Mock()
    monkeypatch.setattr(ssid_display, "run_welcome_ssid_display_case", delegate)
    entry = Mock(return_value={"ssid": "existing-ssid"})
    monkeypatch.setattr(ssid_display, "get_ssid_pwd_entry", entry)
    welcome_page.find_ssid.return_value = True
    data = {}
    case_id = f"Func_Components_Welcome_SsidShow_UI_{number:03d}"

    ssid_display.run_welcome_preconfigured_ssid_display_case(
        data, Mock(), tmp_path, capsys, {"case_id": case_id}
    )

    entry.assert_called_once_with(
        data, entry_id=ssid_display.WELCOME_SSID_PROFILE_BY_CASE[case_id]
    )
    welcome_page.find_ssid.assert_called_once_with("existing-ssid")
    delegate.assert_not_called()


@pytest.mark.parametrize("found", (False, True))
def test_expand_networks_keeps_success_and_failure_behavior(
    welcome_page, tmp_path, capsys, found
) -> None:
    welcome_page.expand_all_and_confirm_more_ssids.return_value = found
    if found:
        navigation.run_welcome_expand_networks_case(Mock(), tmp_path, capsys)
        welcome_page.fail_with_artifacts.assert_not_called()
    else:
        with pytest.raises(AssertionError, match="page failure"):
            navigation.run_welcome_expand_networks_case(Mock(), tmp_path, capsys)
        assert "大屏列表滚动" in welcome_page.fail_with_artifacts.call_args.args[0]


@pytest.mark.parametrize("found", (False, True))
def test_hyperwifi_icon_requires_label_for_configured_ssid(
    welcome_page, network_entry, tmp_path, capsys, found
) -> None:
    welcome_page.find_hyperwifi_label.return_value = object() if found else None
    if found:
        wifi_icon.run_welcome_hyperwifi_icon_case({}, Mock(), tmp_path, capsys)
    else:
        with pytest.raises(AssertionError, match="page failure"):
            wifi_icon.run_welcome_hyperwifi_icon_case({}, Mock(), tmp_path, capsys)
    welcome_page.find_hyperwifi_label.assert_called_once_with(
        preferred_ssid=network_entry["ssid"]
    )


@pytest.mark.parametrize("value", ("1.2", "1.2.3", "1.2.3-beta"))
def test_version_runner_keeps_package_query_and_valid_version(capsys, value) -> None:
    shell = Mock(return_value=f"versionName={value}\n")

    version.run_welcome_version_case(shell, capsys)

    shell.assert_called_once_with("dumpsys package com.sunmi.welcome")


@pytest.mark.parametrize("output", ("", "versionName=unknown"))
def test_version_runner_rejects_missing_or_invalid_version(capsys, output) -> None:
    with pytest.raises(AssertionError, match="未安装或未查询到有效版本号"):
        version.run_welcome_version_case(Mock(return_value=output), capsys)
