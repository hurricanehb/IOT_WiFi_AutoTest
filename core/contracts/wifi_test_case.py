"""Dictionary-compatible WiFi test-case metadata."""
from __future__ import annotations


class WifiTestCase(dict[str, str]):
    """Metadata passed from generated pytest cases to scenario runners."""

    def __init__(
        self,
        *,
        case_id: str,
        title: str,
        tag: str = "",
        pre: str = "",
        **metadata: str,
    ) -> None:
        super().__init__(case_id=case_id, title=title, tag=tag, pre=pre, **metadata)

    def __getattr__(self, name: str) -> str:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc