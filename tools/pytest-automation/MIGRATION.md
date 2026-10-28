# WLAN 分层标记迁移说明

目标：在保留原有 `wifi` / `hyperwifi` / `smoke` 等筛选能力的前提下，为每条用例补齐 **`wlan` 业务域**、**子模块**、**优先级 `p*`**、**`case_id`**，并与 docstring **`【用例ID】`** 对齐。

## 原则

| 规则 | 说明 |
|------|------|
| 业务域 | `testcases/android/wifi_connection/**`、`country_code/**` 下用例必须带 **`wlan`**；**不**把 `wlan` 强加到 Web/API 占位等非 WLAN 用例。 |
| 子模块 | 连接类：`wlan_connection`；国家码：`wlan_country`。 |
| 兼容 | 保留原有 `pytestmark` 中的 `wifi` / `hyperwifi` / `stress` / `weaknet` / `ai` / `smoke`，避免现有 `-m wifi` 等命令失效。 |
| 优先级 | 与需求 P0–P3 对齐；无需求条目时用 **p2** 作默认回归，占位/导入类用 **p3**。 |
| case_id | 稳定字符串，建议前缀：`WIFI-`、`CCODE-`、`SMOKE-`、`ADVWLAN-`；参数化多条逻辑可共用一个 `case_id` 或按 `ids=` 区分（见各文件）。 |
| Phase 2（可选） | CI 全量改为 `-m "wlan and regression"` 后，再评估是否移除冗余的单独 `wifi` mark。 |

## 文件与用例清单（迁移后）

| 文件 | wlan 子模块 | 说明 |
|------|-------------|------|
| `android/wifi_connection/test_wifi_connect.py` | — | `test_WiFi_Conn_*`，P*/WiFi + `run_shell_cmd` |
| `android/wifi_connection/test_wifi_switch.py` | — | `test_WiFi_Switch_*` |
| `android/wifi_connection/test_wifi_stress.py` | — | `test_WiFi_Stress_*`，保留 `stress` |
| `android/wifi_connection/test_wifi_weaknet.py` | — | `test_WiFi_Weaknet_*`，保留 `weaknet` |
| `android/wifi_connection/test_AdvWlanSet_Mode.py` | — | `test_AdvWlanSet_Mode_*`，对齐 wifi-connection.md |
| `android/country_code/test_country_code.py` | `wlan_country` | Halow 国家码 |
| `android/performance/test_perf_throughput_maxtpt.py` 等 | — | `test_Perf_*` 静态脚本 |
| `smoke/test_smoke_wifi.py` | `wlan_connection` | 与 WiFi 数据路径相关 |
| `smoke/test_smoke_web.py` | （无 wlan） | Web 占位 |
| `smoke/test_smoke_api.py` | （无 wlan） | API 占位 |

## 筛选示例

```bash
pytest -m "wlan and wlan_connection and regression" testcases/android/wifi_connection
pytest -m "wlan and wlan_country" testcases/android/country_code
pytest -m "smoke and not wlan" testcases/smoke
```

## 校验

```bash
python -m pytest testcases --collect-only -q
```
