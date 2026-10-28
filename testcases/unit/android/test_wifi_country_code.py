from unittest.mock import Mock, call, patch

import pytest

from core.libs.android.wifi_scenarios import country_code as country_code_cases
from core.libs.android.wifi_scenarios.country_code import force_country_and_restart_wifi
from core.libs.android.wifi_control.controller import WiFiControl
from core.testdata_loader import eu_country_codes, us_country_codes
from core.utils.adb_helper import AdbDeviceUnavailableError


def test_force_country_and_restart_wifi_preserves_command_and_restart_order() -> None:
    events = []
    wifi = Mock(spec=WiFiControl)
    wifi.set_wifi_enabled.side_effect = (
        lambda enabled: events.append(("wifi", enabled)) or True
    )

    def run_shell_cmd(command: str) -> str:
        events.append(("shell", command))
        if command == "cmd wifi get-country-code":
            return "Wifi Country Code = DE"
        return ""

    with patch("core.libs.android.wifi_scenarios.country_code.time.sleep") as sleep:
        force_country_and_restart_wifi(
            run_shell_cmd,
            wifi,
            country_code="DE",
            wait_after_enable=3.0,
        )

    assert events == [
        ("shell", "cmd wifi force-country-code enabled DE"),
        ("shell", "cmd wifi get-country-code"),
        ("wifi", False),
        ("wifi", True),
        ("shell", "cmd wifi get-country-code"),
    ]
    assert sleep.call_args_list == [call(1.0), call(3.0)]


def test_force_country_and_restart_wifi_waits_for_country_code() -> None:
    wifi = Mock(spec=WiFiControl)
    responses = iter([
        "Wifi Country Code = AE",
        "Wifi Country Code = DE",
        "Wifi Country Code = DE",
    ])

    # 只对查询命令发放预置响应，否则 force-country-code 会提前消耗掉未收敛的那一次。
    def run_shell_cmd(command: str) -> str:
        if command == "cmd wifi get-country-code":
            return next(responses)
        return ""

    with patch("core.libs.android.wifi_scenarios.country_code.time.sleep") as sleep:
        force_country_and_restart_wifi(
            run_shell_cmd,
            wifi,
            country_code="DE",
            wait_after_enable=0,
        )

    assert sleep.call_args_list == [call(1.0), call(1.0), call(0)]
    assert wifi.set_wifi_enabled.call_args_list == [call(False), call(True)]


def test_simulate_cloud_eus_uses_eu_country_and_disables_duty_cycle() -> None:
    responses = {
        "cmd wifi force-country-code-sunmi enabled EU": "OK",
        "cmd wifi get-country-code": "Wifi Country Code = EU",
        "cmd wifi set-eus 1": "OK",
        "cmd wifi get-eus": "get-eus: 1",
        "cli_app show duty": "Duty cycle : off",
    }
    run_shell_cmd = Mock(side_effect=lambda command: responses[command])

    country_code_cases.simulate_cloud_country_code(run_shell_cmd, "EUS")

    assert run_shell_cmd.call_args_list == [
        call("cmd wifi force-country-code-sunmi enabled EU"),
        call("cmd wifi get-country-code"),
        call("cmd wifi set-eus 1"),
        call("cmd wifi get-eus"),
        call("cli_app show duty"),
    ]


def test_simulate_cloud_country_rejects_invalid_command_response() -> None:
    def run_shell_cmd(command: str) -> str:
        if command.startswith("cmd wifi force-country-code-sunmi"):
            return "Invalid argument: Country code must be a 2-Character code"
        return "Wifi Country Code = EU"

    with pytest.raises(pytest.fail.Exception, match="设置远程配置国家码失败"):
        country_code_cases.simulate_cloud_country_code(run_shell_cmd, "EU")


def test_simulate_telephony_can_assert_cloud_country_keeps_priority() -> None:
    responses = {
        "cmd wifi force-telephony_country-code enabled EUS": "OK",
        "cmd wifi get-country-code": "Wifi Country Code = US",
    }
    run_shell_cmd = Mock(side_effect=lambda command: responses[command])

    country_code_cases.simulate_telephony_country_code(
        run_shell_cmd,
        "EUS",
        expected_country_code="US",
    )

    assert run_shell_cmd.call_args_list == [
        call("cmd wifi force-telephony_country-code enabled EUS"),
        call("cmd wifi get-country-code"),
    ]


