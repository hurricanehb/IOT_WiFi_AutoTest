from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, Mock, PropertyMock, call

import pytest

from core.libs.android.wifi_scenarios.welcome import ssid_display as welcome_ssid_display
from core.libs.android.wifi_ui.welcome_page import (
    HyperWiFiLabel,
    WelcomeWlanUI,
    WelcomeWifiNetwork,
)
from core.testdata_loader import get_ssid_pwd_entry, load_wifi_ssid


@pytest.mark.parametrize(
    "entry_id",
    (
        "ssid_utf8_chinese_10",
        "ssid_gbk_chinese_16",
        "ssid_cp949_korean",
        "ssid_shift_jis_japanese_16",
    ),
)
def test_welcome_ssid_display_configures_encoding_and_cleans_up(
    monkeypatch, entry_id: str
) -> None:
    data = load_wifi_ssid()
    entry = get_ssid_pwd_entry(data, entry_id=entry_id)
    events = Mock()
    monkeypatch.setattr(welcome_ssid_display, "attach_wifi_status", Mock())
    monkeypatch.setattr(welcome_ssid_display, "assert_ssid_visible_in_scan", events.scan)
    events.welcome.wait_for_ssid.return_value = True
    run_shell_cmd = Mock()
    summary = "Func_Components_Welcome_SsidShow_UI_001"

    welcome_ssid_display.run_welcome_ssid_display_case(
        summary, run_shell_cmd, data, events.welcome, events.ap,
        entry_id=entry_id, settle_sec=0,
    )

    assert events.mock_calls == [
        call.ap.configure_wifi(
            ssid=entry["ssid"], password=entry["password"],
            security="wpa2-aes", band="5g",
            ssid_encoding=entry["ssid_encoding"], verify=True,
        ),
        call.scan(run_shell_cmd, entry["ssid"], summary=summary),
        call.welcome.wait_for_ssid(entry["ssid"]),
        call.ap.teardown_wifi(),
    ]


@pytest.mark.parametrize("failure_stage", ("configure", "scan", "welcome"))
def test_welcome_ssid_display_cleans_up_on_failure(monkeypatch, failure_stage) -> None:
    monkeypatch.setattr(welcome_ssid_display, "attach_wifi_status", Mock())
    scan = Mock()
    monkeypatch.setattr(welcome_ssid_display, "assert_ssid_visible_in_scan", scan)
    ap = Mock()
    page = Mock()
    failing_operation = {
        "configure": ap.configure_wifi,
        "scan": scan,
        "welcome": page.wait_for_ssid,
    }[failure_stage]
    failing_operation.side_effect = RuntimeError(failure_stage)

    with pytest.raises(RuntimeError, match=failure_stage):
        welcome_ssid_display.run_welcome_ssid_display_case(
            "case", Mock(), load_wifi_ssid(), page, ap,
            entry_id="ssid_gbk_chinese_16", settle_sec=0,
        )

    ap.teardown_wifi.assert_called_once_with()


def test_welcome_ssid_display_timeout_saves_artifacts_and_cleans_up(monkeypatch) -> None:
    monkeypatch.setattr(welcome_ssid_display, "attach_wifi_status", Mock())
    monkeypatch.setattr(welcome_ssid_display, "assert_ssid_visible_in_scan", Mock())
    ap = Mock()
    page = Mock()
    page.wait_for_ssid.return_value = False
    page.fail_with_artifacts.side_effect = AssertionError("not displayed")

    with pytest.raises(AssertionError, match="not displayed"):
        welcome_ssid_display.run_welcome_ssid_display_case(
            "case", Mock(), load_wifi_ssid(), page, ap,
            entry_id="ssid_cp949_korean", settle_sec=0,
        )

    page.fail_with_artifacts.assert_called_once()
    assert "cp949" in page.fail_with_artifacts.call_args.args[0]
    ap.teardown_wifi.assert_called_once_with()


def test_welcome_ssid_display_skips_without_ap() -> None:
    with pytest.raises(pytest.skip.Exception, match="ap_config"):
        welcome_ssid_display.run_welcome_ssid_display_case(
            "case", Mock(), load_wifi_ssid(), Mock(), None,
            entry_id="ssid_utf8_chinese_10", settle_sec=0,
        )


def test_welcome_ssid_display_skips_missing_profile() -> None:
    ap = Mock()
    with pytest.raises(pytest.skip.Exception, match="missing SSID profile"):
        welcome_ssid_display.run_welcome_ssid_display_case(
            "case", Mock(), {}, Mock(), ap,
            entry_id="ssid_utf8_chinese_10", settle_sec=0,
        )

    ap.configure_wifi.assert_not_called()
    ap.teardown_wifi.assert_not_called()


def test_click_hyperwifi_label_accepts_localized_intro_title() -> None:
    device = Mock()
    device.dump_hierarchy.side_effect = (
        '<hierarchy><node text="Office" /></hierarchy>',
        '<hierarchy><node text="HyperWiFi介绍界面" /></hierarchy>',
    )
    page = WelcomeWlanUI(device, Path("artifacts"))
    label = HyperWiFiLabel("test", {"left": 10, "top": 20, "right": 30, "bottom": 40})
    page._visible_hyperwifi_label = Mock(return_value=label)

    assert page.click_hyperwifi_label_and_wait_for_intro(label)
    device.click.assert_called_once_with(20, 30)


def test_click_hyperwifi_label_accepts_intro_without_accessible_title() -> None:
    device = Mock()
    device.dump_hierarchy.side_effect = (
        '<hierarchy><node text="Office" /></hierarchy>',
        '<hierarchy><node class="android.widget.FrameLayout" /></hierarchy>',
    )
    page = WelcomeWlanUI(device, Path("artifacts"))
    label = HyperWiFiLabel("test", {"left": 10, "top": 20, "right": 30, "bottom": 40})
    page._visible_hyperwifi_label = Mock(return_value=label)

    assert page.click_hyperwifi_label_and_wait_for_intro(label)
    device.click.assert_called_once_with(20, 30)


