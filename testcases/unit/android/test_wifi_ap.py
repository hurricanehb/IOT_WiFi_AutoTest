from contextlib import contextmanager
from types import SimpleNamespace
from typing import cast
from unittest.mock import Mock

import pytest

from core.libs.access_points import WiFiAPAction
from core.libs.android.wifi_scenarios import ap_configuration as wifi_ap_cases
from core.libs.android.wifi_scenarios import ap_configuration as wifi_ap_scenarios
from core.libs.android.wifi_scenarios import channel_plan as wifi_channel_scenarios
from core.libs.android.wifi_scenarios import status_capture as scenario_status_capture
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_scenarios.ssidpwd_connection import assert_ssid_visible_in_scan
from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.config_loader import Settings
from core.utils.telnet_helper import TelnetClient


class _RecordingClient:
    def __init__(self, *args, **kwargs) -> None:
        self.connected = False
        self.encoding = "utf-8"
        self.errors = "replace"
        self.commands = []

    def connect(self) -> None:
        self.connected = True

    def close(self) -> None:
        self.connected = False

    def write_line(self, command: str) -> None:
        self.commands.append(command)

    def read_until(self, pattern, timeout_sec=None) -> bytes:
        return pattern if isinstance(pattern, bytes) else pattern.encode()

    def read_until_any(self, patterns, timeout_sec=None) -> bytes:
        if tuple(patterns) == ("[Y/N]", "(y/n)[n]:"):
            return b""
        pattern = patterns[0]
        return pattern if isinstance(pattern, bytes) else pattern.encode()


class _SimplePasswordWarningClient(_RecordingClient):
    def read_until_any(self, patterns, timeout_sec=None) -> bytes:
        if self.commands[-1].startswith("security wpa2 psk"):
            return b"Warning: password is too simple. continue?[Y/N]:"
        return super().read_until_any(patterns, timeout_sec)


class _SaveConfirmationClient(_RecordingClient):
    def read_until_any(self, patterns, timeout_sec=None) -> bytes:
        if self.commands[-1] == "save":
            return b"Continue? (y/n)[n]:"
        return super().read_until_any(patterns, timeout_sec)


