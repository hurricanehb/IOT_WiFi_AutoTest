# 无线接入
## 无线连接建立
### 信道适配
#### Sub 1G-US国家码全信道遍历
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Channel_Vali_001；类型：自动化；标签：HyperWiFi

**前置条件：**
1、miniAP配置US国家码
2、miniAP支持的信道列表：
**操作步骤：**
1、miniAP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历miniAP 1/2/4/8MHz频宽下所有信道
**预期结果：**
2、连接成功

---

#### Sub 1G-EU国家码800MHz频段全信道遍历
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Channel_Vali_002；类型：自动化；标签：HyperWiFi

**前置条件：**
1、miniAP配置EU国家码
2、miniAP支持的信道列表：
**操作步骤：**
1、miniAP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历miniAP 1MHz频宽下所有信道
**预期结果：**
2、连接成功

---

#### Sub 1G-EU国家码900MHz频段全信道遍历
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Channel_Vali_003；类型：自动化；标签：HyperWiFi

**前置条件：**
1、miniAP配置EU国家码
2、miniAP支持的信道列表：
**操作步骤：**
1、miniAP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历miniAP 1MHz频宽下所有信道
**预期结果：**
2、连接成功

---

#### 2.4G 全信道遍历
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Channel_Vali_004；类型：自动化；标签：WiFi

**前置条件：**
1、AP配置JP国家码
2、AP支持的信道列表：1~13
**操作步骤：**
1、AP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历AP 2.4G所有信道
**预期结果：**
2、连接成功

---

#### 5G 全信道遍历
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Channel_Vali_005；类型：自动化；标签：WiFi

**前置条件：**
1、AP配置US国家码
2、AP支持的信道列表：
5.2GHz频段：36, 40, 44, 48
DFS频段：52, 56, 60, 64，100, 104, ..., 140, 144
5.8GHz频段：149, 153, 157, 161, 165
**操作步骤：**
1、AP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历AP 5G所有信道
**预期结果：**
2、连接成功

---

#### wifi6E扩展频段全信道遍历
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Channel_Vali_006；类型：自动化；标签：WiFi

**前置条件：**
1. 
Wi-Fi 6E AP（接入点）覆盖所有扩展频段信道（信道132-220）
**操作步骤：**
1、AP修改频宽信道
2、STA进入设置-网络和互联网，点击“WLAN”，进行开启，进行HyperWiFi网络连接
3、遍历AP WiFi6E所有信道
**预期结果：**
2、连接成功

---

### SSID密码字符处理
#### UTF-8编码SSID切换连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_002；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、陪测AP1、AP2，并配置UTF-8编码方式中文SSID
**操作步骤：**
1、进入设置-网络和互联网-无线列表

2、输入正确的密码连接AP1
3、输入正确的密码连接AP2
4、已保存AP1和AP2状态下手动切换连接
**预期结果：**
2、连接成功
3、切换连接成功
4、正常切换连接

---

#### GBK编码SSID切换连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_003；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、陪测AP1、AP2，并配置GBK编码方式中文SSID
**操作步骤：**
1、进入设置-网络和互联网-无线列表

2、输入正确的密码连接AP1
3、输入正确的密码连接AP2
4、已保存AP1和AP2状态下手动切换连接
**预期结果：**
2、连接成功
3、切换连接成功
4、正常切换连接

---

#### Shift_JIS编码SSID切换连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_004；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、陪测AP1、AP2，并配置 Shift_JIS编码日文字符SSID
**操作步骤：**
1、进入设置-网络和互联网-无线列表

2、输入正确的密码连接AP1
3、输入正确的密码连接AP2
**预期结果：**
2、连接成功
3、切换连接成功

---

#### CP949编码SSID切换连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_005；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、陪测AP1、AP2，并配置CP949编码方式韩文字符SSID
**操作步骤：**
1、进入设置-网络和互联网-无线列表

2、输入正确的密码连接AP1
3、输入正确的密码连接AP2
**预期结果：**
2、连接成功
3、切换连接成功

---

#### 网络详情-UTF-8编码SSID“分享二维码”选项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_006；类型：手工；标签：WiFi

**前置条件：**
1、设备恢复出厂
2、陪测试设备为AP，并配置UTF-8编码方式中文SSID
**操作步骤：**
1、AP互联网正常
2、DUT连接无线，点击查看网络详情-点击“分享二维码”
3、使用其他终端扫描二维码，检查无线连接情况
**预期结果：**
2、SSID密码等信息显示正确
3、连接无线成功

---

#### 网络详情-GBK编码SSID“分享二维码”选项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_007；类型：手工；标签：WiFi

**前置条件：**
1、设备恢复出厂
2、陪测试设备为AP，并配置GBK编码方式中文SSID
**操作步骤：**
1、AP互联网正常
2、DUT连接无线，点击查看网络详情-点击“分享二维码”
3、使用其他终端扫描二维码，检查无线连接情况
**预期结果：**
2、SSID密码等信息显示正确
3、连接无线成功

---

#### 网络详情- Shift_JIS编码SSID“分享二维码”选项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_008；类型：手工；标签：WiFi

**前置条件：**
1、设备恢复出厂
2、陪测试设备为AP，并配置 Shift_JIS编码日文字符SSID
**操作步骤：**
1、AP互联网正常
2、DUT连接无线，点击查看网络详情-点击“分享二维码”
3、使用其他终端扫描二维码，检查无线连接情况
**预期结果：**
2、SSID密码等信息显示正确
3、连接无线成功

---

#### 网络详情-CP949编码SSID“分享二维码”选项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_009；类型：手工；标签：WiFi

**前置条件：**
1、设备恢复出厂
2、陪测试设备为AP，并配置CP949编码方式韩文字符SSID
**操作步骤：**
1、AP互联网正常
2、DUT连接无线，点击查看网络详情-点击“分享二维码”
3、使用其他终端扫描二维码，检查无线连接情况
**预期结果：**
2、SSID密码等信息显示正确
3、连接无线成功

---

#### (SSID 1位+密码8位) “数字”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_001；类型：自动化；标签：Common

**前置条件：**
1、陪测试设备为锐捷AP720-A/miniAP
**操作步骤：**
1、AP的SSID为：0，密码：24681357
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### (SSID +密码)16位 "组合字符”正常连接
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_002；类型：自动化；标签：Common

**前置条件：**
1、陪测试设备为锐捷AP720-A/miniAP
**操作步骤：**
1、AP的SSID为16位组合字符（包含中、英、数、特殊字符组合），密码为16位组合字符（包含英、数、特殊字符组合）
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### (SSID +密码)32位 “特殊字符”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_003；类型：自动化；标签：Common

**前置条件：**
1、陪测试设备为锐捷AP720-A/miniAP
**操作步骤：**
1、AP的SSID和密码为：~!@#$%^&*()_+-={}|[]\:";'<>?,./
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### (SSID 32位+密码64位) “英文字符”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_004；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为32位英文字符，密码为64位英文字符
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID “小表情符号”正常连接
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_005；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：小表情
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID全空格正常连接
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_006；类型：手工；标签：Common

**前置条件：**
1、陪测试设备为锐捷AP720-A/miniAP
**操作步骤：**
1、AP的SSID为：空格
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID UTF-8 1位“中文字符”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_007；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：哈
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID UTF-8 10位“中文字符”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_008；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：哈哈哈哈哈哈哈哈哈哈
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID GBK 1位“中文字符”正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_009；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：哈
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID GBK 16位“中文字符”正常连接
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_010；类型：自动化；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：上海商米科技集团有限责任公司深圳，密码：24681357
2、sta进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID Shift_JIS编码（日文）1个字符正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_011；类型：自动化；标签：WiFi

**前置条件：**
暂无AP设备支持配置
**操作步骤：**
1、AP的SSID为：1个日文
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID Shift_JIS编码（日文）16个字符正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_012；类型：自动化；标签：WiFi

**前置条件：**
暂无AP设备支持配置
**操作步骤：**
1、AP的SSID为：16个日文，密码：24681357
2、sta进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID CP949编码（韩文）1个字符正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_013；类型：自动化；标签：WiFi

**前置条件：**
暂无AP设备支持配置
**操作步骤：**
1、AP的SSID为：1个韩文
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### SSID CP949编码（韩文）16个字符正常连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_SsidPwd_Vali_014；类型：自动化；标签：WiFi

**前置条件：**
暂无AP设备支持配置
**操作步骤：**
1、AP的SSID为：16个韩文，密码：24681357
2、sta进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### 中文SSID字符编码格式变化
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_SsidPwd_Excp_001；类型：手工；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP配置UTF-8编码10位SSID，STA输入正确的密码连接
2、AP改配GBK编码，SSID名称保持不变，检查STA连接状态
3、AP改配回UTF-8编码，SSID名称保持不变，检查STA连接状态
**预期结果：**
1、连接成功
2、自动重连成功？？
3、自动重连成功？？

---

### 网络侧加密方式适配
#### AP设置无线加密方式为WEP-40
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_001；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（HW AirEngineer9700S-S）配置加密方式：WEP-40，密码：12345
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WEP
3、连接成功，ping包正常，安全性显示：WEP
4、自动重连成功

---

#### AP设置无线加密方式为WEP-104
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_002；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（HW AirEngineer9700S-S）配置加密方式：WEP-104，密码：1234567890123
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WEP
3、连接成功，ping包正常，安全性显示：WEP
4、自动重连成功

---

#### AP设置无线加密方式为WEP-128
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_003；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（HW AirEngineer9700S-S）配置加密方式：WEP-128，密码：1234567890123
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WEP
3、连接成功，ping包正常，安全性显示：WEP
4、自动重连成功

---

#### AP设置无线加密方式为WPA-CCMP
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_004；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA-CCMP
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA-TKIP/CCMP
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_005；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA-TKIP或CCMP
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-TKIP
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_006；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-TKIP
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-CCMP，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_007；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-CCMP，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-CCMP，可选开启pmf
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Encrypt_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-CCMP，可选开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-CCMP，关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_009；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-CCMP，关闭pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-TKIP或CCMP，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_010；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-TKIP或CCMP，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-TKIP或CCMP，可选开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_011；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-TKIP或CCMP，可选开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA2-TKIP或CCMP，关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_012；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA2-TKIP或CCMP，关闭pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2混合，TKIP加密
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_013；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，TKIP加密
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2混合，CCMP加密，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_014；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，CCMP加密，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2混合，CCMP加密，可选开启pmf
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Encrypt_Vali_015；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，CCMP加密，可选开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2混合，CCMP加密，关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_016；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，CCMP加密，关闭pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_017；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，TKIP或CCMP加密，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，可选开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_018；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，TKIP或CCMP加密，可选开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_019；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA/WPA2混合，TKIP或CCMP加密，关闭pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Personal
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Personal
4、自动重连成功

---

#### WPA2/WPA3混合，可选启用pmf
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_020；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置可选pmf
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、有安全锁
2、连接成功
3、连接成功，ping包正常，安全性显示：
，安全性显示：WPA3

---

#### WPA2/WPA3混合，强制启用pmf（暂无AP支持配置强制开启或关闭pmf）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_021；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置强制启用pmf
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、有安全锁
2、连接成功
3、连接成功，ping包正常，安全性显示：
，安全性显示：WPA3

---

#### WPA2/WPA3混合，强制关闭pmf（暂无AP支持配置强制开启或关闭pmf）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_022；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：HW AirEngineer9700S-S可联网，wpa/wpa3混合加密、配置强制关闭pmf
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、有安全锁
2、连接成功
3、连接成功，ping包正常，安全性显示：
，安全性显示：WPA3

---

