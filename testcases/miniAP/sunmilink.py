import os
import configparser
from time import sleep
from basic.apActions import *
from basic.clientActions import *
from basic.telnet_demo import TelnetClient
from basic.pingCheck import *


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    cfg = configparser.ConfigParser()
    cfg.read(config_path, encoding='utf-8')
    return {
        'ap_info': {
            'ip': cfg.get('ap_info', 'ap_ip'),
            'username': cfg.get('ap_info', 'ap_root'),
            'password': cfg.get('ap_info', 'ap_pwd'),
            'port': cfg.getint('ap_info', 'port')
        },
        'client_info': {
            'ip': cfg.get('client_info', 'client_ip'),
            'username': cfg.get('client_info', 'client_root'),
            'password': cfg.get('client_info', 'client_pwd'),
            'port': cfg.getint('client_info', 'port')
        },
        'ping_info': {
            'ping_list': ["192.168.40.199",]  # 硬编码或从配置读取
        }
    }


def setup_connections(config):
    """建立Telnet连接"""
    print("正在建立AP连接...")
    tc_ap = TelnetClient()
    tc_ap.login(
        config['ap_info']['ip'],
        config['ap_info']['username'],
        config['ap_info']['password'],
        config['ap_info']['port']
    )

    print("正在建立Client连接...")
    tc_client = TelnetClient()
    tc_client.login(
        config['client_info']['ip'],
        config['client_info']['username'],
        config['client_info']['password'],
        config['client_info']['port']
    )

    return apActions(tc_ap), clientActions(tc_client)


def teardown_connections(ap, client):
    """关闭连接"""
    print("正在关闭连接...")
    if hasattr(ap, 'telnet'):
        ap.telnet.close()
    if hasattr(client, 'telnet'):
        client.telnet.close()


def execute_test_case(ap, client, config, case):
    """执行单个测试用例"""
    ssid, pwd, encryption, bandwidth = case
    print("\n" + "=" * 80)
    print(f"开始测试: SSID='{ssid}',加密='{encryption}', 密码='{pwd}', 带宽={bandwidth}MHz")
    print("=" * 80)

    try:
        # 1. 启动Client配网
        print("[1/5] 启动Client配网...")
        client.sunmilink_start()
        sleep(1)

        # 2. 配置AP参数
        print("[2/5] 配置AP参数...")
        ap.set_ssid(ssid)
        ap.set_encryption(encryption)
        if pwd is not None:
            ap.set_password(pwd)
        if bandwidth is not None:
            ap.set_bandwidth(bandwidth)
        ap.uci_commit()
        sleep(1)
        ap.halow_reload()
        sleep(1)

        # 3. 启动AP配网
        print("[3/5] 启动AP配网...")
        ap.sunmilink_start()
        sleep(30)

        # 4. 验证连接
        print("[4/5] 验证网络连接...")
        check_all_ips(config['ping_info']['ping_list'], max_attempts=10)

        # 5. ap退出配网状态
        print("[5/5] ap/client退出配网状态...")
        ap.sunmilink_stop()
        sleep(1)
        client.sunmilink_stop()
        sleep(30)

        print(f"✅ 测试成功: SSID='{ssid}',加密='{encryption}', 密码='{pwd}', 带宽={bandwidth}MHz")
        return True

    except Exception as e:
        print(f"❌ 测试失败: SSID='{ssid}',加密='{encryption}', 密码='{pwd}', 带宽={bandwidth}MHz")
        print(f"错误详情: {str(e)}")
        return False


def main():
    """主执行函数"""
    # 测试用例定义
    test_cases = [
        #("abcdefgh", "abcdefgh", "wpa3-sae", 1),
        #("HyperWiFi_3C50", "HyperWiFi_3C50", "wpa3-sae", 2),
       # ("1234567890212345678903456789012", "1234567890212345678903456789012", "wpa3-sae", 4),
        ("'`~!@#$%^&*()_+-={}[]|\:;<>?,./'", "\"`~!@#$%^&*()_+-={}[]|\:;<>?,./\"", "wpa3-sae", 4),
        #("abcdefgh", None, "open", 1),
        #("HyperWiFi_3C50", None, "open", 2),
        #("1234567890212345678903456789012", None, "open", 4),
        #(r"`~!@#$%^&*()_+-={}[]|\:;<>?,./", None, "open", 4)
    ]

    print("\n" + "=" * 80)
    print("WiFi配置测试套件".center(80))
    print("=" * 80)

    config = load_config()
    ap, client = setup_connections(config)
    total = len(test_cases)
    passed = 0

    try:
        for i, case in enumerate(test_cases, 1):
            print(f"\n▶ 测试进度: {i}/{total}")
            if execute_test_case(ap, client, config, case):
                passed += 1

        print("\n" + "=" * 80)
        print(f"测试完成: 通过 {passed}/{total}".center(80))
        print("=" * 80)

    finally:
        teardown_connections(ap, client)


if __name__ == "__main__":
    main()