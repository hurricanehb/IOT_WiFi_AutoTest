"""信道计划展开工具（用例 plan 在测试脚本内联，不再读 YAML）。"""
from __future__ import annotations

from typing import Any, Iterator, List, Mapping, Optional, Tuple


def expand_channels(spec: Any) -> List[int]:
    """Expand channel spec to a sorted unique int list."""
    if spec is None:
        return []
    if isinstance(spec, int):
        return [spec]
    if isinstance(spec, list):
        out: List[int] = []
        for item in spec:
            out.extend(expand_channels(item))
        return sorted(set(out))
    if isinstance(spec, dict):
        start = spec.get("start")
        end = spec.get("end")
        if start is None or end is None:
            return []
        step = spec.get("step", 1)
        if step <= 0:
            return []
        return list(range(int(start), int(end) + 1, int(step)))
    return []


def iter_channel_steps(plan: Mapping[str, Any]) -> Iterator[Tuple[Optional[int], int]]:
    """
    Yield (bandwidth_mhz, channel) tuples from a plan entry.

    miniAP plans use ``bandwidths`` list; AP plans use flat ``channels`` + ``bandwidth_mhz``.
    """
    bandwidths = plan.get("bandwidths")
    if isinstance(bandwidths, list):
        for bw_entry in bandwidths:
            if not isinstance(bw_entry, dict):
                continue
            mhz = bw_entry.get("mhz")
            channels = expand_channels(bw_entry.get("channels"))
            for ch in channels:
                yield (int(mhz) if mhz is not None else None, ch)
        return

    bw = plan.get("bandwidth_mhz")
    channels = expand_channels(plan.get("channels"))
    for ch in channels:
        yield (int(bw) if bw is not None else None, ch)


def count_channel_steps(plan: Mapping[str, Any]) -> int:
    return sum(1 for _ in iter_channel_steps(plan))
