# PyAutoTest 自动化脚本执行指导

本文适用于当前 PyAutoTest 工程，覆盖 Windows PowerShell 下的环境准备、用例选择、实机执行、报告查看与常见问题排查。

## 1. 执行入口与基本原则

项目使用 pytest 执行测试，建议在仓库根目录通过项目虚拟环境运行：

```powershell
Set-Location D:\01_Autotest\PyAutoTest
& .venv\Scripts\python.exe run.py <参数>
```

- 日常实机执行优先使用 `run.py`，它会选择场景、创建报告目录并透传额外 pytest 参数。
- 调试单个文件或单条用例时，可直接使用 `python -m pytest`。
- 首次执行或调整筛选条件后，先使用 `--list` 或 `--collect-only` 检查收集结果，再连接硬件执行。
- 同一 DUT 上的硬件用例不要使用 `pytest-xdist` 并行执行，以免设备状态、WiFi 生命周期或 AP 配置互相干扰。

## 2. 环境准备

### 2.1 Python 依赖

工程约定使用 `.venv`。若虚拟环境尚未创建：

```powershell
py -m venv .venv
& .venv\Scripts\python.exe -m pip install -r requirements.txt
```

已有虚拟环境时，确认 pytest 可用：

```powershell
& .venv\Scripts\python.exe -m pytest --version
```

主要依赖包括 pytest、pytest-html、allure-pytest、uiautomator2、PyYAML 和 python-dotenv。

### 2.2 ADB 与 DUT

1. 安装 Android platform-tools，并确保 `adb` 已加入 `PATH`。
2. 通过 USB 或网络连接 DUT，开启 USB 调试。
3. 检查设备状态：

```powershell
adb devices
adb -s <ANDROID_SERIAL> get-state
adb -s <ANDROID_SERIAL> shell getprop ro.build.type
```

设备必须处于 `device` 状态。默认 fixture 要求 `adb root` 可用；若设备不是 userdebug/eng 版本，仅在用例确实不需要 root 时设置 `ADB_REQUIRE_ROOT=0`。

### 2.3 创建本地配置

从模板创建本地 `.env`，不要提交凭据：

```powershell
Copy-Item .env.example .env
```

至少按本次测试范围确认以下字段：

```dotenv
ANDROID_SERIAL=<adb devices 中的串号>
DUT_WIFI_CAPABILITY=dualwifi
ADB_TIMEOUT_SEC=30

# 传统 AP 用例
AP_IP=<AP 管理地址>
AP_LOGIN_PASSWORD=<AP 密码>

# HyperWiFi / miniAP 用例
MINIAP_IP=<miniAP 地址>
MINIAP_LOGIN_PASSWORD=<miniAP 密码>

# 按用例所引用的测试数据补充
WIFI_CONNECT_WAIT_SEC=30
```

`DUT_WIFI_CAPABILITY` 可选值：

| 值 | 适用设备 |
|---|---|
| `wifi` | 仅传统 WiFi |
| `hyperwifi` | 仅 HyperWiFi |
| `dualwifi` | 同时支持传统 WiFi 与 HyperWiFi，默认值 |

能力值会在收集阶段决定部分用例是否跳过。`common` 用例可在单 WiFi 或单 HyperWiFi 设备上执行，`dualwifi` 用例只允许双链路设备执行。

配置优先级为：系统环境变量 > `.env` > `config/test_config.json` > 代码默认值。SSID、密码和国家码等测试数据位于 `testdata/`；凭据只应放在 `.env` 或系统环境变量中。

### 2.4 实验室前置检查

执行硬件用例前确认：

- `ANDROID_SERIAL` 指向唯一且在线的 DUT。
- DUT 屏幕可解锁，Settings UI 用例执行期间不要人工操作设备。
- 测试主机可访问 AP、miniAP、衰减器或 iperf 服务端。
- `.env` 中的能力类型与 DUT 实际能力一致。
- `testdata/android/wifi_ssid.yaml` 中被用例引用的网络与实验室实际配置一致。
- 国家码、弱网、漫游、性能等场景所需专用设备均已就绪。

