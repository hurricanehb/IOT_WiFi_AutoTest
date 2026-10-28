"""Minimal iperf3 test script.

Android controls the iperf3 client through ADB.
The PC side server must be started manually before running this script:

    /iperf3 -s

This script keeps only the essentials:
- auto-detect or use a specified ADB serial
- run iperf3 upload/download tests from Android to PC
- print per-run results and averages
"""

import os
import re
import subprocess
import sys
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Alignment


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ====== Run-time settings (edit here before execution) ======
SERVER_IP = '192.168.1.14'  # PC iperf3 server IP
PING_IP = '192.168.1.1'      # Ping target IP
ADB_SERIAL = ''              # Android device serial, empty means auto-detect

TEST_DURATION = 30           # iperf3 duration for each run (seconds)
TEST_TIMES = 3               # run count for uplink/downlink
TEST_PROTOCOL = 'tcp'       # tcp / udp / both
IPERF_PARALLEL_STREAMS = 1   # iperf3 -P 并发流数量
UDP_BANDWIDTH = '10M'        # UDP模式下iperf3 -b
UDP_PACKET_LEN = 1200        # UDP模式下iperf3 -l
STA_FIXED_CHANNEL_WIDTH = '' # 手工指定协商频宽，例如 '20 MHz'/'40 MHz'/'80 MHz'

# Output file naming (prefix + timestamp)
OUTPUT_FILE_PREFIX = 'iperf_android_manual'

PING_COUNT = 10               # ping packet count
PING_LARGE_PACKET_SIZE = 1520  # large ping packet size (bytes)
PING_LARGE_PACKET_COUNT = 10   # large ping packet count

# When True, channel/RX/TX use only `cmd wifi status` to avoid fallback override.
CMD_WIFI_STATUS_ONLY = True


