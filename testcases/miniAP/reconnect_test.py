import configparser
import datetime
import os
import traceback
from time import sleep

import sys
#sys.path.append("路径到 miniAP_test 的父目录")  # 例如 C:\Users\admin\Desktop\控制人程序
#sys.path.append(r"C:\Users\admin\Desktop\挂机小帮手\miniAP_test")  # 例如 C:\Users\admin\Desktop\控制人程序

from basic.apActions import apActions
from basic.clientActions import clientActions
from basic.pingCheck import *
from basic.run_iperf import *
from basic.telnet_demo import TelnetClient
import datetime

# 配置文件路径改为从项目根目录开始
#from testsuits import check_all_ips

config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
cfg = configparser.ConfigParser()

# 读取配置文件的信息
cfg.read(config_path, encoding='utf-8')

# Read configuration values
ap_ip = cfg.get('ap_info', 'ap_ip')
ap_root = cfg.get('ap_info', 'ap_root')
ap_pwd = cfg.get('ap_info', 'ap_pwd')
port = cfg.get('ap_info', 'port')
client_ip = cfg.get('client_info', 'client_ip')
client_root = cfg.get('client_info', 'client_root')
client_pwd = cfg.get('client_info', 'client_pwd')
port = cfg.get('client_info', 'port')
ping_ip = cfg.get('ping_info', 'ping_ip')

# 修改为从配置文件中获取IP列表，或者使用默认值
#ping_list = cfg.get('ping_info', 'ping_ip', fallback='').split(',') or [
ping_list = ["192.10.10.144","192.10.10.137"]

# 清理IP列表中的空白字符
ping_list = [ip.strip() for ip in ping_list if ip.strip()]

country_table = {'US':'46434300','EU':'43450000','EUs':'43450001'}

# 场景1：AP重启重连
def ap_reboot_reconnect(tn):
    '''
    #st = datetime.datetime.now()
    #print(f'【===================={st} AP重启重连====================】')

    #tn.login(ap_ip, ap_root, ap_pwd, '23')
    #sleep(1)
    #tn.execute_command('reboot')
    aa = apActions(tn)
    aa.ap_reboot()
    #sleep(60)
    sleep(2)
    check_all_ips(ping_list, max_attempts=20)
    #sleep(10)
    '''
    aa = apActions(tn)

    print("开始AP重启重连测试...")

    # 执行AP重启
    if aa.ap_reboot():
        print("AP重启命令已发送，等待设备重启...")

        # 等待一段时间让AP完全重启
        time.sleep(60)

        # 尝试重连
        if aa.tn.reconnect(timeout=180):  # 最多等待3分钟
            print("AP重启后重连成功，继续后续测试...")
            # 这里可以添加后续的测试逻辑
            # 例如：检查AP状态、验证网络连接等
            check_all_ips(ping_list, max_attempts=20)
            sleep(10)
            # 示例：执行一个简单的命令验证连接
            try:
                result = aa.tn.execute_command('echo "AP重启测试成功"')
                print(f"测试命令执行结果: {result}")
                return True
            except Exception as e:
                print(f"测试命令执行失败: {e}")
                return False
        else:
            print("AP重启后重连失败")
            return False
    else:
        print("AP重启失败")
        return False

# 场景2：AP重启无线
def ap_halow_restart_reconnect(tn):
    #st = datetime.datetime.now()
    #print(f'【===================={st} AP重启重连====================】')

    #tn.login(ap_ip, ap_root, ap_pwd, '23')
    #sleep(1)
    #tn.execute_command('reboot')
    aa = apActions(tn)
    aa.halow_restart()
    sleep(30)
    #sleep(2)
    #ping_check(client_ip, max_attempts=20)
    #sleep(10)
    check_all_ips(ping_list, max_attempts=20)
    sleep(1)

# 场景3：AP修改无线配置
def ap_change_settings_reconnect(tn):

    #print(f'【===================={st} AP修改无线配置重连====================】')

    aa = apActions(tn)

    aa.set_bandwidth_channel(2, "2")
    sleep(60)
    #check_all_ips(ping_list, max_attempts=10)

    aa.set_bandwidth_channel(2, "26")
    sleep(60)

    #check_all_ips(ping_list, max_attempts=10)
    #sleep(1)

    aa.set_bandwidth_channel(2, "50")
    sleep(60)

    #check_all_ips(ping_list, max_attempts=10)
    #sleep(1)

    #aa.set_bandwidth_channel(8, "44")
    #sleep(60)
    #check_all_ips(ping_list, max_attempts=10)
    #sleep(1)

# 场景4：AP加载无线配置
def ap_halow_reload_reconnect(tn):
    aa = apActions(tn)

    aa.halow_reload()
    sleep(30)
    check_all_ips(ping_list, max_attempts=20)
    sleep(5)

