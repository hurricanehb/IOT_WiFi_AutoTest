from __future__ import annotations

import ipaddress
from unittest.mock import Mock, call

import pytest

from core.utils.adb_helper import AdbDeviceUnavailableError, AdbHelper
from core.utils.config_loader import android_data_path
from core.utils.data_parser import load_yaml
from core.libs.android.wifi_scenarios.ip_configuration import (
    WiFiIPv4Info,
    collect_factory_wifi_macs,
    parse_mac_addresses,
    parse_current_wifi_mac,
    parse_wifi_ipv4_info,
    select_unused_static_address,
)
from core.libs.android.wifi_scenarios import ip_configuration as ip_config
from core.libs.android.wifi_scenarios import ip_configuration as ip_config_ui


@pytest.fixture
def ipcfg_environment() -> dict:
    config = load_yaml(android_data_path("wifi_ssid.yaml"))
    ap1 = (config.get("ipcfg_lab") or {}).get("ap1") or {}
    network = ipaddress.ip_network(ap1["expected_network"], strict=False)
    gateway = ipaddress.ip_address(ap1["gateway"])
    dns_servers = tuple(ipaddress.ip_address(value) for value in ap1["dns"])
    assert gateway in network
    assert dns_servers

    available = (
        ipaddress.IPv4Address(value)
        for value in range(
            int(network.network_address) + 1,
            int(network.broadcast_address),
        )
    )
    hosts = [value for value in available if value != gateway][:2]
    assert len(hosts) == 2, f"测试网段 {network} 至少需要两个可用主机地址"
    return {
        "network": network,
        "gateway": gateway,
        "address": hosts[0],
        "secondary_dns": hosts[1],
        "dns_servers": dns_servers,
    }


def test_parse_wifi_ipv4_info(ipcfg_environment: dict) -> None:
    network = ipcfg_environment["network"]
    gateway = ipcfg_environment["gateway"]
    address = ipcfg_environment["address"]
    secondary_dns = ipcfg_environment["secondary_dns"]
    route_text = (
        f"default via {gateway} dev wlan0 proto dhcp src {address} metric 20\n"
        f"{network} dev wlan0 proto kernel scope link src {address}\n"
    )
    dns_text = f"DnsAddresses: [ /{gateway}, /{secondary_dns} ]"

    info = parse_wifi_ipv4_info(route_text, dns_text)

    assert info.interface == "wlan0"
    assert info.address == address
    assert info.prefix_length == network.prefixlen
    assert info.gateway == gateway
    assert info.dns_servers == (gateway, secondary_dns)


def test_parse_wifi_ipv4_info_requires_default_route(
    ipcfg_environment: dict,
) -> None:
    network = ipcfg_environment["network"]
    address = ipcfg_environment["address"]
    dns = ipcfg_environment["dns_servers"][0]
    with pytest.raises(ValueError, match="默认路由"):
        parse_wifi_ipv4_info(
            f"{network} dev wlan0 scope link src {address}",
            f"DnsAddresses: [/{dns}]",
        )


def test_parse_wifi_ipv4_info_with_android_policy_route(
    ipcfg_environment: dict,
) -> None:
    network = ipcfg_environment["network"]
    gateway = ipcfg_environment["gateway"]
    address = ipcfg_environment["address"]
    dns = ipcfg_environment["dns_servers"][0]
    route_text = f"""\
default dev dummy0 table dummy0 proto static scope link
default via {gateway} dev bond0 table bond0 proto static
{network} dev bond0 proto kernel scope link src {address}
"""
    connectivity_text = (
        "NetworkAgentInfo{WIFI CONNECTED "
        f"lp{{{{InterfaceName: bond0 LinkAddresses: [{address}/{network.prefixlen}] "
        f"DnsAddresses: [/{dns}] "
        f"Routes: [0.0.0.0/0 -> {gateway} bond0]}}}}}}"
    )

    info = parse_wifi_ipv4_info(route_text, connectivity_text)

    assert info.interface == "bond0"
    assert info.address == address
    assert info.prefix_length == network.prefixlen
    assert info.gateway == gateway
    assert info.dns_servers == (dns,)


