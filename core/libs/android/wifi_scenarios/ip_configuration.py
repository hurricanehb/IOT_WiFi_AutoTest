"""WiFi IP configuration scenario runners."""
from __future__ import annotations

import ipaddress
import re
import time
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence

import pytest
import uiautomator2 as u2

from core.libs.android.wifi_scenarios.lab_requirements import env_enabled
from core.libs.android.wifi_control.connection_chk import assert_wifi_connected
from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.settings_pages.ip_settings_page import WiFiIPSettingsUI
from core.utils.adb_helper import AdbDeviceUnavailableError


@dataclass(frozen=True)
class WiFiIPv4Info:
    interface: str
    address: ipaddress.IPv4Address
    prefix_length: int
    gateway: ipaddress.IPv4Address
    dns_servers: tuple[ipaddress.IPv4Address, ...]


def parse_wifi_ipv4_info(route_text: str, dns_text: str) -> WiFiIPv4Info:
    interface_match = re.search(r"InterfaceName:\s*(\S+)", dns_text or "")
    interface_pattern = (
        re.escape(interface_match.group(1)) if interface_match else r"\S+"
    )
    route_match = re.search(
        r"^default\s+via\s+(?P<gateway>\d+(?:\.\d+){3})\s+dev\s+"
        rf"(?P<interface>{interface_pattern})\b.*$",
        route_text or "",
        flags=re.MULTILINE,
    )
    if not route_match:
        raise ValueError(f"未找到 WiFi IPv4 默认路由: {route_text!r}")
    interface = route_match.group("interface")
    prefix_match = re.search(
        rf"^(?P<network>\d+(?:\.\d+){{3}})/(?P<prefix>\d+)\s+dev\s+"
        rf"{re.escape(interface)}\b.*?\bsrc\s+(?P<address>\d+(?:\.\d+){{3}})\b",
        route_text or "",
        flags=re.MULTILINE,
    )
    if not prefix_match:
        raise ValueError(f"未找到 {interface} 的直连网段: {route_text!r}")
    dns_blocks = re.findall(r"DnsAddresses:\s*\[([^\]]*)\]", dns_text or "", re.I)
    dns_servers = tuple(
        dict.fromkeys(
            ipaddress.IPv4Address(value)
            for value in re.findall(
                r"(?<![\d.])\d+(?:\.\d+){3}(?![\d.])", " ".join(dns_blocks)
            )
            if not ipaddress.IPv4Address(value).is_unspecified
        )
    )
    if not dns_servers:
        raise ValueError(f"未找到 IPv4 DNS: {dns_text!r}")
    return WiFiIPv4Info(
        interface=interface,
        address=ipaddress.IPv4Address(prefix_match.group("address")),
        prefix_length=int(prefix_match.group("prefix")),
        gateway=ipaddress.IPv4Address(route_match.group("gateway")),
        dns_servers=dns_servers,
    )


def collect_wifi_ipv4_info(run_shell_cmd: Callable[[str], str]) -> WiFiIPv4Info:
    info = parse_wifi_ipv4_info(
        run_shell_cmd("ip -4 route show table all"),
        run_shell_cmd("dumpsys connectivity | grep 'WIFI CONNECTED'"),
    )
    print(
        "WiFi IPv4: "
        f"interface={info.interface}, address={info.address}/{info.prefix_length}, "
        f"gateway={info.gateway}, dns={list(map(str, info.dns_servers))}"
    )
    return info


def parse_mac_addresses(text: str) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            value.lower()
            for value in re.findall(
                r"(?<![0-9a-f])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![0-9a-f])",
                text or "",
                re.I,
            )
        )
    )


def parse_current_wifi_mac(text: str) -> str:
    match = re.search(
        r"\bMAC:\s*((?:[0-9a-f]{2}:){5}[0-9a-f]{2})\b",
        text or "",
        re.I,
    )
    return match.group(1).lower() if match else ""


