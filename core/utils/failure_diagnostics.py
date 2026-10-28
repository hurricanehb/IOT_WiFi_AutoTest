"""Collect durable, lightweight diagnostics for failed Android tests."""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path
from typing import Any, Optional

from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger
from core.utils.report_utils import report_run_dir

log = get_logger(__name__)

_MAX_TEXT_CHARS = 2_000_000
_DIAGNOSTIC_COMMANDS = (
    ("wifi_status.txt", "cmd wifi status"),
    ("dumpsys_wifi.txt", "dumpsys wifi"),
    ("logcat_tail.txt", "logcat -d -t 2000 -v threadtime"),
)


def safe_artifact_label(text: str) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", (text or "").strip())
    return (cleaned.strip("_") or "failure")[:100]


def failure_signature(phase: str, reason: str) -> str:
    """Group repeated failures without depending on case IDs or temp paths."""
    normalized = re.sub(r"[A-Za-z]:\\[^；,\n]+", "<path>", reason or "")
    normalized = re.sub(r"\d+", "<n>", normalized)
    return f"{phase}:{normalized[-500:]}"


def _write_text(path: Path, text: str) -> None:
    path.write_text((text or "<empty>")[:_MAX_TEXT_CHARS], encoding="utf-8")


def _capture_ui(settings_ui: Any, destination: Path) -> list[Path]:
    artifacts: list[Path] = []
    source_dir = Path(settings_ui.artifact_dir)
    if source_dir.is_dir():
        for source in source_dir.iterdir():
            if source.is_file() and source.suffix.lower() in {".png", ".xml"}:
                target = destination / source.name
                shutil.copy2(source, target)
                artifacts.append(target)

    hierarchy = destination / "current_ui.xml"
    screenshot = destination / "current_ui.png"
    _write_text(hierarchy, settings_ui.device.dump_hierarchy())
    settings_ui.device.screenshot(str(screenshot))
    artifacts.append(hierarchy)
    if screenshot.is_file():
        artifacts.append(screenshot)
    return artifacts


def capture_failure_diagnostics(
    adb: Optional[AdbHelper],
    *,
    label: str,
    phase: str,
    reason: str,
    settings_ui: Optional[Any] = None,
) -> list[Path]:
    """Capture read-only device state without masking the original failure."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    destination = (
        report_run_dir()
        / "failure_artifacts"
        / f"{safe_artifact_label(label)}_{timestamp}"
    )
    destination.mkdir(parents=True, exist_ok=True)

    summary = destination / "failure.txt"
    _write_text(summary, f"phase={phase}\nreason={reason or '-'}\n")
    artifacts = [summary]

    if adb is not None:
        for filename, command in _DIAGNOSTIC_COMMANDS:
            target = destination / filename
            try:
                code, stdout, stderr = adb.shell_line(command, timeout_sec=30.0)
                _write_text(
                    target,
                    f"command={command}\nreturncode={code}\n\n"
                    f"stdout:\n{stdout or '<empty>'}\n\nstderr:\n{stderr or '<empty>'}\n",
                )
            except Exception as error:
                _write_text(target, f"command={command}\nerror={error!r}\n")
            artifacts.append(target)

    if settings_ui is not None:
        try:
            artifacts.extend(_capture_ui(settings_ui, destination))
        except Exception as error:
            ui_error = destination / "ui_capture_error.txt"
            _write_text(ui_error, repr(error))
            artifacts.append(ui_error)

    log.warning("失败诊断已归档：%s", destination)
    return artifacts