"""Provision an independent persistent GBK-encoded SSID on the traditional AP."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.libs.access_points import WiFiAPAction  # noqa: E402
from core.testdata_loader import get_ssid_pwd_entry, load_wifi_ssid  # noqa: E402
from core.utils.stdio_utf8 import ensure_utf8_stdio  # noqa: E402

AP_ID = 0
RADIO_ID = 1
BAND = "5g"
WLAN_ID = 15
VAP_PROFILE = "Lab_GBK_16"
SSID_PROFILE = "Lab_GBK_16-SSID"
SECURITY_PROFILE = "Lab_GBK_16-Security"
SERVICE_VLAN = 2
ENTRY_ID = "ssid_gbk_chinese_16"
SSID_ENCODING = "gbk"


def _wlan_rows(output: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in output.splitlines():
        fields = line.split()
        if (
            len(fields) >= 8
            and fields[0] == str(AP_ID)
            and fields[2] == str(RADIO_ID)
            and fields[3] == str(WLAN_ID)
        ):
            rows.append(fields)
    return rows


def main() -> None:
    entry = get_ssid_pwd_entry(load_wifi_ssid(), entry_id=ENTRY_ID)
    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("password") or "")
    encoding = str(entry.get("ssid_encoding") or "").strip().lower()
    if not ssid or not password:
        raise RuntimeError(f"{ENTRY_ID} 缺少 SSID 或密码")
    if encoding != SSID_ENCODING:
        raise RuntimeError(f"{ENTRY_ID} 编码必须为 {SSID_ENCODING!r}: {encoding!r}")
    encoded_ssid = ssid.encode(SSID_ENCODING)
    if len(encoded_ssid) > 32:
        raise RuntimeError(f"GBK SSID 超过 32 字节: {len(encoded_ssid)}")

    action = WiFiAPAction()
    try:
        current = action._run_encoded(
            [("display vap all", action._ap.ap_flag)], SSID_ENCODING
        )
        conflicts = [row for row in _wlan_rows(current) if row[-1] != ssid]
        if conflicts:
            raise RuntimeError(f"AP0 radio1 wlan15 已被其他 VAP 占用: {conflicts!r}")

        action.set_ssid(SSID_PROFILE, ssid, encoding=SSID_ENCODING)
        action.set_security(SECURITY_PROFILE, "wpa2-aes", password=password)
        action.bind_vap(
            VAP_PROFILE,
            ssid_profile=SSID_PROFILE,
            security_profile=SECURITY_PROFILE,
            service_vlan=SERVICE_VLAN,
            forward_mode="tunnel",
        )
        action.attach_vap_to_radio(
            VAP_PROFILE,
            BAND,
            ap_id=AP_ID,
            wlan_id=WLAN_ID,
        )
        action.wait_for_vap_online(ssid, BAND, encoding=SSID_ENCODING)
        action.save_configuration()

        final = action._run_encoded(
            [("display vap all", action._ap.ap_flag)], SSID_ENCODING
        )
        rows = _wlan_rows(final)
        if len(rows) != 1 or rows[0][5] != "ON" or rows[0][-1] != ssid:
            raise RuntimeError(f"GBK 常驻 VAP 状态异常: {rows!r}")
        print(
            f"GBK 常驻 VAP 已保存: ap={AP_ID}, radio={RADIO_ID}, "
            f"wlan={WLAN_ID}, vlan={SERVICE_VLAN}, bytes={len(encoded_ssid)}, "
            f"ssid={ssid!r}"
        )
    finally:
        action.close()


if __name__ == "__main__":
    ensure_utf8_stdio()
    main()