#### AP设置无线加密方式为WPA3加密，禁用AE_PK，禁用OCV（暂无AP支持配置）
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_023；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 陪测AP：Ruckus R770，已配置禁用AE_PK，禁用OCV
**操作步骤：**
1、DUT无线连接AP，查看密码弹窗的无线安全性显示
2、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3加密，禁用SAE_PK，启用OCV（暂无AP支持配置）
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_024；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 陪测AP：Ruckus R770，已配置禁用SAE_PK，启用OCV
**操作步骤：**
1、DUT无线连接AP，查看密码弹窗的无线安全性显示
2、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3加密，启用SAE_PK，禁用OCV（暂无AP支持配置）
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_025；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 陪测AP：Ruckus R770，已配置启用SAE_PK，禁用OCV
**操作步骤：**
1、DUT无线连接AP，查看密码弹窗的无线安全性显示
2、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3加密，启用SAE_PK，启用OCV（暂无AP支持配置）
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_026；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 陪测AP：Ruckus R770，已配置启用SAE_PK，启用OCV
**操作步骤：**
1、DUT无线连接AP，查看密码弹窗的无线安全性显示
2、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级，CCMP加密，可选开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_027；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
3、备注：miniAP 采用的是CCMP加密方式
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA3个人级，CCMP加密，可选开启pmf
miniAP修改pmf=1：编辑文件vim /lib/halow/nrcwifi.lua
ap修改函数gen_hostapd_conf的file:write(string.format("ieee80211w=%d\n", 1)) ）
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级，CCMP加密，强制开启pmf
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Encrypt_Vali_028；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、拓扑：miniAP有线连接上级路由器
3、备注：miniAP 采用的是CCMP加密方式
**操作步骤：**
1.AP（H3C WX2510H）配置：WPA3个人级，CCMP加密，强制开启pmf
miniAP设置PMF为2 （编辑文件vim /lib/halow/nrcwifi.lua
ap修改函数gen_hostapd_conf的file:write(string.format("ieee80211w=%d\n", 2)) ）
2、DUT无线连接miniAP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级，CCMP加密，强制关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_029；类型：手工；标签：WiFi

**前置条件：**
1、测试环境：办公室
2、拓扑：miniAP有线连接上级路由器
3、备注：miniAP 采用的是CCMP加密方式
**操作步骤：**
1.AP（H3C WX2510H）配置：WPA3个人级，CCMP加密，强制关闭pmf
miniAP设置PMF为0 （编辑文件vim /lib/halow/nrcwifi.lua
ap修改函数gen_hostapd_conf的file:write(string.format("ieee80211w=%d\n", 0)) ）
2、DUT无线连接miniAP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级，AES256GCM加密，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_030；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（HW AirEngineer9700S-S）配置：WPA3个人级，AES256GCM加密，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_031；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA3个人级过渡模式，CCMP加密，强制开启pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2/WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，关闭pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_032；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）配置：WPA3个人级过渡模式，CCMP加密，关闭pmf
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2/WPA3-Personal
3、连接成功，ping包正常，安全性显示：WPA3-Personal
4、自动重连成功

---

#### AP设置无线加密方式为WPA3企业级过渡模式-CCMP
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_033；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）：WPA3企业级过渡模式
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA2/WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA2/WPA3-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA3企业级only模式-CCMP
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_034；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）：WPA3企业级only模式
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA3-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA3企业级-GCMP（无可配ACAP）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Encrypt_Vali_035；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）：WPA3企业级-GCMP
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA3-Enterprise 192bit
4、自动重连成功

---

#### AP设置无线加密方式为WPA3企业级192bit模式-GCMP
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Encrypt_Vali_036；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）：WPA3企业级192bit模式
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA3-Enterprise 192bit
4、自动重连成功

---

#### AP设置无线加密方式为WPA3企业级192bit模式-CNSA（政府军用）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Encrypt_Vali_037；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、AP（H3C WX2510H）：WPA3企业级192bit模式-CNSA
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA3-Enterprise 192bit
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级CCMP加密，可选开启PMF
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_038；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：CCMP
PMF：可选开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级CCMP加密，关闭PMF
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_039；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：CCMP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，强制开启PMF
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_040；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：强制开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，可选开启PMF
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_041；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：可选开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，关闭PMF
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_042；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA2企业级TKIP加密
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_043；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级CCMP加密，强制开启PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_044；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：CCMP
PMF：强制开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA3-Enterprise
3、连接成功，ping包正常，安全性显示：WPA3-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级CCMP加密，可选开启PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_045；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：CCMP
PMF：可选开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级CCMP加密，关闭PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_046；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：CCMP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，强制开启PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_047；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：强制开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，可选开启PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_048；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：可选开启
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，关闭PMF
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_049；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP或CCMP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA/WPA2企业级TKIP加密
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_050；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为WPA企业级TKIP加密
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_051；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好企业级WiFi网络，可通外网
**操作步骤：**
1、陪测AP（H3C WX2510H）：
认证 方式：WPA2-Dot1x
加密套件：TKIP
PMF：关闭
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
5、遍历终端支持的各个<EAP方法+阶段2身份验证+证书>组合
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

#### AP设置无线加密方式为Open
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_052；类型：手工；标签：Common

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：可联网，双频合一/频宽信道auto/密码无/加密方式不加密
**操作步骤：**
1、陪测AP：可联网，双频合一/频宽信道auto/不加密
DUT无线连接AP
2、查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
2、无弹窗
3、连接成功，ping包正常，安全性显示：无

---

#### AP设置无线加密方式为OWE
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_053；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：H3C WX2520X-LI 可联网，OWE网络已配置好
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、无安全锁
2、连接成功
3、连接成功，ping包正常，安全性显示：Enhanced OPEN或OWE

---

#### AP设置无线加密方式为OWE过渡模式
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_054；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：HW AirEngineer9700S-S可联网，OWE过渡模式网络已配置好
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、无安全锁
2、连接成功
3、连接成功，ping包正常，安全性显示：
Enhanced OPEN或OWE/OPEN

---

#### AP设置开放型Portal网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_055；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：商米W1s，可联网，Portal网络已配置好
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、无安全锁
2、连接成功，跳转到web认证页面，无需输入密码点击连接认证成功
3、连接成功，ping包正常，安全性显示：无

---

#### AP设置密码认证型Portal网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_056；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：商米W1s，可联网，Portal网络已配置好
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、无安全锁
2、连接成功，跳转到web认证页面，输入正确的密码点击连接认证成功
3、连接成功，ping包正常，安全性显示：无

---

#### AP设置短信认证型Portal网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_057；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：商米W1s，可联网，Portal网络已配置好
**操作步骤：**
1、检查WLAN列表安全性显示
2、DUT无线连接AP
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
**预期结果：**
1、无安全锁
2、连接成功，跳转到web认证页面，输入手机号和验证码点击连接认证成功
3、连接成功，ping包正常，安全性显示：无

---

#### AP设置mac接入网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Encrypt_Vali_058；类型：手工；标签：WiFi

**前置条件：**
1、 网络拓扑：AP--STA；
2、DUT出厂状态
3、陪测AP：HW AirEngineer9700S-S，可联网，MAC认证网络已配置好
**操作步骤：**
1、陪测AP启用mac认证功能，已允许设备mac接入网络已配置好
2、DUT使用本机mac（设备mac已添加）无线连接AP，观察连接情况
3、DUT使用随机mac连接AP，观察连接情况
**预期结果：**
2、连接成功
3、连接失败

---

#### AP设置无线加密方式为WAPI-PSK
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Encrypt_Vali_059；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 传统 WiFi AP已配置好WAPI-PSK WiFi网络，可通外网
**操作步骤：**
1、AP配置：
安全策略：WAPI
认证方式：PSK
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WAPI PSK
3、连接成功，ping包正常，安全性显示：WAPI PSK
4、自动重连成功

---

#### AP设置无线加密方式为WAPI证书认证--终端未适配，缺测试环境
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Encrypt_Vali_060；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 传统 WiFi AP已配置好WAPI证书认证网络，可通外网
**操作步骤：**
1、AP配置：
安全策略：WAPI
认证方式：证书认证
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、连接成功后，DUT ping网关ip，并点击已连SSID右侧的”配置“图标，查看安全性显示
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WAPI
3、连接成功，ping包正常，安全性显示：WAPI
4、自动重连成功

---

#### AC+AP场景启用FT属性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_061；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 传统 WiFi AP已配置好漫游环境，并启用FT属性，可通外网
**操作步骤：**
1、陪测AP（HW AirEngineer9700S-S）：
认证 方式：WPA2-Dot1x
加密套件：AES
PMF：关闭
11r快速漫游属性：启用
2、DUT无线连接AP，查看密码弹窗的无线安全性显示
3、输入正确的认证配置连接
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、安全性显示：WPA/WPA2-Enterprise
3、连接成功，ping包正常，安全性显示：WPA/WPA2-Enterprise
4、自动重连成功

---

### STA侧连接企业级WiFi EAP方式适配
#### STA选择PWD方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_001；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PWD
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_CA证书_首次使用时信任方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_002；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：首次使用时信任
在线证书状态：不验证
域名：server
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_CA证书_安装证书方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_003；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：安装证书
2、重新进入连接配置页面，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：步骤1安装的证书
在线证书状态：不验证
域名：server
身份：steve
密码：testing
3、检查STA连接状态
4、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
1、跳转到证书安装页面
3、连接成功
4、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_已有CA证书_不验证证书在线状态方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_004；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：目标证书
在线证书状态：不验证
域名：server
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_已有CA证书_需要证书状态（非强制）方式连接
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_EAP_Vali_005；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：目标证书
在线证书状态：需要证书状态（非强制）
域名：server
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_已有CA证书_需要证书状态式连接
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_EAP_Vali_006；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：目标证书
在线证书状态：需要证书状态
域名：server
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_MSCHAPV2_CA证书-不验证方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_007；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
2、金融系列因安全性原因未导入该选项
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：MSCHAPV2
CA证书：不验证证书
域名：server
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_GTC方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：GTC
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_SIM方式连接
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_EAP_Vali_009；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：SIM
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_AKA方式连接
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_EAP_Vali_010；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：AKA
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择PEAP_AKA'方式连接WiFi
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_EAP_Vali_011；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：PEAP
阶段2：AKA'
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择TLS_方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_012；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：TLS
CA证书：目标证书
用户证书：目标证书
身份：steve
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择TTLS_PAP方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_013；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：TTLS
阶段2：PAP
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择TTLS_MSCHAP方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_014；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：TTLS
阶段2：MSCHAP
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择TTLS_MSCHAPV2方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_015；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：TTLS
阶段2：MSCHAPV2
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### STA选择TTLS_GTC方式连接
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Vali_016；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好WPA/WPA2企业级WiFi网络，可通外网
**操作步骤：**
1、点击目标AP SSID进行连接，STA按照以下配置进行连接：
EAP：TTLS
阶段2：GTC
身份：steve
密码：testing
2、检查STA连接状态
3、关闭WLAN开关再打开，检查自动重连是否正常
**预期结果：**
2、连接成功
3、自动重连成功

---

#### WEP/WPA系列密码错误
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_EAP_Excp_001；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、STA选择目标AP输入错误密码连接
2、检查连接状态
**预期结果：**
2、连接失败，提示请检查密码后重试

---

#### 802.1X认证失败-错误的用户名、密码
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_002；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络
**操作步骤：**
1、STA选择目标AP输入错误的用户名或密码连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-客户端证书不匹配
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_003；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络
**操作步骤：**
1、STA选择目标AP通过证书认证方式，并选择错误的客户端证书进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-CA证书过期
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_004；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络
**操作步骤：**
1、STA选择目标AP通过证书认证方式，并选择过期的CA证书进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-CA证书不匹配
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_005；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络
**操作步骤：**
1、STA选择目标AP通过证书认证方式，并选择错误的CA证书进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-域名不匹配
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_006；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络
**操作步骤：**
1、STA选择目标AP通过证书认证方式，并输入错误的域名进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-radius服务器交互异常（无响应、超时、拒绝等）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_007；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络，server端禁用服务器
**操作步骤：**
1、STA选择目标AP进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

#### 802.1X认证失败-eap方式不匹配
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_EAP_Excp_008；类型：手工；标签：WiFi

