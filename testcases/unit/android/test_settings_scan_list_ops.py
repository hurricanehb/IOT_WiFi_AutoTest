from pathlib import Path

from core.libs.android.wifi_scenarios.settings.scan_list_ops import (
    scan_list_menu_items,
)


ROOT = Path(__file__).resolve().parents[3]


def test_scan_list_menu_items_parses_connected_menu_probe() -> None:
    hierarchy = (
        ROOT / "temp" / "scanlistops_connected_longpress_probe.xml"
    ).read_text(encoding="utf-8")

    assert scan_list_menu_items(hierarchy) == (
        "Lab_HW_AutoTest_5G",
        "分享",
        "取消保存",
        "断开连接",
    )


def test_scan_list_menu_items_parses_unsaved_menu_probe() -> None:
    hierarchy = (
        ROOT / "temp" / "scanlistops_unsaved_longpress_probe.xml"
    ).read_text(encoding="utf-8")

    assert scan_list_menu_items(hierarchy) == ("Public_Free", "连接")


def test_scan_list_menu_items_ignores_background_settings_titles() -> None:
        hierarchy = """
        <hierarchy>
            <node class="android.widget.ListView" focused="false">
                <node resource-id="android:id/title" text="Google" />
                <node resource-id="android:id/title" text="网络和互联网" />
            </node>
            <node class="android.widget.ListView" focused="true">
                <node resource-id="android:id/title" text="Lab_AP" />
                <node resource-id="android:id/title" text="分享" />
                <node resource-id="android:id/title" text="断开连接" />
            </node>
        </hierarchy>
        """

        assert scan_list_menu_items(hierarchy) == ("Lab_AP", "分享", "断开连接")