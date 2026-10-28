---
name: pytest-scope-validation
description: "用于改动后验证、测试收集或确定回归范围：在修改 Python、fixtures、测试数据、生成用例、imports 或 scenario runners 后选择最小可靠的 pytest、fresh import 和 collection validation."
---

# Pytest Scope Validation

Choose validation from the behavior and blast radius, not from the number of edited files. Start narrow, then escalate when shared contracts or collection surfaces changed.

## Validation Ladder

1. Run the focused unit module for the changed implementation when one exists.
2. Collect the affected production test package with strict markers enabled by `pytest.ini`.
3. For moved modules, compatibility exports, or import rewrites, import the affected modules in a fresh interpreter before pytest. Pytest's import cache can hide cycles and stale forwarding paths.
4. Run the Android unit suite when changing `core/libs/android/`, Android loaders, shared fixtures, or scenario helpers.
5. Run full Android collection when changing shared APIs, generated tests, markers, fixtures, data IDs, or package layout.

## Commands

```powershell
# Focused behavior
.venv\Scripts\python.exe -m pytest <focused-test-file> -q

# Affected collection
.venv\Scripts\python.exe -m pytest <affected-production-path> --collect-only -q

# Fresh import
.venv\Scripts\python.exe -c "import <affected.module>"

# Shared Android baseline
.venv\Scripts\python.exe -m pytest testcases/unit/android -q
.venv\Scripts\python.exe -m pytest testcases/android --collect-only -q
```

## Decision Rules

- YAML or loader changes: verify structured loading and referenced IDs, then collect consumers.
- Fixture changes: collect every package in the fixture's scope; run focused behavior if hardware-independent tests exist.
- Parser or runner changes: run its unit module, a fresh import, and affected production collection.
- Marker changes: run collection with the repository's `--strict-markers` configuration.
- Generated test changes: check duplicate IDs and collect every generated destination package.

Report commands, pass/fail counts, skips or xfails that matter, and any validation that could not run because hardware or credentials were unavailable.