**前置条件：**
1. 已配置好企业级WiFi网络，server端禁用PWD认证方式
**操作步骤：**
1、STA选择目标AP通过PWD方式并输入正确的用户名密码进行连接
2、检查连接状态
**预期结果：**
2、连接失败

---

### 扫码添加网络
#### +添加网络入口扫码连接测试
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Scanner_Vali_001；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2
**操作步骤：**
1、设置-网络和互联网-WLAN-添加网络，点击入口处“扫码”图标
2、扫码已有的无线二维码
**预期结果：**
2、无线信息被保存，且主动连接成功

---

#### 添加网络设置-扫码连接测试
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Scanner_Vali_002；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2
**操作步骤：**
1、设置-网络和互联网-WLAN-添加网络，点击SSID编辑处“扫码”图标
2、扫码已有的无线二维码
**预期结果：**
2、无线信息被保存，且主动连接成功

---

#### 扫码添加全特殊字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_003；类型：手工；标签：Common

**前置条件：**
1、AP配置ssid为~!@#$%^&*()_+-={}|[]\:";'<>?,./，密码为~!@#$%^&*()_+-={}|[]\:";'<>?,./
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加空格字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_004；类型：手工；标签：Common

**前置条件：**
1、AP配置ssid为空格，密码为8个空格
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加组合字符网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Scanner_Vali_005；类型：手工；标签：Common

**前置条件：**
1、AP配置ssid为"123 'test' 测试 //\\"，密码为"123 'test' //\\"
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加AP SSID UTF-8编码10个中文字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_006；类型：手工；标签：WiFi

**前置条件：**
1、AP配置ssid为UTF-8编码格式的中文字符，密码为"123 'test' //\\"
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加AP SSID GBK编码16个中文字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_007；类型：手工；标签：WiFi

**前置条件：**
1、AP配置为GBK编码格式的中文字符，密码为"123 'test' //\\"
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加AP SSID Shift_JIS编码16个日文字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1、AP配置ssid为Shift_JIS编码的16个日文字符
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 扫码添加AP SSID CP949编码韩文字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_009；类型：手工；标签：WiFi

**前置条件：**
1、AP配置ssid为CP949编码韩文字符
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

### 手动输入添加网络
#### 手动添加网络配置：(SSID 1位+密码8位) “英文字符”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_001；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、AP的SSID为：a，密码：qwertyui
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：(SSID +密码)16位 “组合字符”
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_Manual_Vali_002；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、AP的SSID为：12 /"测试'Test ，密码：12345 Test/"'~!@
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：(SSID +密码)32位 “特殊字符”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_003；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、AP的SSID和密码为：~!@#$%^&*()_+-={}|[]\:";'<>?,./（需遍历所有特殊字符）
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：(32位SSID +64位密码) “数字字符”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_004；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、AP的SSID为32位数字，密码为64位数字
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：SSID “小表情符号”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_005；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、AP的SSID为：12345678acas?:"7890123456789012，密码12345678acas?:"789012345678901212345678acas?:"7890123456789012
2、无线列表，进行连接，ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：(SSID+密码)首中尾包含空格
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_006；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
2、陪测AP：可联网，双频合一/频宽信道auto/密码24681357/加密方式WPA-WPA2
**操作步骤：**
1、设置-网络和互联网-WLAN-添加网络
2、网络名称和密码编辑框输入： Test Test （首中尾均包含空格）
**预期结果：**
2、正常输入

---

#### 手动添加网络配置：AP SSID UTF-8编码10个“中文字符”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_007；类型：手工；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：哈哈哈哈哈哈哈哈哈哈
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：AP SSID GBK编码16个“中文字符”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1、陪测试设备为锐捷AP720-A
**操作步骤：**
1、AP的SSID为：上海商米科技集团有限责任公司深圳，密码：24681357
2、sta进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
5、重启sta，再次检查无线连接和ping包情况
**预期结果：**
2、正常显示目标ap ssid
3、连接成功
4、ping包正常
5、自动重连成功，ping包正常

---

#### 手动添加网络配置：AP SSID Shift_JIS编码16个日文字符
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_009；类型：手工；标签：WiFi

**前置条件：**
1、AP配置ssid为Shift_JIS编码的16个日文字符
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 手动添加网络配置：AP SSID CP949编码韩文字符
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_010；类型：手工；标签：WiFi

**前置条件：**
1、AP配置ssid为CP949编码韩文字符
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

---

#### 添加不存在的SSID
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_011；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN-添加网络
2、网络名称编辑框输入：不存在的网络（该SSID不存在），点击"保存“按钮
**预期结果：**
2、连接失败
3、列表中存在添加的网络

---

#### 未连接状态，手动添加网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_012；类型：手工；标签：Common

**前置条件：**
1、dut处于未连接状态
**操作步骤：**
1、设置-网络和互联网-WLAN-添加网络
2、输入目标AP SSID密码信息，点击"保存“按钮
3、查看已保存的网络列表
**预期结果：**
2、连接成功
3、列表中存在添加的网络

---

#### 已连接状态，手动添加网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_013；类型：手工；标签：Common

**前置条件：**
1、环境中存在同类型网络ap1、ap2或miniAP1、miniAP2
2、DUT已连接ap1
**操作步骤：**
1、dut已连接ap1
2、DUT进入设置-网络和互联网-WLAN-添加网络
3、输入ap2无线信息，点击“保存”按钮
4、查看已保存的网络列表
**预期结果：**
1、连接ap1成功
3、dut从ap1断开切换连接到ap2，ap2无线信息保存成功
4、已保存网络列表中存在ap2网络信息

---

#### 安全性选择“无”
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_014；类型：手工；标签：Common

**前置条件：**
1、华三设置无线加密方式为Open
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“无”
4.点击“保存”按钮
注意：金融系列产品无该安全性选项
**预期结果：**
4.无线信息被保存，并且连接成功

---

#### 安全性选择“WEP”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_015；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WEP方式：12345
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WEP”
4.点击“保存”按钮
注意：金融系列产品无该安全性选项
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2/WPA3-Enterprise”
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_016；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2/WPA3-Enterprise”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-TKIP
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_017；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA-TKIP方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-AES
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_018；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA-AES方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA-TKIP/AES
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_019；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA-TKIP/AES方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-TKIP
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_020；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA2-TKIP方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-AES
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_021；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA2-AES方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2-TKIP/AES
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_022；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA2-TKIP/AES方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA/WPA2-混合
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_023；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA/WPA2-混合方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA3-Personal”，AP设置无线加密方式为WPA3-Personal
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_024；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA3-Personal方式：24681357
**操作步骤：**
1、配置AP：隐藏SSID，WPA3-Personal方式
2.进入设置-WLAN界面
3.点击添加网络项，弹出添加网络提示框
4.输入正确网络SSID名称和密码，安全性选择“WPA3-Personal”
5.点击“保存”按钮
**预期结果：**
5.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA3-Personal”，AP设置无线加密方式为WPA3-SAE
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_025；类型：手工；标签：Common

**前置条件：**
1、华三设置无线加密为WPA3-SAE方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA3-Personal”
4.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 安全性选择“WPA/WPA2-Personal”，AP设置无线加密方式为WPA2/WPA3-混合
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_026；类型：手工；标签：WiFi

**前置条件：**
1、华三设置无线加密为WPA2/WPA3-混合方式：24681357
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
5.输入正确网络SSID名称和密码，安全性选择“WPA3-Personal”
6.点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功
6.wifi信息被保存，并且连接成功

---

#### 安全性选择“Enhanced Open”，手机热点设置无线加密方式为“开放”
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_027；类型：手工；标签：WiFi

**前置条件：**
1、手机热点安全设置为“Enhanced Open”
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“Enhanced Open”
4.点击“保存”按钮
注意：金融系列产品无该安全性选项
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 高级选项-隐藏的网络，选择是
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_028；类型：手工；标签：WiFi

**前置条件：**
1. 锐捷R730-L AP配置隐藏 SSID，编码方式gbk,，不加密；
2、DUT wifi处于未连接状态
3、A9以前才有，A11后选项入口被删除
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称，安全性选择无
4.点击高级选项，隐藏的网络选择“是”，点击“保存”按钮
**预期结果：**
4.wifi信息被保存，并且连接成功

---

#### 高级选项-隐藏的网络，选择是，GBK Encoding选择是
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_029；类型：手工；标签：WiFi

**前置条件：**
1. 锐捷R730-L AP配置隐藏 SSID，编码方式gbk,，不加密；
2、DUT wifi处于未连接状态
3、A9以前才有，A11后选项入口被删除
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称，安全性选择无
4.点击高级选项，隐藏的网络选择“是”，
5. GBK Encoding选择是，点击“保存”按钮
**预期结果：**
4.显示GBK编码方式选择框
5. wifi信息被保存，并且连接成功

---

#### 高级选项-隐藏的网络，选择是，GBK Encoding选择否
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Vali_030；类型：手工；标签：WiFi

**前置条件：**
1. 锐捷R730-L AP配置隐藏 SSID，编码方式utf-8,，不加密；
2、DUT wifi处于未连接状态
3、A9以前才有，A11后选项入口被删除
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称，安全性选择无
4.点击高级选项隐藏的网络选择“是”，
5.GBK Encoding选择否，点击“保存”按钮
**预期结果：**
4.显示GBK编码方式选择框
5. wifi信息被保存，并且连接成功

---

#### 高级选项-隐藏的网络，选择否
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_031；类型：手工；标签：WiFi

**前置条件：**
1. AP配置隐藏 SSID，不加密；
2、DUT wifi处于未连接状态
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称，安全性选择无
4.点击高级选项隐藏的网络选择“否”，
5.点击“保存”按钮
**预期结果：**
4.隐藏GBK编码方式选择框
5. wifi信息被保存，连接失败

---

#### ip设置-DHCP获取IP有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_032；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
3. AP配置不加密网络；
**操作步骤：**
1. 进入设置-WLAN界面
2. 点击添加网络项
3. 输入正确网络SSID名称，安全性选择无
4. 检查高级选项-IP设置默认配置
5. 点击“保存”按钮
6. WLAN界面点击已连接WIFI-编辑按钮，检查网络详情
7.STA ping网关
**预期结果：**
2. 弹出添加网络提示框 
4. 默认DHCP接入；
5. 连接成功
6. STA有IP：192.168.1.1x，网关：192.168.1.1，子网掩码：255.255.255.0，dns:192.168.1.1
7. ping通

---

#### ip设置-静态ip设置有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_033；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
3. AP配置不加密网络；
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项
3.输入正确网络SSID名称，安全性选择无
4.高级选项-IP设置选择静态，配置IP：192.168.1.11，网关：192.168.1.1
5.点击“保存”按钮
6.检查网络详情，
7. STA ping网关
8.WLAN界面点击已连接WIFI-编辑按钮，重复步骤4-6
**预期结果：**
2. 弹出添加网络提示框 
4. 配置成功
5. 连接成功，
6. STA网络信息与步骤4配置保持一致
7. ping通

---

#### ip设置-默认本机MAC有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_034；类型：手工；标签：WiFi

**前置条件：**
DUT为出厂状态
**操作步骤：**
1. 点击设置-网络和互联网-WLAN-点击需要连接的网络，输入密码，点击高级选项，隐私，选择使用设备MAC，点击连接
2. 点击连接的wifi，进入网络详情，查看设备MAC地址
**预期结果：**
1. wifi连接成功
2. 存在MAC地址，且为设备MAC地址

---

#### ip设置-随机MAC有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Manual_Vali_035；类型：手工；标签：WiFi

**前置条件：**
DUT为出厂状态
**操作步骤：**
1. 点击设置-网络和互联网-WLAN-点击需要连接的网络，输入密码，点击高级选项，隐私，选择使用随机MAC，点击连接
2. 点击连接的wifi，进入网络详情，查看随机MAC地址
**预期结果：**
1. wifi连接成功
2. 存在MAC地址，且为随机MAC地址

