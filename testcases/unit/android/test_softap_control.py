from __future__ import annotations

from types import SimpleNamespace

import pytest

from core.libs.android.softap_control import SoftAPControl


def test_find_labeled_bounds_uses_normalized_exact_label() -> None:
    control = object.__new__(SoftAPControl)
    hierarchy = """
        <hierarchy>
            <node text="自动关闭热点" bounds="[0,0][400,80]" />
            <node content-desc="WLAN 热点" bounds="[0,100][400,180]" />
        </hierarchy>
    """

    assert control._find_labeled_bounds(hierarchy, "WLAN热点") == (0, 100, 400, 180)


@pytest.mark.parametrize(
    ("title", "first", "second"),
    [
        ("速度和兼容性", "2.4GHz", "5GHz"),
        ("AP Band", "2.4 GHz频段", "首选5.0 GHz频段"),
    ],
)
def test_compatibility_editor_normalizes_band_options(title, first, second) -> None:
    control = object.__new__(SoftAPControl)
    hierarchy = f"""
        <hierarchy>
            <node text="{title}" bounds="[0,0][400,80]" />
            <node text="{first}" checkable="true" checked="true"
                  bounds="[0,100][400,180]" />
            <node text="{second}" checkable="true" checked="false"
                  bounds="[0,200][400,280]" />
        </hierarchy>
    """
    control.device = SimpleNamespace(dump_hierarchy=lambda: hierarchy)

    assert control.open_compatibility_editor() == (["2.4GHz", "5GHz"], "2.4GHz")


def test_compatibility_summary_uses_preference_row_not_title() -> None:
    control = object.__new__(SoftAPControl)
    hierarchy = """
        <hierarchy>
            <node clickable="true" bounds="[0,0][400,100]">
                <node resource-id="android:id/title" text="热点名称"
                      bounds="[20,0][300,40]" />
                <node resource-id="android:id/summary" text="Lab 5GHz"
                      bounds="[20,40][300,80]" />
            </node>
            <node clickable="true" bounds="[0,100][400,200]">
                <node resource-id="android:id/title" text="项目自定义频段标题"
                      bounds="[20,100][300,140]" />
                <node resource-id="android:id/summary" text="2.4 GHz频段"
                      bounds="[20,140][300,180]" />
            </node>
        </hierarchy>
    """
    control.device = SimpleNamespace(dump_hierarchy=lambda: hierarchy)

    assert control.compatibility_summary() == "2.4GHz频段"


@pytest.mark.parametrize("title", ["AP Band", "速度与兼容性", "新项目频段设置"])
def test_open_compatibility_editor_taps_own_preference_row(title) -> None:
    control = object.__new__(SoftAPControl)
    settings = f"""
        <hierarchy>
            <node clickable="true" bounds="[0,0][400,100]">
                <node resource-id="android:id/title" text="热点名称"
                      bounds="[20,0][300,40]" />
                <node resource-id="android:id/summary" text="Lab 5GHz"
                      bounds="[20,40][300,80]" />
            </node>
            <node clickable="true" bounds="[0,100][400,200]">
                <node resource-id="com.android.settings:id/title" text="{title}"
                      bounds="[20,100][300,140]" />
                <node resource-id="com.android.settings:id/summary" text="2.4 GHz频段"
                      bounds="[20,140][300,180]" />
            </node>
        </hierarchy>
    """
    dialog = """
        <hierarchy>
            <node text="AP Band" bounds="[0,0][400,80]" />
            <node text="2.4 GHz频段" bounds="[20,100][300,180]" />
            <node checkable="true" checked="false" bounds="[320,100][380,180]" />
            <node text="首选5.0 GHz频段" bounds="[20,200][300,280]" />
            <node checkable="true" checked="true" bounds="[320,200][380,280]" />
        </hierarchy>
    """
    taps = []
    control.adb = SimpleNamespace(tap=lambda *point: taps.append(point))
    control.device = SimpleNamespace(dump_hierarchy=lambda: dialog if taps else settings)

    assert control.open_compatibility_editor() == (["2.4GHz", "5GHz"], "5GHz")
    assert taps == [(200, 150)]


