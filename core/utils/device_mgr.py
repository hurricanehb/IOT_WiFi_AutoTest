"""Manage Android device serials vs .env ANDROID_SERIAL / test_config.json."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from core.utils.adb_helper import AdbHelper
from core.utils.config_loader import get_settings
from core.utils.log_handler import get_logger

log = get_logger(__name__)


@dataclass
class DeviceInfo:
    serial: str
    state: str


class DeviceManager:
    def __init__(self, adb: Optional[AdbHelper] = None):
        self._adb = adb

    @property
    def adb(self) -> AdbHelper:
        return self._adb or AdbHelper()

    def list_online(self) -> List[DeviceInfo]:
        rows = self.adb.devices()
        return [DeviceInfo(s, st) for s, st in rows if st == "device"]

    def require_serial(self) -> str:
        s = get_settings().android_serial
        if s:
            for d in self.list_online():
                if d.serial == s:
                    return s
            raise RuntimeError(
                f"ANDROID_SERIAL={s!r} is not among online devices: {[d.serial for d in self.list_online()]}"
            )
        online = self.list_online()
        if len(online) == 1:
            return online[0].serial
        if not online:
            raise RuntimeError("No Android device in 'device' state. Connect USB/WiFi ADB.")
        if not s:
            raise RuntimeError(
                f"Multiple devices online {[d.serial for d in online]}; set ANDROID_SERIAL in .env or config/test_config.json"
            )
        return s

    def bind(self) -> AdbHelper:
        serial = self.require_serial()
        return AdbHelper(serial=serial)
