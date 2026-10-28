"""加载 .env、JSON 配置与 YAML；暴露 Settings。"""
from __future__ import annotations

import json
import os
import warnings
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from core.utils.attenuator import (
    AttenuatorChannelMap,
    AttenuatorDeviceConfig,
)

ROOT = Path(__file__).resolve().parent.parent.parent


def _env(name: str, default: str = "") -> str:
    v = os.environ.get(name)
    return (v or default).strip()


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except ValueError:
        return default


def _config_positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _secret(env_name: str, raw: Any) -> str:
    """凭据优先从环境变量读取；JSON 回退仅供本地过渡，不应提交明文。"""
    return _env(env_name) or ("" if raw is None else str(raw).strip())


class _ConfigSection:
    """按「环境变量 > JSON 节 > 代码默认值」取值，报错时标明来源。"""

    def __init__(self, name: str, data: Any) -> None:
        self._name = name
        self._data = data if isinstance(data, dict) else {}

    def _resolve(self, key: str, env_name: str) -> tuple[str, str]:
        env_value = _env(env_name)
        if env_value:
            return env_name, env_value
        raw = self._data.get(key)
        return f"{self._name}.{key}", "" if raw is None else str(raw).strip()

    def text(self, key: str, env_name: str, default: str = "") -> str:
        _, value = self._resolve(key, env_name)
        return value or default

    def positive_int(self, key: str, env_name: str, default: int) -> int:
        source, value = self._resolve(key, env_name)
        if not value:
            return default
        try:
            parsed = int(value)
        except ValueError:
            raise ValueError(f"{source} 必须是整数，实际值: {value!r}") from None
        if parsed < 1:
            warnings.warn(f"{source}={parsed} 小于下限 1，已按 1 处理", stacklevel=2)
            return 1
        return parsed

    def non_negative_int(self, key: str, env_name: str, default: int) -> int:
        """用于以 0 起编号的标识（如华为 AC 的 ap-id）。"""
        source, value = self._resolve(key, env_name)
        if not value:
            return default
        try:
            parsed = int(value)
        except ValueError:
            raise ValueError(f"{source} 必须是整数，实际值: {value!r}") from None
        if parsed < 0:
            warnings.warn(f"{source}={parsed} 小于下限 0，已按 0 处理", stacklevel=2)
            return 0
        return parsed

    def number(self, key: str, env_name: str, default: float, *, minimum: float = 0.0) -> float:
        source, value = self._resolve(key, env_name)
        if not value:
            return default
        try:
            parsed = float(value)
        except ValueError:
            raise ValueError(f"{source} 必须是数值，实际值: {value!r}") from None
        if parsed < minimum:
            warnings.warn(
                f"{source}={parsed} 小于下限 {minimum}，已按 {minimum} 处理", stacklevel=2
            )
            return minimum
        return parsed


def _read_json(path: Path) -> Any:
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f) or {}


@dataclass
class APConfig:
    ap_ip: str = ""
    ap_login_username: str = ""
    ap_login_password: str = ""
    ap_flag: str = ""
    ap_id: int = 1
    vap_profile: str = "PyAutoTest"
    service_vlan: int = 3
    wlan_id: int = 8


@dataclass
class MiniAPConfig:
    miniAP_ip: str = ""
    miniAP2_ip: str = ""
    miniAP_root: str = ""
    miniAP_login_password: str = ""
    miniAP_flag: str = ""


@dataclass
class DUTInfo:
    eth_ip: str = ""
    serial_A: str = ""
    serial_B: str = ""


@dataclass
class PerformanceConfig:
    iperf_server: str = ""
    iperf_duration_sec: int = 10
    iperf_runs: int = 3
    iperf_parallel_streams: int = 1
    traditional_iperf_parallel_streams: int = 16
    iperf_protocols: str = "tcp,udp"
    udp_bandwidth: str = "100M"
    min_mbps: float = 1.0
    ping_host: str = ""
    ping_count: int = 20
    ping_big_size: int = 1200
    ping_small_size: int = 64


@dataclass
class ScenarioTuningConfig:
    """只影响耗时与稳定性的旋钮；改动不得改变用例判定结论。"""

    wifi_connect_wait_sec: float = 15.0
    wifi_stress_cycles: int = 5
    country_code_stress_cycles: int = 1000
    country_code_halow_ready_timeout_sec: float = 30.0


