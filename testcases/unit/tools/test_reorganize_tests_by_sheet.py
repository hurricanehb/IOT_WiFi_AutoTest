from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[3] / "tools" / "files-transfer" / "reorganize_tests_by_sheet.py"


@pytest.fixture
def reorganizer():
    spec = importlib.util.spec_from_file_location("reorganize_tests_by_sheet", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dry_run_does_not_create_directories_or_move_files(tmp_path, monkeypatch, reorganizer):
    source = tmp_path / "wifi_connection"
    source.mkdir()
    test_file = source / "test_generated.py"
    test_file.write_text('@pytest.mark.case_id("CASE-001")\n', encoding="utf-8")
    destination = tmp_path / "android" / "target"

    monkeypatch.setattr(reorganizer, "SRC", source)
    monkeypatch.setattr(reorganizer, "build_summary_to_sheet", lambda: {"CASE-001": "目标Sheet"})
    monkeypatch.setattr(reorganizer, "sheet_output_dir", lambda _sheet: destination)
    monkeypatch.setattr(
        reorganizer,
        "ensure_sheet_dirs",
        lambda: pytest.fail("dry-run must not create output directories"),
    )

    assert reorganizer.reorganize(dry_run=True) == 0
    assert test_file.exists()
    assert not destination.exists()


def test_dry_run_succeeds_when_source_was_already_migrated(tmp_path, monkeypatch, reorganizer):
    monkeypatch.setattr(reorganizer, "SRC", tmp_path / "missing-wifi-connection")

    assert reorganizer.reorganize(dry_run=True) == 0


def test_dry_run_does_not_create_legacy_destination(tmp_path, monkeypatch, reorganizer):
    source = tmp_path / "wifi_connection"
    source.mkdir()
    test_file = source / "test_AdvWlanSet_Mode.py"
    test_file.write_text("", encoding="utf-8")
    android_cases = tmp_path / "android"

    monkeypatch.setattr(reorganizer, "SRC", source)
    monkeypatch.setattr(reorganizer, "ANDROID_CASES", android_cases)
    monkeypatch.setattr(reorganizer, "build_summary_to_sheet", lambda: {})
    monkeypatch.setattr(
        reorganizer,
        "ensure_sheet_dirs",
        lambda: pytest.fail("dry-run must not create output directories"),
    )

    assert reorganizer.reorganize(dry_run=True) == 0
    assert test_file.exists()
    assert not android_cases.exists()


def test_apply_moves_files_to_mapped_sheet(tmp_path, monkeypatch, reorganizer):
    source = tmp_path / "wifi_connection"
    source.mkdir()
    test_file = source / "test_generated.py"
    test_file.write_text('@pytest.mark.case_id("CASE-001")\n', encoding="utf-8")
    destination = tmp_path / "android" / "target"

    monkeypatch.setattr(reorganizer, "SRC", source)
    monkeypatch.setattr(reorganizer, "build_summary_to_sheet", lambda: {"CASE-001": "目标Sheet"})
    monkeypatch.setattr(reorganizer, "sheet_output_dir", lambda _sheet: destination)
    monkeypatch.setattr(reorganizer, "ensure_sheet_dirs", lambda: [])

    assert reorganizer.reorganize() == 0
    assert not test_file.exists()
    assert (destination / test_file.name).exists()
