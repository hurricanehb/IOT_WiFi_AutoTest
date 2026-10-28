"""Original terminal output support for Android hotspot scenarios."""
from __future__ import annotations

import sys

from core.utils.log_handler import get_logger


log = get_logger('test_func_softap_basic')


def _uncaptured_stdout():
    stdout = sys.__stdout__ or sys.stdout
    if stdout is None:
        raise RuntimeError("标准输出不可用")
    return stdout


def _write_uncaptured_line(capsys, message: str) -> None:
    """确保测试进度和结果单独输出到实际终端。"""
    log.info("%s", message)
    with capsys.disabled():
        stdout = _uncaptured_stdout()
        stdout.write(f"\n{message}\n")
        stdout.flush()
