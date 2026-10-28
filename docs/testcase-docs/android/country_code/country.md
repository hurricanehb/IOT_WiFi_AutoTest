# 国家码自动化说明

规范原文：`country-code.md`。脚本：**`test_func_ccode_adapt.py`**。

## 用例文档格式（与 pytest 一致）

每条需求在 Markdown 中建议包含：

```markdown
#### 用例标题
**属性：** 优先级：P1；摘要：Ccode_Default_Func_004；类型：自动化；标签：HyperWiFi

**前置条件：**
已联网 …

**操作步骤：**
1、shell 命令 …

**预期结果：**
2、Halow 国家码为 Country : EU
```

对应 pytest 函数命名：`test_<摘要ID>`，例如 `test_Ccode_Default_Func_004`。

## pytest 脚本格式样例

```python
@pytest.mark.P0
@pytest.mark.HyperWiFi
def test_Ccode_Default_Func_005(run_shell_cmd, wifi):
    """
    用例摘要：Ccode_Default_Func_005
    初始条件：已联网，非欧盟区国家码 US，占空比默认关闭
    测试目的：验证美国（US）国家码下 Halow 国家码和占空比默认状态
    """
    # Step 1: 修改国家码为美国 US
    run_shell_cmd("cmd wifi force-country-code enabled US")

    # Step 2: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")

    # Step 3: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")

    assert "Country : US" in country_info, "Halow 国家码错误，应为 US"
    assert "Duty cycle : off" in duty_info, "占空比状态错误，应为 off"
```

- **Fixture**：`run_shell_cmd`（`testcases/conftest.py`）、`wifi`（开关 WiFi）。
- **标记**：`P0`–`P3` 对齐需求优先级；`HyperWiFi` / `Common` / `WiFi` 对齐需求标签。
- **手工用例**：函数体内 `pytest.skip("manual: …")`。

## 摘要 → 脚本

| 摘要 ID | 优先级 | 标签 | 函数 |
|---------|--------|------|------|
| Ccode_Default_Func_001 | P1 | HyperWiFi | `test_Ccode_Default_Func_001` |
| Ccode_Default_Func_002 | P1 | HyperWiFi | `test_Ccode_Default_Func_002` |
| Ccode_Default_Func_003 | P1 | HyperWiFi | `test_Ccode_Default_Func_003` |
| Ccode_Default_Func_004 | P1 | HyperWiFi | `test_Ccode_Default_Func_004` |
| Ccode_Default_Func_005 | P0 | HyperWiFi | `test_Ccode_Default_Func_005` |
| Ccode_Default_Excpt_001 | P1 | HyperWiFi | `test_Ccode_Default_Excpt_001`（manual skip） |
| Ccode_Default_Excpt_002 | P1 | HyperWiFi | `test_Ccode_Default_Excpt_002`（manual skip） |
| Ccode_Adapt_Func_001 | P1 | Common | `test_Ccode_Adapt_Func_001`（示例 AD，含 WiFi 连接校验） |
| Ccode_Adapt_Table_US | P2 | Common / wlan_country | `test_Ccode_Adapt_Table_US[XX]`，遍历 `country_code_tables.yaml` |
| Ccode_Adapt_Table_EU | P2 | Common / wlan_country | `test_Ccode_Adapt_Table_EU[XX]`，遍历 EU 表 |
| Ccode_Default_Func_003～005 | P0/P1 | HyperWiFi | 改国家码并重连后调用 `_assert_wifi_connected` |

## 国家码遍历表

- 数据文件：`testdata/android/country_code_tables.yaml`（`us_country_table` / `eu_country_table`）
- 加载：`core/testdata_loader/android/country_code_data.py` → `us_country_codes()` / `eu_country_codes()`
- 环境变量 `CCODE_LIMIT=N`：仅跑每张表前 N 条（调试/冒烟）

## 运行

```bash
pytest testcases/android/country_code/test_func_ccode_adapt.py::test_Ccode_Default_Func_005 -v
pytest testcases/android/country_code -m hyperwifi
pytest testcases/android/country_code/test_func_ccode_adapt.py::test_Ccode_Adapt_Table_US -v
pytest "testcases/android/country_code/test_func_ccode_adapt.py::test_Ccode_Adapt_Table_EU[Func_Ccode_Adapt_Vali_011-DE]" -v
$env:CCODE_LIMIT=5; pytest testcases/android/country_code/test_func_ccode_adapt.py::test_Ccode_Adapt_Table_US -v
```
