# 功能
## MIX机型-USB模式切换
### P3MIX基线版本
#### 工厂恢厂：基线版本，USB Device模式
**属性：** 优先级：P1；摘要：Func_UsbMode_P3Mix_Vali_001；类型：手工；标签：WiFi

**前置条件：**
1. 设备烧录P3MIX基线版本
2. 设备当前模式为「USB Device」
3. HyperWiFi网络已配置
**操作步骤：**
1. 工厂执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
**预期结果：**
1. 恢厂后设备模式为「USB Device」
2. 激活后设备模式更新为「USB Host」
3. WLAN扫描功能正常

---

#### 用户恢厂：基线版本，USB Device模式
**属性：** 优先级：P1；摘要：Func_UsbMode_P3Mix_Vali_002；类型：手工；标签：WiFi

**前置条件：**
1. 设备烧录P3MIX基线版本
2. 设备当前模式为「USB Device」
3. 设备已激活或未激活
4. HyperWiFi网络已配置
**操作步骤：**
1. 用户通过设置执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
**预期结果：**
1. 恢厂后设备模式为「USB Device」
2. 激活后设备模式更新为「USB Host」
3. WLAN扫描功能正常

---

### P3MIX HyperWiFi版本
#### 工厂恢厂：HyperWiFi配置，恢厂前USB Device
**属性：** 优先级：P1；摘要：Func_UsbMode_P3MixH_Vali_001；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置版本
2. 设备当前模式为「USB Device」
3. HyperWiFi网络已配置
**操作步骤：**
1. 工厂执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
7. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Device」（与恢厂前一致）
2. 激活后设备模式更新为「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 工厂恢厂：HyperWiFi配置，恢厂前USB Host
**属性：** 优先级：P1；摘要：Func_UsbMode_P3MixH_Vali_002；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置版本
2. 设备当前模式为「USB Host」（工厂已调整）
3. HyperWiFi网络已配置
**操作步骤：**
1. 工厂执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
7. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Host」（与恢厂前一致）
2. 激活后设备模式继续保持「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 用户恢厂：HyperWiFi配置，恢厂前USB Device
**属性：** 优先级：P1；摘要：Func_UsbMode_P3MixH_Vali_003；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置版本
2. 设备当前模式为「USB Device」
3. 设备已激活或未激活
4. HyperWiFi网络已配置
**操作步骤：**
1. 用户通过设置执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
7. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Device」（与恢厂前一致）
2. 激活后设备模式更新为「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 用户恢厂：HyperWiFi配置，恢厂前USB Host
**属性：** 优先级：P1；摘要：Func_UsbMode_P3MixH_Vali_004；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置版本
2. 设备当前模式为「USB Host」
3. 设备已激活或未激活
4. HyperWiFi网络已配置
**操作步骤：**
1. 用户通过设置执行恢厂操作
2. 恢厂完成后，设备进入Welcome界面
3. 检查设备当前模式
4. 激活设备
5. 检查设备模式
6. 打开WLAN设置，扫描WiFi网络
7. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Host」（与恢厂前一致）
2. 激活后设备模式继续保持「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

### 模式转换验证
#### 激活后模式转换验证
**属性：** 优先级：P1；摘要：Func_UsbMode_ModeSwitch_Vali_001；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备恢厂后处于Welcome界面
2. 当前模式为「USB Device」
3. HyperWiFi网络已配置
**操作步骤：**
1. 执行设备激活操作
2. 激活完成后检查设备模式
3. 打开WLAN设置，扫描WiFi网络
4. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 激活后设备模式更新为「USB Host」
2. WLAN列表可正常扫描到HyperWiFi

---

#### 已激活设备恢厂后模式验证-基线配置
**属性：** 优先级：P2；摘要：Func_UsbMode_ModeSwitch_Vali_002；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备已激活
2. 当前模式为「USB Host」
3. 设备烧录P3MIX基线版本
4. HyperWiFi网络已配置
**操作步骤：**
1. 执行恢厂操作
2. 恢厂完成后检查设备模式
3. 打开WLAN设置，扫描WiFi网络
4. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Device」
2. 激活后设备模式更新为「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 已激活设备恢厂后模式验证-HyperWiFi配置
**属性：** 优先级：P2；摘要：Func_UsbMode_ModeSwitch_Vali_003；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备已激活
2. 当前模式为「USB Host」
3. 设备烧录P3MIX HyperWiFi配置版本
4. HyperWiFi网络已配置
**操作步骤：**
1. 执行恢厂操作
2. 恢厂完成后检查设备模式
3. 打开WLAN设置，扫描WiFi网络
4. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 恢厂后设备模式为「USB Host」
2. 激活后设备模式保持「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 多次恢厂测试-设备模式USB Device
**属性：** 优先级：P2；摘要：Func_UsbMode_ModeSwitch_Stb_001；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置
2. 设备模式为「USB Device」
3. HyperWiFi网络已配置
**操作步骤：**
1. 连续执行恢厂操作3次
2. 每次恢厂后检查USB模式
3. 激活设备
4. 检查最终模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 每次恢厂后设备模式为「USB Device」
2. 激活后模式转换正确为「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

