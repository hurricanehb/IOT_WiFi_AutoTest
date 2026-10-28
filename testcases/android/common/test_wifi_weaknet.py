"""弱网场景 YAML 与 AI 规划。"""
from __future__ import annotations

import pytest

try:
    from core.ai.ai_weaknet_sim import AIWeakNetAdvisor
except ModuleNotFoundError:
    AIWeakNetAdvisor = None


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.weaknet
@pytest.mark.case_id("WiFi_Weaknet_Yaml_001")
@pytest.mark.wifi_case(
    title="弱网场景 YAML 结构含 name 字段",
    pre="weaknet_scene.yaml 存在",
)
def test_WiFi_Weaknet_Yaml_001(weaknet_yaml: dict):
    scenes = weaknet_yaml.get("scenes") or []
    assert len(scenes) >= 1, "scenes 至少 1 条"
    assert all("name" in s for s in scenes), "每条场景应含 name"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.weaknet
@pytest.mark.case_id("WiFi_Weaknet_Plan_001")
@pytest.mark.wifi_case(
    title="从 YAML 生成计划含 baseline",
    pre="weaknet_scene.yaml 可解析",
)
def test_WiFi_Weaknet_Plan_001(weaknet_yaml: dict):
    scenes = weaknet_yaml.get("scenes") or []
    names = {s.get("name") for s in scenes if isinstance(s, dict)}
    assert "baseline" in names, f"计划应含 baseline，实际：{names}"


@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.weaknet
@pytest.mark.ai
@pytest.mark.case_id("WiFi_Weaknet_AI_001")
@pytest.mark.wifi_case(
    title="AI 丰富后的弱网计划不少于 YAML 基线",
    pre="可选 PYAT_AI_API_KEY",
)
def test_WiFi_Weaknet_AI_001(ai_enabled: bool):
    if AIWeakNetAdvisor is None:
        pytest.skip("core.ai 不存在，跳过 AI 弱网增强测试")
    adv = AIWeakNetAdvisor()
    merged = adv.enrich_with_ai(device_metrics="RSSI -65 dBm, ping 40ms stable")
    base = adv.plan_from_yaml()
    assert len(merged) >= len(base), "AI 丰富后场景数应不少于基线"
