"""国家码遍历表：testdata/android/country_code_tables.yaml。"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from core.utils.config_loader import android_data_path
from core.utils.data_parser import load_yaml

COUNTRY_CODE_TABLES_YAML = "country_code_tables.yaml"


def country_code_tables_yaml() -> Path:
    return android_data_path(COUNTRY_CODE_TABLES_YAML)


def load_country_code_tables() -> dict:
    data = load_yaml(country_code_tables_yaml())
    return data if isinstance(data, dict) else {}


def _normalize_codes(raw: object) -> List[str]:
    if not isinstance(raw, list):
        return []
    out: List[str] = []
    seen = set()
    for item in raw:
        code = (str(item) if item is not None else "").strip().upper()
        if len(code) == 2 and code not in seen:
            seen.add(code)
            out.append(code)
    return out


def us_country_codes(*, limit: Optional[int] = None) -> List[str]:
    codes = _normalize_codes(load_country_code_tables().get("us_country_table"))
    return _apply_limit(codes, limit)


def eu_country_codes(*, limit: Optional[int] = None) -> List[str]:
    codes = _normalize_codes(load_country_code_tables().get("eu_country_table"))
    return _apply_limit(codes, limit)


def _apply_limit(codes: List[str], limit: Optional[int]) -> List[str]:
    cap = limit
    if cap is None:
        env = os.environ.get("CCODE_LIMIT", "").strip()
        if env.isdigit():
            cap = int(env)
    if cap is not None and cap > 0:
        return codes[:cap]
    return codes
