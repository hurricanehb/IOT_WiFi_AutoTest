"""全局 Fixture：设备、ADB、WiFi、AI；路径与 .env。"""
from __future__ import annotations

import re
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.utils.stdio_utf8 import ensure_utf8_stdio  # noqa: E402

ensure_utf8_stdio()

import pytest  # noqa: E402

from core.utils.config_loader import (  # noqa: E402
    android_data_path,
    get_settings,
    load_env_file,
)

load_env_file()

from core.utils.adb_helper import AdbHelper  # noqa: E402
from core.utils.data_parser import load_yaml  # noqa: E402
from core.utils.log_handler import get_logger  # noqa: E402
from core.libs.android.wifi_control.controller import WiFiControl  # noqa: E402
from core.libs.android.settings_pages.add_network_page import WiFiAddNetworkUI  # noqa: E402
from core.libs.android.settings_pages.ip_settings_page import WiFiIPSettingsUI  # noqa: E402
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI  # noqa: E402
from core.libs.access_points import WiFiAPAction, MiniAPAction  # noqa: E402
from core.utils.attenuator import (  # noqa: E402
    ConfiguredAttenuatorRig,
    HJRadioRack,
)
from core.utils.device_mgr import DeviceManager  # noqa: E402
from core.utils.device_log_export import export_device_packlogs  # noqa: E402
from core.utils.failure_diagnostics import (  # noqa: E402
    capture_failure_diagnostics,
    failure_signature,
)
from core.utils.report_utils import log_report_dir  # noqa: E402
from testcases.support.case_api import (  # noqa: E402
    wifi_case_description,
    wifi_case_from_markers,
)

log = get_logger("conftest")

# pytest.ini 仅注册小写 marker；`-m` 表达式中的名称不区分大小写
_CANONICAL_MARKERS = (
    "wifi",
    "hyperwifi",
    "common",
    "p0",
    "p1",
    "p2",
    "p3",
    "country_code",
    "regression",
    "stress",
    "weaknet",
    "ai",
    "smoke",
    "miniap",
    "no_wifi_lifecycle",
    "no_dual_wifi_setup",
    "dual_wifi_eu",
    "dual_wifi_us",
)


def _normalize_markexpr(expr: str) -> str:
    out = expr
    for name in sorted(_CANONICAL_MARKERS, key=len, reverse=True):
        out = re.sub(rf"\b{re.escape(name)}\b", name, out, flags=re.IGNORECASE)
    return out


def _configure_report_paths(config) -> None:
    """报告写入 reports/<YYYY-MM-DD>/<HH-MM-SS>/（html、log、allure）。"""
    from core.utils.report_utils import (
        allure_results_dir,
        ensure_report_subdirs,
        html_report_path,
        init_report_run_dir,
        report_run_dir,
    )

    init_report_run_dir()
    run_dir = ensure_report_subdirs()
    config._report_run_dir = run_dir  # type: ignore[attr-defined]

    # pytest-html：未指定 --html 时写入当日目录
    if config.pluginmanager.hasplugin("html"):
        htmlpath = getattr(config.option, "htmlpath", None)
        if not htmlpath:
            path = html_report_path()
            config.option.htmlpath = str(path)
            setattr(config.option, "self_contained_html", True)

    # Allure：未指定 --alluredir 时写入当日目录（需安装 allure-pytest）
    if config.pluginmanager.hasplugin("allure_pytest"):
        alluredir = getattr(config.option, "allure_report_dir", None)
        if not alluredir:
            config.option.allure_report_dir = str(allure_results_dir("raw"))

    log.info("测试报告目录：%s", report_run_dir())

    # pytest 日志文件与 automation.log 同目录（UTF-8）
    if config.pluginmanager.hasplugin("logging-plugin"):
        plugin = config.pluginmanager.get_plugin("logging-plugin")
        if plugin is not None and hasattr(plugin, "set_log_path"):
            plugin.set_log_path(str(report_run_dir() / "pytest.log"))


def pytest_sessionfinish(session, exitstatus) -> None:
    """Windows 上 pytest-html 可能按系统编码写文件，强制以 UTF-8 落盘。"""
    htmlpath = getattr(session.config.option, "htmlpath", None)
    if not htmlpath:
        return
    path = Path(htmlpath)
    if not path.is_file():
        return
    data = path.read_bytes()
    text = None
    for enc in ("utf-8", "gbk", "cp936"):
        try:
            candidate = data.decode(enc)
        except UnicodeDecodeError:
            continue
        text = candidate
        if enc == "utf-8":
            break
        if "前置" in candidate or "已联网" in candidate:
            break
    if text is None:
        text = data.decode("utf-8", errors="replace")
    path.write_text(text, encoding="utf-8")


def pytest_configure(config) -> None:
    ensure_utf8_stdio()
    _configure_report_paths(config)
    config._failure_diagnostic_signatures = set()  # type: ignore[attr-defined]
    config._failure_packlogs_exported = False  # type: ignore[attr-defined]

    expr = getattr(config.option, "markexpr", "") or ""
    if not expr:
        return
    normalized = _normalize_markexpr(expr)
    if normalized != expr:
        config.option.markexpr = normalized
        log.debug("markexpr normalized: %r -> %r", expr, normalized)


