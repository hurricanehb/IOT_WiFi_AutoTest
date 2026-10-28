"""Android Welcome WLAN navigation scenarios."""
from __future__ import annotations

from core.libs.android.wifi_ui.welcome_page import WelcomeWlanUI
from core.utils.log_handler import get_logger


def run_welcome_expand_networks_case(settings_ui, tmp_path, capsys) -> None:
    welcome_wlan_ui = WelcomeWlanUI(settings_ui.device, tmp_path / "welcome-wlan-ui")
    if not welcome_wlan_ui.expand_all_and_confirm_more_ssids():
        message = '\nwelcomeUI，展开全部或大屏列表滚动后未显示更多SSID，FAIL'
        get_logger(__name__).info("%s", message.strip())
        with capsys.disabled():
            print(message)
        welcome_wlan_ui.fail_with_artifacts(message)

    get_logger(__name__).info("welcomeUI，展开全部或大屏列表滚动后显示更多SSID，PASS")
    with capsys.disabled():
        print('\nwelcomeUI，展开全部或大屏列表滚动后显示更多SSID，PASS')
