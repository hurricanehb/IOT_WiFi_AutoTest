import configparser
from time import sleep

from basic.apActions import apActions
from basic.pingCheck import *
from basic.telnet_demo import TelnetClient

config_path = '../config.ini'  # 相对路径
# config_path = 'F:\\02-Project\\prthonProject\\Test_script\\testsuits\\config.ini'  # 绝对路径
cfg = configparser.ConfigParser()
# 读取配置文件的信息
cfg.read(config_path,encoding='utf-8')

# Read configuration values
ap_ip = cfg.get('ap_info', 'ap_ip')
ap_root = cfg.get('ap_info', 'ap_root')
ap_pwd = cfg.get('ap_info', 'ap_pwd')
port = cfg.get('ap_info', 'port')
client_ip = cfg.get('client_info', 'client_ip')
client_root = cfg.get('client_info', 'client_root')
client_pwd = cfg.get('client_info', 'client_pwd')
ping_ip = cfg.get('ping_info', 'ping_ip')

# 可用区域列表
REGIONS = ['US', 'EU', 'TH']

# 可用带宽列表
BANDWIDTHS = ['1', '2', '4']


# 各种带宽的频率表，修改为下发信道对应1MHz的频率值
US_frequency_tables = {
    '1': {
        #1: 9025, 3: 9035, 5: 9045, 7: 9055, 9: 9065, 11: 9075, 13: 9085, 15: 9095,
        5: 9045, 7: 9055, 9: 9065, 11: 9075, 13: 9085, 15: 9095,
        17: 9105, 19: 9115, 21: 9125, 23: 9135, 25: 9145, 27: 9155, 29: 9165, 31: 9175,
        33: 9185, 35: 9195, 37: 9205, 39: 9215, 41: 9225, 43: 9235, 45: 9245, 47: 9255,
        #49: 9265, 51: 9275
    },
    '2': {
        #2: 9030, 6: 9050, 10: 9070, 14: 9090, 18: 9110, 22: 9130,
        6: 9050, 10: 9070, 14: 9090, 18: 9110, 22: 9130,
        26: 9150, 30: 9170, 34: 9190, 38: 9210, 42: 9230, 46: 9250,
        #50: 9270
    },
    '4': {
        8: 9060, 16: 9100, 24: 9140, 32: 9180, 40: 9220, 48: 9260
    },
    '8': {
        12: 9080, 28: 9160, 44: 9240
    },
}

EU_frequency_table = {'1': {1: 8635, 3: 8645, 5: 8655, 7: 8665, 9: 8675}}

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

def channel_test(tn, regions=None, bandwidths=None):
    """
    测试指定区域和频宽的信道
    :param tn: Telnet连接对象
    :param regions: 区域列表（如 ['US', 'EU']），如果为None则测试所有区域
    :param bandwidths: 带宽列表（如 ['1M', '2M']），如果为None则测试所有带宽
    """
    aa = apActions(tn)
    test_regions = REGIONS if regions is None else [r for r in regions if r in REGIONS]
    test_bandwidths = BANDWIDTHS if bandwidths is None else [bw for bw in bandwidths if bw in BANDWIDTHS]

    try:
        for region in test_regions:
            for bw in test_bandwidths:
                channels = frequency_tables[region].get(bw, {})
                print(f"【开始测试 {region} 地区 {bw} MHz带宽的信道】")

                for channel, frequency in channels.items():
                    aa.set_bandwidth_channel(bw, channel)  # 下发索引
                    print(f"下发配置: {channel} 信道对应频率: {frequency}MHz")  # 打印频率
                    sleep(1)
                    ping_check(ping_ip, max_attempts=60)

    except Exception as err:
        print(f"信道测试异常: {err}")


def bandwidth_test(tn, bandwidths=None):
    """
    测试指定频宽
    :param tn: Telnet连接对象
    :param bandwidths: 带宽列表（如 ['1M', '2M']），如果为None则测试所有带宽
    """
    aa = apActions(tn)
    test_bandwidths = BANDWIDTHS if bandwidths is None else [bw for bw in bandwidths if bw in BANDWIDTHS]

    try:
        for i, bandwidth in enumerate(test_bandwidths, start=1):
            print(
                f'【================={datetime.datetime.now()} 第{i}次 修改miniAP频宽：{bandwidth}=================】')
            aa.set_bandwidth(bandwidth)
            sleep(1)
            ping_check(ping_ip, max_attempts=10)

    except Exception as err:
        print(f"带宽测试异常: {err}")


if __name__ == '__main__':
    tc = TelnetClient()
    tc.login(ap_ip,ap_root,ap_pwd,port)

    # 示例：按地区码和频宽指定测试
    for i in range(1000):
     channel_test(tc, regions=['US'], bandwidths=['1', '2','4'])
    # bandwidth_test(tc,bandwidths=['1M', '4M'])

    # 测试所有地区和频宽
    #channel_test(tc)
    # bandwidth_test(tc)
    sleep(2)
