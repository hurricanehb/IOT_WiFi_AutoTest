"""设备端日志导出（adb pull）。"""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path
from typing import Optional

from core.utils.adb_helper import AdbHelper
from core.utils.log_handler import get_logger
from core.utils.report_utils import log_report_dir

log = get_logger(__name__)

DEVICE_LOGS_PATH = "/data/public/logs"


def _safe_label(text: str) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", (text or "").strip())
    return (cleaned.strip("_") or "export")[:60]


def export_device_packlogs(
    adb: AdbHelper,
    *,
    reason: str = "",
    label: str = "",
) -> Optional[Path]:
    """
    将设备日志目录 pull 到本次报告目录。

    命令等价于::
        adb pull /data/public/logs
    """
    dest_dir = log_report_dir() / "device_packlogs"
    dest_dir.mkdir(parents=True, exist_ok=True)

    ts = time.strftime("%Y%m%d_%H%M%S")
    local = dest_dir / f"logs_{_safe_label(label)}_{ts}"

    log.warning(
        "开始导出设备日志：reason=%s label=%s -> %s",
        reason or "-",
        label or "-",
        local,
    )

    shutil.rmtree(local, ignore_errors=True)
    pull_code, _, pull_err = adb.run(
        "pull",
        DEVICE_LOGS_PATH,
        str(local),
        shell=False,
    )
    if pull_code == 0 and local.is_dir() and any(path.is_file() for path in local.rglob("*")):
        try:
            archive = Path(shutil.make_archive(str(local), "zip", root_dir=local))
        except (OSError, shutil.Error) as error:
            log.warning("设备日志压缩失败，保留原始目录：%s error=%r", local, error)
            return local
        shutil.rmtree(local)
        log.info("设备日志已导出并压缩：%s", archive)
        return archive

    log.warning("设备日志目录 pull 失败 rc=%s err=%r", pull_code, pull_err)
    shutil.rmtree(local, ignore_errors=True)
    return None
