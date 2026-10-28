import zipfile
from pathlib import Path
from unittest.mock import Mock

from core.utils import device_log_export


def test_export_device_packlogs_pulls_and_compresses_public_logs(monkeypatch, tmp_path: Path) -> None:
    adb = Mock()

    def pull_logs(*args, **kwargs):
        local = Path(args[2])
        local.mkdir(parents=True)
        (local / "system.log").write_text("failure details", encoding="utf-8")
        return 0, "1 file pulled", ""

    adb.run.side_effect = pull_logs
    monkeypatch.setattr(device_log_export, "log_report_dir", lambda: tmp_path)

    exported = device_log_export.export_device_packlogs(
        adb,
        reason="connection failed",
        label="CASE-001",
    )

    assert exported is not None
    assert exported.parent == tmp_path / "device_packlogs"
    assert exported.name.startswith("logs_CASE-001_")
    assert exported.suffix == ".zip"
    assert not exported.with_suffix("").exists()
    with zipfile.ZipFile(exported) as archive:
        assert archive.read("system.log").decode("utf-8") == "failure details"
    adb.run.assert_called_once_with(
        "pull",
        "/data/public/logs",
        str(exported.with_suffix("")),
        shell=False,
    )


def test_export_device_packlogs_keeps_directory_when_compression_fails(
    monkeypatch, tmp_path: Path
) -> None:
    adb = Mock()

    def pull_logs(*args, **kwargs):
        local = Path(args[2])
        local.mkdir(parents=True)
        (local / "system.log").write_text("failure details", encoding="utf-8")
        return 0, "1 file pulled", ""

    adb.run.side_effect = pull_logs
    monkeypatch.setattr(device_log_export, "log_report_dir", lambda: tmp_path)
    monkeypatch.setattr(
        device_log_export.shutil,
        "make_archive",
        Mock(side_effect=OSError("disk full")),
    )

    exported = device_log_export.export_device_packlogs(adb, label="CASE-002")

    assert exported is not None
    assert exported.is_dir()
    assert (exported / "system.log").is_file()