def test_close_hyperwifi_intro_clicks_close_and_requires_wlan_list() -> None:
    device = Mock()
    close = device.return_value
    close.click_exists.return_value = True
    close.wait_gone.return_value = True
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()

    page.close_hyperwifi_intro()

    device.assert_called_once_with(resourceId="com.sunmi.welcome:id/btn_close")
    close.assert_has_calls([call.click_exists(timeout=5.0), call.wait_gone(timeout=5.0)])
    page._require_wlan_list.assert_called_once_with()


def test_close_hyperwifi_intro_fails_when_close_button_is_missing() -> None:
    device = Mock()
    device.return_value.click_exists.return_value = False
    page = WelcomeWlanUI(device, Path("artifacts"))
    page.fail_with_artifacts = Mock(side_effect=AssertionError("missing close"))
    page._require_wlan_list = Mock()

    with pytest.raises(AssertionError, match="missing close"):
        page.close_hyperwifi_intro()

    page.fail_with_artifacts.assert_called_once_with("未找到 HyperWiFi 介绍弹窗关闭按钮")
    device.return_value.wait_gone.assert_not_called()
    page._require_wlan_list.assert_not_called()


def test_close_hyperwifi_intro_fails_when_dialog_stays_open() -> None:
    device = Mock()
    device.return_value.click_exists.return_value = True
    device.return_value.wait_gone.return_value = False
    page = WelcomeWlanUI(device, Path("artifacts"))
    page.fail_with_artifacts = Mock(side_effect=AssertionError("still open"))
    page._require_wlan_list = Mock()

    with pytest.raises(AssertionError, match="still open"):
        page.close_hyperwifi_intro()

    page.fail_with_artifacts.assert_called_once_with("点击关闭后 HyperWiFi 介绍弹窗未消失")
    page._require_wlan_list.assert_not_called()


def test_expand_all_confirms_new_ssid_after_scrolling() -> None:
    device = Mock()
    expand_all_absent = Mock()
    expand_all_absent.exists = False
    expand_all = Mock()
    expand_all.exists = True
    device.side_effect = (expand_all_absent, expand_all)
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._scroll_to_top = Mock()
    page._visible_ssids = Mock(
        side_effect=({"SSID-1"}, {"SSID-1"}, {"SSID-1", "SSID-2"})
    )
    page._list_signature = Mock(
        side_effect=((("SSID-1", 1, 2),), (("SSID-1", 2, 3),))
    )
    page._swipe_to_next_page = Mock()

    assert page.expand_all_and_confirm_more_ssids(timeout=0.1)
    page._swipe_to_next_page.assert_called_once()
    expand_all.click.assert_called_once()


@pytest.mark.parametrize("forward", (False, True))
@pytest.mark.parametrize(
    ("screen_bounds", "list_bounds", "reported_size"),
    (
        ("[0,0][1920,1080]", "[409,294][1510,965]", (1080, 1920)),
        ("[0,0][720,1280]", "[0,200][720,1180]", (720, 1280)),
    ),
)
def test_wlan_swipes_stay_inside_actual_list(
    monkeypatch, forward, screen_bounds, list_bounds, reported_size
) -> None:
    device = Mock()
    device.window_size.return_value = reported_size
    device.dump_hierarchy.return_value = f"""
        <hierarchy>
            <node bounds="{screen_bounds}">
                <node scrollable="true" bounds="{list_bounds}">
                    <node resource-id="{WelcomeWlanUI.SSID_RESOURCE_ID}"
                          text="SSID-1" bounds="[465,330][527,374]" />
                </node>
            </node>
        </hierarchy>
    """
    monkeypatch.setattr("core.libs.android.wifi_ui.welcome_page.time.sleep", Mock())
    page = WelcomeWlanUI(device, Path("artifacts"))

    if forward:
        page._swipe_to_next_page()
    else:
        page._swipe_to_previous_page()

    start_x, start_y, end_x, end_y = device.swipe.call_args.args
    bounds = page._parse_bounds(list_bounds)
    assert bounds["left"] < start_x == end_x < bounds["right"]
    assert bounds["top"] < min(start_y, end_y) < max(start_y, end_y) < bounds["bottom"]
    assert (end_y < start_y) is forward
    device.window_size.assert_not_called()


@pytest.mark.parametrize(
    ("inset_layout", "pages", "expected"),
    (
        (True, ({"SSID-1"}, {"SSID-1", "SSID-2"}), True),
        (True, ({"SSID-1"}, {"SSID-1"}), False),
        (False, ({"SSID-1"}, {"SSID-1", "SSID-2"}), False),
    ),
)
def test_show_more_without_button_requires_inset_layout_and_new_ssids(
    inset_layout, pages, expected
) -> None:
    device = Mock()
    device.return_value.exists = False
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._scroll_to_top = Mock()
    page._is_inset_wlan_layout = Mock(return_value=inset_layout)
    page._visible_ssids = Mock(side_effect=pages)
    first = (("SSID-1", 10, 20),)
    second = (("SSID-2", 10, 20),)
    page._list_signature = Mock(side_effect=(first, second, second, second))
    page._swipe_to_next_page = Mock()

    assert page.expand_all_and_confirm_more_ssids(max_swipes=2) is expected
    assert page._swipe_to_next_page.call_count == 2


