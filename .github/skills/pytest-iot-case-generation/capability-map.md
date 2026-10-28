# 能力清单（Capability Map）

生成用例时**只允许**调用本清单内的 API、fixture 和 profile。引用任何符号前必须能在工作区中 grep 到其定义。
映射不上的步骤 → 用 `run_manual_placeholder(case, run_shell_cmd)` 或带原因的 `pytest.skip`，**禁止**编写假想实现。

## 1. Fixtures（testcases/conftest.py）

| 名称 | 类型 | 用途 |
|------|------|------|
| `run_shell_cmd` | `Callable[[str], str]` | 整行 ADB shell 下发；含 `|` 管道在设备端执行，避免 Windows 误解析 |
| `wifi` | `WiFiControl` | 开关 WiFi、连接/断开 SSID、扫描 |
| `adb` | `AdbHelper` | 需细粒度返回码时使用（`shell_line` 返回 `(code, out, err)`） |
| `wifi_yaml` | `dict` | `testdata/android/wifi_ssid.yaml` 加载结果 |
| `weaknet_yaml` | `dict` | `testdata/android/weaknet_scene.yaml` |
| `settings_ui` | `AndroidSettingsUI` | 系统设置 UI 操作 |
| `wifi_ip_settings_ui` | `WiFiIPSettingsUI` | IP 设置页 UI |
| `wifi_add_network_ui` | `WiFiAddNetworkUI` | 手动添加网络 UI |
| `miniap_action_optional` | `MiniAPAction \| None` | miniAP Telnet；未配置时返回 None（不 skip） |
| `wifi_ap_action_optional` | `WiFiAPAction \| None` | 传统 WiFi AP Telnet；未配置时返回 None，支持指定 SSID 编码 |

自动注入：`android_wifi_lifecycle`（autouse）负责 WiFi 生命周期；用 `no_wifi_lifecycle` / `no_dual_wifi_setup` marker 关闭。

产品能力标签：`wifi` 仅传统 WiFi，`hyperwifi` 仅 HyperWiFi，`dualwifi` 必须同时具备两条链路，`common` 可在两类设备上独立执行。`DUT_WIFI_CAPABILITY=wifi|hyperwifi|dualwifi` 控制运行时能力门禁，默认 `dualwifi`。

Welcome 页面能力（`core/libs/android/wifi_ui/welcome_page.py`）：`WelcomeWlanUI.close_hyperwifi_intro()` 点击介绍弹窗关闭按钮，等待弹窗消失并确认返回 WLAN 列表。
`WelcomeWlanUI.expand_all_and_confirm_more_ssids()` 在手持全屏布局保留点击“展开全部”后的新增 SSID 检查；当前大屏内嵌布局无该按钮时，必须实际滚动到列表末尾并发现首屏以外的 SSID 才通过。WLAN 查找与翻页共用 UI hierarchy 中的列表边界，不依赖可能返回竖屏尺寸的 `window_size()`。
`WelcomeWlanUI.dismiss_keyboard()` 根据 `dumpsys input_method` 的 `mInputShown` 安全关闭已显示的软键盘，避免大屏无软键盘时 Back 误关配置框；无法查询状态时明确失败。静态 IP 字段查找先检查所有标签别名，再在配置框实际边界内有界双向翻页。
输入法关闭等待状态实际变为隐藏且只发送一次 Back；IP 选项与取消按钮等待动画后的边界稳定。指定网络入口复用 `wait_for_ssid()`，配置框状态根据配置滚动区和取消按钮判断，不依赖密码框始终可见。

## 2. 用例薄壳 API（testcases/support/case_api.py）

- `wifi_case(summary, title, *, tag="", pre="") -> dict` — 构造 case 元数据
- `run_manual_placeholder(case, run_shell_cmd)` — 不可自动化步骤的显式占位（`pytest.skip("manual: …")`）

## 3. Scenario Runners（core/libs/android/wifi_scenarios/）

用例文件只做薄壳：构造 `case` → 打印 `cmd wifi status` → 调用下表 runner。

