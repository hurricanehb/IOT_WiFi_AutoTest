import configparser
import time
import re
import os
import sys
from datetime import datetime
from time import sleep

from openpyxl import Workbook
from openpyxl.styles import Alignment
from basic.telnet_demo import TelnetClient
from basic.apActions import apActions
from basic.clientActions import clientActions

# 读取配置文件
config_path = '../config.ini'
cfg = configparser.ConfigParser()
cfg.read(config_path, encoding='utf-8')

# 获取AP和Client配置信息
# ap_ip = cfg.get('ap_info', 'ap_ip')
# ap_root = cfg.get('ap_info', 'ap_root')
# ap_pwd = cfg.get('ap_info', 'ap_pwd')
# ap_port = cfg.getint('ap_info', 'port') # 转换为整数类型

# client_ip = cfg.get('client_info', 'client_ip')
# client_root = cfg.get('client_info', 'client_root')
# client_pwd = cfg.get('client_info', 'client_pwd')
# client_port = cfg.getint('client_info', 'port') # 转换为整数类型


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

# ====== 测试参数配置（直接在代码中定义） ======
# 测试模式：bandwidth - 频宽遍历，channel - 信道遍历，both - 两者都遍历
TEST_MODE = 'both' # 可选: 'bandwidth', 'channel', 'both'

# 区域配置：US, EU, TH
REGION = 'US' # 可选: 'US', 'EU', 'TH'

# 信道测试时使用的频宽（当TEST_MODE='channel'时有效）
CHANNEL_TEST_BANDWIDTH = '2' # 可选: '1', '2', '4'

# 预设的测试频宽列表（用于bandwidth和both模式）
bandwidth_list = [2]