def test_show_more_does_not_pass_when_swipe_limit_is_exhausted() -> None:
    device = Mock()
    device.return_value.exists = False
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._scroll_to_top = Mock()
    page._is_inset_wlan_layout = Mock(return_value=True)
    page._visible_ssids = Mock(side_effect=({"SSID-1"}, {"SSID-2"}))
    page._list_signature = Mock(side_effect=((("SSID-1", 1, 2),), (("SSID-2", 1, 2),)))
    page._swipe_to_next_page = Mock()

    assert not page.expand_all_and_confirm_more_ssids(max_swipes=1)
    page._swipe_to_next_page.assert_called_once()


@pytest.mark.parametrize("panel_bounds, expected", (
    ("[401,91][1518,989]", True),
    ("[0,0][1920,1080]", False),
))
def test_inset_layout_detection_uses_actual_panel_bounds(panel_bounds, expected) -> None:
    device = Mock()
    device.dump_hierarchy.return_value = f"""
        <hierarchy><node bounds="[0,0][1920,1080]">
            <node resource-id="com.sunmi.welcome:id/ll_cell" bounds="{panel_bounds}" />
        </node></hierarchy>
    """
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._is_inset_wlan_layout() is expected


def test_list_signature_uses_one_snapshot_when_scan_results_shrink() -> None:
    device = Mock()
    device.side_effect = AssertionError("Live selectors can become stale during a scan")
    device.dump_hierarchy.side_effect = (
        '<hierarchy>'
        '<node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" '
        'text="SSID-1" bounds="[40,100][300,140]" />'
        '<node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" '
        'text="SSID-2" bounds="[40,200][300,240]" />'
        '<node resource-id="other:id/title" text="Other" bounds="[0,0][100,40]" />'
        '</hierarchy>',
        '<hierarchy>'
        '<node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" '
        'text="SSID-1" bounds="[40,100][300,140]" />'
        '</hierarchy>',
    )
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._list_signature() == (("SSID-1", 100, 140), ("SSID-2", 200, 240))
    assert page._list_signature() == (("SSID-1", 100, 140),)
    assert device.dump_hierarchy.call_count == 2
    device.assert_not_called()


def test_find_ssid_expands_list_and_continues_scrolling() -> None:
    device = Mock()
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(
        side_effect=({"SSID-1"}, {"SSID-1"}, {"SSID-target"})
    )
    page._expand_all_if_present = Mock(side_effect=(False, True))
    page._list_signature = Mock(
        side_effect=(("SSID-1", 1, 2), ("SSID-1", 2, 3))
    )
    page._swipe_to_previous_page = Mock()

    assert page.find_ssid("SSID-target")
    page._expand_all_if_present.assert_called_once_with()
    page._swipe_to_previous_page.assert_called_once()


def test_find_hyperwifi_label_uses_preferred_ssid() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    expected = HyperWiFiLabel(
        "MyHyperWiFi", {"left": 10, "top": 20, "right": 30, "bottom": 40}
    )
    page._require_wlan_list = Mock()
    page.find_ssid = Mock(return_value=True)
    page._visible_hyperwifi_label = Mock(return_value=expected)

    assert page.find_hyperwifi_label(preferred_ssid="MyHyperWiFi") == expected

    page.find_ssid.assert_called_once_with("MyHyperWiFi", max_swipes=30)
    page._visible_hyperwifi_label.assert_called_once_with(
        preferred_ssid="MyHyperWiFi"
    )


def test_visible_hyperwifi_label_does_not_fall_back_when_preferred_ssid_is_missing() -> None:
        device = Mock()
        device.dump_hierarchy.return_value = """
                <hierarchy>
                    <node clickable="true" bounds="[0,0][500,100]">
                        <node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" text="OtherHyperWiFi" bounds="[10,10][200,50]"/>
                        <node class="android.widget.ImageView" clickable="true" bounds="[220,10][260,50]"/>
                    </node>
                </hierarchy>
        """
        page = WelcomeWlanUI(device, Path("artifacts"))

        assert page._visible_hyperwifi_label(preferred_ssid="MyHyperWiFi") is None


def test_find_ssid_checks_each_page_without_native_search() -> None:
    device = Mock()
    scrollable = Mock()
    scrollable.scroll.to.side_effect = AssertionError("Native search bypasses page checks")
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(side_effect=({"SSID-1"}, {"SSID-1"}, {"SSID-target"}))
    page._expand_all_if_present = Mock(return_value=False)
    page._list_signature = Mock(
        side_effect=((("SSID-1", 1, 2),), (("SSID-target", 1, 2),))
    )
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert page.find_ssid("SSID-target")

    scrollable.scroll.to.assert_not_called()
    page._swipe_to_previous_page.assert_called_once()
    page._swipe_to_next_page.assert_not_called()


def test_find_ssid_returns_false_at_list_bottom() -> None:
    device = Mock()
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page._scroll_to_top = Mock()
    page._visible_ssids = Mock(return_value={"SSID-1"})
    page._expand_all_if_present = Mock(return_value=False)
    page._list_signature = Mock(return_value=(("SSID-1", 1, 2),))
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert not page.find_ssid("SSID-target")
    page._swipe_to_next_page.assert_called_once()
    page._swipe_to_previous_page.assert_called_once()


