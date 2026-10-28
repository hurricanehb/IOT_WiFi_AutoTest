# 性能测试 — 自动化说明

需求原文：`tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md`（本目录 `testcases.md` 为旧版摘要命名，已不再用于生成）。执行脚本为 **静态 pytest 文件**（与 `reference.md` 标准模板一致），**运行 pytest 时不读取 md**。

## 脚本文件

| 文件 | 说明 |
|------|------|
| `test_perf_throughput_maxtpt.py` | 极限吞吐量 TCP/UDP，双向多轮统计 |
| `test_perf_latency_ping.py` | Ping 时延 |
| `test_perf_conn_assoctime.py` | 连接耗时 |
| `test_perf_throughput_pat.py` 等 | PAT/RVR/干扰等，`run_manual_placeholder` |

共享逻辑：`core/libs/android/wifi_scenarios/performance.py`

## 标准用例形态

每条用例均为独立函数，含 `@pytest.mark.p*`、`wifi`/`hyperwifi`、`wlan`、三段 docstring、`# Step N:` 注释；可自动化类在 Step 2 调用 `run_*_case`，手工类 Step 2 为 `pytest.skip("manual: …")`。

## 环境变量

性能参数的版本化默认值配置在 `config/test_config.json` 的 `performance` 节；同名环境变量（`.env` 或终端）优先，用于不同实验室的临时覆盖。优先级与校验统一在 `core/utils/config_loader.py` 解析，runner 只读 `settings.performance`；取值非法时报错会标明来源（环境变量名或 `performance.<key>`）。

| 变量 | `performance` 键 | 含义（默认值） |
|------|------|------|
| `PERF_IPERF_SERVER` | `iperf_server` | iperf3 服务端 IP（空，未配则 skip） |
| `PERF_IPERF_DURATION_SEC` | `iperf_duration_sec` | 跑流时长（10） |
| `PERF_IPERF_RUNS` | `iperf_runs` | 每个协议、每个方向的跑流次数（3） |
| `PERF_IPERF_PARALLEL_STREAMS` | `iperf_parallel_streams` | iperf3 `-P` 并发流数（1） |
| `PERF_TRADITIONAL_IPERF_PARALLEL_STREAMS` | `traditional_iperf_parallel_streams` | 传统 WiFi iperf3 `-P` 并发流数（16，实机饱和探测值） |
| `PERF_IPERF_PROTOCOLS` | `iperf_protocols` | 标题未指明协议时的协议列表（`tcp,udp`） |
| `PERF_UDP_BW` | `udp_bandwidth` | UDP 带宽（`100M`） |
| `PERF_MIN_MBPS` | `min_mbps` | 最低吞吐量 Mbps（1） |
| `PERF_PING_HOST` | `ping_host` | ping 目标（空，未配则 skip） |
| `PERF_PING_COUNT` | `ping_count` | ping 包数（20） |
| `PERF_PING_BIG_SIZE` | `ping_big_size` | 大包字节数（1200） |
| `PERF_PING_SMALL_SIZE` | `ping_small_size` | 小包字节数（64） |

SSID：`testdata/android/wifi_ssid.yaml`

## 运行示例

```bash
python -m pytest testcases/android/performance --collect-only -q

python -m pytest testcases/android/performance/test_perf_conn_assoctime.py::test_Perf_Conn_AssocTime_002 -v

set PERF_IPERF_SERVER=192.168.1.100
python -m pytest testcases/android/performance/test_perf_throughput_maxtpt.py -m p0 -v

set PERF_IPERF_RUNS=3
set PERF_IPERF_PARALLEL_STREAMS=1
set PERF_TRADITIONAL_IPERF_PARALLEL_STREAMS=16
python -m pytest testcases/android/performance/test_perf_throughput_maxtpt.py -k "MaxTpt_001" -v
```

## 文档变更后

对照 `testcases.md` 手动更新 `testcases/android/performance/test_*.py`，保持摘要 ID 与 marker 一致。