def test_open_compatibility_editor_keeps_label_only_fallback() -> None:
    control = object.__new__(SoftAPControl)
    settings = '<hierarchy><node text="AP Band" bounds="[0,0][400,80]" /></hierarchy>'
    dialog = """
        <hierarchy>
            <node text="2.4GHz" checkable="true" checked="true" bounds="[0,0][400,80]" />
            <node text="5GHz" checkable="true" checked="false" bounds="[0,100][400,180]" />
        </hierarchy>
    """
    taps = []
    control.adb = SimpleNamespace(tap=lambda *point: taps.append(point))
    control.device = SimpleNamespace(dump_hierarchy=lambda: dialog if taps else settings)

    assert control.open_compatibility_editor() == (["2.4GHz", "5GHz"], "2.4GHz")
    assert taps == [(200, 40)]


@pytest.mark.parametrize("summary", ["2.4GHz", "2.4 GHz频段", "首选5.0 GHz频段"])
def test_compatibility_summary_prefers_known_title_over_ssid(summary) -> None:
    control = object.__new__(SoftAPControl)
    hierarchy = f"""
        <hierarchy>
            <node bounds="[0,0][400,100]">
                <node resource-id="android:id/title" text="热点名称" bounds="[0,0][300,40]" />
                <node resource-id="android:id/summary" text="5GHz" bounds="[0,40][300,80]" />
            </node>
            <node bounds="[0,100][400,200]">
                <node resource-id="android:id/title" text="AP Band" bounds="[0,100][300,140]" />
                <node resource-id="android:id/summary" text="{summary}" bounds="[0,140][300,180]" />
            </node>
        </hierarchy>
    """
    control.device = SimpleNamespace(dump_hierarchy=lambda: hierarchy)

    assert control.compatibility_summary() == summary.replace(" ", "").replace("5.0GHz", "5GHz")


def test_compatibility_setting_rejects_ambiguous_unknown_titles() -> None:
    control = object.__new__(SoftAPControl)
    rows = "".join(
        f'<node bounds="[0,{index * 100}][400,{index * 100 + 100}]">'
        f'<node resource-id="android:id/title" text="Custom {index}" />'
        '<node resource-id="android:id/summary" text="5GHz" />'
        '</node>'
        for index in range(2)
    )

    with pytest.raises(ValueError, match="无法唯一定位"):
        control._compatibility_setting(f"<hierarchy>{rows}</hierarchy>")


def test_security_editor_still_reads_all_options_in_visual_order() -> None:
    control = object.__new__(SoftAPControl)
    rows = "".join(
        f'<node text="{option}" checkable="true" checked="{str(index == 1).lower()}" '
        f'bounds="[0,{index * 100}][400,{index * 100 + 80}]" />'
        for index, option in enumerate(SoftAPControl._SECURITY_OPTIONS)
    )
    control.device = SimpleNamespace(dump_hierarchy=lambda: f"<hierarchy>{rows}</hierarchy>")

    assert control.open_security_editor() == (
        list(SoftAPControl._SECURITY_OPTIONS), "WPA2/WPA3-Personal"
    )


def test_band_editor_does_not_hide_new_or_missing_options() -> None:
    control = object.__new__(SoftAPControl)
    hierarchy = """
        <hierarchy>
            <node text="2.4GHz" checkable="true" checked="true" bounds="[0,0][400,80]" />
            <node text="6.0 GHz频段" checkable="true" checked="false" bounds="[0,100][400,180]" />
        </hierarchy>
    """
    control.device = SimpleNamespace(dump_hierarchy=lambda: hierarchy)

    assert control.open_compatibility_editor() == (["2.4GHz", "6GHz"], "2.4GHz")