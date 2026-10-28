from __future__ import annotations

from typing import Callable

import allure


def attach_wifi_status(
    case_id: str,
    run_shell_cmd: Callable[[str], str],
) -> str:
    with allure.step("检查 DUT WiFi 初始状态"):
        status = str(run_shell_cmd("cmd wifi status"))
        allure.attach(
            status,
            name=f"{case_id} - cmd wifi status",
            attachment_type=allure.attachment_type.TEXT,
        )
    return status