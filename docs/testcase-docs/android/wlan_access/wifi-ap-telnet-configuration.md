# 传统 WiFi 陪测 AP 后台 Telnet 配置指南

> 已在实验室设备实测：AirEngine9700S-S，VRP 5.170，软件版本 V200R023C00SPC100，
> 设备提示符 `<AirEngine9700S-S-2024>`。

> 适用范围：`testcases/android/wlan_access/**` 中依赖陪测 AP 完成 SSID / 加密方式 / 信道配置的用例
> （如 `test_func_wlanaccess_conn_encrypt.py`、`test_func_wlanaccess_conn_channel.py`、
> `test_func_wlanaccess_conn_manual.py` 中标注 `AP（HW AirEngineer9700S-S）配置...` 的前置条件）。
> 目的：记录如何通过 Telnet 登录 AirEngine9700S-S 并下发 SSID、加密方式、传统 WiFi（2.4G/5G）信道，
> 供后续把“手工/半自动”用例改造为自动化脚本时参考，**不在 pytest 运行期读取本文件**。

## 1. 设备角色与拓扑

```
DUT (Android) <== 2.4G/5G WiFi ==> AirEngine9700S-S（陪测 AP，Fat/自治模式） <== 有线 ==> 测试台交换机/网关
                                         ^
                                         | Telnet（后台命令行，VRP 风格 CLI）
                                    测试主机（本框架）
```

- 当前设备工作在 `Standard (working independently)` 模式，但控制器下挂多个 AP，配置模型为
  `ssid-profile` / `security-profile` / `vap-profile` / `ap-id` / `radio`。下发信道前必须确认目标
  `ap-id`，不能使用通用的 `interface wlan-radio` 模板。
- 与 `core/libs/access_points/miniap.py` 管理 miniAP 的思路一致：**Telnet 登录 + 逐条下发命令 +
  `display` 命令核验**，仅 CLI 语法不同。

## 2. 账密与配置落点

复用框架现有的“陪测 AP”配置槽位（`core/utils/config_loader.py` 的 `APConfig`，对应
`config/test_config.json` 的 `ap_config`）：

```json
"ap_config": {
  "ap_ip": "192.168.2.1",
  "ap_login_username": "test",
  "ap_login_password": "",
  "ap_flag": "<AirEngine9700S-S-2024>"
}
```

> `ap_flag` 用于 `TelnetSession.login()` 内部 `read_until(prompt)` 判断登录/命令执行是否结束，
> 必须与设备实际提示符（含尖括号 `<...>` 或方括号 `[...]`）逐字符一致，登录后可用
> `display current-configuration | include sysname` 核实。

> 登录密码从环境变量 `AP_LOGIN_PASSWORD` 读取（`.env` 或 CI 密钥），**不要写入 `test_config.json`**；
> miniAP 对应 `MINIAP_LOGIN_PASSWORD`。模板见根目录 `.env.example`。

## 3. 登录交互差异（重要）

`core/utils/telnet_session.py` 的 `TelnetSession.login()` 默认按 `login:` / `Login:` 提示符等待
用户名输入，这是面向 miniAP（Linux/BusyBox 风格）设计的。**传统 WiFi AP 的用户名提示符通常是
`Username:`**，直接复用 `login()` 可能等不到匹配而超时，建议二选一：

1. **推荐**：在业务层使用 `core/libs/access_points/wifi_ap.py` 里的底层
   `TelnetClient` 自行走一遍握手，而不是套用 `TelnetSession.login()`：

   ```python
   from core.utils.telnet_helper import TelnetClient

   client = TelnetClient(ap_ip, port=23, timeout_sec=15)
   client.connect()
   client.read_until(b"Username:", timeout_sec=10)
   client.write_line(username)
   client.read_until(b"Password:", timeout_sec=10)
   client.write_line(password)
   client.read_until(prompt.encode(), timeout_sec=10)  # b"<AirEngine9700S-S-2024>"
   ```

2. 或者给 `TelnetSession.login()` 增加可选 `username_prompt` 参数（不同设备提示符不同），
   在改造为自动化代码时再评估是否值得抽象为通用能力（当前仅 miniAP 用到，避免过度设计）。

