from unittest.mock import Mock, patch

import pytest

from core.utils.adb_helper import AdbDeviceUnavailableError, AdbHelper


@pytest.mark.parametrize(
    ("stdout", "stderr"),
    [
        ("", "error: device 'ABC' not found"),
        ("", "error: device offline"),
        ("", "error: device unauthorized"),
        ("", "error: no devices/emulators found"),
        ("List of devices attached\nABC\toffline", ""),
    ],
)
def test_run_raises_when_adb_reports_unavailable_device(stdout: str, stderr: str) -> None:
    completed = Mock(returncode=1, stdout=stdout, stderr=stderr)

    with patch("core.utils.adb_helper.subprocess.run", return_value=completed):
        with pytest.raises(AdbDeviceUnavailableError):
            AdbHelper(serial="ABC").run("get-state")


def test_shell_line_raises_when_adb_reports_unavailable_device() -> None:
    completed = Mock(returncode=1, stdout="", stderr="error: device offline")

    with patch("core.utils.adb_helper.subprocess.run", return_value=completed):
        with pytest.raises(AdbDeviceUnavailableError):
            AdbHelper(serial="ABC").shell_line("cmd wifi status")


@pytest.mark.parametrize("use_shell_line", [False, True])
@pytest.mark.parametrize("check", [False, True])
def test_wifi_dump_history_is_not_reported_as_adb_disconnect(
    use_shell_line: bool, check: bool
) -> None:
    wifi_dump = (
        "mRole: ROLE_SOFTAP_TETHERED\n"
        "getConnectedClientList().size(): 0\n"
        "10-20 15:16:51.979 827 976 I APM::AudioPolicyEngine: "
        "getDevicesForStrategyInt no device found for strategy 7"
    )
    completed = Mock(returncode=0, stdout=wifi_dump, stderr="")
    adb = AdbHelper(serial="ABC")

    with patch("core.utils.adb_helper.subprocess.run", return_value=completed):
        if use_shell_line:
            result = adb.shell_line("dumpsys wifi", check=check)
        else:
            result = adb.shell("dumpsys", "wifi", check=check)

    assert result == (0, wifi_dump, "")


@pytest.mark.parametrize("state", ["device not found", "device offline"])
def test_wait_for_device_returns_false_after_disconnect_timeout(state: str) -> None:
    adb = AdbHelper(serial="ABC")
    with (
        patch.object(adb, "run", side_effect=AdbDeviceUnavailableError(state)) as run,
        patch("core.utils.adb_helper.time.monotonic", side_effect=[0, 0, 1, 2]),
        patch("core.utils.adb_helper.time.sleep") as sleep,
    ):
        assert not adb.wait_for_device(total_sec=2)

    assert run.call_count == 2
    assert sleep.call_count == 2


def test_wait_for_device_does_not_hide_unexpected_errors() -> None:
    adb = AdbHelper(serial="ABC")
    with patch.object(adb, "run", side_effect=RuntimeError("unexpected error")):
        with pytest.raises(RuntimeError, match="unexpected error"):
            adb.wait_for_device()