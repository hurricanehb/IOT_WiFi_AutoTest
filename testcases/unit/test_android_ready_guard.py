from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from testcases.support import android_ready_guard as plugin

pytest_plugins = ["pytester"]

BOOT_ID = "24681357-1234-1234-1234-123456789abc"
NEW_BOOT_ID = "87654321-4321-4321-4321-cba987654321"


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


@pytest.fixture
def clock(monkeypatch):
    clock = FakeClock()
    monkeypatch.setattr(plugin.time, "monotonic", clock.monotonic)
    monkeypatch.setattr(plugin.time, "sleep", clock.sleep)
    return clock


def _ready_output(boot_id=BOOT_ID):
    return (
        f"1\n{boot_id}\nService activity: found\nService package: found\n"
        "Service window: found\nWifi is disabled"
    )


def test_probe_requires_completed_boot_and_services(monkeypatch):
    run = Mock(return_value=SimpleNamespace(returncode=0, stdout=_ready_output(), stderr=""))
    monkeypatch.setattr(plugin.subprocess, "run", run)

    assert plugin.AndroidReadyGuard("ABC")._probe(4.0) == (BOOT_ID, "ready")
    assert run.call_args.kwargs["timeout"] == 4.0
    assert run.call_args.args[0][:4] == ["adb", "-s", "ABC", "shell"]


@pytest.mark.parametrize(
    "output",
    [
        _ready_output().replace("1\n", "0\n", 1),
        _ready_output().replace(BOOT_ID, "invalid"),
        _ready_output().replace("Service activity: found", "Service activity: not found"),
        _ready_output().replace("Service package: found", "Service package: not found"),
        _ready_output().replace("Service window: found", "Service window: not found"),
        _ready_output().replace("Wifi is disabled", "Can't find service: wifi"),
    ],
)
def test_probe_does_not_accept_partial_readiness(monkeypatch, output):
    monkeypatch.setattr(
        plugin.subprocess, "run",
        Mock(return_value=SimpleNamespace(returncode=0, stdout=output, stderr="")),
    )
    assert plugin.AndroidReadyGuard("ABC")._probe(5.0)[0] is None


def test_wait_recovers_after_device_disappears(clock, monkeypatch):
    guard = plugin.AndroidReadyGuard("ABC", timeout_sec=10)
    probe = Mock(side_effect=[
        (None, "ADB unavailable"),
        (None, "Android boot not completed"),
        (BOOT_ID, "ready"),
        (BOOT_ID, "ready"),
        (BOOT_ID, "ready"),
    ])
    monkeypatch.setattr(guard, "_probe", probe)

    guard.wait("test_reboot", "teardown")

    assert clock.now == 4
    assert guard.last_boot_id == BOOT_ID
    assert probe.call_count == 5


def test_wait_resets_stability_when_boot_changes(clock, monkeypatch):
    guard = plugin.AndroidReadyGuard("ABC", timeout_sec=10)
    monkeypatch.setattr(guard, "_probe", Mock(side_effect=[
        (BOOT_ID, "ready"),
        (NEW_BOOT_ID, "ready"),
        (NEW_BOOT_ID, "ready"),
        (NEW_BOOT_ID, "ready"),
    ]))

    guard.wait("test_reboot", "teardown")

    assert clock.now == 3
    assert guard.last_boot_id == NEW_BOOT_ID


def test_next_setup_probes_again_without_extra_delay(clock, monkeypatch):
    guard = plugin.AndroidReadyGuard("ABC")
    guard.last_boot_id = BOOT_ID
    probe = Mock(return_value=(BOOT_ID, "ready"))
    monkeypatch.setattr(guard, "_probe", probe)

    guard.wait("test_next", "setup")

    probe.assert_called_once()
    assert clock.now == 0


def test_recovery_timeout_stops_run(clock, monkeypatch):
    guard = plugin.AndroidReadyGuard("ABC", timeout_sec=3)
    monkeypatch.setattr(guard, "_probe", Mock(return_value=(None, "ADB unavailable")))

    with pytest.raises(pytest.exit.Exception, match="prevent cascading") as caught:
        guard.wait("test_reboot", "teardown")

    assert clock.now == 3
    assert caught.value.returncode == pytest.ExitCode.TESTS_FAILED


def test_guard_ignores_non_android_cases():
    item = SimpleNamespace(
        path=plugin._ANDROID_CASES.parent / "unit" / "android" / "test_example.py",
        fixturenames=("adb",),
    )
    assert not plugin._is_android_device_case(item)