#### 多次恢厂测试-设备模式USB Host
**属性：** 优先级：P2；摘要：Func_UsbMode_ModeSwitch_Stb_002；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备烧录P3MIX HyperWiFi配置
2. 设备模式为「USB Host」
3. HyperWiFi网络已配置
**操作步骤：**
1. 连续执行恢厂操作3次
2. 每次恢厂后检查USB模式
3. 激活设备
4. 检查最终模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 每次恢厂后设备模式为「USB Host」
2. 激活后模式转换正确为「USB Host」
3. WLAN列表可正常扫描到HyperWiFi

---

### 底座切换测试
#### 底座切换：恢厂后未激活，USB Device模式放置底座
**属性：** 优先级：P1；摘要：Func_UsbMode_CradleSwitch_Vali_001；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备恢厂后处于Welcome界面
2. 设备当前模式为「USB Device」
3. 底座可用
4. HyperWiFi网络已配置
**操作步骤：**
1. 检查设备当前USB模式
2. 将设备放置到底座上
3. 等待设备与底座建立连接
4. 检查设备USB模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
7. 激活设备
8. 再次检查USB模式和WLAN扫描
**预期结果：**
1. 放置底座后USB模式切换为「USB Host」
2. WLAN列表可正常扫描到HyperWiFi
3. 激活后USB模式保持「USB Host」
4. WLAN扫描功能正常

---

#### 底座切换：恢厂后未激活，USB Host模式放置底座
**属性：** 优先级：P1；摘要：Func_UsbMode_CradleSwitch_Vali_002；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备恢厂后处于Welcome界面
2. 设备当前模式为「USB Host」
3. 底座可用
4. HyperWiFi网络已配置
**操作步骤：**
1. 检查设备当前USB模式
2. 将设备放置到底座上
3. 等待设备与底座建立连接
4. 检查设备USB模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
7. 激活设备
8. 再次检查USB模式和WLAN扫描
**预期结果：**
1. 放置底座后USB模式保持「USB Host」
2. WLAN列表可正常扫描到HyperWiFi
3. 激活后USB模式保持「USB Host」
4. WLAN扫描功能正常

---

#### 底座切换：已激活设备，USB Device模式放置底座
**属性：** 优先级：P1；摘要：Func_UsbMode_CradleSwitch_Vali_003；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备已激活
2. 设备当前模式为「USB Device」
3. 底座可用
4. HyperWiFi网络已配置
**操作步骤：**
1. 检查设备当前USB模式
2. 将设备放置到底座上
3. 等待设备与底座建立连接
4. 检查设备USB模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 设备USB模式切换为「USB Host」
2. WLAN列表可正常扫描到HyperWiFi

---

#### 底座切换：已激活设备，USB Host模式放置底座
**属性：** 优先级：P1；摘要：Func_UsbMode_CradleSwitch_Vali_004；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备已激活
2. 设备当前模式为「USB Host」
3. 底座可用
4. HyperWiFi网络已配置
**操作步骤：**
1. 检查设备当前USB模式
2. 将设备放置到底座上
3. 等待设备与底座建立连接
4. 检查设备USB模式
5. 打开WLAN设置，扫描WiFi网络
6. 检查是否可扫描到HyperWiFi
**预期结果：**
1. 设备USB模式保持为「USB Host」
2. WLAN列表可正常扫描到HyperWiFi

---

#### 底座切换：多次插拔底座
**属性：** 优先级：P2；摘要：Func_UsbMode_CradleSwitch_Vali_005；类型：手工；标签：HyperWiFi

**前置条件：**
1. 设备可用
2. 底座可用
3. HyperWiFi网络已配置
**操作步骤：**
1. 将设备放置到底座，检查USB模式和WLAN扫描
2. 从底座取下设备，检查USB模式
3. 重复步骤1-2共5次
4. 记录每次模式变化和WLAN扫描结果
**预期结果：**
1. 每次放置底座时USB模式为「USB Host」，WLAN可正常扫描到HyperWiFi
2. 每次取下底座时USB模式恢复为放置前模式

---