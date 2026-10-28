"""WiFi 连接 — Func_Ccode_Shell（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from core.libs.android.wifi_scenarios.country_code import assert_eus_duty_cycle, set_eus_duty_cycle


@pytest.fixture(autouse=True)
def restore_eus_default(run_shell_cmd):
    """每条用例结束后恢复默认：EUS=1，Duty cycle=off。"""
    yield
    set_eus_duty_cycle(run_shell_cmd, True)


@pytest.mark.p3
@pytest.mark.hyperwifi
@pytest.mark.parametrize(
    "country_code, duty_cycle_off, set_value",
    [
        pytest.param("EU", True, None, id="Func_Ccode_Shell_Vali_001_default_off", marks=pytest.mark.case_id("Func_Ccode_Shell_Vali_001")),
        pytest.param("EU", False, False, id="Func_Ccode_Shell_Vali_002_enable", marks=pytest.mark.case_id("Func_Ccode_Shell_Vali_002")),
        pytest.param("EU", True, True, id="Func_Ccode_Shell_Vali_003_disable", marks=pytest.mark.case_id("Func_Ccode_Shell_Vali_003")),
        pytest.param("US", True, True, id="Func_Ccode_Shell_Vali_004_us_off", marks=pytest.mark.case_id("Func_Ccode_Shell_Vali_004")),
    ],
)
def test_Func_Ccode_Shell_Vali(run_shell_cmd, country_code, duty_cycle_off, set_value):
    """通过 shell 设置国家码和 EUS 占空比，并回读验证结果。"""
    result = run_shell_cmd(f"cmd wifi force-country-code enabled {country_code}")
    print(f"cmd wifi force-country-code enabled {country_code}:\n{result}")
    actual = run_shell_cmd("cmd wifi get-country-code")
    print(f"cmd wifi get-country-code:\n{actual}")
    if set_value is None:
        assert_eus_duty_cycle(run_shell_cmd, duty_cycle_off)
    else:
        set_eus_duty_cycle(run_shell_cmd, set_value)