def pytest_collection_modifyitems(items) -> None:
    for item in items:
        marker = item.get_closest_marker("wifi_case")
        if marker is None:
            continue
        case_id_marker = item.get_closest_marker("case_id")
        try:
            case = wifi_case_from_markers(marker, case_id_marker)
        except ValueError as error:
            raise pytest.UsageError(f"{item.nodeid}: {error}") from error
        item.obj.__doc__ = wifi_case_description(case)


def _case_log_name(item) -> str:
    marker = item.get_closest_marker("case_id")
    if marker is not None and marker.args:
        return str(marker.args[0])
    return item.name


def _report_reason(report) -> str:
    detail = getattr(report, "longreprtext", "") or str(report.longrepr or "")
    lines = [line.strip() for line in detail.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _env_enabled(name: str, default: bool = True) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() not in ("0", "false", "no", "off")


def _failure_diagnostic_limit() -> int:
    try:
        return max(0, int(os.environ.get("FAILURE_DIAGNOSTICS_MAX_TYPES", "10")))
    except ValueError:
        return 10


def _attach_failure_artifacts(paths: list[Path]) -> None:
    try:
        import allure

        attachment_types = {
            ".png": allure.attachment_type.PNG,
            ".xml": allure.attachment_type.XML,
            ".txt": allure.attachment_type.TEXT,
        }
        for path in paths:
            allure.attach.file(
                str(path),
                name=f"failure diagnostics - {path.name}",
                attachment_type=attachment_types.get(
                    path.suffix.lower(), allure.attachment_type.TEXT
                ),
            )
    except Exception as error:
        log.warning("失败诊断附加到 Allure 失败：%r", error)


def _capture_failed_report(item, report) -> None:
    if not report.failed or report.when not in ("setup", "call", "teardown"):
        return
    if not _env_enabled("FAILURE_DIAGNOSTICS"):
        return
    if not ({"adb", "settings_ui"} & set(getattr(item, "fixturenames", ()))):
        return
    if getattr(item, "_failure_diagnostics_captured", False):
        return

    reason = _report_reason(report)
    signature = failure_signature(report.when, reason)
    signatures = item.config._failure_diagnostic_signatures
    if signature in signatures or len(signatures) >= _failure_diagnostic_limit():
        return
    signatures.add(signature)
    item._failure_diagnostics_captured = True

    adb_instance = item.funcargs.get("adb")
    try:
        artifacts = capture_failure_diagnostics(
            adb_instance,
            label=_case_log_name(item),
            phase=report.when,
            reason=reason,
            settings_ui=item.funcargs.get("settings_ui"),
        )
        _attach_failure_artifacts(artifacts)
    except Exception as error:
        log.warning("失败诊断采集异常：%r", error)

    packlogs_dir = log_report_dir() / "device_packlogs"
    existing_packlogs = packlogs_dir.is_dir() and any(packlogs_dir.iterdir())
    should_export_packlogs = (
        _env_enabled("FAILURE_PACKLOGS")
        and report.when == "call"
        and "前置条件失败" not in reason
        and adb_instance is not None
        and not item.config._failure_packlogs_exported
        and not existing_packlogs
    )
    if should_export_packlogs:
        item.config._failure_packlogs_exported = True
        try:
            export_device_packlogs(
                adb_instance,
                reason=reason,
                label=_case_log_name(item),
            )
        except Exception as error:
            log.warning("失败后导出设备 packlogs 异常：%r", error)


def _summarize_case_reports(reports) -> tuple[str, float, str]:
    ordered_reports = [
        reports[phase]
        for phase in ("setup", "call", "teardown")
        if phase in reports
    ]
    decisive_report = next(
        (phase_report for phase_report in ordered_reports if phase_report.failed),
        None,
    )
    if decisive_report is None:
        decisive_report = next(
            (phase_report for phase_report in ordered_reports if phase_report.skipped),
            None,
        )
    status = (
        "FAILED"
        if decisive_report and decisive_report.failed
        else "SKIPPED" if decisive_report else "PASSED"
    )
    duration = sum(phase_report.duration for phase_report in ordered_reports)
    reason = _report_reason(decisive_report) if decisive_report else ""
    return status, duration, reason


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item) -> None:
    item._automation_phase_reports = {}
    log.info("用例开始：%s | nodeid=%s", _case_log_name(item), item.nodeid)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    _capture_failed_report(item, report)
    reports = getattr(item, "_automation_phase_reports", {})
    reports[report.when] = report
    item._automation_phase_reports = reports
    if report.when != "teardown":
        return

    status, duration, reason = _summarize_case_reports(reports)
    suffix = f" | 原因={reason}" if reason else ""
    log.info("用例结束：%s | 状态=%s | 耗时=%.2fs%s", _case_log_name(item), status, duration, suffix)


@pytest.fixture
def wifi_case(request) -> dict[str, str]:
    return wifi_case_from_markers(
        request.node.get_closest_marker("wifi_case"),
        request.node.get_closest_marker("case_id"),
    )


