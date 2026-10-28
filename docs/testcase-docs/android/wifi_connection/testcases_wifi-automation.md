# 无线接入（testcases.md）— 自动化说明

需求原文：`tools/files-transfer/testcases.md`（同步副本：`testcases.md`）。脚本为 **静态 pytest 文件**（与 `tools/pytest-automation/reference.md` 模板一致），**运行 pytest 时不读取 md**。

## 模块划分（21 个文件，381 项 pytest 用例 / 361 个唯一 case_id）

`pytest testcases/android/wlan_access --collect-only` 实测收集 **381** 项。其中 **20 个 case_id 在各自文件内被重复收集**（同一 ID 出现在两个函数上），去重后唯一 case_id 为 **361** 个，正式报表统计口径应以唯一 ID 为准。

| 统计口径 | 数值 |
|---------|------|
| pytest 收集项（含重复 ID） | 381 |
| 唯一 case_id | 361 |
| 重复 case_id 组数 | 20（详见下方「已知问题」） |
| 已自动化（唯一 ID，未调用 `run_manual_placeholder`） | 59 |
| 自动化占比（59 / 361） | **16.34%** |
| 手工/UI/专用 AP 占位（调用 `run_manual_placeholder`） | 302 |

自动化用例集中在 `test_func_wlanaccess_conn_channel.py`（信道遍历）、部分 `conn_encrypt` / `conn_ipcfg` / `conn_manual` / `conn_ssidpwd` / `reconnect_apchange` 用例；其余脚本均为 `run_manual_placeholder(case, run_shell_cmd)` 占位（手工/UI/专用 AP 场景）。

完整列表：`test_func_wlanaccess_*`（连接 / 网络 / 双链路 / 重连等子模块）。

## SSID/密码字符处理自动化范围

`test_func_wlanaccess_conn_ssidpwd.py` 共 23 个用例，按实际函数实现标记：

- 自动化 13 个：`Vali_001`～`Vali_005`、`Vali_007`～`Vali_014`，均调用 `run_wifi_ap_ssid_case`。
- 手工占位 10 个：`Vali_006`、`Excp_001`～`Excp_009`，均调用 `run_manual_placeholder`。

自动化标记只表示已接入可执行 runner，不表示实机通过。2026-09-18 实机结果为 5 passed / 8 failed：`Vali_001/002/005/007/008` 通过；`Vali_003` 受 AC 二次确认与 Telnet 响应时序影响；`Vali_004` 的 64 位非十六进制 WPA2 文本密码被 AC 拒绝；`Vali_009`～`Vali_014` 的 GBK、Shift_JIS、CP949 SSID 在 AP 在线时被 DUT 显示为 `<unknown ssid>`。

### 已知问题：20 个重复 case_id

以下 case_id 在同一文件内被两个不同函数重复使用，需在后续清理中改为唯一编号（不影响本次统计已按唯一 ID 去重口径计算）：

`Func_WlanAccess_Conn_EAP_Vali_007`、`Func_WlanAccess_Conn_Scanner_Vali_007`、`Func_WlanAccess_Network_204_Excp_003/004`、`Func_WlanAccess_Network_204_Vali_003/005/007/009/011/014`、`Func_WlanAccess_Network_IpReachMon_Excp_001/002`、`Func_WlanAccess_Network_IpReachMon_Int_004`、`Func_WlanAccess_Network_IpReachMon_Vali_001/002/003`、`Func_WlanAccess_PriBakLink_Connect_Int_003/004`、`Func_WlanAccess_Reconnect_StaChange_Excp_001/002`

## 加密方式自动化范围

`test_func_wlanaccess_conn_encrypt.py` 共 61 个唯一用例，以下 22 个已接入自动化 runner：

