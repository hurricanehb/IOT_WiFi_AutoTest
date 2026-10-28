# 参考：用例模板与检查清单

## 标记（对齐需求文档）

| 类型 | Marker | 示例 |
|------|--------|------|
| 优先级 | `p0` / `p1` / `p2` / `p3`（`-m P0` 等价；需求未标优先级时默认 `p2`） | `@pytest.mark.p0` |
| 产品标签 | `wifi` / `hyperwifi` / `common` | `@pytest.mark.hyperwifi` |

可选保留 `wlan`、`wlan_connection` 等用于目录级筛选；新用例以需求文档 **P*** 与 **标签** 为准。

## 标准用例模板

```python
import pytest


@pytest.mark.p1
@pytest.mark.hyperwifi
def test_Ccode_Default_Func_004(run_shell_cmd, wifi):
    """
    用例摘要：Ccode_Default_Func_004
    初始条件：已联网，欧盟区国家码 EUS，占空比默认关闭
    测试目的：验证德国（DE）下 Halow 国家码和占空比默认状态
    """

    # Step 1: 修改国家码为德国 DE
    if not run_shell_cmd("which cli_app"):
        pytest.skip("缺少 cli_app，无法执行当前用例")

    # Step 2: 修改国家码为德国 DE
    run_shell_cmd("cmd wifi force-country-code enabled DE")

    # Step 3: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    print(f"国家码信息输出：\n{country_info}")

    # Step 4: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")
    print(f"占空比信息输出：\n{duty_info}")

    assert "Country : EU" in country_info, "Halow 国家码错误，应为 EU"
    assert "Duty cycle : off" in duty_info, "占空比状态错误，应为 off"
```

## Fixture

| 名称 | 说明 |
|------|------|
| `run_shell_cmd` | `testcases/conftest.py`：经 `AdbHelper.shell_line` 整行下发（含 `|` 的管道在设备端执行，避免 Windows 误解析） |
| `wifi` | `WiFiControl`，开关 WiFi、连接 SSID |
| `adb` | `AdbHelper`，需细粒度返回码时使用 |

## 需求 → 代码映射

| 需求要素 | pytest 实践 |
|----------|----------------|
| 摘要 ID | 函数名 `test_<摘要ID>` |
| 前置条件 | docstring「初始条件」+ 必要时 `skip` |
| 操作步骤 | `# Step N:` + `run_shell_cmd` |
| 预期结果 | `assert` + 中文失败说明 |
| 手工 | 运行时检查环境后再 `pytest.skip("manual: …")`，不要硬编码无条件 skip |

## 交付策略

- 默认将同模块用例追加到聚合文件 `test_<模块名>.py`
- 仅当单个用例步骤过于庞大繁杂时，才单独拆分为 `test_<摘要ID>.py`
- 大批量同构用例：写成**静态** pytest 文件（与下方标准模板一致），**不要**在 `testcases/` 运行期解析 md
- 可选在同目录补充 `*-automation.md` 映射表

性能模块示例（静态脚本 + 共享 helper）：

| 文件 | 内容 |
|------|------|
| `test_perf_throughput_maxtpt.py` | 极限吞吐量 TCP/UDP，调用 `run_throughput_case` |
| `test_perf_latency_ping.py` | Ping 时延，调用 `run_ping_latency_case` |
| `test_perf_conn_assoctime.py` | 连接耗时，调用 `run_connection_latency_case` |
| `test_perf_throughput_pat.py` 等 | 实验室/手工场景，`run_manual_placeholder` |

共享逻辑：`core/libs/android/wifi_scenarios/performance.py`。

## 收集前检查清单

- [ ] `P0`–`P3`、`WiFi`、`HyperWiFi` 等 marker 已在 `pytest.ini` 注册
- [ ] 函数名与「摘要」一致
- [ ] `pytest --strict-markers` 可收集

## 路径

| 用途 | 路径 |
|------|------|
| 本技能 | `tools/pytest-automation/` |
| 需求文档 | `docs/testcase-docs/` |
| 全局 Fixture | `testcases/conftest.py` |
| Android 域 Fixture | `testcases/android/conftest.py` |
| 国家码示例 | `testcases/android/country_code/test_country_code.py` |
| WLAN 模式示例 | `testcases/android/wifi_connection/test_AdvWlanSet_Mode.py` |
| 性能（静态脚本） | `testcases/android/performance/test_perf_throughput_maxtpt.py` 等 |
| 性能需求原文 | `docs/testcase-docs/android/performance/testcases.md` |
| 性能自动化说明 | `docs/testcase-docs/android/performance/performance-automation.md` |
| WiFi 数据 | `testdata/android/wifi_ssid.yaml` |
| Marker | 项目根 `pytest.ini` |