传统 AP 可先做只读校验：

```powershell
& .venv\Scripts\python.exe tools\verify_wifi_ap_live.py --verify-only
```

不要在未知共享环境中省略 `--verify-only`；该工具的其他模式可能修改 AP 配置。

## 3. 用例收集与筛选

### 3.1 先检查收集结果

全量仅收集：

```powershell
& .venv\Scripts\python.exe run.py --list
```

指定场景仅收集：

```powershell
& .venv\Scripts\python.exe run.py --scene country_code --list -q
```

直接收集目录或文件：

```powershell
& .venv\Scripts\python.exe -m pytest testcases\android\country_code --collect-only -q
& .venv\Scripts\python.exe -m pytest testcases\android\country_code\test_func_ccode_cloudcfg.py --collect-only -q
```

收集成功只能证明导入、marker 和参数化有效，不代表硬件前置已经满足。

### 3.2 `run.py` 场景

| 命令 | 收集范围 |
|---|---|
| `run.py` 或 `run.py --scene all` | 全部 `testcases` |
| `run.py --scene smoke` | `testcases/smoke` 且带 `smoke` marker |
| `run.py --scene hyperwifi` | 全部 Android 用例，不等同于只选 `hyperwifi` marker |
| `run.py --scene country_code` | `testcases/android/country_code` |
| `run.py --scene stress` | Android 下带 `stress` marker 的用例 |
| `run.py --scene weaknet` | Android 下带 `weaknet` marker 的用例 |
| `run.py --scene miniap` | `testcases/miniAP` |
| `run.py --scene ai` | 全工程带 `ai` marker 的用例 |

`run.py` 无法识别的参数会原样传给 pytest，因此可以组合 `-k`、`-m`、`-q`、`-x`、`--maxfail` 等参数。

### 3.3 常用筛选方式

按 marker：

```powershell
& .venv\Scripts\python.exe run.py --scene hyperwifi -m "p0 and hyperwifi and not stress"
& .venv\Scripts\python.exe -m pytest testcases\android -m "wifi and regression"
```

按名称关键字：

```powershell
& .venv\Scripts\python.exe run.py --scene country_code -k "CloudCfg and Vali_009"
```

按文件：

```powershell
& .venv\Scripts\python.exe -m pytest testcases\android\country_code\test_func_ccode_cloudcfg.py -v
```

按 node ID 精确执行单条用例：

```powershell
& .venv\Scripts\python.exe -m pytest "testcases\android\country_code\test_func_ccode_cloudcfg.py::test_Func_Ccode_CloudCfg_Vali_009" -v
```

失败即停或限制失败数：

```powershell
& .venv\Scripts\python.exe run.py --scene country_code -x
& .venv\Scripts\python.exe run.py --scene hyperwifi --maxfail=3
```

## 4. 推荐执行流程

### 4.1 冒烟检查

```powershell
& .venv\Scripts\python.exe run.py --scene smoke --list -q
& .venv\Scripts\python.exe run.py --scene smoke
```

### 4.2 单模块回归

```powershell
& .venv\Scripts\python.exe -m pytest testcases\android\wlan_access --collect-only -q
& .venv\Scripts\python.exe -m pytest testcases\android\wlan_access -m "p0 or p1" -v
```

### 4.3 单条失败用例复测

先复制报告中的完整 node ID，再单独执行：

```powershell
& .venv\Scripts\python.exe -m pytest "<node-id>" -vv --tb=long
```

需要实时查看框架日志时增加：

```powershell
& .venv\Scripts\python.exe -m pytest "<node-id>" -vv -o log_cli=true --log-cli-level=INFO
```

### 4.4 全量或长时执行

仅在单模块验证通过且实验室资源不会冲突时执行：

```powershell
& .venv\Scripts\python.exe run.py
& .venv\Scripts\python.exe run.py --scene stress
```