- WEP：`001`、`002`、`003`（复用实验室预置 VAP，密钥由环境变量提供）
- WPA-CCMP：`004`
- WPA-TKIP/CCMP：`005`
- WPA2-TKIP：`006`
- WPA2-CCMP：`007`、`008`、`009`
- WPA2-TKIP/CCMP：`012`
- WPA/WPA2-TKIP：`013`
- WPA/WPA2-CCMP：`014`、`015`、`016`
- WPA/WPA2-TKIP/CCMP：`019`
- WPA2/WPA3：`020`、`021`、`031`
- WPA3：`028`
- Open/OWE：`052`、`053`
- OWE 过渡模式：`054`（复用预置 `Lab_HW_OWE_Test`）

其余 39 个保留手工或专用 AP。WEP 用例依赖 `WIFI_WEP40_PASSWORD`、`WIFI_WEP104_PASSWORD`、`WIFI_WEP128_PASSWORD`，缺少凭据时明确跳过；OWE 过渡模式要求预置 AP1 SSID 对 DUT 可见，并通过 `OWE_TRANSITION_LAB=1` 启用。企业级 802.1X、Portal、MAC 认证、SAE-PK/OCV、GCMP/CNSA、WAPI 和 FT 漫游仍需补充认证/UI runner 或专用环境。TKIP 相关 5 条已于 2026-09-07 在 AirEngine9700S-S、AP0、5G 环境连续两轮实测通过。

2026-09-18 启用门禁后的实机结果：`001/003` 能扫描到目标 WEP VAP，但使用当前提供的凭据连续三次关联失败；`002` 连续三次扫描不到 `Lab_HW_WEP-104_Test`；`054` 连续三次扫描不到 AP1 的 `Lab_HW_OWE_Test`。这 4 条仅表示自动化 runner 已落地，尚不可计为实机通过。`010/011/017/018` 的 AES+TKIP 与 PMF 组合被 AirEngine9700S-S 明确拒绝，设备提示 PMF optional/mandatory 仅对 WPA2-AES、WPA2-WPA3、WPA3 或 OWE 生效；`014/015` 的 WPA/WPA2 mixed + PMF 同样被当前 AC 拒绝。运行动态 AP 自动化用例前必须配置 `ap_config`；未配置时用例会明确跳过。

共享用例 API：`core/libs/android/wifi_case_api.py`  
信道自动化：`core/libs/android/wifi_cases/channel.py`  
信道计划：`test_func_wlanaccess_conn_channel.py` 内联定义
频点对照：`testdata/miniap/halow_frequency_tables.yaml`

## 用例编号格式

摘要 ID 形如 `Func_WlanAccess_<模块>_<子模块>_<Vali|Excp|UI|Stb|Int>_NNN`，例如：

- `Func_WlanAccess_Conn_Channel_Vali_001`
- `Func_WlanAccess_Conn_Encrypt_Vali_008`

## 环境变量

| 变量 | 含义 |
|------|------|
| `WIFI_WLAN_MODE_LAB=1` | 信道类用例需实验室 AP/miniAP 与 DUT 已配置 |
| `MINIAP_LAB=1` | Vali_001~003：Telnet 调用 `MiniAPAction.set_bandwidth_channel()` 遍历 HaLow 信道 |

## 信道计划（测试脚本内联）

| 用例 ID | driver | 说明 |
|---------|--------|------|
| `Func_WlanAccess_Conn_Channel_Vali_001` | miniAP | US，1/2/4 MHz |
| `Func_WlanAccess_Conn_Channel_Vali_002` | miniAP | EU 800MHz |
| `Func_WlanAccess_Conn_Channel_Vali_003` | miniAP | EU 900MHz |
| `Func_WlanAccess_Conn_Channel_Vali_004` ~ `006` | ap | 2.4G / 5G / 6E（AP 切换未自动化） |

## 文档变更后

```bash
python tools/files-transfer/xlsx2md.py -i testcases.xlsx -o testcases.md
python tools/files-transfer/generate_wifi_connection_tests.py
```

## 运行

```bash
python -m pytest testcases/android/wlan_access/test_func_wlanaccess_conn_channel.py --collect-only -q

set WIFI_WLAN_MODE_LAB=1
set MINIAP_LAB=1
python -m pytest testcases/android/wlan_access/test_func_wlanaccess_conn_channel.py -v
```
