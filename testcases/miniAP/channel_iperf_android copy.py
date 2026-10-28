import configparser
import time
import re
import os
import sys
import subprocess
from datetime import datetime
from time import sleep
from openpyxl.utils import get_column_letter

# Ensure project root is importable when running this script directly.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from openpyxl import Workbook
from openpyxl.styles import Alignment
from basic.telnet_demo import TelnetClient
from basic.apActions import apActions

# 读取配置文件
config_path = os.path.join(PROJECT_ROOT, 'config.ini')
cfg = configparser.ConfigParser()
cfg.read(config_path, encoding='utf-8')

# 获取AP和STA配置信息
ap_ip = cfg.get('ap_info', 'ap_ip')
ap_root = cfg.get('ap_info', 'ap_root')
ap_pwd = cfg.get('ap_info', 'ap_pwd')
ap_port = cfg.getint('ap_info', 'port') # 转换为整数类型

sta_config_section = 'sta_info' if cfg.has_section('sta_info') else 'client_info'
sta_ip = cfg.get(sta_config_section, 'sta_ip', fallback=cfg.get(sta_config_section, 'client_ip', fallback=''))
sta_sn = cfg.get(sta_config_section, 'sta_sn', fallback=cfg.get(sta_config_section, 'adb_sn', fallback='')).strip()


# ====== 测试执行参数 ======
# 测试次数配置
TEST_TIMES = 3
# 测试时间配置（单位：秒）
TEST_DURATION = 30 # 默认10秒，可修改
# UDP iperf3测试配置
ENABLE_UDP_TEST = True
UDP_BANDWIDTH = '10M' # iperf3 -b 参数，如 2M/10M/20M
UDP_PACKET_LEN = 1200 # iperf3 -l 参数
# iperf3并发流参数（-P）
IPERF_PARALLEL_STREAMS = 1
# 协议测试模式：tcp / udp / both（可在main中通过命令行参数覆盖）
TEST_PROTOCOL = 'both'
# Ping测试配置
PING_GATEWAY = "192.168.1.1" # 默认网关IP
PING_COUNT = 30 # 默认ping次数
# Ping大包测试配置
PING_LARGE_PACKET_SIZE = 1520 # ICMP负载大小（字节）
PING_LARGE_PACKET_COUNT = 30 # 大包ping次数

# ====== 测试参数配置（直接在代码中定义） ======
# 测试模式：bandwidth - 频宽遍历，channel - 信道遍历，both - 两者都遍历
TEST_MODE = 'both' # 可选: 'bandwidth', 'channel', 'both'

# 区域配置：US, EU, TH
REGION = 'US' # 可选: 'US', 'EU', 'TH'

# 信道测试时使用的频宽（当TEST_MODE='channel'时有效）
CHANNEL_TEST_BANDWIDTH = '4' # 可选: '1', '2', '4'

# 预设的测试频宽列表（用于bandwidth和both模式）
bandwidth_list = [2]

# ====== 频率表定义 =====
US_frequency_tables = {
'1': {
3: 9035, 27: 9155, 49: 9265,#5: 9045, 7: 9055, 9: 9065, 11: 9075, 13: 9085, 15: 9095,
#17: 9105, 19: 9115, 21: 9125, 23: 9135, 25: 9145, 27: 9155, 29: 9165, 31: 9175,
#33: 9185, 35: 9195, 37: 9205, 39: 9215, 41: 9225, 43: 9235, 45: 9245, 47: 9255, 49: 9265,
},
'2': {
42: 9230,
# 6: 9050, #10: 9070, 14: 9090, 18: 9110, 22: 9130,
# 26: 9150, #30: 9170, 34: 9190, 38: 9210, 42: 9230,
# 46: 9250,
},
'4': {
8: 9060, #16: 9100,
24: 9140, #32: 9180,
40: 9220, #48: 9260
},
#'8': {
# 12: 9080, 28: 9160, 44: 9240
#},
}

EU_frequency_table = {'1': {#1: 8635, 3: 8645, 5: 8655, 7: 8665, 9: 8675
    5: 8655,
     }}

TH_frequency_table = {
'1': {
37: 9205, 39: 9215, 41: 9225, 43: 9235
},
'2': {
38: 9210, 42: 9230
},
'4': {
40: 9220
}
}

frequency_tables = {
'US': US_frequency_tables,
'EU': EU_frequency_table,
'TH': TH_frequency_table
}