---

#### 手动添加网络配置：SSID密码含单引号
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Excp_001；类型：手工；标签：Common

**前置条件：**
1、AP的SSID为：'1234'5678'，密码：'1234'5678'
**操作步骤：**
1、AP的SSID为：'123'45678'，密码：'123'45678'
2、进入设置-网络和互联网，启用“WLAN”，查看无线列表展示情况
3、welcome-无线列表，选择目标AP输入正确的密码进行连接，检查连接情况
4、sta ping网关ip
**预期结果：**
2、正常显示目标ap ssid
3、连接成功，
4、ping包正常

---

#### 手动添加网络配置：SSID密码含双引号
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Excp_002；类型：手工；标签：Common

**前置条件：**
1、AP的SSID为："1234"5678"，密码："1234"5678"
**操作步骤：**
1、设置-网络和互联网-热点和网络共享-WLAN热点，开启WLAN热点
2、热点名称修改为："1234"5678"，确认
3、使用手机连接热点
**预期结果：**
2、修改成功
3、无线连接成功

---

#### 手动添加网络配置：安全性选择与AP配置不匹配
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Excp_003；类型：手工；标签：Common

**前置条件：**
1、AP无线配置WPA3-Personal加密
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项，弹出添加网络提示框
3.输入正确网络SSID名称和密码，安全性选择“WPA/WPA2-Personal”
4.点击“保存”按钮
**预期结果：**
4.无线信息被保存，连接失败

---

#### SSID长度>32位报错
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_001；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、手动输入SSID长度33位
**预期结果：**
2、超出部分无法输入或提示错误无法保存

---

#### SSID （UTF-8 编码）超长中文字符输入报错（不可选编码，未知最大长度限制）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_002；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、手动输入SSID 11位
**预期结果：**
1、保存成功

---

#### SSID （GBK 编码）超长中文字符输入报错（不可选，未知最大长度限制）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_003；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、手动输入SSID 17位
**预期结果：**
2、超出部分无法输入或提示错误无法保存

---

#### SSID （Shift_JIS编码）超长日文字符输入报错（不可选，未知最大长度限制）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_004；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、手动输入SSID 17位
**预期结果：**
1、保存成功

---

#### SSID （CP949编码）超长韩文字符输入报错（不可选，未知最大长度限制）
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_005；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、手动输入SSID 17位
**预期结果：**
2、超出部分无法输入或提示错误无法保存

---

#### 密码输入为空，“连接按键”置灰
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_006；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、不输入密码点击“连接”按钮
**预期结果：**
1、“连接按键”置灰不可操作

---

#### 密码长度<8位报错
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_007；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、输入7位密码
**预期结果：**
1、“连接按键”置灰不可操作

---

#### 密码长度>32位报错
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_008；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、输入33位密码
**预期结果：**
2、超出部分无法输入或提示错误无法保存

---

#### 密码长度>64位报错
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_009；类型：手工；标签：WiFi

**前置条件：**
无
**操作步骤：**
1、输入65位密码
**预期结果：**
2、超出部分无法输入或提示错误无法保存

---

#### 密码输入中文字符
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_Manual_UI_010；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、输入中文字符
**预期结果：**
2、提示非法字符无法保存

---

#### 隐藏网络STA重启重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Manual_Stb_001；类型：手工；标签：WiFi

**前置条件：**
1、AP配置隐藏网络
2、dut已保存网络列表只有目标隐藏网络
**操作步骤：**
1、dut已手动添加目标隐藏网络
2、dut重启系统，检查是否自动重连成功
3、压测2H，检查重连情况
**预期结果：**
2、自动重连成功
3、重连成功率100%

---

## IP分配
### 高级选项-IP设置
#### DHCP获取IP
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_IPCfg_Vali_001；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.、进入设置-WLAN设置界面
2、DUT无线连接AP，
3、检查网络详情
**预期结果：**
2. 连接成功，
3. 无线类型、mac、ip、网关、前缀长度、dns、链接速率

---

#### DHCP IP续约
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_Vali_002；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，租期2min；
**操作步骤：**
1.、进入设置-WLAN设置界面
2、DUT无线连接AP（租约时间设置5分钟），检查网络详情
3、DUT持续ping AP网关
4、2min后检查网络详情
**预期结果：**
2. 连接成功，DUT有IP：192.168.1.1x
2. 稳定ping通
3. IP保持不变

---

#### DHCP ip更新有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_Vali_003；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP1已运行DHCP服务器，IP pool：192.168.1/10~20；
3. AP2已运行DHCP服务器，IP pool：192.168.2/10~20；
**操作步骤：**
1.、进入设置-WLAN设置界面
2、DUT无线连接AP1，检查网络详情
3、DUT ping AP1网关
4、回退WLAN设置界面，DUT选择AP2连接，连接后，检查网络详情
5、DUT ping AP2网关
**预期结果：**
2、获取ip为192.168.1.x，网关：192.168.1.1，子网掩码：255.255.255.0，dns:192.168.1.1
3、ping通
4、获取ip为192.168.2.x，网关：192.168.2.1，子网掩码：255.255.255.0，dns:192.168.2.1

---

#### 静态IP，与AP同网段
**属性：** 优先级：P0；摘要：Func_WlanAccess_Conn_IPCfg_Vali_004；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项
3.输入正确网络SSID名称和密码
4.高级选项-IP设置选择静态，配置IP：192.168.1.11，网关：192.168.1.1
5.点击“保存”按钮
6.检查网络详情，
7. STA ping网关
8.WLAN界面点击已连接WIFI-编辑按钮，重复步骤4-6
**预期结果：**
2. 弹出添加网络提示框 
4. 配置成功
5. 连接成功，
6. STA网络信息与步骤4配置保持一致
7. ping通

---

#### 静态IP，与AP不同网段
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_Vali_005；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面
2.点击添加网络项
3.输入正确网络SSID名称和密码
4.高级选项-IP设置选择静态，配置IP：192.168.2.11，网关：192.168.2.1
5.点击“保存”按钮
6.检查网络详情，
7.STA ping网关
8.WLAN界面点击已连接WIFI-编辑按钮，重复步骤4-6
**预期结果：**
2. 弹出添加网络提示框 
4. 配置成功
5. 连接成功，
6. STA网络信息与步骤4配置保持一致
7. ping不通

---

#### DNS默认配置有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_Vali_006；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：Internet--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面，DUT无线连接AP
2.高级选项-IP设置选择静态，检查默认DNS
3.配置IP：192.168.1.11，网关：192.168.1.1，DNS1：默认，DNS2:默认，点击“保存”按钮
4.查看网络详情DNS信息
5.STA访问外网：百度等网站；
**预期结果：**
2. DNS1:8.8.8.8，DNS2:8.8.4.4
3. 配置成功
4. DNS信息：DNS1:8.8.8.8，DNS2:8.8.4.4
5. STA正常上网上网

---

#### DNS配置为网关ip有效性
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_Vali_007；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：Internet--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面，DUT无线连接AP
2.高级选项-IP设置选择静态
3.配置IP：192.168.1.11，网关：192.168.1.1，DNS1：192.168.1.1，DNS2:192.168.1.1，点击“保存”按钮
4.查看网络详情DNS信息
5.STA访问外网：百度等网站；
**预期结果：**
3. 配置成功
4. DNS信息：DNS1:192.168.1.1，DNS2:192.168.1.1
5. STA正常上网上网

---

#### DNS1正确+DNS2错误配置有效性
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_Vali_008；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：Internet--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面，DUT无线连接AP
2.高级选项-IP设置选择静态
3.配置IP：192.168.1.11，网关：192.168.1.1，DNS1：8.8.8.8，DNS2:192.168.10.1，点击“保存”按钮
4.查看网络详情DNS信息
5.STA访问外网：百度等网站；
**预期结果：**
3. 配置成功
4. DNS信息：DNS1:8.8.8.8，DNS2:192.168.10.1
5. STA正常上网上网

---

#### DNS1错误+DNS2正确配置有效性
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_Vali_009；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：Internet--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面，DUT无线连接AP
2.高级选项-IP设置选择静态
3.配置IP：192.168.1.11，网关：192.168.1.1，DNS1：192.168.10.1，DNS2:8.8.8.8，点击“保存”按钮
4.查看网络详情DNS信息
5.STA访问外网：百度等网站；
**预期结果：**
3. 配置成功
4. DNS信息：DNS1:192.168.10.1，DNS2:8.8.8.8
5. STA正常上网上网

---

#### DNS1错误+DNS2错误配置有效性
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_Vali_010；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：Internet--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1.进入设置-WLAN界面，DUT无线连接AP
2.高级选项-IP设置选择静态
3.配置IP：192.168.1.11，网关：192.168.1.1，DNS1：192.168.10.1，DNS2:192.168.20.1，点击“保存”按钮
4.查看网络详情DNS信息
5.STA访问外网：百度等网站；
**预期结果：**
3. 配置成功
4. DNS信息：DNS1:192.168.10.1，DNS2:192.168.20.1
5. STA无法上网

---

#### IP配置下电保存
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_Excp_001；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. .进入设置-WLAN界面，选择目标AP并配置IP设置-DHCP方式进行连接
2. 重启设备，等待STA自动重连成功后检查IP配置方式
3.点击“铅笔”图标修改IP设置-静态，并配置IP：192.168.1.11，网关：192.168.1.1，点击“保存”按钮后
4. 重启设备，等待STA自动重连成功后检查IP配置方式
**预期结果：**
1、连接成功
2、DHCP配置保持不变
3、保存成功
4、静态配置保持不变

---

#### 已连接网络，静态和DHCP互相切换
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_Excp_002；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. .进入设置-WLAN界面，选择目标AP并配置IP设置-DHCP方式进行连接后，检查网络详情
2.点击“铅笔”图标修改IP设置-静态，并配置IP：192.168.1.11，网关：192.168.1.1，点击“保存”按钮后， 检查网络详情
**预期结果：**
2. 连接成功，STA获取AP分配的IP：192.168.1.1x，网关：192.168.1.1，子网掩码：255.255.255.0，dns:192.168.1.1
3. 配置成功，STA网络信息与配置保持一致

---

### UI
#### 默认配置检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_UI_001；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”，查看IP设置配置
**预期结果：**
2、默认DHCP

---

#### 可选IP配置项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_UI_002；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”，查看IP设置配置
**预期结果：**
2、两种选项：DHCP、静态

---

#### 静态IP可配置项检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_IPCfg_UI_003；类型：手工；标签：Common

**前置条件：**
1、DUT出厂状态
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、高级选项-IP设置，选择静态，查看可配置项
**预期结果：**
2、可配置项：IP地址、网关、网络前缀长度、DNS1、DNS2

---

#### 静态ip-IP地址配置：ip正常格式输入
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_004；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、输入ip：192.168.1.x，点击“保存”
**预期结果：**
3、正常输入，保存成功

---

#### 静态ip-IP地址配置：静态ip-IP地址配置特殊字符输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_005；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、输入ip：~!，点击保存按钮
**预期结果：**
3、“保存”按钮置灰，不可操作

---

#### 静态ip-IP地址配置：静态ip-IP地址配置中文输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_006；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、输入ip：中文，点击保存按钮
**预期结果：**
3、“保存”按钮置灰，不可操作

---

#### 静态ip-IP地址配置：英文字母输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_007；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、输入ip：zxccxzc，点击保存按钮
**预期结果：**
3、“保存”按钮置灰，不可操作

---

#### 静态ip-IP地址配置：输入为空
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_008；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、输入ip：为空，点击保存按钮
**预期结果：**
3、“保存”按钮置灰，不可操作

---

#### 静态ip-网关配置：ip正常格式输入
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_009；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网关配置：192.168.1.x
**预期结果：**
3、正常输入

---

#### 静态ip-网关配置：特殊字符输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_010；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网关配置：~!
**预期结果：**
3、提示非法输入

---

#### 静态ip-网关配置：中文输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_011；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网关配置：中文
**预期结果：**
3、提示非法输入

