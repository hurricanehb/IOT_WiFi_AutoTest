from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from testcases import conftest
from testcases.conftest import _case_log_name, _summarize_case_reports


class FakeItem:
    name = "test_fallback_name"

    def get_closest_marker(self, name):
        if name == "case_id":
            return SimpleNamespace(args=("CASE-001",))
        return None


def _report(*, duration=0.1, failed=False, skipped=False, detail=""):
    return SimpleNamespace(
        duration=duration,
        failed=failed,
        skipped=skipped,
        longrepr=detail,
        longreprtext=detail,
    )


def test_case_log_name_prefers_case_id_marker() -> None:
    assert _case_log_name(FakeItem()) == "CASE-001"


def test_summarize_case_reports_returns_passed_and_total_duration() -> None:
    status, duration, reason = _summarize_case_reports(
        {
            "setup": _report(duration=0.1),
            "call": _report(duration=0.2),
            "teardown": _report(duration=0.3),
        }
    )

    assert status == "PASSED"
    assert duration == 0.6
    assert reason == ""


def test_summarize_case_reports_preserves_skip_reason() -> None:
    status, duration, reason = _summarize_case_reports(
        {
            "setup": _report(skipped=True, detail="Skipped: cli_app 不可用"),
            "teardown": _report(),
        }
    )

    assert status == "SKIPPED"
    assert duration == 0.2
    assert reason == "Skipped: cli_app 不可用"


def test_summarize_case_reports_prioritizes_failure() -> None:
    status, _, reason = _summarize_case_reports(
        {
            "call": _report(skipped=True, detail="Skipped: earlier skip"),
            "teardown": _report(failed=True, detail="AssertionError: cleanup failed"),
        }
    )

    assert status == "FAILED"
    assert reason == "AssertionError: cleanup failed"


def test_capture_failed_report_collects_once_and_exports_one_packlog(
    monkeypatch,
) -> None:
    config = SimpleNamespace(
        _failure_diagnostic_signatures=set(),
        _failure_packlogs_exported=False,
    )
    item = SimpleNamespace(
        name="test_wifi_failure",
        nodeid="test_wifi_failure",
        fixturenames=("adb", "settings_ui"),
        funcargs={"adb": Mock(), "settings_ui": Mock()},
        config=config,
        get_closest_marker=Mock(return_value=None),
    )
    report = SimpleNamespace(
        failed=True,
        when="call",
        longrepr="AssertionError: disconnected",
        longreprtext="AssertionError: disconnected",
    )
    capture = Mock(return_value=[Path("failure.txt")])
    export = Mock()
    monkeypatch.setattr(conftest, "capture_failure_diagnostics", capture)
    monkeypatch.setattr(conftest, "_attach_failure_artifacts", Mock())
    monkeypatch.setattr(conftest, "export_device_packlogs", export)
    monkeypatch.setattr(conftest, "log_report_dir", lambda: Path("missing-log-dir"))

    conftest._capture_failed_report(item, report)
    conftest._capture_failed_report(item, report)

    capture.assert_called_once()
    export.assert_called_once()
    assert config._failure_packlogs_exported is True


def test_capture_failed_report_skips_packlogs_for_prerequisite_failure(
    monkeypatch,
) -> None:
    config = SimpleNamespace(
        _failure_diagnostic_signatures=set(),
        _failure_packlogs_exported=False,
    )
    item = SimpleNamespace(
        name="test_wifi_setup",
        nodeid="test_wifi_setup",
        fixturenames=("adb",),
        funcargs={"adb": Mock()},
        config=config,
        get_closest_marker=Mock(return_value=None),
    )
    report = SimpleNamespace(
        failed=True,
        when="setup",
        longrepr="前置条件失败：无法打开 WiFi 开关",
        longreprtext="前置条件失败：无法打开 WiFi 开关",
    )
    export = Mock()
    monkeypatch.setattr(conftest, "capture_failure_diagnostics", Mock(return_value=[]))
    monkeypatch.setattr(conftest, "_attach_failure_artifacts", Mock())
    monkeypatch.setattr(conftest, "export_device_packlogs", export)

    conftest._capture_failed_report(item, report)

    export.assert_not_called()


def test_capture_failed_report_does_not_raise_when_diagnostics_fail(
    monkeypatch,
) -> None:
    item = SimpleNamespace(
        name="test_wifi_failure",
        nodeid="test_wifi_failure",
        fixturenames=("adb",),
        funcargs={"adb": Mock()},
        config=SimpleNamespace(
            _failure_diagnostic_signatures=set(),
            _failure_packlogs_exported=False,
        ),
        get_closest_marker=Mock(return_value=None),
    )
    report = SimpleNamespace(
        failed=True,
        when="call",
        longrepr="AssertionError: original failure",
        longreprtext="AssertionError: original failure",
    )
    monkeypatch.setattr(
        conftest,
        "capture_failure_diagnostics",
        Mock(side_effect=OSError("report directory is read-only")),
    )
    monkeypatch.setattr(conftest, "export_device_packlogs", Mock())
    monkeypatch.setattr(conftest, "log_report_dir", lambda: Path("missing-log-dir"))

    conftest._capture_failed_report(item, report)