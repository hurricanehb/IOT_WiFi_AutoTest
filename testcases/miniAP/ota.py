import datetime
import sys
import telnetlib
import time

import datetime as datetime
import traceback

host = "10.17.6.32"

for i in range(1000):

    dtime = datetime.datetime.now()
    print("=======================" + str(dtime) +"   第" + str(i) + "次执行测试=======================")
    try:
        # 创建Telnet对象
        tn = telnetlib.Telnet(host, port=23, timeout=10)

        # 连接telnet
        tn.read_until(bytes('login: ', encoding="utf8"), timeout=5)
        tn.write(b'root\r\n')
        tn.read_until(bytes('Password: ', encoding="utf8"), timeout=5)
        tn.write(b'EXAMPLE_PASSWORD\r\n')
        tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)

        # 执行命令
        #tn.write(b'your_command\n')
        print("*** 获取当前资源包版本号 ***")
        tn.write(bytes("getfirm RESVERSION\r\n", encoding="utf8"))
        res1 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
        output1 = str(res1, encoding="utf8")
        print(output1)
        if "1.3.0" in output1:
            print("*** 资源包版本号降级 ***")
            tn.write(bytes("sed -i 's/1.3.0/1.0.0/g' /tmp/user-info\r\n", encoding="utf8"))
            time.sleep(5)
            res2 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
            output2 = str(res2, encoding="utf8")
            print(output2)

            tn.write(bytes("cat /tmp/user-info\r\n", encoding="utf8"))
            time.sleep(5)
            res3 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
            output3 = str(res3, encoding="utf8")
            print(output3)

            tn.write(bytes("flashmanager -w /tmp/user-info -p user-info\r\n", encoding="utf8"))
            time.sleep(5)

            print("*** 重启设备:等待中 ***")
            tn.write(bytes("reboot\r\n", encoding="utf8"))
            time.sleep(150)
        else:
            print("*** 资源包版本不匹配，测试终止 *** ")
            # 关闭连接
            print("*** 关闭telnet连接 ***")
            tn.close()
            break
    except Exception as e:
        traceback.print_exc()

    '''
    print("*** 获取当前固件版本号 ***")
        tn.write(bytes("getfirm SOFTVERSION\r\n", encoding="utf8"))
        res1 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
        output1 = str(res1, encoding="utf8")
        print(output1)
        if "1.3.0" in output1:
            print("*** 固件版本号降级 ***")
            tn.write(bytes("sed -i 's/1.3.0/1.0.0/g' /tmp/softversion\r\n", encoding="utf8"))
            time.sleep(5)
            res2 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
            output2 = str(res2, encoding="utf8")
            print(output2)

            tn.write(bytes("cat /tmp/softversion\r\n", encoding="utf8"))
            time.sleep(5)
            res3 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
            output3 = str(res3, encoding="utf8")
            print(output3)

            tn.write(bytes("flashmanager -w /tmp/softversion -p soft-version\r\n", encoding="utf8"))
            time.sleep(5)

            print("*** 重启设备 ***")
            tn.write(bytes("reboot\r\n", encoding="utf8"))
            time.sleep(150)
        else:
            print("*** 固件版本不匹配，测试终止 *** ")
            # 关闭连接
            print("*** 关闭telnet连接 ***")
            tn.close()
            break
    except Exception as e:
        traceback.print_exc()
    '''

    print("*** 设备重启完成，重新连接telnet ***")
    try:
        tn = telnetlib.Telnet(host, port=23, timeout=10)
        tn.read_until(bytes('login: ', encoding="utf8"), timeout=5)
        tn.write(b'root\r\n')
        tn.read_until(bytes('Password: ', encoding="utf8"), timeout=5)
        tn.write(b'EXAMPLE_PASSWORD\r\n')
        tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)

        print("*** 设备升级重启成功，读取设备信息 ***")
        #tn.write(bytes("flashmanager -r /tmp/productinfo_test -p product-info > /dev/null 2>&1 \r\n", encoding="utf8"))
        #time.sleep(5)
        tn.write(bytes("getfirm DEV_ID\r\n", encoding="utf8"))
        time.sleep(5)
        res4 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
        output4 = str(res4, encoding="utf8")

        tn.write(bytes("getfirm PRODUCT_NAME\r\n", encoding="utf8"))
        time.sleep(5)
        res5 = tn.read_until(bytes('login:~# ', encoding="utf8"), timeout=5)
        output5 = str(res5, encoding="utf8")

        #tn.write(bytes("flashmanager -r /tmp/factoryinfo_test -p factory-info > /dev/null 2>&1 \r\n", encoding="utf8"))
        #time.sleep(5)

        print("*** 判断测试结果 ***")
        if "ZHYONL022E012" in output4 and "FW020" in output5:
            #print("factory-info文件信息：" + output5)
            print(output4)
            print(output5)

            print("*** 重置sunmilog token *** ")
            tn.write(bytes("flashmanager -e -p log\r\n", encoding="utf8"))
            time.sleep(5)
            tn.write(bytes("/etc/init.d/sunmilogd restart\r\n", encoding="utf8"))
            time.sleep(5)

            # 关闭连接"
            print("*** 关闭telnet连接 ***")
            tn.close()
            print("============================ 测试PASS ============================== ")
            time.sleep(60)
        else:
            print("******************** 获取设备信息FAILED，测试终止 ******************** ")
            # 关闭连接
            print("*** 关闭telnet连接 ***")
            tn.close()
            break
    except Exception as e:
        traceback.print_exc()
