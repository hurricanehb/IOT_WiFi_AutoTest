from PIL import Image, ImageDraw

from core.libs.android.wifi_scenarios.wifi_icon_image import (
    has_h_glyph,
    has_hyper_badge,
)
from core.libs.android.wifi_scenarios.settings.wifi_icon import (
    wifi_icon_rows,
    wifi_standard_generations,
)


def test_wifi_icon_rows_extracts_standard_and_hyper_resources() -> None:
    hierarchy = """
<hierarchy><node>
  <node clickable="true" content-desc="Lab_AP,[{aa=5180,-50,Wi-Fi 6,1s}]">
    <node text="Lab_AP" resource-id="android:id/title" />
    <node resource-id="android:id/icon" bounds="[632,100][680,148]" />
  </node>
  <node clickable="true" content-desc="Hyper_AP,WPA3(SAE)">
    <node text="Hyper_AP" resource-id="android:id/title" />
    <node resource-id="com.android.settings:id/turbolink_button" bounds="[470,200][552,248]" />
    <node resource-id="android:id/icon" bounds="[632,200][680,248]" />
  </node>
</node></hierarchy>
"""

    rows = wifi_icon_rows(hierarchy)

    assert [row.ssid for row in rows] == ["Lab_AP", "Hyper_AP"]
    assert wifi_standard_generations(rows) == {6}
    assert "com.android.settings:id/turbolink_button" in rows[1].resources


def test_hyper_badge_requires_dark_background_and_light_text() -> None:
    image = Image.new("L", (82, 48), 128)
    ImageDraw.Draw(image).rectangle((10, 10, 70, 16), fill=255)

    assert has_hyper_badge(image, (0, 0, 82, 48))
    assert not has_hyper_badge(Image.new("L", (82, 48), 255), (0, 0, 82, 48))


def test_h_glyph_rejects_digit_six_shape() -> None:
    h_icon = Image.new("L", (48, 48), 255)
    draw = ImageDraw.Draw(h_icon)
    draw.rectangle((1, 27, 3, 39), fill=128)
    draw.rectangle((8, 27, 10, 39), fill=128)
    draw.rectangle((1, 33, 10, 35), fill=128)
    six_icon = Image.new("L", (48, 48), 255)
    draw = ImageDraw.Draw(six_icon)
    draw.ellipse((1, 27, 10, 39), outline=128, width=3)

    assert has_h_glyph(h_icon, (0, 0, 48, 48))
    assert not has_h_glyph(six_icon, (0, 0, 48, 48))