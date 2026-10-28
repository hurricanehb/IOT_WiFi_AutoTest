import ipaddress
from types import SimpleNamespace

import pytest

from core.libs.android.wifi_scenarios import ssidpwd_connection
from core.libs.android.wifi_scenarios.ssidpwd_connection import (
    _default_gateway,
    assert_gateway_ping,
    run_add_network_connection_case,
)


class _AdbWithPolicyRoute:
    def shell(self, *args):
        assert args == ("ip", "route", "show", "table", "all")
        return (
            0,
            "default via 192.168.0.1 dev bond0 table bond0 proto static\n"
            "192.168.0.0/24 dev bond0 table bond0 proto static scope link\n",
            "",
        )


def test_default_gateway_reads_android_policy_route_table() -> None:
    assert _default_gateway(_AdbWithPolicyRoute()) == "192.168.0.1"


def test_gateway_ping_is_strict_by_default() -> None:
    wifi = SimpleNamespace(
        adb=SimpleNamespace(shell=lambda *args: (0, "", ""))
    )

    with pytest.raises(pytest.fail.Exception, match="未解析到默认网关"):
        assert_gateway_ping(wifi, summary="case")


def test_add_network_connection_requires_ipv4_and_gateway(monkeypatch) -> None:
    calls = []
    info = SimpleNamespace(gateway=ipaddress.ip_address("192.168.2.1"))
    monkeypatch.setattr(
        ssidpwd_connection,
        "wait_for_wifi_ipv4",
        lambda run_shell_cmd: calls.append("ipv4") or info,
    )
    monkeypatch.setattr(
        ssidpwd_connection,
        "assert_gateway_reachable",
        lambda run_shell_cmd, gateway: calls.append(("ping", gateway)),
    )
    wifi = SimpleNamespace(
        set_wifi_enabled=lambda enabled: True,
        list_networks_blob=lambda: 'networkId=1 ssid="Open-Lab"',
        list_connected_ssids=lambda **kwargs: ["Open-Lab"],
    )
    add_network_ui = SimpleNamespace(
        open=lambda: None,
        set_ssid=lambda value: value,
        select_security=lambda value: None,
        save=lambda: None,
    )

    run_add_network_connection_case(
        "case",
        lambda command: "",
        wifi,
        {},
        add_network_ui,
        profile={
            "ssid": "Open-Lab",
            "password": "",
            "encrypt": "OPEN",
            "type": "normal",
            "expect": "connected",
        },
        security="open",
    )

    assert calls == ["ipv4", ("ping", info.gateway)]


def test_nrc_miniap_compatibility_configures_connects_and_pings(monkeypatch) -> None:
    calls = []
    miniap = SimpleNamespace(
        set_wifi_profile=lambda **kwargs: calls.append(("configure", kwargs))
    )
    monkeypatch.setenv("MINIAP_LAB", "1")
    monkeypatch.setattr(
        ssidpwd_connection,
        "assert_wifi_connected",
        lambda *args, **kwargs: calls.append(("connect", kwargs["entry"])) or "NRC-Lab",
    )
    monkeypatch.setattr(
        ssidpwd_connection,
        "assert_gateway_ping",
        lambda *args, **kwargs: calls.append(("ping", kwargs["summary"])),
    )

    connected = ssidpwd_connection.run_nrc_miniap_compatibility_case(
        {"case_id": "AP_Comp_005"},
        lambda command: "",
        SimpleNamespace(),
        {
            "wifi_list": [
                {
                    "ssid": "NRC-Lab",
                    "pwd": "24681357",
                    "encrypt": "WPA3",
                    "type": "hyperwifi",
                    "expect": "connected",
                }
            ]
        },
        miniap,
    )

    assert connected == "NRC-Lab"
    assert [name for name, _ in calls] == ["configure", "connect", "ping"]