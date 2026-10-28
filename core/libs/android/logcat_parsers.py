"""Shared parsers for Android logcat output."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Iterable, List, Optional

_LOG_TS_RE = re.compile(
    r"^(\d{2}-\d{2})\s+(\d{2}):(\d{2}):(\d{2})\.(\d{3})"
)


def _parse_logcat_timestamp(line: str, year: int) -> Optional[datetime]:
    match = _LOG_TS_RE.match((line or "").strip())
    if not match:
        return None
    month_day, hour, minute, second, millis = match.groups()
    try:
        return datetime.strptime(
            f"{year}-{month_day} {hour}:{minute}:{second}.{millis}",
            "%Y-%m-%d %H:%M:%S.%f",
        )
    except ValueError:
        return None


def parse_logcat_event_offsets(
    log_text: str,
    event_hints: Iterable[str],
) -> List[float]:
    """Return event offsets while accounting for a year rollover."""
    hints = tuple(hint.lower() for hint in event_hints)
    timestamps: List[datetime] = []
    year = 2000

    for line in (log_text or "").splitlines():
        lower = line.lower()
        if not any(hint in lower for hint in hints):
            continue
        timestamp = _parse_logcat_timestamp(line, year)
        if timestamp is None:
            continue
        if timestamps and timestamp < timestamps[-1]:
            year += 1
            timestamp = _parse_logcat_timestamp(line, year)
            if timestamp is None:
                continue
        timestamps.append(timestamp)

    if not timestamps:
        return []
    base = timestamps[0]
    return [(timestamp - base).total_seconds() for timestamp in timestamps]