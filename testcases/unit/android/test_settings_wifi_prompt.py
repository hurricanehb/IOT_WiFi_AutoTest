from core.libs.android.wifi_scenarios.settings.wifi_prompt import (
    HYPER_GUIDANCE,
    WIFI_GUIDANCE,
    hierarchy_has_guidance,
    normalize_guidance,
)


def test_hierarchy_has_hyper_guidance_with_nonbreaking_hyphen() -> None:
    hierarchy = f'<hierarchy><node text="{HYPER_GUIDANCE.replace("-", "‑")}" /></hierarchy>'

    assert hierarchy_has_guidance(hierarchy, HYPER_GUIDANCE)


def test_hierarchy_has_wifi_guidance_across_whitespace() -> None:
    hierarchy = f'<hierarchy><node content-desc="{WIFI_GUIDANCE.replace(" ", "  ")}" /></hierarchy>'

    assert hierarchy_has_guidance(hierarchy, WIFI_GUIDANCE)


def test_normalize_guidance_does_not_accept_incomplete_prompt() -> None:
    assert normalize_guidance("获得更稳定的上网体验") not in normalize_guidance(
        HYPER_GUIDANCE
    )