def collect_factory_wifi_macs(
    run_shell_cmd: Callable[[str], str],
) -> tuple[str, ...]:
    factory_macs = parse_mac_addresses(
        run_shell_cmd("cmd wifi get-factory-mac-addresses")
    )
    if factory_macs:
        return factory_macs
    return tuple(
        dict.fromkeys(
            mac
            for interface in ("wlan0", "wlan1")
            for mac in parse_mac_addresses(run_shell_cmd(f"ethtool -P {interface}"))
        )
    )


def assert_gateway_reachable(
    run_shell_cmd: Callable[[str], str], gateway: ipaddress.IPv4Address
) -> None:
    output = run_shell_cmd(f"ping -c 4 -W 2 {gateway}")
    if not re.search(r"(?:(?<!\d)0% packet loss|4 (?:packets )?received)", output or "", re.I):
        pytest.fail(f"网关 {gateway} ping 不通:\n{output}")


def assert_wifi_link_details(
    run_shell_cmd: Callable[[str], str], info: WiFiIPv4Info
) -> None:
    status = run_shell_cmd("cmd wifi status")
    mac_match = re.search(r"\bMAC:\s*((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})", status)
    mac = mac_match.group(1) if mac_match else run_shell_cmd(
        f"cat /sys/class/net/{info.interface}/address"
    ).strip()
    if not re.fullmatch(r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", mac):
        pytest.fail(f"未能读取 {info.interface} 的有效 MAC 地址: {mac!r}")
    if not re.search(r"(?:Link speed|Tx Link speed|tx bitrate).*?\d+", status, re.I):
        link = run_shell_cmd(f"iw dev {info.interface} link")
        if not re.search(r"bitrate:\s*\d+", link, re.I):
            pytest.fail(f"未能读取 WiFi 链路速率:\n{status}\n{link}")
    print(f"WiFi link: interface={info.interface}, mac={mac}")


def assert_gateway_stable_for(
    run_shell_cmd: Callable[[str], str],
    gateway: ipaddress.IPv4Address,
    duration_sec: float,
) -> None:
    deadline = time.monotonic() + duration_sec
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return
        count = max(1, min(10, int(remaining + 0.999)))
        output = run_shell_cmd(f"ping -c {count} -i 1 -W 2 {gateway}")
        if not re.search(r"(?<!\d)0% packet loss", output or "", re.I):
            pytest.fail(f"DHCP 续租观察期间网关 {gateway} ping 不稳定:\n{output}")


def ipcfg_lab_entry(wifi_yaml: dict, name: str) -> Optional[dict]:
    entry = (wifi_yaml.get("ipcfg_lab") or {}).get(name)
    return entry if isinstance(entry, dict) else None


def wifi_entry_for_lab(wifi_yaml: dict, lab_entry: Optional[dict]) -> Optional[dict]:
    if lab_entry:
        wanted = (lab_entry.get("ssid") or "").strip()
        for entry in wifi_yaml.get("wifi_list") or []:
            if (entry.get("ssid") or "").strip() == wanted:
                return entry
        pytest.skip(f"wifi_list 无 ipcfg_lab 指定的 SSID={wanted!r}")
    for entry in wifi_yaml.get("wifi_list") or []:
        if (entry.get("type") or "normal").lower() != "hyperwifi":
            return entry
    return None


def assert_expected_network(info: WiFiIPv4Info, lab_entry: Optional[dict]) -> None:
    expected = ((lab_entry or {}).get("expected_network") or "").strip()
    if not expected:
        return
    network = ipaddress.ip_network(expected, strict=False)
    assert info.address in network, f"IPv4 应属于 {network}，实际={info.address}"
    assert info.prefix_length == network.prefixlen
    expected_gateway = ((lab_entry or {}).get("gateway") or "").strip()
    if expected_gateway:
        assert info.gateway == ipaddress.ip_address(expected_gateway)
    expected_dns = (lab_entry or {}).get("dns") or []
    missing = [
        value
        for value in expected_dns
        if ipaddress.ip_address(value) not in set(info.dns_servers)
    ]
    assert not missing, f"缺少期望 DNS {missing!r}，实际={list(map(str, info.dns_servers))}"


def open_connected_ip_editor(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
) -> WiFiIPv4Info:
    entry = wifi_entry_for_lab(wifi_yaml, ipcfg_lab_entry(wifi_yaml, "ap1"))
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    info = collect_wifi_ipv4_info(run_shell_cmd)
    ip_settings_ui.open_network_editor(ssid)
    return info


def select_unused_static_address(info: WiFiIPv4Info) -> ipaddress.IPv4Address:
    network = ipaddress.ip_network(f"{info.address}/{info.prefix_length}", strict=False)
    for offset in (1, 2, 10, -1, -2):
        candidate = ipaddress.IPv4Address(int(info.address) + offset)
        if candidate in network and candidate not in (
            info.address,
            info.gateway,
            network.network_address,
            network.broadcast_address,
        ):
            return candidate
    raise ValueError(f"无法在 {network} 中选择静态测试地址")


def wait_for_wifi_ipv4(
    run_shell_cmd: Callable[[str], str],
    *,
    expected_address: Optional[ipaddress.IPv4Address] = None,
    timeout_sec: float = 20.0,
) -> WiFiIPv4Info:
    deadline = time.monotonic() + timeout_sec
    last_error = None
    while time.monotonic() < deadline:
        try:
            info = collect_wifi_ipv4_info(run_shell_cmd)
            if expected_address is None or info.address == expected_address:
                return info
        except ValueError as exc:
            last_error = exc
        time.sleep(1.0)
    pytest.fail(
        f"等待 WiFi IPv4 配置生效超时，期望地址={expected_address}，"
        f"最后错误={last_error!r}"
    )


def gateway_is_reachable(
    run_shell_cmd: Callable[[str], str], gateway: ipaddress.IPv4Address
) -> bool:
    output = run_shell_cmd(f"ping -c 2 -W 2 {gateway}")
    return bool(re.search(r"(?:(?<!\d)0% packet loss|2 (?:packets )?received)", output or "", re.I))


def internet_is_reachable(run_shell_cmd: Callable[[str], str]) -> bool:
    output = run_shell_cmd("ping -c 2 -W 3 www.baidu.com")
    return bool(re.search(r"PING\s+www\.baidu\.com\s+\(\d+(?:\.\d+){3}\)", output or "", re.I))


def apply_ip_mode(
    ip_settings_ui: WiFiIPSettingsUI,
    ssid: str,
    mode: str,
    values: Optional[Dict[str, str]] = None,
) -> None:
    if not ip_settings_ui.device(text="IP 设置").exists:
        ip_settings_ui.open_network_editor(ssid)
    ip_settings_ui.select_ip_mode(mode)
    if values is not None:
        ip_settings_ui.fill_static(values)
    ip_settings_ui.save()
    time.sleep(2.0)


def _dismiss_printer_paper_not_ready_dialog(
    wifi: WiFiControl, timeout_sec: float = 10.0
) -> None:
    """Dismiss the printer service's post-boot paper-not-ready dialog when shown."""
    device = u2.connect(wifi.adb.serial)
    printer_package = "woyou.aidlservice.jiuiv5"
    paper_not_ready = device(
        packageName=printer_package,
        textContains="打印纸未准备好",
    )
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        if paper_not_ready.exists:
            acknowledge = device(
                packageName=printer_package,
                resourceId=f"{printer_package}:id/linear_bottom",
            )
            if not acknowledge.click_exists(timeout=1):
                pytest.fail("打印纸未准备好提示弹窗未找到“知道了”确认区域")
            if paper_not_ready.wait_gone(timeout=3):
                return
            pytest.fail("点击打印纸未准备好提示弹窗“知道了”后弹窗未消失")
        time.sleep(0.2)


def reboot_and_wait(wifi: WiFiControl, timeout_sec: float = 120.0) -> None:
    wifi.adb.run("reboot")
    if not wifi.adb.wait_for_device(total_sec=timeout_sec):
        pytest.fail(f"设备重启后 {timeout_sec:g}s 内未恢复 ADB")
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            code, output, _ = wifi.adb.shell("getprop", "sys.boot_completed")
        except AdbDeviceUnavailableError:
            time.sleep(1.0)
            continue
        if code == 0 and output.strip() == "1":
            wifi.adb.ensure_root()
            time.sleep(5.0)
            _dismiss_printer_paper_not_ready_dialog(wifi)
            return
        time.sleep(1.0)
    pytest.fail(f"设备重启后 {timeout_sec:g}s 内未完成启动")


def run_dhcp_acquisition_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
) -> WiFiIPv4Info:
    lab_entry = ipcfg_lab_entry(wifi_yaml, "ap1")
    entry = wifi_entry_for_lab(wifi_yaml, lab_entry)
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    info = collect_wifi_ipv4_info(run_shell_cmd)
    assert_expected_network(info, lab_entry)
    assert_wifi_link_details(run_shell_cmd, info)
    assert_gateway_reachable(run_shell_cmd, info.gateway)
    return info


