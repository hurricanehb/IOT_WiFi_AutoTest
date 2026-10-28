---
name: pytest-iot-case-generation
description: "用于生成用例、补充用例或重构测试：从需求文档、Markdown、手工步骤或检查清单创建 PyAutoTest IoT pytest cases，并处理 markers、fixtures、case IDs、scenario runners 和 collection validation. Use when adding, generating, or refactoring repository pytest cases."
---

# Pytest IoT Case Generation

Generate static pytest cases that follow this repository's conventions. Do not make tests parse requirement Markdown at runtime.

## Workflow

1. Locate the source requirement under `docs/testcase-docs/` or `tools/files-transfer/` and identify its summary ID, priority, product tag, preconditions, steps, and expected results.
2. Read `pytest.ini`, `testcases/conftest.py`, and the nearest domain `conftest.py`. Search existing tests, fixtures, scenario runners, helpers, and test-data profiles before adding anything.
3. Reuse an existing runner or helper when it represents the same behavior. Add a new abstraction only when the scenario is behaviorally distinct.
4. Place the test in the matching `testcases/<domain>/<module>/` package. Prefer a module-oriented test file; split out a case only when its implementation is unusually large.
5. Use `test_<summary_id>` as the function name and add registered markers only:
   - Priority: `p0`, `p1`, `p2`, or `p3`; default to `p2` if unspecified.
    - Product: `wifi` for traditional WiFi only, `hyperwifi` for HyperWiFi only,
       `dualwifi` when both links are required, or `common` when either device type
       can execute the case independently.
   - Domain/type markers where applicable, plus an explicit `@pytest.mark.case_id("<summary_id>")`. Never synthesize `case_id` in a fixture or collection hook because external result mapping reads it before test execution.
6. Declare report/runtime metadata with `@pytest.mark.wifi_case(title="<title>", pre="<precondition>")` and request the `wifi_case` fixture. The collection bridge builds the Allure description; do not duplicate this metadata in a three-part docstring.
7. For unavailable devices, commands, APs, or lab capabilities, perform a runtime check and use a reasoned `skip` or `xfail`. Never add an unconditional skip merely because automation is incomplete.
8. Validate the smallest affected test path with `--collect-only`; run focused unit tests when shared logic changed.

## Zero-Pseudocode Rule（零伪代码）

生成的用例代码必须直接可执行，禁止任何伪代码/假想调用。硬性约束：

1. **只调用能力清单内的 API**：函数体中的每个调用、fixture、testdata profile 必须出现在 [capability-map.md](capability-map.md) 中，或能在工作区 grep 到真实定义。引用前先 grep 验证符号存在与签名一致。
2. **映射不上就显式占位**：某步骤无法映射到现有能力时，用 `run_manual_placeholder(case, run_shell_cmd)` 或带原因的 `pytest.skip("manual: …")`，绝不写假实现、注释掉的代码或 `pass`。
3. **共享逻辑下沉**：可复用的设备交互/断言一律放入 `core/libs/.../wifi_scenarios/`，用例文件保持薄壳并只调用 runner。诊断信息和可复用执行步骤由 runner 统一通过 Allure attachment/step 展示，不在每个用例中重复打印或注释步骤。
4. **禁止发明参数**：runner 签名以 `capability-map.md` 与源码为准；需要新参数/新 profile 时，先按仓根 copilot-instructions 的复用原则确认无法复用再新增，并同步更新能力清单。

### 生成后自检（缺一不可）

- 符号核验：函数体内每个非内建名称都能 grep 到定义。
- Fresh import：新进程 `python -c "import <module>"` 成功（捕获模块级语法/导入错误）。
- 收集：`pytest <path> --collect-only -q` 通过且用例数量符合预期。
- 存量占位比例未恶化：新增文件中 `run_manual_placeholder` 占比不得高于同模块既有水平（除非整模块都是实验室/手工场景）。

## Validation

```powershell
.venv\Scripts\python.exe -m pytest <affected-test-path> --collect-only -q
.venv\Scripts\python.exe -m pytest testcases/unit/android -q
```

Run the second command only when shared Android behavior is touched. Escalate broader validation through the `pytest-scope-validation` skill.

## Project Resources

- **能力清单（生成前必读）**: [capability-map.md](capability-map.md) — 可调用的 runner / fixture / profile 全表
- Detailed templates and checklist: [reference.md](reference.md)
- Marker registry: `pytest.ini`
- Shared test facade: `testcases/support/`
- Android scenarios: `core/libs/android/wifi_scenarios/`
- Test data: `testdata/android/` and `testdata/miniap/`
- 自动化率度量: `tools/automation_coverage.py`（统计已实现 vs placeholder）
