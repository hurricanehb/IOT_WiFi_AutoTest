# 功能
## HyperWiFi低功耗
### HyperWiFi低功耗基础状态有效性测试
#### 亮屏，出厂启用WLAN但不连接，不进入低功耗模式（IDLE）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
1、设备为恢复出厂状态
**操作步骤：**
1、设备恢复出厂后未连接HyperWiFi
2、后台cli_app show ps_status，查看低功耗状态
3、dmesg -Tw | grep -iE 'ps mode|ps state'
**预期结果：**
2、显示低功耗模式为wake
3、显示为active

---

#### 亮屏，WLAN已连接但无业务，不进入低功耗模式（PowerSave）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、连接HyperWiFi，不做任何操作放置
2、后台cli_app show ps_status，查看低功耗状态
3、dmesg -Tw | grep -iE 'ps mode|ps state'
**预期结果：**
2、显示低功耗模式为wake
3、显示为active

---

#### 亮屏，WLAN断开且不扫描，不进入低功耗模式（IDLE）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、连接HyperWiFi，不做任何操作放置
2、断开HyperWiFi，dmesg -Tw | grep -iE 'ps mode|ps state'查看状态变化
**预期结果：**
2、一直为active和wake

---

#### 亮屏，出厂关闭WLAN，为低功耗模式（IDLE）
**属性：** 优先级：P0；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
1、设备为恢复出厂状态
备注：
出厂状态下：
1、MTK系列（SP01、SP10等）Wlan默认关闭
2、高通系列（V3MIX等）Wlan默认开启
**操作步骤：**
1、设备未进入welcome-语言选择页面
2、后台cli_app show ps_status，查看低功耗状态
3、cli_app show idle_mode，查看是否为idle模式
**预期结果：**
2、显示低功耗模式为sleep
3、显示为dile模式

---

#### 亮屏，无连接状态下关闭WLAN，进入低功耗模式（IDLE）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_005；类型：；标签：HyperWiFi

**前置条件：**
1、未连接HyperWiFi网络
**操作步骤：**
1、亮屏-开启wlan下，查看ps_status
2、关闭wlan，同步查看ps_status、idle_mode
3、dmesg -Tw | grep -iE 'ps mode|ps state'查看状态变化
**预期结果：**
1、显示低功耗模式为wake
2、显示为sleep和idle
3、显示wake>>sleep、DEEP_NONTIM

---

#### 亮屏，已连接状态下关闭WLAN，进入低功耗模式（IDLE）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_006；类型：；标签：HyperWiFi

**前置条件：**
1、已连接HyperWiFi网络
**操作步骤：**
1、亮屏-开启wlan下，查看ps_status
2、关闭wlan，同步查看ps_status、idle_mode
3、dmesg -Tw | grep -iE 'ps mode|ps state'查看状态变化
**预期结果：**
1、显示低功耗模式为wake
2、显示为sleep和idle
3、显示wake>>sleep、DEEP_NONTIM

---

#### 亮屏，开启飞行模式，进入低功耗模式（IDLE）
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOn_Vali_007；类型：；标签：HyperWiFi

**前置条件：**
1、已连接HyperWiFi网络
**操作步骤：**
1、亮屏查看ps_status
2、开启飞行模式，同步查看ps_status、idle_mode
3、dmesg -Tw | grep -iE 'ps mode|ps state'查看状态变化
4、关闭飞行模式，重复步骤3
**预期结果：**
1、显示低功耗模式为wake
2、显示为sleep和idle
3、显示wake>>sleep、DEEP_NONTIM
4、显示sleep>>wake、active

---

#### 亮屏状态下低功耗模式切换--禁用启用Wlan开关
**属性：** 优先级：P3；摘要：Func_HalowLP_BasicState_ScreenOn_Stb_001；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、使用脚本反复禁用启用wlan开关，查看每次切换后低功耗状态
**预期结果：**
1、每次正常切换低功耗模式

---

