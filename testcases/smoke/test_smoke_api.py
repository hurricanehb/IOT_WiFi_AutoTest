"""API 冒烟占位：接入真实 HTTP 接口后在此编写用例。"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.p3
@pytest.mark.case_id("SMOKE-API-PLACEHOLDER-001")
@pytest.mark.skip(reason="尚未配置被测 API 基址与鉴权")
def test_api_health_placeholder():
    """【用例ID】SMOKE-API-PLACEHOLDER-001\nAPI 健康检查占位（非 WLAN 域，不加 wlan）。"""
    assert True
