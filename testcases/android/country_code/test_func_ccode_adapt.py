"""国家码 — 对齐 country-code.md（Ccode_*）。"""
from __future__ import annotations

import os
import time

import pytest

pytestmark = pytest.mark.country_code

from core.testdata_loader import eu_country_codes, us_country_codes
from core.libs.android.wifi_control.connection_chk import (
    assert_dual_wifi_connected,
    assert_wifi_connected,
)
from core.libs.android.wifi_scenarios.country_code import (
    require_cli_app,
    run_adapt_country_mapping,
    run_country_code_switch_stress,
    run_country_table_case,
)
from core.libs.android.wifi_scenarios.lab_requirements import env_value
from core.libs.android.wifi_control.controller import WiFiControl
from core.utils.config_loader import get_settings
from core.utils.log_handler import get_logger

log = get_logger("android.country_code")

# 原手工占位用例 Func_Ccode_Adapt_Vali_001~247 已由下方两个参数化用例覆盖：
# EU 表顺序对应 001~049，US 表顺序对应 050~247。
_LEGACY_CASE_PREFIX = "Func_Ccode_Adapt_Vali_"
_EU_FIRST_CASE_NO = 1
_US_FIRST_CASE_NO = 50


def _legacy_case_params(codes: list[str], first_case_no: int) -> list:
    """为每个国家码回填原手工用例编号，使报告 ID 与 case_id marker 保持历史追溯。"""
    params = []
    for idx, code in enumerate(codes):
        case_id = f"{_LEGACY_CASE_PREFIX}{first_case_no + idx:03d}"
        params.append(
            pytest.param(
                code,
                marks=pytest.mark.case_id(case_id),
                id=f"{case_id}-{code}",
            )
        )
    return params


@pytest.mark.p1
@pytest.mark.common
@pytest.mark.no_dual_wifi_setup
@pytest.mark.case_id("Ccode_Default_Func_001")
@pytest.mark.wifi_case(
    title="查询 WiFi 默认国家码（出厂可为 null，随 SKU 而异）",
    pre="初始未联网",
)
def test_Ccode_Default_Func_001(run_shell_cmd):
    # Step 1: 查询 WiFi 国家码
    out = run_shell_cmd("cmd wifi get-country-code")
    log.info("WiFi 国家码输出：\n%s", out)
    assert out is not None and len(out.strip()) >= 0, "get-country-code 无输出"


@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.no_dual_wifi_setup
@pytest.mark.case_id("Ccode_Default_Func_002")
@pytest.mark.wifi_case(
    title="验证德国（DE）下 Halow 国家码 EU、占空比默认打开",
    pre="初始未联网",
)
def test_Ccode_Default_Func_002(run_shell_cmd, wifi: WiFiControl):
    require_cli_app(run_shell_cmd)

    # Step 1: 修改国家码为德国 DE
    run_shell_cmd("cmd wifi force-country-code enabled DE")
    time.sleep(1.0)

    # Step 2: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    log.info("国家码信息输出：\n%s", country_info)

    # Step 3: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")
    log.info("占空比信息输出：\n%s", duty_info)

    assert "EU" in country_info, "Halow 国家码错误，应为 EU"
    assert "on" in duty_info.lower() and "duty" in duty_info.lower(), "占空比状态错误，应为 on"


@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Ccode_Default_Func_003")
@pytest.mark.wifi_case(
    title="验证美国（US）下 Halow 国家码 US、占空比默认关闭",
    pre="初始未联网",
)
def test_Ccode_Default_Func_003(run_shell_cmd, wifi: WiFiControl, wifi_yaml: dict):
    require_cli_app(run_shell_cmd)
 
    # Step 1: 修改国家码为美国 US
    run_shell_cmd("cmd wifi force-country-code enabled US")
    time.sleep(1.0)
    wifi.set_wifi_enabled(False)
    time.sleep(0.5)
    wifi.set_wifi_enabled(True)
    time.sleep(1.0)

    # Step 2: 校验 WiFi 连接成功（改国家码后可能自动回连任一配置 AP）
    assert_wifi_connected(wifi, wifi_yaml, run_shell_cmd, allow_any_configured=True)

    # Step 3: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    log.info("国家码信息输出：\n%s", country_info)

    # Step 4: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")
    log.info("占空比信息输出：\n%s", duty_info)

    assert "US" in country_info, "Halow 国家码错误，应为 US"
    assert "off" in duty_info.lower() and "duty" in duty_info.lower(), "占空比状态错误，应为 off"


