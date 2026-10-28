"""Traditional WiFi AP configuration over Telnet."""
from __future__ import annotations

import codecs
from dataclasses import dataclass
import re
import time
from typing import Callable, Optional, Sequence, Tuple

from core.utils.config_loader import APConfig, Settings, get_settings
from core.utils.log_handler import get_logger
from core.utils.telnet_helper import TelnetClient

log = get_logger(__name__)

TELNET_PORT = 23
DEFAULT_AP_ID = 1


def _resolve_ap_id(override: Optional[int], configured: Optional[int]) -> int:
    """ap-id 以 0 起编号，不能用 or 链取默认值。"""
    if override is not None:
        return int(override)
    if configured is not None:
        return int(configured)
    return DEFAULT_AP_ID
RADIO_BY_BAND = {"2g": 0, "5g": 1}
CHANNELS_20MHZ = {
    "2g": tuple(range(1, 14)),
    "5g": (36, 40, 44, 48, 52, 56, 60, 64, 149, 153, 157, 161, 165),
}
_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,35}$")
_CONFIRMATION_MARKERS = ("[Y/N]", "(y/n)[n]:")
_MAX_CONFIRMATIONS = 5
_CONFIRMATION_SETTLE_SEC = 0.3


@dataclass(frozen=True)
class SecurityProfile:
    mode: str
    password: str = ""
    pmf: str = ""
    cipher: str = "aes"


SECURITY_PROFILES = {
    "open": SecurityProfile("open"),
    "wep40": SecurityProfile("wep-40"),
    "wep104": SecurityProfile("wep-104"),
    "wep128": SecurityProfile("wep-128"),
    "wpa-aes": SecurityProfile("wpa"),
    "wpa-tkip": SecurityProfile("wpa", cipher="tkip"),
    "wpa-aes-tkip": SecurityProfile("wpa", cipher="aes-tkip"),
    "wpa2-aes": SecurityProfile("wpa2"),
    "wpa2-tkip": SecurityProfile("wpa2", cipher="tkip"),
    "wpa2-aes-tkip": SecurityProfile("wpa2", cipher="aes-tkip"),
    "wpa2-aes-pmf-optional": SecurityProfile("wpa2", pmf="optional"),
    "wpa2-aes-pmf-mandatory": SecurityProfile("wpa2", pmf="mandatory"),
    "wpa-wpa2-aes": SecurityProfile("wpa-wpa2"),
    "wpa-wpa2-tkip": SecurityProfile("wpa-wpa2", cipher="tkip"),
    "wpa-wpa2-aes-tkip": SecurityProfile("wpa-wpa2", cipher="aes-tkip"),
    "wpa-wpa2-aes-pmf-optional": SecurityProfile("wpa-wpa2", pmf="optional"),
    "wpa-wpa2-aes-pmf-mandatory": SecurityProfile("wpa-wpa2", pmf="mandatory"),
    "wpa2-wpa3-aes": SecurityProfile("wpa2-wpa3", pmf="optional"),
    "wpa2-wpa3-aes-pmf-mandatory": SecurityProfile(
        "wpa2-wpa3", pmf="mandatory"
    ),
    "wpa3-aes": SecurityProfile("wpa3", pmf="mandatory"),
    "enhanced-open": SecurityProfile("enhanced-open", pmf="mandatory"),
    "wapi-psk": SecurityProfile("wapi"),
}

Command = Tuple[str, str]


