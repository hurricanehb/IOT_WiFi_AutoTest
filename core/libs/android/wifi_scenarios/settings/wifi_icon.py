"""Settings WiFi-standard and HyperWiFi icon scenarios."""
from __future__ import annotations

import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from xml.etree import ElementTree

import allure
from PIL import Image
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status
from core.libs.android.wifi_scenarios.wifi_icon_image import (
    has_h_glyph,
    has_hyper_badge,
)
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI
from core.testdata_loader import get_dual_wifi_entry

_BOUNDS_RE = re.compile(r"\[(\d+),(\d+)]\[(\d+),(\d+)]")
_STANDARD_RE = re.compile(r"Wi[\N{NON-BREAKING HYPHEN}-]?Fi\s*([4-7])", re.IGNORECASE)
_HYPER_BADGE_ID = "com.android.settings:id/turbolink_button"
_WIFI_ICON_ID = "android:id/icon"


@dataclass(frozen=True)
class WifiIconRow:
    ssid: str
    description: str
    resources: dict[str, tuple[int, int, int, int]]


def _bounds(value: str) -> tuple[int, int, int, int] | None:
    match = _BOUNDS_RE.fullmatch(value or "")
    return tuple(int(group) for group in match.groups()) if match else None


def wifi_icon_rows(hierarchy: str) -> list[WifiIconRow]:
    root = ElementTree.fromstring(hierarchy)
    parents = {child: parent for parent in root.iter() for child in parent}
    rows: list[WifiIconRow] = []
    for title in root.iter("node"):
        if title.get("resource-id") != "android:id/title":
            continue
        ssid = title.get("text", "").strip()
        if not ssid:
            continue
        container = title
        while container is not None and container.get("clickable") != "true":
            container = parents.get(container)
        if container is None:
            continue
        resources: dict[str, tuple[int, int, int, int]] = {}
        for node in container.iter("node"):
            resource_id = node.get("resource-id", "")
            node_bounds = _bounds(node.get("bounds", ""))
            if resource_id and node_bounds is not None:
                resources[resource_id] = node_bounds
        rows.append(
            WifiIconRow(
                ssid=ssid,
                description=container.get("content-desc", ""),
                resources=resources,
            )
        )
    return rows


def wifi_standard_generations(rows: list[WifiIconRow]) -> set[int]:
    generations: set[int] = set()
    for row in rows:
        if _HYPER_BADGE_ID in row.resources:
            continue
        generations.update(int(value) for value in _STANDARD_RE.findall(row.description))
    return generations


def _wait_for_rows(settings_ui: AndroidSettingsUI, ssid: str, timeout: float = 20.0) -> list[WifiIconRow]:
    deadline = time.monotonic() + timeout
    rows: list[WifiIconRow] = []
    settings_ui.open_wifi_settings()
    while time.monotonic() < deadline:
        settings_ui.device.shell("cmd wifi start-scan")
        time.sleep(2.0)
        rows = wifi_icon_rows(settings_ui.device.dump_hierarchy())
        if any(row.ssid == ssid for row in rows):
            return rows
    settings_ui.fail_with_artifacts(
        f"等待 WLAN 图标目标 {ssid!r} 超时，当前={[row.ssid for row in rows]!r}"
    )
    return []


def _target_hyper_ssid(wifi_yaml: dict) -> str:
    entry = get_dual_wifi_entry(wifi_yaml, entry_id="dual_wifi_24g_hyperwifi_us")
    hyper = entry.get("hyper_wifi")
    ssid = str(hyper.get("ssid") or "") if isinstance(hyper, dict) else ""
    if not ssid:
        pytest.skip("dual_wifi_24g_hyperwifi_us 缺少 HyperWiFi SSID")
    return ssid


@allure.step("执行 Settings WLAN 标准图标验证")
def run_settings_wifi_icon_case(
    summary: str,
    run_shell_cmd: Callable[[str], str],
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
) -> None:
    attach_wifi_status(summary, run_shell_cmd)
    if summary.endswith("UI_001"):
        settings_ui.open_wifi_settings()
        settings_ui.device.shell("cmd wifi start-scan")
        time.sleep(3.0)
        generations = wifi_standard_generations(
            wifi_icon_rows(settings_ui.device.dump_hierarchy())
        )
        if not generations:
            pytest.fail(f"{summary}: Settings WLAN 列表未检测到 Wi-Fi 4/5/6/7 下标")
        print(f"[{summary}] Settings 检测到 Wi-Fi 标准下标: {sorted(generations)}")
        return

    if not summary.endswith(("UI_002", "UI_003")):
        raise ValueError(f"未知 Settings WifiIcon 用例: {summary}")

    ssid = _target_hyper_ssid(wifi_yaml)
    rows = _wait_for_rows(settings_ui, ssid)
    row = next(item for item in rows if item.ssid == ssid)
    badge_bounds = row.resources.get(_HYPER_BADGE_ID)
    icon_bounds = row.resources.get(_WIFI_ICON_ID)
    settings_ui.artifact_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = settings_ui.artifact_dir / f"{summary}.png"
    settings_ui.device.screenshot(str(screenshot_path))
    image = Image.open(screenshot_path)
    allure.attach.file(
        str(screenshot_path),
        name=f"{summary}-settings-wifi-icons",
        attachment_type=allure.attachment_type.PNG,
    )

    if summary.endswith("UI_002"):
        if badge_bounds is None or not has_hyper_badge(image, badge_bounds):
            settings_ui.fail_with_artifacts(
                f"{summary}: {ssid!r} 未显示有效的 HYPER Wi-Fi 徽标"
            )
        return

    if icon_bounds is None or not has_h_glyph(image, icon_bounds):
        settings_ui.fail_with_artifacts(
            f"{summary}: {ssid!r} 的无线图标左下角未识别到 H"
        )