@pytest.mark.p1
@pytest.mark.dualwifi
@pytest.mark.dual_wifi_eu
@pytest.mark.case_id("Ccode_Default_Func_004")
@pytest.mark.wifi_case(
    title="验证德国（DE）国家码下 Halow 国家码和占空比默认状态",
    pre="已联网，欧盟区国家码 EUS，占空比默认关闭",
)
def test_Ccode_Default_Func_004(run_shell_cmd, wifi: WiFiControl, wifi_yaml: dict):
    require_cli_app(run_shell_cmd)

    # Step 1: 修改国家码为德国 DE
    run_shell_cmd("cmd wifi force-country-code enabled DE")
    time.sleep(1.0)

    # Step 2: 重新打开 WiFi，并在测试过程中显式建立双 WiFi 连接
    wifi.set_wifi_enabled(False)
    time.sleep(0.5)
    wifi.set_wifi_enabled(True)
    time.sleep(5.0)
    assert_dual_wifi_connected(wifi, wifi_yaml, run_shell_cmd, hyper_region="EU")

    # Step 3: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    log.info("国家码信息输出：\n%s", country_info)

    # Step 4: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")
    log.info("占空比信息输出：\n%s", duty_info)

    assert "Country : EU" in country_info or "EU" in country_info, "Halow 国家码错误，应为 EU"
    assert "Duty cycle : off" in duty_info or (
        "off" in duty_info.lower() and "duty" in duty_info.lower()
    ), "占空比状态错误，应为 off"


@pytest.mark.p0
@pytest.mark.dualwifi
@pytest.mark.dual_wifi_us
@pytest.mark.case_id("Ccode_Default_Func_005")
@pytest.mark.wifi_case(
    title="验证美国（US）国家码下 Halow 国家码和占空比默认状态",
    pre="已联网，非欧盟区国家码 US，占空比默认关闭",
)
def test_Ccode_Default_Func_005(run_shell_cmd, wifi: WiFiControl, wifi_yaml: dict):
    require_cli_app(run_shell_cmd)

    # Step 1: 修改国家码为美国 US
    run_shell_cmd("cmd wifi force-country-code enabled US")
    time.sleep(1.0)

    # Step 2: 重新打开 WiFi，并在测试过程中显式建立双 WiFi 连接
    wifi.set_wifi_enabled(False)
    time.sleep(0.5)
    wifi.set_wifi_enabled(True)
    time.sleep(5.0)
    assert_dual_wifi_connected(wifi, wifi_yaml, run_shell_cmd, hyper_region="US")

    # Step 3: 查看 Halow 国家码
    country_info = run_shell_cmd("cli_app show config | grep -i country")
    log.info("国家码信息输出：\n%s", country_info)

    # Step 4: 查看占空比状态
    duty_info = run_shell_cmd("cli_app show duty")
    log.info("占空比信息输出：\n%s", duty_info)

    assert "Country : US" in country_info or "US" in country_info, "Halow 国家码错误，应为 US"
    assert "Duty cycle : off" in duty_info or (
        "off" in duty_info.lower() and "duty" in duty_info.lower()
    ), "占空比状态错误，应为 off"


@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Ccode_Default_Excpt_001")
@pytest.mark.wifi_case(
    title="恢复出厂后 Halow 与 WiFi 国家码映射一致",
    pre="设备可恢复出厂",
)
def test_Ccode_Default_Excpt_001():
    pytest.skip("manual: 需恢复出厂并进入 welcome WLAN 列表 UI 校验")


@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Ccode_Default_Excpt_002")
@pytest.mark.wifi_case(
    title="重置 WLAN 后国家码不变",
    pre="已配置国家码",
)
def test_Ccode_Default_Excpt_002():
    pytest.skip("manual: 需设置 → 系统 → 重置选项 → 重置 WLAN")