class WiFiAPAction:
    """Configure an AirEngine9700S-S using its VRP WLAN profile model."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        *,
        client_factory: Callable[..., TelnetClient] = TelnetClient,
    ) -> None:
        self._settings = settings or get_settings()
        self._ap: APConfig = self._settings.ap_config
        self._client_factory = client_factory
        self._client: Optional[TelnetClient] = None
        self._sysname = self._parse_sysname(self._ap.ap_flag)

    @staticmethod
    def _parse_sysname(prompt: str) -> str:
        value = (prompt or "").strip()
        if value.startswith("<") and value.endswith(">") and len(value) > 2:
            return value[1:-1]
        raise ValueError(f"传统 WiFi AP 用户视图提示符无效: {prompt!r}")

    @staticmethod
    def _safe_name(value: str, field: str) -> str:
        text = (value or "").strip()
        if not _NAME_RE.fullmatch(text):
            raise ValueError(f"{field} 仅允许字母、数字、点、下划线、连字符: {value!r}")
        return text

    @staticmethod
    def _safe_value(value: str, field: str, *, allow_empty: bool = False) -> str:
        text = str(value or "")
        if "\r" in text or "\n" in text:
            raise ValueError(f"{field} 不允许换行符")
        if not text and not allow_empty:
            raise ValueError(f"{field} 不能为空")
        return text

    @property
    def connected(self) -> bool:
        return self._client is not None and self._client.connected

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def login(self) -> None:
        if self.connected:
            return
        if not self._ap.ap_ip:
            raise ValueError("传统 WiFi AP ap_ip 为空")
        client = self._client_factory(
            self._ap.ap_ip,
            port=TELNET_PORT,
            timeout_sec=15,
            encoding="utf-8",
            errors="replace",
        )
        client.connect()
        client.read_until(b"Username:", timeout_sec=10)
        client.write_line(self._ap.ap_login_username)
        client.read_until(b"Password:", timeout_sec=10)
        client.write_line(self._ap.ap_login_password)
        output = client.read_until(self._ap.ap_flag, timeout_sec=15)
        if self._ap.ap_flag.encode() not in output:
            client.close()
            raise ConnectionError("传统 WiFi AP 登录失败：未读取到用户视图提示符")
        self._client = client
        self._execute("screen-length 0 temporary", self._ap.ap_flag)
        log.info("传统 WiFi AP Telnet 登录成功：%s", self._ap.ap_ip)

    def _execute(self, command: str, expected_prompt: str) -> str:
        if self._client is None:
            raise RuntimeError("传统 WiFi AP 未登录")
        self._client.write_line(command)
        chunks = []
        text = ""
        for _ in range(_MAX_CONFIRMATIONS + 1):
            output = self._client.read_until_any(
                (expected_prompt, *_CONFIRMATION_MARKERS), timeout_sec=20
            )
            chunks.append(output)
            text = b"".join(chunks).decode(
                self._client.encoding, errors=self._client.errors
            )
            output_text = output.decode(
                self._client.encoding, errors=self._client.errors
            )
            if expected_prompt in output_text:
                follow_up = self._client.read_until_any(
                    _CONFIRMATION_MARKERS,
                    timeout_sec=_CONFIRMATION_SETTLE_SEC,
                )
                if not follow_up:
                    break
                chunks.append(follow_up)
                text = b"".join(chunks).decode(
                    self._client.encoding, errors=self._client.errors
                )
                output_text = follow_up.decode(
                    self._client.encoding, errors=self._client.errors
                )
            if not any(marker in output_text for marker in _CONFIRMATION_MARKERS):
                break
            self._client.write_line("Y")
        if expected_prompt not in text:
            raise TimeoutError(
                f"命令未返回预期提示符 {expected_prompt!r}: {command!r}\n{text}"
            )
        if "Error:" in text:
            raise RuntimeError(f"传统 WiFi AP 命令失败: {command!r}\n{text}")
        return text

    def _run(self, commands: Sequence[Command]) -> str:
        self.login()
        output = ""
        for command, prompt in commands:
            output = self._execute(command, prompt)
        return output

    def _run_encoded(self, commands: Sequence[Command], encoding: str) -> str:
        target_encoding = codecs.lookup(encoding or "utf-8").name
        self.login()
        if self._client is None:
            raise RuntimeError("传统 WiFi AP 未登录")
        previous_encoding = self._client.encoding
        self._client.encoding = target_encoding
        try:
            return self._run(commands)
        finally:
            self._client.encoding = previous_encoding

    def _wlan_commands(self) -> list[Command]:
        return [
            ("system-view", f"[{self._sysname}]"),
            ("wlan", f"[{self._sysname}-wlan-view]"),
        ]

    def set_ssid(
        self,
        profile_name: str,
        ssid: str,
        *,
        hidden: bool = False,
        encoding: str = "utf-8",
    ) -> None:
        profile = self._safe_name(profile_name, "SSID profile")
        target_ssid = self._safe_value(ssid, "SSID")
        prompt = f"[{self._sysname}-wlan-ssid-prof-{profile}]"
        commands = self._wlan_commands() + [
            (f"ssid-profile name {profile}", prompt),
            (f"ssid {target_ssid}", prompt),
        ]
        # 复用同一 SSID profile，必须显式清除上一用例遗留的隐藏状态。
        commands.append(("ssid-hide enable" if hidden else "undo ssid-hide enable", prompt))
        commands.append(("return", self._ap.ap_flag))
        self._run_encoded(commands, encoding)

    def set_security(
        self,
        profile_name: str,
        security: str,
        *,
        password: str = "",
    ) -> None:
        profile = self._safe_name(profile_name, "Security profile")
        key = (security or "").strip().lower()
        if key not in SECURITY_PROFILES:
            raise ValueError(f"不支持的传统 WiFi AP 加密方式: {security!r}")
        spec = SECURITY_PROFILES[key]
        secret = self._safe_value(password, "WiFi 密码", allow_empty=True)
        prompt = f"[{self._sysname}-wlan-sec-prof-{profile}]"
        commands = self._wlan_commands() + [(f"security-profile name {profile}", prompt)]
        if not spec.pmf:
            commands.append(("undo pmf", prompt))

        if spec.mode == "open":
            security_command = "security open"
        elif spec.mode.startswith("wep-"):
            if not secret:
                raise ValueError(f"{security} 需要 WEP 密钥")
            security_command = "security wep"
            commands.append((security_command, prompt))
            commands.append((f"wep key 0 {spec.mode} pass-phrase {secret}", prompt))
            security_command = ""
        elif spec.mode == "wpa3":
            security_command = f"security wpa3 sae pass-phrase {secret} aes"
        elif spec.mode == "wpa2-wpa3":
            security_command = f"security wpa2-wpa3 psk-sae pass-phrase {secret} aes"
        elif spec.mode == "enhanced-open":
            security_command = "security enhanced-open aes"
        elif spec.mode == "wapi":
            security_command = f"security wapi psk pass-phrase {secret}"
        else:
            security_command = (
                f"security {spec.mode} psk pass-phrase {secret} {spec.cipher}"
            )

        if spec.mode not in ("open", "enhanced-open") and not secret:
            raise ValueError(f"{security} 需要 WiFi 密码")
        if security_command:
            commands.append((security_command, prompt))
        if spec.pmf:
            commands.append((f"pmf {spec.pmf}", prompt))
        commands.append(("return", self._ap.ap_flag))
        self._run(commands)

    def bind_vap(
        self,
        vap_profile: str,
        *,
        ssid_profile: str,
        security_profile: str,
        service_vlan: int = 3,
        forward_mode: Optional[str] = None,
    ) -> None:
        vap = self._safe_name(vap_profile, "VAP profile")
        ssid = self._safe_name(ssid_profile, "SSID profile")
        security = self._safe_name(security_profile, "Security profile")
        if int(service_vlan) <= 0 or int(service_vlan) > 4094:
            raise ValueError(f"service_vlan 超出范围: {service_vlan!r}")
        mode = (forward_mode or "").strip().lower()
        if mode not in ("", "direct-forward", "tunnel"):
            raise ValueError(f"forward_mode 必须为 direct-forward 或 tunnel: {forward_mode!r}")
        prompt = f"[{self._sysname}-wlan-vap-prof-{vap}]"
        profile_commands = [(f"vap-profile name {vap}", prompt)]
        if mode:
            profile_commands.append((f"forward-mode {mode}", prompt))
        self._run(
            self._wlan_commands()
            + profile_commands
            + [
                (f"service-vlan vlan-id {int(service_vlan)}", prompt),
                (f"ssid-profile {ssid}", prompt),
                (f"security-profile {security}", prompt),
                ("return", self._ap.ap_flag),
            ]
        )

    def attach_vap_to_radio(
        self,
        vap_profile: str,
        band: str,
        *,
        ap_id: Optional[int] = None,
        wlan_id: Optional[int] = None,
    ) -> None:
        vap = self._safe_name(vap_profile, "VAP profile")
        target_band = (band or "").strip().lower()
        if target_band not in RADIO_BY_BAND:
            raise ValueError(f"band 必须为 2g 或 5g: {band!r}")
        target_ap_id = _resolve_ap_id(ap_id, self._ap.ap_id)
        target_wlan_id = int(wlan_id or self._ap.wlan_id)
        if target_wlan_id <= 0 or target_wlan_id > 16:
            raise ValueError(f"wlan_id 超出范围 1~16: {target_wlan_id!r}")
        radio = RADIO_BY_BAND[target_band]
        ap_prompt = f"[{self._sysname}-wlan-ap-{target_ap_id}]"
        radio_prompt = f"[{self._sysname}-wlan-radio-{target_ap_id}/{radio}]"
        self._run(
            self._wlan_commands()
            + [
                (f"ap-id {target_ap_id}", ap_prompt),
                (f"radio {radio}", radio_prompt),
                (f"vap-profile {vap} wlan {target_wlan_id}", radio_prompt),
                ("return", self._ap.ap_flag),
            ]
        )

    def detach_vap_from_radio(
        self,
        vap_profile: str,
        band: str,
        *,
        ap_id: Optional[int] = None,
        wlan_id: Optional[int] = None,
    ) -> None:
        vap = self._safe_name(vap_profile, "VAP profile")
        target_band = (band or "").strip().lower()
        if target_band not in RADIO_BY_BAND:
            raise ValueError(f"band 必须为 2g 或 5g: {band!r}")
        target_ap_id = _resolve_ap_id(ap_id, self._ap.ap_id)
        target_wlan_id = int(wlan_id or self._ap.wlan_id)
        radio = RADIO_BY_BAND[target_band]
        ap_prompt = f"[{self._sysname}-wlan-ap-{target_ap_id}]"
        radio_prompt = f"[{self._sysname}-wlan-radio-{target_ap_id}/{radio}]"
        self._run(
            self._wlan_commands()
            + [
                (f"ap-id {target_ap_id}", ap_prompt),
                (f"radio {radio}", radio_prompt),
                (f"undo vap-profile {vap} wlan {target_wlan_id}", radio_prompt),
                ("return", self._ap.ap_flag),
            ]
        )

    @staticmethod
    def _vap_is_online(
        output: str,
        *,
        ap_id: int,
        radio: int,
        ssid: str,
    ) -> bool:
        for line in output.splitlines():
            fields = line.split()
            if (
                len(fields) >= 7
                and fields[0] == str(ap_id)
                and fields[2] == str(radio)
                and fields[5].upper() == "ON"
                and line.rstrip().endswith(ssid)
            ):
                return True
        return False

    def wait_for_vap_online(
        self,
        ssid: str,
        band: str,
        *,
        encoding: str = "utf-8",
        attempts: int = 10,
        interval_sec: float = 2.0,
    ) -> None:
        target_band = (band or "").strip().lower()
        if target_band not in RADIO_BY_BAND:
            raise ValueError(f"band 必须为 2g 或 5g: {band!r}")
        target_ap_id = _resolve_ap_id(None, self._ap.ap_id)
        target_radio = RADIO_BY_BAND[target_band]
        total_attempts = max(1, int(attempts))
        for attempt in range(1, total_attempts + 1):
            output = self._run_encoded(
                [("display vap all", self._ap.ap_flag)], encoding
            )
            if self._vap_is_online(
                output,
                ap_id=target_ap_id,
                radio=target_radio,
                ssid=ssid,
            ):
                log.info(
                    "传统 WiFi AP VAP 已上线：ap_id=%s band=%s ssid=%r attempt=%s",
                    target_ap_id,
                    target_band,
                    ssid,
                    attempt,
                )
                return
            if attempt < total_attempts and interval_sec > 0:
                time.sleep(interval_sec)
        raise RuntimeError(
            "传统 WiFi AP VAP 未在等待时间内上线："
            f"ap_id={target_ap_id} band={target_band} ssid={ssid!r}"
        )

    @staticmethod
    def _resolve_bands(band: str) -> tuple[str, ...]:
        """band 支持 2g / 5g / both（双频合一，同一 SSID 同时挂两个射频）。"""
        value = (band or "").strip().lower()
        if value in ("both", "dual", "2g+5g"):
            return ("2g", "5g")
        if value in RADIO_BY_BAND:
            return (value,)
        raise ValueError(f"band 必须为 2g、5g 或 both: {band!r}")

    def configure_wifi(
        self,
        *,
        ssid: str,
        password: str,
        security: str,
        band: str,
        hidden: bool = False,
        ssid_encoding: str = "utf-8",
        verify: bool = False,
    ) -> None:
        base = self._safe_name(self._ap.vap_profile, "VAP profile")
        ssid_profile = f"{base}-SSID"
        security_profile = f"{base}-Security"
        self.set_ssid(
            ssid_profile,
            ssid,
            hidden=hidden,
            encoding=ssid_encoding,
        )
        self.set_security(security_profile, security, password=password)
        self.bind_vap(
            base,
            ssid_profile=ssid_profile,
            security_profile=security_profile,
            service_vlan=self._ap.service_vlan,
        )
        target_bands = self._resolve_bands(band)
        for other in ("2g", "5g"):
            if other not in target_bands:
                self.detach_vap_from_radio(base, other)
        for target in target_bands:
            self.attach_vap_to_radio(base, target)
        if verify:
            for target in target_bands:
                self.wait_for_vap_online(ssid, target, encoding=ssid_encoding)

    def teardown_wifi(self) -> None:
        """Stop broadcasting the automation VAP by detaching it from both radios."""
        base = self._safe_name(self._ap.vap_profile, "VAP profile")
        for band in ("2g", "5g"):
            self.detach_vap_from_radio(base, band)
        log.info("传统 WiFi AP 自动化 VAP 已下线：vap_profile=%s", base)

    def save_configuration(self) -> None:
        """Persist the current AC configuration across restarts."""
        self.login()
        self._execute("save", self._ap.ap_flag)
        log.info("传统 WiFi AP 配置已保存")

    def set_channel(
        self,
        band: str,
        channel: int,
        *,
        bandwidth_mhz: int = 20,
        ap_id: Optional[int] = None,
        verify: bool = False,
    ) -> None:
        target_band = (band or "").strip().lower()
        if target_band not in RADIO_BY_BAND:
            raise ValueError(f"band 必须为 2g 或 5g: {band!r}")
        target_channel = int(channel)
        if bandwidth_mhz == 20 and target_channel not in CHANNELS_20MHZ[target_band]:
            raise ValueError(
                f"当前设备 {target_band} 20MHz 不支持信道 {target_channel}: "
                f"{CHANNELS_20MHZ[target_band]}"
            )
        if bandwidth_mhz not in (20, 80, 160, 320):
            raise ValueError("bandwidth_mhz 支持 20/80/160/320；40MHz 需明确 plus/minus")
        radio = RADIO_BY_BAND[target_band]
        bandwidth = f"{int(bandwidth_mhz)}mhz"
        target_ap_id = _resolve_ap_id(ap_id, self._ap.ap_id)
        ap_prompt = f"[{self._sysname}-wlan-ap-{target_ap_id}]"
        radio_prompt = f"[{self._sysname}-wlan-radio-{target_ap_id}/{radio}]"
        channel_command = f"channel {bandwidth} {target_channel}"
        self._run(
            self._wlan_commands()
            + [
                (f"ap-id {target_ap_id}", ap_prompt),
                (f"radio {radio}", radio_prompt),
                ("calibrate auto-channel-select disable", radio_prompt),
                ("calibrate auto-bandwidth-select disable", radio_prompt),
            ]
        )
        if self._client is None:
            raise RuntimeError("传统 WiFi AP 未登录")
        confirmation = "Continue?[Y/N]"
        self._client.write_line(channel_command)
        output = self._client.read_until(confirmation, timeout_sec=20)
        text = output.decode(self._client.encoding, errors=self._client.errors)
        if "Error:" in text:
            raise RuntimeError(f"传统 WiFi AP 命令失败: {channel_command!r}\n{text}")
        if confirmation in text:
            self._client.write_line("Y")
            output = self._client.read_until(radio_prompt, timeout_sec=20)
            text = output.decode(self._client.encoding, errors=self._client.errors)
        if radio_prompt not in text:
            self.close()
        else:
            self._execute("return", self._ap.ap_flag)
        if verify:
            self.verify_channel(
                target_band,
                target_channel,
                ap_id=target_ap_id,
            )

    def current_channel(self, band: str, *, ap_id: Optional[int] = None) -> int:
        target_band = (band or "").strip().lower()
        if target_band not in RADIO_BY_BAND:
            raise ValueError(f"band 必须为 2g 或 5g: {band!r}")
        target_ap_id = _resolve_ap_id(ap_id, self._ap.ap_id)
        target_radio = RADIO_BY_BAND[target_band]
        output = self._run([("display radio all", self._ap.ap_flag)])
        for line in output.splitlines():
            fields = line.split()
            if len(fields) < 7 or not fields[0].isdigit():
                continue
            if int(fields[0]) == target_ap_id and int(fields[2]) == target_radio:
                return int(fields[6].split("/", 1)[0])
        raise RuntimeError(
            f"未找到 AP {target_ap_id} 的 {target_band} radio 运行状态"
        )

    def verify_channel(
        self,
        band: str,
        channel: int,
        *,
        ap_id: Optional[int] = None,
        attempts: int = 5,
        interval_sec: float = 2.0,
    ) -> None:
        last_channel: Optional[int] = None
        last_error: Optional[Exception] = None
        for attempt in range(1, attempts + 1):
            try:
                self.close()
                last_channel = self.current_channel(band, ap_id=ap_id)
                if last_channel == int(channel):
                    return
            except (ConnectionError, OSError, RuntimeError, TimeoutError) as exc:
                last_error = exc
            if attempt < attempts:
                time.sleep(interval_sec)
        detail = f"实际信道={last_channel}" if last_channel is not None else str(last_error)
        raise RuntimeError(
            f"传统 WiFi AP 信道切换校验失败: band={band} 预期={channel}，{detail}"
        )

    def display_ap_all(self) -> str:
        return self._run([("display ap all", self._ap.ap_flag)])
