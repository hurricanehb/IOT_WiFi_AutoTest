from types import SimpleNamespace

import pytest

from testcases.android.conftest import (
    _wifi_capability_skip_reason,
    pytest_collection_modifyitems,
)


def _node(*markers: str) -> SimpleNamespace:
    return SimpleNamespace(keywords={marker: True for marker in markers})


@pytest.mark.parametrize(
    ("capability", "marker", "should_skip"),
    [
        ("wifi", "wifi", False),
        ("wifi", "common", False),
        ("wifi", "hyperwifi", True),
        ("wifi", "dualwifi", True),
        ("hyperwifi", "wifi", True),
        ("hyperwifi", "common", False),
        ("hyperwifi", "hyperwifi", False),
        ("hyperwifi", "dualwifi", True),
        ("dualwifi", "wifi", False),
        ("dualwifi", "common", False),
        ("dualwifi", "hyperwifi", False),
        ("dualwifi", "dualwifi", False),
    ],
)
def test_wifi_capability_matrix(
    capability: str, marker: str, should_skip: bool
) -> None:
    reason = _wifi_capability_skip_reason(_node(marker), capability)

    assert (reason is not None) is should_skip


def test_invalid_wifi_capability_is_rejected(monkeypatch) -> None:
    monkeypatch.setenv("DUT_WIFI_CAPABILITY", "unsupported")

    with pytest.raises(pytest.UsageError, match="DUT_WIFI_CAPABILITY"):
        pytest_collection_modifyitems([])