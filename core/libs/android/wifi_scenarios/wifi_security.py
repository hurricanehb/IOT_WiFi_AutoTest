"""SP WiFi security workflows with explicit operator observations."""
from __future__ import annotations

import os
import sys
import time
from typing import Callable
from xml.etree import ElementTree

import allure
import pytest

from core.libs.android.wifi_scenarios.status_capture import attach_wifi_status

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_control.ssid_parsers import saved_network_ssids, ssid_match
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


NETWORK_MODES = (
    "WEP",
    "Open（无密码）",
    "Portal + 无密码",
    "Portal + 普通密码认证",
    "Portal + 短信认证",
    "MAC 认证",
    "MAC 优先 Portal 认证",
)


def is_sp_model(model: str) -> bool:
    normalized = (model or "").strip().casefold()
    return normalized.startswith(("p", "sp"))


def confirm_step(summary: str, instruction: str) -> None:
    """Require an affirmative observation; missing input is never a pass."""
    for attempt in range(3):
        try:
            answer = input(
                f"[{summary}] {instruction}\n"
                "输入 yes=已完成且符合描述 / no=不符合 / skip=环境不具备: "
            ).strip().casefold()
        except (EOFError, OSError):
            pytest.skip(f"{summary}: 半自动用例需要交互终端，请使用 pytest -s 且不要使用 -n")
        if answer == "yes":
            print(f"[{summary}] 人工确认: {instruction}")
            return
        if answer == "no":
            pytest.fail(f"{summary}: 人工观察不符合预期: {instruction}")
        if answer == "skip":
            pytest.skip(f"{summary}: 人工声明环境不具备: {instruction}")
        print(f"[{summary}] 无效回答 ({attempt + 1}/3)，需要明确输入 yes/no/skip")
    pytest.fail(f"{summary}: 未收到有效的人工确认")


def _target_ssid(summary: str) -> str:
    value = os.environ.get("WIFISEC_WEAK_SSID", "").strip()
    if not value:
        try:
            value = input(f"[{summary}] 输入本用例陪测 AP 的准确 SSID（不要输入密码）: ").strip()
        except (EOFError, OSError):
            pytest.skip(f"{summary}: 需要交互终端输入目标 SSID，请使用 pytest -s")
    if not value or value.casefold() == "skip":
        pytest.skip(f"{summary}: 未提供目标 SSID")
    return value


def _capture(settings_ui: AndroidSettingsUI, stage: str) -> str:
    directory = settings_ui.artifact_dir
    directory.mkdir(parents=True, exist_ok=True)
    hierarchy = settings_ui.device.dump_hierarchy()
    xml_path = directory / f"{stage}.xml"
    screenshot_path = directory / f"{stage}.png"
    xml_path.write_text(hierarchy, encoding="utf-8")
    settings_ui.device.screenshot(str(screenshot_path))
    print(f"[半自动留证] XML={xml_path}; screenshot={screenshot_path}")
    return hierarchy


def _observe(
    summary: str, settings_ui: AndroidSettingsUI, stage: str, instruction: str
) -> ElementTree.Element:
    try:
        confirm_step(summary, instruction)
    finally:
        hierarchy = _capture(settings_ui, stage)
    try:
        return ElementTree.fromstring(hierarchy)
    except ElementTree.ParseError:
        pytest.fail(f"{summary}: {stage} 控件树无效，无法验证观察结果")


def _page_texts(root: ElementTree.Element, package: str) -> set[str]:
    nodes = [node for node in root.iter("node") if node.get("package") == package]
    if not nodes:
        pytest.fail(f"当前界面不属于 {package}，请停留在待验证页面")
    return {node.get("text", "").strip() for node in nodes if node.get("text", "").strip()}


