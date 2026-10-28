#api本地升级，telnet获取版本号对比md5值

import base64
import json
import os
import re
import sys
import time
import telnetlib
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# 初始化路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
resource_dir = os.path.join(project_root, "resource")
resource_file = "FW020-UN-up-ver1-3-3-P1-20250425-rel-37133.bin"
local_file_path = os.path.join(resource_dir, resource_file)

# 从文件名中提取目标版本号 (37133)
try:
    # 匹配文件名中"rel-"后的数字（如rel-37133.bin）
    target_version = re.search(r'rel-(\d+)\.bin$', resource_file).group(1)
except AttributeError:
    print(f"无法从文件名 {resource_file} 中提取版本号")
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
        multipart_encoder = None  # 初始化变量，避免引用错误

        try:
            # 检查固件文件是否存在
            if not os.path.isfile(binname):
                raise FileNotFoundError(f"固件文件不存在: {binname}")

            # 第一步：获取token
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
            print(f"  设备 {ip} 升级成功!")

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
            if multipart_encoder:
                for field in multipart_encoder.fields.values():
                    if hasattr(field, 'file') and hasattr(field.file, 'close'):
                        field.file.close()
            results[ip] = device_result

    return results

def getSoftversion(host):
    """获取设备软件版本并对比（适配新的版本返回格式）"""
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
        #print(f"设备 {host} 版本信息返回: {output.strip()}")  # 打印原始返回，便于调试

        # 关键修改：从返回结果中提取"Rel. "后的版本号（适配格式：1.3.3 Build 20250425 Rel. 37133）
        version_match = re.search(r'Rel\.\s*(\d+)', output)  # 匹配"Rel. "后的数字
        if not version_match:
            print(f"设备 {host} - 无法从返回结果中提取版本号")
            return False

        current_version = version_match.group(1)
        print(f"设备 {host} - 当前版本: {current_version}, 目标版本: {target_version}")

        # 对比版本号
        return current_version == target_version

    except Exception as e:
        print(f"检查设备 {host} 版本出错: {e}")
        return False
    finally:
        try:
            tn.close()
        except NameError:
            pass

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
            version_results[ip] = getSoftversion(ip)
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