def run_dhcp_renewal_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
) -> None:
    lab_entry = ipcfg_lab_entry(wifi_yaml, "ap1")
    if not lab_entry or "lease_wait_sec" not in lab_entry:
        pytest.skip("ipcfg_lab.ap1 未配置 lease_wait_sec，无法验证 DHCP 续租")
    before = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    wait_seconds = float(lab_entry["lease_wait_sec"])
    if wait_seconds <= 0:
        pytest.fail("ipcfg_lab.ap1.lease_wait_sec 必须大于 0")
    print(f"持续 ping 网关 {wait_seconds:g}s，跨过 DHCP 租约检查窗口")
    assert_gateway_stable_for(run_shell_cmd, before.gateway, wait_seconds)
    after = collect_wifi_ipv4_info(run_shell_cmd)
    assert_gateway_reachable(run_shell_cmd, after.gateway)
    assert after.address == before.address, (
        f"DHCP 续租后 IP 应保持不变，续租前={before.address}，续租后={after.address}"
    )


def run_dhcp_switch_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
) -> None:
    ap1 = ipcfg_lab_entry(wifi_yaml, "ap1")
    ap2 = ipcfg_lab_entry(wifi_yaml, "ap2")
    if not ap1 or not ap2:
        pytest.skip("DHCP IP 更新用例需要配置 ipcfg_lab.ap1 和 ipcfg_lab.ap2")

    first_entry = wifi_entry_for_lab(wifi_yaml, ap1)
    second_entry = wifi_entry_for_lab(wifi_yaml, ap2)
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=first_entry)
    first = collect_wifi_ipv4_info(run_shell_cmd)
    assert_expected_network(first, ap1)
    assert_gateway_reachable(run_shell_cmd, first.gateway)

    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=second_entry)
    second = collect_wifi_ipv4_info(run_shell_cmd)
    assert_expected_network(second, ap2)
    assert_gateway_reachable(run_shell_cmd, second.gateway)
    assert second.address != first.address, (
        f"切换 AP 后 IP 应更新，AP1={first.address}，AP2={second.address}"
    )