class TimestampLogger:
    """带时间戳的日志记录器，同时输出到控制台和文件"""

    def __init__(self, log_filename):
        self.log_filename = log_filename
        self.log_file = open(log_filename, 'w', encoding='utf-8')
        self.console = sys.stdout

    def _get_timestamp(self):
        """获取当前时间戳字符串"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # 精确到毫秒

    def write(self, message):
        """写入日志，同时输出到控制台和文件"""
        if message.strip(): # 只处理非空消息
            timestamp = self._get_timestamp()

            # 为每行消息添加时间戳
            lines = message.split('\n')
            formatted_lines = []
            for line in lines:
                if line.strip(): # 跳过空行
                    # 格式化日志行: [时间戳] 消息
                    formatted_line = f"[{timestamp}] {line}\n"
                    formatted_lines.append(formatted_line)

            formatted_message = ''.join(formatted_lines)

            # 写入文件
            self.log_file.write(formatted_message)
            self.log_file.flush()

            # 输出到控制台（带颜色格式）
            for line in lines:
                if line.strip():
                    # 控制台输出也带时间戳
                    console_line = f"\033[90m[{timestamp}]\033[0m {line}"
                    self.console.write(console_line + '\n')
        else:
            # 对于空消息，直接传递
            self.console.write(message)
            self.log_file.write(message)

    def flush(self):
        """刷新缓冲区"""
        self.log_file.flush()
        self.console.flush()

    def close(self):
        """关闭日志文件"""
        if self.log_file:
            self.log_file.close()


class AdbShellSta:
    """通过adb shell在Android STA上执行命令"""

    def __init__(self, serial=''):
        self.serial = serial
        self.connected = False

    def _run_adb(self, args, timeout=10):
        cmd = ['adb']
        if self.serial:
            cmd.extend(['-s', self.serial])
        cmd.extend(args)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            check=False
        )
        stdout = (result.stdout or '').replace('\r\n', '\n')
        stderr = (result.stderr or '').replace('\r\n', '\n')
        return result.returncode, stdout, stderr

    @staticmethod
    def _list_devices(timeout=8):
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=timeout,
            check=False
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
                raise RuntimeError(f'检测到多个ADB设备，请在config.ini中配置sta_sn: {devices}')
            else:
                raise RuntimeError('未检测到ADB设备，请检查USB连接和adb授权')

        code, stdout, stderr = self._run_adb(['get-state'], timeout=8)
        state = (stdout or stderr).strip().lower()
        if code != 0 or 'device' not in state:
            raise RuntimeError(f'ADB设备状态异常({self.serial}): {state or "unknown"}')

        self.connected = True

    def execute_command(self, command, timeout=10):
        if not self.connected:
            self.login(self.serial)

        code, stdout, stderr = self._run_adb(['shell', command], timeout=timeout)
        output = (stdout + ('\n' + stderr if stderr else '')).strip()
        if code != 0 and not output:
            raise RuntimeError(f'adb shell执行失败: {command}')
        return output

    def logout(self):
        self.connected = False


class IperfTester:
    def __init__(self, test_duration=TEST_DURATION, ping_gateway=PING_GATEWAY, ping_count=PING_COUNT,
                 ping_large_packet_size=PING_LARGE_PACKET_SIZE,
                 ping_large_packet_count=PING_LARGE_PACKET_COUNT,
                 test_protocol=TEST_PROTOCOL):
        # 初始化Telnet客户端（只初始化，不立即连接）
        self.ap_telnet = TelnetClient()
        self.sta_shell = AdbShellSta(sta_sn) # STA(Android)通过ADB控制
        self.sta_ip_for_iperf = sta_ip

        # 设置测试时间
        self.test_duration = test_duration
        # 设置ping测试参数
        self.ping_gateway = ping_gateway
        self.ping_count = ping_count
        self.ping_large_packet_size = ping_large_packet_size
        self.ping_large_packet_count = ping_large_packet_count

        # 获取测试配置
        self.test_mode = TEST_MODE
        self.region = REGION
        self.channel_test_bandwidth = CHANNEL_TEST_BANDWIDTH
        self.test_protocol = (test_protocol or 'both').strip().lower()
        if self.test_protocol not in ('tcp', 'udp', 'both'):
            print(f"无效的协议模式: {self.test_protocol}，已回退为both")
            self.test_protocol = 'both'

        self.enable_tcp_test = self.test_protocol in ('tcp', 'both')
        self.enable_udp_test = ENABLE_UDP_TEST and self.test_protocol in ('udp', 'both')

        # 获取频率表
        self.frequency_table = frequency_tables.get(self.region, US_frequency_tables)

        # 创建测试结果目录
        self.result_dir = "./test_results"
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)

        # 获取时间戳用于文件名
        timestamp = time.strftime('%Y%m%d_%H%M%S')

        # 初始化Excel文件名
        if self.test_mode == 'bandwidth':
            self.excel_filename = os.path.join(self.result_dir,
                                              f"iperf_bandwidth_test_{self.test_duration}s_{timestamp}.xlsx")
        elif self.test_mode == 'channel':
            self.excel_filename = os.path.join(self.result_dir,
                                              f"iperf_channel_test_{self.region}_{self.channel_test_bandwidth}MHz_{self.test_duration}s_{timestamp}.xlsx")
        else: # both
            self.excel_filename = os.path.join(self.result_dir,
                                              f"iperf_test_{self.region}_{self.test_duration}s_{timestamp}.xlsx")

        # 初始化日志文件名
        if self.test_mode == 'bandwidth':
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_bandwidth_test_{self.test_duration}s_{timestamp}.txt")
        elif self.test_mode == 'channel':
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_channel_test_{self.region}_{self.channel_test_bandwidth}MHz_{self.test_duration}s_{timestamp}.txt")
        else: # both
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_test_{self.region}_{self.test_duration}s_{timestamp}.txt")

        # 设置带时间戳的日志记录器
        self.logger = TimestampLogger(self.log_filename)
        sys.stdout = self.logger # 重定向标准输出到日志记录器

        # 输出初始信息
        print("=" * 80)
        print(f"测试开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试模式: {self.test_mode}")
        print(f"测试区域: {self.region}")
        print(f"测试配置: {TEST_TIMES}次测试，每次{self.test_duration}秒")
        print(f"协议模式: {self.test_protocol.upper()}")
        print(f"TCP测试: {'开启' if self.enable_tcp_test else '关闭'}")
        print(f"UDP测试: {'开启' if self.enable_udp_test else '关闭'}")
        if self.enable_udp_test:
            print(f"UDP参数: 带宽={UDP_BANDWIDTH}, 包长={UDP_PACKET_LEN} bytes")
        print(f"STA控制方式: ADB shell")
        print(f"STA设备序列号: {sta_sn if sta_sn else '未配置(自动检测)'}")
        print(f"Ping测试配置: 网关IP={self.ping_gateway}, 次数={self.ping_count}")
        print(
            f"Ping大包测试配置: 网关IP={self.ping_gateway}, 次数={self.ping_large_packet_count}, "
            f"包大小={self.ping_large_packet_size}"
        )

        if self.test_mode == 'channel':
            print(f"信道测试: 频宽={self.channel_test_bandwidth}MHz")
            available_channels = list(self.frequency_table.get(self.channel_test_bandwidth, {}).keys())
            print(f"可用信道: {available_channels}")
        elif self.test_mode == 'both':
            print(f"综合测试: 频宽列表={bandwidth_list}")

        print(f"Excel文件: {os.path.basename(self.excel_filename)}")
        print(f"日志文件: {os.path.basename(self.log_filename)}")
        print(f"日志目录: {self.result_dir}")
        print("=" * 80)

        # 初始化Excel工作簿（创建时就立即保存到文件）
        self._create_excel_file()

        print(f"Excel文件已创建: {os.path.basename(self.excel_filename)}")
        print(f"日志记录已启动: {os.path.basename(self.log_filename)}")

    def _create_excel_file(self):
        """创建Excel文件并初始化表头"""
        try:
            # 创建新的工作簿
            self.wb = Workbook()
            self.ws = self.wb.active
            self.ws.title = "吞吐量测试结果"

            # 初始化表头
            self._init_excel_header()

            # 立即保存文件
            self.wb.save(self.excel_filename)
            print("Excel文件已保存初始表头")

            # 测试数据行索引
            self.row_idx = 2

        except Exception as e:
            print(f"创建Excel文件失败: {str(e)}")
            # 恢复标准输出以便错误信息能显示在控制台
            sys.stdout = self.logger.console
            raise

    def _init_excel_header(self):
        """初始化Excel表头（根据TEST_TIMES动态创建）"""
        # 基本表头，增加了 STA RX MCS 和 STA TX MCS
        headers = [
            "测试时间", "频宽(MHz)", "AP信道",
            "AP RSSI", "AP SNR", "AP RX MCS", "AP TX MCS",
            "STA RSSI", "STA SNR", "STA RX MCS", "STA TX MCS"
        ]

        if self.enable_tcp_test:
            # 添加TCP上行测试列
            for i in range(TEST_TIMES):
                headers.append(f"上行{i + 1}(Mbits/sec)")
            headers.append("上行平均(Mbits/sec)")

            # 添加TCP下行测试列
            for i in range(TEST_TIMES):
                headers.append(f"下行{i + 1}(Mbits/sec)")
            headers.append("下行平均(Mbits/sec)")

        if self.enable_udp_test:
            # 添加UDP上行测试列
            for i in range(TEST_TIMES):
                headers.append(f"UDP上行{i + 1}(Mbits/sec)")
            headers.append("UDP上行平均吞吐(Mbits/sec)")
            headers.append("UDP上行平均丢包率(%)")
            headers.append("UDP上行平均抖动(ms)")

            # 添加UDP下行测试列
            for i in range(TEST_TIMES):
                headers.append(f"UDP下行{i + 1}(Mbits/sec)")
            headers.append("UDP下行平均吞吐(Mbits/sec)")
            headers.append("UDP下行平均丢包率(%)")
            headers.append("UDP下行平均抖动(ms)")

        # 添加Ping测试列
        headers.append("Ping丢包率(%)")
        headers.append("Ping最小延时(ms)")
        headers.append("Ping平均延时(ms)")
        headers.append("Ping最大延时(ms)")

        # 添加Ping大包测试列
        headers.append("Ping大包丢包率(%)")
        headers.append("Ping大包最小延时(ms)")
        headers.append("Ping大包平均延时(ms)")
        headers.append("Ping大包最大延时(ms)")

        # 写入表头并设置格式
        for col, header in enumerate(headers, 1):
            cell = self.ws.cell(row=1, column=col, value=header)
            cell.alignment = Alignment(horizontal='center', vertical='center')

            # 动态调整列宽
            col_letter = get_column_letter(col)
            if col <= 11: # 基本信息列（增加到11列）
                self.ws.column_dimensions[col_letter].width = 15
            else: # 测试数据列
                self.ws.column_dimensions[col_letter].width = 18

        print(f"表头创建完成，共{len(headers)}列")
        print(f" - 基本信息: 11列")
        if self.enable_tcp_test:
            print(f" - TCP测试: 上行{TEST_TIMES}次+平均值，下行{TEST_TIMES}次+平均值")
        if self.enable_udp_test:
            print(f" - UDP测试: 上行{TEST_TIMES}次+平均吞吐/丢包/抖动，下行{TEST_TIMES}次+平均吞吐/丢包/抖动")
        print(f" - Ping测试: 4列 (丢包率、最小延时、平均延时、最大延时)")
        print(f" - Ping大包测试: 4列 (丢包率、最小延时、平均延时、最大延时)")

        # 计算列索引位置（用于数据写入）
        next_col = 12

        if self.enable_tcp_test:
            self.up_start_col = next_col
            self.up_avg_col = self.up_start_col + TEST_TIMES
            self.down_start_col = self.up_avg_col + 1
            self.down_avg_col = self.down_start_col + TEST_TIMES
            next_col = self.down_avg_col + 1
        else:
            self.up_start_col = None
            self.up_avg_col = None
            self.down_start_col = None
            self.down_avg_col = None

        if self.enable_udp_test:
            self.udp_up_start_col = next_col
            self.udp_up_avg_col = self.udp_up_start_col + TEST_TIMES
            self.udp_up_loss_col = self.udp_up_avg_col + 1
            self.udp_up_jitter_col = self.udp_up_loss_col + 1
            self.udp_down_start_col = self.udp_up_jitter_col + 1
            self.udp_down_avg_col = self.udp_down_start_col + TEST_TIMES
            self.udp_down_loss_col = self.udp_down_avg_col + 1
            self.udp_down_jitter_col = self.udp_down_loss_col + 1
            next_col = self.udp_down_jitter_col + 1
        else:
            self.udp_up_start_col = None
            self.udp_up_avg_col = None
            self.udp_up_loss_col = None
            self.udp_up_jitter_col = None
            self.udp_down_start_col = None
            self.udp_down_avg_col = None
            self.udp_down_loss_col = None
            self.udp_down_jitter_col = None

        self.ping_packet_loss_col = next_col # Ping丢包率列
        self.ping_min_latency_col = self.ping_packet_loss_col + 1 # Ping最小延时列
        self.ping_avg_latency_col = self.ping_packet_loss_col + 2 # Ping平均延时列
        self.ping_max_latency_col = self.ping_packet_loss_col + 3 # Ping最大延时列
        self.ping_large_packet_loss_col = self.ping_max_latency_col + 1 # Ping大包丢包率列
        self.ping_large_min_latency_col = self.ping_max_latency_col + 2 # Ping大包最小延时列
        self.ping_large_avg_latency_col = self.ping_max_latency_col + 3 # Ping大包平均延时列
        self.ping_large_max_latency_col = self.ping_max_latency_col + 4 # Ping大包最大延时列

    def _save_row_to_excel(self, row_data):
        """将单行数据保存到Excel文件（实时保存）"""
        try:
            # 写入数据到当前行
            for col, value in enumerate(row_data, 1):
                cell = self.ws.cell(row=self.row_idx, column=col, value=value)
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # 保存到文件（实时保存）
            self.wb.save(self.excel_filename)
            print(f"测试数据已实时保存到Excel（第{self.row_idx}行）")

            # 行索引递增
            self.row_idx += 1
            return True

        except Exception as e:
            print(f"保存数据到Excel失败: {str(e)}")
            # 尝试重新保存
            try:
                self.wb.save(self.excel_filename)
                print("重试保存成功")
                return True
            except Exception as e2:
                print(f"重试保存失败: {str(e2)}")
                return False

    def _connect_ap(self):
        """连接AP设备"""
        try:
            print(f"连接到AP: {ap_ip}:{ap_port}")
            self.ap_telnet.login(ap_ip, ap_root, ap_pwd, ap_port)
            self.ap_actions = apActions(self.ap_telnet)
            return True
        except Exception as e:
            print(f"AP连接失败: {str(e)}")
            return False

    def _connect_sta(self):
        """连接STA设备（Android STA，ADB延迟连接）"""
        try:
            print(f"连接到STA(Android) ADB: {self.sta_shell.serial or 'auto'}")
            self.sta_shell.login()

            detected_ip = self._get_android_sta_ip()
            if detected_ip:
                self.sta_ip_for_iperf = detected_ip
            else:
                self.sta_ip_for_iperf = sta_ip

            print(f"STA iperf目标IP: {self.sta_ip_for_iperf}")
            return True
        except Exception as e:
            print(f"STA连接失败: {str(e)}")
            return False

    def _get_android_sta_ip(self):
        """通过ADB获取Android STA的wlan IP"""
        commands = [
            'ip -f inet addr show wlan0',
            'ifconfig wlan0',
            'getprop dhcp.wlan0.ipaddress'
        ]
        for cmd in commands:
            try:
                output = self.sta_shell.execute_command(cmd, timeout=8)
                if not output:
                    continue

                if cmd == 'getprop dhcp.wlan0.ipaddress':
                    ip = output.strip().splitlines()[-1].strip()
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
                        print(f"通过getprop获取STA IP: {ip}")
                        return ip
                    continue

                match = re.search(r'inet\s+(?:addr:)?(\d+\.\d+\.\d+\.\d+)', output)
                if match:
                    ip = match.group(1)
                    print(f"通过网络接口信息获取STA IP: {ip}")
                    return ip
            except Exception:
                continue

        print(f"未能通过ADB获取STA IP，回退使用config.ini中的sta_ip/client_ip: {sta_ip}")
        return None

    def _disconnect_devices(self):
        """断开设备连接"""
        try:
            if self.ap_telnet and hasattr(self.ap_telnet, 'tn') and self.ap_telnet.tn:
                self.ap_telnet.logout()
            if self.sta_shell and hasattr(self.sta_shell, 'logout'):
                self.sta_shell.logout()
            print("设备连接已断开")
        except Exception as e:
            print(f"断开连接时出错: {str(e)}")

    def _get_ap_channel(self):
        """获取AP当前信道（完整记录Frequency冒号后面的所有数据）"""
        try:
            output = self.ap_telnet.execute_command('cli_app show config | grep Frequency', timeout=8)
            # 匹配格式："Frequency : 9195 (35)"
            # 完整提取冒号后面的所有内容
            match = re.search(r'Frequency\s*:\s*(.+)', output)

            if match:
                channel_info = match.group(1).strip() # 获取冒号后面的完整内容并去除首尾空格
                print(f"AP信道信息: {channel_info}")
                return channel_info
            else:
                print(f"未匹配到Frequency信息，原始输出: {output}")
                return "未知"
        except Exception as e:
            print(f"获取AP信道信息失败: {str(e)}")
            return "错误"

    def _get_ap_signal_info(self):
        """获取AP的RSSI和SNR（适配实际返回格式）"""
        try:
            output = self.ap_telnet.execute_command('cli_app show signal', timeout=8)
            # 匹配格式："rssi : -55"
            rssi_match = re.search(r'rssi\s*:\s*(-?\d+)', output)
            # 匹配格式："snr : 29"
            snr_match = re.search(r'snr\s*:\s*(-?\d+)', output)

            rssi = rssi_match.group(1) if rssi_match else "未知"
            snr = snr_match.group(1) if snr_match else "未知"

            print(f"AP RSSI: {rssi} dBm, SNR: {snr} dB")
            return rssi, snr
        except Exception as e:
            print(f"获取AP信号信息失败: {str(e)}")
            return "错误", "错误"

    def _get_ap_mcs_values(self):
        """获取AP的RX和TX bit rate值（从结构化数据中提取）"""
        try:
            output = self.ap_telnet.execute_command('cli_app show sta 0', timeout=8)

            # 按行分割输出
            lines = output.strip().split('\n')

            # 查找包含数据的那一行（通常在第3行或找到包含MAC地址的行）
            data_line = None
            for line in lines:
                if len(line.split()) >= 6 and ':' in line.split()[1]: # MAC地址包含冒号
                    data_line = line
                    break

            if not data_line:
                print("未找到STA数据行")
                return "未知", "未知"

            # 使用更智能的分割方法：按2个或更多空格分割，但不分割括号内的内容
            parts = re.split(r'\s{2,}', data_line.strip())

            # 如果还是分割不正确，尝试手动提取
            if len(parts) < 6:
                # 备用方法：使用固定位置提取
                # 寻找格式：数字 MAC地址 数字 状态 TX值 RX值
                match = re.search(r'(\d+)\s+([0-9a-fA-F:]+)\s+(\d+)\s+(\w+)\s+(.+?)\s+(.+)$', data_line.strip())
                if match:
                    parts = match.groups()

            # 第5列是TX bit rate，第6列是RX bit rate
            if len(parts) >= 6:
                tx_value = parts[4] # 第5列，索引4
                rx_value = parts[5] # 第6列，索引5

                print(f"AP TX: {tx_value}, RX: {rx_value}")
                return tx_value, rx_value
            else:
                print(f"数据行格式不正确: {data_line}")
                return "未知", "未知"

        except Exception as e:
            print(f"获取AP bit rate值失败: {str(e)}")
            return "错误", "错误"

    def _get_sta_signal_info(self):
        """获取STA的RSSI和SNR（适配实际返回格式）"""
        try:
            output = self.sta_shell.execute_command('cli_app show signal', timeout=8)
            # 匹配格式："rssi : -55"
            rssi_match = re.search(r'rssi\s*:\s*(-?\d+)', output)
            # 匹配格式："snr : 29"
            snr_match = re.search(r'snr\s*:\s*(-?\d+)', output)

            rssi = rssi_match.group(1) if rssi_match else "未知"
            snr = snr_match.group(1) if snr_match else "未知"

            print(f"STA RSSI: {rssi} dBm, SNR: {snr} dB")
            return rssi, snr
        except Exception as e:
            print(f"获取STA信号信息失败: {str(e)}")
            return "错误", "错误"

    def _get_sta_mcs_values(self):
        """获取STA的RX和TX bit rate值（从表格格式中提取）"""
        try:
            output = self.sta_shell.execute_command('cli_app show ap 0', timeout=8)

            print(f"cli_app show ap 0 原始输出:\n{output}")

            # 按行分割输出
            lines = output.strip().split('\n')

            # 查找包含数据的那一行（查找包含MAC地址的行）
            data_line = None
            for line in lines:
                # 匹配格式：MAC地址（XX:XX:XX:XX:XX:XX）后面跟有数据
                if re.search(r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', line):
                    # 过滤掉表头行
                    if 'BSSID' not in line and '===' not in line:
                        data_line = line.strip()
                        break

            if not data_line:
                print("未找到STA数据行")
                return "未知", "未知"

            print(f"找到的数据行: {data_line}")

            # 使用正则表达式直接提取 TX bit rate 和 RX bit rate
            # 匹配格式: 数字.MBits/s(MCS 数字) 或 数字MBit/s(MCS 数字)
            # 例如: 3.00MBit/s(MCS 7)
            pattern = r'(\d+\.?\d*MBit/s\(MCS\s*\d+\))'

            # 查找所有匹配项
            matches = re.findall(pattern, data_line)

            if len(matches) >= 2:
                tx_value = matches[0]  # TX bit rate
                rx_value = matches[1]  # RX bit rate
                print(f"STA TX: {tx_value}, RX: {rx_value}")
                return tx_value, rx_value
            elif len(matches) == 1:
                # 如果只匹配到一个，可能是格式问题，尝试另一种方法
                print(f"只匹配到一个值: {matches[0]}")
                # 尝试匹配包含MCS的内容
                all_mcs = re.findall(r'[\d\.]+MBit/s\(MCS\s*\d+\)', data_line)
                if len(all_mcs) >= 2:
                    tx_value = all_mcs[0]
                    rx_value = all_mcs[1]
                    print(f"STA TX (备用): {tx_value}, RX: {rx_value}")
                    return tx_value, rx_value

            # 如果正则表达式匹配失败，尝试手动解析
            # 按空格分割，然后重新组合包含括号的部分
            parts = data_line.split()
            tx_value = "未知"
            rx_value = "未知"

            # 查找包含 "MBit/s" 的字段并组合
            mcs_parts = []
            i = 0
            while i < len(parts):
                if 'MBit/s' in parts[i]:
                    # 开始收集，直到遇到包含 ')' 的部分
                    part_collector = parts[i]
                    i += 1
                    while i < len(parts) and ')' not in part_collector:
                        part_collector += ' ' + parts[i]
                        i += 1
                    mcs_parts.append(part_collector)
                else:
                    i += 1

            if len(mcs_parts) >= 2:
                tx_value = mcs_parts[0]
                rx_value = mcs_parts[1]
                print(f"STA TX (手动组合): {tx_value}, RX: {rx_value}")
                return tx_value, rx_value

            print(f"无法解析STA MCS值，数据行: {data_line}")
            return "未知", "未知"

        except Exception as e:
            print(f"获取STA MCS值失败: {str(e)}")
            return "错误", "错误"

    def _extract_udp_metrics(self, output):
        """从iperf3 UDP输出中提取丢包率(%)和抖动(ms)"""
        lines = output.split('\n')
        for line in lines:
            if 'receiver' not in line or 'bits/sec' not in line:
                continue

            # 典型格式: ... 1.09 Mbits/sec 0.041 ms 0/783 (0%) receiver
            match = re.search(
                r'bits/sec\s+([\d\.]+)\s+ms\s+\d+/\d+\s+\(([\d\.]+)%\)\s+receiver',
                line,
                re.IGNORECASE
            )
            if match:
                return match.group(2), match.group(1)

        # 备用匹配（跨行）
        fallback = re.search(
            r'bits/sec\s+([\d\.]+)\s+ms\s+\d+/\d+\s+\(([\d\.]+)%\).*?receiver',
            output,
            re.IGNORECASE | re.DOTALL
        )
        if fallback:
            return fallback.group(2), fallback.group(1)

        return "未匹配到数据", "未匹配到数据"

    def _run_iperf_test(self, reverse=False, udp=False):
        """
        运行iperf测试（AP侧Telnet执行客户端命令，STA侧ADB执行server命令）
        reverse: True表示上行流(-R), False表示下行流
        提取receiver行的Bandwidth值作为测试结果
        udp: True表示UDP测试
        """
        protocol = "UDP" if udp else "TCP"
        test_type = f"{protocol}{'上行' if reverse else '下行'}"
        try:
            # ===== 1. 确保STA端iperf服务器处于运行状态 =====
            print("检查并重启STA端iperf服务器...")
            # 先停止STA端可能存在的iperf进程（失败时仅告警，不中断后续测试）
            try:
                self.sta_shell.execute_command('pkill -f iperf', timeout=5)
            except Exception as e:
                print(f"告警: 停止STA端iperf进程失败，继续执行: {str(e)}")
            time.sleep(2)
            # 启动STA端iperf3服务器（后台运行）
            try:
                self.sta_shell.execute_command('/data/local/tmp/iperf3 -s &', timeout=5)
            except Exception as e:
                print(f"告警: 启动STA端iperf3服务器失败，继续执行: {str(e)}")
            time.sleep(2) # 等待服务器启动完成

            # ===== 2. 在AP端执行iperf3客户端命令 =====
            sta_target_ip = self.sta_ip_for_iperf
            parallel_arg = f'-P {IPERF_PARALLEL_STREAMS}' if IPERF_PARALLEL_STREAMS and IPERF_PARALLEL_STREAMS > 1 else ''
            # 构造iperf3命令（-R 上行流，无-R 下行流）
            if udp:
                cmd = (
                    f'iperf3 -c {sta_target_ip} -u -b {UDP_BANDWIDTH} -l {UDP_PACKET_LEN} '
                    f'-t {self.test_duration} -i 1 {parallel_arg} {"-R" if reverse else ""}'
                )
            else:
                cmd = f'iperf3 -c {sta_target_ip} -t {self.test_duration} -i 1 {parallel_arg} {"-R" if reverse else ""}'
            cmd = ' '.join(cmd.split())
            print(f"在AP端执行{test_type}测试命令: {cmd}")

            # 执行命令（超时设为测试时间+15秒缓冲）
            timeout = self.test_duration + 15
            output = self.ap_telnet.execute_command(cmd, timeout=timeout)
            if not output:
                print(f"{test_type}测试无输出内容")
                return ("无输出", "无输出", "无输出") if udp else "无输出"

            # 调试输出
            print(f"iperf原始输出:\n{output}")

            # ===== 3. 匹配receiver行的Bandwidth值 =====
            # 改进匹配逻辑，更灵活地匹配receiver行
            lines = output.split('\n')
            receiver_throughput = None

            for line in lines:
                if 'receiver' in line and 'Bandwidth' not in line:
                    # 匹配格式: [ 4] 0.00-30.00 sec 2.18 MBytes 609 Kbits/sec receiver
                    # 或者: [ 4] 0.00-30.00 sec 2.18 MBytes 609 Kbits/sec receiver
                    match = re.search(r'(\d+(?:\.\d+)?)\s+(M|K|G)bits/sec\s+receiver', line)
                    if match:
                        throughput_value = float(match.group(1))
                        unit = match.group(2)

                        # 统一转换为 Mbit/sec
                        if unit == 'K':
                            throughput = round(throughput_value / 1000, 3)
                        elif unit == 'G':
                            throughput = round(throughput_value * 1000, 3)
                        else: # M
                            throughput = throughput_value

                        receiver_throughput = throughput
                        print(f"{test_type}吞吐量(receiver): {throughput} Mbits/sec (原始值: {throughput_value} {unit}bits/sec)")
                        break

            if receiver_throughput is not None:
                throughput_str = str(receiver_throughput)
                if udp:
                    udp_loss, udp_jitter = self._extract_udp_metrics(output)
                    print(f"{test_type}UDP指标: 丢包率={udp_loss}%, 抖动={udp_jitter} ms")
                    return throughput_str, udp_loss, udp_jitter
                return throughput_str

            # 备用匹配：尝试匹配更通用的模式
            match = re.search(r'receiver.*?(\d+(?:\.\d+)?)\s+(M|K|G)bits/sec', output, re.DOTALL | re.IGNORECASE)
            if not match:
                # 最后的尝试：直接查找包含"bits/sec"的receiver行
                match = re.search(r'(\d+(?:\.\d+)?)\s+(M|K|G)bits/sec.*?receiver', output, re.IGNORECASE)

            if match:
                throughput_value = float(match.group(1))
                unit = match.group(2).upper()

                if unit == 'K':
                    throughput = round(throughput_value / 1000, 3)
                elif unit == 'G':
                    throughput = round(throughput_value * 1000, 3)
                else:
                    throughput = throughput_value

                print(f"{test_type}吞吐量(receiver备用匹配): {throughput} Mbits/sec")
                throughput_str = str(throughput)
                if udp:
                    udp_loss, udp_jitter = self._extract_udp_metrics(output)
                    print(f"{test_type}UDP指标: 丢包率={udp_loss}%, 抖动={udp_jitter} ms")
                    return throughput_str, udp_loss, udp_jitter
                return throughput_str
            else:
                print(f"未匹配到{test_type}吞吐量receiver值，原始输出:\n{output}")
                # 尝试打印所有包含receiver的行以便调试
                print("包含'receiver'的行:")
                for line in lines:
                    if 'receiver' in line:
                        print(f"  {line}")
                if udp:
                    return "未匹配到数据", "未匹配到数据", "未匹配到数据"
                return "未匹配到数据"

        except Exception as e:
            print(f"{test_type}测试失败: {str(e)}")
            return ("错误", "错误", "错误") if udp else "错误"

    def _run_ping_test(self):
        """
        在STA端执行ping测试
        返回: (丢包率%, 最小延时ms, 平均延时ms, 最大延时ms)
        """
        try:
            # 先停止STA端可能存在的iperf进程
            self.sta_shell.execute_command('pkill -f iperf', timeout=5)
            time.sleep(2)
            print(f"开始Ping测试: 目标={self.ping_gateway}, 次数={self.ping_count}")

            # Android不同版本/ROM的ping位置可能不同，按顺序回退
            ping_commands = [
                f'ping -c {self.ping_count} {self.ping_gateway}',
                f'/system/bin/ping -c {self.ping_count} {self.ping_gateway}',
                f'toybox ping -c {self.ping_count} {self.ping_gateway}'
            ]

            output = ""
            last_error = ""
            for cmd in ping_commands:
                try:
                    print(f"尝试Ping命令: {cmd}")
                    output = self.sta_shell.execute_command(cmd, timeout=self.ping_count * 2 + 8)
                    # 命令返回文本里包含明显错误时继续尝试下一条
                    if re.search(r'not found|unknown command|inaccessible|permission denied', output, re.IGNORECASE):
                        last_error = output
                        continue
                    break
                except Exception as e:
                    last_error = str(e)
                    continue

            if not output:
                print(f"Ping命令执行失败，最后错误: {last_error}")
                return "测试失败", "测试失败", "测试失败", "测试失败"

            if not output:
                print("Ping测试无输出内容")
                return "无输出", "无输出", "无输出", "无输出"

            # 输出ping结果到日志
            print(f"Ping测试结果:\n{output}")

            # 解析ping结果
            # 匹配格式: 10 packets transmitted, 10 packets received, 0% packet loss
            packet_loss_match = re.search(r'(\d+(?:\.\d+)?)%\s*packet loss', output, re.IGNORECASE)

            # 兼容格式:
            # round-trip min/avg/max = a/b/c ms
            # rtt min/avg/max/mdev = a/b/c/d ms
            latency_match = re.search(
                r'(?:round-trip|rtt)\s+min/avg/max(?:/[a-z]+)?\s*=\s*([\d\.]+)/([\d\.]+)/([\d\.]+)(?:/[\d\.]+)?\s*ms',
                output,
                re.IGNORECASE
            )

            if packet_loss_match and latency_match:
                packet_loss = packet_loss_match.group(1)
                min_latency = latency_match.group(1)
                avg_latency = latency_match.group(2)
                max_latency = latency_match.group(3)

                print(f"Ping测试解析结果:")
                print(f" 丢包率: {packet_loss}%")
                print(f" 最小延时: {min_latency} ms")
                print(f" 平均延时: {avg_latency} ms")
                print(f" 最大延时: {max_latency} ms")

                return packet_loss, min_latency, avg_latency, max_latency
            else:
                print("未匹配到Ping测试结果")
                print(f"原始输出:\n{output}")
                return "解析失败", "解析失败", "解析失败", "解析失败"

        except Exception as e:
            print(f"Ping测试失败: {str(e)}")
            return "测试失败", "测试失败", "测试失败", "测试失败"

    def _run_ping_large_packet_test(self):
        """
        在STA端执行ping大包测试
        返回: (丢包率%, 最小延时ms, 平均延时ms, 最大延时ms)
        """
        try:
            print(
                f"开始Ping大包测试: 目标={self.ping_gateway}, 次数={self.ping_large_packet_count}, "
                f"包大小={self.ping_large_packet_size}"
            )

            # Android不同版本/ROM的ping位置可能不同，按顺序回退
            ping_commands = [
                f'ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_gateway}',
                f'/system/bin/ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_gateway}',
                f'toybox ping -c {self.ping_large_packet_count} -s {self.ping_large_packet_size} {self.ping_gateway}'
            ]

            output = ""
            last_error = ""
            for cmd in ping_commands:
                try:
                    print(f"尝试Ping大包命令: {cmd}")
                    output = self.sta_shell.execute_command(cmd, timeout=self.ping_large_packet_count * 2 + 8)
                    if re.search(r'not found|unknown command|inaccessible|permission denied', output, re.IGNORECASE):
                        last_error = output
                        continue
                    break
                except Exception as e:
                    last_error = str(e)
                    continue

            if not output:
                print(f"Ping大包命令执行失败，最后错误: {last_error}")
                return "测试失败", "测试失败", "测试失败", "测试失败"

            if not output:
                print("Ping大包测试无输出内容")
                return "无输出", "无输出", "无输出", "无输出"

            print(f"Ping大包测试结果:\n{output}")

            packet_loss_match = re.search(r'(\d+(?:\.\d+)?)%\s*packet loss', output, re.IGNORECASE)
            latency_match = re.search(
                r'(?:round-trip|rtt)\s+min/avg/max(?:/[a-z]+)?\s*=\s*([\d\.]+)/([\d\.]+)/([\d\.]+)(?:/[\d\.]+)?\s*ms',
                output,
                re.IGNORECASE
            )

            if packet_loss_match and latency_match:
                packet_loss = packet_loss_match.group(1)
                min_latency = latency_match.group(1)
                avg_latency = latency_match.group(2)
                max_latency = latency_match.group(3)

                print(f"Ping大包测试解析结果:")
                print(f" 丢包率: {packet_loss}%")
                print(f" 最小延时: {min_latency} ms")
                print(f" 平均延时: {avg_latency} ms")
                print(f" 最大延时: {max_latency} ms")

                return packet_loss, min_latency, avg_latency, max_latency

            print("未匹配到Ping大包测试结果")
            print(f"原始输出:\n{output}")
            return "解析失败", "解析失败", "解析失败", "解析失败"

        except Exception as e:
            print(f"Ping大包测试失败: {str(e)}")
            return "测试失败", "测试失败", "测试失败", "测试失败"

    def _calculate_average(self, data_list):
        """计算平均值（过滤非数字值）"""
        try:
            # 过滤掉非数字的结果
            valid_data = []
            for data in data_list:
                try:
                    valid_data.append(float(data))
                except (ValueError, TypeError):
                    continue

            if not valid_data:
                return "无有效数据"

            average = round(sum(valid_data) / len(valid_data), 3)
            return str(average)
        except Exception as e:
            print(f"计算平均值失败: {str(e)}")
            return "计算错误"

    def _calculate_ping_metrics_average(self, metrics_list):
        """计算Ping四项指标的平均值（丢包率、最小/平均/最大延时）"""
        try:
            if not metrics_list:
                return "无有效数据", "无有效数据", "无有效数据", "无有效数据"

            averages = []
            for idx in range(4):
                values = []
                for metrics in metrics_list:
                    try:
                        values.append(float(metrics[idx]))
                    except (ValueError, TypeError, IndexError):
                        continue

                if values:
                    averages.append(str(round(sum(values) / len(values), 3)))
                else:
                    averages.append("无有效数据")

            return tuple(averages)
        except Exception as e:
            print(f"计算Ping平均值失败: {str(e)}")
            return "计算错误", "计算错误", "计算错误", "计算错误"

    def _calculate_udp_metrics_average(self, metrics_list):
        """计算UDP指标平均值（吞吐、丢包率、抖动）"""
        try:
            if not metrics_list:
                return "无有效数据", "无有效数据", "无有效数据"

            throughput_list = []
            loss_list = []
            jitter_list = []
            for metrics in metrics_list:
                if not isinstance(metrics, (tuple, list)) or len(metrics) < 3:
                    continue
                throughput_list.append(metrics[0])
                loss_list.append(metrics[1])
                jitter_list.append(metrics[2])

            return (
                self._calculate_average(throughput_list),
                self._calculate_average(loss_list),
                self._calculate_average(jitter_list)
            )
        except Exception as e:
            print(f"计算UDP平均值失败: {str(e)}")
            return "计算错误", "计算错误", "计算错误"

    def _run_single_test(self, bandwidth, channel=None):
        """执行单个测试配置（频宽和信道）"""
        try:
            # # 设置AP频宽和信道
            # if channel is not None:
            #     print(f"\n设置AP频宽为{bandwidth}MHz, 信道{channel}")
            #     self.ap_actions.set_bandwidth_channel(bandwidth, channel)
            # else:
            #     print(f"\n设置AP频宽为{bandwidth}MHz")
            #     self.ap_actions.set_bandwidth(bandwidth)

            # time.sleep(30) # 等待设置生效

            # 连接STA
            print("AP设置完成，开始连接STA...")
            if not self._connect_sta():
                print("STA连接失败，跳过当前测试")
                if hasattr(self.sta_shell, 'logout'):
                    self.sta_shell.logout()
                return False

            # 收集AP信息
            ap_channel = self._get_ap_channel()
            time.sleep(2)
            ap_rssi, ap_snr = self._get_ap_signal_info()
            time.sleep(2)
            ap_rx_mcs, ap_tx_mcs = self._get_ap_mcs_values()
            time.sleep(2)

            # 收集STA信息
            sta_rssi, sta_snr = self._get_sta_signal_info()
            time.sleep(2)
            sta_rx_mcs, sta_tx_mcs = self._get_sta_mcs_values()
            time.sleep(2)

            # 创建初始数据行（修改为11个基本信息）
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            initial_data = [
                current_time, bandwidth, ap_channel,
                ap_rssi, ap_snr, ap_rx_mcs, ap_tx_mcs,
                sta_rssi, sta_snr, sta_rx_mcs, sta_tx_mcs
            ]

            if self.enable_tcp_test:
                # 添加TCP上行占位符
                for i in range(TEST_TIMES + 1):
                    initial_data.append("")

                # 添加TCP下行占位符
                for i in range(TEST_TIMES + 1):
                    initial_data.append("")

            if self.enable_udp_test:
                # 添加UDP上行占位符
                for i in range(TEST_TIMES + 1):
                    initial_data.append("")
                # UDP上行平均丢包/抖动占位符
                initial_data.append("")
                initial_data.append("")

                # 添加UDP下行占位符
                for i in range(TEST_TIMES + 1):
                    initial_data.append("")
                # UDP下行平均丢包/抖动占位符
                initial_data.append("")
                initial_data.append("")

            # 添加Ping测试占位符
            for i in range(4):
                initial_data.append("")

            # 添加Ping大包测试占位符
            for i in range(4):
                initial_data.append("")

            # 保存初始数据到Excel
            if not self._save_row_to_excel(initial_data):
                print("初始数据保存失败，继续测试...")

            # 运行TCP上行吞吐量测试
            up_results = []
            down_results = []
            up_average = "未启用"
            down_average = "未启用"

            if self.enable_tcp_test:
                for i in range(TEST_TIMES):
                    print(f"\n开始上行测试第{i + 1}次")
                    up_result = self._run_iperf_test(reverse=True)
                    up_results.append(up_result)

                    # 实时更新上行测试结果到Excel
                    try:
                        self.ws.cell(row=self.row_idx - 1, column=self.up_start_col + i, value=up_result)
                        self.wb.save(self.excel_filename)
                        print(f"上行第{i + 1}次结果已更新到Excel")
                    except Exception as e:
                        print(f"更新上行结果到Excel失败: {str(e)}")

                    time.sleep(5)

                # 计算上行平均值并更新Excel
                up_average = self._calculate_average(up_results)
                try:
                    self.ws.cell(row=self.row_idx - 1, column=self.up_avg_col, value=up_average)
                    self.wb.save(self.excel_filename)
                    print("上行平均值已更新到Excel")
                except Exception as e:
                    print(f"更新上行平均值到Excel失败: {str(e)}")

            # 运行TCP下行吞吐量测试
            down_results = []
            if self.enable_tcp_test:
                for i in range(TEST_TIMES):
                    print(f"\n开始下行测试第{i + 1}次")
                    down_result = self._run_iperf_test(reverse=False)
                    down_results.append(down_result)

                    # 实时更新下行测试结果到Excel
                    try:
                        self.ws.cell(row=self.row_idx - 1, column=self.down_start_col + i, value=down_result)
                        self.wb.save(self.excel_filename)
                        print(f"下行第{i + 1}次结果已更新到Excel")
                    except Exception as e:
                        print(f"更新下行结果到Excel失败: {str(e)}")

                    time.sleep(5)

                # 计算下行平均值并更新Excel
                down_average = self._calculate_average(down_results)
                try:
                    self.ws.cell(row=self.row_idx - 1, column=self.down_avg_col, value=down_average)
                    self.wb.save(self.excel_filename)
                    print("下行平均值已更新到Excel")
                except Exception as e:
                    print(f"更新下行平均值到Excel失败: {str(e)}")

            udp_up_results = []
            udp_down_results = []
            udp_up_average = "未启用"
            udp_down_average = "未启用"
            udp_up_loss_avg = "未启用"
            udp_up_jitter_avg = "未启用"
            udp_down_loss_avg = "未启用"
            udp_down_jitter_avg = "未启用"

            if self.enable_udp_test:
                # 运行UDP上行吞吐量测试
                for i in range(TEST_TIMES):
                    print(f"\n开始UDP上行测试第{i + 1}次")
                    udp_up_throughput, udp_up_loss, udp_up_jitter = self._run_iperf_test(reverse=True, udp=True)
                    udp_up_results.append((udp_up_throughput, udp_up_loss, udp_up_jitter))

                    try:
                        self.ws.cell(row=self.row_idx - 1, column=self.udp_up_start_col + i, value=udp_up_throughput)
                        self.wb.save(self.excel_filename)
                        print(f"UDP上行第{i + 1}次结果已更新到Excel")
                    except Exception as e:
                        print(f"更新UDP上行结果到Excel失败: {str(e)}")

                    time.sleep(3)

                udp_up_average, udp_up_loss_avg, udp_up_jitter_avg = self._calculate_udp_metrics_average(udp_up_results)
                try:
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_up_avg_col, value=udp_up_average)
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_up_loss_col, value=udp_up_loss_avg)
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_up_jitter_col, value=udp_up_jitter_avg)
                    self.wb.save(self.excel_filename)
                    print("UDP上行平均吞吐/丢包/抖动已更新到Excel")
                except Exception as e:
                    print(f"更新UDP上行平均指标到Excel失败: {str(e)}")

                # 运行UDP下行吞吐量测试
                for i in range(TEST_TIMES):
                    print(f"\n开始UDP下行测试第{i + 1}次")
                    udp_down_throughput, udp_down_loss, udp_down_jitter = self._run_iperf_test(reverse=False, udp=True)
                    udp_down_results.append((udp_down_throughput, udp_down_loss, udp_down_jitter))

                    try:
                        self.ws.cell(row=self.row_idx - 1, column=self.udp_down_start_col + i, value=udp_down_throughput)
                        self.wb.save(self.excel_filename)
                        print(f"UDP下行第{i + 1}次结果已更新到Excel")
                    except Exception as e:
                        print(f"更新UDP下行结果到Excel失败: {str(e)}")

                    time.sleep(3)

                udp_down_average, udp_down_loss_avg, udp_down_jitter_avg = self._calculate_udp_metrics_average(udp_down_results)
                try:
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_down_avg_col, value=udp_down_average)
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_down_loss_col, value=udp_down_loss_avg)
                    self.ws.cell(row=self.row_idx - 1, column=self.udp_down_jitter_col, value=udp_down_jitter_avg)
                    self.wb.save(self.excel_filename)
                    print("UDP下行平均吞吐/丢包/抖动已更新到Excel")
                except Exception as e:
                    print(f"更新UDP下行平均指标到Excel失败: {str(e)}")

            # 运行Ping测试（多轮并取均值）
            print(f"\n开始Ping测试，共{TEST_TIMES}轮...")
            ping_results = []
            for i in range(TEST_TIMES):
                print(f"Ping测试第{i + 1}轮")
                ping_results.append(self._run_ping_test())
                time.sleep(2)

            packet_loss, min_latency, avg_latency, max_latency = self._calculate_ping_metrics_average(ping_results)
            print(
                f"Ping测试均值结果: 丢包率={packet_loss}%, "
                f"延时={min_latency}/{avg_latency}/{max_latency} ms"
            )

            # 更新Ping测试结果到Excel
            try:
                self.ws.cell(row=self.row_idx - 1, column=self.ping_packet_loss_col, value=packet_loss)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_min_latency_col, value=min_latency)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_avg_latency_col, value=avg_latency)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_max_latency_col, value=max_latency)
                self.wb.save(self.excel_filename)
                print("Ping测试结果已更新到Excel")
            except Exception as e:
                print(f"更新Ping测试结果到Excel失败: {str(e)}")

            # 运行Ping大包测试（多轮并取均值）
            print(f"\n开始Ping大包测试，共{TEST_TIMES}轮...")
            ping_large_results = []
            for i in range(TEST_TIMES):
                print(f"Ping大包测试第{i + 1}轮")
                ping_large_results.append(self._run_ping_large_packet_test())
                time.sleep(2)

            large_packet_loss, large_min_latency, large_avg_latency, large_max_latency = \
                self._calculate_ping_metrics_average(ping_large_results)
            print(
                f"Ping大包测试均值结果: 丢包率={large_packet_loss}%, "
                f"延时={large_min_latency}/{large_avg_latency}/{large_max_latency} ms"
            )

            # 更新Ping大包测试结果到Excel
            try:
                self.ws.cell(row=self.row_idx - 1, column=self.ping_large_packet_loss_col, value=large_packet_loss)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_large_min_latency_col, value=large_min_latency)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_large_avg_latency_col, value=large_avg_latency)
                self.ws.cell(row=self.row_idx - 1, column=self.ping_large_max_latency_col, value=large_max_latency)
                self.wb.save(self.excel_filename)
                print("Ping大包测试结果已更新到Excel")
            except Exception as e:
                print(f"更新Ping大包测试结果到Excel失败: {str(e)}")

            # 打印测试结果汇总
            print(f"\n测试结果汇总:")
            if channel is not None:
                print(f" 频宽: {bandwidth}MHz, 信道: {channel}")
            else:
                print(f" 频宽: {bandwidth}MHz")
            print(f" AP信息: RSSI={ap_rssi}dBm, SNR={ap_snr}dB, RX MCS={ap_rx_mcs}, TX MCS={ap_tx_mcs}")
            print(f" STA信息: RSSI={sta_rssi}dBm, SNR={sta_snr}dB, RX MCS={sta_rx_mcs}, TX MCS={sta_tx_mcs}")
            if self.enable_tcp_test:
                print(f" 上行测试结果: {up_results}, 平均值: {up_average} Mbits/sec")
                print(f" 下行测试结果: {down_results}, 平均值: {down_average} Mbits/sec")
            if self.enable_udp_test:
                print(
                    f" UDP上行测试结果: {udp_up_results}, 平均吞吐: {udp_up_average} Mbits/sec, "
                    f"平均丢包率: {udp_up_loss_avg}%, 平均抖动: {udp_up_jitter_avg} ms"
                )
                print(
                    f" UDP下行测试结果: {udp_down_results}, 平均吞吐: {udp_down_average} Mbits/sec, "
                    f"平均丢包率: {udp_down_loss_avg}%, 平均抖动: {udp_down_jitter_avg} ms"
                )
            print(f" Ping测试结果: 丢包率={packet_loss}%, 延时={min_latency}/{avg_latency}/{max_latency} ms")
            print(
                f" Ping大包测试结果(包大小={self.ping_large_packet_size}): "
                f"丢包率={large_packet_loss}%, 延时={large_min_latency}/{large_avg_latency}/{large_max_latency} ms"
            )
            print(f" 数据已实时保存到: {os.path.basename(self.excel_filename)}")

            # 断开STA连接
            print("本次测试完成，断开STA连接...")
            if hasattr(self.sta_shell, 'logout'):
                self.sta_shell.logout()
            print("STA连接已断开")

            return True

        except Exception as e:
            print(f"单次测试失败: {str(e)}")
            return False

    def run_test(self):
        """运行完整测试流程"""
        try:
            # 第一步：先连接AP
            if not self._connect_ap():
                print("AP连接失败，测试中止")
                return

            # 根据测试模式执行不同的测试
            if self.test_mode == 'bandwidth':
                # 频宽遍历测试
                print(f"\n{'=' * 40}")
                print(f"开始频宽遍历测试")
                print(f"测试频宽: {bandwidth_list}")
                print('=' * 40)

                for bandwidth in bandwidth_list:
                    self._run_single_test(bandwidth)

            elif self.test_mode == 'channel':
                # 信道遍历测试
                print(f"\n{'=' * 40}")
                print(f"开始信道遍历测试")
                print(f"区域: {self.region}, 频宽: {self.channel_test_bandwidth}MHz")
                print('=' * 40)

                # 获取该频宽下的所有信道
                channels = self.frequency_table.get(self.channel_test_bandwidth, {})
                if not channels:
                    print(f"区域{self.region}的{self.channel_test_bandwidth}MHz频宽下无可用信道")
                    return

                print(f"可用信道数: {len(channels)}")

                for channel in channels.keys():
                    self._run_single_test(int(self.channel_test_bandwidth), channel)

            elif self.test_mode == 'both':
                # 综合测试：先遍历频宽，在每个频宽下遍历信道
                print(f"\n{'=' * 40}")
                print(f"开始综合测试")
                print(f"区域: {self.region}")
                print(f"测试频宽: {bandwidth_list}")
                print('=' * 40)

                for bandwidth in bandwidth_list:
                    # 获取该频宽下的所有信道
                    channels = self.frequency_table.get(str(bandwidth), {})
                    if not channels:
                        print(f"区域{self.region}的{bandwidth}MHz频宽下无可用信道，跳过")
                        continue

                    print(f"\n{'=' * 30}")
                    print(f"频宽: {bandwidth}MHz, 可用信道数: {len(channels)}")
                    print('=' * 30)

                    for channel in channels.keys():
                        self._run_single_test(bandwidth, channel)

            else:
                print(f"未知的测试模式: {self.test_mode}，请使用 'bandwidth', 'channel' 或 'both'")
                return

            print("=" * 80)
            print(f"测试结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"所有测试完成！")
            print(f"测试结果已保存到: {os.path.basename(self.excel_filename)}")
            print(f"运行日志已保存到: {os.path.basename(self.log_filename)}")
            print(f"文件位置: {self.result_dir}")
            print("=" * 80)

        except Exception as e:
            print(f"测试过程中发生错误: {str(e)}")
            print(f"已保存的数据可在文件中查看:")
            print(f" - Excel文件: {os.path.basename(self.excel_filename)}")
            print(f" - 日志文件: {os.path.basename(self.log_filename)}")
        finally:
            # 确保断开所有连接
            self._disconnect_devices()
            # 关闭日志记录器
            if hasattr(self, 'logger'):
                self.logger.close()
                # 恢复标准输出
                sys.stdout = self.logger.console


def main():
    """主入口：支持命令行指定协议模式 tcp/udp/both"""
    protocol = TEST_PROTOCOL
    if len(sys.argv) > 1:
        protocol = sys.argv[1].strip().lower()

    print(f"启动协议模式: {protocol}")

    tester = IperfTester(
        test_duration=TEST_DURATION,
        ping_gateway=PING_GATEWAY,
        ping_count=PING_COUNT,
        ping_large_packet_size=PING_LARGE_PACKET_SIZE,
        ping_large_packet_count=PING_LARGE_PACKET_COUNT,
        test_protocol=protocol
    )
    tester.run_test()


if __name__ == '__main__':
    main()