# PyAutoTest_IoT

Android WiFi / IoT 自动化测试框架（pytest + ADB + Telnet），按产品域拆分用例，配置、数据与业务库分层。

## 关于此备份

此仓库是 2026-10-28 导出的独立源码快照，仅作额外备份，不是主开发仓库，也不会与主仓库自动同步。

- 包含导出时全部 471 个受版本控制的文件，不复制主仓库的 Git 历史。
- 不包含 `.env`、虚拟环境、缓存、运行报告和临时文件。
- 设备登录密码、共享 WiFi 密码和设备序列号已替换为示例值；代码、测试数据、文档及 Excel 中的相关引用同步脱敏。
- 示例值不是实际实验室凭据。运行前请按下文配置本地 `.env` 和测试数据；历史独立脚本中的设备参数也需自行配置。
- 导出和推送在隔离副本中进行，主项目的源码、`origin`、默认推送目标、分支跟踪关系、索引和提交历史均保持不变。

导出验证：单元测试 890 项通过，生产用例 2010 项收集成功。另有 3 项既有单元测试失败，已在未脱敏的原始提交独立导出中复现：2 项依赖未纳入版本控制的临时 XML，1 项开放网络 SSID 的断言与共享数据不一致。此备份不修改这些既有问题。

## 目录结构

```
.
├── README.md
├── .gitignore
├── pytest.ini              # pytest 路径、标记、日志格式
├── requirements.txt
├── run.py                  # 推荐入口：场景化收集 + 报告路径
├── .env                    # 本地环境变量（不提交 Git，见 .env.example）
├── config/
│   ├── test_config.json    # AP / miniAP / DUT / Android 串号、报告路径提示（不放明文凭据）
│   └── env_config.json     # 环境 profile（dev / test / prod）—— 预留，当前无代码读取
├── core/
│   ├── testdata_loader/    # 测试数据加载与查询
│   │   ├── android/        # wifi_ssid、country_code_tables 等
│   │   └── miniap/         # HaLow 频点表、信道计划展开工具
│   ├── libs/               # 设备侧业务封装
│   │   ├── access_points/  # 传统 WiFi AP 与 HaLow miniAP 控制
│   │   └── android/
│   │       ├── lab_requirements.py # 实验室能力与前置条件检查
│   │       ├── logcat_parsers.py   # Android 日志解析
│   │       ├── wifi/       # WiFi 状态、连接、清理、控制与校验
│   │       ├── wifi_ui/    # Android Settings WiFi Page Objects
│   │       └── wifi_scenarios/ # pytest 场景编排
│   └── utils/              # ADB、Telnet、配置、日志、断言、报告路径、设备管理
├── testdata/
│   ├── android/            # wifi_ssid.yaml、country_code_tables.yaml、weaknet_scene.yaml
│   └── miniap/             # halow_frequency_tables.yaml
├── docs/
│   ├── testcase-docs/      # 用例文本参考库（生成/校对 md，非可执行代码）
│   └── framework-share-summary.md
├── testcases/
│   ├── conftest.py         # 全局 Fixture（ADB、WiFi、miniAP、.env）
│   ├── android/            # Android / HyperWiFi 测试域
│   │   ├── conftest.py     # android_wifi_lifecycle 前置/后置
│   │   ├── common/         # Android 通用 WiFi 场景
│   │   ├── compatibility/  # 兼容性场景
│   │   ├── country_code/   # 国家码映射与遍历
│   │   ├── dual_link_failover/ # 双链路切换与容错
│   │   ├── hyperwifi_low_power/ # HyperWiFi 低功耗
│   │   ├── itr/            # ITR 场景
│   │   ├── mix_usb_mode_switch/ # USB 模式切换
│   │   ├── multi_network_coexistence/ # 多网络共存
│   │   ├── net_selection/  # 网络选择
│   │   ├── performance/    # 时延、吞吐、Ping 等性能用例
│   │   ├── roaming/        # 漫游场景
│   │   ├── stability/      # 稳定性场景
│   │   ├── wifi_low_power/ # 传统 WiFi 低功耗
│   │   ├── wlan_access/    # WLAN 接入、加密、信道与 IP 配置
│   │   ├── wlan_advanced_settings/ # WLAN 高级设置
│   │   ├── wlan_blacklist/ # WLAN 黑名单
│   │   ├── wlan_components_settings/ # Settings 组件场景
│   │   ├── wlan_components_systemui/ # SystemUI 组件场景
│   │   ├── wlan_components_welcome/ # Welcome 组件场景
│   │   └── wlan_hotspot/   # SoftAP / 热点场景
│   ├── miniAP/             # miniAP 驱动测试（标记 miniap）
│   ├── smoke/              # 冒烟
│   ├── support/            # 测试辅助模块
│   └── unit/               # 硬件无关单元测试
├── tools/
│   ├── files-generator/    # 框架文档生成
│   ├── files-transfer/     # Excel → md、WiFi 用例批量生成
│   ├── pytest-automation/  # 用例生成规范（SKILL / reference）
│   └── verify_wifi_ap_live.py # 传统 WiFi AP 实机配置校验
├── reports/                # 运行产物（Git 忽略）
│   └── YYYY-MM-DD/
│       └── HH-MM-SS/
│           ├── html/report.html
│           ├── log/automation.log
│           └── allure/raw/
└── temp/                   # 临时截图等（Git 忽略）
```

