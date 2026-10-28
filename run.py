"""
测试执行入口：按场景封装 pytest 命令（HTML / 可选 Allure）。

用法示例:
  python run.py                    # 全量 testcases
  python run.py --scene smoke
  python run.py --scene country_code           # 国家码 wlan_country 子模块（含遍历）
  python run.py --scene country_code -k Adapt_Table
  python run.py -- --collect-only
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent


def _ensure_dirs() -> None:
    from core.utils.report_utils import ensure_report_subdirs, init_report_run_dir

    init_report_run_dir()
    ensure_report_subdirs()
    (ROOT / "temp").mkdir(parents=True, exist_ok=True)


def _scene_targets(scene: str) -> List[str]:
    if scene == "all":
        return [str(ROOT / "testcases")]
    if scene == "hyperwifi":
        return [str(ROOT / "testcases" / "android")]
    if scene == "miniap":
        return [str(ROOT / "testcases" / "miniAP")]
    if scene == "smoke":
        return [str(ROOT / "testcases" / "smoke"), "-m", "smoke"]
    if scene == "stress":
        return [str(ROOT / "testcases" / "android"), "-m", "stress"]
    if scene == "weaknet":
        return [str(ROOT / "testcases" / "android"), "-m", "weaknet"]
    if scene == "country_code":
        return [str(ROOT / "testcases" / "android" / "country_code")]
    if scene == "ai":
        return [str(ROOT / "testcases"), "-m", "ai"]
    return [str(ROOT / "testcases")]


def run_pytest(scene: str, extra: Optional[List[str]] = None, use_allure: bool = False) -> int:
    _ensure_dirs()
    from core.utils.report_utils import allure_results_dir, html_report_path, report_run_dir

    report = html_report_path("report.html")
    cmd: List[str] = [sys.executable, "-m", "pytest"] + _scene_targets(scene)
    cmd.append(f"--html={report}")
    cmd.append("--self-contained-html")
    if use_allure:
        cmd.append(f"--alluredir={allure_results_dir('raw')}")
    print(f"报告目录: {report_run_dir()}")
    if extra:
        cmd.extend(extra)
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    # 默认开启 ssidpwd miniAP 自动下发，避免实验室场景下遗漏环境变量导致连网失败。
    env.setdefault("SSIDPWD_MINIAP_AUTOCFG", "1")
    return subprocess.call(cmd, cwd=str(ROOT), env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="PyAutoTest_IoT — pytest runner")
    parser.add_argument(
        "--scene",
        choices=["all", "hyperwifi", "miniap", "smoke", "stress", "weaknet", "country_code", "ai"],
        default="all",
        help="预置收集范围与部分场景标记",
    )
    parser.add_argument(
        "--allure",
        action="store_true",
        help="写入 Allure 原始结果到 reports/<日期>/allure/raw",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help="仅收集用例，不执行",
    )
    args, pytest_args = parser.parse_known_args()
    tail: List[str] = list(pytest_args)
    if args.list_only:
        tail.insert(0, "--collect-only")
    code = run_pytest(args.scene, tail if tail else None, use_allure=args.allure)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