def test_cloud_country_code_precedes_manual_shell_configuration() -> None:
    country_codes = iter(["Wifi Country Code = EU", "Wifi Country Code = US"])
    responses = {
        "cmd wifi force-country-code-sunmi enabled EU": "OK",
        "cmd wifi force-country-code enabled US": "OK",
        "cli_app show config | grep -i country": "Country code : EU",
        "cmd wifi set-eus 1": (
            "This device has been remotely configured, remote eus: -1"
        ),
    }
    run_shell_cmd = Mock(
        side_effect=lambda command: (
            next(country_codes)
            if command == "cmd wifi get-country-code"
            else responses[command]
        )
    )

    country_code_cases.assert_cloud_country_code_precedes_shell(run_shell_cmd)

    assert run_shell_cmd.call_args_list == [
        call("cmd wifi force-country-code-sunmi enabled EU"),
        call("cmd wifi get-country-code"),
        call("cmd wifi force-country-code enabled US"),
        call("cmd wifi get-country-code"),
        call("cli_app show config | grep -i country"),
        call("cmd wifi set-eus 1"),
    ]


def test_country_table_case_runs_shared_steps_in_order() -> None:
    wifi = Mock(spec=WiFiControl)
    run_shell_cmd = Mock()
    events = []

    with (
        patch.object(country_code_cases, "require_cli_app", side_effect=lambda _: events.append("require")),
        patch.object(country_code_cases, "force_country_and_restart_wifi", side_effect=lambda *args, **kwargs: events.append(("force", kwargs))),
        patch.object(country_code_cases, "assert_dual_wifi_connected", side_effect=lambda *args, **kwargs: events.append(("dual", kwargs))),
        patch.object(country_code_cases, "wait_for_wifi_ipv4", return_value=Mock(gateway="192.0.2.1")),
        patch.object(country_code_cases, "assert_gateway_reachable", side_effect=lambda *args: events.append("ping")),
        patch.object(country_code_cases, "assert_country_and_duty", side_effect=lambda *args, **kwargs: events.append(("assert", kwargs))),
    ):
        country_code_cases.run_country_table_case(
            " de ",
            run_shell_cmd,
            wifi,
            {},
            capability="dualwifi",
            expected_halow=" eu ",
        )

    assert events == [
        "require",
        ("force", {"country_code": "DE", "wait_after_enable": 0.0}),
        ("dual", {"hyper_region": "EU"}),
        "ping",
        ("assert", {"country_code": "DE", "expected_halow": "EU"}),
    ]


def test_country_table_case_uses_wifi_without_halow_cli() -> None:
    wifi = Mock(spec=WiFiControl)
    run_shell_cmd = Mock()
    entry = {"id": "wifi_ap_ssid_default", "ssid": "Lab_HW_AutoTest"}
    ipv4 = Mock(gateway="192.0.2.1")

    with (
        patch.object(country_code_cases, "require_cli_app") as require_cli,
        patch.object(country_code_cases, "force_country_and_restart_wifi") as force,
        patch.object(country_code_cases, "get_wifi_list_entry", return_value=entry) as get_entry,
        patch.object(country_code_cases, "assert_wifi_connected") as connect,
        patch.object(country_code_cases, "wait_for_wifi_ipv4", return_value=ipv4),
        patch.object(country_code_cases, "assert_gateway_reachable") as ping,
        patch.object(country_code_cases, "_wait_for_wifi_country_code") as wait_country,
        patch.object(country_code_cases, "assert_dual_wifi_connected") as connect_dual,
        patch.object(country_code_cases, "assert_country_and_duty") as assert_halow,
    ):
        country_code_cases.run_country_table_case(
            " de ",
            run_shell_cmd,
            wifi,
            {},
            capability="wifi",
            expected_halow=" eu ",
        )

    require_cli.assert_not_called()
    force.assert_called_once_with(
        run_shell_cmd, wifi, country_code="DE", wait_after_enable=0.0
    )
    get_entry.assert_called_once_with({}, entry_id="wifi_ap_ssid_default")
    connect.assert_called_once_with(
        wifi,
        {},
        run_shell_cmd,
        entry=entry,
        allow_any_configured=False,
    )
    ping.assert_called_once_with(run_shell_cmd, ipv4.gateway)
    wait_country.assert_called_once_with(run_shell_cmd, expected="DE", timeout=20.0)
    connect_dual.assert_not_called()
    assert_halow.assert_not_called()