### network_204.py — 204 / NetworkMonitor 检测
- `run_204_default_config_case(summary, run_shell_cmd, wifi)` — 默认配置检查
- `run_dual_wifi_204_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 双 WiFi 检测独立性
- `run_dual_wifi_204_period_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 检测周期验证
- `run_dual_wifi_204_disabled_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 关闭 204 场景
- 前置守卫：`require_wan_state(expected, summary)` / `require_204_switch(expected, summary)`（环境不符时自动 skip）
- 解析/断言：`capture_networkmonitor_log`、`parse_captive_success_flags`、`parse_probe_event_epochs`、`assert_network_204_log`、`assert_network_204_disabled_log`、`assert_exponential_probe_intervals`

### ip_reachability.py — 网关/链路可达性
- Runners：`run_dual_wifi_ipreach_case`、`run_dual_wifi_ipreach_ipv6_case`、`run_ipreach_period_case`、`run_ipreach_recovery_case`、`run_ipreach_failover_case`、`run_ipreach_roam_case`、`run_ipreach_ip_mode_switch_case`
- 守卫：`require_ip_mode(expected, summary)` / `require_gateway_state(expected, summary)`
- 断言：`assert_dual_independent_monitor`、`assert_monitor_outcome`、`assert_ns_probe_intervals`

### ip_configuration.py — DHCP / 静态 IP
- Runners：`run_dhcp_acquisition_case`、`run_dhcp_renewal_case`、`run_dhcp_switch_case`、`run_static_configuration_case`、`run_ip_configuration_reboot_case`、`run_default_ip_mode_ui_case`、`run_ip_mode_options_ui_case`、`run_static_fields_ui_case`、`run_static_field_input_ui_case`、`run_mac_privacy_case`
- 工具：`collect_wifi_ipv4_info`、`assert_gateway_reachable`、`assert_wifi_link_details`、`wait_for_wifi_ipv4`、`internet_is_reachable`、`apply_ip_mode`、`reboot_and_wait`
- Profile 选择：`ipcfg_lab_entry(wifi_yaml, name)` + `wifi_entry_for_lab(wifi_yaml, lab_entry)`

### ssidpwd_connection.py — SSID/密码连接
- Runners：`run_ssidpwd_connect_case`、`run_ssidpwd_switch_case`、`run_ssidpwd_qr_case`、`run_ssidpwd_encoding_change_case`、`run_manual_network_connect_case`、`run_add_network_field_case`、`run_add_network_connection_case`、`run_add_network_switch_case`、`run_nrc_miniap_compatibility_case`
- 断言：`assert_gateway_ping`、`assert_ssid_visible_in_scan`
- 收尾：`restore_miniap_default_if_enabled(wifi_yaml, summary=...)`

### ap_configuration.py — AP 配置变更
- `run_wifi_ap_security_case`、`run_wifi_ap_manual_add_security_case`、`run_hidden_network_reboot_stress_case`、`run_preconfigured_wifi_security_case`、`run_wifi_ap_ssid_case`、`run_wifi_ap_ssid_change_case`、`run_wifi_ap_password_change_case`、`run_wifi_ap_security_change_case`、`run_wifi_ap_channel_change_case`

### welcome/ — Welcome WLAN 场景
- `connection_config.py`：`run_welcome_hyperwifi_intro_case`、`run_welcome_open_network_case`、`run_welcome_encrypted_config_case`、`run_welcome_password_input_case`、`run_welcome_empty_password_case`、`run_welcome_password_length_case`、`run_welcome_password_visibility_case`、`run_welcome_clear_password_case`、`run_welcome_cancel_config_case`、`run_welcome_connect_button_case`、`run_welcome_ip_mode_switch_case`、`run_welcome_wrong_password_reopen_case`
- `network_details.py`：`run_welcome_ip_mode_default_case`、`run_welcome_ip_mode_options_case`、`run_welcome_static_fields_case`、`run_welcome_static_field_input_case`、`run_welcome_static_field_rejection_case`、`run_welcome_delete_network_case`、`run_welcome_cancel_static_config_case`、`run_welcome_save_static_config_case`
- `ssid_display.py`：`run_welcome_encoded_ssid_display_case` 保留可控 AP 的编码显示流程；`run_welcome_preconfigured_ssid_display_case` 仅检查环境中已有 SSID，不新增 AP 控制依赖。`WELCOME_SSID_PROFILE_BY_CASE` 维护原用例与共享 profile 的映射。
- `ssid_display.py`：`run_welcome_ssid_display_case(summary, run_shell_cmd, wifi_yaml, welcome_wlan_ui, wifi_ap_action, *, entry_id, settle_sec=5.0)` — 配置传统 AP、检查底层扫描并等待 Welcome WLAN 精确显示；成功或失败均下线自动化 VAP
- `navigation.py`：`run_welcome_expand_networks_case`；`wifi_icon.py`：`run_welcome_hyperwifi_icon_case`；`version.py`：`run_welcome_version_case`
- 用例保留原 markers、参数化和 fixture 声明，仅委托场景函数执行。场景继续使用当前 Welcome 页面及原截图目录，不调用 Settings 页面准备，不改变原等待、连接清理和手工占位行为。

### advanced_settings/ — WLAN 高级设置场景
- `band.py`、`energy_save.py`、`mode.py`、`priority.py`、`roam_sensitivity.py`、`roam_threshold.py`、`timeout_disconnect.py` 分别承接原测试文件的执行逻辑；`run_wlan_<功能>_*_case` 封装默认值、可选项、配置显示、自定义输入、非法输入、生命周期保持和循环检查，具体签名以对应模块为准。
- 既有 `_assert_wlan_*` 共用校验按原参数提升为 `run_wlan_*_case`；测试文件只调用场景函数，不依赖 case ID 分派。没有新增配置、测试数据或页面操作 API。
- `wlan_advanced_settings/conftest.py` 仍提供 `AdvancedSettingsSupportUI`；页面操作复用 `WiFiAdvancedSettingsUI`。各功能原有的重启、Settings/SystemUI WLAN 开关、飞行模式恢复及后台属性检查保持不变，不合并行为存在差异的生命周期 helper。

### hotspot/ — WLAN 热点场景
- `defaults.py`：`run_hotspot_default_switch_case`、`run_hotspot_default_security_case`、`run_hotspot_default_band_case`、`run_hotspot_default_auto_shutdown_case`、`run_hotspot_security_editor_default_case`、`run_hotspot_security_options_case`、`run_hotspot_band_editor_default_case`、`run_hotspot_band_options_case`，参数均为 `(adb, capsys)`。
- `auto_shutdown.py`：`run_hotspot_auto_shutdown_enabled_case(adb, capsys)` 保留无客户端连接时 09:30–10:30 自动关闭窗口；`run_hotspot_auto_shutdown_disabled_case(adb, capsys)` 保留 12 分钟观察。原客户端连接跳过条件及 UI/服务状态检查方式不变。
- `stability.py`：`run_hotspot_toggle_stability_case(adb, capsys)`、`run_hotspot_fast_toggle_stability_case(adb, capsys)` 保留 20 次循环；快速场景仍使用 0.1 秒轮询及主开关坐标缓存。
- 底层复用 `SoftAPControl`，`wlan_hotspot/conftest.py` 的蓝牙/WLAN 重置前置保持不变；原日志名称、输出、异常和手工占位不变。

### connection_config.py — Settings/SystemUI 共用连接配置
- `run_connection_config_case(..., open_networks=None)` — 共用连接配置框断言；Settings 使用默认入口，SystemUI 通过 `open_networks` 注入网络面板入口
- `connection_config_entry(...)` — 按加密类型和 WiFi/HyperWiFi 类型选择连接配置

### settings/wlan_switch.py — WLAN 开关与稳定性
- `run_wlan_switch_on_case` / `run_wlan_switch_off_case` — WLAN 开关与扫描状态校验
- `run_hotspot_wlan_switch_case` — SoftAP 与 WLAN 并发、开关及自动重连
- `run_airplane_wlan_switch_case` — 飞行模式内外 WLAN 开关及自动重连
- `run_cross_component_wlan_switch_case(summary, run_shell_cmd, wifi, settings_ui)` — Settings 与 SystemUI WLAN 开关状态一致性
- `run_wlan_toggle_stability_case` — WLAN 开关循环与 Settings 闪退检查
- `run_wlan_list_scroll_stability_case` — WLAN 列表循环滑动与 Settings 闪退检查
- `run_wrong_password_reconnect_stability_case` — 错误密码拒绝、正确密码循环重连与闪退检查

### settings/wifi_scan_switch.py — WLAN 扫描开关
- `run_wifi_scan_default_case(summary, run_shell_cmd, settings_ui)` — 删除显式扫描配置后验证 ROM 默认 UI 为关闭，并恢复原值
- `run_wifi_scan_always_case(...)` / `run_wifi_scan_toggle_case(summary, run_shell_cmd, wifi, settings_ui)` — 验证始终扫描开关及 WLAN ON/OFF 两态的后台和设置页扫描结果

### settings/connection_status.py — WLAN 连接状态
- `run_conn_status_connected_case` — 验证正常联网时 WLAN 列表显示已连接且无异常提示
- `run_conn_status_no_internet_case` — 在声明 WAN down 的实验室环境验证已关联网络显示无互联网提示
- `run_conn_status_disconnect_case` — 在声明的 WAN 状态下断开当前 WLAN，并验证网络保留为已保存
- `run_conn_status_wrong_password_case` — 验证错误密码连接后的列表状态

### settings/wifi_security.py — WiFi 安全过滤
- `run_wifi_security_switch_case` — WiFi 安全关闭后弱加密网络恢复显示
- `run_wifi_security_filter_case` — WiFi 安全开启时过滤 WEP/Open，切换 WPA2 后恢复显示
- `run_wifi_security_option_absent_case` — 添加网络安全性列表不提供指定弱安全类型

### wifi_security.py — SP 系列 WiFi 安全
- `run_sp_wifi_security_case(case, run_shell_cmd, wifi, settings_ui)` — SP 指 P 系列产品；P 系列进入安全中心半自动流程，V 系列在交互和 AP 修改前按机型能力跳过

### settings/network_details.py — Settings 网络详情
- `run_network_details_status_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 连接状态、信号、频率和安全性
- `run_network_details_advanced_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — HyperWiFi 的 MAC、IP、网关、掩码、DNS 和链路速率，并与系统状态交叉校验
- `run_network_details_edit_password_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — Settings 修改密码并校验断连
- `run_network_details_forget_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — Settings 取消保存并校验断连
- `run_network_details_disconnect_reconnect_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — Settings 断开并重新连接

