"""Android Welcome WLAN wifi icon scenarios."""
from __future__ import annotations

import pytest

from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI
from core.testdata_loader import get_wifi_list_entry
from core.utils.log_handler import get_logger


_WELCOME_HYPERWIFI_ENTRY_ID = "welcome_hyperwifi"


def _welcome_hyperwifi_ssid(wifi_yaml: dict) -> str:
    entry = get_wifi_list_entry(wifi_yaml, entry_id=_WELCOME_HYPERWIFI_ENTRY_ID)
    ssid = str(entry.get("ssid") or "").strip()
    if not ssid:
        pytest.skip(f"wifi_ssid.yaml 缺少 {_WELCOME_HYPERWIFI_ENTRY_ID!r} 测试数据")
    return ssid


def run_welcome_hyperwifi_icon_case(wifi_yaml, settings_ui, tmp_path, capsys) -> None:
    ssid = _welcome_hyperwifi_ssid(wifi_yaml)
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    label = welcome_wlan_ui.find_hyperwifi_label(preferred_ssid=ssid)
    message = (
        f'\nwelcomeUI，WLAN列表 {ssid!r} 的"HYPER Wi-Fi"标识显示正常'
        if label is not None
        else f'\nwelcomeUI，WLAN列表不存在 {ssid!r} 的"HYPER Wi-Fi"标识'
    )
    get_logger(__name__).info("%s", message.strip())
    with capsys.disabled():
        print(message)
    if label is None:
        welcome_wlan_ui.fail_with_artifacts(message)