def _check_list(
    summary: str,
    settings_ui: AndroidSettingsUI,
    ssid: str,
    *,
    present: bool,
    stage: str,
    system_ui: bool = False,
) -> None:
    if system_ui:
        page = "SP 下拉快捷设置的 SystemUI WLAN 列表（不是 Settings）"
        package = "com.android.systemui"
    else:
        settings_ui.open_wifi_settings()
        page = "设置 > 网络和互联网 > WLAN 列表"
        package = "com.android.settings"
    expectation = "可以看到目标，且将目标滚动到当前屏幕" if present else "遍历完整列表后确认不存在目标"
    root = _observe(
        summary, settings_ui, stage,
        f"进入{page}，等待列表刷新；{expectation} SSID={ssid!r}。停留在该列表，不要点击连接",
    )
    texts = _page_texts(root, package)
    found = ssid in texts
    if found != present:
        pytest.fail(f"{summary}: {stage} 目标 {ssid!r} 可见性期望={present}，实际={found}")


def _configure_ap(summary: str, ssid: str, mode: str, *, hidden: bool = False) -> None:
    confirm_step(
        summary,
        f"在陪测 AP 上配置 SSID={ssid!r}，认证方式={mode}，隐藏网络={'是' if hidden else '否'}；"
        "确认 AP 配置已生效且正在发射，使用另一台不受 WiFi 安全限制的终端确认网络可用。"
        "Portal 的网页登录密码不能替代无线加密配置，不要改动无关实验室网络",
    )


def _assert_not_added(summary: str, wifi: WiFiControl, ssid: str) -> None:
    networks = wifi.list_networks_blob()
    if not networks or not any(
        heading in networks.casefold() for heading in ("network id", "saved networks")
    ):
        pytest.fail(f"{summary}: 无法识别 list-networks 返回值，不能判定未保存目标网络")
    saved = saved_network_ssids(networks)
    connected = wifi.list_connected_ssids(trust_status_fallback=True)
    if any(ssid_match(ssid, candidate) for candidate in saved + connected):
        pytest.fail(f"{summary}: 禁止添加的网络 {ssid!r} 已被保存或连接")


