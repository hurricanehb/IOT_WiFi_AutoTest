#api本地升级，获取版本号对比版本号
import base64
import json
import os
import re
import sys
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 初始化路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
resource_dir = os.path.join(project_root, "resource")
resource_file = "FW020-UN-up-ver1-3-4-P1-20250613-rel-66492.bin"
local_file_path = os.path.join(resource_dir, resource_file)

# 从文件名中提取目标版本号 (1.3.4)
try:
    # 尝试从"verX-Y-Z"格式中提取版本号
    match = re.search(r'ver(\d+)-(\d+)-(\d+)', resource_file)
    if match:
        target_version = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    else:
        # 尝试从"verX.Y.Z"格式中提取版本号
        match = re.search(r'ver(\d+\.\d+\.\d+)', resource_file)
        if match:
            target_version = match.group(1)
        else:
            raise AttributeError("无法从文件名中提取版本号")
except AttributeError as e:
    print(f"错误: {str(e)} - 文件名格式应为类似 'ver1-3-4' 或 'ver1.3.4'")
    sys.exit(1)

tftp_process = None
ips = ["192.168.40.199", "192.168.40.202"]


def upgrade_firmware(binname, password='24681357', base_url='http://{}/api'):
    """依次对多个设备进行固件升级"""
    results = {}
    encoded_password = base64.b64encode(password.encode('utf8')).decode('utf8')

    for ip in ips:
        print(f"\n正在升级设备: {ip}")
        url = base_url.format(ip)
        device_result = {"status": "failed", "message": "", "response": None}

        try:
            # 检查固件文件是否存在
            if not os.path.isfile(binname):
                raise FileNotFoundError(f"固件文件不存在: {binname}")

            # 第一步：获取升级前的token
            print(f"  获取认证token...")
            headers = {'Content-Type': 'application/json'}
            data = {
                "msg_id": "1234",
                "params": [
                    {"opcode": "0x2000", "param": {"account": {"user": "admin", "password": encoded_password}}}]
            }

            r = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
            r.raise_for_status()
            response_data = r.json()
            token = response_data.get('data', [{}])[0].get('result', {}).get('account', {}).get('token')

            if not token:
                raise ValueError("无法获取认证token")

            print(f"  获取token成功: {token[:8]}...")
            time.sleep(1)

            # 第二步：上传固件
            print(f"  开始上传固件: {binname}")
            headers1 = {'XSRF-TOKEN': token}
            multipart_encoder = MultipartEncoder(
                fields={
                    'file': (os.path.basename(binname), open(binname, 'rb'), 'application/octet-stream'),
                    'opcode': '4'
                }
            )
            headers1['Content-Type'] = multipart_encoder.content_type

            response = requests.post(url, headers=headers1, data=multipart_encoder, timeout=120)
            response.raise_for_status()

            device_result["status"] = "success"
            device_result["message"] = "固件上传成功"
            device_result["response"] = response.json()
            print(f"  设备 {ip} 升级请求已发送!")

        except FileNotFoundError as e:
            device_result["message"] = f"固件文件未找到: {str(e)}"
            print(f"  错误: {device_result['message']}")
        except requests.exceptions.RequestException as e:
            device_result["message"] = f"网络请求错误: {str(e)}"
            print(f"  错误: {device_result['message']}")
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            device_result["message"] = f"响应解析错误: {str(e)}"
            print(f"  错误: {device_result['message']}")
        except Exception as e:
            device_result["message"] = f"未知错误: {str(e)}"
            print(f"  错误: {device_result['message']}")
        finally:
            # 关闭文件资源
            results[ip] = device_result

    return results


def get_new_token(ip, password='24681357', base_url='http://{}/api'):
    """获取升级后的新token"""
    print(f"  获取升级后的新token: {ip}")
    url = base_url.format(ip)
    encoded_password = base64.b64encode(password.encode('utf8')).decode('utf8')

    headers = {'Content-Type': 'application/json'}
    data = {
        "msg_id": "1234",
        "params": [
            {"opcode": "0x2000", "param": {"account": {"user": "admin", "password": encoded_password}}}]
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        r.raise_for_status()
        response_data = r.json()
        token = response_data.get('data', [{}])[0].get('result', {}).get('account', {}).get('token')

        if not token:
            raise ValueError("无法获取新token")

        print(f"  新token获取成功: {token[:8]}...")
        return token
    except Exception as e:
        print(f"获取新token失败: {str(e)}")
        return None


def ap_get_version(token, ip, password='24681357', base_url='http://{}/api'):
    """通过API获取设备版本信息"""
    if not token:
        print(f"缺少token，无法获取设备 {ip} 版本信息")
        return None

    url = base_url.format(ip)
    headers = {
        'Content-Type': 'application/json',
        'XSRF-TOKEN': token
    }
    data = {
        "params": [{"opcode": "0x2071", "param": {}}],
        "count": "1"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取设备 {ip} 版本信息失败: {str(e)}")
        return None


def compare_softVer(host):
    """通过API获取并对比设备软件版本"""
    print(f"检查设备 {host} 版本...")

    # 获取升级后的新token
    new_token = get_new_token(host)
    if not new_token:
        print(f"无法获取设备 {host} 的新token，版本检查失败")
        return False

    # 使用新token获取版本信息
    version_data = ap_get_version(new_token, host)
    if not version_data:
        return False

    # 从API响应中提取current_version字段
    current_version = version_data.get('data', [{}])[0].get('result', {}).get('upgrade', {}).get('current_version', '')
    print(f"API返回当前版本: {current_version}, 目标版本: {target_version}")

    # 对比版本号
    return current_version == target_version


if __name__ == "__main__":
    firmware_file = local_file_path

    print(f"开始批量升级固件，目标设备: {', '.join(ips)}")
    print(f"使用固件文件: {firmware_file}")
    print(f"目标版本号: {target_version}")

    # 检查固件文件是否存在
    if not os.path.isfile(firmware_file):
        print(f"错误: 固件文件不存在 - {firmware_file}")
        sys.exit(1)

    upgrade_results = upgrade_firmware(firmware_file)

    # 等待设备重启完成
    print("\n等待设备重启...")
    time.sleep(90)

    # 验证版本号
    print("\n开始验证设备版本...")
    version_results = {}
    for ip in ips:
        try:
            print(f"\n验证设备: {ip}")
            version_results[ip] = compare_softVer(ip)
        except Exception as e:
            print(f"验证设备 {ip} 时出错: {e}")
            version_results[ip] = False

    # 输出最终结果
    print("\n升级结果汇总:")
    for ip in ips:
        upgrade_status = upgrade_results.get(ip, {}).get("status", "failed")
        version_status = version_results.get(ip, False)
        status = "成功" if (upgrade_status == "success" and version_status) else "失败"
        print(f"设备 {ip}: {status}")