## 快速开始

1. 安装依赖：`pip install -r requirements.txt`
2. 在项目根目录创建 `.env`，按需配置：
   - `ANDROID_SERIAL` — 被测 Android 设备
  - `DUT_WIFI_CAPABILITY` — DUT WiFi 能力：`wifi`、`hyperwifi` 或 `dualwifi`（默认 `dualwifi`）
  - `WIFI_PASS_*` — 各 SSID 密码（与 `testdata/android/wifi_ssid.yaml` 对应）
  - `SSIDPWD_MINIAP_AUTOCFG` — ssidpwd 用例是否自动下发 miniAP（1 开启；`run.py` 默认注入为 1）
  - `WIFI_CONNECT_WAIT_SEC` — WiFi 关联等待秒数（建议 30）
  - `SSIDPWD_REQUIRE_GATEWAY` — 网关校验是否严格（1 严格，0 仅告警）
   - `PYAT_AI_API_KEY` — 可选，供标记 `ai` 的用例使用
3. `config/test_config.json` 提供共享实验室默认值。不同实验室在 `.env` 覆盖 `AP_*`、`MINIAP_*`、`DUT_ETH_IP`、`ANDROID_SERIAL` 等字段；环境变量优先，避免修改受版本控制的默认配置。
4. 连接设备并确认 ADB 在线：`adb devices`

## 运行方式

### run.py（推荐）

| 命令 | 说明 |
|------|------|
| `python run.py` | 全量 `testcases` |
| `python run.py --scene smoke` | 冒烟（`-m smoke`） |
| `python run.py --scene hyperwifi` | Android 域 `testcases/android` |
| `python run.py --scene country_code` | 国家码子模块（按目录收集） |
| `python run.py --scene stress` | Android 压力/长时（`-m stress`） |
| `python run.py --scene weaknet` | 弱网场景（`-m weaknet`） |
| `python run.py --scene miniap` | miniAP 域 |
| `python run.py --scene ai` | 调用 AI 模块的用例 |
| `python run.py --allure` | 额外写入 `reports/<日期>/<时间>/allure/raw` |
| `python run.py --list` | 仅收集用例，不执行 |
| `python run.py --scene smoke -q` | pytest 参数原样追加到命令末尾 |

### 直连 pytest

```bash
pytest testcases -m "wifi and not stress"
pytest testcases/android/performance -v
pytest testcases/android/country_code --collect-only -q
```

`pythonpath` 已在 `pytest.ini` 设为项目根；`run.py` 使用 `parse_known_args`，未知参数会传给 pytest。

## 维护规范

