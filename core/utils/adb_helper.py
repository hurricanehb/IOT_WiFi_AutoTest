"""ADB command wrapper for Android automation."""
from __future__ import annotations

import re
import subprocess
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

from core.utils.config_loader import get_settings
from core.utils.log_handler import get_logger

log = get_logger(__name__)


class AdbDeviceUnavailableError(RuntimeError):
    """ADB cannot communicate with the selected hardware device."""

    def __init__(self, message: str, *, statistics: Optional[str] = None):
        super().__init__(message)
        self.statistics = statistics


_DEVICE_UNAVAILABLE_PATTERNS = (
    re.compile(r"\bdevice(?:\s+['\"]?[^\s'\"]+['\"]?)?\s+not found\b", re.IGNORECASE),
    re.compile(r"\bdevice\s+(?:is\s+)?offline\b", re.IGNORECASE),
    re.compile(r"\bdevice\s+(?:is\s+)?unauthorized\b", re.IGNORECASE),
    re.compile(r"\bno devices?(?:/emulators)? found\b", re.IGNORECASE),
    re.compile(r"^\S+\s+(?:offline|unauthorized)$", re.IGNORECASE | re.MULTILINE),
)


def _raise_if_device_unavailable(command: List[str], out: str, err: str) -> None:
    output = "\n".join(part for part in (out, err) if part)
    if any(pattern.search(output) for pattern in _DEVICE_UNAVAILABLE_PATTERNS):
        raise AdbDeviceUnavailableError(
            f"ADB device unavailable: {' '.join(command)}\n{output}"
        )


class AdbHelper:
    def __init__(self, serial: Optional[str] = None, timeout_sec: Optional[int] = None):
        s = get_settings()
        self.serial = (serial or s.android_serial or "").strip() or None
        self.timeout_sec = timeout_sec if timeout_sec is not None else s.adb_timeout_sec

    def _base(self) -> List[str]:
        cmd = ["adb"]
        if self.serial:
            cmd.extend(["-s", self.serial])
        return cmd

    def run(
        self,
        *adb_args: str,
        shell: bool = False,
        check: bool = False,
        capture: bool = True,
    ) -> Tuple[int, str, str]:
        if shell:
            cmd = self._base() + ["shell"] + list(adb_args)
        else:
            cmd = self._base() + list(adb_args)
        try:
            p = subprocess.run(
                cmd,
                capture_output=capture,
                text=True,
                timeout=self.timeout_sec,
                encoding="utf-8",
                errors="replace",
            )
            out = (p.stdout or "").strip()
            err = (p.stderr or "").strip()
            if p.returncode != 0:
                _raise_if_device_unavailable(cmd, out, err)
            if check and p.returncode != 0:
                raise RuntimeError(f"ADB failed: {' '.join(cmd)}\n{err or out}")
            return p.returncode, out, err
        except subprocess.TimeoutExpired:
            log.warning("ADB timeout: %s", " ".join(cmd))
            return -1, "", "timeout"

    def devices(self) -> List[Tuple[str, str]]:
        code, out, _ = self.run("devices", shell=False)
        rows: List[Tuple[str, str]] = []
        if code != 0:
            return rows
        for line in out.splitlines()[1:]:
            parts = line.split("\t")
            if len(parts) == 2:
                rows.append((parts[0].strip(), parts[1].strip()))
        return rows

    def shell(self, *args: str, check: bool = False) -> Tuple[int, str, str]:
        """Discrete adb shell tokens, e.g. shell(\"cmd\", \"wifi\", \"status\")."""
        return self.run(*args, shell=True, check=check)

    def shell_line(
        self,
        command: str,
        check: bool = False,
        timeout_sec: Optional[float] = None,
    ) -> Tuple[int, str, str]:
        """
        Run one shell command line on device (pipes/redirection stay on device).

        Uses ``adb shell <command>`` with the whole line as a single argument so
        Windows hosts do not interpret ``|`` and adbd does not split ``sh -c`` words.
        """
        command = (command or "").strip()
        if not command:
            return 0, "", ""
        cmd = self._base() + ["shell", command]
        try:
            p = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec or self.timeout_sec,
                encoding="utf-8",
                errors="replace",
            )
            out = (p.stdout or "").strip()
            err = (p.stderr or "").strip()
            if p.returncode != 0:
                _raise_if_device_unavailable(cmd, out, err)
            if check and p.returncode != 0:
                raise RuntimeError(f"ADB failed: {' '.join(cmd)}\n{err or out}")
            return p.returncode, out, err
        except subprocess.TimeoutExpired:
            log.warning("ADB timeout: %s", " ".join(cmd))
            return -1, "", "timeout"

    def tap(self, x: int, y: int) -> None:
        self.shell("input", "tap", str(x), str(y))

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300) -> None:
        self.shell(
            "input",
            "swipe",
            str(x1),
            str(y1),
            str(x2),
            str(y2),
            str(duration_ms),
        )

    def keyevent(self, keycode: Union[str, int]) -> None:
        self.shell("input", "keyevent", str(keycode))

    def screenshot(self, device_path: str = "/sdcard/pyautotest_cap.png") -> Path:
        s = get_settings()
        local_root = Path(__file__).resolve().parent.parent / s.screenshot_dir
        local_root.mkdir(parents=True, exist_ok=True)
        self.shell("screencap", "-p", device_path)
        name = f"cap_{int(time.time() * 1000)}.png"
        local = local_root / name
        code, _, err = self.run("pull", device_path, str(local), shell=False)
        if code != 0:
            log.warning("screencap pull failed: %s", err)
        self.shell("rm", device_path)
        return local

    def wait_for_device(self, total_sec: float = 60.0, interval: float = 1.0) -> bool:
        deadline = time.monotonic() + total_sec
        while time.monotonic() < deadline:
            try:
                code, out, _ = self.run("get-state", shell=False)
                if code == 0 and out.strip() == "device":
                    return True
            except AdbDeviceUnavailableError as exc:
                log.debug("等待 ADB 设备恢复: %s", exc)
            time.sleep(interval)
        return False

    def is_root(self) -> bool:
        """Return True when adb shell runs as root (uid 0)."""
        code, out, _ = self.shell("id", "-u")
        if code == 0 and out.strip() == "0":
            return True
        code, out, _ = self.shell_line("id")
        text = (out or "").strip()
        return text == "0" or "uid=0" in text

    def ensure_root(self, *, try_adb_root: bool = True) -> bool:
        """
        Ensure adb shell has root. Tries ``adb root`` once when not already root.
        Returns False if still non-root (e.g. user/production build).
        """
        if self.is_root():
            log.info("ADB shell 已为 root (serial=%s)", self.serial or "default")
            return True
        if not try_adb_root:
            return False
        code, out, err = self.run("root", shell=False)
        msg = " ".join(x for x in (out, err) if x).strip()
        if code != 0:
            log.warning("adb root 失败 (serial=%s): %s", self.serial or "default", msg or code)
        else:
            log.info("adb root 已执行 (serial=%s)%s", self.serial or "default", f": {msg}" if msg else "")
        time.sleep(1.0)
        if self.is_root():
            return True
        log.warning("ADB shell 仍非 root (serial=%s)", self.serial or "default")
        return False