def test_guard_ignores_data_only_android_cases():
    item = SimpleNamespace(
        path=plugin._ANDROID_CASES / "test_example.py", fixturenames=("wifi_yaml",),
    )
    assert not plugin._is_android_device_case(item)


def _configure_pytester_device(pytester, monkeypatch, state, probe):
    monkeypatch.setattr(plugin, "_ANDROID_CASES", pytester.path)
    monkeypatch.setattr(plugin, "_test_state", state, raising=False)
    monkeypatch.setattr(plugin, "get_settings", lambda: SimpleNamespace(android_serial="ABC"))
    monkeypatch.setattr(plugin.AndroidReadyGuard, "_probe", probe)
    pytester.makeini("[pytest]\n")
    pytester.makeconftest('''
import pytest
from testcases.support import android_ready_guard as plugin

@pytest.fixture
def adb(request):
    plugin._test_state["events"].append("setup")
    def cleanup():
        plugin._test_state["events"].append("cleanup")
        assert plugin._test_state["ready"]
    request.addfinalizer(cleanup)
    return object()
''')
    pytester.makepyfile('''
from core.utils.adb_helper import AdbDeviceUnavailableError
from testcases.support import android_ready_guard as plugin

def test_reboot(adb):
    plugin._test_state["events"].append("reboot")
    plugin._test_state["ready"] = False
    raise AdbDeviceUnavailableError("error: device 'ABC' not found")

def test_next(adb):
    plugin._test_state["events"].append("next")
    assert plugin._test_state["ready"]
''')


def test_pytest_waits_before_cleanup_and_preserves_original_failure(
    pytester, monkeypatch, clock,
):
    state = {"ready": True, "recovered": False, "offline_polls": 0, "events": []}

    def probe(self, timeout_sec):
        if not state["ready"]:
            state["offline_polls"] += 1
            if state["offline_polls"] < 3:
                return None, "ADB unavailable"
            state["ready"] = True
            state["recovered"] = True
            state["events"].append("recovered")
        return (NEW_BOOT_ID if state["recovered"] else BOOT_ID), "ready"

    _configure_pytester_device(pytester, monkeypatch, state, probe)

    result = pytester.runpytest_inprocess("-p", plugin.__name__, "-q")

    result.assert_outcomes(failed=1, passed=1)
    assert state["events"] == [
        "setup", "reboot", "recovered", "cleanup", "setup", "next", "cleanup",
    ]
    assert state["offline_polls"] == 3


def test_pytest_stops_before_next_case_when_recovery_times_out(
    pytester, monkeypatch, clock,
):
    state = {"ready": True, "events": []}

    def probe(self, timeout_sec):
        return (BOOT_ID, "ready") if state["ready"] else (None, "ADB unavailable")

    _configure_pytester_device(pytester, monkeypatch, state, probe)

    result = pytester.runpytest_inprocess(
        "-p", plugin.__name__, "--android-ready-timeout=3", "-q",
    )

    result.assert_outcomes(failed=1, errors=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert "next" not in state["events"]
    assert "Android readiness timeout" in result.stdout.str()


def test_pytest_does_not_probe_marked_skipped_case(pytester, monkeypatch):
    monkeypatch.setattr(plugin, "_ANDROID_CASES", pytester.path)
    probe = Mock(side_effect=AssertionError("Skipped case must not access ADB"))
    monkeypatch.setattr(plugin.AndroidReadyGuard, "_probe", probe)
    pytester.makeini("[pytest]\n")
    pytester.makeconftest('''
import pytest

@pytest.fixture
def adb():
    raise AssertionError("Skipped case must not set up fixtures")
''')
    pytester.makepyfile('''
import pytest

@pytest.mark.skip(reason="not applicable")
def test_skipped(adb):
    raise AssertionError("Skipped case must not run")
''')

    result = pytester.runpytest_inprocess("-p", plugin.__name__, "-q")

    result.assert_outcomes(skipped=1)
    probe.assert_not_called()


@pytest.mark.parametrize("timeout", [0, 2, float("nan"), float("inf")])
def test_plugin_rejects_invalid_recovery_timeout(timeout):
    config = SimpleNamespace(
        getoption=Mock(return_value=timeout), option=SimpleNamespace(numprocesses=None),
    )
    with pytest.raises(pytest.UsageError, match="greater than 2"):
        plugin.pytest_configure(config)


def test_plugin_rejects_parallel_device_execution():
    config = SimpleNamespace(
        getoption=Mock(return_value=180), option=SimpleNamespace(numprocesses=2),
    )
    with pytest.raises(pytest.UsageError, match="serial pytest"):
        plugin.pytest_configure(config)