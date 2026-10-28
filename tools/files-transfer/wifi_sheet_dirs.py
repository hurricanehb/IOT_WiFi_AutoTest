"""Excel sheet 名称与 testcases/android 子目录映射。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANDROID_CASES = ROOT / "testcases" / "android"
MD_DIR = ROOT / "tools" / "files-transfer" / "Android WiFi&HyperWiFi"

SHEET_TO_DIR: dict[str, str] = {
    "ITR专项": "itr",
    "兼容性": "compatibility",
    "WLAN高级设置": "wlan_advanced_settings",
    "国家码": "country_code",
    "WLAN热点": "wlan_hotspot",
    "HyperWiFi低功耗": "hyperwifi_low_power",
    "传统WiFi低功耗": "wifi_low_power",
    "无线黑名单": "wlan_blacklist",
    "无线接入": "wlan_access",
    "组件": "wlan_components",
    "网络选择": "net_selection",
    "多网络共存": "multi_network_coexistence",
    "MIX机型-USB模式切换": "mix_usb_mode_switch",
    "双链路主备切换管理": "dual_link_failover",
    "漫游": "roaming",
    "稳定性测试": "stability",
    "性能测试": "performance",
    "testcases": "wlan_access",
}

# 组件 sheet 内 ### 子模块 -> 输出目录
COMPONENT_SUBSECTION_DIRS: dict[str, str] = {
    "Settings组件": "wlan_components_settings",
    "SystemUI组件": "wlan_components_systemui",
    "Welcome组件": "wlan_components_welcome",
}

LEGACY_FILE_DIRS: dict[str, str] = {
    "test_AdvWlanSet_Mode.py": "wlan_advanced_settings",
    "test_wifi_stress.py": "stability",
    "test_wifi_connect.py": "common",
    "test_wifi_switch.py": "common",
    "test_wifi_weaknet.py": "common",
}


def sheet_output_dir(sheet_name: str) -> Path:
    folder = SHEET_TO_DIR.get(sheet_name)
    if not folder:
        folder = sheet_name.replace(" ", "_")
    return ANDROID_CASES / folder


def component_subsection_dir(subsection: str) -> Path:
    folder = COMPONENT_SUBSECTION_DIRS.get(subsection, "wlan_components")
    return ANDROID_CASES / folder


def ensure_sheet_dirs() -> list[Path]:
    created: list[Path] = []
    for folder in sorted(set(SHEET_TO_DIR.values()) | set(COMPONENT_SUBSECTION_DIRS.values()) | {"common"}):
        path = ANDROID_CASES / folder
        path.mkdir(parents=True, exist_ok=True)
        if path not in created:
            created.append(path)
    return created
