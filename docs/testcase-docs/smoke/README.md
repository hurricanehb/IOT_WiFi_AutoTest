# Smoke 测试用例参考文档

这里存放冒烟场景的文本参考资料，用于生成或校对 `testcases/smoke/**` 下的 pytest 用例 md。

## 覆盖范围

- `test_smoke_wifi.py`：工程与核心模块导入、基础 WLAN 相关冒烟
- `test_smoke_web.py`：Web 占位冒烟
- `test_smoke_api.py`：API 占位冒烟
- `test_utf8_report.py`：报告中文编码检查

## 文档约定

- 冒烟用例优先保持轻量、可快速收集、可快速执行
- 暂未接入的 Web / API 场景先以占位文档和 `skip` 说明保留
- 需要与 pytest 代码一一对应时，优先使用稳定的 `case_id` 和函数名

## 用例清单

| 用例 ID | 优先级 | 标签 | 自动化/手工 | 对应脚本 | 说明 |
|---|---|---|---|---|---|
| SMOKE-WIFI-IMPORT-001 | P3 | smoke / wlan / wlan_connection | 自动化 | `test_smoke_wifi.py::test_core_imports` | 核心路径与配置可加载 |
| SMOKE-WEB-PLACEHOLDER-001 | P3 | smoke | 自动化 | `test_smoke_web.py::test_web_home_placeholder` | Web 占位，等待驱动接入 |
| SMOKE-API-PLACEHOLDER-001 | P3 | smoke | 自动化 | `test_smoke_api.py::test_api_health_placeholder` | API 占位，等待基址与鉴权 |
| SMOKE-UTF8-REPORT-001 | P3 | smoke | 自动化 | `test_utf8_report.py::test_utf8_in_html_report` | HTML 报告中文字符校验 |

## 单条用例模板

### <CaseId>

**属性：** 优先级：P3；摘要：<CaseId>；类型：自动化；标签：smoke

**前置条件：**
- <前置条件>

**操作步骤：**
1. <步骤 1>
2. <步骤 2>

**预期结果：**
1. <预期 1>
2. <预期 2>
