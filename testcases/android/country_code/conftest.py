import pytest
import time
from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.log_handler import get_logger

log = get_logger("android.country_code.conftest")

default_country_code = "US"

@pytest.fixture(scope="module", autouse=True)
def restore_country_code_after_module(request, adb):
    """
    Module-level fixture: after all tests, restore WiFi country code to US.
    """
    yield
    wifi = WiFiControl(adb)
    # 尝试恢复国家码为 US
    try:
        wifi.adb.shell("cmd", "wifi", "force-country-code", "enabled", default_country_code)
        time.sleep(1.0)
    except Exception as e:
        log.warning("[后置条件] 恢复国家码 US 失败: %s", e)