- 单文件用例数量建议 ≤100；按功能域继续拆子目录。
- Android 测试数据 YAML 放在 `testdata/android/`；加载与查询见 `core/testdata_loader/android/`（如 `wifi_data.py`、`country_code_data.py`）。
- AP 设备控制统一放在 `core/libs/access_points/`；`wifi_ap.py` 管理传统 WiFi AP，`miniap.py` 管理 HaLow miniAP。
- Android WiFi 控制能力、Settings/SystemUI 页面对象和 pytest 场景编排分别放在 `core/libs/android/wifi_control/`、`settings_pages/`/`systemui_pages/` 和 `wifi_scenarios/`。
- Welcome WLAN 场景按连接配置、网络详情、SSID 显示、列表展开、图标和版本放在 `core/libs/android/wifi_scenarios/welcome/`；页面操作继续复用 `wifi_ui/welcome_page.py`。`testcases/android/wlan_components_welcome/` 只保留用例元数据、原 fixture 声明和场景调用；手工占位及原有设备/AP 前置条件不变。
- WLAN 高级设置场景按频段、省电模式、模式、优先级、漫游灵敏度、漫游阈值和超时断连放在 `core/libs/android/wifi_scenarios/advanced_settings/`；热点场景按默认配置、自动关闭和稳定性放在 `core/libs/android/wifi_scenarios/hotspot/`。测试入口保留原用例 ID、markers 和 fixture 声明，执行逻辑分别复用 `WiFiAdvancedSettingsUI` / `AdvancedSettingsSupportUI` 和 `SoftAPControl`；原等待时间、循环次数、异常处理、生命周期操作及手工占位不变。
- 用例正文与需求说明统一放在 `docs/testcase-docs/`；`testcases/` 只保留可执行 pytest 代码。
- 报告默认写入 `reports/<日期>/<时间>/`；可通过环境变量覆盖：
  - `REPORT_DATE` — 固定日期段
  - `REPORT_TIME` — 固定时间子目录
  - `PYTEST_REPORT_RUN_DIR` — 指定完整运行目录
- 域专属 Fixture 写在对应域的 `conftest.py`（如 `testcases/android/conftest.py`）；全局 Fixture 在 `testcases/conftest.py`。
- Android WiFi 用例默认启用 `android_wifi_lifecycle`（开/关 WiFi、清理已保存网络）；用 `@pytest.mark.no_wifi_lifecycle` 可跳过。

## 标记说明

### 产品 / 域

| 标记 | 含义 |
|------|------|
| wifi | 仅支持传统 WiFi 能力的用例 |
| hyperwifi | 仅支持 HyperWiFi 能力的用例 |
| dualwifi | 必须同时具备传统 WiFi 与 HyperWiFi 双链路能力的用例 |
| country_code | 国家码功能测试 |
| miniap | miniAP 产品域 |
| common | 传统 WiFi 与 HyperWiFi 设备均可独立执行的用例 |

### 类型 / 优先级

| 标记 | 含义 |
|------|------|
| smoke | 冒烟 |
| regression | 回归 |
| stress | 压力 / 长时 |
| weaknet | 弱网仿真 |
| ai | 调用 AI 模块 |
| p0 / p1 / p2 / p3 | 需求优先级 |
| case_id("WIFI-001") | 用例追溯 ID |

### Android 生命周期控制

| 标记 | 含义 |
|------|------|
| no_wifi_lifecycle | 跳过 WiFi 前置/后置清理 |
| no_dual_wifi_setup | 跳过双 WiFi 预连接 |
| dual_wifi_eu / dual_wifi_us | 使用对应区域双 WiFi 列表 |

## 实网 WiFi

配置好 `testdata/android/wifi_ssid.yaml` 与各 `WIFI_PASS_*`（或 yaml 内 `pwd`）后，可执行需连接 AP 的用例；AP 不可达时对应用例会 `skip` 或 `xfail`。

## 仓库

远程地址：`git@code.sunmi.com:iot_test/pytest_iot.git`
