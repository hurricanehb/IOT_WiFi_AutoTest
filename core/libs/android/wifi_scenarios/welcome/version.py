"""Android Welcome WLAN version scenarios."""
from __future__ import annotations

import re

from core.utils.log_handler import get_logger


def run_welcome_version_case(run_shell_cmd, capsys) -> None:
    package_info = run_shell_cmd("dumpsys package com.sunmi.welcome")
    version_match = re.search(r"\bversionName\s*=\s*(\d+(?:\.\d+)+(?:[._-][A-Za-z0-9]+)*)", package_info)
    version = version_match.group(1) if version_match else ""
    failure_message = "Welcome 组件未安装或未查询到有效版本号"

    get_logger(__name__).info("%s", f"Welcome 组件版本号：{version}" if version else failure_message)
    with capsys.disabled():
        if version:
            print(f"\nWelcome 组件版本号：{version}")
        else:
            print(failure_message)

    assert version, failure_message