---

#### 静态ip-网关配置：英文字母输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_012；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网关配置：zxccxzc
**预期结果：**
3、提示非法输入

---

#### 静态ip-网关配置：输入为空
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_013；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网关配置：为空
**预期结果：**
3、提示非法输入

---

#### 静态ip-网络前缀长度配置：正常格式输入
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_014；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网络前缀长度配置：24
**预期结果：**
3、正常输入

---

#### 静态ip-网络前缀长度配置：特殊字符输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_015；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网络前缀长度配置：~!
**预期结果：**
3、提示非法输入

---

#### 静态ip-网络前缀长度配置：中文输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_016；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网络前缀长度配置：中文
**预期结果：**
3、提示非法输入

---

#### 静态ip-网络前缀长度配置：英文字母输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_017；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、网络前缀长度配置：zxccxzc
**预期结果：**
3、提示非法输入

---

#### 静态ip-ip和网关不在同一网段
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_018；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、配置IP：192.168.0.10，网关：192.168.2.1，网络前缀：31
**预期结果：**
3、提示不在同一网段或禁止保存

---

#### 静态ip-DNS1配置：正常格式输入
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_019；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS1：223.5.5.5
**预期结果：**
3、正常输入

---

#### 静态ip-DNS1配置：特殊字符输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_020；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS1：~!
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS1配置：中文输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_021；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS1：中文
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS1配置：英文字母输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_022；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS1：zxccxzc
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS1配置：输入为空
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_023；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS1：空值
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS2配置：正常格式输入
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_024；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS2：223.5.5.5
**预期结果：**
3、正常输入

---

#### 静态ip-DNS2配置：特殊字符输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_025；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS2：~!
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS2配置：中文输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_026；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS2：中文
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS2配置：英文字母输入
**属性：** 优先级：P3；摘要：Func_WlanAccess_Conn_IPCfg_UI_027；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS2：zxccxzc
**预期结果：**
3、提示非法输入

---

#### 静态ip-DNS2配置：输入为空
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_IPCfg_UI_028；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、设置-网络和互联网-WLAN，开启WLAN，DUT进行无线连接AP
2、点击“无线密码编辑框”中的“高级选项”-IP设置，设置静态
3、DNS2：8.8.8.8，DNS2：空值
**预期结果：**
3、保存成功

---

## 网络检测
### 204检测
#### 204检测默认配置检查
**属性：** 优先级：P1；摘要：Func_WlanAccess_Network_204_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网正常
2、setting-特色功能，检查204开关默认情况
**预期结果：**
2、默认开启

---

#### 204开关开启，外网正常-双WiFi网络检测独立性
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网正常
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "networkmonitor"，并同步查看连接状态显示
**预期结果：**
2.1、WiFi和HyperWiFi分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，并TCP连接成功
2.2、关键字段isCaptivePortal: isSuccessful()=true
2.3、连接状态显示：已连接

---

#### 204开关开启，外网正常-LAN/WLAN/蜂窝检测独立性
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_003；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均可访问外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络检测状态
**预期结果：**
2.1、各链路分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，并TCP连接成功
2.2、关键字段isCaptivePortal: isSuccessful()=true

---

#### 204开关开启，外网正常-双WiFi网络连通性检测周期验证
**属性：** 优先级：P1；摘要：Func_WlanAccess_Network_204_Vali_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网异常（未设置重定向）
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
3、AP、miniAP外网异常（设置重定向）
4、重复步骤2，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min
4、按照10min的周期检测

---

#### 204开关开启，外网正常-LAN/WLAN/蜂窝检测周期验证
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_005；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均可访问外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min

---

#### 204开关开启，外网异常-双WiFi网络检测独立性
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_006；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网异常
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "networkmonitor"，并同步查看连接状态显示
**预期结果：**
2.1、WiFi和HyperWiFi分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，但是TCP连接失败
2.2、关键字段isCaptivePortal: isSuccessful()=false
2.3、连接状态显示：已连接到设备，但无法提供互联网连接

---

#### 204开关开启，外网异常-LAN/WLAN/蜂窝检测独立性
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_007；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均无外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络检测状态
**预期结果：**
2.1、各链路分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，并TCP连接成功
2.2、关键字段isCaptivePortal: isSuccessful()=true

---

#### 204开关开启，外网异常-双WiFi网络连通性检测周期验证
**属性：** 优先级：P1；摘要：Func_WlanAccess_Network_204_Vali_008；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网异常（未设置重定向）
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
3、AP、miniAP外网异常（设置重定向）
4、重复步骤2，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min
4、按照10min的周期检测

---

#### 204开关开启，外网异常-LAN/WLAN/蜂窝检测周期验证
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_009；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均无外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min

---

#### 204开关开启，外网正常与异常互切-双WiFi网络连通性验证
**属性：** 优先级：P1；摘要：Func_WlanAccess_Network_204_Vali_010；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网正常
2、DUT依次连接WiFi、HyperWiFi，查看连接状态显示
3、拔掉AP、miniAP外网网线，使得互联网异常，30s后观察双WiFi连接状态显示
4、通过浏览器访问百度、腾讯，30s后观察双WiFi连接状态显示
5、接上AP、miniAP外网网线，使得互联网恢复正常，观察双WiFi连接状态显示，后台logcat | grep -i "networkmonitor"
**预期结果：**
2、显示：已连接
3、显示：已连接
4、显示：已连接到设备，但无法提供互联网连接
5、后台查看到下一个检测周期后，连接状态显示为：已连接

---

#### 204开关开启，外网正常与异常互切-LAN/WLAN/蜂窝网络连通性验证
**属性：** 优先级：P1；摘要：Func_WlanAccess_Network_204_Vali_011；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、各链路外网正常
2、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，检查网络检测状态
3、断开各链路上级外网，
4、通过浏览器访问百度、腾讯，检查网络检测状态
5、恢复各链路上级外网，查看网络检测状态
**预期结果：**
2、显示：已连接
3、显示：已连接
4、显示：已连接到设备，但无法提供互联网连接
5、后台查看到下一个检测周期后，连接状态显示为：已连接

---

#### 204开关开启，外网正常与异常：一条正常、一条不正常
**属性：** 优先级：P3；摘要：Func_WlanAccess_Network_204_Vali_012；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网正常
2、DUT依次连接WiFi、HyperWiFi，查看连接状态显示
3、拔掉AP、miniAP外网网线，使得互联网异常，30s后观察双WiFi连接状态显示
4、通过浏览器访问百度、腾讯，30s后观察双WiFi连接状态显示
5、接上AP、miniAP外网网线，使得互联网恢复正常，观察双WiFi连接状态显示，后台logcat | grep -i "networkmonitor"
**预期结果：**
2、显示：已连接
3、显示：已连接
4、显示：已连接到设备，但无法提供互联网连接
5、后台查看到下一个检测周期后，连接状态显示为：已连接

---

#### 204开关关闭，双WiFi网络连通性验证
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Vali_013；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP外网正常
2、setting-特色功能，关闭204开关，同步后台logcat | grep -i "networkmonitor"
3、DUT依次连接WiFi、HyperWiFi，观察连接状态显示
**预期结果：**
3.1 后台查看到关键字打印isCaptivePortalDetectionEnabled: false
3.2 后台查看到没有发起DNS解析
3.3 连接状态显示：已连接

---

#### 204开关关闭，LAN/WLAN/蜂窝网络连通性验证
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Vali_014；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均可访问外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络检测状态
**预期结果：**
3.1 后台查看到关键字打印isCaptivePortalDetectionEnabled: false
3.2 后台查看到没有发起DNS解析

---

#### sta收到非正常的dns解析ip
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Excp_001；类型：手工；标签：Common

**前置条件：**
1、陪测AP、miniAP
2、router具有DNS劫持功能，如腾达路由器
**操作步骤：**
1、AP、miniAP外网异常
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "networkmonitor"，并同步查看连接状态显示
**预期结果：**
2.1、WiFi和HyperWiFi分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，但是TCP连接失败
2.2、关键字段isCaptivePortal: isSuccessful()=false
2.3、连接状态显示：已连接到设备，但无法提供互联网连接

---

#### 单网络断网恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Excp_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、sta依次连接portal WiFi（含认证），HyperWiFi
2、portal WiFi认证超时后检查sta双WiFi连接状态
3、重新进行Portal WiFi认证，检查sta双WiFi连接状态
**预期结果：**
1、WiFi和HyperWiFi分别发起检测且通过
2、WiFi显示“登录到网络”，HyperWiFi显示“已连接”
3、双WiFi显示“已连接”

---

#### LAN<->WLAN网络断网恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Excp_003；类型：手工；标签：Common

**前置条件：**
1、LAN连接router1，WLAN连接Router2&minIAP
**操作步骤：**
1、dut同时连接lan、wlan且有外网，检查连接状态
2、断开router1外网，检查连接状态
3、恢复router1外网，检查连接状态
4、断开router2外网，检查连接状态
5、恢复router2外网，检查连接状态
**预期结果：**
1、优先连接lan
2、切换到WLAN
3、切回LAN
4、保持LAN连接
5、保持LAN连接

---

#### WLAN<->蜂窝网络断网恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Excp_004；类型：手工；标签：Common

**前置条件：**
1、WLAN连接Router2&minIAP
**操作步骤：**
1、dut同时连接wlan、蜂窝且有外网，检查连接状态
2、断开router2外网，检查连接状态
3、恢复router2外网，检查连接状态
4、断开蜂窝外网（错误的apn），检查连接状态
5、恢复蜂窝外网（正确的apn），检查连接状态
**预期结果：**
1、优先连接WLAN
2、切换到蜂窝
3、切回LWLAN
4、保持WLAN连接
5、保持WLAN连接

---

#### 关闭204，连接无外网网络再启用204
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Excp_005；类型：手工；标签：Common

**前置条件：**
1、AP、miniAP无外网
**操作步骤：**
1、sta禁用204
2、依次连接WiFi、HyperWiFi，检查连接状态
3、sta启用204
4、观察双WiFi连接状态显示，后台logcat | grep -i "networkmonitor"
5、开关wlan，观察双WiFi连接状态显示，后台logcat | grep -i "networkmonitor"
**预期结果：**
2、显示已连接
3、配置成功
4、不立即触发检测
5.1、WiFi和HyperWiFi分别发起DNS解析 ：www.qualcomm.cn、connectivitycheck.gstatic.com、connect.rom.miui.com、www.google.com、connectivitycheck.platform.hicloud.com，但是TCP连接失败
5.2、关键字段isCaptivePortal: isSuccessful()=false
5.3、连接状态显示：已连接到设备，但无法提供互联网连接

---

#### portal网络识别
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Int_001；类型：手工；标签：WiFi

**前置条件：**
1、AP外网正常
2、sta启用204
**操作步骤：**
1、连接到portal网络，检查连接状态，后台logcat | grep -i "networkmonitor"
**预期结果：**
1、显示“需要登录”，自动跳转到登录页面，isPortal=true RedirectURL=xxx

---

#### 设备休眠 / 锁屏后状态下的 204 检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Int_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
3、sta启用204
**操作步骤：**
1、AP、miniAP外网正常，sta连接双WiFi
2、sta息屏后拔掉AP、miniAP外网网线，后台logcat | grep -i "networkmonitor"检查是否发起204检测
3、通过浏览器访问百度、腾讯，30s后观察双WiFi连接状态显示
4、后台logcat | grep -i "networkmonitor"检查是否发起204检测
**预期结果：**
2、未发起204检测
4、WiFi和HyperWiFi分别发起204检测

---

#### 双WiFi接入，主备链路切换后重新检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Int_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：屏蔽箱
2、陪测试设备为AP、miniAP
3、sta启用204
**操作步骤：**
1、AP、miniAP外网正常，sta连接双WiFi
2、调节衰减器改变双WiFi连接质量使sta发生主备切换，后台logcat | grep -i "networkmonitor"检查是否发起204检测
**预期结果：**
2、分别立即发起204检测