压力循环次数可通过 `.env` 调整，例如 `WIFI_STRESS_CYCLES` 和 `CCODE_STRESS_CYCLES`。修改循环数会改变执行时长，执行记录中应注明实际值。

### 4.5 含重启用例的串行批量执行

在启动命令中显式加载独立的设备就绪插件，无需修改现有用例或功能代码：

```powershell
$env:ANDROID_SERIAL = '<设备串号>'
& .venv\Scripts\python.exe -m pytest -p testcases.support.android_ready_guard testcases\android\wlan_advanced_settings -vv -s -o log_cli=true --log-cli-level=INFO
```

- VS Code 的 `WLAN Advanced Settings - All Cases` 任务已加载该插件。
- 插件仅作用于 `testcases/android` 下使用设备 fixture 的用例；单文件和整目录均适用，仅收集时不访问设备。
- 每条用例前置之前、后置清理之前，只读检查系统启动完成、有效 boot ID、Activity/Package/Window 服务和 WiFi 状态命令可用。
- 首次就绪及每次后置要求同一 boot ID 的服务连续稳定至少 2 秒；下一条前置仍会重新探测，不直接信任上次状态。
- 重启期间暂时找不到设备、设备离线、探测超时或服务尚未就绪时持续等待，并每 10 秒输出等待状态。
- 每道检查默认最多等待 180 秒，可用 `--android-ready-timeout=240` 调整；恢复超时以非零退出码终止本次测试，避免后续用例连续设备错误。后置检查超时后仍让 pytest 完成正常收尾，可能发生的清理错误记录到当前用例，但不再执行下一条。
- 当前用例已有的失败保持原样，插件不重跑、不改判、不修改 WiFi 配置，也不替代用例内部的重启等待。它不拦截重启命令，稳定检查不等于证明任意延迟重启已经发生。
- 不支持 `pytest-xdist -n` 并发设备测试，也不能隔离另一个进程或人工操作同一设备；同一 DUT 仍只能由一个测试任务占用。

## 5. 生命周期与执行影响

`testcases/android` 下使用 `adb`、`wifi` 或 `run_shell_cmd` 且属于 WiFi 域的用例，默认启用 `android_wifi_lifecycle`：

- 前置确保 WiFi 已开启。
- 后置断开连接、清除已保存网络，并恢复用例开始前的 WiFi 开关状态。
- 后置最终返回 Android Home 页面。
- 标记 `no_wifi_lifecycle` 的用例跳过该处理。

因此，多条用例连续执行时不要依赖上一条用例留下的已保存网络或页面状态。测试期间中止进程可能来不及执行 teardown，应在重跑前检查 DUT 和 AP 状态。

AP fixture 在会话结束时可能下线自动化 VAP；同一 AP 被多人或多个任务共享时，应协调执行窗口。

### 5.1 Welcome 手持与大屏设备

- 执行 `wlan_components_welcome` 中的 UI 用例前，手动进入 Welcome 的“设置网络 / WLAN”页；fixture 保留当前页面，不自动恢复出厂或跳过激活步骤。
- WLAN 查找、HyperWiFi 标识查找及列表翻页根据控件 hierarchy 中的实际列表边界滑动，兼容手持全屏和大屏内嵌列表，不依赖横屏 ROM 可能错误返回的竖屏窗口尺寸。
- `Func_Components_Welcome_Button_UI_001` 优先点击“展开全部”并验证新增 SSID，保留手持设备原断言。仅在识别到大屏内嵌布局且遍历至列表末尾仍无该按钮时，改为验证实际滚动后出现首屏以外的 SSID；日志区分两种模式。未发现更多 SSID、未确认列表末尾或手持布局缺少按钮仍然失败。
- 连接配置、静态 IP 和网络详情继续使用原控件 ID、标签和实际控件边界，不按设备型号维护坐标表。AP、miniAP 与网络状态前置仍须独立满足，不能因屏幕适配而忽略。
- 静态 IP 字段按实际配置框边界有界双向查找，并在每页检查所有标签别名（如 `DNS2` / `DNS 2`）。输入完成后只在输入法状态确认软键盘已显示时按 Back；大屏无软键盘时保留配置框，输入法状态不可查询时明确失败。
- 配置框是否打开以配置滚动区和取消按钮判断，不以密码框是否在当前视口中判断，避免展开静态 IP 后密码框滚出可见区域时误判弹窗已关闭。
- 输入法关闭会等待状态实际变为隐藏，期间只发送一次 Back；IP 选项与取消按钮点击前等待控件边界稳定，避免键盘和弹窗动画造成坐标偏移。指定网络入口复用 SSID 等待逻辑，允许扫描列表短暂刷新，但最终不可见仍然失败。

