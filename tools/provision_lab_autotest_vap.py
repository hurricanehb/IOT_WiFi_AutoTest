"""Provision the persistent Lab_HW_AutoTest VAP on the traditional AP."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.libs.access_points import WiFiAPAction  # noqa: E402
from core.testdata_loader import get_wifi_list_entry, load_wifi_ssid  # noqa: E402
from core.utils.stdio_utf8 import ensure_utf8_stdio  # noqa: E402

AP_ID = 0
WLAN_ID = 13
VAP_PROFILE = "Lab_HW_AutoTest"
SSID_PROFILE = "Lab_HW_AutoTest-SSID"
SECURITY_PROFILE = "Lab_HW_AutoTest-Security"
SERVICE_VLAN = 2


def _wlan_rows(output: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in output.splitlines():
        fields = line.split()
        if (
            len(fields) >= 8
            and fields[0] == str(AP_ID)
            and fields[2] in {"0", "1"}
            and fields[3] == str(WLAN_ID)
        ):
            rows.append(fields)
    return rows


def main() -> None:
    entry = get_wifi_list_entry(
        load_wifi_ssid(),
        entry_id="wifi_ap_ssid_default",
    )
    ssid = str(entry.get("ssid") or "")
    password = str(entry.get("pwd") or "")
    if not ssid or not password:
        raise RuntimeError("wifi_ap_ssid_default 缺少 SSID 或密码")

    action = WiFiAPAction()
    try:
        current = action._run([("display vap all", action._ap.ap_flag)])
        conflicts = [row for row in _wlan_rows(current) if row[-1] != ssid]
        if conflicts:
            raise RuntimeError(f"AP0 wlan13 已被其他 VAP 占用: {conflicts!r}")

        action.set_ssid(SSID_PROFILE, ssid)
        action.set_security(SECURITY_PROFILE, "wpa2-aes", password=password)
        action.bind_vap(
            VAP_PROFILE,
            ssid_profile=SSID_PROFILE,
            security_profile=SECURITY_PROFILE,
            service_vlan=SERVICE_VLAN,
            forward_mode="tunnel",
        )
        for band in ("2g", "5g"):
            action.attach_vap_to_radio(
                VAP_PROFILE,
                band,
                ap_id=AP_ID,
                wlan_id=WLAN_ID,
            )

        action.teardown_wifi()
        action.save_configuration()

        final = action._run([("display vap all", action._ap.ap_flag)])
        rows = _wlan_rows(final)
        if len(rows) != 2 or any(row[5] != "ON" or row[-1] != ssid for row in rows):
            raise RuntimeError(f"常驻 VAP 状态异常: {rows!r}")
        print(
            f"常驻 VAP 已保存: ap={AP_ID}, radios=0/1, wlan={WLAN_ID}, "
            f"vlan={SERVICE_VLAN}, ssid={ssid!r}"
        )
    finally:
        action.close()


if __name__ == "__main__":
    ensure_utf8_stdio()
    main()