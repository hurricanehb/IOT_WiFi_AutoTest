import pytest

from core.libs.android.wifi_scenarios.settings.saved_networks import (
    SAVED_NETWORKS_TEXTS,
    contains_any_text,
    run_saved_network_case,
)


def test_contains_saved_network_entry_in_localized_hierarchy() -> None:
    hierarchy = '<node text="已保存的网络" resource-id="android:id/title" />'

    assert contains_any_text(hierarchy, SAVED_NETWORKS_TEXTS)
    assert not contains_any_text('<node text="添加网络" />', SAVED_NETWORKS_TEXTS)


def test_saved_network_runner_rejects_unsupported_case() -> None:
    with pytest.raises(ValueError, match="未知 SavedNet"):
        run_saved_network_case(
            "Func_Components_Settings_SavedNet_Vali_003",
            lambda command: "",
            None,  # type: ignore[arg-type]
            {},
            None,  # type: ignore[arg-type]
        )