#### 亮屏状态下低功耗模式切换--禁用启用飞行模式
**属性：** 优先级：P3；摘要：Func_HalowLP_BasicState_ScreenOn_Stb_002；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、使用脚本反复禁用启用飞行模式，查看每次切换后低功耗状态
**预期结果：**
1、每次正常切换低功耗模式

---

#### 息屏，出厂未连接状态下，进入IDLE模式验证
**属性：** 优先级：P0；摘要：Func_HalowLP_BasicState_ScreenOff_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
1、恢复出厂且未连接过HyperWiFi
**操作步骤：**
1、设备恢复出厂后未连接HyperWiFi
2、息屏后观察：dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态变换过程
3、同步查看ps_status、idle_mode
**预期结果：**
2、state为sleep、mode为DEEP_NONTIM
3、state为sleep、mode为IDLE
注意该操作无pno扫描

---

#### 息屏，PNO扫描不到目标网络，进入IDLE模式
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOff_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
1、恢复出厂且连接HyperWiFi
**操作步骤：**
1、息屏后，下电miniAP
2、观察pno不到结果后：dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态变换过程
3、同步查看ps_status、idle_mode
**预期结果：**
2、state为wake>>sleep、mode为DEEP_NONTIM
3、state为sleep、mode为IDLE

---

#### 息屏，已连接状态但无流量，进入PowerSave模式验证
**属性：** 优先级：P0；摘要：Func_HalowLP_BasicState_ScreenOff_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、设备连接HyperWiFi，不做任何业务操作放置
2、息屏观察：dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态变换过程
**预期结果：**
2、state为wake>>sleep、mode为DEEP_TIM（PowerSave模式）
注意设备会不间断在进行数据交互，状态也会反复变化，所以只需要判断期间是否wake>>sleep

---

#### 息屏，PNO扫描成功后无流量或业务，进入powersave模式
**属性：** 优先级：P1；摘要：Func_HalowLP_BasicState_ScreenOff_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、息屏后，重启miniAP
2、观察pno扫描结果后：dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态变换过程
3、不做任何操作，观察低功耗状态
**预期结果：**
2、state为sleep>>wake、
3、state为wake>>sleep，mode为DEEP_TIM（PowerSave模式）

---

### HyperWiFi低功耗状态转换与触发测试
#### 已连接状态亮屏->息屏（无业务或流量等），进入低功耗PowerSave模式
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScrChange_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、亮屏下连接HyperWiFi，查看ps status
2、息屏后无业务操作后台dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、状态为wake
2、状态变化wake>>sleep，mode为DEEP_TIM（PS模式）

---

#### 亮屏状态断开连接->息屏（无扫描等），进入低功耗IDLE模式
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScrChange_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、亮屏下手动断开HyperWiFi，查看ps status
2、息屏后待无pno扫描，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、状态为wake
2、状态变化wake>>sleep，mode为DEEP_NONTIM（IDLE模式）

---

#### 亮屏状态取消保存网络（无保存网络）->息屏（无扫描等），进入低功耗IDLE模式
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScrChange_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、亮屏下取消HyperWiFi，查看ps status
2、息屏后，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、状态为wake
2、状态变化wake>>sleep，mode为DEEP_NONTIM（IDLE模式）

---

#### 未连接息屏，再亮屏，立即退出IDLE模式
**属性：** 优先级：P0；摘要：Func_HalowLP_StateChange_ScrChange_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
1、未连接HyperWiFi
**操作步骤：**
1、息屏查看低功耗状态
2、亮屏后查看低功耗状态转换情况
**预期结果：**
1、低功耗为sleep状态
2、状态有sleep >> wake

---

#### 已连接息屏，再亮屏，立即退出PowerSave模式
**属性：** 优先级：P0；摘要：Func_HalowLP_StateChange_ScrChange_Vali_005；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、连接HyperWiFi，不做业务等操作
2、亮屏，dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
3、后台cli_app show ps state、idle_mode，查看低功耗状态
**预期结果：**
2、状态由sleep转为wake
3、显示wake状态，模式为no idle