# ====== 频率表定义 =====
US_frequency_tables = {
'1': {
27: 9155
# 3: 9035, 27: 9155, 49: 9265,#5: 9045, 7: 9055, 9: 9065, 11: 9075, 13: 9085, 15: 9095,
# #17: 9105, 19: 9115, 21: 9125, 23: 9135, 25: 9145, 27: 9155, 29: 9165, 31: 9175,
# #33: 9185, 35: 9195, 37: 9205, 39: 9215, 41: 9225, 43: 9235, 45: 9245, 47: 9255, 49: 9265,
},
'2': {
26: 9150
# 6: 9050, #10: 9070, 14: 9090, 18: 9110, 22: 9130,
# 26: 9150, #30: 9170, 34: 9190, 38: 9210, 42: 9230,
# 46: 9250,
},
'4': {
# 8: 9060, #16: 9100,
24: 9140, #32: 9180,
# 40: 9220, #48: 9260
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

# ====== 测试执行参数 ======
# 测试次数配置
TEST_TIMES = 3
# 测试时间配置（单位：秒）
TEST_DURATION = 30 # 默认10秒，可修改
# Ping测试配置
PING_GATEWAY = "192.168.1.1" # 默认网关IP
PING_COUNT = 30 # 默认ping次数


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


class IperfTester:
    def __init__(self, test_duration=TEST_DURATION, ping_gateway=PING_GATEWAY, ping_count=PING_COUNT):
        # 初始化Telnet客户端（只初始化，不立即连接）
        self.ap_telnet = TelnetClient()
        self.client_telnet = TelnetClient() # Client端先初始化但不连接

        # 设置测试时间
        self.test_duration = test_duration
        # 设置ping测试参数
        self.ping_gateway = ping_gateway
        self.ping_count = ping_count

        # 获取测试配置
        self.test_mode = TEST_MODE
        self.region = REGION
        self.channel_test_bandwidth = CHANNEL_TEST_BANDWIDTH

        # 获取频率表
        self.frequency_table = frequency_tables.get(self.region, US_frequency_tables)

        # 创建测试结果目录
        self.result_dir = "../test_results"
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
                                              f"iperf_comprehensive_test_{self.region}_{self.test_duration}s_{timestamp}.xlsx")

        # 初始化日志文件名
        if self.test_mode == 'bandwidth':
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_bandwidth_test_{self.test_duration}s_{timestamp}.txt")
        elif self.test_mode == 'channel':
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_channel_test_{self.region}_{self.channel_test_bandwidth}MHz_{self.test_duration}s_{timestamp}.txt")
        else: # both
            self.log_filename = os.path.join(self.result_dir,
                                            f"iperf_comprehensive_test_{self.region}_{self.test_duration}s_{timestamp}.txt")

        # 设置带时间戳的日志记录器
        self.logger = TimestampLogger(self.log_filename)
        sys.stdout = self.logger # 重定向标准输出到日志记录器

        # 输出初始信息
        print("=" * 80)
        print(f"测试开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试模式: {self.test_mode}")
        print(f"测试区域: {self.region}")
        print(f"测试配置: {TEST_TIMES}次测试，每次{self.test_duration}秒")
        print(f"Ping测试配置: 网关IP={self.ping_gateway}, 次数={self.ping_count}")

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
        # 基本表头，增加了 Client RX MCS 和 Client TX MCS
        headers = [
            "测试时间", "频宽(MHz)", "AP信道",
            "AP RSSI", "AP SNR", "AP RX MCS", "AP TX MCS",
            "Client RSSI", "Client SNR", "Client RX MCS", "Client TX MCS"
        ]

        # 添加上行测试列
        for i in range(TEST_TIMES):
            headers.append(f"上行{i + 1}(Mbits/sec)")
        headers.append("上行平均(Mbits/sec)")

        # 添加下行测试列
        for i in range(TEST_TIMES):
            headers.append(f"下行{i + 1}(Mbits/sec)")
        headers.append("下行平均(Mbits/sec)")

        # 添加Ping测试列
        headers.append("Ping丢包率(%)")
        headers.append("Ping最小延时(ms)")
        headers.append("Ping平均延时(ms)")
        headers.append("Ping最大延时(ms)")

        # 写入表头并设置格式
        for col, header in enumerate(headers, 1):
            cell = self.ws.cell(row=1, column=col, value=header)
            cell.alignment = Alignment(horizontal='center', vertical='center')

            # 动态调整列宽
            if col <= 11: # 基本信息列（增加到11列）
                self.ws.column_dimensions[chr(64 + col) if col <= 26 else f'{chr(64 + (col-26))}{chr(64 + (col-26))}'].width = 15
            elif col <= (11 + TEST_TIMES * 2 + 2): # iperf测试数据列
                col_letter = chr(64 + col) if col <= 26 else f'{chr(64 + (col-26))}{chr(64 + (col-26))}'
                self.ws.column_dimensions[col_letter].width = 18
            else: # Ping测试数据列
                col_letter = chr(64 + col) if col <= 26 else f'{chr(64 + (col-26))}{chr(64 + (col-26))}'
                self.ws.column_dimensions[col_letter].width = 18

        print(f"表头创建完成，共{len(headers)}列")
        print(f" - 基本信息: 11列")
        print(f" - iperf测试: 上行{TEST_TIMES}次+平均值，下行{TEST_TIMES}次+平均值")
        print(f" - Ping测试: 4列 (丢包率、最小延时、平均延时、最大延时)")

        # 计算列索引位置（用于数据写入）
        self.up_start_col = 12 # 上行测试开始列（基本信息11列，第12列开始）
        self.up_avg_col = 12 + TEST_TIMES # 上行平均值列
        self.down_start_col = 13 + TEST_TIMES # 下行测试开始列
        self.down_avg_col = 13 + TEST_TIMES * 2 # 下行平均值列
        self.ping_packet_loss_col = 14 + TEST_TIMES * 2 # Ping丢包率列
        self.ping_min_latency_col = self.ping_packet_loss_col + 1 # Ping最小延时列
        self.ping_avg_latency_col = self.ping_packet_loss_col + 2 # Ping平均延时列
        self.ping_max_latency_col = self.ping_packet_loss_col + 3 # Ping最大延时列

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

    def _connect_client(self):
        """连接Client设备（延迟连接）"""
        try:
            print(f"连接到Client: {client_ip}:{client_port}")
            self.client_telnet.login(client_ip, client_root, client_pwd, client_port)
            self.client_actions = clientActions(self.client_telnet)
            return True
        except Exception as e:
            print(f"Client连接失败: {str(e)}")
            return False

    def _disconnect_devices(self):
        """断开设备连接"""
        try:
            if self.ap_telnet and hasattr(self.ap_telnet, 'tn') and self.ap_telnet.tn:
                self.ap_telnet.logout()
            if self.client_telnet and hasattr(self.client_telnet, 'tn') and self.client_telnet.tn:
                self.client_telnet.logout()
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

    def _get_client_signal_info(self):
        """获取Client的RSSI和SNR（适配实际返回格式）"""
        try:
            output = self.client_telnet.execute_command('cli_app show signal', timeout=8)
            # 匹配格式："rssi : -55"
            rssi_match = re.search(r'rssi\s*:\s*(-?\d+)', output)
            # 匹配格式："snr : 29"
            snr_match = re.search(r'snr\s*:\s*(-?\d+)', output)

            rssi = rssi_match.group(1) if rssi_match else "未知"
            snr = snr_match.group(1) if snr_match else "未知"

            print(f"Client RSSI: {rssi} dBm, SNR: {snr} dB")
            return rssi, snr
        except Exception as e:
            print(f"获取AP信号信息失败: {str(e)}")
            return "错误", "错误"

    def _get_client_mcs_values(self):
        """获取Client的RX和TX bit rate值（从表格格式中提取）"""
        try:
            output = self.client_telnet.execute_command('cli_app show ap 0', timeout=8)

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
                print("未找到Client数据行")
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
                print(f"Client TX: {tx_value}, RX: {rx_value}")
                return tx_value, rx_value
            elif len(matches) == 1:
                # 如果只匹配到一个，可能是格式问题，尝试另一种方法
                print(f"只匹配到一个值: {matches[0]}")
                # 尝试匹配包含MCS的内容
                all_mcs = re.findall(r'[\d\.]+MBit/s\(MCS\s*\d+\)', data_line)
                if len(all_mcs) >= 2:
                    tx_value = all_mcs[0]
                    rx_value = all_mcs[1]
                    print(f"Client TX (备用): {tx_value}, RX: {rx_value}")
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
                print(f"Client TX (手动组合): {tx_value}, RX: {rx_value}")
                return tx_value, rx_value

            print(f"无法解析Client MCS值，数据行: {data_line}")
            return "未知", "未知"

        except Exception as e:
            print(f"获取Client MCS值失败: {str(e)}")
            return "错误", "错误"

    def _run_iperf_test(self, reverse=False):
        """
        运行iperf测试（分别通过Telnet连接AP/Client执行对应命令）
        reverse: True表示上行流(-R), False表示下行流
        提取receiver行的Bandwidth值作为测试结果
        """
        try:
            # ===== 1. 确保Client端iperf服务器处于运行状态 =====
            print("检查并重启Client端iperf服务器...")
            # 先停止Client端可能存在的iperf进程
            self.client_telnet.execute_command('pkill -f iperf', timeout=5)
            time.sleep(2)
            # 启动Client端iperf3服务器（后台运行）
            self.client_telnet.execute_command('iperf3 -s &', timeout=5)
            time.sleep(2) # 等待服务器启动完成

            # ===== 2. 在AP端执行iperf3客户端命令 =====
            client_ip = self.client_telnet.ip # 获取Client的Telnet连接IP
            test_type = "上行" if reverse else "下行"
            # 构造iperf3命令（-R 上行流，无-R 下行流），使用可配置的测试时间
            cmd = f'iperf3 -c {client_ip} -t {self.test_duration} -i 1 {"-R" if reverse else ""}'
            print(f"在AP端执行{test_type}测试命令: {cmd}")

            # 执行命令（超时设为测试时间+15秒缓冲）
            timeout = self.test_duration + 15
            output = self.ap_telnet.execute_command(cmd, timeout=timeout)
            if not output:
                print(f"{test_type}测试无输出内容")
                return "无输出"

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
                return str(receiver_throughput)

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
                return str(throughput)
            else:
                print(f"未匹配到{test_type}吞吐量receiver值，原始输出:\n{output}")
                # 尝试打印所有包含receiver的行以便调试
                print("包含'receiver'的行:")
                for line in lines:
                    if 'receiver' in line:
                        print(f"  {line}")
                return "未匹配到数据"

        except Exception as e:
            print(f"{test_type}测试失败: {str(e)}")
            return "错误"

    def _run_ping_test(self):
        """
        在Client端执行ping测试
        返回: (丢包率%, 最小延时ms, 平均延时ms, 最大延时ms)
        """
        try:
            # 先停止Client端可能存在的iperf进程
            self.client_telnet.execute_command('pkill -f iperf', timeout=5)
            time.sleep(2)
            print(f"开始Ping测试: ping {self.ping_gateway} -c {self.ping_count}")

            # 执行ping命令
            cmd = f'ping {self.ping_gateway} -c {self.ping_count}'
            output = self.client_telnet.execute_command(cmd, timeout=self.ping_count * 2 + 5)

            if not output:
                print("Ping测试无输出内容")
                return "无输出", "无输出", "无输出", "无输出"

            # 输出ping结果到日志
            print(f"Ping测试结果:\n{output}")

            # 解析ping结果
            # 匹配格式: 10 packets transmitted, 10 packets received, 0% packet loss
            packet_loss_match = re.search(r'(\d+)% packet loss', output)

            # 匹配格式: round-trip min/avg/max = 15.633/232.108/1589.862 ms
            latency_match = re.search(r'min/avg/max = ([\d\.]+)/([\d\.]+)/([\d\.]+) ms', output)

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

    def _run_single_test(self, bandwidth, channel=None):
        """执行单个测试配置（频宽和信道）"""
        try:
            # 设置AP频宽和信道
            if channel is not None:
                print(f"\n设置AP频宽为{bandwidth}MHz, 信道{channel}")
                self.ap_actions.set_bandwidth_channel(bandwidth, channel)
            else:
                print(f"\n设置AP频宽为{bandwidth}MHz")
                self.ap_actions.set_bandwidth(bandwidth)

            time.sleep(30) # 等待设置生效

            # 连接Client
            print("AP设置完成，开始连接Client...")
            if not self._connect_client():
                print("Client连接失败，跳过当前测试")
                if hasattr(self.client_telnet, 'tn') and self.client_telnet.tn:
                    self.client_telnet.logout()
                return False

            # 收集AP信息
            ap_channel = self._get_ap_channel()
            time.sleep(2)
            ap_rssi, ap_snr = self._get_ap_signal_info()
            time.sleep(2)
            ap_rx_mcs, ap_tx_mcs = self._get_ap_mcs_values()
            time.sleep(2)

            # 收集Client信息
            client_rssi, client_snr = self._get_client_signal_info()
            time.sleep(2)
            client_rx_mcs, client_tx_mcs = self._get_client_mcs_values()
            time.sleep(2)

            # 创建初始数据行（修改为11个基本信息）
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            initial_data = [
                current_time, bandwidth, ap_channel,
                ap_rssi, ap_snr, ap_rx_mcs, ap_tx_mcs,
                client_rssi, client_snr, client_rx_mcs, client_tx_mcs
            ]

            # 添加上行占位符
            for i in range(TEST_TIMES + 1):
                initial_data.append("")

            # 添加下行占位符
            for i in range(TEST_TIMES + 1):
                initial_data.append("")

            # 添加Ping测试占位符
            for i in range(4):
                initial_data.append("")

            # 保存初始数据到Excel
            if not self._save_row_to_excel(initial_data):
                print("初始数据保存失败，继续测试...")

            # 运行上行吞吐量测试
            up_results = []
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

            # 运行下行吞吐量测试
            down_results = []
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

            # 运行Ping测试
            print(f"\n开始Ping测试...")
            packet_loss, min_latency, avg_latency, max_latency = self._run_ping_test()

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

            # 打印测试结果汇总
            print(f"\n测试结果汇总:")
            if channel is not None:
                print(f" 频宽: {bandwidth}MHz, 信道: {channel}")
            else:
                print(f" 频宽: {bandwidth}MHz")
            print(f" AP信息: RSSI={ap_rssi}dBm, SNR={ap_snr}dB, RX MCS={ap_rx_mcs}, TX MCS={ap_tx_mcs}")
            print(f" Client信息: RSSI={client_rssi}dBm, SNR={client_snr}dB, RX MCS={client_rx_mcs}, TX MCS={client_tx_mcs}")
            print(f" 上行测试结果: {up_results}, 平均值: {up_average} Mbits/sec")
            print(f" 下行测试结果: {down_results}, 平均值: {down_average} Mbits/sec")
            print(f" Ping测试结果: 丢包率={packet_loss}%, 延时={min_latency}/{avg_latency}/{max_latency} ms")
            print(f" 数据已实时保存到: {os.path.basename(self.excel_filename)}")

            # 断开Client连接
            print("本次测试完成，断开Client连接...")
            if hasattr(self.client_telnet, 'tn') and self.client_telnet.tn:
                self.client_telnet.logout()
            print("Client连接已断开")

            return True

        except Exception as e:
            print(f"单次测试失败: {str(e)}")
            return False

    def run_test(self):
        """运行完整测试流程"""
        try:
            # # 第一步：先连接AP
            # if not self._connect_ap():
            #     print("AP连接失败，测试中止")
            #     return

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


if __name__ == '__main__':
    # 初始化并运行测试
    tester = IperfTester(
        test_duration=TEST_DURATION,
        ping_gateway=PING_GATEWAY,
        ping_count=PING_COUNT
    )

    tester.run_test()