from unittest.mock import Mock

from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.adb_helper import AdbHelper


def test_disconnect_all_forgets_current_network() -> None:
    adb = Mock(spec=AdbHelper)
    connected = True

    def shell(*args):
        nonlocal connected
        if args == ("cmd", "wifi", "status"):
            return 0, 'Wi-Fi is enabled\nWi-Fi is connected to "Lab"', ""
        if args == ("cmd", "wifi", "list-networks"):
            if connected:
                return 0, 'Network ID SSID Security\n1 "Lab" [CURRENT]', ""
            return 0, "No networks", ""
        if args == ("cmd", "wifi", "forget-network", "1"):
            connected = False
            return 0, "", ""
        if args == ("cmd", "wifi", "disconnect"):
            return 0, "", ""
        return 1, "", "unsupported"

    adb.shell.side_effect = shell
    adb.shell_line.return_value = (0, "", "")
    wifi = WiFiControl(adb)

    assert wifi.disconnect_all(settle_sec=0, post_wait_sec=0)
    adb.shell.assert_any_call("cmd", "wifi", "forget-network", "1")