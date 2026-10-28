"""测试数据解析：YAML/JSON/文本；主机网络探测。"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional, Union


def load_yaml(path: Union[Path, str]) -> Any:
    import yaml

    p = Path(path)
    if not p.is_file():
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(path: Union[Path, str], data: Any) -> None:
    import yaml

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def load_json(path: Union[Path, str]) -> Any:
    p = Path(path)
    if not p.is_file():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f) or {}


def read_text_safe(path: Union[Path, str], default: str = "") -> str:
    p = Path(path)
    if not p.is_file():
        return default
    return p.read_text(encoding="utf-8", errors="replace")


def write_text_safe(path: Union[Path, str], content: str, encoding: str = "utf-8") -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


def read_csv_rows(path: Union[Path, str], encoding: str = "utf-8") -> list:
    """预留：CSV 驱动用例时可使用 pandas 或 csv 模块扩展。"""
    import csv

    p = Path(path)
    if not p.is_file():
        return []
    with open(p, encoding=encoding, newline="") as f:
        return list(csv.DictReader(f))


def ping_host(host: str, count: int = 1, timeout_sec: float = 2.0) -> bool:
    if sys.platform == "win32":
        cmd = ["ping", "-n", str(count), "-w", str(int(timeout_sec * 1000)), host]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(max(1, int(timeout_sec))), host]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec + 5)
        return p.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def tcp_available(host: str, port: int, timeout_sec: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except OSError:
        return False