### settings/primary_backup_icon.py — Settings 主备网络显示与切换
- `run_primary_backup_icon_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, attenuator)` — 按连接顺序或 RSSI/断链触发主备切换，并交叉校验 `ROLE_CLIENT_PRIMARY`、Settings 首行和橙色高亮

### settings/saved_networks.py — 已保存网络
- `run_saved_network_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 验证空保存列表、联网网络保存、错误密码保存项，以及从保存列表/在线详情取消保存
- `run_saved_hidden_network_case(case, run_shell_cmd, wifi, wifi_yaml, add_network_ui, wifi_ap_action)` — 配置隐藏 WPA2 VAP，通过 Settings 添加并验证保存列表

### settings/scan_list.py — Settings WLAN 扫描列表
- `run_settings_scan_list_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action)` — 默认条目信息、AP 增删、加密/开放连接、RSSI 排序及页面恢复耗时
- `run_settings_scan_list_toggle_stability_case(summary, run_shell_cmd, wifi, settings_ui)` — 20 次 WLAN 开关并逐轮验证列表在 6 秒内刷新
- `run_settings_scan_list_user_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 单/双链路连接、断开或取消保存后的 WLAN 列表滚动稳定性

### settings/scan_list_ops.py — Settings WLAN 扫描列表快捷菜单
- `run_settings_scan_list_ops_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action)` — 已连接、已保存未连接及未保存网络的长按菜单和按钮动作

