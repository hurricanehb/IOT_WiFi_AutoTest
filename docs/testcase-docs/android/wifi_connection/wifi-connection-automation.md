# WiFi 连接 / WLAN 模式 — 自动化说明

需求原文：`wifi-connection.md`。脚本：**`test_AdvWlanSet_Mode.py`**。

## pytest 脚本格式样例

```python
@pytest.mark.P0
@pytest.mark.WiFi
def test_AdvWlanSet_Mode_Func_001(wifi, wifi_yaml):
    """
    用例摘要：AdvWlanSet_Mode_Func_001
    初始条件：实验室已配置 AP 与 DUT WLAN 模式
    测试目的：WLAN 模式默认值有效性
    """
    # Step 1: 连接 AP（实验室环境）
    ...
```

- **函数名**：`test_<摘要ID>`，与需求「摘要」字段一致。
- **Docstring**：`用例摘要` / `初始条件` / `测试目的` 三段。
- **步骤**：`# Step N:` + `run_shell_cmd("…")`（定义于 `testcases/conftest.py`）。
- **标记**：`P0`–`P3` 对齐优先级；`WiFi` / `HyperWiFi` / `Common` 对齐需求标签。

## 环境变量

| 变量 | 含义 |
|------|------|
| `WIFI_WLAN_MODE_LAB=1` | Func_001～012、Stb_005 等需 AP + UI 已配置时执行 |

## 摘要 → 脚本（节选）

| 摘要 ID | 优先级 | 标签 | 说明 |
|---------|--------|------|------|
| AdvWlanSet_Mode_Func_001 | P0 | WiFi | 实验室 + 连接/ping/链路 |
| AdvWlanSet_Mode_Func_013 | P2 | WiFi | DUT：`cmd wifi status` 关→开 |
| AdvWlanSet_Mode_Stb_002 | P1 | WiFi | WiFi 开关后 status |
| AdvWlanSet_Mode_Stb_004 | P2 | WiFi | 飞行模式 roundtrip |
| AdvWlanSet_Mode_Int_* / UI_* | P1–P3 | WiFi | `pytest.skip(manual: …)` |

## 运行

```bash
pytest testcases/android/wifi_connection/test_AdvWlanSet_Mode.py::test_AdvWlanSet_Mode_Func_013 -v
pytest testcases/android/wifi_connection -m WiFi
```