登录后若需要免交互执行多条命令，同样可复用 `TelnetClient.execute()` /
`TelnetSession.execute_command()`，一次调用可传入以 `\n` 分隔的多行命令。

## 4. VRP 视图切换速查

```
<AirEngine9700S-S-2024>screen-length 0 temporary
<AirEngine9700S-S-2024>display version
<AirEngine9700S-S-2024>display current-configuration
<AirEngine9700S-S-2024>system-view
[AirEngine9700S-S-2024]wlan
[AirEngine9700S-S-2024-wlan-view]quit
[AirEngine9700S-S-2024]quit
<AirEngine9700S-S-2024>save       # 保存配置（有 Y/N 确认，自动化需单独应答 y）
```

> 每次改动 SSID / 加密 / 信道后建议 `display this`（当前视图配置）或
> `display current-configuration` 核实是否生效，再切回 DUT 侧 `cmd wifi status` 对照。

## 5. SSID 配置命令模板

```
system-view
wlan
ssid-profile name ssid_test01
 ssid Func_WlanAccess_Test
 quit

vap-profile name vap_test01
 ssid-profile ssid_test01
 quit
```

- SSID 长度限制：传统 WiFi AP profile 一般允许 1~32 字节（对应用例 `Func_WlanAccess_Conn_Manual_UI_001`
  “SSID长度>32位报错”场景，用于反向验证边界）。
- 隐藏 SSID：实测命令位于 `ssid-profile` 视图，关键字为 `ssid-hide`；恢复广播使用
  `undo ssid-hide`。
- 中文/GBK/Shift_JIS/CP949 等编码 SSID（对应 `_008`~`_010` 用例）：SSID 编码通常取决于终端网页/CLI
  当前会话编码，Telnet 会话建议按 `core/utils/telnet_helper.py` 的 `encoding` 参数显式指定
  `gbk` / `shift_jis` / `cp949` 后再 `write_line`，避免用 UTF-8 误写入。

## 6. 加密方式配置命令模板

用例文档中出现的加密组合（详见 `tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md` 第
520~900 行 `Func_WlanAccess_Conn_Encrypt_*`）：WEP-40/104/128、WPA-TKIP/CCMP、
WPA2-TKIP/CCMP（含 PMF 强制/可选/关闭）、WPA/WPA2 混合、WPA2/WPA3 混合（含 PMF）、WPA3-SAE。

```
system-view
wlan
security-profile name sec_wep40
 security wep
 wep key 0 wep-40 pass-phrase 12345
 quit

security-profile name sec_wep104
 security wep
 wep key 0 wep-104 pass-phrase 1234567890123
 quit

security-profile name sec_wep128
 security wep
 wep key 0 wep-128 pass-phrase 1234567890123
 quit

security-profile name sec_wpa
 security wpa psk pass-phrase 24681357 aes
 quit

security-profile name sec_wpa2_pmf_required
 security wpa2 psk pass-phrase 24681357 aes
 pmf mandatory
 quit

security-profile name sec_wpa_wpa2
 security wpa-wpa2 psk pass-phrase 24681357 aes
 quit

security-profile name sec_wpa3_sae
 security wpa3 sae pass-phrase 24681357 aes
 pmf mandatory
 quit

security-profile name sec_wpa2_wpa3
 security wpa2-wpa3 psk-sae pass-phrase 24681357 aes
 pmf optional
 quit

vap-profile name vap_test01
 security-profile sec_wpa2_ccmp_pmf_required
 quit
```

以上命令来自设备现有配置和 `?` 帮助。现有 profile 已覆盖 Open、Enhanced Open、WEP-40/104/128、
WPA、WPA2、WPA3、WPA/WPA2、WPA2/WPA3、WPA2/WPA3-Enterprise 及 PMF optional/mandatory。
更换正在使用的安全 profile 会使对应 SSID 短暂中断，建议新建独立 profile 后再绑定到测试 VAP。

## 7. 传统 WiFi 信道遍历命令模板

