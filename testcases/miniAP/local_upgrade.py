import sys
import os
import re
import telnetlib
import time
import subprocess

ips = ["192.168.40.199", "192.168.40.202"]
tftp_server = "192.168.40.185"
resource_file = "FW020-UN-up-ver1-3-3-P1-20250425-rel-37133.bin"
tftp_exe = "tftpd32.exe"

# 初始化路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
resource_dir = os.path.join(project_root, "resource")
tftp_exe_path = os.path.join(resource_dir, tftp_exe)
local_file_path = os.path.join(resource_dir, resource_file)

# 从文件名中提取版本号 (37133)
try:
    target_version = re.search(r'rel-(\d+)\.bin$', resource_file).group(1)
except AttributeError:
    print(f"无法从文件名 {resource_file} 中提取版本号")
    sys.exit(1)

tftp_process = None


def get_local_file_size():
    """获取本地文件大小"""
    try:
        return os.path.getsize(local_file_path)
    except Exception as e:
        print(f"获取本地文件大小失败: {e}")
        return -1


def get_remote_file_size(tn):
    """获取远程文件大小"""
    try:
        tn.write(b"ls -l /tmp/*.bin\r\n")
        output = tn.read_until(b'admin@Client_3C4F:/tmp# ', timeout=5).decode('utf-8')

        # 简化文件大小提取逻辑
        for line in output.split('\n'):
            if resource_file in line and '-rw-' in line:
                size = int(line.split()[4])
                print(f"远程文件大小: {size} 字节")
                return size
        return -1
    except Exception as e:
        print(f"获取远程文件大小失败: {e}")
        return -1


def monitor_transfer_progress(tn, host):
    """监控文件传输进度"""
    local_size = get_local_file_size()
    if local_size <= 0:
        return False

    print(f"开始监控 {resource_file} 传输进度 (目标大小: {local_size} 字节)")

    while True:
        remote_size = get_remote_file_size(tn)
        if remote_size == local_size:
            print(f"设备 {host} - 传输完成 (100%)")
            return True
        elif remote_size > 0:
            progress = min(100, int(remote_size / local_size * 100))
            print(f"设备 {host} - 传输进度: {progress}% ({remote_size}/{local_size} 字节)")
        time.sleep(2)


def start_tftp_server():
    """启动TFTP服务器"""
    global tftp_process
    if not os.path.exists(tftp_exe_path):
        print(f"TFTP服务器程序不存在: {tftp_exe_path}")
        return False

    try:
        tftp_process = subprocess.Popen(
            [tftp_exe_path, "-i", tftp_server, "-s", resource_dir],
            cwd=resource_dir
        )
        time.sleep(1)
        if tftp_process.poll() is not None:
            print("TFTP服务器启动失败")
            return False
        print(f"TFTP服务器已启动，目录: {resource_dir}")
        return True
    except Exception as e:
        print(f"启动TFTP服务器出错: {e}")
        return False


def stop_tftp_server():
    """停止TFTP服务器"""
    global tftp_process
    if tftp_process and tftp_process.poll() is None:
        tftp_process.terminate()
        print("TFTP服务器已停止")


def handle_device(host):
    """处理单个设备"""
    try:
        print(f"连接设备: {host}")
        tn = telnetlib.Telnet(host, 23, 10)

        # 登录流程
        tn.read_until(b'login: ', 5)
        tn.write(b'root\r\n')
        tn.read_until(b'Password: ', 5)
        tn.write(b'EXAMPLE_PASSWORD\r\n')
        tn.read_until(b'admin@Client_3C4F:~# ', 5)

        # 进入/tmp目录并开始传输
        tn.write(b'cd /tmp\r\n')
        tn.read_until(b'admin@Client_3C4F:/tmp# ', 5)
        tn.write(f'upgrade {tftp_server} {resource_file}\r\n'.encode())

        # 监控传输进度
        if not monitor_transfer_progress(tn, host):
            print(f"设备 {host} - 传输失败")
            tn.close()
            return False

        # 其他操作...
        print(f"设备 {host} - 传输成功，执行重启")
        tn.write(b'reboot\r\n')

        tn.close()
        return True

    except Exception as e:
        print(f"处理设备 {host} 出错: {e}")
        return False



def getSoftversion(host):
    """获取设备软件版本并对比"""
    try:
        print(f"连接设备 {host} 检查版本...")
        tn = telnetlib.Telnet(host, 23, 10)

        # 登录流程
        tn.read_until(b'login: ', 5)
        tn.write(b'root\r\n')
        tn.read_until(b'Password: ', 5)
        tn.write(b'EXAMPLE_PASSWORD\r\n')
        tn.read_until(b'admin@Client_3C4F:~# ', 5)

        # 获取版本信息
        tn.write(b'getfirm SOFTVERSION\r\n')
        output = tn.read_until(b'admin@Client_3C4F:~# ', 10).decode('utf-8')

        # 提取版本号
        version_match = re.search(r'SOFTVERSION\s*:\s*(\d+)', output)
        if not version_match:
            print(f"设备 {host} - 无法获取版本号")
            return False

        current_version = version_match.group(1)
        print(f"设备 {host} - 当前版本: {current_version}, 目标版本: {target_version}")

        # 对比版本号
        if current_version == target_version:
            print(f"设备 {host} - 版本验证成功!")
            return True
        else:
            print(f"设备 {host} - 版本验证失败!")
            return False

    except Exception as e:
        print(f"检查设备 {host} 版本出错: {e}")
        return False
    finally:
        try:
            tn.close()
        except:
            pass


if __name__ == "__main__":
    if not os.path.exists(local_file_path):
        print(f"升级文件不存在: {local_file_path}")
        sys.exit(1)

    if not start_tftp_server():
        sys.exit(1)

    # 升级设备
    upgrade_results = {}
    try:
        for ip in ips:
            print(f"\n处理设备: {ip}")
            upgrade_results[ip] = handle_device(ip)
    finally:
        stop_tftp_server()

    # 等待设备重启完成
    print("\n等待设备重启...")
    time.sleep(60)

    # 验证版本号
    print("\n开始验证设备版本...")
    version_results = {}
    for ip in ips:
        try:
            print(f"\n验证设备: {ip}")
            version_results[ip] = getSoftversion(ip)
        except Exception as e:
            print(f"验证设备 {ip} 时出错: {e}")
            version_results[ip] = False

    # 输出最终结果
    print("\n升级结果汇总:")
    for ip in ips:
        status = "成功" if upgrade_results.get(ip, False) and version_results.get(ip, False) else "失败"
        print(f"设备 {ip}: {status}")

    print("\n所有操作完成")