### settings/wifi_auto_on.py — 自动开启 WLAN
- `run_wifi_auto_on_case(summary, run_shell_cmd, settings_ui)` — 默认关闭 UI、扫描前置弹窗、取消和开启动作，并交叉校验 `wifi_wakeup_enabled` / `wifi_scan_always_enabled`

### settings/wifi_icon.py — WLAN 标准与 HyperWiFi 图标
- `run_settings_wifi_icon_case(summary, run_shell_cmd, wifi_yaml, settings_ui)` — 从 Settings 行描述验证 Wi-Fi 4/5/6/7 代际，并以行资源归属和像素签名验证 HYPER Wi-Fi 徽标及 H 图标

### settings/wifi_prompt.py — WLAN 引导接入提示
- `run_settings_wifi_prompt_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 分别连接传统 WiFi/HyperWiFi，验证 WLAN 列表对另一链路类型显示完整引导文案

### systemui/ — SystemUI 快捷设置组件
- `run_systemui_wifi_icon_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 先连接目标网络固定到不可滚动面板首行，再验证 Wi-Fi 代际、HYPER Wi-Fi 徽标和 H 图标
- `run_systemui_status_bar_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui)` — 通过右上角 `wifi_signal` / `sub_wifi_signal` 验证传统、Hyper、双 WiFi 图标及连接、断开和 primary 顺序变化
- `run_systemui_button_case(summary, run_shell_cmd, wifi, settings_ui)` — 快捷设置 WLAN/互联网入口、长按、查看全部和网络详情跳转
- `run_systemui_connection_config_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, *, operation, hyper=False)` — 从 SystemUI 网络面板验证连接配置框
- `run_systemui_switch_page_case(summary, run_shell_cmd, settings_ui)` — 网络页切换、重复打开、锁屏恢复和 5 分钟刷新
- `run_systemui_scan_list_default_case(summary, run_shell_cmd, settings_ui)` — 扫描条目的 SSID、信号和加密图标校验
- `run_systemui_scan_list_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action=None)` — AP 驱动的列表刷新、增删、连接、编码、去重、安全过滤及双 WiFi 条目状态校验
- `run_systemui_ssid_display_case(summary, run_shell_cmd, wifi_yaml, settings_ui, wifi_ap_action)` — 配置复用 SSID profile 并校验 SystemUI 精确字符显示
- `run_systemui_conn_status_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_ui, wifi_ap_action=None)` — SystemUI 单/双 WiFi 连接状态、错误密码、断开及取消保存校验
- `run_systemui_encrypt_icon_case(summary, run_shell_cmd, settings_ui, wifi_ap_action)` — AP 驱动的 WPA/WPA2/WPA3 与 Open/OWE 锁图标矩阵校验
- `run_systemui_ssid_order_case(summary, run_shell_cmd, settings_ui)` — WiFi/HyperWiFi 混合列表按最强 RSSI 降序校验

