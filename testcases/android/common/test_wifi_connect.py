"""WiFi 连接与 AI 辅助 — 通用连接能力。"""
from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, Optional, Type

import pytest

from core.libs.android.wifi_control.controller import WiFiControl


def _load_optional_ai_class(module_name: str, class_name: str) -> Optional[Type[Any]]:
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as error:
        if module_name.startswith(f"{error.name}."):
            return None
        raise
    return getattr(module, class_name)


AIWiFiCaseGenerator = _load_optional_ai_class(
    "core.ai.ai_wifi_case_gen", "AIWiFiCaseGenerator"
)
AIResultAnalyzer = _load_optional_ai_class(
    "core.ai.ai_result_analyze", "AIResultAnalyzer"
)
AIUILocator = _load_optional_ai_class("core.ai.ai_ui_locator", "AIUILocator")


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Conn_Toggle_001")
@pytest.mark.wifi_case(
    title="验证 WiFi 开关循环后 cmd wifi status 可正常查询",
    pre="设备 ADB 在线",
)
def test_WiFi_Conn_Toggle_001(run_shell_cmd, wifi: WiFiControl):
    # Step 1: 打开 WiFi
    assert wifi.set_wifi_enabled(True) or wifi.is_wifi_enabled()
    assert wifi.is_wifi_enabled(), "WiFi 应处于开启状态"

    # Step 2: 关闭 WiFi 并查询 status
    wifi.set_wifi_enabled(False)
    out = run_shell_cmd("cmd wifi status")
    print(f"WiFi status（关闭后）：\n{out}")
    assert out, "cmd wifi status 在关 WiFi 后应仍有输出"

    # Step 3: 再次打开 WiFi
    wifi.set_wifi_enabled(True)
    out2 = run_shell_cmd("cmd wifi status")
    assert out2, "重新打开 WiFi 后 status 应可查询"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Conn_Status_001")
@pytest.mark.wifi_case(
    title="开启 WiFi 后 cmd wifi status 输出有效",
    pre="设备 ADB 在线",
)
def test_WiFi_Conn_Status_001(run_shell_cmd, wifi: WiFiControl):
    # Step 1: 打开 WiFi
    wifi.set_wifi_enabled(True)

    # Step 2: 查询 status
    out = run_shell_cmd("cmd wifi status")
    print(f"WiFi status 输出：\n{out}")
    assert len(out.strip()) > 10, "cmd wifi status 输出过短，可能未拿到有效状态"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Conn_AI_Heur_001")
@pytest.mark.wifi_case(
    title="AI 启发式生成用例列表结构合法",
    pre="wifi_ssid.yaml 可加载",
)
def test_WiFi_Conn_AI_Heur_001(wifi_yaml: dict):
    if AIWiFiCaseGenerator is None:
        pytest.skip("core.ai 不存在，跳过 AI 启发式测试")
    gen = AIWiFiCaseGenerator()
    cases = gen.heuristic_cases()
    assert isinstance(cases, list), "启发式用例应为 list"
    if wifi_yaml.get("networks"):
        assert any("ssid" in c for c in cases), "networks 配置存在时应含 ssid 字段"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.ai
@pytest.mark.case_id("WiFi_Conn_AI_Merge_001")
@pytest.mark.wifi_case(
    title="AI 合并生成用例非空",
    pre="可选 PYAT_AI_API_KEY",
)
def test_WiFi_Conn_AI_Merge_001(ai_enabled: bool):
    if AIWiFiCaseGenerator is None:
        pytest.skip("core.ai 不存在，跳过 AI 合并测试")
    gen = AIWiFiCaseGenerator()
    merged = gen.generate_with_ai(extra_context="Focus on reconnect after screen off.")
    assert isinstance(merged, list)
    assert len(merged) >= 1, "AI 合并结果应至少 1 条"


@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("WiFi_Conn_E2E_001")
@pytest.mark.wifi_case(
    title="连接 primary_ssid / wifi_list 并确认关联成功",
    pre="wifi_ssid.yaml 中 SSID 在现网可用",
)
def test_WiFi_Conn_E2E_001(wifi: WiFiControl, wifi_yaml: dict):
    primary = wifi_yaml.get("primary_ssid") or (wifi_yaml.get("networks") or [{}])[0].get("ssid")
    if not primary:
        entry = (wifi_yaml.get("wifi_list") or [{}])[0]
        primary = entry.get("ssid")
    if not primary:
        pytest.skip("yaml 中无可用 SSID")

    nets = {n.get("ssid"): n for n in (wifi_yaml.get("networks") or [])}
    info = nets.get(primary) or {}
    if not info and wifi_yaml.get("wifi_list"):
        for row in wifi_yaml["wifi_list"]:
            if row.get("ssid") == primary:
                info = row
                break

    sec = (info.get("security") or "OPEN").upper()
    pwd = (info.get("pwd") or "").strip()
    if not pwd:
        env_name = info.get("password_env") or ""
        pwd = wifi.resolve_password(env_name)

    # Step 1: 打开 WiFi 并连接
    wifi.set_wifi_enabled(True)
    if sec == "OPEN" and not pwd:
        ok = wifi.connect_open(primary)
    else:
        if not pwd:
            pytest.skip(f"缺少密码或环境变量：{info.get('password_env')}")
        ok = wifi.connect_wpa2(primary, pwd)

    # Step 2: 校验当前 SSID
    cur = wifi.get_connected_ssid()
    print(f"当前 SSID：{cur!r}，目标：{primary!r}")
    if not ok:
        pytest.xfail("connect-network 不支持或 AP 不可达")
    assert primary in cur or cur == primary, f"关联 SSID 不符：预期 {primary!r}，实际 {cur!r}"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.ai
@pytest.mark.case_id("WiFi_Conn_AI_Res_001")
@pytest.mark.wifi_case(
    title="AI 分析 pytest 失败输出并返回 summary",
    pre="无",
)
def test_WiFi_Conn_AI_Res_001():
    if AIResultAnalyzer is None:
        pytest.skip("core.ai 不存在，跳过 AI 结果分析测试")

    ar = AIResultAnalyzer()
    r = ar.analyze(pytest_output="FAILED test_demo - AssertionError: SSID mismatch")
    assert isinstance(r, dict)
    assert "summary" in r, "分析结果应含 summary 字段"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.ai
@pytest.mark.case_id("WiFi_Conn_AI_UI_001")
@pytest.mark.wifi_case(
    title="无图时 UI 定位器返回 no_image",
    pre="无截图文件",
)
def test_WiFi_Conn_AI_UI_001(tmp_path):
    if AIUILocator is None:
        pytest.skip("core.ai 不存在，跳过 AI UI 定位测试")

    loc = AIUILocator()
    p = tmp_path / "missing.png"
    x, y, note = loc.suggest_tap(Path(p), "open WiFi")
    assert x is None and y is None
    assert note == "no_image"
