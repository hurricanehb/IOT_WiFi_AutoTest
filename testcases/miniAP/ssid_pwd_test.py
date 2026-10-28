import os

from basic.apActions import *
from basic.clientActions import *
from basic.telnet_demo import TelnetClient
from basic.pingCheck import *

# 配置文件路径改为从项目根目录开始
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
ping_ip = cfg.get('ping_info', 'ping_ip')


if __name__ == "__main__":
    tc_ap = TelnetClient()
    tc_ap.login(ap_ip,ap_root,ap_pwd,port)

    tc_client = TelnetClient()
    tc_client.login(client_ip,client_root,client_pwd,port)

    ap = apActions(tc_ap)
    client = clientActions(tc_client)

    ssid_list = ["`~!@#$%^&*()_'+'-\"=\"{}|\\\\:;<>?,./", 'abcdefghijklmnop', '24681357', '1234567890\"abcdefgh\"123456789012',
                     'HyperWi-Fi_US']
    pwd_list = ["`~!@#$%^&*()_'+'-\"=\"{}|\\\\:;<>?,./", 'abcdefghijklmnop', '24681357', '1234567890\"abcdefgh\"123456789012',
                    'HyperWi-Fi_US']
    encryption_list = ['wpa3-sae', 'open']

    for ssid in ssid_list:
        for encryption in encryption_list:
            if encryption == 'open':
                # 对于开放网络，不需要密码，直接测试
                try:
                    # 配置Client
                    #client.set_ssid(ssid)
                   # client.set_encryption(encryption)
                    #client.uci_commit()

                    # 配置AP
                    ap.set_ssid(ssid)
                    ap.set_encryption(encryption)
                    ap.uci_commit()

                    # 这里添加连接测试逻辑
                except Exception as e:
                    print(f"Error occurred with SSID={ssid}, Encryption={encryption}: {str(e)}")
            else:
                # 对于需要密码的网络，遍历密码列表
                for pwd in pwd_list:
                    try:
                        # 配置Client
                        #client.set_ssid(ssid)
                        #client.set_encryption(encryption)
                        #client.set_password(pwd)
                        #client.uci_commit()

                        # 配置AP
                        ap.set_ssid(ssid)
                        ap.set_encryption(encryption)
                        ap.set_password(pwd)
                        ap.uci_commit()

                        sleep(30)
                        check_all_ips(ping_list,max_attempts=10)

                    except Exception as e:
                        print(f"Error occurred with SSID={ssid}, Encryption={encryption}, Password={pwd}: {str(e)}")