@pytest.mark.parametrize("target_index", (0, 3, 4, None))
@pytest.mark.parametrize("has_scroll_container", (False, True))
@pytest.mark.parametrize("wait_for_scan", (False, True))
def test_find_ssid_searches_both_sides_from_middle(
    monkeypatch, target_index, has_scroll_container, wait_for_scan
) -> None:
    device = Mock()
    device.window_size.return_value = (720, 1280)
    current_index = 2

    def hierarchy() -> str:
        ssid = "SSID-target" if current_index == target_index else f"SSID-{current_index}"
        resource_id = 'resource-id="com.sunmi.welcome:id/recyclerview"' if has_scroll_container else ""
        return (
            f'<hierarchy><node {resource_id} scrollable="true" bounds="[0,200][720,1180]">'
            '<node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" '
            f'text="{ssid}" bounds="[40,400][300,440]" /></node></hierarchy>'
        )

    def swipe(start_x, start_y, end_x, end_y, duration) -> None:
        nonlocal current_index
        step = 1 if end_y < start_y else -1
        current_index = min(4, max(0, current_index + step))

    device.dump_hierarchy.side_effect = hierarchy
    device.swipe.side_effect = swipe
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    scrollable = None
    if has_scroll_container:
        scrollable = Mock()
        scrollable.scroll.to.side_effect = AssertionError("Unexpected native search")
    page._expand_all_if_present = Mock(return_value=False)
    monkeypatch.setattr("core.libs.android.wifi_ui.welcome_page.time.sleep", Mock())

    found = (
        page.wait_for_ssid("SSID-target", timeout=0.0)
        if wait_for_scan
        else page.find_ssid("SSID-target", max_swipes=6)
    )
    assert found is (target_index is not None)
    if target_index is not None:
        assert current_index == target_index
    else:
        assert any(args.args[3] > args.args[1] for args in device.swipe.call_args_list)
        assert any(args.args[3] < args.args[1] for args in device.swipe.call_args_list)
    assert device.swipe.call_count <= 12


def test_find_ssid_visible_target_does_not_scroll() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(return_value={"SSID-target"})
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert page.find_ssid("SSID-target")

    page._swipe_to_next_page.assert_not_called()
    page._swipe_to_previous_page.assert_not_called()


def test_find_ssid_zero_swipes_does_not_move_list() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(return_value={"SSID-other"})
    page._expand_all_if_present = Mock(return_value=False)
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert not page.find_ssid("SSID-target", max_swipes=0)

    page._swipe_to_next_page.assert_not_called()
    page._swipe_to_previous_page.assert_not_called()


def test_find_ssid_checks_target_after_last_allowed_swipe() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(
        side_effect=({"SSID-other"}, {"SSID-other"}, {"SSID-target"})
    )
    page._expand_all_if_present = Mock(return_value=False)
    page._list_signature = Mock(
        side_effect=((("SSID-other", 1, 2),), (("SSID-target", 1, 2),))
    )
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert page.find_ssid("SSID-target", max_swipes=1)

    page._swipe_to_previous_page.assert_called_once()
    page._swipe_to_next_page.assert_not_called()


def test_find_ssid_bounds_swipes_when_scan_results_keep_changing() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(return_value={"SSID-other"})
    page._expand_all_if_present = Mock(return_value=False)
    page._list_signature = Mock(
        side_effect=(((f"SSID-{index}", 1, 2),) for index in range(120))
    )
    page._swipe_to_next_page = Mock()
    page._swipe_to_previous_page = Mock()

    assert not page.find_ssid("SSID-target")

    assert page._swipe_to_next_page.call_count == 30
    assert page._swipe_to_previous_page.call_count == 30


@pytest.mark.parametrize(
    ("requested_ssid", "expected"),
    (("HyperWi-Fi_3C74_Office", True), ("HyperWi-Fi_3C74_office", False)),
)
def test_find_ssid_keeps_network_names_case_sensitive(requested_ssid, expected) -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(return_value={"HyperWi-Fi_3C74_Office"})
    page._expand_all_if_present = Mock(return_value=False)

    assert page.find_ssid(requested_ssid, max_swipes=0) is expected


def test_find_ssid_stops_direction_when_pages_repeat() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page._require_wlan_list = Mock()
    page._visible_ssids = Mock(return_value={"SSID-other"})
    page._expand_all_if_present = Mock(return_value=False)
    first_page = (("SSID-1", 1, 2),)
    second_page = (("SSID-2", 1, 2),)
    page._list_signature = Mock(
        side_effect=(
            first_page, second_page, second_page, first_page,
            first_page, first_page, first_page,
        )
    )
    page._swipe_to_previous_page = Mock()
    page._swipe_to_next_page = Mock()

    assert not page.find_ssid("SSID-target")

    assert page._swipe_to_previous_page.call_count == 2
    page._swipe_to_next_page.assert_called_once()


def test_wlan_list_bounds_uses_nearest_ssid_scroll_ancestor() -> None:
    device = Mock()
    device.dump_hierarchy.return_value = """
        <hierarchy>
            <node scrollable="true" bounds="[0,0][1920,1080]">
            <node resource-id="com.sunmi.welcome:id/wifi_list" scrollable="true"
                  bounds="[409,294][1510,965]">
                <node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" text="SSID-1" />
            </node>
            </node>
        </hierarchy>
    """
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._wlan_list_bounds() == {
        "left": 409, "top": 294, "right": 1510, "bottom": 965,
    }
    device.assert_not_called()


def test_wait_for_ssid_listens_until_target_refreshes() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    page.find_ssid = Mock(side_effect=(False, True))

    assert page.wait_for_ssid("SSID-target", timeout=1.0, poll_interval=0.0)
    assert page.find_ssid.call_args_list == [
        call("SSID-target"),
        call("SSID-target"),
    ]


def test_open_encrypted_network_config_clicks_preferred_network() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = True
    cancel = Mock()
    cancel.exists = False
    device.side_effect = lambda **kwargs: (
        cancel
        if kwargs["resourceId"] == WelcomeWlanUI.CANCEL_RESOURCE_ID
        else password_field
    )
    page = WelcomeWlanUI(device, Path("artifacts"))
    network = WelcomeWifiNetwork(
        "encrypted-ssid", {"left": 10, "top": 20, "right": 50, "bottom": 60}
    )
    page._require_wlan_list = Mock()
    page.wait_for_ssid = Mock(return_value=True)
    page._find_encrypted_network = Mock(return_value=network)

    assert page.open_encrypted_network_config("encrypted-ssid") == "encrypted-ssid"
    device.click.assert_called_once_with(30, 40)
    password_field.wait.assert_called_once_with(timeout=5.0)
    page.wait_for_ssid.assert_called_once_with("encrypted-ssid")


