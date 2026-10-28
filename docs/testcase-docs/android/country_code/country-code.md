# 国家码
## 出厂状态国家码
### 功能有效性
#### 初始未联网，WiFi默认国家码检查
**属性：** 优先级：P1；摘要：Ccode_Default_Func_001；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、adb后台输入cmd wifi get-country-code，查询WiFi国家码
**预期结果：**
1、显示为null
ps：默认为空，跟随产品型号自定义，没有统一

---

#### 初始未联网，欧盟区Halow国家码为EU，占空比默认打开
**属性：** 优先级：P1；摘要：Ccode_Default_Func_002；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、shell命令修改国家码 cmd wifi force-country-code enabled DE （德国）
2、shell命令查看 Halow国家码：cli_app show config | grep -i country
3、查看占空比是否打开： cli_app show duty
**预期结果：**
2、欧盟区Halow国家码：EU，
3、占空比打开：Duty cycle : on

---

#### 初始未联网，非欧盟区Halow国家码为US，占空比默认关闭
**属性：** 优先级：P1；摘要：Ccode_Default_Func_003；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、shell命令修改国家码 cmd wifi force-country-code enabled US （美国）
2、shell命令查看 Halow国家码：cli_app show config | grep -i country
3、查看占空比是否打开： cli_app show duty
**预期结果：**
2、非欧盟区HyperWIFI国家默认US，
3、占空比关闭：Duty cycle : off

---

#### 初始已联网，欧盟区Halow国家码为EUS，占空比默认关闭
**属性：** 优先级：P1；摘要：Ccode_Default_Func_004；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、shell命令修改国家码 cmd wifi force-country-code enabled DE （德国）
2、shell命令查看 Halow国家码：cli_app show config | grep -i country
3、查看占空比是否打开： cli_app show duty
**预期结果：**
2、Halow国家码为 Country : EU

3、占空比关闭：Duty cycle : off

---

#### 初始已联网，非欧盟区Halow国家码为US，占空比默认关闭
**属性：** 优先级：P0；摘要：Ccode_Default_Func_005；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、shell命令修改国家码 cmd wifi force-country-code enabled US （美国）
2、shell命令查看 Halow国家码：cli_app show config | grep -i country
3、查看占空比是否打开： cli_app show duty
**预期结果：**
2、Halow国家码为 Country : US
3、占空比关闭：Duty cycle : off

---

### 功能容错性
#### 设备再次恢复出厂设置
**属性：** 优先级：P1；摘要：Ccode_Default_Excpt_001；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、将设备恢复恢复出厂设置后，进入welcome WLAN列表页面
2、shell命令查看 Halow国家码：cli_app show config | grep -i country
**预期结果：**
2、Halow国家码和出厂的WiFi国家码映射关系一致

---

#### 设备重置WLAN，不影响当前配置
**属性：** 优先级：P1；摘要：Ccode_Default_Excpt_002；类型：手工；标签：HyperWiFi

**前置条件：**
无
**操作步骤：**
1、进入设置-> 系统-> 重置选项-> 重置WLAN
**预期结果：**
2、WLAN相关配置被清空，国家码不会变更

---

## 蜂窝联网自动映射国家码
### 功能有效性
#### ad:Europe/Andorra
**属性：** 优先级：P1；摘要：Ccode_Adapt_Func_001；类型：自动化；标签：Common

**前置条件：**
无
**操作步骤：**
1、shell命令配置设备使用欧盟国家码cmd wifi force-country-code enabled {country_code} ，重新打开WiFi开关
2、shell命令查看传统国家码：cmd wifi get-country-code
3、shell命令查看HyperWIFI国家码：cli_app show config | grep -i country ， cli_app show duty 
4、检测WiFi和HyperWiFi是否连接成功
**预期结果：**
1、WLAN列表扫描到HyperWiFi、WiFi 2.4G、5G SSID
2、WiFi国家码为 {country_code} 
3、Halow国家码为EU，默认Duty cycle : off
4、WiFi和HyperWiFi均可连接成功

---