---

#### 未连接状态，亮屏息屏互切低功耗状态检查
**属性：** 优先级：P3；摘要：Func_HalowLP_StateChange_ScrChange_Stb_001；类型：；标签：HyperWiFi

**前置条件：**
1、未连接HyperWiFi
**操作步骤：**
1、使用脚本反复禁亮息屏，查看每次切换后低功耗状态
**预期结果：**
1、低功耗状态正常切换

---

#### 已连接状态，亮屏息屏互切低功耗状态检查
**属性：** 优先级：P3；摘要：Func_HalowLP_StateChange_ScrChange_Stb_002；类型：；标签：HyperWiFi

**前置条件：**
1、已连接HyperWiFi
**操作步骤：**
1、使用脚本反复禁亮息屏，查看每次切换后低功耗状态
**预期结果：**
1、低功耗状态正常切换

---

#### 未连接息屏，PNO扫描获取结果后，退出IDLE模式验证
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScreenOff_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、息屏后，下电miniAP
2、观察pno不到结果后：dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态变换过程
3、上电miniAP，观察pno扫描到后获取到结果，低功耗状态变化
**预期结果：**
2、状态有wake转为sleep
3、状态有sleep转为wake

---

#### 已连接息屏，有流量或业务时，退出PowerSave模式验证
**属性：** 优先级：P0；摘要：Func_HalowLP_StateChange_ScreenOff_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、连接HyperWiFi，进行后台iperf跑流
2、dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
**预期结果：**
2、状态有sleep转为wake
注意设备会不间断在进行数据交互（icmp、arp等），状态也会反复变化，所以只需要判断期间是否sleep>>wake

---

#### 已连接息屏，弱信号下发起扫描时，退出PowerSave模式验证
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScreenOff_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、连接HyperWiFi，不做业务等操作
2、dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
3、后台cli_app show config，查看低功耗状态
4、调价衰减使得rssi为-88dBm，观察扫描时的状态变化
**预期结果：**
2、状态有wake转为sleep
3、显示在PowerSave模式（DEEP_TIM）
4、状态有sleep转为wake（唤醒）

---

#### 已连接息屏，断开连接时，退出PowerSave模式验证
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScreenOff_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、连接HyperWiFi，不做业务等操作
2、dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
3、后台cli_app show config，查看低功耗状态
4、关闭miniAP无线使得HyperWiFi断开，观察状态变化
**预期结果：**
2、状态有wake转为sleep
3、显示在PowerSave模式（DEEP_TIM）
4、状态有sleep转为wake（唤醒）

---

#### 已连接息屏，DHCP续租时，退出PowerSave模式
**属性：** 优先级：P1；摘要：Func_HalowLP_StateChange_ScreenOff_Vali_005；类型：；标签：HyperWiFi

**前置条件：**
1、设置DHCP租约时间为2分钟
**操作步骤：**
1、连接HyperWiFi，不做业务等操作
2、ip续约时，dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
3、后台cli_app show ps state、idle_mode，查看低功耗状态
**预期结果：**
2、状态由sleep转为wake
3、显示wake状态，模式为no idle

---

### 双WiFi下HyperWiFi低功耗
#### 亮屏，先后连接WiFi、HyperWiFi的过程中，HyperWiFi仍为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOn_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
**操作步骤：**
1、setting页面，连接WiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
2、setting页面，连接HyperWiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
**预期结果：**
1、HyperWiFi处于active状态
2、状态不变，仍处于active状态

---

#### 亮屏，先后连接HyperiWiFi、WiFi的过程中，HyperWiFi仍为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOn_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
**操作步骤：**
1、setting页面，连接HyperWiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
2、setting页面，连接WiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
**预期结果：**
1、HyperWiFi处于active状态
2、状态不变，仍处于active状态

