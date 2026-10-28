"""WiFi 连接 — Func_Components_Settings_ConnCfg（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/组件.md
"""
from __future__ import annotations

import pytest

from core.contracts.wifi_test_case import WifiTestCase
from core.libs.android.wifi_scenarios.connection_config import run_connection_config_case
from testcases.support.skip import run_manual_placeholder

_AP_PRE = "1、设备恢复出厂 2、陪测试设备为AP"


def _case_param(
    case_id: str,
    title: str,
    tag: str,
    operation: str | None,
    *,
    hyper: bool = False,
    pre: str = _AP_PRE,
    status: str = "implemented",
):
    marks = [
        pytest.mark.p2,
        getattr(pytest.mark, tag.lower()),
        pytest.mark.case_id(case_id),
    ]
    if status == "manual":
        marks.append(pytest.mark.manual_placeholder)
    return pytest.param(
        WifiTestCase(case_id=case_id, title=title, tag=tag, pre=pre),
        operation,
        hyper,
        id=case_id,
        marks=marks,
    )


@pytest.mark.parametrize(
    ("case", "operation", "hyper"),
    (
        _case_param("Func_Components_Settings_ConnCfg_UI_001", "点击HyperWiFi-logo跳转界面检查", "hyperwifi", "hyperwifi_intro", hyper=True, pre="1、设备恢复出厂 2、陪测试设备为miniAP"),
        _case_param("Func_Components_Settings_ConnCfg_UI_002", "open网络连接无“配置框”弹出检查", "common", "open_no_dialog"),
        _case_param("Func_Components_Settings_ConnCfg_UI_003", "加密网络连接“配置框”弹出检查", "common", "dialog"),
        _case_param("Func_Components_Settings_ConnCfg_UI_004", "加密网络连接“配置框”信息检查", "common", "dialog_info"),
        _case_param("Func_Components_Settings_ConnCfg_UI_005", "密码输入为空，“连接按键”置灰", "common", "empty_password"),
        _case_param("Func_Components_Settings_ConnCfg_UI_006", "密码长度<8位报错", "hyperwifi", "min_password", hyper=True),
        _case_param("Func_Components_Settings_ConnCfg_UI_007", "密码长度>32位报错-HyperWiFi", "hyperwifi", "max_password", hyper=True),
        _case_param("Func_Components_Settings_ConnCfg_UI_008", "密码长度>64位输入-WiFi", "wifi", "max_password"),
        _case_param("Func_Components_Settings_ConnCfg_UI_009", "密码输入框明文/密文切换按钮", "common", "visibility"),
        _case_param("Func_Components_Settings_ConnCfg_UI_010", "密码输入框“删除”按钮有效", "common", "clear"),
        _case_param("Func_Components_Settings_ConnCfg_UI_011", "密码输入框“取消”按钮有效", "common", "cancel"),
        _case_param("Func_Components_Settings_ConnCfg_UI_012", "密码输入框“连接”按钮有效", "common", "connect"),
        _case_param("Func_Components_Settings_ConnCfg_UI_013", "高级选项-IP设置", "common", "advanced"),
        _case_param("Func_Components_Settings_ConnCfg_UI_014", "再次点击“密码错误”提示的无线-配置框自动弹出", "common", "wrong_password_reopen"),
    ),
)
def test_connection_config(
    request,
    run_shell_cmd,
    wifi,
    wifi_yaml,
    case: WifiTestCase,
    operation: str | None,
    hyper: bool,
):
    """Run one declarative WLAN connection-configuration case."""
    if operation is None:
        run_manual_placeholder(case)
        return

    settings_ui = request.getfixturevalue("settings_ui")
    run_connection_config_case(
        case.case_id,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        settings_ui,
        operation=operation,
        hyper=hyper,
    )