## 6. 报告与结果判读

每次运行默认生成独立目录：

```text
reports/<YYYY-MM-DD>/<HH-MM-SS>/
├── html/report.html
├── log/automation.log
├── pytest.log
├── allure/raw/
└── perf/                  # 仅性能场景按需生成
```

直接 pytest 和 `run.py` 都会初始化报告目录；`run.py` 会在控制台打印本次目录。常用产物：

- `html/report.html`：测试结果、失败堆栈和用例描述。
- `log/automation.log`：框架与场景日志。
- `pytest.log`：pytest 日志插件输出。
- `failure_artifacts/`：Android 用例失败时按失败类型去重保存 WiFi 状态、
	`dumpsys wifi`、截断 logcat，以及可用的 UI XML/截图；默认最多 10 类。
- `log/device_packlogs/`：首次非前置条件失败自动导出的 DUT 完整日志。

可通过 `FAILURE_DIAGNOSTICS=0` 关闭轻量失败取证，
`FAILURE_DIAGNOSTICS_MAX_TYPES=<数量>` 调整单次运行的失败类型上限，
或通过 `FAILURE_PACKLOGS=0` 关闭完整设备日志自动导出。
- `allure/raw/`：Allure 原始结果。使用 `run.py --allure` 可显式启用。

需要固定目录供外部任务收集时，可设置 `PYTEST_REPORT_RUN_DIR`；也可分别设置 `REPORT_DATE` 和 `REPORT_TIME`。同一固定目录不要并发写入。

pytest 结果含义：

| 状态 | 含义与处理 |
|---|---|
| `PASSED` | 用例断言通过 |
| `FAILED` | 产品行为、环境、数据或脚本断言失败，需结合日志定位 |
| `ERROR` | 多发生在 fixture、导入或 teardown 阶段 |
| `SKIPPED` | 前置不满足、能力不匹配或手工占位用例；不等同于通过 |
| `XFAILED` | 已声明的预期失败；需要核对原因是否仍有效 |
| `XPASSED` | 预期失败却通过，应检查产品状态和 xfail 条件 |

调用 `run_manual_placeholder(...)` 的脚本属于尚未自动化的手工占位用例，执行结果会是 `SKIPPED`，不能计入自动化通过数。

## 7. 常见问题排查

### 7.1 用例全部或大量跳过

依次检查：

1. HTML 或控制台中的 skip reason。
2. `DUT_WIFI_CAPABILITY` 是否匹配用例的 `wifi`、`hyperwifi`、`dualwifi` marker。
3. `ANDROID_SERIAL` 是否有效，设备是否在线。
4. 默认 root 校验是否通过。
5. AP、miniAP、衰减器或专用实验室开关是否缺失。
6. 用例是否调用了 `run_manual_placeholder(...)`。

### 7.2 ADB 设备异常

```powershell
adb devices
adb -s <ANDROID_SERIAL> wait-for-device
adb -s <ANDROID_SERIAL> shell cmd wifi status
```

- `unauthorized`：在 DUT 上重新确认 USB 调试授权。
- `offline`：重插 USB、检查网络 ADB 链路，必要时再执行 `adb kill-server` 与 `adb start-server`。
- 多设备：必须在 `.env` 明确设置 `ANDROID_SERIAL`。
- root 失败：确认 DUT 是 userdebug/eng；不要为绕过真实前置而随意关闭 root 校验。