### wifi_security.py — SP WiFi 安全半自动流程
- `run_sp_wifi_security_case(case, run_shell_cmd, wifi, settings_ui)` — WifiSec Vali_001–017 和 UI_001；人工配置 AP、切换安全开关、观察扫码拒绝，脚本检查界面及保存/连接状态并留证
- 使用 `pytest -s` 单进程执行；人工必须明确输入 `yes/no/skip`，无交互输入则跳过；半自动流程不代表无人值守自动化
- 复用 `WIFISEC_WEAK_SSID`，未设置时询问目标 SSID；不采集密码，不依赖 `WIFISEC_SWITCH` 环境声明

### country_code.py — 国家码 / 占空比
- `run_country_table_case`、`run_adapt_country_mapping`、`run_country_code_switch_stress`
- 守卫/操作：`require_cli_app(run_shell_cmd)`、`force_country_and_restart_wifi`、`simulate_telephony_country_code(..., case_id=None)`、`simulate_cloud_country_code(..., case_id=None)`、`simulate_cloud_country_code_sequence(..., case_id=None)`、`set_eus_duty_cycle`
- 断言：`assert_country_and_duty`、`assert_eus_duty_cycle`

### channel_plan.py — Halow 信道/频宽
- `run_channel_automation_case`（主入口）、`setup_halow_region_country`、`restore_halow_us_default`
- 工具：`pick_wifi_yaml_entry(case, wifi_yaml)`、`halow_frequency_mhz`、`channel_settle_sec`、`assert_dut_channel`

