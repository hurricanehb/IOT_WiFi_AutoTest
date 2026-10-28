---
name: android-wifi-diagnostics
description: "用于失败排查、实机诊断或日志分析：定位 PyAutoTest Android WiFi 用例中的 ADB 连接、设备状态、WiFi 关联、AP 可达性、国家码、双链路、实验室前置条件和设备日志问题。"
---

# Android WiFi Diagnostics

Separate environment failures from product defects and test-code defects. Begin with non-mutating observations and do not change AP or device configuration until the current state has been captured.

## Diagnostic Flow

1. Reproduce the smallest failing case and record its node ID, marker selection, serial, report directory, and relevant environment profile without exposing credentials.
2. Confirm the selected ADB device is online and unambiguous. Check `ANDROID_SERIAL` and `config/test_config.json` resolution when multiple devices are attached.
3. Capture WiFi state, saved networks, current SSID/BSSID, IP address, gateway, country code, and relevant `dumpsys wifi` or logcat output.
4. Check the case's lab requirements and test-data profile. Distinguish missing AP, wrong credentials, unsupported device capability, and lifecycle setup failure.
5. For AP-backed cases, verify reachability and current AP configuration before applying changes. `tools/verify_wifi_ap_live.py` performs real AP operations unless `--verify-only` is used.
6. Inspect the run's `automation.log`, HTML report, and exported device logs. Correlate timestamps around the failing step.
7. Classify the failure as environment, device/product, automation logic, parser/assertion, or test-data/configuration.
8. Make the smallest corrective change and rerun the focused case. Restore mutable lab state when the workflow changed it.

## Useful Resources

- ADB wrapper: `core/utils/adb_helper.py`
- Device selection: `core/utils/device_mgr.py`
- Device log export: `core/utils/device_log_export.py`
- WiFi control and state: `core/libs/android/wifi_control/`
- Lab requirements: `core/libs/android/wifi_scenarios/lab_requirements.py`
- AP verification: `tools/verify_wifi_ap_live.py`
- Runtime reports: `reports/<date>/<time>/`

## Guardrails

- Never print passwords, API keys, tokens, or complete secret-bearing configuration.
- Prefer read-only commands first. State clearly before invoking commands that alter AP, country-code, radio, or saved-network state.
- Do not convert a reproducible product failure into `skip` or `xfail` without an explicit requirement.
- Hardware-unavailable validation must be reported as not run, not passed.