def run_static_configuration_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
    *,
    different_subnet: bool = False,
    dns_servers: Optional[Sequence[str]] = None,
    expect_gateway_reachable: bool = True,
    expect_internet: Optional[bool] = None,
) -> WiFiIPv4Info:
    before = open_connected_ip_editor(wifi, wifi_yaml, run_shell_cmd, ip_settings_ui)
    if expect_internet is not None and not internet_is_reachable(run_shell_cmd):
        ip_settings_ui.cancel()
        pytest.skip("当前 AP 无法解析外网域名，不满足 Internet--AP--STA 前置条件")
    entry = wifi_entry_for_lab(wifi_yaml, ipcfg_lab_entry(wifi_yaml, "ap1"))
    if entry is None:
        pytest.skip("wifi_list 中没有可用于 IP 配置验证的普通 WiFi")
    ssid = str(entry["ssid"])
    network = ipaddress.ip_network(f"{before.address}/{before.prefix_length}", strict=False)
    if different_subnet:
        adjacent_address = ipaddress.IPv4Address(int(network.network_address) + network.num_addresses)
        network = ipaddress.ip_network(f"{adjacent_address}/{network.prefixlen}", strict=False)
        address = ipaddress.IPv4Address(int(network.network_address) + 11)
        gateway = ipaddress.IPv4Address(int(network.network_address) + 1)
    else:
        address = select_unused_static_address(before)
        gateway = before.gateway
    dns = list(dns_servers or ("8.8.8.8", "8.8.4.4"))
    values = {
        "ip_address": str(address), "gateway": str(gateway),
        "prefix_length": str(network.prefixlen), "dns1": dns[0], "dns2": dns[1],
    }
    try:
        ip_settings_ui.select_ip_mode("静态")
        ip_settings_ui.fill_static(values)
        ip_settings_ui.save()
        applied = wait_for_wifi_ipv4(run_shell_cmd, expected_address=address)
        assert applied.gateway == gateway
        assert applied.prefix_length == network.prefixlen
        expected_dns = {ipaddress.ip_address(value) for value in dns}
        assert expected_dns.issubset(set(applied.dns_servers))
        reachable = gateway_is_reachable(run_shell_cmd, gateway)
        assert reachable is expect_gateway_reachable
        if expect_internet is not None:
            assert internet_is_reachable(run_shell_cmd) is expect_internet
        return applied
    finally:
        apply_ip_mode(ip_settings_ui, ssid, "DHCP")
        wait_for_wifi_ipv4(run_shell_cmd, expected_address=before.address, timeout_sec=30.0)