---

#### 亮屏，已连接双WiFi，断开WiFi的过程中，HyperWiFi仍为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOn_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接HyperWiFi
**操作步骤：**
1、setting页面，连接双WiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
2、setting页面，断开WiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
**预期结果：**
1、HyperWiFi处于active状态
2、状态不变，仍处于active状态

---

#### 亮屏，已连接双WiFi，断开HyperWiFi的过程中，HyperWiFi仍为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOn_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接HyperWiFi
**操作步骤：**
1、setting页面，连接双WiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
2、setting页面，断开HyperWiFi，后台dmesg -Tw | grep -iE "setting ps state"查看状态
**预期结果：**
1、HyperWiFi处于active状态
2、状态不变，仍处于active状态

---

#### 亮屏，连接双WiFi后-无业务或流量（无扫描）时，HyperWiFi仍为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOn_Vali_005；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接HyperWiFi
**操作步骤：**
1、setting页面，连接双WiFi，不做任何业务放置，后台dmesg -Tw | grep -iE "setting ps state"查看状态
**预期结果：**
1、HyperWiFi一直处于active状态

---

#### 息屏，未连接HyperWiFi（无保存网络），WiFi进行PNO扫描，HyperWiFi低功耗模式不变
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、息屏，不连接HyperWiFi（无保存网络），后台dmesg -Tw | grep -iE "setting ps state"查看状态
2、重启AP无线，使得WiFi断开，logcat | grep -iE "pno"查看扫描情况
3、同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi处于sleep状态
2、WiFi发起pno扫描
3、状态不变，仍处于sleep状态（DEEPSLEEP_NONTIM）

---

#### 息屏，未连接HyperWiFi（已保存网络）且未进行PNO扫描，WiFi进行PNO扫描，HyperWiFi退出低功耗模式
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、息屏，不连接HyperWiFi（已保存网络，但目标miniAP已下线），后台logcat | grep -iE "pno"查看扫描情况和dmesg -Tw | grep -iE "setting ps state"查看状态
2、重启AP无线，使得WiFi断开，logcat | grep -iE "pno"查看扫描情况
3、同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi发起PNO，但扫不到目标网络，状态sleep>>wake>>sleep
2、WiFi发起PNO，同时HyperWiFi也发起PNO（虽未到扫描周期）
3、状态sleep>>wake

---

#### 息屏，已连接HyperWiFi（PowerSave模式），断开WiFi网络，HyperWiFi低功耗模式不变
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接双WiFi
**操作步骤：**
1、息屏，后台dmesg -Tw | grep -iE "setting ps state"查看HyperWiFi状态
2、重启AP无线，使得WiFi断开，同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi处于sleep状态
2、状态不变，仍处于sleep状态

---

#### 息屏，已连接HyperWiFi（PowerSave模式），WiFi发起PNO扫描连接，HyperWiFi低功耗模式不变
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接双WiFi
**操作步骤：**
1、息屏，后台dmesg -Tw | grep -iE "setting ps state"查看HyperWiFi状态
2、重启AP无线，使得WiFi断开，logcat | grep -iE "pno"查看扫描情况
3、同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi处于sleep状态
2、WiFi发起pno扫描
3、状态不变，仍处于sleep状态

---

#### 息屏，WiFi保持连接，接入HyperWiFi且有流量（业务时），HyperWiFi退出功耗模式
**属性：** 优先级：P1；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_005；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接双WiFi
**操作步骤：**
1、息屏，后台dmesg -Tw | grep -iE "setting ps state"查看HyperWiFi状态
2、同步tcpdump -n -vvv -xxx -iwlan1查看数据包交互情况
3、后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi处于sleep状态
2、HyperWiFi不间断发送arp、icmpv6等
3、状态由sleep转为wake

---

