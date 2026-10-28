"""报告路径：reports/<YYYY-MM-DD>/<HH-MM-SS>/{html,log,allure}/。"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

_RUN_DIR: Optional[Path] = None


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def report_date_stamp(when: Optional[datetime] = None) -> str:
    dt = when or datetime.now()
    return dt.strftime("%Y-%m-%d")


def report_time_stamp(when: Optional[datetime] = None) -> str:
    dt = when or datetime.now()
    return dt.strftime("%H-%M-%S")


def init_report_run_dir(when: Optional[datetime] = None, *, force: bool = False) -> Path:
    """
    初始化并固定本次运行的报告根目录（进程内只初始化一次）。
    路径：reports/<日期>/<时分秒>/
    """
    global _RUN_DIR

    env_root = (os.environ.get("PYTEST_REPORT_RUN_DIR") or "").strip()
    if env_root and not force:
        _RUN_DIR = Path(env_root)
        return _RUN_DIR

    if _RUN_DIR is not None and not force:
        return _RUN_DIR

    dt = when or datetime.now()
    date_part = (os.environ.get("REPORT_DATE") or "").strip() or report_date_stamp(dt)
    time_part = (os.environ.get("REPORT_TIME") or "").strip() or report_time_stamp(dt)

    root = project_root()
    d = root / "reports" / date_part / time_part
    d.mkdir(parents=True, exist_ok=True)
    _RUN_DIR = d
    os.environ["PYTEST_REPORT_RUN_DIR"] = str(d)
    return d


def report_run_dir() -> Path:
    """本次 pytest 运行的报告根目录（与 init_report_run_dir 一致）。"""
    if _RUN_DIR is not None:
        return _RUN_DIR
    return init_report_run_dir()


def html_report_path(filename: str = "report.html") -> Path:
    p = report_run_dir() / "html" / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def log_report_dir() -> Path:
    p = report_run_dir() / "log"
    p.mkdir(parents=True, exist_ok=True)
    return p


def allure_results_dir(sub: str = "raw") -> Path:
    p = report_run_dir() / "allure" / sub
    p.mkdir(parents=True, exist_ok=True)
    return p


def perf_report_dir() -> Path:
    """性能实测数据存档目录（iperf3 原始 JSON 与汇总 CSV）。"""
    p = report_run_dir() / "perf"
    p.mkdir(parents=True, exist_ok=True)
    return p


def junit_report_path(filename: str = "junit.xml") -> Path:
    p = report_run_dir() / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def ensure_report_subdirs() -> Path:
    """创建 html / log / allure 子目录，返回本次运行根目录。"""
    base = init_report_run_dir()
    for rel in ("html", "log", "allure/raw"):
        (base / rel).mkdir(parents=True, exist_ok=True)
    return base