def test_select_unused_static_address_avoids_active_addresses() -> None:
    info = WiFiIPv4Info(
        interface="wlan0",
        address=ipaddress.IPv4Address("192.168.1.10"),
        prefix_length=24,
        gateway=ipaddress.IPv4Address("192.168.1.11"),
        dns_servers=(ipaddress.IPv4Address("192.168.1.1"),),
    )

    selected = select_unused_static_address(info)

    assert selected == ipaddress.IPv4Address("192.168.1.12")


def test_parse_mac_addresses_normalizes_and_deduplicates() -> None:
    assert parse_mac_addresses(
        "Factory MAC: AA:BB:CC:DD:EE:FF current=aa:bb:cc:dd:ee:ff "
        "secondary=02:11:22:33:44:55"
    ) == ("aa:bb:cc:dd:ee:ff", "02:11:22:33:44:55")


def test_parse_current_wifi_mac_ignores_preceding_bssid() -> None:
    status = (
        'WifiInfo: SSID: "Lab", BSSID: 54:f6:e2:e9:4a:4c, '
        "MAC: B8:1B:CB:13:1F:B4, IP: /192.168.2.81"
    )

    assert parse_current_wifi_mac(status) == "b8:1b:cb:13:1f:b4"


def test_collect_factory_wifi_macs_falls_back_to_ethtool() -> None:
    outputs = {
        "cmd wifi get-factory-mac-addresses": "Unknown command",
        "ethtool -P wlan0": "Permanent address: B8:1B:CB:13:1F:B4",
        "ethtool -P wlan1": "Cannot get permanent address",
    }

    assert collect_factory_wifi_macs(outputs.__getitem__) == (
        "b8:1b:cb:13:1f:b4",
    )


def test_collect_factory_wifi_macs_prefers_wifi_command() -> None:
    run_shell_cmd = Mock(return_value="Factory MAC: AA:BB:CC:DD:EE:FF")

    assert collect_factory_wifi_macs(run_shell_cmd) == ("aa:bb:cc:dd:ee:ff",)
    run_shell_cmd.assert_called_once_with("cmd wifi get-factory-mac-addresses")


def test_dismiss_printer_paper_not_ready_dialog_acknowledges_prompt(monkeypatch) -> None:
    wifi = Mock()
    wifi.adb.serial = "device-serial"
    prompt = Mock()
    prompt.exists = True
    prompt.wait_gone.return_value = True
    acknowledge = Mock()
    acknowledge.click_exists.return_value = True
    device = Mock(side_effect=[prompt, acknowledge])
    monkeypatch.setattr(ip_config.u2, "connect", Mock(return_value=device))

    ip_config._dismiss_printer_paper_not_ready_dialog(wifi)

    ip_config.u2.connect.assert_called_once_with("device-serial")
    acknowledge.click_exists.assert_called_once_with(timeout=1)
    prompt.wait_gone.assert_called_once_with(timeout=3)


def test_reboot_and_wait_dismisses_printer_dialog_after_boot(monkeypatch) -> None:
    wifi = Mock()
    wifi.adb.wait_for_device.return_value = True
    wifi.adb.shell.return_value = (0, "1", "")
    dismiss_dialog = Mock()
    monkeypatch.setattr(
        ip_config, "_dismiss_printer_paper_not_ready_dialog", dismiss_dialog
    )
    monkeypatch.setattr(ip_config.time, "sleep", Mock())

    ip_config.reboot_and_wait(wifi)

    wifi.adb.run.assert_called_once_with("reboot")
    wifi.adb.ensure_root.assert_called_once_with()
    dismiss_dialog.assert_called_once_with(wifi)


