"""Shared image classifiers for product WiFi icon decorations."""
from __future__ import annotations

from typing import cast

from PIL import Image


def has_hyper_badge(image: Image.Image, bounds: tuple[int, int, int, int]) -> bool:
    crop = image.convert("L").crop(bounds).resize((82, 48))
    pixels = [
        cast(int, crop.getpixel((x, y)))
        for y in range(crop.height)
        for x in range(crop.width)
    ]
    dark_ratio = sum(value < 180 for value in pixels) / len(pixels)
    light_ratio = sum(value > 220 for value in pixels) / len(pixels)
    return dark_ratio >= 0.55 and light_ratio >= 0.08


def has_h_glyph(image: Image.Image, bounds: tuple[int, int, int, int]) -> bool:
    crop = image.convert("L").crop(bounds).resize((48, 48))

    def is_dark(x: int, y: int) -> bool:
        return cast(int, crop.getpixel((x, y))) < 200

    column_counts = [
        sum(is_dark(x, y) for y in range(27, 40))
        for x in range(16)
    ]
    left_bar = max(column_counts[1:4], default=0)
    right_bar = min(column_counts[8:11], default=0)
    bridge = sum(
        is_dark(x, y)
        for x in range(1, 11)
        for y in range(33, 36)
    )
    return left_bar >= 9 and right_bar >= 8 and bridge >= 24
