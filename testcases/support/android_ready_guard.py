"""Opt-in pytest readiness barriers for serial Android hardware runs."""
from __future__ import annotations

import logging
import math
import subprocess
import time
from pathlib import Path
from uuid import UUID

import pytest

from core.utils.config_loader import get_settings
from core.utils.device_mgr import DeviceManager

log = logging.getLogger(__name__)
_ANDROID_CASES = Path(__file__).resolve().parents[1] / "android"
_DEVICE_FIXTURES = {"adb", "wifi", "run_shell_cmd", "settings_ui"}
_READINESS_COMMAND = (
    "getprop sys.boot_completed; cat /proc/sys/kernel/random/boot_id; "
    "service check activity; service check package; service check window; "
    "cmd wifi status"
)


class AndroidReadyGuard:
    def __init__(self, serial: str, timeout_sec: float = 180.0):
        self.serial = serial
        self.timeout_sec = timeout_sec
        self.last_boot_id: str | None = None

    def _probe(self, timeout_sec: float) -> tuple[str | None, str]:
        try:
            result = subprocess.run(
                ["adb", "-s", self.serial, "shell", _READINESS_COMMAND],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_sec,
            )
        except subprocess.TimeoutExpired:
            return None, "ADB probe timed out"
        except OSError as error:
            pytest.exit(
                f"Android readiness guard cannot execute adb: {error}",
                returncode=pytest.ExitCode.TESTS_FAILED,
            )

        if result.returncode != 0:
            reason = "ADB unavailable"
            if "unauthorized" in (result.stderr or "").lower():
                reason = "ADB unauthorized"
            return None, reason
        lines = result.stdout.strip().splitlines()
        if not lines or lines[0].strip() != "1":
            return None, "Android boot not completed"
        if len(lines) < 6:
            return None, "Android services not ready"
        try:
            boot_id = str(UUID(lines[1].strip()))
        except ValueError:
            return None, "Android boot ID unavailable"
        for service, output in zip(("activity", "package", "window"), lines[2:5]):
            if output.strip() != f"Service {service}: found":
                return None, f"Android {service} service not ready"
        wifi_output = "\n".join(lines[5:]).lower()
        if not wifi_output.strip() or any(
            value in wifi_output
            for value in ("can't find service", "unknown command", "exception", "error:")
        ):
            return None, "Android WiFi service not ready"
        return boot_id, "ready"

    def wait(self, nodeid: str, phase: str) -> None:
        deadline = time.monotonic() + self.timeout_sec
        stable_since: float | None = None
        stable_boot_id: str | None = None
        last_reason = "readiness not checked"
        last_log_time = float("-inf")
        observed_unready = False
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            boot_id, last_reason = self._probe(min(5.0, remaining))
            now = time.monotonic()
            if now >= deadline:
                break
            if boot_id is not None:
                if (
                    phase == "setup"
                    and not observed_unready
                    and boot_id == self.last_boot_id
                ):
                    return
                if boot_id != stable_boot_id:
                    stable_boot_id = boot_id
                    stable_since = now
                if stable_since is not None and now - stable_since >= 2.0:
                    self.last_boot_id = boot_id
                    log.info(
                        "Android ready: serial=%s phase=%s case=%s",
                        self.serial, phase, nodeid,
                    )
                    return
                last_reason = "waiting for stable Android services"
            else:
                observed_unready = True
                stable_boot_id = None
                stable_since = None
            if now - last_log_time >= 10.0:
                log.info(
                    "Waiting for Android: serial=%s phase=%s remaining=%.1fs "
                    "state=%s case=%s",
                    self.serial, phase, max(0.0, deadline - now), last_reason, nodeid,
                )
                last_log_time = now
            time.sleep(min(1.0, max(0.0, deadline - time.monotonic())))
        pytest.exit(
            f"Android readiness timeout ({self.timeout_sec:g}s): "
            f"serial={self.serial}, phase={phase}, state={last_reason}, "
            f"case={nodeid}; stopping to prevent cascading device failures",
            returncode=pytest.ExitCode.TESTS_FAILED,
        )


def pytest_addoption(parser) -> None:
    group = parser.getgroup("android-ready-guard")
    group.addoption(
        "--android-ready-timeout", type=float, default=180.0,
        help="Maximum seconds for each Android readiness barrier (default: 180).",
    )


def pytest_configure(config) -> None:
    timeout_sec = config.getoption("android_ready_timeout")
    if not math.isfinite(timeout_sec) or timeout_sec <= 2.0:
        raise pytest.UsageError("--android-ready-timeout must be finite and greater than 2")
    if getattr(config.option, "numprocesses", None) not in (None, 0):
        raise pytest.UsageError("Android readiness guard requires serial pytest execution")


def _is_android_device_case(item) -> bool:
    return item.path.is_relative_to(_ANDROID_CASES) and bool(
        _DEVICE_FIXTURES & set(item.fixturenames)
    )


def _wait_for_item(item, phase: str) -> None:
    if not _is_android_device_case(item):
        return
    if phase == "teardown" and not getattr(item, "_android_ready_guard_active", False):
        return
    guard = getattr(item.config, "_android_ready_guard", None)
    if guard is None:
        serial = get_settings().android_serial
        if not serial:
            try:
                serial = DeviceManager().require_serial()
            except RuntimeError as error:
                pytest.exit(str(error), returncode=pytest.ExitCode.TESTS_FAILED)
        guard = AndroidReadyGuard(
            serial, timeout_sec=item.config.getoption("android_ready_timeout")
        )
        item.config._android_ready_guard = guard
    guard.wait(item.nodeid, phase)
    item._android_ready_guard_active = True


@pytest.hookimpl
def pytest_runtest_setup(item) -> None:
    _wait_for_item(item, "setup")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem) -> None:
    try:
        _wait_for_item(item, "teardown")
    except pytest.exit.Exception as error:
        item.session.shouldfail = str(error)
        log.error("%s", error)