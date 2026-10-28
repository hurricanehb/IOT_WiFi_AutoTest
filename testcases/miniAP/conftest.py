"""miniAP 域 Fixture。"""
from __future__ import annotations

import os

import pytest

from core.libs.access_points import MiniAPAction
from core.utils.config_loader import get_settings


@pytest.fixture(scope="session")
def miniap_settings():
    return get_settings()


@pytest.fixture
def miniap_action(miniap_settings) -> MiniAPAction:
    cfg = miniap_settings.miniAP_config
    if not (cfg.miniAP_ip or "").strip():
        pytest.skip("config/test_config.json 未配置 miniAP_config.miniAP_ip")
    if not (cfg.miniAP_login_password or "").strip():
        pytest.skip("未配置环境变量 MINIAP_LOGIN_PASSWORD（见 .env.example）")
    if os.environ.get("MINIAP_LAB") != "1":
        pytest.skip("miniAP Telnet 用例需实验室环境，设置 MINIAP_LAB=1")
    action = MiniAPAction(settings=miniap_settings)
    yield action
    action.close()