def test_country_table_case_uses_region_hyperwifi_without_dual_link() -> None:
    wifi = Mock(spec=WiFiControl)
    run_shell_cmd = Mock()
    entry = {"id": "hyperwifi_eu", "ssid": "HyperWi-Fi_EU"}
    ipv4 = Mock(gateway="192.0.2.1")

    with (
        patch.object(country_code_cases, "require_cli_app") as require_cli,
        patch.object(country_code_cases, "force_country_and_restart_wifi"),
        patch.object(country_code_cases, "get_wifi_list_entry", return_value=entry) as get_entry,
        patch.object(country_code_cases, "assert_wifi_connected") as connect,
        patch.object(country_code_cases, "wait_for_wifi_ipv4", return_value=ipv4),
        patch.object(country_code_cases, "assert_gateway_reachable") as ping,
        patch.object(country_code_cases, "assert_dual_wifi_connected") as connect_dual,
        patch.object(country_code_cases, "assert_country_and_duty") as assert_halow,
    ):
        country_code_cases.run_country_table_case(
            " de ",
            run_shell_cmd,
            wifi,
            {},
            capability="hyperwifi",
            expected_halow=" eu ",
        )

    require_cli.assert_called_once_with(run_shell_cmd)
    get_entry.assert_called_once_with({}, entry_id="hyperwifi_eu")
    connect.assert_called_once_with(
        wifi,
        {},
        run_shell_cmd,
        entry=entry,
        allow_any_configured=False,
    )
    ping.assert_called_once_with(run_shell_cmd, ipv4.gateway)
    connect_dual.assert_not_called()
    assert_halow.assert_called_once_with(
        run_shell_cmd, country_code="DE", expected_halow="EU"
    )


def test_country_stress_continues_after_one_cycle_failure() -> None:
    wifi = Mock(spec=WiFiControl)
    wifi.adb = Mock()
    run_shell_cmd = Mock()

    with (
        patch.object(country_code_cases, "require_cli_app"),
        patch.object(
            country_code_cases,
            "force_country_and_restart_wifi",
            side_effect=[RuntimeError("first cycle failed"), None],
        ),
        patch.object(country_code_cases, "assert_country_and_duty"),
        patch.object(country_code_cases, "assert_dual_wifi_connected"),
        patch.object(country_code_cases, "export_device_packlogs") as export_logs,
    ):
        result = country_code_cases.run_country_code_switch_stress(
            run_shell_cmd, wifi, {}, cycles=2, wait_after_enable=0
        )

    assert result.passed_cycles == 1
    assert result.failed_cycles == 1
    assert "first cycle failed" in result.failures[0]
    export_logs.assert_called_once()


def test_country_stress_aborts_without_counting_or_exporting_unavailable_cycle() -> None:
    wifi = Mock(spec=WiFiControl)
    wifi.adb = Mock()
    run_shell_cmd = Mock()

    with (
        patch.object(country_code_cases, "require_cli_app"),
        patch.object(
            country_code_cases,
            "force_country_and_restart_wifi",
            side_effect=[None, AdbDeviceUnavailableError("device offline"), None],
        ) as force_country,
        patch.object(country_code_cases, "assert_country_and_duty"),
        patch.object(country_code_cases, "assert_dual_wifi_connected"),
        patch.object(country_code_cases, "export_device_packlogs") as export_logs,
    ):
        with pytest.raises(AdbDeviceUnavailableError) as error:
            country_code_cases.run_country_code_switch_stress(
                run_shell_cmd, wifi, {}, cycles=3, wait_after_enable=0
            )

    assert "总轮次=3, 成功=1, 失败=0" in str(error.value)
    assert error.value.statistics == "总轮次=3, 成功=1, 失败=0, 失败详情=无"
    assert force_country.call_count == 2
    export_logs.assert_not_called()


def test_country_tables_keep_legacy_case_id_anchors() -> None:
    """国家码表顺序即原手工用例编号，改表会让 Func_Ccode_Adapt_Vali_* 追溯错位。"""
    eu = eu_country_codes()
    us = us_country_codes()

    assert len(eu) == 49, "EU 表数量变化会移位 Func_Ccode_Adapt_Vali_001~049"
    assert len(us) == 198, "US 表数量变化会移位 Func_Ccode_Adapt_Vali_050~247"
    assert "NO" in eu, "挪威易被 YAML 1.1 解析成布尔而丢失，需保持带引号"

    for case_no, code in ((1, "AD"), (17, "GB"), (37, "NO"), (49, "VA")):
        assert eu[case_no - 1] == code
    for case_no, code in ((50, "AE"), (247, "ZW")):
        assert us[case_no - 50] == code