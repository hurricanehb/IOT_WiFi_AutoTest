from __future__ import annotations

import pytest

from core.libs.android.wifi_scenarios.systemui.ssid_display import _SSID_SHOW_PROFILES
from core.testdata_loader import (
    get_ssid_pwd_entry,
    get_wifi_list_entry,
    load_wifi_ssid,
)
from core.libs.android.wifi_scenarios.welcome.ssid_display import (
    WELCOME_SSID_PROFILE_BY_CASE,
)


def test_shared_wifi_entries_resolve_for_welcome_and_advanced_settings() -> None:
    data = load_wifi_ssid()

    welcome_encrypted = get_wifi_list_entry(
        data, entry_id="welcome_connection_wpa2"
    )
    welcome_open = get_wifi_list_entry(data, entry_id="welcome_connection_open")
    advanced_default = get_wifi_list_entry(data, entry_id="wifi_ap_ssid_default")

    assert welcome_encrypted["ssid"] == "MyXiaoMiWiFi"
    assert welcome_encrypted["pwd"] == advanced_default["pwd"]
    assert welcome_open == {
        "id": "welcome_connection_open",
        "ssid": "123456",
        "pwd": "",
        "encrypt": "OPEN",
        "type": "normal",
        "region": "",
        "expect": "connected",
    }


@pytest.mark.parametrize("number", (1, 2, 3, 4))
def test_welcome_encoded_ssid_display_profiles_reuse_systemui_testdata(number) -> None:
    data = load_wifi_ssid()
    case_id = f"Func_Components_Welcome_SsidShow_UI_{number:03d}"
    profile_id = WELCOME_SSID_PROFILE_BY_CASE[case_id]
    assert profile_id == _SSID_SHOW_PROFILES[number]
    entry = get_ssid_pwd_entry(data, entry_id=profile_id)
    assert entry["ssid"]
    assert entry["password"]
    assert 1 <= len(entry["ssid"].encode(entry["ssid_encoding"])) <= 32


def test_welcome_numeric_ssid_display_profile_resolves_from_shared_testdata() -> None:
    data = load_wifi_ssid()
    assert get_ssid_pwd_entry(
        data, entry_id="ssid_numeric_32_password_64"
    )["ssid"] == "12345678901234567890123456789012"