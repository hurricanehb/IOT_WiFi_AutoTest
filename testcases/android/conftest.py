"""Android 域：WiFi 前置/后置（见 android_wifi_lifecycle）。"""
from __future__ import annotations

import pytest

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.lab_requirements import env_value
from core.utils.log_handler import get_logger

log = get_logger("android.conftest")

# 命中任一 marker 且需要设备时启用生命周期（纯 YAML/AI 用例见 _yaml_only_fixtures）
_WIFI_DOMAIN_MARKERS = frozenset(
    {
        "wifi",
        "hyperwifi",
        "dualwifi",
        "stress",
        "weaknet",
    }
)

_DEVICE_FIXTURES = frozenset({"wifi", "run_shell_cmd", "adb"})
_YAML_ONLY_FIXTURES = frozenset(
    {
        "wifi_yaml",
        "weaknet_yaml",
        "ai_enabled",
        "tmp_path",
        "cycles",
    }
)

_WIFI_CAPABILITIES = frozenset({"wifi", "hyperwifi", "dualwifi"})


def _wifi_capability_skip_reason(node, capability: str) -> str | None:
    keywords = set(getattr(node, "keywords", {}))
    if "dualwifi" in keywords and capability != "dualwifi":
        return f"用例需要双链路能力，当前 DUT_WIFI_CAPABILITY={capability}"
    if "common" in keywords:
        return None
    if "wifi" in keywords and capability == "hyperwifi":
        return "用例需要传统 WiFi 能力，当前 DUT_WIFI_CAPABILITY=hyperwifi"
    if "hyperwifi" in keywords and capability == "wifi":
        return "用例需要 HyperWiFi 能力，当前 DUT_WIFI_CAPABILITY=wifi"
    return None


def pytest_collection_modifyitems(items) -> None:
    capability = env_value("DUT_WIFI_CAPABILITY", "dualwifi")
    if capability not in _WIFI_CAPABILITIES:
        choices = ", ".join(sorted(_WIFI_CAPABILITIES))
        raise pytest.UsageError(
            f"DUT_WIFI_CAPABILITY={capability!r} 无效，可选值：{choices}"
        )

    for item in items:
        reason = _wifi_capability_skip_reason(item, capability)
        if reason:
            item.add_marker(pytest.mark.skip(reason=reason))


def _has_wifi_domain_marker(node) -> bool:
    return bool(_WIFI_DOMAIN_MARKERS & set(getattr(node, "keywords", {})))


def _uses_device(node) -> bool:
    names = set(getattr(node, "fixturenames", ()) or ())
    return bool(names & _DEVICE_FIXTURES)


def _yaml_only_case(node) -> bool:
    names = set(getattr(node, "fixturenames", ()) or ())
    if not names:
        return False
    return names.issubset(_YAML_ONLY_FIXTURES)


def _apply_android_wifi_lifecycle(node) -> bool:
    if "no_wifi_lifecycle" in getattr(node, "keywords", {}):
        return False
    if not _uses_device(node):
        return False
    if _yaml_only_case(node):
        return False
    if _has_wifi_domain_marker(node) or "wifi" in set(getattr(node, "fixturenames", ()) or ()):
        return True
    return False


@pytest.fixture(autouse=True)
def android_wifi_lifecycle(request, adb) -> None:
    """
    前置：关闭 WiFi -> 清除已保存配置 -> 打开 WiFi（默认未连接起始）。
    后置：断开 WiFi -> 清除已保存配置 -> 还原初始 WiFi 开关状态。

    作用于 testcases/android 下使用 adb/wifi/run_shell_cmd 且带 WiFi 域 marker 的用例；
    纯 YAML/AI 数据用例不启用。用 @pytest.mark.no_wifi_lifecycle 可跳过。
    """
    def _return_home() -> None:
        adb.keyevent("KEYCODE_HOME")
        log.info("android_wifi_lifecycle: 后置 — 已返回 Home 页面")

    request.addfinalizer(_return_home)

    if not _apply_android_wifi_lifecycle(request.node):
        return

    wifi = WiFiControl(adb)
    initial_wifi_enabled = wifi.is_wifi_enabled()

    def _cleanup() -> None:
        log.info("android_wifi_lifecycle: 后置 — 断开 WiFi 并清理已保存配置")

        # 为保证 disconnect/forget 可执行，后置阶段先确保 WiFi 可操作。
        wifi.set_wifi_enabled(True)

        before = wifi.list_connected_ssids(trust_status_fallback=True)
        ok = wifi.disconnect_all(max_rounds=2, settle_sec=2.0, post_wait_sec=5.0)
        cleared = wifi.clear_saved_networks(max_rounds=2, settle_sec=0.3)

        if ok or wifi.is_disconnected():
            log.info(
                "后置完成：断开前=%r，清理保存网络=%r，当前无保存网络=%s",
                before or None,
                cleared or None,
                not wifi.has_saved_networks(),
            )
        else:
            after = wifi.list_connected_ssids(trust_status_fallback=True)
            log.warning(
                "后置断开未完全生效：断开前=%r，当前=%r，清理保存网络=%r，list-networks:\n%s",
                before or None,
                after or None,
                cleared or None,
                wifi.list_networks_blob()[:300],
            )

        if wifi.set_wifi_enabled(initial_wifi_enabled):
            log.info("后置还原 WiFi 开关状态：%s", "ON" if initial_wifi_enabled else "OFF")
        else:
            log.warning("后置还原 WiFi 开关状态失败，目标=%s", initial_wifi_enabled)

    # Finalizers run in reverse registration order: clean WiFi first, then show Home.
    request.addfinalizer(_cleanup)

    # # 仅在当前 WiFi 状态不符时才切换，减少多余操作
    # log.info("android_wifi_lifecycle: 前置 — 检查并关闭 WiFi（如已开启）")
    # if wifi.is_wifi_enabled():
    #     if not wifi.set_wifi_enabled(False):
    #         pytest.fail("前置条件失败：无法关闭 WiFi 开关")

    # cleared = wifi.clear_saved_networks(max_rounds=2, settle_sec=0.3)
    # log.info("android_wifi_lifecycle: 前置 — 清理已保存网络: %r", cleared or None)

    log.info("android_wifi_lifecycle: 前置 — 检查并打开 WiFi 开关")
    if not wifi.is_wifi_enabled():
        if not wifi.set_wifi_enabled(True):
            pytest.fail("前置条件失败：无法打开 WiFi 开关")
