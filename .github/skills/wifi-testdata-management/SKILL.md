---
name: wifi-testdata-management
description: "用于新增、修改、复用、合并或排查测试数据：管理 PyAutoTest WiFi、国家码、弱网、双 WiFi、SSID/password、miniAP、频点和信道计划 YAML 及其 Python loaders."
---

# WiFi Test-Data Management

Treat test data, loaders, fixtures, and test references as one contract. Reuse existing entries by test intent before creating a new ID or profile.

## Workflow

1. Identify the behavior the test needs, including which values are essential and which are incidental.
2. Search `testdata/`, `core/testdata_loader/`, fixtures, scenario runners, and tests for an existing entry that expresses that behavior.
3. Prefer an existing profile and align nonessential values such as passwords. Express scenario differences through existing arguments or case metadata when possible.
4. Add a new entry only when existing data cannot represent a behaviorally distinct requirement. Give the ID a name that communicates that distinction.
5. Use loader APIs rather than parsing YAML directly in tests. Keep loader normalization and fallback behavior explicit.
6. When consolidating entries, update every reference and remove obsolete data only after confirming no consumers remain.
7. Validate loading, uniqueness, reference resolution, and collection of affected tests.

## Owned Data

- `testdata/android/wifi_ssid.yaml`
- `testdata/android/country_code_tables.yaml`
- `testdata/android/weaknet_scene.yaml`
- `testdata/miniap/`
- `core/testdata_loader/android/`
- `core/testdata_loader/miniap/`

## Validation

Use the repository loader in a fresh interpreter, then run focused loader or scenario tests and collect affected production tests:

```powershell
.venv\Scripts\python.exe -c "from core.testdata_loader.android.wifi_data import load_wifi_ssid; data = load_wifi_ssid(); assert isinstance(data, dict); print(sorted(data))"
.venv\Scripts\python.exe -m pytest testcases/unit/android -q
.venv\Scripts\python.exe -m pytest <affected-test-path> --collect-only -q
```

Before finishing, search for removed IDs and verify they have no remaining references.
