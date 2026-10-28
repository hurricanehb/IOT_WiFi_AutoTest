"""Apply and verify one live traditional WiFi AP SSID and channel change."""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.libs.access_points import WiFiAPAction


TARGET_SSID = "PyAutoTest_Live_0729"
SSID_PROFILE = "PyAutoTest-SSID"
BAND = "2g"
CHANNEL = 6


def _verify(action: WiFiAPAction) -> None:
    config = action._run(
        [("display current-configuration", action._ap.ap_flag)]
    )
    ssid_hits = [
        line.strip() for line in config.splitlines() if TARGET_SSID in line
    ]
    radio_status = action._run([("display radio all", action._ap.ap_flag)])
    radio_id = "0" if BAND == "2g" else "1"
    channel_hits = []
    for line in radio_status.splitlines():
        fields = line.split()
        if (
            len(fields) >= 7
            and fields[0] == "2"
            and fields[2] == radio_id
            and fields[6] == f"{CHANNEL}/20M"
        ):
            channel_hits.append(line.strip())
    print(f"SSID VERIFY: {ssid_hits or 'NOT FOUND'}")
    print(f"CHANNEL VERIFY: {channel_hits or 'NOT FOUND'}")

    if not ssid_hits or not channel_hits:
        raise RuntimeError("设备当前配置回查失败")
    print("LIVE CHANGE RESULT: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--inspect-channel", action="store_true")
    args = parser.parse_args()
    action = WiFiAPAction()
    try:
        inventory = action.display_ap_all()
        online_line = next(
            (
                line.strip()
                for line in inventory.splitlines()
                if line.strip().startswith("2 ")
            ),
            "AP ID 2 row not found",
        )
        print(f"PREFLIGHT: {online_line}")

        if args.inspect_channel:
            radio = 0 if BAND == "2g" else 1
            radio_prompt = f"[{action._sysname}-wlan-radio-2/{radio}]"
            action._run(
                action._wlan_commands()
                + [
                    ("ap-id 2", f"[{action._sysname}-wlan-ap-2]"),
                    (f"radio {radio}", radio_prompt),
                ]
            )
            print("CHANNEL HELP:")
            print(action._execute("channel 20mhz ?", radio_prompt))
            return

        if not args.verify_only:
            action.set_ssid(SSID_PROFILE, TARGET_SSID)
            print(
                f"SSID COMMAND: PASS profile={SSID_PROFILE} ssid={TARGET_SSID}"
            )

            action.set_channel(BAND, CHANNEL, bandwidth_mhz=20, ap_id=2)
            print(
                "CHANNEL COMMAND: PASS "
                f"ap_id=2 band={BAND} bandwidth=20mhz channel={CHANNEL}"
            )

        _verify(action)
    finally:
        action.close()


if __name__ == "__main__":
    main()