#### 息屏，WiFi保持连接，断开HyperWiFi后发起pno扫描，退出低功耗（唤醒状态）
**属性：** 优先级：P1；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_006；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接双WiFi
**操作步骤：**
1、息屏，后台dmesg -Tw | grep -iE "setting ps state"查看HyperWiFi状态
2、重启miniAP无线，使得HyperWiFi断开，logcat | grep -iE "pno"查看扫描情况
3、同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi处于sleep状态
2、HyperWiFi发起pno扫描
3、状态由sleep转为wake

---

#### 息屏，WiFi保持连接，断开HyperWiFi后pno扫描不到目标网络，进入低功耗（idle状态）
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_007；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、息屏，下电miniAP，使得HyperWiFi断开，后台logcat | grep -iE "pno"查看扫描情况和dmesg -Tw | grep -iE "setting ps state"查看状态
2、HyperWiFi没有重连成功，同步后台dmesg -Tw | grep -iE "setting ps state|hw scan"查看状态是否变化
**预期结果：**
1、HyperWiFi发起PNO，，状态sleep>>wake
2、状态wake>>sleep

---

#### 息屏，已连接双WiFi，HyperWiFi（PowerSave模式），WiFi进行DHCP续约，HyperWiFi低功耗模式不变
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScreenOff_Vali_008；类型：；标签：HyperWiFi

**前置条件：**
1、环境拓扑：上级网关--AP/miniAP
2、测试环境：办公位或者实验室
3、已连接WiFi
**操作步骤：**
1、连接双WiFi，不做业务等操作
2、WiFi ip续约时，dmesg -Tw | grep -iE "setting ps state"查看状态变换过程
3、后台cli_app show ps state、idle_mode，查看低功耗状态
**预期结果：**
1、HyperWiFi一直处于active状态

---

#### 亮屏连接双WiFi-断开WiFi后息屏，HyperWiFi（无流量等）进入低功耗PowerSave模式
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScrChange_Vali_001；类型：；标签：HyperWiFi

**前置条件：**
1、已连接双WiFi
**操作步骤：**
1、亮屏断开WiFi，查看ps status
2、息屏后，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、wake状态
2、wake 》》sleep，mode为PS模式

---

#### 亮屏连接双WiFi-断开HyperWiFi后息屏，HyperWiFi（无扫描等）进入低功耗IDLE模式
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScrChange_Vali_002；类型：；标签：HyperWiFi

**前置条件：**
1、已连接双WiFi
**操作步骤：**
1、亮屏取消保存HyperWiFi，查看ps status
2、息屏后，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、wake状态
2、wake 》》sleep，mode为IDLE模式

---

#### 息屏连接双WiFi（HyperWiFi为PS）-亮屏后HyperWiFi切换为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScrChange_Vali_003；类型：；标签：HyperWiFi

**前置条件：**
1、已连接双WiFi
**操作步骤：**
1、息屏下无业务操作，查看ps status
2、亮屏后，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、sleep状态，powersave模式
2、sleep 》》wake

---

#### 息屏只连接WiFi（HyperWiFi为IDLE）-亮屏后HyperWiFi切换为唤醒状态
**属性：** 优先级：P2；摘要：Func_HalowLP_DoubleWifi_ScrChange_Vali_004；类型：；标签：HyperWiFi

**前置条件：**
1、已连接WiFi
**操作步骤：**
1、息屏下无业务操作，查看ps status
2、亮屏后，dmesg -Tw | grep -iE "setting ps state|ps mode"查看状态是否变化
**预期结果：**
1、sleep状态，idle模式
2、sleep 》》wake

---

#### 整机低功耗休眠唤醒HyperWiFi
**属性：** 优先级：P3；摘要：Func_HalowLP_DoubleWifi_ScrChange_Int_001；类型：；标签：HyperWiFi

**前置条件：**
1、已连接WiFi
**操作步骤：**
1、设备亮屏无业务状态放置12H
2、检查logcat日志，设备进入dozing模式唤醒后HyperWiFi是都自动重连
**预期结果：**
2、自动重连成功

---