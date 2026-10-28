---
name: pytest-automation
description: Generates and extends pytest automation under testcases/ from requirement docs, manual steps, or checklists. Use when adding or refactoring tests in testcases/, porting ADB/WiFi/AI flows to pytest, or applying layered markers (domain, submodule, type, priority, case_id) per project conventions.
disable-model-invocation: true
---

# PyAutoTest_IoT — 通用脚本生成

## Instructions

1. **定域**：确认目标目录（如 `testcases/android/<module>/`、`testcases/miniAP/`、`testcases/smoke/`），只改该域及必要的共享封装，避免顺带大重构。需求原文在 `docs/testcase-docs/<域>/<module>/`（如 `docs/testcase-docs/android/performance/testcases.md`）。
2. **读链**：读 `testcases/conftest.py`；若目标包下有 `conftest.py`（如 `testcases/android/conftest.py`）一并读。读 `pytest.ini` 的 `markers` 与 `addopts`。业务数据见 `testdata/android/`（如 `wifi_ssid.yaml`）；共享库见 `core/`。
3. **命名与标记**（均在 `pytest.ini` 注册）：
   - **函数名**：`test_<摘要ID>`，与需求「摘要」一致，如 `test_Ccode_Default_Func_004`。
   - **优先级**：`@pytest.mark.p0` … `p3`（与需求 P0–P3 对齐；若需求文档中未标明优先级，请默认使用 `@pytest.mark.p2`；`-m` 大小写不敏感）。
   - **产品标签**：`@pytest.mark.wifi` / `hyperwifi` / `common`。
4. **Docstring**（三段）：
   - `用例摘要：` + 摘要 ID
   - `初始条件：` + 前置说明
   - `测试目的：` + 一句话
5. **步骤**：`# Step N:` 注释 + `run_shell_cmd("cmd wifi …")` 或 `cli_app … | grep`（fixture 见 `conftest.py`）。
6. **断言**：中文失败说明；关键输出可用 `print` 便于报告排查。
7. **Fixture**：`run_shell_cmd`、`wifi`、`adb`、`wifi_yaml` 等（`testcases/conftest.py`）。
8. **不稳定能力**：在测试代码中增加动态的环境检查逻辑（例如：`if not device_ready: pytest.skip("缺设备")`），当缺设备、缺 `cli_app`、缺 AP 时动态触发 `skip` / `xfail`；请勿硬编码无条件 skip；实验室场景可用 `WIFI_WLAN_MODE_LAB=1`。
9. **交付物**：优先将同模块用例追加到按模块聚合的 `test_<模块名>.py` 文件中；如果单个用例步骤过于庞大繁杂，则单独生成 `test_<摘要ID>.py`。大批量同构用例写成**静态** pytest 脚本（运行期不读 md，见 `testcases/android/performance/`）；可选在 `docs/testcase-docs/<域>/<module>/` 下补充 `*-automation.md` 映射表。
10. **校验**：`python -m pytest <路径> --collect-only`；**禁止**使用未在 `pytest.ini` 声明的 marker。

## 工程路径

| 用途 | 路径 |
|------|------|
| 本技能 | `tools/pytest-automation/`（`SKILL.md`、`reference.md`、`MIGRATION.md`） |
| 需求 / 用例 md | `docs/testcase-docs/`（如 `android/performance/testcases.md`） |
| 自动化说明 | `docs/testcase-docs/<域>/<module>/*-automation.md` |
| pytest 用例 | `testcases/`（如 `testcases/android/performance/`） |
| 全局 Fixture | `testcases/conftest.py` |
| Android 域 Fixture | `testcases/android/conftest.py` |
| 业务数据 | `testdata/android/`（如 `wifi_ssid.yaml`） |
| 共享库 | `core/libs/android/`、`core/utils/` |
| Marker 注册 | 项目根 `pytest.ini` |

## Examples

- **分层标记 + 参数化**：见 [reference.md](reference.md) 完整模板。
- **半自动步骤**：无法 ADB 完成的 UI 流在文档中标注「手工」，代码里 `pytest.skip("manual: …")` 并写明原因。
- **大批量静态用例**：`testcases/android/performance/test_*.py`（与 `reference.md` 模板一致，运行期不依赖 md）

## Additional resources

- 模板与检查清单：[reference.md](reference.md)
- 分层标记迁移与文件清单：[MIGRATION.md](MIGRATION.md)

## 位置说明

本技能位于 `tools/pytest-automation/`。若团队习惯在 Cursor 的 `.cursor/skills/` 下集中管理技能，可复制同名目录到 `.cursor/skills/pytest-automation/` 并尽量保持内容一致。
