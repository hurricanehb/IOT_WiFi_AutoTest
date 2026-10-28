"""日志：文件 UTF-8；pytest 下不写 StreamHandler（避免与 capture 编码冲突）。"""
from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

_initialized = False


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _default_log_dir() -> Path:
    try:
        from core.utils.report_utils import log_report_dir

        return log_report_dir()
    except Exception:
        stamp = datetime.now().strftime("%Y-%m-%d")
        return _project_root() / "reports" / stamp / "log"


def _under_pytest() -> bool:
    return "pytest" in sys.modules


def get_logger(
    name: str = "PyAutoTest_IoT",
    log_dir: Optional[Path] = None,
    *,
    console: Optional[bool] = None,
) -> logging.Logger:
    global _initialized
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    level = logging.INFO
    try:
        from core.utils.config_loader import get_settings

        raw = (get_settings().log_level or "INFO").upper()
        level = getattr(logging, raw, logging.INFO)
    except Exception:
        pass
    logger.setLevel(level)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    use_console = console if console is not None else not _under_pytest()
    if use_console:
        from core.utils.stdio_utf8 import ensure_utf8_stdio

        ensure_utf8_stdio()
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    out = log_dir if log_dir is not None else _default_log_dir()
    out.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(out / "automation.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    _initialized = True
    return logger