def run_ip_configuration_reboot_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
) -> None:
    if not env_enabled("IPCFG_REBOOT_CHECK"):
        pytest.skip("设置 IPCFG_REBOOT_CHECK=1 后执行两次 DUT 重启持久性验证")
    before = run_dhcp_acquisition_case(wifi, wifi_yaml, run_shell_cmd)
    entry = wifi_entry_for_lab(wifi_yaml, ipcfg_lab_entry(wifi_yaml, "ap1"))
    if entry is None:
        pytest.skip("wifi_list 中没有可用于 IP 配置验证的普通 WiFi")
    ssid = str(entry["ssid"])
    address = select_unused_static_address(before)
    values = {
        "ip_address": str(address), "gateway": str(before.gateway),
        "prefix_length": str(before.prefix_length),
        "dns1": str(before.dns_servers[0]), "dns2": "8.8.4.4",
    }
    reboot_and_wait(wifi)
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    ip_settings_ui.open_network_editor(ssid)
    assert ip_settings_ui.current_ip_mode() == "DHCP"
    ip_settings_ui.cancel()
    try:
        apply_ip_mode(ip_settings_ui, ssid, "静态", values)
        wait_for_wifi_ipv4(run_shell_cmd, expected_address=address)
        reboot_and_wait(wifi)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        persisted = wait_for_wifi_ipv4(run_shell_cmd, expected_address=address, timeout_sec=30.0)
        assert persisted.gateway == before.gateway
        ip_settings_ui.open_network_editor(ssid)
        assert ip_settings_ui.current_ip_mode() == "静态"
        ip_settings_ui.cancel()
    finally:
        apply_ip_mode(ip_settings_ui, ssid, "DHCP")
        wait_for_wifi_ipv4(run_shell_cmd, timeout_sec=30.0)


def run_default_ip_mode_ui_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
) -> None:
    open_connected_ip_editor(wifi, wifi_yaml, run_shell_cmd, ip_settings_ui)
    assert ip_settings_ui.current_ip_mode() == "DHCP"
    ip_settings_ui.cancel()


def run_ip_mode_options_ui_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
) -> None:
    open_connected_ip_editor(wifi, wifi_yaml, run_shell_cmd, ip_settings_ui)
    assert ip_settings_ui.ip_mode_options() == ["DHCP", "静态"]
    ip_settings_ui.cancel()


