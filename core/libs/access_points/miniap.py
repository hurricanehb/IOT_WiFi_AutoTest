"""HaLow miniAP radio, country-code, and security configuration."""
from __future__ import annotations

import re
from shlex import quote
import time
from typing import Optional, Union

from core.utils.telnet_session import TelnetSession
from core.utils.config_loader import MiniAPConfig, Settings, get_settings
from core.utils.log_handler import get_logger

log = get_logger(__name__)

TELNET_PORT = 23
DEFAULT_RELOAD_WAIT_SEC = 20
DEFAULT_REBOOT_WAIT_SEC = 60
DEFAULT_LOGIN_RETRY_INTERVAL_SEC = 5
_COUNTRY_ID_RE = re.compile(r"^[0-9A-Fa-f]{8}$")


class MiniAPAction:
    """Configure the HaLow miniAP over Telnet."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        *,
        session: Optional[TelnetSession] = None,
    ) -> None:
        self._session = session or TelnetSession()
        self._settings = settings or get_settings()
        self._mini: MiniAPConfig = self._settings.miniAP_config

    def close(self) -> None:
        self._session.close()

    def _cmd(self, command: str) -> str:
        return self._session.execute_command(command)

    def _uci_set(self, option: str, value: Union[int, str]) -> str:
        return self._cmd(f"uci set {option}={quote(str(value))}")

    @staticmethod
    def _positive_integer(value: Union[int, str], name: str) -> str:
        text = str(value).strip()
        if not text.isdigit() or int(text) <= 0:
            raise ValueError(f"{name} 必须为正整数: {value!r}")
        return text

    def _login_miniap(self) -> None:
        self._session.login(
            self._mini.miniAP_ip,
            self._mini.miniAP_root,
            self._mini.miniAP_login_password,
            TELNET_PORT,
            self._mini.miniAP_flag,
        )

    def _wait_for_miniap_ready(
        self,
        timeout_sec: float = DEFAULT_REBOOT_WAIT_SEC,
        interval_sec: float = DEFAULT_LOGIN_RETRY_INTERVAL_SEC,
    ) -> None:
        """等待 miniAP 重启完成并连续两次可重新登录。"""
        deadline = time.monotonic() + timeout_sec
        last_error: Optional[Exception] = None
        consecutive_logins = 0

        while True:
            try:
                self._login_miniap()
                consecutive_logins += 1
                if consecutive_logins >= 2:
                    log.info("miniAP 已稳定重新登录")
                    return
            except Exception as exc:
                last_error = exc
                consecutive_logins = 0

            remaining_sec = deadline - time.monotonic()
            if remaining_sec <= 0:
                raise TimeoutError(
                    f"等待 miniAP 重启完成超时（{timeout_sec} 秒）"
                ) from last_error

            log.info(
                "miniAP 尚未就绪，%.1f 秒后重试：%s",
                min(interval_sec, remaining_sec),
                last_error or "等待连续登录确认",
            )
            time.sleep(min(interval_sec, remaining_sec))

    def _reload_halow(self, wait_sec: float = DEFAULT_RELOAD_WAIT_SEC) -> None:
        self._cmd("/etc/init.d/halow reload")
        time.sleep(wait_sec)

    def set_countrycode(
        self,
        region: Union[int, str],
        special_id: Union[int, str],
        h_ssid: str,
        h_pwd: str,
    ) -> None:
        """修改国家码并重建 HyperWiFi SSID/密钥。

        miniAP 命令序列：
          dwrite SPECIAL_ID={special_id},COUNTRY_ID={region}
          halow reset country
          reboot
        """
        country_id = str(region).strip().upper()
        sid = str(special_id).strip()
        if country_id not in ("US", "EU"):
            raise ValueError(f"不支持的 miniAP 国家码: {region!r}，支持 US/EU")
        if not _COUNTRY_ID_RE.fullmatch(sid):
            raise ValueError(f"SPECIAL_ID 必须为 8 位十六进制数: {special_id!r}")
        log.info(
            "设置 miniAP 国家码：dwrite SPECIAL_ID=%s,COUNTRY_ID=%s",
            sid,
            country_id,
        )
        self._login_miniap()
        time.sleep(2)
        self._cmd(f"dwrite SPECIAL_ID={sid},COUNTRY_ID={country_id}")
        time.sleep(1)
        self._cmd("halow reset country")
        time.sleep(2)
        self._cmd("reboot")
        self._wait_for_miniap_ready()
        time.sleep(1)
        self._uci_set("halow.ap.ssid", h_ssid)
        time.sleep(1)
        self._uci_set("halow.ap.key", h_pwd)
        time.sleep(1)
        self._cmd("uci commit")
        time.sleep(3)
        self._reload_halow(10)

    def set_channel(self, channel: Union[int, str]) -> None:
        target_channel = self._positive_integer(channel, "channel")
        self._login_miniap()
        time.sleep(1)
        self._uci_set("halow.ap.channel", target_channel)
        time.sleep(2)
        self._cmd("uci commit")
        time.sleep(2)
        self._reload_halow()

    def set_bandwidth_channel(self, bandwidth: Union[int, str], channel: Union[int, str]) -> None:
        target_bandwidth = self._positive_integer(bandwidth, "bandwidth")
        target_channel = self._positive_integer(channel, "channel")
        log.info(
            "设置 miniAP 带宽/信道：bandwidth=%sMHz channel=%s",
            target_bandwidth,
            target_channel,
        )
        self._login_miniap()
        time.sleep(1)
        self._uci_set("halow.ap.bandwidth", target_bandwidth)
        time.sleep(1)
        self._uci_set("halow.ap.channel", target_channel)
        time.sleep(1)
        self._cmd("uci commit")
        time.sleep(2)
        self._reload_halow()

    def set_bandwidth(self, bandwidth: Union[int, str]) -> None:
        target_bandwidth = self._positive_integer(bandwidth, "bandwidth")
        self._login_miniap()
        time.sleep(1)
        self._uci_set("halow.ap.bandwidth", target_bandwidth)
        time.sleep(2)
        self._cmd("uci commit")
        time.sleep(2)
        self._reload_halow()

    def set_ssid(self, ssid: str) -> None:
        self._login_miniap()
        time.sleep(1)
        self._uci_set("halow.ap.ssid", ssid)
        time.sleep(2)
        self._cmd("uci commit")
        self._reload_halow()

    def restart_wl(self) -> None:
        self._login_miniap()
        time.sleep(1)
        self._cmd("/etc/init.d/halow restart")
        time.sleep(30)

    def stop_radio(self) -> None:
        self._login_miniap()
        self._cmd("/etc/init.d/halow stop")

    def start_radio(self, wait_sec: float = 35.0) -> None:
        self._login_miniap()
        self._cmd("/etc/init.d/halow start")
        time.sleep(wait_sec)

    def reboot_miniAP(self) -> None:
        self._login_miniap()
        time.sleep(1)
        self._cmd("reboot")
        self._wait_for_miniap_ready()

    def mAP_connect_check(self, keywords: str) -> bool:
        self._login_miniap()
        time.sleep(1)
        results = self._cmd("cli_app show sta 0")
        time.sleep(1)
        ok = keywords in results
        if ok:
            log.info("miniAP STA 校验成功：keywords=%r output=%s", keywords, results[:300])
        else:
            log.warning("miniAP STA 校验失败：keywords=%r output=%s", keywords, results[:300])
        return ok

    def set_encryption(self, encryption: str, key: str = "24681357") -> None:
        self._login_miniap()
        time.sleep(1)
        enc = self._normalize_encryption(encryption)
        if enc == "open":
            self._uci_set("halow.ap.encryption", enc)
            time.sleep(2)
            self._cmd("uci delete halow.ap.key")
            time.sleep(2)
        else:
            self._uci_set("halow.ap.encryption", enc)
            time.sleep(2)
            self._uci_set("halow.ap.key", key)
            time.sleep(2)

        self._cmd("uci commit")
        time.sleep(2)
        self._reload_halow(60)

    @staticmethod
    def _normalize_encryption(encryption: str) -> str:
        raw = (encryption or "").strip().lower()
        if raw in ("open", "none"):
            return "open"
        if raw in ("wpa3", "wpa3-sae", "sae"):
            return "wpa3-sae"
        if raw in ("wpa2", "wpa2-psk", "psk2"):
            return "psk2"
        if raw in ("wpa", "wpa-psk", "psk"):
            return "psk"
        raise ValueError(
            f"不支持的加密方式: {encryption!r}，支持 open/wpa/wpa2/wpa3"
        )

    def set_wifi_profile(self, ssid: str, pwd: str, encryption: str) -> None:
        """一键设置 miniAP 的 SSID/密码/加密，并重载无线。"""
        self._login_miniap()
        time.sleep(1)

        target_ssid = (ssid or "").strip()
        if not target_ssid:
            raise ValueError("SSID 不能为空")

        enc = self._normalize_encryption(encryption)
        self._uci_set("halow.ap.ssid", target_ssid)
        time.sleep(1)
        self._uci_set("halow.ap.encryption", enc)
        time.sleep(1)

        if enc == "open":
            self._cmd("uci delete halow.ap.key")
        else:
            self._uci_set("halow.ap.key", (pwd or "").strip())
        time.sleep(1)

        self._cmd("uci commit")
        time.sleep(2)
        # 对 SSID/加密改配，restart 比 reload 更稳定，避免旧配置残留。
        self._cmd("/etc/init.d/halow restart")
        time.sleep(35)

    def read_wifi_profile_summary(self) -> str:
        """读取 miniAP 当前 WiFi 关键配置，供日志排查。"""
        self._login_miniap()
        time.sleep(1)
        lines = []
        for key in ("ssid", "encryption", "key"):
            lines.append(self._cmd(f"uci get halow.ap.{key}"))
            time.sleep(0.5)
        return "\n".join(line.strip() for line in lines if line)