def test_reboot_and_wait_retries_disconnects_until_boot_completed(monkeypatch) -> None:
    adb = AdbHelper(serial="device-serial")
    run = Mock(
        side_effect=[
            (0, "", ""),
            AdbDeviceUnavailableError("device not found"),
            (0, "device", ""),
            (0, "0", ""),
            AdbDeviceUnavailableError("device offline"),
            (0, "1", ""),
        ]
    )
    monkeypatch.setattr(adb, "run", run)
    ensure_root = Mock()
    monkeypatch.setattr(adb, "ensure_root", ensure_root)
    wifi = Mock(adb=adb)
    dismiss_dialog = Mock()
    monkeypatch.setattr(
        ip_config, "_dismiss_printer_paper_not_ready_dialog", dismiss_dialog
    )
    sleep = Mock()
    monkeypatch.setattr(ip_config.time, "sleep", sleep)

    ip_config.reboot_and_wait(wifi)

    assert run.call_args_list == [
        call("reboot"),
        call("get-state", shell=False),
        call("get-state", shell=False),
        call("getprop", "sys.boot_completed", shell=True, check=False),
        call("getprop", "sys.boot_completed", shell=True, check=False),
        call("getprop", "sys.boot_completed", shell=True, check=False),
    ]
    ensure_root.assert_called_once_with()
    dismiss_dialog.assert_called_once_with(wifi)
    assert sleep.call_count == 4


def test_reboot_and_wait_fails_when_adb_does_not_recover(monkeypatch) -> None:
    wifi = Mock()
    wifi.adb.wait_for_device.return_value = False
    dismiss_dialog = Mock()
    monkeypatch.setattr(
        ip_config, "_dismiss_printer_paper_not_ready_dialog", dismiss_dialog
    )

    with pytest.raises(pytest.fail.Exception, match="2s 内未恢复 ADB"):
        ip_config.reboot_and_wait(wifi, timeout_sec=2)

    wifi.adb.shell.assert_not_called()
    wifi.adb.ensure_root.assert_not_called()
    dismiss_dialog.assert_not_called()


@pytest.mark.parametrize("disconnected", [False, True])
def test_reboot_and_wait_fails_when_boot_does_not_complete(
    monkeypatch, disconnected: bool
) -> None:
    wifi = Mock()
    wifi.adb.wait_for_device.return_value = True
    if disconnected:
        wifi.adb.shell.side_effect = AdbDeviceUnavailableError("device offline")
    else:
        wifi.adb.shell.return_value = (0, "0", "")
    dismiss_dialog = Mock()
    monkeypatch.setattr(
        ip_config, "_dismiss_printer_paper_not_ready_dialog", dismiss_dialog
    )
    monkeypatch.setattr(ip_config.time, "monotonic", Mock(side_effect=[0, 0, 1, 2]))
    monkeypatch.setattr(ip_config.time, "sleep", Mock())

    with pytest.raises(pytest.fail.Exception, match="2s 内未完成启动"):
        ip_config.reboot_and_wait(wifi, timeout_sec=2)

    assert wifi.adb.shell.call_count == 2
    wifi.adb.ensure_root.assert_not_called()
    dismiss_dialog.assert_not_called()


def test_static_field_input_ui_case_applies_defaults_and_overrides(monkeypatch) -> None:
    info = WiFiIPv4Info(
        interface="wlan0",
        address=ipaddress.IPv4Address("192.168.1.10"),
        prefix_length=24,
        gateway=ipaddress.IPv4Address("192.168.1.1"),
        dns_servers=(ipaddress.IPv4Address("192.168.1.2"),),
    )
    monkeypatch.setattr(ip_config_ui, "open_connected_ip_editor", Mock(return_value=info))
    ui = Mock()
    ui.set_static_field.side_effect = lambda name, value: value
    ui.save_enabled.return_value = True

    ip_config_ui.run_static_field_input_ui_case(
        Mock(),
        {},
        Mock(),
        ui,
        overrides={"dns2": "1.1.1.1"},
        expect_save_enabled=True,
        expect_values=True,
    )

    ui.select_ip_mode.assert_called_once_with("静态")
    ui.set_static_field.assert_any_call("gateway", "192.168.1.1")
    ui.set_static_field.assert_any_call("dns2", "1.1.1.1")
    ui.cancel.assert_called_once_with()


