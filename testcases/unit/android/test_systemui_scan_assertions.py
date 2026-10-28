from unittest.mock import Mock

from core.libs.android.wifi_scenarios.systemui.scan_assertions import (
    systemui_scan_snapshot,
    visible_systemui_ssids,
)


def test_visible_systemui_ssids_reads_wifi_rows() -> None:
    settings_ui = Mock()
    settings_ui.device.dump_hierarchy.return_value = """
        <hierarchy>
          <node resource-id="com.android.systemui:id/wifi_list">
            <node resource-id="com.android.systemui:id/wifi_title" text="Lab_AP" />
          </node>
        </hierarchy>
    """

    assert visible_systemui_ssids(settings_ui) == ("Lab_AP",)


def test_systemui_scan_snapshot_reads_title_and_summary() -> None:
    settings_ui = Mock()
    settings_ui.device.dump_hierarchy.return_value = """
        <hierarchy>
          <node resource-id="com.android.systemui:id/wifi_list">
            <node resource-id="com.android.systemui:id/wifi_title" text="Lab_AP" />
            <node resource-id="com.android.systemui:id/wifi_summary" text="已保存" />
          </node>
        </hierarchy>
    """

    assert systemui_scan_snapshot(settings_ui) == (("Lab_AP", "已保存"),)
