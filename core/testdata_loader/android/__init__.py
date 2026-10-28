"""Android 域测试数据：wifi_ssid、country_code_tables 等。"""
from core.testdata_loader.android.country_code_data import (
    eu_country_codes,
    load_country_code_tables,
    us_country_codes,
)
from core.testdata_loader.android import wifi_data as _wifi_data

dual_wifi_list_rows = _wifi_data.dual_wifi_list_rows
dual_wifi_ssids = _wifi_data.dual_wifi_ssids
get_dual_wifi_entry = _wifi_data.get_dual_wifi_entry
get_dual_wifi_entry_by_region = _wifi_data.get_dual_wifi_entry_by_region
get_ssid_pwd_entry = _wifi_data.get_ssid_pwd_entry
get_wifi_list_entry = _wifi_data.get_wifi_list_entry
load_wifi_ssid = _wifi_data.load_wifi_ssid
save_wifi_ssid = _wifi_data.save_wifi_ssid
ssid_pwd_profile_rows = _wifi_data.ssid_pwd_profile_rows
wifi_list_rows = _wifi_data.wifi_list_rows
weaknet_scene_yaml = _wifi_data.weaknet_scene_yaml
wifi_ssid_yaml = _wifi_data.wifi_ssid_yaml

# 统一对外导出新名称
get_expected_connected_ssids = _wifi_data.get_expected_connected_ssids

__all__ = [
    "dual_wifi_list_rows",
    "dual_wifi_ssids",
    "eu_country_codes",
    "get_expected_connected_ssids",
    "get_dual_wifi_entry",
    "get_dual_wifi_entry_by_region",
    "get_ssid_pwd_entry",
    "get_wifi_list_entry",
    "load_country_code_tables",
    "load_wifi_ssid",
    "save_wifi_ssid",
    "ssid_pwd_profile_rows",
    "us_country_codes",
    "weaknet_scene_yaml",
    "wifi_list_rows",
    "wifi_ssid_yaml",
]