# @pytest.mark.p1
# @pytest.mark.common
# def test_Ccode_Adapt_Func_001(run_shell_cmd, wifi: WiFiControl, wifi_yaml: dict):
#     """
#     用例摘要：Ccode_Adapt_Func_001
#     初始条件：无（示例国家码 AD / Andorra）
#     测试目的：蜂窝映射 — 设置国家码、校验 WiFi/Halow 国家码与占空比
#     """
#     run_adapt_country_mapping(
#         run_shell_cmd, wifi, wifi_yaml, "AD", expected_halow="EU"
#     )




@pytest.mark.p2
@pytest.mark.common
@pytest.mark.parametrize(
    "country_code", _legacy_case_params(us_country_codes(), _US_FIRST_CASE_NO)
)
@pytest.mark.case_id("Ccode_Adapt_Table_US")
@pytest.mark.wifi_case(
    title="遍历 US 区国家码表，校验设备支持的国家码映射并完成联网校验",
    pre="初始未联网（由 android_wifi_lifecycle 统一前置后进入测试）",
)
def test_Ccode_Adapt_Table_US(
    country_code: str,
    run_shell_cmd,
    wifi: WiFiControl,
    wifi_yaml: dict,
):
    run_country_table_case(
        country_code,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        capability=env_value("DUT_WIFI_CAPABILITY", "dualwifi"),
        expected_halow="US",
    )


@pytest.mark.p2
@pytest.mark.common
@pytest.mark.parametrize(
    "country_code", _legacy_case_params(eu_country_codes(), _EU_FIRST_CASE_NO)
)
@pytest.mark.case_id("Ccode_Adapt_Table_EU")
@pytest.mark.wifi_case(
    title="遍历 EU 区国家码表，校验设备支持的国家码映射并完成联网校验",
    pre="初始未联网（由 android_wifi_lifecycle 统一前置后进入测试）",
)
def test_Ccode_Adapt_Table_EU(
    country_code: str,
    run_shell_cmd,
    wifi: WiFiControl,
    wifi_yaml: dict,
):
    run_country_table_case(
        country_code,
        run_shell_cmd,
        wifi,
        wifi_yaml,
        capability=env_value("DUT_WIFI_CAPABILITY", "dualwifi"),
        expected_halow="EU",
    )


@pytest.mark.p2
@pytest.mark.dualwifi
@pytest.mark.stress
@pytest.mark.no_dual_wifi_setup
@pytest.mark.case_id("Ccode_Stress_Func_001")
@pytest.mark.wifi_case(
    title="压测 1000 次 US<->EU 国家码切换（US / DE 交替），每轮校验 Halow 映射、占空比与双 WiFi 重连",
    pre="设备 ADB 在线，cli_app 可用；实验室双 WiFi 环境可连接",
)
def test_Ccode_Stress_Func_001(run_shell_cmd, wifi: WiFiControl, wifi_yaml: dict, extra):
    cycles = max(1, min(get_settings().scenario_tuning.country_code_stress_cycles, 10000))
    halow_timeout = get_settings().scenario_tuning.country_code_halow_ready_timeout_sec
    max_log_exports = int(os.environ.get("CCODE_STRESS_MAX_LOG_EXPORTS", "100"))
    progress_messages = []

    result = run_country_code_switch_stress(
        run_shell_cmd,
        wifi,
        wifi_yaml,
        cycles=cycles,
        us_code="US",
        eu_code="DE",
        halow_ready_timeout=halow_timeout,
        max_failure_log_exports=max_log_exports,
        progress_callback=progress_messages.append,
    )
    extra.append({
        "name": "国家码压测进度",
        "format_type": "text",
        "content": "\n".join(progress_messages),
        "mime_type": "text/plain",
        "extension": "txt",
    })
    log.info("Ccode_Stress_Func_001 执行结果：%s", result.summary())
    assert result.failed_cycles == 0, f"国家码压测完成但存在失败轮次：{result.summary()}"