@allure.step("执行 SP WiFi 安全验证")
def run_sp_wifi_security_case(
    case: dict,
    run_shell_cmd: Callable[[str], str],
    wifi: WiFiControl,
    settings_ui: AndroidSettingsUI,
) -> None:
    """Execute all 18 WifiSec requirements with logged operator participation."""
    summary = case["case_id"]
    attach_wifi_status(case["case_id"], run_shell_cmd)
    model = run_shell_cmd("getprop ro.product.model").strip()
    if not is_sp_model(model):
        pytest.skip(
            f"{summary}: WiFi 安全中心仅支持 SP（P 系列）设备，"
            f"当前型号={model or '<empty>'!r}"
        )
    system_ui = summary == "Func_Components_Settings_WifiSec_UI_001"
    if system_ui:
        number = 0
    else:
        prefix = "Func_Components_Settings_WifiSec_Vali_"
        if not summary.startswith(prefix) or summary[len(prefix):] not in {
            f"{value:03d}" for value in range(1, 18)
        }:
            raise ValueError(f"未知 SP WiFi 安全用例: {summary}")
        number = int(summary[len(prefix):])
    print(f"[{summary}] 半自动执行，设备={settings_ui.serial}，model={model!r}")
    confirm_step(
        summary,
        "确认当前连接设备为 SP，已记录陪测 AP 原配置；"
        "本次允许人工修改陪测 AP 和 WiFi 安全开关，结束时恢复。"
        "所有 yes 都表示已实际观察，不得仅按预期回答",
    )
    ssid = _target_ssid(summary)
    try:
        if number == 1:
            _observe(
                summary, settings_ui, "factory_default",
                "确认 SP 当前确为出厂状态；打开 安全 > 安全中心 > WiFi安全，"
                "在未手动启用之前观察开关默认已开启。若不是出厂状态请输入 skip，不要执行恢复出厂",
            )
        else:
            _observe(
                summary, settings_ui, "security_on",
                "打开 SP 安全 > 安全中心 > WiFi安全，确认开关已开启（SP 默认开启）；停留在该页",
            )
        if not wifi.set_wifi_enabled(True):
            pytest.fail(f"{summary}: 无法开启 WLAN")
        if system_ui or number == 1:
            _configure_ap(summary, ssid, "Open 或 WEP 弱加密")
            if system_ui:
                _check_list(summary, settings_ui, ssid, present=False, stage="systemui_on", system_ui=True)
            _observe(
                summary, settings_ui, "security_off",
                "在 SP 安全 > 安全中心 > WiFi安全，手动关闭开关并确认关闭状态；停留在该页",
            )
            _check_list(summary, settings_ui, ssid, present=True, stage="security_off_list", system_ui=system_ui)
        elif 2 <= number <= 8:
            _configure_ap(summary, ssid, NETWORK_MODES[number - 2])
            _check_list(summary, settings_ui, ssid, present=False, stage="insecure_list")
            _configure_ap(summary, ssid, "WPA2-Personal（AES），关闭 Portal/MAC 认证；保持同一 SSID")
            _check_list(summary, settings_ui, ssid, present=True, stage="wpa2_list")
        elif number in (9, 10):
            _configure_ap(summary, ssid, NETWORK_MODES[number - 9], hidden=True)
            settings_ui.open_wifi_settings()
            forbidden = {"wep"} if number == 9 else {"open", "none", "无", "无安全性"}
            root = _observe(
                summary, settings_ui, "security_options",
                f"在 WLAN > 添加网络 > 安全性打开下拉列表，完整查看（必要时滚动）所有选项，"
                f"确认无 {sorted(forbidden)!r}；停留在展开的安全性列表，至少显示一项 WPA 安全选项",
            )
            texts = _page_texts(root, "com.android.settings")
            normalized = {text.casefold() for text in texts}
            if not any("wpa" in text for text in normalized):
                pytest.fail(f"{summary}: 未读取到 WPA 安全选项，不能确认安全性列表已展开")
            if normalized & forbidden:
                pytest.fail(f"{summary}: 安全性列表仍有禁止选项 {sorted(normalized & forbidden)!r}")
        else:
            _configure_ap(summary, ssid, NETWORK_MODES[number - 11])
            confirm_step(
                summary,
                f"在 SP 忘记 SSID={ssid!r} 的所有已保存条目并断开该网络。"
                "为上述 AP 生成对应 WiFi 二维码并在外部显示器展示；密码只在本地填写，不要输入测试终端",
            )
            _assert_not_added(summary, wifi, ssid)
            _observe(
                summary, settings_ui, "qr_result",
                f"在 SP WLAN > 添加网络 > 扫码添加，扫描 SSID={ssid!r} 的二维码。"
                "必须确认二维码已被识别且因 WiFi 安全策略明确拒绝添加；保留结果界面。"
                "镜头未识别、无响应、二维码错误或仅连接超时不能回答 yes；无法确认识别结果请输入 skip",
            )
            for sample in range(6):
                _assert_not_added(summary, wifi, ssid)
                if sample < 5:
                    time.sleep(2.0)
            _capture(settings_ui, "qr_after_observation")
    finally:
        primary_error = sys.exc_info()[0] is not None
        try:
            confirm_step(
                summary,
                "收尾：将 SP WiFi 安全恢复为开启；还原陪测 AP 原始 SSID、认证方式、隐藏状态；"
                "删除本用例意外新增的目标网络，不要清空其他网络。确认完成后停留在 WiFi 安全开启页面",
            )
            _capture(settings_ui, "restored")
        except BaseException as cleanup_error:
            if not primary_error:
                raise
            print(f"[{summary}] 收尾未完成，需人工恢复；保留原用例失败/跳过结果: {cleanup_error}")