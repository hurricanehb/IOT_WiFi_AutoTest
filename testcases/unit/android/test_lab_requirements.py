import pytest

from core.libs.android.wifi_scenarios.lab_requirements import (
    env_enabled,
    env_value,
    require_env_value,
)


def test_env_value_and_enabled_normalize_environment(monkeypatch) -> None:
    monkeypatch.setenv("ANDROID_LAB_TEST_FLAG", " YES ")

    assert env_value("ANDROID_LAB_TEST_FLAG") == "yes"
    assert env_enabled("ANDROID_LAB_TEST_FLAG")


def test_require_env_value_skips_on_mismatch(monkeypatch) -> None:
    monkeypatch.setenv("ANDROID_LAB_TEST_STATE", "down")

    with pytest.raises(pytest.skip.Exception, match="ANDROID_LAB_TEST_STATE='up'"):
        require_env_value(
            "ANDROID_LAB_TEST_STATE",
            "up",
            "lab case",
            hint="set the expected state",
        )


def test_require_env_value_accepts_normalized_match(monkeypatch) -> None:
    monkeypatch.setenv("ANDROID_LAB_TEST_STATE", " UP ")

    require_env_value("ANDROID_LAB_TEST_STATE", "up", "lab case")