### 7.3 WiFi 连接或扫描失败

先记录现场，不要立即修改 AP：

```powershell
adb -s <ANDROID_SERIAL> shell cmd wifi status
adb -s <ANDROID_SERIAL> shell cmd wifi list-networks
adb -s <ANDROID_SERIAL> shell dumpsys wifi
```

随后核对 SSID 是否广播、密码变量、频段/信道、国家码、DUT 能力和 `wifi_ssid.yaml` profile。若失败发生在多用例之后，还需检查上一轮是否被强制终止，导致设备或 AP 清理未完成。

### 7.4 AP 或 miniAP 不可用

- 先确认测试主机到管理地址的网络可达性。
- 核对 IP、账号和密码来自正确实验室 profile，排查时不要打印密码。
- 传统 AP 使用 `tools\verify_wifi_ap_live.py --verify-only` 获取只读结果。
- 修改 AP、国家码、射频或保存网络前先保留当前状态，结束后恢复共享环境。

### 7.5 UI 用例不稳定

- 保持屏幕点亮、设备解锁，关闭会遮挡 Settings 的弹窗。
- 确认 uiautomator2 能连接目标串号。
- 执行期间不要人工点击设备。
- 先用单 node ID 重跑，并查看 HTML、`automation.log`、截图或 UI hierarchy 产物。

### 7.6 收集失败

```powershell
& .venv\Scripts\python.exe -m pytest <受影响路径> --collect-only -q
```

重点检查导入路径、语法错误、重复参数 ID、未知 marker 和测试数据加载异常。项目启用了 `--strict-markers`，未在 `pytest.ini` 注册的 marker 会使收集失败。

## 8. 改动后的最小验证

修改脚本或公共能力后，按影响范围逐级验证：

```powershell
# 1. 硬件无关的聚焦单元测试
& .venv\Scripts\python.exe -m pytest <focused-unit-test> -q

# 2. 受影响模块收集
& .venv\Scripts\python.exe -m pytest <affected-test-path> --collect-only -q

# 3. Android 公共逻辑变更
& .venv\Scripts\python.exe -m pytest testcases\unit\android -q
& .venv\Scripts\python.exe -m pytest testcases\android --collect-only -q

# 4. 最小实机用例
& .venv\Scripts\python.exe -m pytest "<node-id>" -vv
```

只有实际连接了所需硬件并执行完成的检查才能记为实机通过；仅收集成功或因硬件缺失跳过不能替代实机结果。

## 9. 执行记录建议

每轮执行至少记录：

- Git 分支和提交号。
- 完整命令、node ID 或 marker 表达式。
- DUT 型号、版本、`ANDROID_SERIAL` 和 `DUT_WIFI_CAPABILITY`。
- AP/miniAP profile、频段、信道及必要实验室拓扑，不记录明文凭据。
- 报告目录。
- passed、failed、error、skipped、xfailed、xpassed 数量。
- 首个失败步骤、关键日志时间点和失败分类。

推荐先复现最小失败用例，再把问题归类为实验室环境、DUT/产品、自动化逻辑、解析/断言或测试数据，完成修复后执行相同 node ID 回归。

## 10. 每周自动化统计

每周一统计上一个完整自然周（周一至周日）的各模块自动化分布和新增数量：

```powershell
& .venv\Scripts\python.exe tools\automation_coverage.py --weekly
```

补算指定自然周时，传入该周的周日日期：

```powershell
& .venv\Scripts\python.exe tools\automation_coverage.py --weekly --week-ending 2026-09-20
```

统计按 pytest 实际收集出的唯一 `case_id` 去重。输出包含每个模块的用例总数、已实现数、自动化率、本周新增自动化数和自动化率提升；提升值为周末相对周初增加的百分点（pp）。Git 快照统计不包含未提交改动。