def run_static_fields_ui_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
) -> None:
    open_connected_ip_editor(wifi, wifi_yaml, run_shell_cmd, ip_settings_ui)
    ip_settings_ui.select_ip_mode("静态")
    labels = ip_settings_ui.static_field_labels()
    assert labels[:3] == ["IP 地址", "网关", "网络前缀长度"]
    assert any(label.startswith("DNS 1") for label in labels)
    assert any(label.startswith("DNS 2") for label in labels)
    ip_settings_ui.cancel()


def run_static_field_input_ui_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
    *,
    overrides: Dict[str, str],
    expect_save_enabled: bool,
    expect_values: bool = False,
) -> None:
    info = open_connected_ip_editor(wifi, wifi_yaml, run_shell_cmd, ip_settings_ui)
    ip_settings_ui.select_ip_mode("静态")
    values = {
        "ip_address": str(select_unused_static_address(info)),
        "gateway": str(info.gateway),
        "prefix_length": str(info.prefix_length),
        "dns1": str(info.dns_servers[0]) if info.dns_servers else "8.8.8.8",
        "dns2": "8.8.4.4",
    }
    for name, value in values.items():
        if name not in overrides:
            ip_settings_ui.set_static_field(name, value)
    actual = {
        name: ip_settings_ui.set_static_field(name, value)
        for name, value in overrides.items()
    }
    if expect_values:
        for name, expected in overrides.items():
            assert actual[name] == expected, (
                f"{name} 应接受输入 {expected!r}，实际={actual[name]!r}"
            )
    save_enabled = ip_settings_ui.save_enabled()
    rejected_input = any(
        actual[name] != expected for name, expected in overrides.items()
    )
    assert save_enabled is expect_save_enabled or (
        not expect_save_enabled and rejected_input
    ), f"非法输入应被拒绝或禁用保存，save_enabled={save_enabled}，字段值={actual!r}"
    ip_settings_ui.cancel()


def run_mac_privacy_case(
    wifi: WiFiControl,
    wifi_yaml: dict,
    run_shell_cmd: Callable[[str], str],
    ip_settings_ui: WiFiIPSettingsUI,
    *,
    mode: str,
) -> None:
    entry = wifi_entry_for_lab(wifi_yaml, ipcfg_lab_entry(wifi_yaml, "ap1"))
    ssid = assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
    factory_macs = collect_factory_wifi_macs(run_shell_cmd)
    if not factory_macs:
        pytest.skip("设备未返回 factory/permanent WiFi MAC，无法验证隐私模式")

    password = str(entry.get("pwd") or entry.get("password") or "")
    wifi.clear_saved_networks()
    ip_settings_ui.open_network_connection_editor(ssid, password)
    original_mode = ip_settings_ui.current_privacy_mode()
    try:
        ip_settings_ui.select_privacy_mode(mode)
        ip_settings_ui.save()
        time.sleep(3.0)
        assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, entry=entry)
        current = parse_current_wifi_mac(run_shell_cmd("cmd wifi status"))
        if not current:
            pytest.fail("cmd wifi status 未返回当前关联 MAC")
        if mode == "device":
            assert current in factory_macs, (
                f"设备 MAC 模式应使用 factory MAC，当前={current}，factory={factory_macs}"
            )
        elif mode == "randomized":
            assert current not in factory_macs, (
                f"随机 MAC 不应等于 factory MAC，当前={current}，factory={factory_macs}"
            )
            assert int(current.split(":", 1)[0], 16) & 0x02, (
                f"随机 MAC 应设置本地管理位，当前={current}"
            )
        else:
            raise ValueError(f"不支持的 WiFi 隐私模式: {mode!r}")
    finally:
        if original_mode != mode:
            wifi.clear_saved_networks()
            ip_settings_ui.open_network_connection_editor(ssid, password)
            ip_settings_ui.select_privacy_mode(original_mode)
            ip_settings_ui.save()