class _DelayedConfirmationClient(_RecordingClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.confirmation_pending = False

    def read_until_any(self, patterns, timeout_sec=None) -> bytes:
        if self.commands[-1].startswith("ssid ") and len(patterns) > 2:
            self.confirmation_pending = True
            return patterns[0].encode()
        if self.confirmation_pending and tuple(patterns) == ("[Y/N]", "(y/n)[n]:"):
            self.confirmation_pending = False
            return b"Warning: This action may cause service interruption. Continue?[Y/N]"
        return super().read_until_any(patterns, timeout_sec)


def _action():
    client = _RecordingClient()
    settings = SimpleNamespace(
        ap_config=SimpleNamespace(
            ap_ip="192.0.2.1",
            ap_login_username="test",
            ap_login_password="secret",
            ap_flag="<AirEngine9700S-S-2024>",
            ap_id=1,
            vap_profile="PyAutoTest",
            service_vlan=3,
            wlan_id=8,
        )
    )
    action = WiFiAPAction(
        settings=cast(Settings, settings),
        client_factory=lambda *args, **kwargs: cast(TelnetClient, client),
    )
    return action, client


def test_set_2g_channel_uses_ap_radio_view() -> None:
    action, client = _action()

    action.set_channel("2g", 13, ap_id=1)

    assert client.commands == [
        "test",
        "secret",
        "screen-length 0 temporary",
        "system-view",
        "wlan",
        "ap-id 1",
        "radio 0",
        "calibrate auto-channel-select disable",
        "calibrate auto-bandwidth-select disable",
        "channel 20mhz 13",
        "Y",
        "return",
    ]


def test_save_configuration_uses_user_view() -> None:
    action, client = _action()

    action.save_configuration()

    assert client.commands[-1] == "save"


def test_save_configuration_confirms_lowercase_prompt() -> None:
    action, _ = _action()
    client = _SaveConfirmationClient()
    action._client_factory = lambda *args, **kwargs: cast(TelnetClient, client)

    action.save_configuration()

    assert client.commands[-2:] == ["save", "Y"]


def test_set_security_builds_verified_wpa2_pmf_commands() -> None:
    action, client = _action()

    action.set_security(
        "PyAutoTest-Security",
        "wpa2-aes-pmf-mandatory",
        password="24681357",
    )

    assert "security wpa2 psk pass-phrase 24681357 aes" in client.commands
    assert "pmf mandatory" in client.commands


def test_set_security_clears_pmf_before_switching_to_open() -> None:
    action, client = _action()

    action.set_security("PyAutoTest-Security", "open")

    assert client.commands.index("undo pmf") < client.commands.index("security open")


def test_manual_add_security_case_configures_ap_then_uses_ui_runner() -> None:
    action = SimpleNamespace(configure_wifi=Mock())
    add_network_ui = cast(WiFiAddNetworkUI, SimpleNamespace())
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    original_add = wifi_ap_scenarios.run_add_network_connection_case
    calls = []
    wifi_ap_scenarios.assert_ssid_visible_in_scan = lambda *args, **kwargs: None
    wifi_ap_scenarios.run_add_network_connection_case = (
        lambda *args, **kwargs: calls.append((args, kwargs))
    )
    try:
        wifi_ap_scenarios.run_wifi_ap_manual_add_security_case(
            {"case_id": "Func_Manual_Vali_018"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            add_network_ui,
            action,
            security="wpa-aes",
            ui_security="personal",
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan
        wifi_ap_scenarios.run_add_network_connection_case = original_add

    action.configure_wifi.assert_called_once_with(
        ssid="PyAutoTest_018_wpaaes",
        password="24681357",
        security="wpa-aes",
        band="5g",
        hidden=False,
        verify=True,
    )
    assert calls[0][1]["security"] == "personal"
    assert calls[0][1]["expect_connected"] is True


@pytest.mark.parametrize(
    ("security", "pmf_command"),
    [
        ("wpa-wpa2-aes", "undo pmf"),
        ("wpa-wpa2-aes-pmf-optional", "pmf optional"),
        ("wpa-wpa2-aes-pmf-mandatory", "pmf mandatory"),
    ],
)
def test_set_security_builds_wpa_wpa2_pmf_commands(
    security: str, pmf_command: str
) -> None:
    action, client = _action()

    action.set_security("PyAutoTest-Security", security, password="24681357")

    assert "security wpa-wpa2 psk pass-phrase 24681357 aes" in client.commands
    assert pmf_command in client.commands


def test_set_security_confirms_simple_password_warning() -> None:
    action, _ = _action()
    client = _SimplePasswordWarningClient()
    action._client_factory = lambda *args, **kwargs: cast(TelnetClient, client)

    action.set_security("PyAutoTest-Security", "wpa2-aes", password="24681357")

    security_index = client.commands.index(
        "security wpa2 psk pass-phrase 24681357 aes"
    )
    assert client.commands[security_index + 1] == "Y"


def test_set_security_enhanced_open_requires_mandatory_pmf() -> None:
    action, client = _action()

    action.set_security("PyAutoTest-Security", "enhanced-open")

    assert "security enhanced-open aes" in client.commands
    assert "pmf mandatory" in client.commands
    assert "undo pmf" not in client.commands


def test_set_channel_rejects_unsupported_device_channel() -> None:
    action, client = _action()

    with pytest.raises(ValueError, match="不支持信道 100"):
        action.set_channel("5g", 100)

    assert client.commands == []


def test_profile_name_rejects_command_injection() -> None:
    action, client = _action()

    with pytest.raises(ValueError):
        action.set_ssid("test\nreturn", "ssid")

    assert client.commands == []


def test_visible_ssid_clears_previous_hidden_state() -> None:
    action, client = _action()

    action.set_ssid("PyAutoTest-SSID", "PyAutoTest_Live")

    assert "ssid PyAutoTest_Live" in client.commands
    assert "undo ssid-hide enable" in client.commands


def test_set_ssid_confirms_warning_arriving_after_prompt() -> None:
    action, _ = _action()
    client = _DelayedConfirmationClient()
    action._client_factory = lambda *args, **kwargs: cast(TelnetClient, client)

    action.set_ssid("PyAutoTest-SSID", "special-ssid")

    ssid_index = client.commands.index("ssid special-ssid")
    assert client.commands[ssid_index + 1] == "Y"
    assert client.commands[ssid_index + 2] == "undo ssid-hide enable"
    assert client.commands.count("Y") == 1


def test_hidden_ssid_uses_enable_keyword() -> None:
    action, client = _action()

    action.set_ssid("PyAutoTest-SSID", "PyAutoTest_Hidden", hidden=True)

    assert "ssid-hide enable" in client.commands
    assert "undo ssid-hide enable" not in client.commands


def test_bind_vap_can_enable_tunnel_forwarding() -> None:
    action, client = _action()

    action.bind_vap(
        "Lab_HW_AutoTest",
        ssid_profile="Lab_HW_AutoTest-SSID",
        security_profile="Lab_HW_AutoTest-Security",
        service_vlan=2,
        forward_mode="tunnel",
    )

    assert "forward-mode tunnel" in client.commands
    assert "service-vlan vlan-id 2" in client.commands


@pytest.mark.parametrize(
    ("security", "expected"),
    [
        ("wpa-tkip", "security wpa psk pass-phrase 24681357 tkip"),
        ("wpa-aes-tkip", "security wpa psk pass-phrase 24681357 aes-tkip"),
        ("wpa2-tkip", "security wpa2 psk pass-phrase 24681357 tkip"),
        ("wpa2-aes-tkip", "security wpa2 psk pass-phrase 24681357 aes-tkip"),
    ],
)
def test_set_security_builds_tkip_cipher_commands(
    security: str, expected: str
) -> None:
    action, client = _action()

    action.set_security("PyAutoTest-Security", security, password="24681357")

    assert expected in client.commands


def test_configure_wifi_binds_profile_to_target_radio() -> None:
    action, client = _action()

    action.configure_wifi(
        ssid="PyAutoTest_2G",
        password="24681357",
        security="wpa2-aes",
        band="2g",
    )

    assert "ssid PyAutoTest_2G" in client.commands
    assert "security wpa2 psk pass-phrase 24681357 aes" in client.commands
    assert "undo vap-profile PyAutoTest wlan 8" in client.commands
    assert "vap-profile PyAutoTest wlan 8" in client.commands


def test_assert_dut_channel_retries_until_target_frequency() -> None:
    statuses = iter(
        [
            "Frequency: 5200MHz",
            "Frequency: 5200MHz",
            "Frequency: 5220MHz",
        ]
    )
    wifi_channel_scenarios.assert_dut_channel(
        lambda command: next(statuses),
        band="5g",
        channel=44,
        summary="channel-switch",
        attempts=3,
        interval_sec=0,
    )


def test_assert_wifi_connected_accepts_current_ssid_when_match_source_lags() -> None:
    wifi = SimpleNamespace(
        set_wifi_enabled=lambda enabled: True,
        list_connected_ssids=lambda **kwargs: ["Lab_5G"],
        ensure_wifi_connected=lambda entry: True,
        match_associated_ssids=lambda *args, **kwargs: ([], []),
    )

    connected = assert_wifi_connected(
        cast(WiFiControl, wifi),
        {"wifi_list": [{"ssid": "Lab_5G", "encrypt": "WPA2"}]},
        lambda command: 'Wifi is connected to "Lab_5G"',
        entry={"ssid": "Lab_5G", "encrypt": "WPA2"},
    )

    assert connected == "Lab_5G"


def test_channel_helper_does_not_require_hyperwifi_cli_for_ap(monkeypatch) -> None:
    class RecordingAction:
        def current_channel(self, band, **kwargs) -> int:
            return 6

        def configure_wifi(self, **kwargs) -> None:
            pass

        def set_channel(self, band, channel, **kwargs) -> None:
            pass

    require_cli_app = Mock(side_effect=AssertionError("不应检查 HyperWiFi cli_app"))
    force_country = Mock(side_effect=AssertionError("不应设置 HyperWiFi 国家码"))
    monkeypatch.setattr(wifi_channel_scenarios, "require_cli_app", require_cli_app)
    monkeypatch.setattr(
        wifi_channel_scenarios,
        "force_country_and_restart_wifi",
        force_country,
    )
    monkeypatch.setattr(
        wifi_channel_scenarios,
        "assert_wifi_connected",
        lambda *args, **kwargs: None,
    )

    wifi_channel_scenarios.run_channel_automation_case(
        {"case_id": "jp-channels", "title": "2.4G", "tag": "WiFi"},
        lambda command: "Frequency: 2412MHz",
        cast(WiFiControl, SimpleNamespace(disconnect_all=lambda: True)),
        {
            "wifi_list": [
                {
                    "ssid": "Lab_2.4G",
                    "pwd": "24681357",
                    "encrypt": "WPA2",
                    "type": "normal",
                }
            ]
        },
        plan={
            "driver": "ap",
            "band": "2g",
            "country": "JP",
            "channels": [1],
            "settle_sec": 0,
        },
        wifi_ap_action=RecordingAction(),
    )

    require_cli_app.assert_not_called()
    force_country.assert_not_called()


def test_dfs_channel_uses_cac_settle_time() -> None:
    assert wifi_channel_scenarios.channel_settle_sec("5g", 52, 5.0) == 65.0
    assert wifi_channel_scenarios.channel_settle_sec("5g", 149, 5.0) == 5.0
    assert wifi_channel_scenarios.channel_settle_sec("2g", 12, 5.0) == 5.0


def test_vap_online_requires_matching_ap_radio_status_and_ssid() -> None:
    output = """
2     AP2      0    8    54F6-E2E9-4AE7 ON      WPA2-PSK  0  Other
2     AP2      1    8    54F6-E2E9-4AF7 ON      WPA2-PSK  0  0
"""

    assert WiFiAPAction._vap_is_online(output, ap_id=2, radio=1, ssid="0")
    assert not WiFiAPAction._vap_is_online(output, ap_id=2, radio=0, ssid="0")


def test_channel_helper_drives_ap_and_checks_each_channel() -> None:
    class RecordingAction:
        def __init__(self) -> None:
            self.profile = None
            self.channels = []

        def current_channel(self, band, **kwargs) -> int:
            return 6

        def configure_wifi(self, **kwargs) -> None:
            self.profile = kwargs

        def set_channel(self, band, channel, **kwargs) -> None:
            self.channels.append((band, channel, kwargs))

    action = RecordingAction()
    disconnects = []
    checks = []
    original_assert = wifi_channel_scenarios.assert_wifi_connected
    wifi_channel_scenarios.assert_wifi_connected = lambda *args, **kwargs: checks.append(kwargs)
    try:
        frequencies = iter((2412, 2412, 2437, 2462))
        wifi_channel_scenarios.run_channel_automation_case(
            {"case_id": "channel-test", "title": "2.4G", "tag": "WiFi"},
            lambda command: f"Frequency: {next(frequencies)}MHz",
            cast(
                WiFiControl,
                SimpleNamespace(disconnect_all=lambda: disconnects.append(None) or True),
            ),
            {
                "wifi_list": [
                    {
                        "ssid": "Lab_2.4G",
                        "pwd": "24681357",
                        "encrypt": "WPA2",
                        "type": "normal",
                    }
                ]
            },
            plan={
                "driver": "ap",
                "band": "2g",
                "configured_ssid": "PyAutoTest_Channel",
                "ap_id": 1,
                "bandwidth_mhz": 20,
                "channels": [1, 6, 11],
                "settle_sec": 0,
            },
            wifi_ap_action=action,
        )
    finally:
        wifi_channel_scenarios.assert_wifi_connected = original_assert

    assert action.profile == {
        "ssid": "PyAutoTest_Channel",
        "password": "24681357",
        "security": "wpa2-aes",
        "band": "2g",
    }
    assert [item[1] for item in action.channels] == [1, 6, 11, 6]
    assert len(disconnects) == 3
    assert len(checks) == 3
    assert all(check["entry"]["ssid"] == "PyAutoTest_Channel" for check in checks)


def test_channel_helper_restores_ap_channel_after_failure(monkeypatch) -> None:
    class RecordingAction:
        def __init__(self) -> None:
            self.channels = []

        def current_channel(self, band, **kwargs) -> int:
            return 6

        def configure_wifi(self, **kwargs) -> None:
            pass

        def set_channel(self, band, channel, **kwargs) -> None:
            self.channels.append(channel)

    action = RecordingAction()
    monkeypatch.setattr(
        wifi_channel_scenarios,
        "assert_dut_channel",
        Mock(side_effect=RuntimeError("DUT association failed")),
    )
    monkeypatch.setattr(
        wifi_channel_scenarios,
        "assert_wifi_connected",
        Mock(return_value="Lab_2.4G"),
    )

    with pytest.raises(RuntimeError, match="DUT association failed"):
        wifi_channel_scenarios.run_channel_automation_case(
            {"case_id": "channel-failure", "title": "2.4G", "tag": "WiFi"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace(disconnect_all=lambda: True)),
            {
                "wifi_list": [
                    {
                        "ssid": "Lab_2.4G",
                        "pwd": "24681357",
                        "encrypt": "WPA2",
                        "type": "normal",
                    }
                ]
            },
            plan={
                "driver": "ap",
                "band": "2g",
                "channels": [1, 6, 11],
                "settle_sec": 0,
            },
            wifi_ap_action=action,
        )

    assert action.channels == [1, 6]


def test_channel_helper_can_reuse_existing_wifi_profile() -> None:
    class RecordingAction:
        def __init__(self) -> None:
            self.configured = False
            self.channels = []

        def current_channel(self, band, **kwargs) -> int:
            return 149

        def configure_wifi(self, **kwargs) -> None:
            self.configured = True

        def set_channel(self, band, channel, **kwargs) -> None:
            self.channels.append(channel)

    action = RecordingAction()
    original_assert = wifi_channel_scenarios.assert_wifi_connected
    wifi_channel_scenarios.assert_wifi_connected = lambda *args, **kwargs: None
    try:
        wifi_channel_scenarios.run_channel_automation_case(
            {"case_id": "existing-profile", "title": "5G", "tag": "WiFi"},
            lambda command: "Frequency: 5180MHz",
            cast(WiFiControl, SimpleNamespace(disconnect_all=lambda: True)),
            {
                "wifi_list": [
                    {
                        "ssid": "Lab_5G",
                        "pwd": "24681357",
                        "encrypt": "WPA2",
                    }
                ]
            },
            plan={
                "driver": "ap",
                "band": "5g",
                "channels": [36],
                "configure_wifi": False,
                "wifi_entry_ssid": "Lab_5G",
                "settle_sec": 0,
            },
            wifi_ap_action=action,
        )
    finally:
        wifi_channel_scenarios.assert_wifi_connected = original_assert

    assert action.configured is False
    assert action.channels == [36, 149]


def test_security_case_configures_ap_and_connects_dut(monkeypatch) -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    step_titles = []
    attachments = []
    commands = []
    scans = []
    connects = []
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    original_connect = wifi_ap_scenarios.assert_wifi_connected
    original_ping = wifi_ap_scenarios.assert_gateway_ping
    wifi_ap_scenarios.assert_ssid_visible_in_scan = (
        lambda command, ssid, summary: scans.append(ssid)
    )
    wifi_ap_scenarios.assert_wifi_connected = (
        lambda *args, **kwargs: connects.append(kwargs["entry"]) or kwargs["entry"]["ssid"]
    )
    wifi_ap_scenarios.assert_gateway_ping = lambda *args, **kwargs: None

    @contextmanager
    def record_step(title):
        step_titles.append(title)
        yield

    monkeypatch.setattr(wifi_ap_scenarios.allure, "step", record_step)
    monkeypatch.setattr(scenario_status_capture.allure, "step", record_step)
    monkeypatch.setattr(
        scenario_status_capture.allure,
        "attach",
        lambda body, **kwargs: attachments.append((body, kwargs)),
    )
    try:
        wifi_ap_scenarios.run_wifi_ap_security_case(
            {"case_id": "Func_Encrypt_Vali_007"},
            lambda command: commands.append(command) or "Wi-Fi is enabled",
            cast(WiFiControl, SimpleNamespace()),
            {},
            action,
            security="wpa2-aes-pmf-mandatory",
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan
        wifi_ap_scenarios.assert_wifi_connected = original_connect
        wifi_ap_scenarios.assert_gateway_ping = original_ping

    assert commands == ["cmd wifi status"]
    assert step_titles == [
        "检查 DUT WiFi 初始状态",
        "配置 AP：wpa2-aes-pmf-mandatory，频段：5g",
        f"扫描并确认目标 SSID：{configured[0]['ssid']}",
        f"连接目标网络：{configured[0]['ssid']}",
        "验证网关连通性",
    ]
    assert attachments == [
        (
            "Wi-Fi is enabled",
            {
                "name": "Func_Encrypt_Vali_007 - cmd wifi status",
                "attachment_type": scenario_status_capture.allure.attachment_type.TEXT,
            },
        )
    ]
    assert configured[0]["security"] == "wpa2-aes-pmf-mandatory"
    assert scans == [configured[0]["ssid"]]
    assert connects[0]["encrypt"] == "WPA2"


def test_preconfigured_security_case_connects_without_ap_configuration() -> None:
    connects = []
    pings = []
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    original_connect = wifi_ap_scenarios.assert_wifi_connected
    original_ping = wifi_ap_scenarios.assert_gateway_ping
    wifi_ap_scenarios.assert_ssid_visible_in_scan = lambda *args, **kwargs: None
    wifi_ap_scenarios.assert_wifi_connected = (
        lambda *args, **kwargs: connects.append(kwargs["entry"]) or kwargs["entry"]["ssid"]
    )
    wifi_ap_scenarios.assert_gateway_ping = (
        lambda *args, **kwargs: pings.append(kwargs["summary"])
    )

    def run_shell_cmd(command: str) -> str:
        if command == "cmd wifi list-scan-results":
            return "00:11:22:33:44:55 5180 -42 0 Lab_WPA2 [WPA2-PSK-CCMP][MFPR][ESS]"
        return ""

    try:
        connected = wifi_ap_scenarios.run_preconfigured_wifi_security_case(
            {"case_id": "Func_Encrypt_Vali_007"},
            run_shell_cmd,
            cast(WiFiControl, SimpleNamespace()),
            {
                "wifi_list": [
                    {
                        "id": "encrypt_wpa2_pmf",
                        "ssid": "Lab_WPA2",
                        "pwd": "24681357",
                        "encrypt": "WPA2",
                    }
                ]
            },
            entry_id="encrypt_wpa2_pmf",
            expected_capabilities=("WPA2-PSK-CCMP", "MFPR"),
        )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan
        wifi_ap_scenarios.assert_wifi_connected = original_connect
        wifi_ap_scenarios.assert_gateway_ping = original_ping

    assert connected == "Lab_WPA2"
    assert connects[0]["id"] == "encrypt_wpa2_pmf"
    assert pings == ["Func_Encrypt_Vali_007"]


def test_preconfigured_security_case_rejects_wrong_capability() -> None:
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    wifi_ap_scenarios.assert_ssid_visible_in_scan = lambda *args, **kwargs: None
    try:
        with pytest.raises(pytest.fail.Exception, match="未广播预期安全能力"):
            wifi_ap_scenarios.run_preconfigured_wifi_security_case(
                {"case_id": "Func_Encrypt_Vali_006"},
                lambda command: (
                    "00:11:22:33:44:55 2412 -42 0 Lab_TKIP [WPA2-PSK-CCMP][ESS]"
                ),
                cast(WiFiControl, SimpleNamespace()),
                {
                    "wifi_list": [
                        {
                            "id": "encrypt_wpa2_tkip",
                            "ssid": "Lab_TKIP",
                            "pwd": "24681357",
                            "encrypt": "WPA2",
                        }
                    ]
                },
                entry_id="encrypt_wpa2_tkip",
                expected_capabilities=("TKIP",),
                ping_gateway=False,
            )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan


def test_preconfigured_security_case_skips_when_password_env_is_missing(
    monkeypatch,
) -> None:
    monkeypatch.delenv("WIFI_TEST_PASSWORD", raising=False)

    with pytest.raises(pytest.skip.Exception, match="WIFI_TEST_PASSWORD"):
        wifi_ap_scenarios.run_preconfigured_wifi_security_case(
            {"case_id": "Func_Encrypt_Vali_001"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {
                "wifi_list": [
                    {
                        "id": "encrypt_wep",
                        "ssid": "Lab_WEP",
                        "password_env": "WIFI_TEST_PASSWORD",
                        "encrypt": "WEP",
                    }
                ]
            },
            entry_id="encrypt_wep",
            expected_capabilities=("WEP",),
        )


def test_preconfigured_security_case_requires_declared_lab_flag(monkeypatch) -> None:
    monkeypatch.delenv("OWE_TRANSITION_LAB", raising=False)

    with pytest.raises(pytest.skip.Exception, match="OWE_TRANSITION_LAB"):
        wifi_ap_scenarios.run_preconfigured_wifi_security_case(
            {"case_id": "Func_Encrypt_Vali_054"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {
                "wifi_list": [
                    {
                        "id": "owe_transition",
                        "ssid": "Lab_OWE",
                        "lab_flag": "OWE_TRANSITION_LAB",
                        "encrypt": "OWE",
                    }
                ]
            },
            entry_id="owe_transition",
            expected_capabilities=("OWE",),
        )


def test_ssid_case_uses_yaml_profile() -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    original_connect = wifi_ap_scenarios.assert_wifi_connected
    original_ping = wifi_ap_scenarios.assert_gateway_ping
    wifi_ap_scenarios.assert_ssid_visible_in_scan = lambda *args, **kwargs: None
    wifi_ap_scenarios.assert_wifi_connected = (
        lambda *args, **kwargs: kwargs["entry"]["ssid"]
    )
    wifi_ap_scenarios.assert_gateway_ping = lambda *args, **kwargs: None
    try:
        wifi_ap_scenarios.run_wifi_ap_ssid_case(
            {"case_id": "Func_SsidPwd_Vali_001"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {
                "ssid_pwd_defaults": {"security": "WPA2"},
                "ssid_pwd_profiles": {
                    "ssid_numeric_min": {"ssid": "0", "password": "24681357"}
                },
            },
            action,
            entry_id="ssid_numeric_min",
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan
        wifi_ap_scenarios.assert_wifi_connected = original_connect
        wifi_ap_scenarios.assert_gateway_ping = original_ping

    assert configured == [
        {
            "ssid": "0",
            "password": "24681357",
            "security": "wpa2-aes",
            "band": "5g",
            "ssid_encoding": "utf-8",
            "verify": True,
        }
    ]


def test_ssid_case_forwards_non_utf8_encoding() -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    original_scan = wifi_ap_scenarios.assert_ssid_visible_in_scan
    original_connect = wifi_ap_scenarios.assert_wifi_connected
    original_ping = wifi_ap_scenarios.assert_gateway_ping
    wifi_ap_scenarios.assert_ssid_visible_in_scan = lambda *args, **kwargs: None
    wifi_ap_scenarios.assert_wifi_connected = lambda *args, **kwargs: "哈"
    wifi_ap_scenarios.assert_gateway_ping = lambda *args, **kwargs: None
    try:
        wifi_ap_scenarios.run_wifi_ap_ssid_case(
            {"case_id": "gbk-ssid"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {
                "ssid_pwd_profiles": {
                    "gbk": {
                        "ssid": "哈",
                        "password": "24681357",
                        "ssid_encoding": "gbk",
                    }
                }
            },
            action,
            entry_id="gbk",
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios.assert_ssid_visible_in_scan = original_scan
        wifi_ap_scenarios.assert_wifi_connected = original_connect
        wifi_ap_scenarios.assert_gateway_ping = original_ping

    assert configured[0]["ssid_encoding"] == "gbk"


def test_ssid_scan_retries_until_target_is_visible() -> None:
    scans = iter(
        [
            "OtherNetwork",
            "StillOther",
            "  54:f6:e2:e9:4a:f7 5180 -27(0:-27) 6.600 0 [WPA2-PSK][ESS]",
        ]
    )
    commands = []

    def run_shell_cmd(command: str) -> str:
        commands.append(command)
        return next(scans) if command == "cmd wifi list-scan-results" else ""

    assert_ssid_visible_in_scan(
        run_shell_cmd,
        "0",
        summary="delayed-ssid",
        attempts=3,
        scan_wait_sec=0,
    )

    assert commands == [
        "cmd wifi start-scan",
        "cmd wifi list-scan-results",
    ] * 3


def test_ssid_scan_fails_after_all_attempts() -> None:
    commands = []

    def run_shell_cmd(command: str) -> str:
        commands.append(command)
        return "OtherNetwork"

    with pytest.raises(pytest.fail.Exception, match="连续扫描 2 次未找到"):
        assert_ssid_visible_in_scan(
            run_shell_cmd,
            "0",
            summary="missing-ssid",
            attempts=2,
            scan_wait_sec=0,
        )

    assert commands.count("cmd wifi start-scan") == 2


def test_security_change_case_applies_transitions_and_restores_initial() -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    reconnects = []
    original_connect = wifi_ap_scenarios._configure_and_connect
    original_reconnect = wifi_ap_scenarios._assert_auto_reconnected
    try:
        wifi_ap_scenarios._configure_and_connect = lambda *args, **kwargs: None
        wifi_ap_scenarios._assert_auto_reconnected = (
            lambda wifi, ssid, **kwargs: reconnects.append(ssid)
        )
        wifi_ap_scenarios.run_wifi_ap_security_change_case(
            {"case_id": "security-change"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            action,
            initial_security="wpa2-aes-pmf-mandatory",
            transitions=[
                ("wpa3-aes", True),
                ("wpa2-wpa3-aes-pmf-mandatory", True),
            ],
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios._configure_and_connect = original_connect
        wifi_ap_scenarios._assert_auto_reconnected = original_reconnect

    assert [item["security"] for item in configured] == [
        "wpa3-aes",
        "wpa2-wpa3-aes-pmf-mandatory",
        "wpa2-aes-pmf-mandatory",
    ]
    assert len(reconnects) == 2


def test_password_change_case_checks_failure_then_recovery() -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    disconnected = []
    reconnected = []
    original_connect = wifi_ap_scenarios._configure_and_connect
    original_disconnect = wifi_ap_scenarios._assert_stays_disconnected
    original_reconnect = wifi_ap_scenarios._assert_auto_reconnected
    try:
        wifi_ap_scenarios._configure_and_connect = lambda *args, **kwargs: None
        wifi_ap_scenarios._assert_stays_disconnected = (
            lambda wifi, ssid, **kwargs: disconnected.append(ssid)
        )
        wifi_ap_scenarios._assert_auto_reconnected = (
            lambda wifi, ssid, **kwargs: reconnected.append(ssid)
        )
        wifi_ap_scenarios.run_wifi_ap_password_change_case(
            {"case_id": "password-change"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            action,
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios._configure_and_connect = original_connect
        wifi_ap_scenarios._assert_stays_disconnected = original_disconnect
        wifi_ap_scenarios._assert_auto_reconnected = original_reconnect

    assert [item["password"] for item in configured] == [
        "87654321",
        "24681357",
        "24681357",
    ]
    assert len(disconnected) == 1
    assert len(reconnected) == 1


def test_ssid_change_case_connects_both_profiles_then_restores_first() -> None:
    configured = []
    action = SimpleNamespace(configure_wifi=lambda **kwargs: configured.append(kwargs))
    original_connect = wifi_ap_scenarios.assert_wifi_connected
    original_ping = wifi_ap_scenarios.assert_gateway_ping
    original_reconnect = wifi_ap_scenarios._assert_auto_reconnected
    try:
        wifi_ap_scenarios.assert_wifi_connected = lambda *args, **kwargs: kwargs["entry"]["ssid"]
        wifi_ap_scenarios.assert_gateway_ping = lambda *args, **kwargs: None
        wifi_ap_scenarios._assert_auto_reconnected = lambda *args, **kwargs: None
        wifi_ap_scenarios.run_wifi_ap_ssid_change_case(
            {"case_id": "ssid-change"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            action,
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios.assert_wifi_connected = original_connect
        wifi_ap_scenarios.assert_gateway_ping = original_ping
        wifi_ap_scenarios._assert_auto_reconnected = original_reconnect

    assert [item["ssid"] for item in configured] == [
        "PyAutoTest_ApChange_1",
        "PyAutoTest_ApChange_2",
        "PyAutoTest_ApChange_1",
        "PyAutoTest_ApChange_1",
    ]


def test_channel_change_case_restores_initial_channel_and_bandwidth() -> None:
    channels = []
    action = SimpleNamespace(
        configure_wifi=lambda **kwargs: None,
        set_channel=lambda band, channel, **kwargs: channels.append(
            (band, channel, kwargs["bandwidth_mhz"], kwargs["verify"])
        ),
    )
    original_connect = wifi_ap_scenarios._configure_and_connect
    original_reconnect = wifi_ap_scenarios._assert_auto_reconnected
    try:
        wifi_ap_scenarios._configure_and_connect = lambda *args, **kwargs: None
        wifi_ap_scenarios._assert_auto_reconnected = lambda *args, **kwargs: None
        wifi_ap_scenarios.run_wifi_ap_channel_change_case(
            {"case_id": "channel-change"},
            lambda command: "",
            cast(WiFiControl, SimpleNamespace()),
            {},
            action,
            settle_sec=0,
        )
    finally:
        wifi_ap_scenarios._configure_and_connect = original_connect
        wifi_ap_scenarios._assert_auto_reconnected = original_reconnect

    assert channels == [
        ("5g", 36, 20, True),
        ("5g", 149, 80, True),
        ("5g", 36, 20, True),
    ]