from __future__ import annotations

from unittest.mock import Mock, call

from core.libs.android.bluetooth_wlan_reset_control import BluetoothWlanResetControl


def test_find_labeled_bounds_matches_one_semantic_attribute() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    hierarchy = """
        <hierarchy>
            <node text="网络重置选项" bounds="[0,0][400,80]" />
            <node text="ignored" content-desc="重置 蓝牙和 WLAN" bounds="[0,100][400,180]" />
        </hierarchy>
    """

    assert control._find_labeled_bounds(hierarchy, ("重置蓝牙和WLAN",)) == (
        0,
        100,
        400,
        180,
    )


def test_find_labeled_bounds_accepts_localized_reset_alias() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    hierarchy = '<hierarchy><node text="Reset options" bounds="[0,100][400,180]" /></hierarchy>'

    assert control._find_labeled_bounds(
        hierarchy, control._RESET_OPTIONS_LABELS
    ) == (0, 100, 400, 180)


def test_scroll_down_uses_scrollable_container_bounds() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control.adb = Mock()
    hierarchy = """
        <hierarchy>
            <node bounds="[0,0][1080,2400]" />
            <node scrollable="true" bounds="[40,200][1040,1800]" />
        </hierarchy>
    """

    control._scroll_down(hierarchy)

    control.adb.swipe.assert_called_once_with(540, 1400, 540, 600, 300)


def test_settings_navigation_ignores_non_settings_window_nodes() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    hierarchy = """
        <hierarchy>
            <node text="系统" package="com.android.launcher" bounds="[0,1800][300,1900]" />
            <node text="系统" package="com.android.settings" bounds="[0,400][720,500]" />
        </hierarchy>
    """

    assert control._find_labeled_bounds(hierarchy, control._SYSTEM_LABELS) == (
        0,
        400,
        720,
        500,
    )


def test_scroll_down_uses_settings_scroll_container_in_dual_window() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control.adb = Mock()
    hierarchy = """
        <hierarchy>
            <node package="com.android.launcher" scrollable="true" bounds="[0,0][1920,1080]" />
            <node package="com.android.settings" scrollable="true" bounds="[0,144][720,996]" />
        </hierarchy>
    """

    control._scroll_down(hierarchy)

    control.adb.swipe.assert_called_once_with(360, 783, 360, 357, 300)


def test_scroll_down_uses_largest_pane_by_default_when_settings_has_two_panes() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control.adb = Mock()
    hierarchy = """
        <hierarchy>
            <node package="com.android.settings" scrollable="true" bounds="[0,144][720,996]" />
            <node package="com.android.settings" scrollable="true" bounds="[720,144][1920,996]" />
        </hierarchy>
    """

    control._scroll_down(hierarchy)

    control.adb.swipe.assert_called_once_with(1320, 783, 1320, 357, 300)


def test_scroll_down_uses_requested_pane_when_settings_has_two_panes() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control.adb = Mock()
    hierarchy = """
        <hierarchy>
            <node package="com.android.settings" scrollable="true" bounds="[0,144][720,996]" />
            <node package="com.android.settings" scrollable="true" bounds="[720,144][1920,996]" />
        </hierarchy>
    """

    control._scroll_down(hierarchy, pane="left")
    control._scroll_down(hierarchy, pane="right")

    assert control.adb.swipe.call_args_list == [
        call(360, 783, 360, 357, 300),
        call(1320, 783, 1320, 357, 300),
    ]


def test_confirm_reset_prefers_standard_positive_button() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control.adb = Mock()
    control._wait_for_reset_confirm_bounds = Mock()
    control._wait_for_stable_settings_xml = Mock(return_value="<hierarchy />")
    control._find_resource_bounds = Mock(return_value=(10, 20, 50, 60))
    control._tap_labeled_item = Mock()
    control._wait_for_confirm_to_close = Mock()

    control._confirm_reset()

    control.adb.tap.assert_called_once_with(30, 40)
    control._tap_labeled_item.assert_not_called()


def test_find_reset_confirm_bounds_falls_back_to_confirm_label() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    hierarchy = '<hierarchy><node text="重置" bounds="[10,20][50,60]" /></hierarchy>'

    assert control._find_reset_confirm_bounds(hierarchy) == (10, 20, 50, 60)


def test_reset_from_current_reset_options_page() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control._open_settings = Mock()
    control._tap_labeled_item = Mock()
    control._reset_from_reset_options = Mock()
    control._tap_labeled_item_if_visible = Mock(return_value=True)
    control._confirm_reset = Mock()

    control._reset_bluetooth_and_wlan_once()

    control._tap_labeled_item_if_visible.assert_called_once_with(
        control._RESET_BLUETOOTH_WLAN_LABELS
    )
    control._confirm_reset.assert_called_once_with()
    control._open_settings.assert_not_called()
    control._tap_labeled_item.assert_not_called()
    control._reset_from_reset_options.assert_not_called()


def test_reset_item_search_uses_right_settings_detail_pane() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control._tap_labeled_item = Mock()
    control._confirm_reset = Mock()

    control._reset_from_reset_options()

    control._tap_labeled_item.assert_called_once_with(
        control._RESET_BLUETOOTH_WLAN_LABELS,
        scroll=True,
        scroll_pane="right",
    )
    control._confirm_reset.assert_called_once_with()


def test_reset_navigates_from_settings_root_when_reset_option_is_not_visible() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    control._open_settings = Mock()
    control._tap_labeled_item = Mock()
    control._reset_from_reset_options = Mock()
    control._tap_labeled_item_if_visible = Mock(return_value=False)

    control._reset_bluetooth_and_wlan_once()

    control._open_settings.assert_called_once_with()
    control._tap_labeled_item.assert_has_calls(
        [
            call(control._SYSTEM_LABELS, scroll=True, scroll_pane="left"),
            call(control._RESET_OPTIONS_LABELS, scroll=True, scroll_pane="right"),
        ]
    )
    control._reset_from_reset_options.assert_called_once_with()


def test_reset_labels_include_bluetooth_and_wlan_settings() -> None:
    control = object.__new__(BluetoothWlanResetControl)
    hierarchy = '<hierarchy><node text="重置蓝牙和 WLAN 设置" bounds="[0,100][400,180]" /></hierarchy>'

    assert control._find_labeled_bounds(
        hierarchy, control._RESET_BLUETOOTH_WLAN_LABELS
    ) == (0, 100, 400, 180)