### performance.py — 性能（吞吐量/时延/连接耗时）
- Runners：`run_throughput_case(..., wifi_entry_id=None)`、`run_pat_throughput_case(case, run_shell_cmd, wifi, wifi_yaml, attenuator)`、`run_ping_latency_case(case, run_shell_cmd, wifi, wifi_yaml)`、`run_connection_latency_case(case, run_shell_cmd, wifi, wifi_yaml)`
- 吞吐量用例需要固定网络配置时，通过 `wifi_entry_id` 显式引用 `wifi_list` 条目，禁止使用 `case["tag"]` 选择网络
- PAT 未配置基线时进入数据采集模式：按标题选择网络和 TCP/UDP，从当前 RSSI 开始每 5 dB 扫描至断连，每个 TX/RX 方向采集 2 组并归档。配置 `performance_pat.<case_id>` 后增加产品基线自动判定：配置 `wifi_entry_id`、`ap_index`、`min_disconnect_rssi_dbm`、`inflection_rssi_dbm`、`inflection_drop_pct`，以及至少两个按强到弱排列的 `points`；每个点配置 `rssi_dbm`、`min_tx_mbps`、`min_rx_mbps`，可选 `max_drop_pct`
- 判别：`is_stress_case(case)`、`is_throughput_tcp_udp_case(summary)`、`is_ping_latency_case(summary)`、`is_connection_latency_case(summary)`
- 工具：`pick_wifi_entry`、`connect_by_entry`、`parse_iperf_mbps`、`parse_ping_metrics`、`archive_iperf_run`

### status_capture.py — WiFi 状态采集
- `attach_wifi_status(case_id, run_shell_cmd)` — 在“检查 DUT WiFi 初始状态”步骤中采集 `cmd wifi status` 并附加文本结果；runner 统一调用，用例脚本不重复打印

### hyperwifi_low_power.py — HyperWiFi 低功耗
- `run_hyperwifi_wlan_cycle_stability_case(summary, run_shell_cmd, wifi, wifi_yaml, *, cycles=None)` — 亮屏下循环关闭/开启 WLAN，逐轮验证 IDLE/ACTIVE 状态与 HyperWiFi 自动回连
- `run_hyperwifi_airplane_cycle_stability_case(summary, run_shell_cmd, wifi, wifi_yaml, *, cycles=None)` — 亮屏下循环开启/关闭飞行模式，逐轮验证 IDLE/ACTIVE 状态
- `run_hyperwifi_no_saved_screen_off_idle_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 清空保存网络并息屏，验证无 PNO 时进入 DEEP_NONTIM 与 IDLE
- `run_hyperwifi_dual_screen_on_case(summary, run_shell_cmd, wifi, wifi_yaml, *, operation)` — 双 WiFi 按序连接、断开单腿或静置时验证 HyperWiFi 保持 ACTIVE
- `run_hyperwifi_dual_screen_transition_case(summary, run_shell_cmd, wifi, wifi_yaml, *, operation)` — 双 WiFi 断开单腿或保持连接后息屏/亮屏，验证 PowerSave、IDLE 与 ACTIVE 转换

### reconnect_rssi.py — RSSI 回连阈值
- `run_reconnect_rssi_threshold_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, *, hyper, no_reconnect_rssi, reconnect_rssi, expected_band="")` — 最大衰减下连续确认断链，再从弱信号侧逐步降低衰减，记录首次稳定回连 RSSI 并验证阈值

### qr_scanner.py — 扫码连接
- `run_wifi_scanner_case(...)`；`WifiQrDisplay`（上下文管理器，弹窗显示二维码）；`wifi_qr_payload(ssid, password, security="WPA2")`

### dual_link_failover.py — 双链路主备切换
- `run_beacon_loss_failover_case(summary, run_shell_cmd, wifi, wifi_yaml, *, loss_target, expect_failover=True, expect_primary="wifi", hyper_region="US", dual_wifi_entry_id=None, settle_sec=45.0)` — beacon loss 触发主备切换；`loss_target`="wifi"/"hyper"，`expect_primary`="wifi"(wlan0)/"hyper"(wlan1)，`expect_failover=False` 用于“备链路 beacon loss 不触发”
- `run_score_debounce_failover_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 校准传统WiFi/HyperWiFi为-65/-70 dBm并建立WiFi主链路，立即将WiFi降至-73 dBm，逐个采集5次独立候选评分，验证前4次不切换且第5次Hyper成为主链路
- `run_screen_off_wifi_pno_failover_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 建立Hyper备链路与传统WiFi主链路，将WiFi衰减至断链，息屏后恢复至-65 dBm，验证PNO自动重连且WiFi恢复主链路，并恢复衰减器与屏幕状态
- `run_screen_off_hyper_pno_failover_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 建立传统WiFi备链路与Hyper主链路，将Hyper衰减至断链，息屏后恢复至-65 dBm，验证PNO自动重连且Hyper恢复主链路，并恢复衰减器与屏幕状态
- 解析/断言：`parse_link_roles(log_text)`、`assert_beacon_loss_and_failover(log_text, *, summary, expect_primary_iface)`、`capture_failover_log(adb, duration_sec)`
- 物理操作（衰减器/断电）由 runner 打印步骤引导；设 `DUAL_LINK_MANUAL_CONFIRM=1` 进入逐条回车确认的联调模式

