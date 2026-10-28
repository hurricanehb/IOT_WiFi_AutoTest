"""SystemUI WiFi connection-configuration scenarios."""
from __future__ import annotations

import allure

from core.libs.android.wifi_control.controller import WiFiControl
from core.libs.android.wifi_scenarios.connection_config import (
    run_connection_config_case,
)
from core.libs.android.systemui_pages.quick_settings_page import open_internet_dialog
from core.libs.android.settings_pages.settings_page import AndroidSettingsUI


@allure.step("执行 SystemUI 连接配置验证")
def run_systemui_connection_config_case(
    summary: str,
    run_shell_cmd,
    wifi: WiFiControl,
    wifi_yaml: dict,
    settings_ui: AndroidSettingsUI,
    *,
    operation: str,
    hyper: bool = False,
) -> None:
    """Run a connection-dialog assertion from the SystemUI network panel."""
    run_connection_config_case(
        summary,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        settings_ui,
        operation=operation,
        hyper=hyper,
        open_networks=lambda: open_internet_dialog(settings_ui),
    )