def test_find_encrypted_network_uses_clickable_row_bounds() -> None:
        device = Mock()
        device.dump_hierarchy.return_value = """
                <hierarchy>
                    <node clickable="false" bounds="[20,620][700,748]">
                        <node clickable="true" bounds="[20,620][700,748]">
                            <node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" text="encrypted-ssid" bounds="[40,663][245,706]" />
                            <node resource-id="com.sunmi.welcome:id/item_iv_lock" />
                        </node>
                    </node>
                </hierarchy>
        """
        page = WelcomeWlanUI(device, Path("artifacts"))

        assert page._find_encrypted_network("encrypted-ssid") == WelcomeWifiNetwork(
                "encrypted-ssid", {"left": 20, "top": 620, "right": 700, "bottom": 748}
        )


def test_network_status_requires_matching_ssid_row() -> None:
        device = Mock()
        device.dump_hierarchy.return_value = """
                <hierarchy>
                    <node clickable="true">
                        <node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" text="other-ssid" />
                        <node text="请检查密码是否正确" />
                    </node>
                    <node clickable="true">
                        <node resource-id="com.sunmi.welcome:id/item_tv_wifi_name" text="target-ssid" />
                        <node text="已保存" />
                    </node>
                </hierarchy>
        """
        page = WelcomeWlanUI(device, Path("artifacts"))

        assert page._network_has_status("target-ssid", ("请检查密码", "已保存"))
        assert not page._network_has_status("missing-ssid", ("请检查密码", "已保存"))


def test_connect_open_network_clicks_target_without_opening_config() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = False
    cancel = Mock()
    cancel.exists = False
    device.side_effect = lambda **kwargs: (
        cancel
        if kwargs["resourceId"] == WelcomeWlanUI.CANCEL_RESOURCE_ID
        else password_field
    )
    page = WelcomeWlanUI(device, Path("artifacts"))
    network = WelcomeWifiNetwork(
        "open-ssid", {"left": 10, "top": 20, "right": 50, "bottom": 60}
    )
    page._require_wlan_list = Mock()
    page.wait_for_ssid = Mock(return_value=True)
    page._find_open_network = Mock(return_value=network)

    page.connect_open_network("open-ssid")

    device.click.assert_called_once_with(30, 40)
    password_field.wait.assert_called_once_with(timeout=2.0)
    page.wait_for_ssid.assert_called_once_with("open-ssid")


def test_open_connected_network_details_clicks_specified_ssid() -> None:
    device = Mock()
    cancel = Mock()
    cancel.exists = False
    network = Mock()
    network.click_exists.return_value = True
    device.side_effect = lambda **kwargs: (
        cancel if kwargs.get("resourceId") == WelcomeWlanUI.CANCEL_RESOURCE_ID else network
    )
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_wlan_list = Mock()
    page.wait_for_ssid = Mock(return_value=True)

    page.open_connected_network_details("target-ssid")

    page.wait_for_ssid.assert_called_once_with("target-ssid")
    network.click_exists.assert_called_once_with(timeout=5.0)
    device.assert_any_call(resourceId=WelcomeWlanUI.SSID_RESOURCE_ID, text="target-ssid")


def test_delete_network_from_details_scrolls_dialog_to_delete_button() -> None:
    device = Mock()
    details_scroll = Mock()
    details_scroll.wait.return_value = True
    details_scroll.scroll.to.return_value = True
    delete = Mock()
    delete.click_exists.return_value = True
    device.side_effect = lambda **kwargs: (
        details_scroll
        if kwargs.get("resourceId") == WelcomeWlanUI.DETAILS_SCROLL_RESOURCE_ID
        else delete
    )
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.delete_network_from_details()

    details_scroll.scroll.to.assert_called_once_with(text=WelcomeWlanUI.DELETE_NETWORK_TEXT)
    delete.click_exists.assert_called_once_with(timeout=5.0)


@pytest.mark.parametrize("scroll_exists, cancel_exists", ((True, True), (False, True), (True, False)))
def test_is_network_config_open_does_not_require_password_in_viewport(
    scroll_exists, cancel_exists
) -> None:
    device = Mock()
    password = Mock()
    password.exists = False
    scroll = Mock()
    scroll.exists = scroll_exists
    cancel = Mock()
    cancel.exists = cancel_exists
    selectors = {
        WelcomeWlanUI.PASSWORD_RESOURCE_ID: password,
        WelcomeWlanUI.CONFIG_SCROLL_RESOURCE_ID: scroll,
        WelcomeWlanUI.CANCEL_RESOURCE_ID: cancel,
    }
    device.side_effect = lambda **kwargs: selectors[kwargs["resourceId"]]
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page.is_network_config_open() is (scroll_exists and cancel_exists)


def test_cancel_network_config_accepts_welcome_page_with_no_visible_ssids() -> None:
    device = Mock()
    cancel = Mock()
    cancel.click_exists.return_value = True
    device.return_value = cancel
    device.app_current.return_value = {"package": WelcomeWlanUI.WELCOME_PACKAGE}
    page = WelcomeWlanUI(device, Path("artifacts"))
    page.is_network_config_open = Mock(return_value=False)
    page.dismiss_keyboard = Mock()
    page._wait_for_stable_bounds = Mock()

    page.cancel_network_config()

    cancel.click_exists.assert_called_once_with(timeout=5.0)
    page.dismiss_keyboard.assert_called_once_with()
    page._wait_for_stable_bounds.assert_called_once_with(cancel)
    device.app_current.assert_called_once_with()


