from types import SimpleNamespace
from unittest.mock import Mock

from core.utils import failure_diagnostics


def test_capture_failure_diagnostics_keeps_summary_when_device_commands_fail(
    tmp_path, monkeypatch
) -> None:
    monkeypatch.setattr(failure_diagnostics, "report_run_dir", lambda: tmp_path)
    adb = Mock()
    adb.shell_line.side_effect = RuntimeError("device offline")
    settings_ui = SimpleNamespace(
        artifact_dir=tmp_path / "missing-ui",
        device=SimpleNamespace(
            dump_hierarchy=Mock(side_effect=RuntimeError("uiautomator unavailable")),
            screenshot=Mock(),
        ),
    )

    artifacts = failure_diagnostics.capture_failure_diagnostics(
        adb,
        label="CASE/001",
        phase="call",
        reason="assertion failed",
        settings_ui=settings_ui,
    )

    names = {path.name for path in artifacts}
    assert "failure.txt" in names
    assert "wifi_status.txt" in names
    assert "dumpsys_wifi.txt" in names
    assert "logcat_tail.txt" in names
    assert "ui_capture_error.txt" in names
    assert "assertion failed" in next(
        path for path in artifacts if path.name == "failure.txt"
    ).read_text(encoding="utf-8")


def test_failure_signature_groups_case_numbers_and_temp_paths() -> None:
    first = failure_diagnostics.failure_signature(
        "setup",
        r"CASE_001 前置条件失败；UI hierarchy=C:\Temp\pytest-1\failure.xml",
    )
    second = failure_diagnostics.failure_signature(
        "setup",
        r"CASE_002 前置条件失败；UI hierarchy=C:\Temp\pytest-2\failure.xml",
    )

    assert first == second