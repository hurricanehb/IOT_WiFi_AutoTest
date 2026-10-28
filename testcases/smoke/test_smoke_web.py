"""Web 冒烟占位：接入浏览器驱动后在此编写用例。"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.p3
@pytest.mark.case_id("SMOKE-WEB-PLACEHOLDER-001")
@pytest.mark.skip(reason="尚未接入 Web / Playwright 等依赖")
def test_web_home_placeholder():
    """【用例ID】SMOKE-WEB-PLACEHOLDER-001\nWeb 首页占位（非 WLAN 域，不加 wlan）。"""
    assert True
