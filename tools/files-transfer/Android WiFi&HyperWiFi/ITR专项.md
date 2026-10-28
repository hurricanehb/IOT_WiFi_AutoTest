# ITR专项
## WiFi
### WiFi7 AP连接失败：11be识别失败（ITR-11155/11452/11665/11928/13529/13597）
#### 连接WiFi7 AP（按兼容性矩阵扩充：）
**属性：** 优先级：P1；摘要：Func_ITR_WiFi7_Conn_Vali_001；类型：手工；标签：WiFi

**前置条件：**
AP外网可达
**操作步骤：**
1、DUT无线连接陪测AP的2.4G，并ping百度
2、DUT无线连接陪测AP的5G，并ping百度
**预期结果：**
1. 连接成功，并且ping通

---

### AP配置WPA3加密连接失败：SAE/OCV不兼容（ITR-11155/11452/11665/11928/13529/13597）
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

### 企业级WiFi CA证书“不验证”选项缺失（ITR-11407/11954/12085）
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

### Welcome连接WiFi失败：谷歌激活流程204检验异常（ITR-12561/12873）
#### 离线激活-连接双WiFi激活
**属性：** 优先级：P0；摘要：Func_Components_Welcome_Activation_Int_004；类型：；标签：Common

**前置条件：**
DUT恢复出厂设置，选择离线激活
**操作步骤：**
1、dut连接双WiFi过激活流程后
2、检查settings-网络和互联网-WLAN状态
3、检查无线连接状态
4、检查systemUI-互联网/WLAN状态
**预期结果：**
2. wlan开关保持打开
3. 双WiFi保持连接
4、wlan开关保持打开，连接状态一致

---

#### 离线激活-连接单WiFi激活
**属性：** 优先级：P0；摘要：Func_Components_Welcome_Activation_Int_005；类型：；标签：Common

**前置条件：**
DUT恢复出厂设置，选择离线激活
**操作步骤：**
1、dut连接WiFi或HyperWiFi过激活流程后
2、检查settings-网络和互联网-WLAN状态
3、检查无线连接状态
4、检查systemUI-互联网/WLAN状态
**预期结果：**
2. wlan开关保持打开
3. 无线保持连接
4、wlan开关保持打开，连接状态一致

---

### 重启后机器不进系统：对GBK支持不足（ITR-13012）
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
2. 自动重连成功，STA  IP :192.168.1.1x

---

### 无法连接wifi：竞争能力不足（ITR-11201/13344/13289）
#### AP/miniAP重启-双WiFi重连测试（多STA竞争接入）-300次
**属性：** 优先级：P1；摘要：Stability_SinRssi_CellInt_002；类型：自动化；标签：Common

**前置条件：**
1、拓扑：AC--AP/miniAP--STA

2、压测脚本（正弦调整rssi）
3、测试环境：实验室屏蔽箱
4、测试软件：Ixchariot或iperf3
5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）
**操作步骤：**
1、启动脚本，观察STA 双WiFi重连情况
2、测试500次，观察STA 双WiFi重连情况
**预期结果：**
1、双WiFi重连成功
2、双WiFi重连成功，成功率100%

---

#### 禁用启用WLAN开关-双WiFi重连测试--500次
**属性：** 优先级：P1；摘要：Stability_SinRssi_CellInt_001；类型：；标签：Common

**前置条件：**
1、拓扑：AC--AP/miniAP--STA

2、压测脚本（正弦调整rssi）
3、测试环境：实验室屏蔽箱
4、测试软件：Ixchariot或iperf3
5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）
**操作步骤：**
1、启动脚本，观察STA 双WiFi重连情况
2、测试500次，观察STA 双WiFi重连情况
**预期结果：**
1、双WiFi重连成功
2、双WiFi重连成功，成功率100%

---

### 搜索不到5G WiFi：设备国家码与当地不匹配（ITR-11456）
#### 初始未联网，WiFi默认国家码检查
**属性：** 优先级：P1；摘要：Func_Ccode_Default_Vali_001；类型：手工；标签：HyperWiFi

**前置条件：**
1、设备恢复出厂设置
**操作步骤：**
1、adb后台输入cmd wifi get-country-code，查询WiFi国家码
**预期结果：**
1、显示为null
ps：默认为空，跟随产品型号自定义，没有统一
（无蜂窝的设备，与出货地需要保持一致）

---

### 开机扫不到WiFi无法自动连接：WIFi驱动加载失败（ITR-10889）
#### STA 重启-双WiFi重连测试--300次
**属性：** 优先级：P0；摘要：Stability_HRssi_Reconnect_003；类型：；标签：Common

**前置条件：**
1、拓扑：AC--AP/miniAP--STA

2、miniAPrssi控制在-45dBm左右
3、测试环境：实验室屏蔽箱
4、测试软件：Ixchariot或iperf3
5、配置好压测脚本
**操作步骤：**
1、启动脚本，观察双WiFi重连情况
2、测试1000次，观察双WiFi重连情况
**预期结果：**
1、双WiFi重连成功
2、双WiFi重连成功，成功率100%

---

### 自动断开后搜不到WiFi：反复重连失败后WIFI固件异常（ITR-11312）
#### STA 反复移动断开-双WiFi重连测试--500次
**属性：** 优先级：P0；摘要：Stability_HRssi_Reconnect_008；类型：；标签：Common

**前置条件：**
1、拓扑：AC--AP/miniAP--STA