@pytest.fixture(scope="session")
def device_serial() -> str:
    dm = DeviceManager()
    try:
        return dm.require_serial()
    except RuntimeError as e:
        pytest.skip(str(e))


@pytest.fixture(scope="session")
def adb(device_serial: str) -> AdbHelper:
    a = AdbHelper(serial=device_serial)
    if not a.wait_for_device():
        pytest.skip("ADB device not ready in time")
    if os.environ.get("ADB_REQUIRE_ROOT", "1").strip().lower() not in ("0", "false", "no"):
        if not a.ensure_root():
            pytest.skip(
                "ADB 非 root：请使用 userdebug/eng 设备并执行 adb root，"
                "或设置 ADB_REQUIRE_ROOT=0 跳过该校验"
            )
    return a


@pytest.fixture(scope="function")
def wifi(adb: AdbHelper) -> WiFiControl:
    return WiFiControl(adb)


@pytest.fixture(scope="function")
def settings_ui(device_serial: str, tmp_path: Path, request) -> AndroidSettingsUI:
    preserved_modules = {
        "wlan_components_welcome",
        "wlan_hotspot",
        "wlan_advanced_settings",
    }
    preserved_case = request.node.path.parent.name in preserved_modules
    if not preserved_case:
        request.getfixturevalue("adb")
    settings = AndroidSettingsUI(device_serial, tmp_path / "settings-ui")
    if not preserved_case:
        settings.prepare()
    return settings


@pytest.fixture(scope="function")
def wifi_ip_settings_ui(settings_ui: AndroidSettingsUI) -> WiFiIPSettingsUI:
    return WiFiIPSettingsUI(settings_ui)


@pytest.fixture(scope="function")
def wifi_add_network_ui(settings_ui: AndroidSettingsUI) -> WiFiAddNetworkUI:
    return WiFiAddNetworkUI(settings_ui)


@pytest.fixture(scope="session")
def wifi_yaml() -> dict:
    return load_yaml(android_data_path("wifi_ssid.yaml"))


@pytest.fixture(scope="session")
def weaknet_yaml() -> dict:
    return load_yaml(android_data_path("weaknet_scene.yaml"))


@pytest.fixture
def miniap_action_optional():
    """miniAP Telnet；未配置 miniAP IP 或密码时返回 None（不 skip）。"""
    settings = get_settings()
    cfg = settings.miniAP_config
    if not (cfg.miniAP_ip or "").strip() or not (cfg.miniAP_login_password or "").strip():
        yield None
        return
    action = MiniAPAction(settings=settings)
    yield action
    action.close()


@pytest.fixture
def attenuator_optional():
    """可调衰减器；未配置地址时返回 None，配置后负责连接和关闭。"""
    settings = get_settings()
    cfg = settings.attenuator_device
    if not cfg.host.strip():
        yield None
        return
    attenuator = HJRadioRack(
        host=cfg.host,
        port=cfg.port,
        timeout_sec=cfg.timeout_sec,
        max_attenuation_db=cfg.max_attenuation_db,
    )
    rig = ConfiguredAttenuatorRig(attenuator, settings.attenuator_channels)
    try:
        attenuator.connect()
    except OSError as exc:
        pytest.skip(f"可调衰减器 {cfg.host}:{cfg.port} 不可连接: {exc}")
    try:
        yield rig
    finally:
        attenuator.close()


@pytest.fixture(scope="session")
def wifi_ap_session_cleanup():
    """会话结束后把自动化 VAP 从两个射频上摘除，避免测试 SSID 残留广播。"""
    state = {"configured": False}
    yield state
    if not state["configured"]:
        return
    action = WiFiAPAction(settings=get_settings())
    try:
        action.teardown_wifi()
    except Exception as exc:  # AP 清理失败不应让整个会话报错
        log.warning("会话结束：自动化 VAP 下线失败：%s", exc)
    finally:
        action.close()


@pytest.fixture
def wifi_ap_action_optional(wifi_ap_session_cleanup):
    """传统 WiFi AP Telnet；未配置 AP IP 或密码时返回 None。"""
    settings = get_settings()
    ap = settings.ap_config
    if not (ap.ap_ip or "").strip() or not (ap.ap_login_password or "").strip():
        yield None
        return
    action = WiFiAPAction(settings=settings)
    wifi_ap_session_cleanup["configured"] = True
    yield action
    action.close()


@pytest.fixture
def ai_enabled() -> bool:
    return bool((os.environ.get("PYAT_AI_API_KEY") or "").strip())


@pytest.fixture
def run_shell_cmd(adb: AdbHelper):
    """执行 adb shell 命令并返回合并后的文本输出（供用例 Step 调用）。"""

    def _run(cmd: str, timeout_sec: float | None = None) -> str:
        cmd = (cmd or "").strip()
        if not cmd:
            return ""
        code, out, err = adb.shell_line(cmd, timeout_sec=timeout_sec)
        text = (out or "") + (("\n" + err) if err else "")
        if code != 0:
            log.warning("shell 命令返回非零 rc=%s: %s", code, cmd)
        return text

    return _run