区别于 `wifi_cases.channel.run_channel_automation_case` 里 `"driver": "miniAP"` 走的 Sub-1G
HaLow 信道（见 `core/libs/access_points/miniap.py::set_channel`），此设备传统 WiFi 信道配置位于
`wlan -> ap-id -> radio` 视图。`radio 0` 为 2.4G、`radio 1` 为 5G。2026-07-29 实机
`display ap all` 显示 `ap-id 1 (AP1)` 为 idle，当前在线目标为
`ap-id 2 (AP2, 192.168.2.80)`；执行时以配置文件的 `ap_id` 为准：

```
system-view
wlan
ap-id 2
 radio 0
 channel 20mhz 6
 quit
 radio 1
 channel 20mhz 149
 quit
 quit
quit
```

- `radio 0` 实测 20MHz 可选信道：`1~13`。
- `radio 1` 实测 20MHz 可选信道：`36,40,44,48,52,56,60,64,149,153,157,161,165`。
- `radio 1` 实测频宽关键字：`20mhz`、`40mhz-minus`、`40mhz-plus`、`80mhz`、`80+80mhz`、
  `160mhz`、`320mhz`；例如 `channel 80mhz 149`。`channel 40mhz` 是模糊命令，必须明确
  使用 `40mhz-minus` 或 `40mhz-plus`。
- `radio 2` 返回 `No configurable channel`，不纳入遍历。
- 当前法规域没有列出 5G 的 `100~144` 信道，遍历代码必须以设备 `channel <bandwidth> ?`
  返回值为准，不能硬编码其他法规域信道。
- 每次切换信道后建议等待 AP 完成射频重启（经验值 5~10 秒）再触发 DUT 侧连接/扫描，
  可参考 `core/libs/access_points/miniap.py` 中 `_reload_halow` 的“下发后 `sleep` 再核验”写法。

## 8. 与框架集成建议（后续自动化落地时参考）

如果要把 `test_func_wlanaccess_conn_channel.py` / `test_func_wlanaccess_conn_encrypt.py` 里的
手工/占位用例改造为自动化，使用 `core/libs/access_points/wifi_ap.py`，结构上对齐
`core/libs/access_points/miniap.py`：

```python
class WiFiAPAction:
    def __init__(self, settings=None, *, client=None):
        self._client = client  # 直接持有 TelnetClient，登录走本文件 §3 的自定义握手
        self._ap = (settings or get_settings()).ap_config

    def _login(self):
        ...  # 见 §3：Username: / Password: / prompt 三段式

    def set_ssid(self, ssid: str) -> None: ...
    def set_security(self, profile: str, **kwargs) -> None: ...
    def set_channel(self, radio: str, channel: int, bandwidth_mhz: int = 20) -> None: ...
    def traverse_channels(self, radio: str, channels: list[int], bandwidth_mhz: int = 20): ...
```

`radio` 建议取值 `"2g"` / `"5g"`，内部映射到目标 `ap-id` 的 `radio 0` / `radio 1`；
`ap_id` 必须作为配置参数，当前在线值为 `2`，但执行前仍应通过 `display ap all`
核对 AP 名称、MAC 和在线状态。

## 9. 验证与排障

- 下发命令后核实：`display current-configuration`、`display vap ssid <ssid>`、
  `display station ssid <ssid>`（在线终端）。
- DUT 侧交叉核对：`run_shell_cmd("cmd wifi status")`（框架内已有的惯用排查手段，
  参见 `test_func_wlanaccess_conn_manual.py` 中多处 `Step 1` 用法）。
- 若 Telnet 会话卡在命令回显未结束：多为 `prompt` 与 `ap_flag` 不完全匹配（尖括号/方括号/
  设备名大小写），优先检查 `config/test_config.json` 里 `ap_flag` 的取值。

## 10. 仍需确认

- [x] WEP / WPA / WPA2 / WPA3 / 混合模式及 PMF 语法已从当前配置核实。
- [x] 隐藏 SSID 关键字已通过 `ssid-profile` 视图帮助核实为 `ssid-hide`。
- [x] 20/40/80MHz 及更高频宽关键字已通过 `radio 1` 视图帮助核实。
- [ ] GBK / Shift_JIS / CP949 SSID 的 CLI 输入编码与 DUT 显示需做一次端到端验证。
- [ ] 将 `ap-id`、目标 VAP/profile 名称加入配置层，避免自动化脚本误操作其他实验室 AP。