2、miniAPrssi控制在-45dBm左右
3、测试环境：实验室屏蔽箱
4、测试软件：Ixchariot或iperf3
5、配置好压测脚本
**操作步骤：**
1、DUT放置于屏蔽箱，无线连接AP、miniAP；台式PC有线连接AP，并开启ping包工具ping通DUT
2、通过可调衰减器（RvR）1dB步进加大衰减，直到wifi掉线（rssi约-90dBm），Hyperwifi掉线（rssi约102dBm）
3、待5分钟后，5bB步进减小衰减，rssi约-50dBm，后台logcat | grep -i “siganl_poll”，查询回连的状态和rssi
4、重复步骤2、3，操作100次，观察DUT无线连接状态、ping包情况
**预期结果：**
3、wifi回连-75dBm，HyperWiFi回连-98dBm
4、正常回连，无异常

---

#### STA移动断开后-停留一段时间再往回走-双WiFi重连测试
**属性：** 优先级：P1；摘要：Stability_PulRssi_Reconnectt_001；类型：；标签：Common

**前置条件：**
1、拓扑：AC--多AP/多miniAP--STA

2、压测脚本（脉冲调整rssi）
3、测试环境：实验室屏蔽箱
4、测试软件：Ixchariot或iperf3
5、陪测干扰源*3，持续进行吞吐（2Mbps，按照50%）
**操作步骤：**
1、启动脚本，观察STA 随着rssi的变化后的断连与重连情况
**预期结果：**
1.1、wifi回连-75dBm，HyperWiFi回连-98dBm（回连rssi与扫描时间点有相关）
1.2、成功率100%

---

### 搜不到WiFi信号：扫码头VID/PID与WiFi冲突（ITR-12044）
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

### AP配置WPA2/WPA3混合加密连接失败：芯片方案不支持WPA3（ITR-10914）
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

### WiFi连接失败：WPA2/WPA3混合、WPA3启用PMF（ITR-11440）
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

#### AP设置无线加密方式为WPA3个人级，AES256GCM加密，强制开启pmf
**属性：** 优先级：P1；摘要：Func_WlanAccess_Conn_Encrypt_Vali_030；类型：手工；标签：WiFi

**前置条件：**
1. DUT为出厂状态
2. 已配置好WiFI网络，可通外网
**操作步骤：**
1、AP（HW  AirEngineer9700S-S）配置：WPA3个人级，AES256GCM加密，强制开启pmf
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

### 中文SSID显示乱码且无法连接：对GBK支持不足（ITR-13488）
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

#### 扫码添加AP SSID GBK编码16个中文字符网络
**属性：** 优先级：P2；摘要：Func_WlanAccess_Conn_Scanner_Vali_007；类型：手工；标签：WiFi

**前置条件：**
1、AP配置为GBK编码格式的中文字符，密码为"123 'test'  //\\"
**操作步骤：**
1、被测设备扫码添加网络
2、dut重启系统
**预期结果：**
1、无线信息被保存，且主动连接成功
2、自动重连成功

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

#### GBK编码SSID切换连接
**属性：** 优先级：P1；摘要：Func_Components_SystemUI_ScanList_Excp_002；类型：；标签：WiFi

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

#### 网络详情-GBK编码SSID“分享二维码”选项检查
**属性：** 优先级：P1；摘要：Func_Components_Settings_NetDetails_UI_006；类型：UI自动化；标签：Common

**前置条件：**
1、设备恢复出厂
2、陪测试设备为AP
**操作步骤：**
1、AP互联网正常
2、DUT连接无线，点击查看网络详情-点击“分享二维码”
3、使用其他终端扫描二维码，检查无线连接情况
**预期结果：**
3、连接无线成功

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
3. 根据网络选择逻辑选择任一网络自动重连成功，STA  IP :192.168.1.1x

---

### 无法连接5g网络：A11下BZ国家码无5G（ITR-13454）
#### bz:America/Belize
**属性：** 优先级：P2；摘要：Func_Ccode_Adapt_Vali_077；类型：自动化；标签：Common

**前置条件：**
1、设备联网在线
**操作步骤：**
1、shell命令配置设备使用欧盟国家码cmd wifi force-country-code enabled  {country_code} ，重新打开WiFi开关
2、shell命令查看传统国家码：cmd wifi get-country-code
3、shell命令查看HyperWIFI国家码：cli_app show config | grep -i country  ， cli_app  show duty
4、检测WiFi和HyperWiFi是否连接成功
**预期结果：**
1、WLAN列表扫描到HyperWiFi、WiFi 2.4G、5G SSID
2、WiFi国家码为 {country_code}
3、Halow国家码为US，默认Duty cycle : off
4、WiFi和HyperWiFi均可连接成功

---

### 无法自动连接wifi：204检测关闭（ITR-13185）
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

#### 204开关开启，外网正常-LAN/WLAN/蜂窝检测周期验证
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_005；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均可访问外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min

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

#### 204开关开启，外网异常-LAN/WLAN/蜂窝检测周期验证
**属性：** 优先级：P0；摘要：Func_WlanAccess_Network_204_Vali_009；类型：手工；标签：Common

**前置条件：**
LAN、WiFi、HyperWiFi蜂窝均无外网
**操作步骤：**
1、DUT依次接入LAN、WiFi、HyperWiFi、蜂窝，后台logcat | grep -i "networkmonitor"，查看网络连通性检测周期
**预期结果：**
2、按照1/2/4/8s...倍数递增，最大周期为10min

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

### WiFi经常断网：ip可达性检测（ITR-13364，客户场景与需求不匹配）
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
03-02 10:54:05.432  2915 22666 W IpClient.bond0: [IpReachabilityMonitor] WARN ALERT neighbor went from: NeighborEvent{@235098910,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]} to: NeighborEvent{@235101212,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]}

03-02 10:54:05.433  2915 22666 W IpReachabilityMonitor: FAILURE: LOST_PROVISIONING, NeighborEvent{@235101212,RTM_NEWNEIGH,if=27,192.0.0.1,NUD_FAILED,[null]}

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