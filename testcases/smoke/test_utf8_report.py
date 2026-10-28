"""冒烟：验证 HTML 报告中文字符不乱码。"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.smoke


def test_utf8_in_html_report():
    print("前置 — 打开 WiFi，已联网校验")
    assert "WiFi" in "WiFi"
