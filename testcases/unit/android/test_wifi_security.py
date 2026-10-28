from unittest.mock import Mock

import pytest

from core.libs.android.wifi_scenarios.wifi_security import confirm_step
from core.libs.android.wifi_scenarios import wifi_security as scenarios


@pytest.mark.parametrize(
    "model", ["P", "P100", "p-a16", " P_Test ", "SP", "SP100"]
)
def test_sp_model_detection_accepts_sp_series(model):
    assert scenarios.is_sp_model(model)


@pytest.mark.parametrize("model", ["", "V3_A16", "X100"])
def test_sp_model_detection_rejects_other_series(model):
    assert not scenarios.is_sp_model(model)


def test_sp_security_case_skips_non_sp_before_interaction(monkeypatch):
    monkeypatch.setattr(scenarios, "attach_wifi_status", Mock())
    confirm = Mock()
    target = Mock()
    monkeypatch.setattr(scenarios, "confirm_step", confirm)
    monkeypatch.setattr(scenarios, "_target_ssid", target)

    with pytest.raises(pytest.skip.Exception, match="当前型号='V3_A16'"):
        scenarios.run_sp_wifi_security_case(
            {"case_id": "Func_Components_Settings_WifiSec_Vali_001"},
            Mock(return_value="V3_A16"),
            Mock(),
            Mock(),
        )

    confirm.assert_not_called()
    target.assert_not_called()


def test_target_preserves_ssid_case(monkeypatch):
    monkeypatch.setenv("WIFISEC_WEAK_SSID", "Lab_SP_Open")
    assert scenarios._target_ssid("case") == "Lab_SP_Open"


@pytest.mark.parametrize("networks", ["", "Unknown command", "Permission denied"])
def test_unreadable_saved_networks_cannot_pass(networks):
    wifi = Mock()
    wifi.list_networks_blob.return_value = networks
    with pytest.raises(pytest.fail.Exception, match="无法识别"):
        scenarios._assert_not_added("case", wifi, "target")


@pytest.mark.parametrize("saved, connected", [(True, False), (False, True)])
def test_qr_fails_when_target_saved_or_connected(saved, connected):
    wifi = Mock()
    wifi.list_networks_blob.return_value = "Network Id SSID Security type\n" + (
        '0 "target" open' if saved else ""
    )
    wifi.list_connected_ssids.return_value = ["target"] if connected else []
    with pytest.raises(pytest.fail.Exception, match="已被保存或连接"):
        scenarios._assert_not_added("case", wifi, "target")


@pytest.mark.parametrize("answer", ["yes", " YES "])
def test_confirmation_accepts_explicit_yes(monkeypatch, answer):
    monkeypatch.setattr("builtins.input", Mock(return_value=answer))
    confirm_step("case", "observation")


@pytest.mark.parametrize("answer", ["no", ""])
def test_confirmation_never_passes_failure_or_empty_input(monkeypatch, answer):
    monkeypatch.setattr("builtins.input", Mock(return_value=answer))
    with pytest.raises(pytest.fail.Exception):
        confirm_step("case", "observation")


@pytest.mark.parametrize("error", [EOFError(), OSError()])
def test_confirmation_skips_without_interactive_stdin(monkeypatch, error):
    monkeypatch.setattr("builtins.input", Mock(side_effect=error))
    with pytest.raises(pytest.skip.Exception, match="pytest -s"):
        confirm_step("case", "observation")