### net_selection.py — 网络选择扫描
- `run_autoscan_skip_hyper_traffic_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — Home页绑定活动数据接口生成20包/秒流量，验证wlan1不扫描与`hasActiveStream:true`，停止流量并按1 dB/s降低RSSI后验证低流量策略日志
- `run_autoscan_recent_selection_skip_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 保存miniAP1/2并使miniAP2信号更优，WLAN关闭3秒后开启，验证10秒内跳过网络选择且保持miniAP1，并恢复CH13/15及新增保存项
- `run_candidate_skip_hyper_traffic_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — Settings页绑定wlan1生成20包/秒流量，验证10秒扫描、`hasActiveStream:true`，停止流量并按1 dB/s降低RSSI后验证低流量策略日志
- `run_score_hyper_candidates_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, stronger_target_rssi=..., weaker_target_rssi=..., expected_rssi_scores=..., require_equal_final_scores=...)` — CH13/CH15校准miniAP1/2，验证两路候选评分及RSSI择优，并恢复两路衰减与新增保存项
- `run_screen_on_disconnected_hyper_scan_case(summary, run_shell_cmd, wifi, wifi_yaml, miniap_action)` — 保存HyperWiFi后临时停止miniAP无线，在亮屏Home页验证未连接wlan1的20秒扫描周期，并在finally恢复miniAP无线
- `run_screen_on_scan_backoff_reset_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 校准HyperWiFi至-88 dBm并等待wlan1退避到80秒，息屏亮屏后验证扫描重置为20/40/80/160秒，恢复衰减与亮屏状态
- `run_screen_on_single_link_disconnected_radio_scan_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 分别建立仅传统/仅Hyper单链路，验证未连接接口实际扫描退避且调度序列完整包含20/40/80/160秒
- `run_dual_link_network_selection_independence_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 双链路连接并分别校准至-88 dBm，验证wlan0/wlan1各自扫描并独立进入网络选择，恢复两路衰减
- `run_candidate_skip_hyper_rssi_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 校准HyperWiFi至-80 dBm，在Settings周期扫描时验证当前链路充足且跳过候选提名
- `run_candidate_skip_wifi_rssi_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, expected_band=..., threshold_rssi=...)` — 锁定传统WiFi分频段BSSID并校准到阈值以上，在Settings周期扫描时验证当前链路充足且跳过候选提名
- `run_screen_on_settings_periodic_scan_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, *, hyper=True, target_rssi=-75)` — 可选校准传统 WiFi 或 HyperWiFi RSSI，在亮屏 Settings 页验证对应接口以 10 秒周期扫描并恢复衰减值
- `run_screen_on_hyper_rssi_scan_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, target_rssi=..., expect_scan=...)` — 亮屏Home页校准HyperWiFi RSSI，低信号验证退避扫描、高信号验证无扫描，并检查连接保持与恢复衰减值
- `run_pno_connected_screen_off_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 连接 HyperWiFi 后息屏，验证连接保持且固件未启动 PNO 扫描，并恢复亮屏
- `run_pno_disconnected_screen_off_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, *, hyper=True, screen_off_before_disconnect=False, verify_reconnect=True)` — 衰减器模拟传统 WiFi 或 HyperWiFi AP 不可达，按用例顺序息屏并验证 PNO 启动，可选验证恢复信号后自动回连
- `run_pno_miniap_reboot_screen_off_case(summary, run_shell_cmd, wifi, wifi_yaml, miniap_action)` — 连接可控miniAP的HyperWiFi后息屏并后台重启miniAP，验证先断连、启动PNO且从PNO开始30秒内回连，恢复亮屏
- `run_pno_no_saved_network_screen_off_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 连接后取消保存并确认保存列表为空，息屏验证不启动 PNO，并恢复亮屏
- `run_screen_off_wifi_roaming_scan_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 校准传统 WiFi 至 -76 dBm，息屏施加弱信号并验证 wlan0 发起漫游扫描，恢复衰减与亮屏
- `run_autoscan_after_wlan_toggle_case(summary, run_shell_cmd, wifi)` — 验证 WLAN 关闭再开启后系统自主发起一次网络选择扫描；不主动调用 `cmd wifi start-scan`
- `run_autoscan_after_disconnect_case(summary, run_shell_cmd, wifi, wifi_yaml, settings_page=False)` — 验证 Settings 或非 Settings 页面断连后的自主扫描
- `run_autoscan_after_airplane_cycle_case(summary, run_shell_cmd, wifi)` — 验证飞行模式开启再关闭后的自主扫描
- `run_autoscan_after_screen_wake_case(summary, run_shell_cmd, wifi)` — 验证未连接状态息屏再亮屏后的自主扫描
- `run_autoscan_after_weak_signal_disconnect_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 通过现有传统 WiFi 信号 profile 和衰减器验证弱信号断连后的自主扫描，并恢复通道原值
- `run_autoscan_airplane_wlan_enable_case(summary, run_shell_cmd, wifi, wifi_yaml)` — 验证飞行模式下开启 WLAN 后自主扫描并重连
- `run_autoscan_skip_wifi_rssi_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator, expected_band=..., threshold_rssi=...)` — 锁定传统 WiFi 分频段 BSSID，验证高于 RSSI 阈值时目标接口不扫描、低于阈值后启动 20s 周期扫描，并恢复衰减值
- `run_autoscan_skip_hyper_rssi_case(summary, run_shell_cmd, wifi, wifi_yaml, attenuator)` — 复用 HyperWiFi US profile 与 CH13，验证 wlan1 高于 RSSI 阈值不扫描、低于阈值恢复退避扫描，并恢复衰减值
- 解析/断言：`parse_network_selection_scan_events(log_text)`、`assert_single_immediate_scan(log_text, elapsed_sec=..., summary=...)`

## 4. 测试数据 Profile（testdata/android/wifi_ssid.yaml）

- `wifi_list` — 普通 AP 连接条目
- 传统加密预置网络：`wifi_wep40_lab`、`wifi_wep104_lab`、`wifi_wep128_lab`、`wifi_owe_transition`；WEP 密钥分别由同名 `WIFI_WEP*_PASSWORD` 环境变量提供，OWE 过渡环境由 `OWE_TRANSITION_LAB=1` 启用
- `dual_wifi_list` — 双 WiFi 条目（如 `dual_wifi_24g_hyperwifi_us`）
- `ipcfg_lab` — IP 实验室条目（`ap1` 等，经 `ipcfg_lab_entry` 使用）
- `enterprise_wifi` — 802.1X 企业网（Office_8021X）
- `ssid_pwd_profiles` — SSID/密码编码矩阵：`scanner_default`、`ssid_ascii_min_password_min`、`ssid_utf8_chinese_10`、`ssid_gbk_chinese_16`、`ssid_shift_jis_japanese_16`、`ssid_cp949_korean`、`ssid_nonexistent` 等（按需 grep 确认全名）

**复用原则**：新增 profile 前先搜索现有条目；相同测试目的优先复用并对齐非关键值（见仓根 copilot-instructions）。

## 5. 环境变量守卫（实验室前置）

| 变量 | 含义 |
|------|------|
| `NETWORK_204_WAN` | 实验室外网 up/down（`require_wan_state`） |
| `NETWORK_204_SWITCH` | 204 开关 on/off（`require_204_switch`） |
| `ADB_REQUIRE_ROOT` | 默认 1；非 root 设备设 0 跳过 root 校验 |
| `DUAL_LINK_MANUAL_CONFIRM` | 设 1 时主备切换物理操作逐条回车确认（联调模式） |

> 本清单靠人工维护：新增 runner/fixture/profile 时同步更新，否则生成规则会拒绝引用它。