def test_static_field_lookup_does_not_start_native_search_for_missing_alias() -> None:
    device = Mock()
    label = Mock()
    label.exists = False
    config_scroll = Mock()
    config_scroll.exists = True
    config_scroll.scroll.to.return_value = False
    device.side_effect = lambda **kwargs: (
        label if "text" in kwargs else config_scroll
    )
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("IP地址") is None

    config_scroll.scroll.to.assert_not_called()


def test_find_static_field_checks_all_aliases_before_scrolling() -> None:
    page = WelcomeWlanUI(Mock(), Path("artifacts"))
    field = Mock()
    page._field_next_to_label = Mock(side_effect=(None, field))
    page._swipe_in_bounds = Mock()

    assert page._find_static_field("dns2") is field
    assert page._field_next_to_label.call_args_list == [call("DNS2"), call("DNS 2")]
    page._swipe_in_bounds.assert_not_called()


@pytest.mark.parametrize("found", (False, True))
def test_find_static_field_scrolls_dialog_in_both_directions_with_a_limit(found) -> None:
    device = Mock()
    device.return_value.exists = True
    bounds = {"left": 601, "top": 200, "right": 1319, "bottom": 700}
    device.return_value.info = {"bounds": bounds}
    device.dump_hierarchy.return_value = "<hierarchy />"
    page = WelcomeWlanUI(device, Path("artifacts"))
    field = Mock()
    page._field_next_to_label = Mock(
        side_effect=(None, None, field) if found else None,
        return_value=None,
    )
    page._swipe_in_bounds = Mock()

    assert page._find_static_field("dns2") is (field if found else None)
    expected = [call(bounds, forward=True)]
    if not found:
        expected.append(call(bounds, forward=False))
    assert page._swipe_in_bounds.call_args_list == expected
    device.return_value.scroll.to.assert_not_called()


@pytest.mark.parametrize("shown", (False, True))
def test_dismiss_keyboard_only_presses_back_when_input_is_shown(shown) -> None:
    device = Mock()
    device.shell.side_effect = [
        Mock(exit_code=0, output=f"mInputShown={str(shown).lower()}\n mIsInputViewShown=true"),
        Mock(exit_code=0, output="mInputShown=false\n mIsInputViewShown=true"),
    ]
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.dismiss_keyboard()

    assert device.shell.call_args_list == [call("dumpsys input_method")] * (2 if shown else 1)
    if shown:
        device.press.assert_called_once_with("back")
    else:
        device.press.assert_not_called()


def test_dismiss_keyboard_waits_for_delayed_hide_without_a_second_back(monkeypatch) -> None:
    device = Mock()
    device.shell.side_effect = [
        Mock(exit_code=0, output=f"mInputShown={state}")
        for state in ("true", "true", "false")
    ]
    monkeypatch.setattr("core.libs.android.wifi_ui.welcome_page.time.sleep", Mock())
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.dismiss_keyboard()

    device.press.assert_called_once_with("back")
    assert device.shell.call_count == 3


def test_wait_for_stable_bounds_tracks_dialog_resize(monkeypatch) -> None:
    device = Mock()
    selector = Mock()
    first = {"left": 601, "top": 200, "right": 1319, "bottom": 600}
    final = {"left": 601, "top": 300, "right": 1319, "bottom": 800}
    info = PropertyMock(side_effect=[
        {"bounds": first}, {"bounds": final}, {"bounds": final},
        {"bounds": final}, {"bounds": final},
    ])
    type(selector).info = info
    monkeypatch.setattr("core.libs.android.wifi_ui.welcome_page.time.sleep", Mock())
    page = WelcomeWlanUI(device, Path("artifacts"))

    page._wait_for_stable_bounds(selector)

    assert info.call_count == 5


@pytest.mark.parametrize("exit_code, output", ((1, ""), (0, "unknown IME state")))
def test_dismiss_keyboard_reports_unavailable_state_instead_of_closing_dialog(
    exit_code, output
) -> None:
    device = Mock()
    device.shell.return_value.exit_code = exit_code
    device.shell.return_value.output = output
    page = WelcomeWlanUI(device, Path("artifacts"))
    page.fail_with_artifacts = Mock(side_effect=AssertionError("IME state unavailable"))

    with pytest.raises(AssertionError, match="IME state unavailable"):
        page.dismiss_keyboard()
    device.press.assert_not_called()


def test_static_field_lookup_matches_overlapping_spaced_dns_field() -> None:
    device = Mock()
    label = Mock()
    label.exists = True
    label.info = {"bounds": {"left": 40, "top": 500, "right": 150, "bottom": 540}}
    dns1_field = Mock()
    dns1_field.info = {"bounds": {"left": 180, "top": 490, "right": 700, "bottom": 550}}
    dns2_field = Mock()
    dns2_field.info = {"bounds": {"left": 180, "top": 560, "right": 700, "bottom": 620}}
    fields = MagicMock()
    fields.count = 2
    fields.__getitem__.side_effect = (dns1_field, dns2_field)
    device.side_effect = lambda **kwargs: (
        label if kwargs.get("text") == "DNS 1" else fields
    )
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("DNS 1") is dns1_field