---

#### 网络重选后重新检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_204_Int_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：屏蔽箱
2、陪测试设备为AP1、AP2、miniAP1、miniAP2
3、sta启用204
**操作步骤：**
1、AP1、AP2外网正常，sta连接AP1，已保存AP2
2、调节衰减器使sta连接从AP1切换到AP2，后台logcat | grep -i "networkmonitor"检查是否发起204检测
3、miniAP1、miniAP2外网正常，sta连接miniAP1，已保存miniAP2
2、调节衰减器使sta连接从miniAP1切换到miniAP2，后台logcat | grep -i "networkmonitor"检查是否发起204检测
**预期结果：**
2、立即发起204检测
4、立即发起204检测

---

#### 204开关反复开启/关闭测试
**属性：** 优先级：P3；摘要：Func_WlanAccess_Network_204_Stb_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、反复关闭-开启204开关20次，DUT连接双WiFi，查看后台log打印的关键字
2、取消保存双WiFi
3、反复开启-关闭204开关20次，DUT连接双WiFi，查看后台log打印的关键字
**预期结果：**
1、打印关键字isCaptivePortalDetectionEnabled: true
3、打印关键字isCaptivePortalDetectionEnabled: false

---

### IpReachableMonitor检测
#### 正常接入，网关可达-IPV4
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_IpReachMon_Vali_001；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router启用DHCPs
**操作步骤：**
1、IP设置默认配置（DHCP）连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
**预期结果：**
2、双WiFi连接成功
3、分别触发检测

---

#### 正常接入，网关可达-IPV6
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Vali_002；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router启用DHCPs
**操作步骤：**
1、IP设置默认配置（DHCP）连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
**预期结果：**
2、双WiFi连接成功
3、分别触发检测

---

#### 静态ip可达性检测
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_IpReachMon_Vali_003；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router&miniAP禁用DHCPs
**操作步骤：**
1、IP设置-静态IP配置（与Router网关同一网段，且双WiFi IP相同）连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
**预期结果：**
2、双WiFi连接成功
3、分别触发检测

---

#### 周期性检测验证
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Vali_004；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router&miniAP禁用DHCPs：192.168.0.1/24
**操作步骤：**
1、IP设置-静态IP配置双WiFi IP:192.168.2.10，网关：192.168.2.1，掩码：255.255.255.0连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查网关可达性检测周期
**预期结果：**
2、无线先连接成功，约7.5s后断开连接
3、每 750ms 发送一次 NS 包，最多发送 10 次。如果在 10 × 750ms = 7.5秒 内都没有收到回应则判定邻居不可达

---

#### 连接WLAN，网关不可达
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Excp_001；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router&miniAP禁用DHCPs：192.168.0.1/24
**操作步骤：**
1、IP设置-静态IP配置双WiFi IP:192.168.2.10，网关：192.168.2.1，掩码：255.255.255.0连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
**预期结果：**
1、配置成功
2、双WiFi反复断连
3、分别触发检测，且检测失败：
03-02 10:54:05.432 2915 22666 W IpClient.bond0: [IpReachabilityMonitor] WARN ALERT neighbor went from: NeighborEvent{@235098910,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]} to: NeighborEvent{@235101212,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]}

03-02 10:54:05.433 2915 22666 W IpReachabilityMonitor: FAILURE: LOST_PROVISIONING, NeighborEvent{@235101212,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]}

---

#### 网关不可达，再恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Excp_002；类型：手工；标签：Common

**前置条件：**
1、拓扑：Internet--Router（AP）--miniAP
2、Router&miniAP禁用DHCPs：192.168.0.1/24
**操作步骤：**
1、IP设置-静态IP配置双WiFi IP:192.168.2.10，网关：192.168.2.1，掩码：255.255.255.0连接双WiFi
2、检查无线连接状态
3、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
4、Router改配DHCPs：192.168.2.1/24
5、查看日志：logcat | grep -iE “IpReachabilityMonitor”检查双WiFi是否分别触发网关可达性检测
**预期结果：**
1、配置成功
2、双WiFi反复断连
3、分别触发检测，且检测失败
4、配置成功
5、分别发起检测，且检测成功

---

#### 双WiFi接入独立检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Int_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP网关可达
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
**预期结果：**
2.WiFi和HyperWiFi分别发起网关可达性检测

---

#### 双WiFi不共网关，主网络断开后备链路变主链路重新触发检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Int_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
3、AP和miniAP不共网关
**操作步骤：**
1、AP、miniAP网关可达
2、DUT依次连接WiFi、HyperWiFi，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
3、断开主网络WiFi，检查连接状态
**预期结果：**
2.WiFi和HyperWiFi分别发起网关可达性检测
3、HyperWiFi切换为主网络，重新发起网关可达性检测（主备网络共网关不会重启发起检查检测）

---

#### 切换ap连接时重新检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Int_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：屏蔽箱环境
2、陪测试设备为AP1、AP2、miniAP1、miniAP2
**操作步骤：**
1、sta连接AP1，已保存AP2
2、调节衰减器使sta连接从AP1切换到AP2，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
3、sta连接miniAP1，已保存miniAP2
4、调节衰减器使sta连接从miniAP1切换到miniAP2，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
**预期结果：**
2、切换后立即发起网关可达性检测
4、切换后立即发起网关可达性检测

---

#### 漫游后触发检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Int_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：屏蔽箱环境
2、陪测试设备为AP1、AP2、miniAP1、miniAP2
**操作步骤：**
1、sta连接AP1，已保存AP2
2、调节衰减器使sta连接从AP1漫游到AP2，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
3、sta连接miniAP1，已保存miniAP2
4、调节衰减器使sta连接从miniAP1漫游到miniAP2，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
**预期结果：**
2、漫游后，系统会每 750ms 发送一次 NS 包，最多发送 5 次。如果在 5 × 750ms = 3.75秒 内都没有收到回应，就会判定新的网关不可达
4、漫游后，系统会每 750ms 发送一次 NS 包，最多发送 5 次。如果在 5 × 750ms = 3.75秒 内都没有收到回应，就会判定新的网关不可达

---

#### dhcp和静态ip切换后重新检测
**属性：** 优先级：P2；摘要：Func_WlanAccess_Network_IpReachMon_Int_005；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、AP、miniAP网关可达
2、DUT分别连接WiFi/HyperWiFi，IP设置配置“静态”，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
3、DUT分别连接WiFi/HyperWiFi，IP设置配置“DHCP”，后台logcat | grep -i "IpReachabilityMonitor"检查是否发起网关可达性检测
**预期结果：**
2、切换后立即发起网关可达性检测
3、切换后立即发起网关可达性检测

---

## 无线重连
### 无线重连开关
#### 开启“自动连接”开关
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_Switch_Vali_001；类型：手工；标签：Common

**前置条件：**
1、DUT已成功连接AP
2、屏蔽房或干扰少的环境
**操作步骤：**
1、在网络详情内，开启“自动连接”
2、WLAN开关-禁用启用，观察无线重连情况
**预期结果：**
1、设置成功
2、无线重连成功

---

#### 关闭“自动连接”开关
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_Switch_Vali_002；类型：手工；标签：Common

**前置条件：**
1、DUT已成功连接AP
2、屏蔽房或干扰少的环境
**操作步骤：**
1、在网络详情内，关闭“自动连接”
2、WLAN开关-禁用启用，观察无线重连情况
**预期结果：**
1、设置成功
2、无线重连失败

---