# 场景5：AP重置模组
def ap_halow_reset_reconnect(tn):
    aa = apActions(tn)

    aa.halow_reset_module()
    sleep(60)
    check_all_ips(ping_list, max_attempts=20)
    sleep(10)

# 场景6：AP主动踢客户端
def ap_kick_sta_reconnect(tn):
    aa = apActions(tn)

    aa.halow_kick_sta()
    sleep(30)
    check_all_ips(ping_list, max_attempts=20)
    sleep(10)

# 场景7：client重启重连
def client_reboot_reconnect(tn):
    #st = datetime.datetime.now()
    #print(f'【===================={str(st)} client重启重连====================】')

    #tn.login(client_ip, client_root, client_pwd, '23')
    #sleep(1)
    #tn.execute_command('reboot')
    #sleep(40)
    mc = clientActions(tn)
    mc.client_reboot()
    sleep(60)
    check_all_ips(ping_list, max_attempts=20)
    sleep(10)

def client_halow_reset_reconnect(tn):
    #st = datetime.datetime.now()
    #print(f'【===================={str(st)} client重启重连====================】')

    #tn.login(client_ip, client_root, client_pwd, '23')
    #sleep(1)
    #tn.execute_command('reboot')
    #sleep(40)
    mc = clientActions(tn)
    mc.client_reboot()
    sleep(40)

def modify_countryCode_reconnect(tn):
    aa = apActions(tn)
    mc = clientActions(tn)
    # 遍历country_table字典
    for country_code, special_id in country_table.items():
        print(f"正在设置国家码: {country_code}, 特殊ID: {special_id}")

        # 使用clientActions设置国家码
        mc.set_countrycode(country_code, special_id)
        sleep(2)

        # 使用apActions设置国家码
        aa.set_countrycode(country_code, special_id)
        sleep(60)

        # 检查所有IP连接
        check_all_ips(ping_list, max_attempts=20)

    sleep(60)

if __name__ == '__main__':
    try:
        '''

        client_tc = TelnetClient()
        client_tc.login(client_ip, client_root, client_pwd, port)
        mc = clientActions(client_tc)
        '''
        ap_tc = TelnetClient()
        ap_tc.login(ap_ip, ap_root, ap_pwd, port)
        ma = apActions(ap_tc)


        for i in range(1000):


            #tc = TelnetClient()
            #tc.login(ap_ip, ap_root, ap_pwd, port)
            #tc.login(client_ip, client_root, client_pwd, port)

            #client_tc = TelnetClient()
            #client_tc.login(client_ip, client_root, client_pwd, port)
            #mc = clientActions(client_tc)

            st = datetime.datetime.now()

            #print(f'【========================{str(st)} 第 {i} 轮次重连测试：client重启重连========================】')
            #client_reboot_reconnect(client_tc)

            '''
            print(f'【========================{str(st)} 第 {i} 轮次重连测试：AP主动踢客户端========================】')
            ap_kick_sta_reconnect(ap_tc)
            '''
            #print(f'【========================{str(st)} 第 {i} 轮次重连测试：重启AP========================】')
            #ap_reboot_reconnect(ap_tc)

            print(f'【========================{str(st)} 第 {i} 轮次重连测试：修改AP无线配置========================】')
            ap_change_settings_reconnect(ap_tc)

            #print(f'【========================{str(st)} 第 {i} 轮次重连测试：重启client========================】')
            #client_reboot_reconnect(client_tc)

            #print(f'【========================{str(st)} 第 {i} 轮次重连测试：ap halow reload========================】')
            #ap_halow_reload_reconnect(tc)

            #print(f'【========================{str(st)} 第 {i} 轮次重连测试：ap halow restart========================】')
            #ap_halow_restart_reconnect(tc)

            #print(f'【========================{str(st)} 第 {i} 轮次重置模组：ap halow reset========================】')
            #ap_halow_restart_reconnect(tc)
            '''
            print(f'【========================{str(st)} 第 {i} 轮次测试开始执行========================】')
            print(f'【========================修改client为wpa3========================】')
            mc.set_wpa3("HyperWi-Fi_3C34", "wpa3-sae", "85576889")
            sleep(2)

            print(f'【========================修改ap为wpa3========================】')
            ma.set_wpa3("HyperWi-Fi_3C34", "wpa3-sae", "85576889")
            sleep(30)

            ping_check(ping_ip, max_attempts=20)
            sleep(2)

            print(f'【========================修改client为open========================】')
            mc.set_open("HyperWi-Fi_3C34", "open")
            sleep(2)

            print(f'【========================修改ap为open========================】')
            ma.set_open("HyperWi-Fi_3C34", "open")
            sleep(30)

            ping_check(ping_ip, max_attempts=20)
            sleep(2)
            '''

    except Exception as e:
        # 打印详细的错误信息
        traceback.print_exc()