def test_dhcp_acquisition_case_runs_connection_and_network_checks(monkeypatch) -> None:
    info = WiFiIPv4Info(
        interface="wlan0",
        address=ipaddress.IPv4Address("192.168.1.10"),
        prefix_length=24,
        gateway=ipaddress.IPv4Address("192.168.1.1"),
        dns_servers=(ipaddress.IPv4Address("192.168.1.1"),),
    )
    lab_entry = {"ssid": "AP1"}
    wifi_entry = {"ssid": "AP1", "pwd": "24681357"}
    monkeypatch.setattr(ip_config, "ipcfg_lab_entry", Mock(return_value=lab_entry))
    monkeypatch.setattr(ip_config, "wifi_entry_for_lab", Mock(return_value=wifi_entry))
    monkeypatch.setattr(ip_config, "assert_wifi_connected", Mock())
    monkeypatch.setattr(ip_config, "collect_wifi_ipv4_info", Mock(return_value=info))
    monkeypatch.setattr(ip_config, "assert_expected_network", Mock())
    monkeypatch.setattr(ip_config, "assert_wifi_link_details", Mock())
    monkeypatch.setattr(ip_config, "assert_gateway_reachable", Mock())

    result = ip_config.run_dhcp_acquisition_case(Mock(), {}, Mock())

    assert result is info
    ip_config.assert_wifi_connected.assert_called_once()
    ip_config.assert_gateway_reachable.assert_called_once_with(
        ip_config.assert_wifi_connected.call_args.args[2], info.gateway
    )


def test_dhcp_renewal_case_checks_stability_and_preserves_address(monkeypatch) -> None:
    info = WiFiIPv4Info(
        interface="wlan0",
        address=ipaddress.IPv4Address("192.168.1.10"),
        prefix_length=24,
        gateway=ipaddress.IPv4Address("192.168.1.1"),
        dns_servers=(ipaddress.IPv4Address("192.168.1.1"),),
    )
    run_shell_cmd = Mock()
    monkeypatch.setattr(
        ip_config, "ipcfg_lab_entry", Mock(return_value={"lease_wait_sec": 120})
    )
    monkeypatch.setattr(ip_config, "run_dhcp_acquisition_case", Mock(return_value=info))
    monkeypatch.setattr(ip_config, "assert_gateway_stable_for", Mock())
    monkeypatch.setattr(ip_config, "collect_wifi_ipv4_info", Mock(return_value=info))
    monkeypatch.setattr(ip_config, "assert_gateway_reachable", Mock())

    ip_config.run_dhcp_renewal_case(Mock(), {}, run_shell_cmd)

    ip_config.assert_gateway_stable_for.assert_called_once_with(
        run_shell_cmd, info.gateway, 120.0
    )


def test_dhcp_switch_case_checks_both_networks(monkeypatch) -> None:
    first = WiFiIPv4Info(
        "wlan0", ipaddress.IPv4Address("192.168.1.10"), 24,
        ipaddress.IPv4Address("192.168.1.1"), (ipaddress.IPv4Address("192.168.1.1"),),
    )
    second = WiFiIPv4Info(
        "wlan0", ipaddress.IPv4Address("192.168.2.10"), 24,
        ipaddress.IPv4Address("192.168.2.1"), (ipaddress.IPv4Address("192.168.2.1"),),
    )
    monkeypatch.setattr(
        ip_config, "ipcfg_lab_entry", Mock(side_effect=[{"ssid": "AP1"}, {"ssid": "AP2"}])
    )
    monkeypatch.setattr(
        ip_config, "wifi_entry_for_lab", Mock(side_effect=[{"ssid": "AP1"}, {"ssid": "AP2"}])
    )
    monkeypatch.setattr(ip_config, "assert_wifi_connected", Mock())
    monkeypatch.setattr(ip_config, "collect_wifi_ipv4_info", Mock(side_effect=[first, second]))
    monkeypatch.setattr(ip_config, "assert_expected_network", Mock())
    monkeypatch.setattr(ip_config, "assert_gateway_reachable", Mock())

    ip_config.run_dhcp_switch_case(Mock(), {}, Mock())

    assert ip_config.assert_wifi_connected.call_count == 2
    assert ip_config.assert_expected_network.call_count == 2