def test_static_field_lookup_scrolls_when_dns_field_is_clipped_by_keyboard() -> None:
    device = Mock()
    clipped_label = Mock()
    clipped_label.exists = True
    clipped_label.info = {
        "bounds": {"left": 88, "top": 522, "right": 166, "bottom": 555}
    }
    visible_label = Mock()
    visible_label.exists = True
    visible_label.info = {
        "bounds": {"left": 88, "top": 418, "right": 166, "bottom": 451}
    }
    labels = iter((clipped_label, visible_label))

    clipped_fields = MagicMock()
    clipped_fields.count = 1
    prefix_field = Mock()
    prefix_field.info = {
        "bounds": {"left": 88, "top": 390, "right": 632, "bottom": 474}
    }
    clipped_fields.__getitem__.return_value = prefix_field
    visible_fields = MagicMock()
    visible_fields.count = 1
    dns1_field = Mock()
    dns1_field.info = {
        "bounds": {"left": 88, "top": 467, "right": 632, "bottom": 551}
    }
    visible_fields.__getitem__.return_value = dns1_field
    fields = iter((clipped_fields, visible_fields))

    config_scroll = Mock()
    config_scroll.exists = True
    config_scroll.info = {
        "bounds": {"left": 40, "top": 347, "right": 680, "bottom": 555}
    }

    def selector(**kwargs):
        if kwargs.get("text") == "DNS 1":
            return next(labels)
        if kwargs.get("className") == "android.widget.EditText":
            return next(fields)
        return config_scroll

    device.side_effect = selector
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("DNS 1") is dns1_field
    device.swipe.assert_called_once_with(360, 529, 360, 425, duration=0.2)


def test_static_field_lookup_prefers_edit_text_on_gateway_label_row() -> None:
    device = Mock()
    label = Mock()
    label.exists = True
    label.info = {"bounds": {"left": 40, "top": 400, "right": 150, "bottom": 440}}
    ip_address_field = Mock()
    ip_address_field.info = {"bounds": {"left": 180, "top": 350, "right": 700, "bottom": 390}}
    gateway_field = Mock()
    gateway_field.info = {"bounds": {"left": 180, "top": 400, "right": 700, "bottom": 440}}
    fields = MagicMock()
    fields.count = 2
    fields.__getitem__.side_effect = (ip_address_field, gateway_field)
    device.side_effect = lambda **kwargs: (
        label if kwargs.get("text") == "网关" else fields
    )
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("网关") is gateway_field


def test_static_field_lookup_does_not_fall_back_to_another_row() -> None:
    device = Mock()
    label = Mock()
    label.exists = True
    label.info = {"bounds": {"left": 40, "top": 500, "right": 150, "bottom": 540}}
    gateway_field = Mock()
    gateway_field.info = {
        "bounds": {"left": 180, "top": 400, "right": 700, "bottom": 440}
    }
    fields = MagicMock()
    fields.count = 1
    fields.__getitem__.return_value = gateway_field
    device.side_effect = lambda **kwargs: label if kwargs.get("text") else fields
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("网络前缀长度") is None


def test_static_field_lookup_matches_edit_text_below_prefix_label() -> None:
    device = Mock()
    label = Mock()
    label.exists = True
    label.info = {"bounds": {"left": 88, "top": 660, "right": 256, "bottom": 702}}
    gateway_field = Mock()
    gateway_field.info = {
        "bounds": {"left": 88, "top": 528, "right": 632, "bottom": 612}
    }
    prefix_field = Mock()
    prefix_field.info = {
        "bounds": {"left": 88, "top": 718, "right": 632, "bottom": 802}
    }
    fields = MagicMock()
    fields.count = 2
    fields.__getitem__.side_effect = (gateway_field, prefix_field)
    device.side_effect = lambda **kwargs: label if kwargs.get("text") else fields
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page._field_next_to_label("网络前缀长度") is prefix_field


def test_set_static_field_clears_value_when_default_hint_is_displayed() -> None:
    device = Mock()
    field = Mock()
    field.info = {
        "bounds": {"left": 10, "top": 20, "right": 110, "bottom": 60},
        "hint": "请输入 IP 地址",
        "text": "",
    }
    field.get_text.return_value = "请输入 IP 地址"
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_static_field = Mock(return_value=field)
    page.dismiss_keyboard = Mock()

    assert page.set_static_field("ip_address", "") == ""

    field.clear_text.assert_called_once_with()
    field.set_text.assert_not_called()
    page.dismiss_keyboard.assert_called_once_with()


def test_set_static_field_empty_value_ignores_displayed_placeholder_text() -> None:
    device = Mock()
    field = Mock()
    field.info = {
        "bounds": {"left": 10, "top": 20, "right": 110, "bottom": 60},
        "hint": "请输入网关",
        "text": "192.168.1.1",
    }
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_static_field = Mock(return_value=field)
    page.dismiss_keyboard = Mock()

    assert page.set_static_field("gateway", "") == ""

    field.clear_text.assert_called_once_with()
    device.shell.assert_not_called()
    page.dismiss_keyboard.assert_called_once_with()


def test_set_static_field_skips_repeated_lookup_for_invalid_dns_value() -> None:
    device = Mock()
    initial_field = Mock()
    initial_field.info = {
        "bounds": {"left": 88, "top": 467, "right": 632, "bottom": 551},
        "resourceName": "com.sunmi.welcome:id/et_dns1",
    }
    focused_field = Mock()
    device.return_value = focused_field
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_static_field = Mock(return_value=initial_field)
    page.dismiss_keyboard = Mock()

    assert page.set_static_field("dns1", "~!", verify_readback=False) == "~!"

    page._require_static_field.assert_called_once_with("dns1")
    device.assert_called_once_with(resourceId="com.sunmi.welcome:id/et_dns1")
    focused_field.clear_text.assert_called_once_with()
    focused_field.set_text.assert_called_once_with("~!")
    focused_field.get_text.assert_not_called()
    page.dismiss_keyboard.assert_called_once_with()


def test_clear_static_field_clears_located_field_without_button_coordinates() -> None:
    device = Mock()
    field = Mock()
    field.info = {"bounds": {"left": 10, "top": 20, "right": 110, "bottom": 60}}
    field.get_text.side_effect = ("192.168.1.2", "")
    clear = Mock()
    clear.exists = False
    device.return_value = clear
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._require_static_field = Mock(return_value=field)

    page.clear_static_field_with_button("ip_address")

    field.clear_text.assert_called_once_with()
    device.window_size.assert_not_called()
    device.long_click.assert_not_called()