@dataclass
class Settings:
    android_serial: str = ""
    adb_timeout_sec: int = 30
    log_level: str = "INFO"
    log_dir: str = "reports/log"
    report_dir: str = "reports/html"
    screenshot_dir: str = "temp/screenshots"
    ap_config: APConfig = field(default_factory=APConfig)
    miniAP_config: MiniAPConfig = field(default_factory=MiniAPConfig)
    attenuator_device: AttenuatorDeviceConfig = field(
        default_factory=AttenuatorDeviceConfig
    )
    attenuator_channels: AttenuatorChannelMap = field(
        default_factory=AttenuatorChannelMap
    )
    dut_info: DUTInfo = field(default_factory=DUTInfo)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    scenario_tuning: ScenarioTuningConfig = field(default_factory=ScenarioTuningConfig)


def android_data_path(name: str) -> Path:
    return ROOT / "testdata" / "android" / name


def miniap_data_path(name: str) -> Path:
    return ROOT / "testdata" / "miniap" / name


def data_path(name: str) -> Path:
    """Return a file under the shared test-data root."""
    return ROOT / "testdata" / name


def load_env_file() -> None:
    """.env 的唯一加载入口；override=False 保证真实环境变量优先。"""
    load_dotenv(ROOT / ".env", override=False)


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    load_env_file()
    s = Settings(
        android_serial=_env("ANDROID_SERIAL"),
        adb_timeout_sec=_env_int("ADB_TIMEOUT_SEC", 30),
        log_level=_env("LOG_LEVEL", "INFO"),
        log_dir=_env("LOG_DIR", "reports/log"),
        report_dir=_env("REPORT_DIR", "reports/html"),
        screenshot_dir=_env("SCREENSHOT_DIR", "temp/screenshots"),
    )
    tc = _read_json(ROOT / "config" / "test_config.json")
    ap = _ConfigSection("ap_config", tc.get("ap_config"))
    mini_ap = _ConfigSection("miniAP_config", tc.get("miniAP_config"))
    attenuator = _ConfigSection("attenuator_device", tc.get("attenuator_device"))
    attenuator_channels = _ConfigSection(
        "attenuator_channels", tc.get("attenuator_channels")
    )
    dut = _ConfigSection("dut_info", tc.get("dut_info"))
    performance = _ConfigSection("performance", tc.get("performance"))
    scenario_tuning = _ConfigSection("scenario_tuning", tc.get("scenario_tuning"))

    s.ap_config = APConfig(
        ap_ip=ap.text("ap_ip", "AP_IP"),
        ap_login_username=ap.text("ap_login_username", "AP_LOGIN_USERNAME"),
        ap_login_password=_secret("AP_LOGIN_PASSWORD", ap.text("ap_login_password", "")),
        ap_flag=ap.text("ap_flag", "AP_FLAG"),
        ap_id=ap.non_negative_int("ap_id", "AP_ID", 1),
        vap_profile=ap.text("vap_profile", "AP_VAP_PROFILE", "PyAutoTest"),
        service_vlan=ap.positive_int("service_vlan", "AP_SERVICE_VLAN", 3),
        wlan_id=ap.positive_int("wlan_id", "AP_WLAN_ID", 8),
    )
    s.miniAP_config = MiniAPConfig(
        miniAP_ip=mini_ap.text("miniAP_ip", "MINIAP_IP"),
        miniAP2_ip=mini_ap.text("miniAP2_ip", "MINIAP2_IP"),
        miniAP_root=mini_ap.text("miniAP_root", "MINIAP_ROOT"),
        miniAP_login_password=_secret(
            "MINIAP_LOGIN_PASSWORD", mini_ap.text("miniAP_login_password", "")
        ),
        miniAP_flag=mini_ap.text("miniAP_flag", "MINIAP_FLAG"),
    )
    s.attenuator_device = AttenuatorDeviceConfig(
        host=attenuator.text("host", "ATTENUATOR_HOST"),
        port=attenuator.positive_int("port", "ATTENUATOR_PORT", 50000),
        timeout_sec=attenuator.number(
            "timeout_sec", "ATTENUATOR_TIMEOUT_SEC", 5.0, minimum=0.1
        ),
        max_attenuation_db=attenuator.number(
            "max_attenuation_db", "ATTENUATOR_MAX_DB", 122.0, minimum=1.0
        ),
    )
    s.attenuator_channels = AttenuatorChannelMap(
        mini_ap_1=attenuator_channels.positive_int(
            "mini_ap_1_channel", "ATTENUATOR_MINI_AP_1_CHANNEL", 13
        ),
        traditional_ap_1=attenuator_channels.positive_int(
            "traditional_ap_1_channel", "ATTENUATOR_TRADITIONAL_AP_1_CHANNEL", 14
        ),
        mini_ap_2=attenuator_channels.positive_int(
            "mini_ap_2_channel", "ATTENUATOR_MINI_AP_2_CHANNEL", 15
        ),
        traditional_ap_2=attenuator_channels.positive_int(
            "traditional_ap_2_channel", "ATTENUATOR_TRADITIONAL_AP_2_CHANNEL", 16
        ),
    )
    s.dut_info = DUTInfo(
        eth_ip=dut.text("eth_ip", "DUT_ETH_IP"),
        serial_A=dut.text("serial_A", "DUT_SERIAL_A"),
        serial_B=dut.text("serial_B", "DUT_SERIAL_B"),
    )
    s.performance = PerformanceConfig(
        iperf_server=performance.text("iperf_server", "PERF_IPERF_SERVER"),
        iperf_duration_sec=performance.positive_int(
            "iperf_duration_sec", "PERF_IPERF_DURATION_SEC", 10
        ),
        iperf_runs=performance.positive_int("iperf_runs", "PERF_IPERF_RUNS", 3),
        iperf_parallel_streams=performance.positive_int(
            "iperf_parallel_streams", "PERF_IPERF_PARALLEL_STREAMS", 1
        ),
        traditional_iperf_parallel_streams=performance.positive_int(
            "traditional_iperf_parallel_streams",
            "PERF_TRADITIONAL_IPERF_PARALLEL_STREAMS",
            16,
        ),
        iperf_protocols=performance.text(
            "iperf_protocols", "PERF_IPERF_PROTOCOLS", "tcp,udp"
        ),
        udp_bandwidth=performance.text("udp_bandwidth", "PERF_UDP_BW", "100M"),
        min_mbps=performance.number("min_mbps", "PERF_MIN_MBPS", 1.0),
        ping_host=performance.text("ping_host", "PERF_PING_HOST"),
        ping_count=performance.positive_int("ping_count", "PERF_PING_COUNT", 20),
        ping_big_size=performance.positive_int("ping_big_size", "PERF_PING_BIG_SIZE", 1200),
        ping_small_size=performance.positive_int(
            "ping_small_size", "PERF_PING_SMALL_SIZE", 64
        ),
    )
    s.scenario_tuning = ScenarioTuningConfig(
        wifi_connect_wait_sec=scenario_tuning.number(
            "wifi_connect_wait_sec", "WIFI_CONNECT_WAIT_SEC", 15.0, minimum=3.0
        ),
        wifi_stress_cycles=scenario_tuning.positive_int(
            "wifi_stress_cycles", "WIFI_STRESS_CYCLES", 5
        ),
        country_code_stress_cycles=scenario_tuning.positive_int(
            "country_code_stress_cycles", "CCODE_STRESS_CYCLES", 1000
        ),
        country_code_halow_ready_timeout_sec=scenario_tuning.number(
            "country_code_halow_ready_timeout_sec", "CCODE_HALOW_READY_TIMEOUT", 30.0,
            minimum=1.0,
        ),
    )

    android = tc.get("android") or {}
    serial = (android.get("serial") or "").strip()
    if serial and not s.android_serial:
        s.android_serial = serial
    at = tc.get("adb_timeout_sec")
    if at is not None and not _env("ADB_TIMEOUT_SEC"):
        try:
            s.adb_timeout_sec = int(at)
        except (TypeError, ValueError):
            pass
    return s


def reload_settings() -> Settings:
    """丢弃缓存并重新读取配置；仅在测试或运行期改了配置/环境变量时使用。"""
    get_settings.cache_clear()
    return get_settings()