### 断连触发机制
#### Beacon Timeout 断连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、陪测试设备为AP、miniAP
**操作步骤：**
1、sta无线连接成功后下电AP
2、检查好sta连接状态
**预期结果：**
2、连续40 个 Beacon(约4s） 周期自动断开连接，并尝试重连或切换网络

---

#### 密码错误
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_002；类型：手工；标签：Common

**前置条件：**
1、AP、miniAP配置wpa3加密
**操作步骤：**
1、sta输入错误的密码连接目标AP
2、检查sta连接状态
**预期结果：**
2、连接失败，提示“密码错误”，且不会尝试自动重连

---

#### 认证超时
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_003；类型：手工；标签：Common

**前置条件：**
/
**操作步骤：**
实测未能构建实现条件
**预期结果：**
/

---

#### 认证失败
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_004；类型：手工；标签：Common

**前置条件：**
/
**操作步骤：**
如认证超时类
**预期结果：**
/

---

#### 关联失败
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_005；类型：手工；标签：Common

**前置条件：**
1、接入点满载
**操作步骤：**
1、sta连接目标AP
2、检查sta连接状态
**预期结果：**
2、反复断开重连

---

#### dhcp失败
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_006；类型：手工；标签：Common

**前置条件：**
1、AP、miniAP关闭DHCP服务器
**操作步骤：**
1、sta连接目标AP
2、检查sta连接状态
**预期结果：**
2、断开连接，显示“获取ip失败”
（正在连接...反复重连）

---

#### 网关不可达主动断连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Vali_007；类型：手工；标签：Common

**前置条件：**
1、AP、miniAP配置防ping或sta配置与AP、miniAP不同网段
**操作步骤：**
1、sta连接目标AP
2、检查sta连接状态
**预期结果：**
2、反复断开重连

---

#### 不自动重连黑名单内ap
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Int_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室工位
2、AC+AP拓扑，关闭陪测AP、miniAP的dhcp服务器
**操作步骤：**
1、sta连接陪测AP，观察连接状态
2、sta禁用启用wlan开关，观察重连情况
**预期结果：**
1、连接失败，提示ip获取失败
2、不自动重连

---

#### 自动重连无外网ap
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Int_002；类型：手工；标签：Common

**前置条件：**
1、陪测AP、miniAP无外网
**操作步骤：**
1、sta连接陪测AP，观察连接状态
2、sta禁用启用wlan开关，观察重连情况
**预期结果：**
1、连接成功，提示“已连接，但无法提供互联网”
2、自动重连成功，提示“已连接，但无法提供互联网”

---

#### 连续 7 次失败（认证、关联、dhcp）触发 Watchdog
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_Trigger_Int_003；类型：手工；标签：Common

**前置条件：**
1、陪测AP、miniAP关闭DHCPs
**操作步骤：**
1、sta连接陪测AP，观察连接状态
2、等待连续失败次数达到阈值（7次）后检查无线状态
3、启用陪测AP DHCPs，检查连接状态
**预期结果：**
1、连接失败
2、自动关闭在打开WLAN开关，尝试重连
3、自动重连成功

---

### 回连阈值
#### 2.4G回连阈值（-86dbm）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_RSSI_Vali_001；类型：手工；标签：WiFi

**前置条件：**
1、屏蔽环境
2、设备亮屏，WiFi断开连接
**操作步骤：**
1、屏蔽箱调节可调衰减器，使得DUT断开连接rssi -103
2、屏蔽箱调节可调衰减器，使得DUT的rssi 为-87
3、屏蔽箱调节可调衰减器，使得DUT的rssi 为-75
**预期结果：**
1、DUT断开连接
2、DUT不会回连
3、DUT回连成功

---

#### 5G回连阈值（-83dBm）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_RSSI_Vali_002；类型：手工；标签：WiFi

**前置条件：**
1、屏蔽环境
2、设备亮屏，WiFi断开连接
**操作步骤：**
1、屏蔽箱调节可调衰减器，使得DUT断开连接rssi -103
2、屏蔽箱调节可调衰减器，使得DUT的rssi 为-84
3、屏蔽箱调节可调衰减器，使得DUT的rssi 为-83
**预期结果：**
1、DUT断开连接
2、DUT不会回连
3、DUT回连成功

---

#### HyperWiFi回连阈值（-93dBm）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_RSSI_Vali_003；类型：手工；标签：HyperWiFi

**前置条件：**
1、屏蔽环境
2、设备亮屏，HyperWIFI断开连接
**操作步骤：**
1、屏蔽箱调节可调衰减器，使得DUT断开连接rssi -103
2、屏蔽箱调节可调衰减器，使得DUT的rssi 为-94
3、屏蔽箱调节可调衰减器，使得DUT的rssi 为-93
**预期结果：**
1、DUT断开连接
2、DUT不会回连
3、DUT回连成功

---

### 网络侧状态改变
#### AP系统重启
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_001；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
3. STA已经连接AP；
**操作步骤：**
1. AP下电再上电；
2. 观察STA连接状态，记录AP第一个Beacon到Association帧的时间差；
3. 重复步骤1-3 10次；
**预期结果：**
2. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改DHCP服务器配置
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_002；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. STA连接AP
2. AP DHCP服务器网关地址从192.168.1.1改配192.168.2.1
3. 观察STA连接状态和耗时
4. 重复步骤1-3 3次
**预期结果：**
1. 连接成功，STA IP ：192.168.1.1x
3. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改无线SSID
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_003；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP配置SSID1，密码1，STA连接AP，检查STA连通性；
2. AP改配SSID2，密码2，STA连接AP，检查STA连通性；
4. AP改配回SSID1、密码1，观察STA连接状态和耗时；
5. 重复步骤1-3 3次；
**预期结果：**
2. 连接成功，STA IP ：192.168.1.1x
3. 连接成功，STA IP ：192.168.1.1x
4. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改无线密码
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_004；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP配置SSID，密码1，STA连接AP，检查STA连通性；
2. AP保持SSID不变，改配密码2，观察STA连接状态和耗时；
4. AP保持SSID不变、改配回密码1，观察STA连接状态和耗时；
5. 重复步骤1-3 3次；
**预期结果：**
2. 连接成功，STA IP ：192.168.1.1x
3. 自动重连失败，报密码错误
4. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改加密方式-WPA/WPA2/WPA3
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_005；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP配置加密方式WPA2，密码24681357；
2. STA连接AP，检查STA连通性；
3. AP修改加密方式为WPA2->WPA2/WPA3，观察STA连接状态和耗时；
4. AP修改加密方式为WPA2->WPA3，观察STA连接状态和耗时；
5. 重复步骤1-3 3次；
**预期结果：**
1. 连接成功，STA IP ：192.168.1.1x
3. 自动重连成功，STA IP ：192.168.1.1x；
4. 自动重连成功，STA IP ：192.168.1.1x

---

#### AP修改加密方式-open和加密互切
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_006；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP WIFI默认配置；
2. STA连接AP，检查STA连通性；
3. AP修改加密方式为Open，观察STA连接状态和耗时；
4. AP修改加密方式为WPA/WPA2，观察STA连接状态和耗时；
5. 重复步骤1-3 3次；
**预期结果：**
1. 连接成功，STA IP ：192.168.1.1x
3. 自动重连失败；
4. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改无线频宽/信道
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_007；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP WIFI默认配置；
2. STA连接AP，检查STA连通性；
3. AP修改固定频宽和信道，观察STA接状态和耗时；
4. 重复步骤1-3 3次；
**预期结果：**
1. 连接成功，STA IP ：192.168.1.1x
3. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### AP修改无线模式
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. AP 2.4GWIFI配置工作模式为b/g/n；
2. STA连接AP，检查STA连通性；
3. AP 2.4GWIFI配置工作模式为b/g，观察STA连接状态和耗时；
4. 重复步骤1-3 3次；
**预期结果：**
1. 连接成功，STA IP ：192.168.1.1x
3. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### STA亮灭屏wifi重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Vali_009；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. STA连接AP后保持亮屏，AP下电再上电，记录AP第一个Beacon到 assoc resp帧的时间差；
2. STA连接AP后灭屏再亮屏，AP下电再上电，记录AP第一个Beacon到 assoc resp帧的时间差；
3. 重复步骤1-3 10次，记录数据；
**预期结果：**
1. 自动重连成功，耗时<10s，STA IP :192.168.1.1x
2. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### DHCP失败恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Excp_001；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、陪测AP、miniAP关闭DHCPs
2、sta连接陪测AP，观察连接状态
3、陪测AP启用DHCPs，检查连接状态
**预期结果：**
2、连接失败
3、连接成功

---

#### 认证失败恢复
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Excp_002；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1、陪测AP、miniAP关闭认证服务器
2、sta连接陪测AP，观察连接状态
3、启用认证服务器，检查连接状态
**预期结果：**
2、连接失败
3、连接成功

---

#### AP修改加密方式-WPA2和WPA3互切（含pmf配置）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Excp_003；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1、陪测AP配置WPA2加密，强制启用PMF
2、sta连接陪测AP，检查连接状态
3、陪测AP改配WPA3加密，强制启用PMF
4、检查连接状态
**预期结果：**
2、连接成功
4、自动重连成功

---

#### AP修改加密方式-WPA2和WPA2/WPA3互切（含pmf配置）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_ApChange_Excp_004；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AC--AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1、陪测AP配置WPA2加密，强制启用PMF
2、sta连接陪测AP，检查连接状态
3、陪测AP改配WPA2/WPA3加密，强制启用PMF
4、检查连接状态
**预期结果：**
2、连接成功
4、自动重连成功

---

### 多网络环境重连
#### 2.4G/5G双频（非漫游）
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_MultiAp_Vali_001；类型：手工；标签：WiFi

**前置条件：**
1、AP配置双频合一
**操作步骤：**
1、sta输入正确的密码连接目标AP
**预期结果：**
1、连接成功，频段可为2.4G/5G

---

#### 不同ap相同ssid自动连接
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_MultiAp_Vali_002；类型：手工；标签：Common

**前置条件：**
1. AP1和AP2配置相同ssid、密码，不同信道频宽
**操作步骤：**
1、ap1上电
2、sta输入正确的密码连接ap1
3、ap1下电，ap2上电
4、检查sta wifi连接状态
**预期结果：**
2、连接成功
4、自动连接成功

---

### STA发生状态改变
#### STA软重启自动重连
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_001；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；

3. STA已经连接AP；
**操作步骤：**
1. STA重启系统；
2. 观察STA连接状态和耗时；
**预期结果：**
2. 自动重连成功，STA IP :192.168.1.1x

---

#### STA开关机自动重连
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_002；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；

3. STA已经连接AP；
**操作步骤：**
1. STA关机再开机；
2. 观察STA连接状态和耗时；
**预期结果：**
2. 自动重连成功，STA IP :192.168.1.1x

---

#### setting页面-wlan开关“禁用启用”自动重连
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：miniAP有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、setting-互联网-wlan，DUT连上HyperWiFi网络
2、禁用启用“wlan”开关，查看HyperWiFi重连情况与耗时，并使用wifi魔盒ping网关，后台
logcat | grep -iE "setwifi|on real|connection to"
**预期结果：**
2.1、HyperWiFi网络重连成功，耗时 ≤ 8s，ping通网关
2.2、后台打印开启wlan后，发起扫描startSingleScan on real: wlan1，然后约8s左右connection to HyperWiFi网络

---

#### systemUI组件-wlan开关“禁用启用”自动重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：miniAP有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、SystemUI-wlan，DUT连上HyperWiFi网络
2、禁用启用“wlan”开关，查看HyperWiFi重连情况与耗时，并使用wifi魔盒ping网关，后台
logcat | grep -iE "setwifi|on real|connection to"
**预期结果：**
2.1、HyperWiFi网络重连成功，耗时 ≤ 8s，ping通网关
2.2、后台打印开启wlan后，发起扫描startSingleScan on real: wlan1，然后约8s左右connection to HyperWiFi网络

---

#### systemUI组件-飞行模式“禁用启用”自动重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_005；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：miniAP有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、systemUI-wlan，DUT连上HyperWiFi网络
2、点亮点灭“飞机”图标，查看HyperWiFi重连情况，使用wifi魔盒ping网关，后台
logcat | grep -iE "airplane|on real|connection to"
**预期结果：**
2.1、HyperWiFi网络重连成功，耗时 ≤ 8s，ping通网关
2.2、后台打印开启wlan后，发起扫描startSingleScan on real: wlan1，然后约8s左右connection to HyperWiFi网络

---

#### 网络详情切换隐私选项
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_006；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；

3. STA已经连接AP；
**操作步骤：**
1. 网络详情，隐私切换“随机MAC”；
2. 观察STA连接状态和耗时；
**预期结果：**
2. 1、弹窗提示“无线网络断开，正重新连接，请稍等xx秒”
2.2、自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### 网络详情切换IP设置选项
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_007；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；

3. STA已经连接AP；
**操作步骤：**
1. 网络详情，IP设置切换静态IP；
2. 观察STA连接状态和耗时；
**预期结果：**
2. 1、弹窗提示“无线网络断开，正重新连接，请稍等xx秒”
2.2、自动重连成功，耗时<10s，STA IP 与步骤1配置的静态IP保持一致

---

#### 改配WLAN高级设置选项
**属性：** 优先级：P2；摘要：Func_WlanAccess_Reconnect_StaChange_Vali_008；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；

3. STA已经连接AP；
**操作步骤：**
1. 进入Settings-网络和互联网-WLAN高级设置，修改WLAN频段/模式/漫游参数/模式/超时断连/优先级等参数
2. 观察STA连接状态和耗时；
**预期结果：**
2. 1、弹窗提示“无线网络断开，正重新连接，请稍等xx秒”
2.2、自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### STA开关机自动重连-超长GBK编码
**属性：** 优先级：P3；摘要：Func_WlanAccess_Reconnect_StaChange_Excp_001；类型：手工；标签：WiFi

**前置条件：**
1. 陪测试设备为锐捷AP720-A
2. AP配置16位GBK编码SSBD

3. STA已经连接AP；
**操作步骤：**
1. STA关机再开机；
2. 观察STA连接状态和耗时；
**预期结果：**
2. 自动重连成功，STA IP :192.168.1.1x

---

#### STA开关机自动重连-已保存多个GBK编码网络且共网关
**属性：** 优先级：P3；摘要：Func_WlanAccess_Reconnect_StaChange_Excp_002；类型：手工；标签：WiFi

**前置条件：**
1. 搭建网络拓扑：AC+AP--STA；
2. AC已运行DHCP服务器，IP pool：192.168.1/10~20；

3. 创建n≥2个GBK编码 SSID
**操作步骤：**
1. STA已保存n≥2个GBK编码 SSID；
2. 重启STA
3、观察STA连接状态和耗时；
**预期结果：**
3. 根据网络选择逻辑选择任一网络自动重连成功，STA IP :192.168.1.1x

---

#### STA远近移动拉断回连
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_User_001；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20；
**操作步骤：**
1. 近距离STA连接AP；
2. 将STA移出AP覆盖范围；
3. STA返回AP覆盖范围，观察STA连接状态和耗时；
4. 重复步骤1-3 10次；
**预期结果：**
2. 无线断开
3. 自动重连成功，耗时<10s，STA IP :192.168.1.1x

---

#### 断开当前网络，自动重连另一个已保存的网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_User_002；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP1/AP2--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，AP开启WiFi；
3. AP和STA放置于强干扰环境，如办公室
4. STA已安装wifi魔盒
**操作步骤：**
1、DUT无线连接AP1
2、DUT无线连接AP2
3、手动断开AP2的连接，观察DUT无线连接情况
4、重复步骤1/2，手动取消AP2的保存，观察DUT无线连接情况
**预期结果：**
3、AP2断开，DUT自动连接到AP1
4、AP2断开，DUT自动连接到AP1

---

#### 取消保存当前网络，自动重连另一个已保存的网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_Reconnect_StaChange_User_003；类型：手工；标签：Common

**前置条件：**
1. 搭建网络拓扑：AP1/AP2--STA；
2. AP已运行DHCP服务器，IP pool：192.168.1/10~20，AP开启WiFi；
3. AP和STA放置于强干扰环境，如办公室
4. STA已安装wifi魔盒
**操作步骤：**
1、DUT无线连接AP1
2、DUT无线连接AP2
3、手动断开AP2的连接，观察DUT无线连接情况
4、重复步骤1/2，手动取消AP2的保存，观察DUT无线连接情况
**预期结果：**
3、AP2断开，DUT自动连接到AP1
4、AP2断开，DUT自动连接到AP1

---

## 双WiFi接入（不涉及切换）
### 接口检查
#### wlan0/wlan1接口与bond0接口mac一致
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Interface_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、adb shell后台ifconfig查看接口mac情况
**预期结果：**
1、wlan0/wlan1接口与bond0接口mac一致

---

#### wlan0/wlan1接口与bond0接口共用ip
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Interface_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、wifi和HyperWiFi网络连接成功后，后台ifconfig查看接口ip情况
**预期结果：**
1、wlan0/wlan1接口与bond0接口共用一个ip

---

### 基础接入
#### 接入共网关下WiFi网络/HyperWiFi网络
**属性：** 优先级：P0；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接同一上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、查看无线列表显示连接情况
**预期结果：**
2、列表显示WIFI网络和HyperWiFi网络为“已连接”

---

#### 接入不共网关下WiFi网络/HyperWiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接不同上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、查看无线列表显示连接情况
**预期结果：**
2、列表显示WIFI网络和HyperWiFi网络为“已连接”

---

#### 依次连接WiFi、HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AP、miniAP的加密方式分别设置为wpa2/wpa3混合、wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### 依次连接HyperWiFi、WiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AP、miniAP的加密方式分别设置为wpa2/wpa3混合、wpa3
2、先连接HyperWiFi，观察连接情况
3、连接WiFi，观察连接情况
**预期结果：**
2、HyperWiFi连接成功
3、WiFi连接成功

---

#### wpa/wpa2 WiFi+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_005；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AP、miniAP的加密方式分别设置为wpa/wpa2混合、wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa2/wpa3 WiFi+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_006；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AP、miniAP的加密方式分别设置为wpa2/wpa3混合、wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa3 WiFi+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_007；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AP、miniAP的加密方式分别设置为wpa3、wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### portal认证网络+HyperWiFi网络
**属性：** 优先级：P3；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_008；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为Portal认证接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa2+802.1x网络+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_009；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa2+802.1x接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa2+802.1x+证书网络+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_010；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa2+802.1x+证书接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa3+802.1x网络+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_011；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa3+802.1x接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa3+802.1x+证书网络+HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_012；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa3+802.1x+证书接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### 双WiFi接入后，手动切换新的WIFI网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_013；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、手动切换连接到新的WIFI网络，观察双WiFi状态
**预期结果：**
2、列表显示WIFI网络和HyperWiFi网络为“已连接”

---

#### 双WiFi接入后，手动切换新的HyperWiFi网络
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Vali_014；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、手动切换连接到新的HyperWiFi网络，观察双WiFi状态
**预期结果：**
2、列表显示WIFI网络和HyperWiFi网络为“已连接”

---

#### 连接双WiFi后启用热点
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Int_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1.dut1依次连接WiFi、HyperWiFi后启用热点
2.使用dut2连接dut1热点，并访问外网
3. dut1依次连接HyperWiFi、WiFi后启用热点，
3. dut2连接dut1热点，并访问外网
**预期结果：**
1、双WiFi连接成功，热点启用成功
2. 连接成功，外网正常
3. 双WiFi连接成功，热点启用成功
4. 连接成功，外网正常

---

#### 启用热点后连接双WiFi
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Connect_Int_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1. dut1启用热点
2. dut1l启用WLAN，连接双WiFi
3. dut2连接dut1热点
**预期结果：**
1. 启用成功
2. 双WiFi连接成功
3. 连接成功，外网正常

---

#### 连接usb外设后启用WiFi并连接
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Connect_Int_003；类型：手工；标签：Common

**前置条件：**
1、dut禁用WLAN
**操作步骤：**
1. dut接入usb 外设（扫码头）
2. 启用WLAN开关，连接双WiFi
**预期结果：**
2. 连接成功

---

#### 已连接WiFi，插拔usb外设
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Connect_Int_004；类型：手工；标签：Common

**前置条件：**
无
**操作步骤：**
1. dut已连接双WiFi后接入usb外设（扫码头）
2. 检查双WiFi连接状态
**预期结果：**
2. 保持连接，无断开重连等现象

---

### 网络配置独立性
#### 新接入HyperWiFi网络，不影响已连的WiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、先手动连接WIFI网络
2、新连接HyperWiFi网络，观察WIFI网络连接情况
**预期结果：**
2、WIFI正常连接，无异常

---

#### 断开HyperWiFi网络，不影响已连的WiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、断开HyperWiFi网络，观察WIFI网络连接情况
**预期结果：**
2、WIFI正常连接，无异常

---

#### 删除HyperWiFi网络，不影响已连的WiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、删除HyperWiFi网络，观察WIFI网络连接情况
**预期结果：**
2、WIFI正常连接，无异常

---

#### 切换HyperWiFi网络，不影响已连的WiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP1、miniAP2分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi1网络
2、切换连接到HyperWiFi2网络，观察WIFI网络连接情况
**预期结果：**
2、WIFI正常连接，无异常

---

#### 修改HyperWiFi配置（ip设置、隐私），不影响已连的WiFi网络
**属性：** 优先级：P3；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_005；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、修改HyperWiFi IP设置选项，观察WiFi网络连接情况
**预期结果：**
2、WiFi正常连接，无异常

---

#### 新接入WiFi网络，不影响已连的HyperWiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_006；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、先手动连接HyperWiFi网络
2、新连接WIFI网络，观察HyperWiFi网络连接情况
**预期结果：**
2、HyperWiFi正常连接，无异常

---

#### 断开WiFi网络，不影响已连的HyperWiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_007；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、断开WIFI网络，观察HyperWiFi网络连接情况
**预期结果：**
2、HyperWiFi正常连接，无异常

---

#### 删除WiFi网络，不影响已连的HyperWiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_008；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、删除WIFI网络，观察HyperWiFi网络连接情况
**预期结果：**
2、HyperWiFi正常连接，无异常

---

#### 切换WiFi网络，不影响已连的HyperWiFi网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_009；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由1和路由器2、miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接HyperWiFi网络和WIFI1网络
2、切换连接到WIFI2网络，观察HyperWiFi网络连接情况
**预期结果：**
2、HyperWiFi正常连接，无异常

---

#### 连接新HyperWiFi（密码错误）失败，不影响已连接的双WiFi
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_010；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP1、miniAP2分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi1网络
2、切换连接到HyperWiFi2网络，输入错误密码连接失败，观察双WIFI网络连接情况
**预期结果：**
2、双WiFi正常连接

---

#### 连接新WiFi（密码错误）失败，不影响已连接的双WiFi
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_011；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由1和路由器2、miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接HyperWiFi网络和WIFI1网络
2、切换连接到WIFI2网络，输入错误密码连接失败，观察双WiFi网络连接情况
**预期结果：**
2、双WiFi正常连接

---

#### 修改WiFi配置（高级设置项），不影响已连的HyperWiFi网络
**属性：** 优先级：P3；摘要：Func_WlanAccess_PriBakLink_CfgIndep_Vali_012；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、修改WIFI高级设置（协议、频段等），观察HyperWiFi网络连接情况
**预期结果：**
2、HyperWiFi正常连接，无异常

---

### 双WiFi网络ip更新
#### （共网关）HyperWiFi网络切换后双WiFi ip不变
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_IpRenew_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP1、nimiAP2分别有线连接同一上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接HyperWiFi1网络和WIFI网络，分别查看网络详情的ip情况
2、切换连接到HyperWiFi2网络，WIFI网络不变，分别查看网络详情的ip情况
**预期结果：**
1、HyperWiFi1网络和IWIFI网络获取同一个ip
2、HyperWiFi2网络和IWIFI网络（ip不变）获取同一个ip

---

#### （共网关）WiFi网络切换后双WiFi ip不变
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_IpRenew_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由1、路由2和miniAP分别有线连接同一上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接HyperWiFi网络和WIFI1网络，分别查看网络详情的ip情况
2、切换连接到WIFI2网络，HyperWiFi网络不变，分别查看网络详情的ip情况
**预期结果：**
1、HyperWiFi网络和IWIFI1网络获取同一个ip
2、HyperWiFi网络和IWIFI2网络（ip不变）获取同一个ip

---

### 双WiFi网络重连
#### STA重启后自动重连
**属性：** 优先级：P1；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_001；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、手动重启DUT，待重启完成后，设置-互联网，查看无线列表中，WIFI网络和HyperWiFi网络重连情况，并使用WiFi魔盒ping网关
**预期结果：**
2、无线列表显示WiFi网络和HyperWiFi网络已连接，ping通网关

---

#### 禁用启用无线开关后自动重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_002；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、手动禁用wlan，查看无线列表中，WIFI网络和HyperWiFi网络连接情况，并使用WiFi魔盒ping网关
3、手动启用wlan，查看无线列表中，WIFI网络和HyperWiFi网络连接情况，并使用WiFi魔盒ping网关
**预期结果：**
2、无线列表显示WiFi网络和HyperWiFi网络已断开，ping不通网关
3、无线列表显示WiFi网络和HyperWiFi网络已连接，ping通网关

---

#### 禁用启用飞行模式后自动重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_003；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、手动开启飞行模式，查看无线列表中，WIFI网络和HyperWiFi网络连接情况，并使用WiFi魔盒ping网关
3、手动关闭飞行模式，查看无线列表中，WIFI网络和HyperWiFi网络连接情况，并使用WiFi魔盒ping网关
**预期结果：**
2、无线列表显示WiFi网络和HyperWiFi网络已断开，ping不通网关
3、无线列表显示WiFi网络和HyperWiFi网络已连接，ping通网关

---

#### 息屏-亮屏后自动重连
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_004；类型：手工；标签：Common

**前置条件：**
1、测试环境：实验室屏蔽箱环境
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、手动连接WIFI网络和HyperWiFi网络
2、通过衰减器增加衰减，使得WiFi和HyperWiFi掉线，然后息屏，并使用WiFi魔盒ping网关
3、调节衰减器减低衰减，后台查看WiFi重连（pno扫描），并使用WiFi魔盒ping网关
4、亮屏，查看HyperWiFi的重连情况
**预期结果：**
3、WiFi网络重连成功，ping通网关
4、HyperWiFi网络重连成功

---

#### portal认证网络+HyperWiFi网络-断开重连测试
**属性：** 优先级：P3；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_005；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为Portal认证接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
4、禁用启用wlan开关，观察双WiFi重连情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功
4、双WiFi重连成功

---

#### wpa2+802.1x网络+HyperWiFi网络-断开重连测试
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_006；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa2+802.1x接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
4、禁用启用wlan开关，观察双WiFi重连情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功

---

#### wpa2+802.1x+证书网络+HyperWiFi网络-断开重连测试
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_007；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa2+802.1x+证书接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
4、禁用启用wlan开关，观察双WiFi重连情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功
4、双WiFi重连成功

---

#### wpa3+802.1x网络+HyperWiFi网络-断开重连测试
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_008；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa3+802.1x接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
4、禁用启用wlan开关，观察双WiFi重连情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功
4、双WiFi重连成功

---

#### wpa3+802.1x+证书网络+HyperWiFi网络-断开重连测试
**属性：** 优先级：P2；摘要：Func_WlanAccess_PriBakLink_Reconnect_Vali_009；类型：手工；标签：Common

**前置条件：**
1、测试环境：办公室
2、拓扑：陪测路由和miniAP分别有线连接上级路由器
3、miniAP加密方式为WPA3
**操作步骤：**
1、AC配置WiFi为wpa3+802.1x+证书接入，miniAP加密为wpa3
2、先连接WiFi，观察连接情况
3、连接HyperWiFi，观察连接情况
4、禁用启用wlan开关，观察双WiFi重连情况
**预期结果：**
2、WiFi连接成功
3、HyperWiFi连接成功
4、双WiFi重连成功

---