def test_enter_password_accepts_plaintext_readback() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = True
    password_field.get_text.return_value = "P1ss!@#Mix16Chars"
    device.return_value = password_field
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page.enter_password("P1ss!@#Mix16Chars")
    password_field.set_text.assert_called_once_with("P1ss!@#Mix16Chars")


def test_enter_password_accepts_equal_length_masked_readback() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = True
    password_field.get_text.return_value = "••••••••"
    device.return_value = password_field
    page = WelcomeWlanUI(device, Path("artifacts"))

    assert page.enter_password("24681357")


def test_clear_password_and_get_connect_button_state() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = True
    connect_button = Mock()
    connect_button.wait.return_value = True
    connect_button.info = {"enabled": False}
    device.side_effect = (password_field, connect_button)
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.clear_password()
    assert not page.is_connect_enabled()
    password_field.clear_text.assert_called_once()


def test_connect_network_clicks_connect_button() -> None:
    device = Mock()
    connect_button = Mock()
    connect_button.click_exists.return_value = True
    device.return_value = connect_button
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.connect_network()

    connect_button.click_exists.assert_called_once_with(timeout=5.0)


def test_clear_password_with_button_accepts_password_hint() -> None:
    device = Mock()
    clear_button = Mock()
    clear_button.click_exists.return_value = True
    password_field = Mock()
    password_field.wait.return_value = True
    password_field.get_text.return_value = WelcomeWlanUI.PASSWORD_HINT_TEXT
    device.side_effect = (clear_button, password_field)
    page = WelcomeWlanUI(device, Path("artifacts"))

    page.clear_password_with_button()

    clear_button.click_exists.assert_called_once_with(timeout=5.0)


def test_ip_mode_options_waits_for_both_options() -> None:
    device = Mock()
    selector = Mock()
    selector.click_exists.return_value = True
    dhcp_option = Mock()
    dhcp_option.wait.return_value = True
    dhcp_option.exists = True
    dhcp_option.click_exists.return_value = True
    static_option = Mock()
    static_option.wait.return_value = True
    static_option.exists = True
    selectors = {
        WelcomeWlanUI.IP_SELECTOR_RESOURCE_ID: selector,
        WelcomeWlanUI.DHCP_IP_RESOURCE_ID: dhcp_option,
        WelcomeWlanUI.STATIC_IP_RESOURCE_ID: static_option,
    }
    device.side_effect = lambda **kwargs: selectors[kwargs["resourceId"]]
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._wait_for_stable_bounds = Mock()

    assert page.ip_mode_options() == {"DHCP", "静态"}

    dhcp_option.wait.assert_called_once_with(timeout=5.0)
    static_option.wait.assert_called_once_with(timeout=5.0)
    dhcp_option.click_exists.assert_called_once_with(timeout=1.0)


def test_select_ip_mode_retries_when_option_is_not_initially_shown() -> None:
    device = Mock()
    selector = Mock()
    selector.click_exists.return_value = True
    static_option = Mock()
    static_option.click_exists.side_effect = (False, True)
    mode_text = Mock()
    mode_text.wait.return_value = True
    mode_text.get_text.return_value = "静态"
    selectors = {
        WelcomeWlanUI.IP_SELECTOR_RESOURCE_ID: selector,
        WelcomeWlanUI.STATIC_IP_RESOURCE_ID: static_option,
        WelcomeWlanUI.IP_MODE_TEXT_RESOURCE_ID: mode_text,
    }
    device.side_effect = lambda **kwargs: selectors[kwargs["resourceId"]]
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._wait_for_stable_bounds = Mock()

    page.select_ip_mode("静态")

    assert selector.click_exists.call_count == 2
    assert static_option.click_exists.call_count == 2


def test_password_visibility_and_ip_mode_controls() -> None:
    device = Mock()
    password_field = Mock()
    password_field.wait.return_value = True
    password_field.get_text.return_value = "••••••••"
    visibility = Mock()
    visibility.wait.return_value = True
    visibility.info = {"checked": False}
    def show_password() -> None:
        visibility.info["checked"] = True
        password_field.get_text.return_value = "24681357"

    visibility.click.side_effect = show_password
    options = Mock()
    options.wait.return_value = True
    options.info = {"checked": False}
    ip_selector = Mock()
    ip_selector.wait.return_value = True
    ip_selector.click_exists.return_value = True
    ip_mode_text = Mock()
    ip_mode_text.wait.return_value = True
    ip_mode_text.get_text.side_effect = ("DHCP", "静态")
    static_option = Mock()
    static_option.click_exists.return_value = True
    selectors = {
        WelcomeWlanUI.PASSWORD_RESOURCE_ID: password_field,
        WelcomeWlanUI.PASSWORD_VISIBILITY_RESOURCE_ID: visibility,
        WelcomeWlanUI.ADVANCED_OPTIONS_RESOURCE_ID: options,
        WelcomeWlanUI.IP_SELECTOR_RESOURCE_ID: ip_selector,
        WelcomeWlanUI.IP_MODE_TEXT_RESOURCE_ID: ip_mode_text,
        WelcomeWlanUI.STATIC_IP_RESOURCE_ID: static_option,
    }
    device.side_effect = lambda **kwargs: selectors[kwargs["resourceId"]]
    page = WelcomeWlanUI(device, Path("artifacts"))
    page._wait_for_stable_bounds = Mock()

    assert page.is_password_masked()
    page.toggle_password_visibility()
    assert visibility.info["checked"]
    assert not page.is_password_masked()
    page.open_advanced_options()
    assert page.current_ip_mode() == "DHCP"
    page.select_ip_mode("静态")

    visibility.wait.assert_called_once_with(timeout=5.0)
    visibility.click.assert_called_once()
    options.click.assert_called_once()
    static_option.click_exists.assert_called_once_with(timeout=5.0)