class AdbShellSta:
    """Run shell commands on Android via adb."""

    def __init__(self, serial=''):
        self.serial = serial
        self.connected = False

    @staticmethod
    def _list_devices(timeout=8):
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            check=False,
        )

        devices = []
        for line in (result.stdout or '').splitlines():
            line = line.strip()
            if not line or line.startswith('List of devices attached'):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[1] == 'device':
                devices.append(parts[0])
        return devices

    def login(self, serial=''):
        if serial:
            self.serial = serial

        if not self.serial:
            devices = self._list_devices()
            if len(devices) == 1:
                self.serial = devices[0]
            elif len(devices) > 1:
                raise RuntimeError(f'检测到多个ADB设备，请指定serial: {devices}')
            else:
                raise RuntimeError('未检测到ADB设备，请检查USB连接和adb授权')

        result = subprocess.run(
            ['adb', '-s', self.serial, 'get-state'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=8,
            check=False,
        )
        state = (result.stdout or result.stderr or '').strip().lower()
        if result.returncode != 0 or 'device' not in state:
            raise RuntimeError(f'ADB设备状态异常({self.serial}): {state or "unknown"}')

        self.connected = True

    def execute_command(self, command, timeout=10):
        if not self.connected:
            self.login(self.serial)

        result = subprocess.run(
            ['adb', '-s', self.serial, 'shell', command],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            check=False,
        )
        stdout = (result.stdout or '').replace('\r\n', '\n')
        stderr = (result.stderr or '').replace('\r\n', '\n')
        output = (stdout + ('\n' + stderr if stderr else '')).strip()
        if result.returncode != 0 and not output:
            raise RuntimeError(f'adb shell执行失败: {command}')
        return output

    def logout(self):
        self.connected = False


def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class TimestampDualLogger:
    """Write logs to console and file with timestamp prefix."""

    def __init__(self, log_file_path, console):
        self.console = console
        self.log_file = open(log_file_path, 'w', encoding='utf-8')

    def write(self, message):
        if not message:
            return

        if message.strip():
            ts = now_str()
            lines = message.split('\n')
            for line in lines:
                if line.strip():
                    formatted = f'[{ts}] {line}'
                    self.console.write(formatted + '\n')
                    self.log_file.write(formatted + '\n')
        else:
            self.console.write(message)
            self.log_file.write(message)

    def flush(self):
        self.console.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.flush()
        self.log_file.close()


def to_mbps(output):
    """Parse iperf3 receiver throughput and normalize to Mbits/sec."""
    lines = (output or '').splitlines()

    def _to_mbps(value_str, unit_str):
        value = float(value_str)
        unit = unit_str.upper()
        if unit == 'K':
            return round(value / 1000, 3)
        if unit == 'G':
            return round(value * 1000, 3)
        return round(value, 3)

    # 并发(-P)时会有多行receiver，倒序取最后一条可拿到最终汇总值。
    for line in reversed(lines):
        if 'receiver' not in line.lower():
            continue
        match = re.search(r'(\d+(?:\.\d+)?)\s+([KMG])bits/sec\s+receiver', line, re.IGNORECASE)
        if match:
            return _to_mbps(match.group(1), match.group(2))

    # 兜底：若输出异常缺少receiver关键字，取最后一个bits/sec值。
    for line in reversed(lines):
        match = re.search(r'(\d+(?:\.\d+)?)\s+([KMG])bits/sec', line, re.IGNORECASE)
        if match:
            return _to_mbps(match.group(1), match.group(2))

    return None


def average(values):
    nums = []
    for item in values:
        try:
            nums.append(float(item))
        except (TypeError, ValueError):
            continue
    if not nums:
        return None
    return round(sum(nums) / len(nums), 3)


def parse_ping_result(output):
    """Parse ping packet loss and latency summary."""
    packet_loss_match = re.search(r'(\d+(?:\.\d+)?)%\s*packet loss', output or '', re.IGNORECASE)
    latency_match = re.search(
        r'(?:round-trip|rtt)\s+min/avg/max(?:/[a-z]+)?\s*=\s*([\d\.]+)/([\d\.]+)/([\d\.]+)(?:/[\d\.]+)?\s*ms',
        output or '',
        re.IGNORECASE,
    )

    if not packet_loss_match or not latency_match:
        return None, None, None, None

    return (
        packet_loss_match.group(1),
        latency_match.group(1),
        latency_match.group(2),
        latency_match.group(3),
    )


class IperfAndroidManualServerTester:
    def __init__(
        self,
        server_ip,
        ping_ip,
        duration=30,
        times=3,
        protocol='both',
        parallel_streams=1,
        udp_bandwidth='10M',
        udp_packet_len=1200,
        ping_count=4,
        ping_large_packet_size=1520,
        ping_large_packet_count=10,
        serial=''
    ):
        self.server_ip = server_ip
        self.ping_ip = ping_ip
        self.duration = duration
        self.times = times
        self.protocol = (protocol or 'both').strip().lower()
        if self.protocol not in ('tcp', 'udp', 'both'):
            self.protocol = 'both'

        self.enable_tcp_test = self.protocol in ('tcp', 'both')
        self.enable_udp_test = self.protocol in ('udp', 'both')
        self.parallel_streams = parallel_streams if parallel_streams and parallel_streams > 0 else 1
        self.udp_bandwidth = udp_bandwidth
        self.udp_packet_len = udp_packet_len
        self.ping_count = ping_count
        self.ping_large_packet_size = ping_large_packet_size
        self.ping_large_packet_count = ping_large_packet_count
        self.last_channel_width = '未知'
        self.fixed_channel_width = None
        self.sta_shell = AdbShellSta(serial)
        self.iperf3_path = '/data/local/tmp/iperf3'
        self.result_dir = os.path.join(PROJECT_ROOT, 'test_results')
        os.makedirs(self.result_dir, exist_ok=True)
        run_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.excel_path = os.path.join(
            self.result_dir,
            f'{OUTPUT_FILE_PREFIX}_{run_tag}.xlsx'
        )
        self.log_path = os.path.join(self.result_dir, f'{OUTPUT_FILE_PREFIX}_{run_tag}.log')
        self.logger = None
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'iperf结果'
        self._init_excel()

    @staticmethod
    def _map_android_channel_width(value):
        """Map Android channelWidth enum/int to readable MHz text when possible."""
        mapping = {
            '0': '20 MHz',
            '1': '40 MHz',
            '2': '80 MHz',
            '3': '160 MHz',
            '4': '80+80 MHz',
            '5': '320 MHz',
        }
        return mapping.get(str(value).strip())

    def _start_logging(self):
        if self.logger is None:
            self.logger = TimestampDualLogger(self.log_path, sys.stdout)
            sys.stdout = self.logger

    def _stop_logging(self):
        if self.logger is not None:
            sys.stdout = self.logger.console
            self.logger.close()
            self.logger = None

    def _init_excel(self):
        headers = [
            '测试时间', 'ADB设备', 'PC服务器IP', '协议模式', '并发流(P)', '测试时长(s)', 'Ping目标IP', 'Ping次数',
            'STA信道', 'STA RSSI', 'STA RX', 'STA TX',
            'Ping丢包率(%)', 'Ping最小延时(ms)', 'Ping平均延时(ms)', 'Ping最大延时(ms)',
            'Ping大包丢包率(%)', 'Ping大包最小延时(ms)', 'Ping大包平均延时(ms)', 'Ping大包最大延时(ms)',
        ]

        if self.enable_tcp_test:
            for i in range(self.times):
                headers.append(f'TCP上行{i + 1}(Mbits/sec)')
            headers.append('TCP上行平均(Mbits/sec)')
            for i in range(self.times):
                headers.append(f'TCP下行{i + 1}(Mbits/sec)')
            headers.append('TCP下行平均(Mbits/sec)')
            for i in range(self.times):
                headers.append(f'TCP上行{i + 1}前频宽')
                headers.append(f'TCP上行{i + 1}后频宽')
            for i in range(self.times):
                headers.append(f'TCP下行{i + 1}前频宽')
                headers.append(f'TCP下行{i + 1}后频宽')

        if self.enable_udp_test:
            for i in range(self.times):
                headers.append(f'UDP上行{i + 1}(Mbits/sec)')
            headers.append('UDP上行平均(Mbits/sec)')
            for i in range(self.times):
                headers.append(f'UDP下行{i + 1}(Mbits/sec)')
            headers.append('UDP下行平均(Mbits/sec)')
            for i in range(self.times):
                headers.append(f'UDP上行{i + 1}前频宽')
                headers.append(f'UDP上行{i + 1}后频宽')
            for i in range(self.times):
                headers.append(f'UDP下行{i + 1}前频宽')
                headers.append(f'UDP下行{i + 1}后频宽')

        for col, header in enumerate(headers, 1):
            cell = self.ws.cell(row=1, column=col, value=header)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            self.ws.column_dimensions[cell.column_letter].width = 18

        self.row_idx = 2

    def _save_row(self, row_data):
        for col, value in enumerate(row_data, 1):
            cell = self.ws.cell(row=self.row_idx, column=col, value=value)
            cell.alignment = Alignment(horizontal='center', vertical='center')
        self.wb.save(self.excel_path)
        self.row_idx += 1

    def run_ping_once(self):
        commands = [
            f'ping -c {self.ping_count} {self.ping_ip}',
            f'/system/bin/ping -c {self.ping_count} {self.ping_ip}',
            f'toybox ping -c {self.ping_count} {self.ping_ip}',
        ]

        output = ''
        last_error = ''
        for cmd in commands:
            try:
                print(f'[{now_str()}] Android执行Ping: {cmd}')
                output = self.sta_shell.execute_command(cmd, timeout=self.ping_count * 2 + 8)
                if re.search(r'not found|unknown command|inaccessible|permission denied', output, re.IGNORECASE):
                    last_error = output
                    continue
                break
            except Exception as exc:
                last_error = str(exc)

        if not output:
            print(f'[{now_str()}] Ping失败: {last_error}')
            return '测试失败', '测试失败', '测试失败', '测试失败'

        print(output)
        packet_loss, min_latency, avg_latency, max_latency = parse_ping_result(output)
        if packet_loss is None:
            print(f'[{now_str()}] Ping结果解析失败')
            return '解析失败', '解析失败', '解析失败', '解析失败'

        return packet_loss, min_latency, avg_latency, max_latency

    def run_ping_large_packet_once(self):
        commands = [
            f'ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_ip}',
            f'/system/bin/ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_ip}',
            f'toybox ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_ip}',
        ]

        output = ''
        last_error = ''
        for cmd in commands:
            try:
                print(f'[{now_str()}] Android执行Ping大包: {cmd}')
                output = self.sta_shell.execute_command(cmd, timeout=self.ping_large_packet_count * 2 + 8)
                if re.search(r'not found|unknown command|inaccessible|permission denied', output, re.IGNORECASE):
                    last_error = output
                    continue
                break
            except Exception as exc:
                last_error = str(exc)

        if not output:
            print(f'[{now_str()}] Ping大包失败: {last_error}')
            return '测试失败', '测试失败', '测试失败', '测试失败'

        print(output)
        packet_loss, min_latency, avg_latency, max_latency = parse_ping_result(output)
        if packet_loss is None:
            print(f'[{now_str()}] Ping大包结果解析失败')
            return '解析失败', '解析失败', '解析失败', '解析失败'

        return packet_loss, min_latency, avg_latency, max_latency

    @staticmethod
    def _parse_wifi_status_fields(text):
        """Split cmd wifi status comma-separated fields into a dict (key lowercased)."""
        flat = re.sub(r'[\r\n]+', ', ', text or '')
        fields = {}
        for token in flat.split(','):
            token = token.strip()
            m = re.match(r'^([^:=]+?)\s*[:=]\s*(.+)$', token)
            if m:
                key = m.group(1).strip().lower()
                fields[key] = m.group(2).strip()
        return fields

    @staticmethod
    def _freq_to_channel(freq_mhz):
        """Convert center frequency (MHz) to Wi-Fi channel when possible."""
        try:
            f = int(freq_mhz)
        except (TypeError, ValueError):
            return None

        if f == 2484:
            return 14
        if 2412 <= f <= 2472:
            return (f - 2407) // 5
        if 5000 <= f <= 5900:
            return (f - 5000) // 5
        if 5955 <= f <= 7115:
            return (f - 5950) // 5
        return None

    def get_sta_link_metrics(self):
        """Get STA channel/RSSI/RX/TX from Android shell with fallbacks."""
        channel = '未知'
        rssi = '未知'
        rx_rate = '未知'
        tx_rate = '未知'
        freq = ''

        # First choice: standard Linux wireless info
        if not CMD_WIFI_STATUS_ONLY:
            try:
                output = self.sta_shell.execute_command('iw dev wlan0 link', timeout=8)
                if output and 'not connected' not in output.lower():
                    for raw_line in output.splitlines():
                        line = raw_line.strip()

                        match = re.search(r'freq:\s*(\d+)', line, re.IGNORECASE)
                        if match:
                            freq = match.group(1)

                        match = re.search(r'channel\s+(\d+)', line, re.IGNORECASE)
                        if match:
                            channel = match.group(1)

                        match = re.search(r'signal:\s*(-?\d+)\s*dBm', line, re.IGNORECASE)
                        if match:
                            rssi = match.group(1)

                        match = re.search(r'rx\s+bitrate:\s*(.+)$', line, re.IGNORECASE)
                        if match:
                            rx_rate = match.group(1).strip()

                        match = re.search(r'tx\s+bitrate:\s*(.+)$', line, re.IGNORECASE)
                        if match:
                            tx_rate = match.group(1).strip()
            except Exception:
                pass

        # Prefer TX (and RX if available) from Android framework status.
        try:
            wifi_status = self.sta_shell.execute_command('cmd wifi status', timeout=8)
            if wifi_status:
                fields = self._parse_wifi_status_fields(wifi_status)

                # channel: derive from Frequency field
                freq_val = fields.get('frequency', '')
                freq_match = re.search(r'(\d+)', freq_val)
                if freq_match:
                    freq = freq_match.group(1)
                    fw_channel = self._freq_to_channel(freq)
                    if fw_channel is not None:
                        channel = f'{fw_channel} ({freq}MHz)'
                    else:
                        channel = f'freq:{freq}MHz'
                    print(f'[{now_str()}] cmd wifi status 频率解析值: {channel}')

                # TX: exact key "tx link speed"
                tx_val = fields.get('tx link speed', '')
                if tx_val:
                    if re.fullmatch(r'\d+(?:\.\d+)?', tx_val):
                        tx_val = f'{tx_val} Mbps'
                    elif re.fullmatch(r'\d+(?:\.\d+)?\s*mbps', tx_val, re.IGNORECASE):
                        tx_val = re.sub(r'\s*mbps$', ' Mbps', tx_val, flags=re.IGNORECASE)
                    tx_rate = tx_val
                    print(f'[{now_str()}] cmd wifi status TX解析值: {tx_rate}')

                # RX: exact key "rx link speed"
                rx_val = fields.get('rx link speed', '')
                if rx_val:
                    if re.fullmatch(r'\d+(?:\.\d+)?', rx_val):
                        rx_val = f'{rx_val} Mbps'
                    elif re.fullmatch(r'\d+(?:\.\d+)?\s*mbps', rx_val, re.IGNORECASE):
                        rx_val = re.sub(r'\s*mbps$', ' Mbps', rx_val, flags=re.IGNORECASE)
                    rx_rate = rx_val
                    print(f'[{now_str()}] cmd wifi status RX解析值: {rx_rate}')

                # RSSI: exact key "rssi"
                rssi_val = fields.get('rssi', '')
                rssi_match = re.search(r'-?\d+', rssi_val)
                if rssi_match:
                    rssi = rssi_match.group(0)
                    print(f'[{now_str()}] cmd wifi status RSSI解析值: {rssi}')
        except Exception:
            pass

        # Fallback for channel
        if channel == '未知' and not CMD_WIFI_STATUS_ONLY:
            try:
                output = self.sta_shell.execute_command('cli_app show config | grep Frequency', timeout=8)
                match = re.search(r'Frequency\s*:\s*(.+)', output)
                if match:
                    channel = match.group(1).strip()
            except Exception:
                pass

        # Fallback for RSSI
        if rssi == '未知':
            try:
                output = self.sta_shell.execute_command('cli_app show signal', timeout=8)
                match = re.search(r'rssi\s*:\s*(-?\d+)', output, re.IGNORECASE)
                if match:
                    rssi = match.group(1)
            except Exception:
                pass

        # Fallback for RX/TX bit rate
        if (rx_rate == '未知' or tx_rate == '未知') and not CMD_WIFI_STATUS_ONLY:
            try:
                output = self.sta_shell.execute_command('cli_app show ap 0', timeout=8)
                rates = re.findall(r'[\d\.]+MBit/s\(MCS\s*\d+\)', output)
                if len(rates) >= 2:
                    if tx_rate == '未知':
                        tx_rate = rates[0]
                    if rx_rate == '未知':
                        rx_rate = rates[1]
            except Exception:
                pass

        if channel == '未知' and freq:
            channel = f'freq:{freq}'

        if CMD_WIFI_STATUS_ONLY and (channel == '未知' or rx_rate == '未知' or tx_rate == '未知'):
            print(
                f'[{now_str()}] 告警: CMD_WIFI_STATUS_ONLY开启，'
                f'部分字段未从cmd wifi status解析到: channel={channel}, RX={rx_rate}, TX={tx_rate}'
            )

        return channel, rssi, rx_rate, tx_rate

    def get_sta_channel_width(self):
        """Get current negotiated channel width (e.g. 20/40/80/160/320 MHz)."""
        width = '未知'

        def _normalize_width(raw):
            if not raw:
                return None
            match = re.search(r'([0-9]+)\s*MHz', raw, re.IGNORECASE)
            if match:
                return f'{match.group(1)} MHz'
            return None

        def _extract_width_from_text(text, allow_enum=True):
            if not text:
                return None

            # Explicit width/bandwidth key-value styles.
            key_patterns = [
                r'(?:channel\s*width|chwidth|bandwidth|bw)\s*[:=]\s*([^\n\r,;]+)',
                r'\b(?:channel\s*width|chwidth|bandwidth|bw)\b[^\n\r]*?([0-9]+\s*MHz)'
            ]
            for pattern in key_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    normalized = _normalize_width(match.group(1))
                    if normalized:
                        return normalized

            # Android / dumpsys style numeric enums, e.g. channelWidth=2
            if allow_enum:
                enum_match = re.search(r'channelwidth\s*[:=]\s*(\d+)', text, re.IGNORECASE)
                if enum_match:
                    mapped = self._map_android_channel_width(enum_match.group(1))
                    if mapped:
                        return mapped

            # iw bitrate line can contain width like "... 80MHz ..."
            bitrate_lines = re.findall(r'(?:tx|rx)\s+bitrate:[^\n\r]+', text, re.IGNORECASE)
            for line in bitrate_lines:
                normalized = _normalize_width(line)
                if normalized:
                    return normalized

            return None

        def _extract_width_from_dumpsys(text, ref_freq=None, ref_bssid=''):
            """Parse width from dumpsys using current connected freq/BSSID context."""
            if not text:
                return None

            # Prefer explicit width descriptors if they are in a line with the current frequency.
            lines = (text or '').splitlines()
            ref_freq_str = str(ref_freq) if ref_freq is not None else ''
            ref_bssid_norm = (ref_bssid or '').strip().lower()

            for raw_line in lines:
                line = raw_line.strip()
                if not line:
                    continue
                if ref_freq_str and ref_freq_str not in line:
                    continue
                parsed = _extract_width_from_text(line, allow_enum=False)
                if parsed:
                    return parsed

            # Fallback: parse channelWidth enum only for strictly matched current link context.
            # If multiple widths appear for same context, treat as ambiguous and return None.
            matched_widths = []
            for raw_line in lines:
                line = raw_line.strip()
                if 'channelwidth' not in line.lower():
                    continue

                enum_match = re.search(r'channelwidth\s*[:=]\s*(\d+)', line, re.IGNORECASE)
                if not enum_match:
                    continue
                mapped = self._map_android_channel_width(enum_match.group(1))
                if not mapped:
                    continue

                freq_match = re.search(r'(?:\bfreq\b|\bfrequency\b)\s*[:=]\s*(\d+)', line, re.IGNORECASE)
                line_freq = freq_match.group(1) if freq_match else ''

                bssid_match = re.search(r'\bbssid\b\s*[:=]\s*([0-9a-f]{2}(?::[0-9a-f]{2}){5})', line, re.IGNORECASE)
                line_bssid = bssid_match.group(1).lower() if bssid_match else ''

                # Require exact frequency match when available.
                if ref_freq_str and line_freq != ref_freq_str:
                    continue

                # Require exact bssid match when available.
                if ref_bssid_norm:
                    if not line_bssid or line_bssid != ref_bssid_norm:
                        continue

                matched_widths.append(mapped)

            unique_widths = sorted(set(matched_widths))
            if len(unique_widths) == 1:
                return unique_widths[0]
            if len(unique_widths) > 1:
                print(
                    f'[{now_str()}] dumpsys频宽候选冲突: '
                    f'freq={ref_freq_str or "未知"}, bssid={ref_bssid_norm or "未知"}, '
                    f'候选={unique_widths}'
                )
            return None

        def _compact_output(text, max_lines=6, max_chars=300):
            if not text:
                return ''
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            compact = ' | '.join(lines[:max_lines])
            if len(compact) > max_chars:
                compact = compact[:max_chars] + '...'
            return compact

        probes = [
            ('iw dev wlan0 info', 8),
            ('iw dev wlan0 link', 8),
            ('iw dev wlan0 station dump', 8),
            ('cmd wifi status', 8),
            ('dumpsys wifi', 12),
        ]

        probe_summaries = []
        connected_freq = None
        connected_bssid = ''

        for command, timeout in probes:
            try:
                output = self.sta_shell.execute_command(command, timeout=timeout)
                if command == 'cmd wifi status':
                    fields = self._parse_wifi_status_fields(output)
                    freq_val = fields.get('frequency', '')
                    freq_match = re.search(r'(\d+)', freq_val)
                    if freq_match:
                        connected_freq = int(freq_match.group(1))
                    connected_bssid = (fields.get('bssid', '') or '').strip()

                if command == 'dumpsys wifi':
                    parsed = _extract_width_from_dumpsys(output, connected_freq, connected_bssid)
                else:
                    parsed = _extract_width_from_text(output, allow_enum=True)
                if parsed:
                    print(f'[{now_str()}] 协商频宽解析成功({command}): {parsed}')
                    return parsed

                summary = _compact_output(output)
                if summary:
                    probe_summaries.append(f'{command} => {summary}')
                else:
                    probe_summaries.append(f'{command} => <empty>')
            except Exception as exc:
                probe_summaries.append(f'{command} => <error: {exc}>')

        print(f'[{now_str()}] 协商频宽解析失败，已探测输出:')
        if connected_freq is not None or connected_bssid:
            print(
                f'[{now_str()}] 连接上下文: '
                f'frequency={connected_freq if connected_freq is not None else "未知"}, '
                f'bssid={connected_bssid or "未知"}'
            )
        for summary in probe_summaries:
            print(f'[{now_str()}] {summary}')

        return width

    def resolve_iperf3_path(self):
        """Prefer iperf3 in PATH, fallback to /data/local/tmp/iperf3."""
        try:
            output = self.sta_shell.execute_command('command -v iperf3', timeout=8).strip()
            if output and 'not found' not in output.lower():
                self.iperf3_path = 'iperf3'
                return
        except Exception:
            pass

        self.iperf3_path = '/data/local/tmp/iperf3'

    def run_once(self, reverse=False, udp=False):
        protocol_name = 'UDP' if udp else 'TCP'
        direction = f'{protocol_name}{"下行" if reverse else "上行"}'
        pre_width = self.fixed_channel_width if self.fixed_channel_width is not None else self.get_sta_channel_width()
        if pre_width == '未知' and self.last_channel_width != '未知':
            pre_width = self.last_channel_width
        print(f'[{now_str()}] {direction}测试前协商频宽: {pre_width}')

        cmd = f'{self.iperf3_path} -c {self.server_ip} -t {self.duration} -i 1'
        if self.parallel_streams > 1:
            cmd += f' -P {self.parallel_streams}'
        if udp:
            cmd += f' -u -b {self.udp_bandwidth} -l {self.udp_packet_len}'
        if reverse:
            cmd += ' -R'

        print(f'[{now_str()}] Android执行{direction}测试: {cmd}')
        try:
            output = self.sta_shell.execute_command(cmd, timeout=self.duration + 15)
        except Exception as exc:
            print(f'[{now_str()}] {direction}测试执行失败: {str(exc)}')
            return '错误', pre_width, '未知'

        print(output)

        if STA_FIXED_CHANNEL_WIDTH.strip():
            post_width = self.fixed_channel_width
        else:
            post_width = self.get_sta_channel_width()
            if post_width == '未知' and pre_width != '未知':
                post_width = pre_width
        if post_width != '未知':
            self.last_channel_width = post_width
        print(f'[{now_str()}] {direction}测试后协商频宽: {post_width}')

        throughput = to_mbps(output)
        if throughput is None:
            print(f'[{now_str()}] {direction}吞吐量解析失败')
            return '解析失败', pre_width, post_width

        print(f'[{now_str()}] {direction}吞吐量: {throughput} Mbits/sec')
        return throughput, pre_width, post_width

    def run(self):
        self._start_logging()
        print('=' * 80)
        print(f'[{now_str()}] 测试开始')
        print(f'[{now_str()}] ADB设备: {self.sta_shell.serial or "auto"}')
        print(f'[{now_str()}] PC端iperf3服务器: {self.server_ip}')
        print(f'[{now_str()}] 协议模式: {self.protocol.upper()}')
        print(f'[{now_str()}] 并发流(P): {self.parallel_streams}')
        if self.enable_udp_test:
            print(f'[{now_str()}] UDP参数: 带宽={self.udp_bandwidth}, 包长={self.udp_packet_len}')
        print(f'[{now_str()}] Ping目标: {self.ping_ip}, 次数: {self.ping_count}')
        print(
            f'[{now_str()}] Ping大包: 目标={self.ping_ip}, 次数={self.ping_large_packet_count}, '
            f'包大小={self.ping_large_packet_size}'
        )
        print(f'[{now_str()}] 测试时长: {self.duration}s, 轮次: {self.times}')
        print(f'[{now_str()}] 说明: 请先在PC端手工启动 `/data/local/tmp/iperf3 -s`')
        print(f'[{now_str()}] 运行日志文件: {self.log_path}')
        print('=' * 80)

        try:
            self.sta_shell.login()
            print(f'[{now_str()}] ADB连接成功: {self.sta_shell.serial}')
            self.resolve_iperf3_path()
            print(f'[{now_str()}] Android端iperf3命令: {self.iperf3_path}')

            if STA_FIXED_CHANNEL_WIDTH.strip():
                self.fixed_channel_width = STA_FIXED_CHANNEL_WIDTH.strip()
            else:
                self.fixed_channel_width = self.get_sta_channel_width()
            if self.fixed_channel_width != '未知':
                self.last_channel_width = self.fixed_channel_width
            print(f'[{now_str()}] 本轮固定协商频宽: {self.fixed_channel_width}')

            sta_channel, sta_rssi, sta_rx, sta_tx = self.get_sta_link_metrics()
            print(
                f'[{now_str()}] STA链路信息: '
                f'信道={sta_channel}, RSSI={sta_rssi}, RX={sta_rx}, TX={sta_tx}'
            )

            ping_result = self.run_ping_once()
            ping_large_result = self.run_ping_large_packet_once()

            tcp_up_results = []
            tcp_down_results = []
            tcp_up_bw_before = []
            tcp_up_bw_after = []
            tcp_down_bw_before = []
            tcp_down_bw_after = []

            udp_up_results = []
            udp_down_results = []
            udp_up_bw_before = []
            udp_up_bw_after = []
            udp_down_bw_before = []
            udp_down_bw_after = []

            if self.enable_tcp_test:
                for index in range(self.times):
                    print(f'\n[{now_str()}] 第{index + 1}轮TCP上行测试')
                    value, pre_bw, post_bw = self.run_once(reverse=False, udp=False)
                    tcp_up_results.append(value)
                    tcp_up_bw_before.append(pre_bw)
                    tcp_up_bw_after.append(post_bw)

                for index in range(self.times):
                    print(f'\n[{now_str()}] 第{index + 1}轮TCP下行测试')
                    value, pre_bw, post_bw = self.run_once(reverse=True, udp=False)
                    tcp_down_results.append(value)
                    tcp_down_bw_before.append(pre_bw)
                    tcp_down_bw_after.append(post_bw)

            if self.enable_udp_test:
                for index in range(self.times):
                    print(f'\n[{now_str()}] 第{index + 1}轮UDP上行测试')
                    value, pre_bw, post_bw = self.run_once(reverse=False, udp=True)
                    udp_up_results.append(value)
                    udp_up_bw_before.append(pre_bw)
                    udp_up_bw_after.append(post_bw)

                for index in range(self.times):
                    print(f'\n[{now_str()}] 第{index + 1}轮UDP下行测试')
                    value, pre_bw, post_bw = self.run_once(reverse=True, udp=True)
                    udp_down_results.append(value)
                    udp_down_bw_before.append(pre_bw)
                    udp_down_bw_after.append(post_bw)

            tcp_up_avg = average(tcp_up_results)
            tcp_down_avg = average(tcp_down_results)
            udp_up_avg = average(udp_up_results)
            udp_down_avg = average(udp_down_results)

            excel_row = [
                now_str(),
                self.sta_shell.serial,
                self.server_ip,
                self.protocol,
                self.parallel_streams,
                self.duration,
                self.ping_ip,
                self.ping_count,
                sta_channel,
                sta_rssi,
                sta_rx,
                sta_tx,
                *ping_result,
                *ping_large_result,
            ]

            if self.enable_tcp_test:
                excel_row.extend(tcp_up_results)
                excel_row.append(tcp_up_avg if tcp_up_avg is not None else '无有效数据')
                excel_row.extend(tcp_down_results)
                excel_row.append(tcp_down_avg if tcp_down_avg is not None else '无有效数据')
                excel_row.extend([v for pair in zip(tcp_up_bw_before, tcp_up_bw_after) for v in pair])
                excel_row.extend([v for pair in zip(tcp_down_bw_before, tcp_down_bw_after) for v in pair])

            if self.enable_udp_test:
                excel_row.extend(udp_up_results)
                excel_row.append(udp_up_avg if udp_up_avg is not None else '无有效数据')
                excel_row.extend(udp_down_results)
                excel_row.append(udp_down_avg if udp_down_avg is not None else '无有效数据')
                excel_row.extend([v for pair in zip(udp_up_bw_before, udp_up_bw_after) for v in pair])
                excel_row.extend([v for pair in zip(udp_down_bw_before, udp_down_bw_after) for v in pair])

            self._save_row(excel_row)

            print('\n' + '=' * 80)
            if self.enable_tcp_test:
                print(f'[{now_str()}] TCP上行结果: {tcp_up_results}')
                print(f'[{now_str()}] TCP上行平均值: {tcp_up_avg if tcp_up_avg is not None else "无有效数据"} Mbits/sec')
                print(f'[{now_str()}] TCP下行结果: {tcp_down_results}')
                print(f'[{now_str()}] TCP下行平均值: {tcp_down_avg if tcp_down_avg is not None else "无有效数据"} Mbits/sec')
                print(f'[{now_str()}] TCP上行每轮频宽(前/后): {list(zip(tcp_up_bw_before, tcp_up_bw_after))}')
                print(f'[{now_str()}] TCP下行每轮频宽(前/后): {list(zip(tcp_down_bw_before, tcp_down_bw_after))}')
            if self.enable_udp_test:
                print(f'[{now_str()}] UDP上行结果: {udp_up_results}')
                print(f'[{now_str()}] UDP上行平均值: {udp_up_avg if udp_up_avg is not None else "无有效数据"} Mbits/sec')
                print(f'[{now_str()}] UDP下行结果: {udp_down_results}')
                print(f'[{now_str()}] UDP下行平均值: {udp_down_avg if udp_down_avg is not None else "无有效数据"} Mbits/sec')
                print(f'[{now_str()}] UDP上行每轮频宽(前/后): {list(zip(udp_up_bw_before, udp_up_bw_after))}')
                print(f'[{now_str()}] UDP下行每轮频宽(前/后): {list(zip(udp_down_bw_before, udp_down_bw_after))}')
            print(f'[{now_str()}] STA链路信息: 信道={sta_channel}, RSSI={sta_rssi}, RX={sta_rx}, TX={sta_tx}')
            print(f'[{now_str()}] Ping结果: {ping_result}')
            print(f'[{now_str()}] Ping大包结果(包大小={self.ping_large_packet_size}): {ping_large_result}')
            print(f'[{now_str()}] Excel已保存: {self.excel_path}')
            print(f'[{now_str()}] 测试结束')
            print('=' * 80)

        finally:
            self.sta_shell.logout()
            self._stop_logging()


if __name__ == '__main__':
    tester = IperfAndroidManualServerTester(
        server_ip=SERVER_IP,
        ping_ip=PING_IP,
        duration=TEST_DURATION,
        times=TEST_TIMES,
        protocol=TEST_PROTOCOL,
        parallel_streams=IPERF_PARALLEL_STREAMS,
        udp_bandwidth=UDP_BANDWIDTH,
        udp_packet_len=UDP_PACKET_LEN,
        ping_count=PING_COUNT,
        ping_large_packet_size=PING_LARGE_PACKET_SIZE,
        ping_large_packet_count=PING_LARGE_PACKET_COUNT,
        serial=ADB_SERIAL,
    )
    tester.run()