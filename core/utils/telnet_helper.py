"""Telnet / 行模式 TCP：连接交换机、路由器、串口服务器等（基于 socket，不依赖 telnetlib）。"""
from __future__ import annotations

import select
import socket
import time
from typing import Optional, Sequence, Union

from core.utils.log_handler import get_logger

log = get_logger(__name__)

Pattern = Union[str, bytes]


def _to_bytes(p: Pattern, encoding: str) -> bytes:
    if isinstance(p, bytes):
        return p
    return p.encode(encoding)


class TelnetClient:
    """面向「交互式字符终端」的 TCP 客户端：发一行、读到提示符或超时。"""

    def __init__(
        self,
        host: str,
        port: int = 23,
        timeout_sec: float = 10.0,
        newline: str = "\r\n",
        encoding: str = "utf-8",
        errors: str = "replace",
    ):
        self.host = (host or "").strip()
        self.port = int(port)
        self.timeout_sec = float(timeout_sec)
        self.newline = newline
        self.encoding = encoding
        self.errors = errors
        self._sock: Optional[socket.socket] = None
        self._buf = bytearray()

    def __repr__(self) -> str:
        return f"TelnetClient({self.host!r}, {self.port})"

    @property
    def connected(self) -> bool:
        return self._sock is not None

    def connect(self) -> None:
        if self._sock is not None:
            return
        if not self.host:
            raise ValueError("host is empty")
        s = socket.create_connection((self.host, self.port), timeout=self.timeout_sec)
        s.settimeout(self.timeout_sec)
        self._sock = s
        log.debug("telnet connected %s:%s", self.host, self.port)

    def close(self) -> None:
        if self._sock is None:
            return
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self._sock.close()
        except OSError:
            pass
        self._sock = None
        self._buf.clear()
        log.debug("telnet closed %s:%s", self.host, self.port)

    def __enter__(self) -> TelnetClient:
        self.connect()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _ensure(self) -> socket.socket:
        if self._sock is None:
            raise RuntimeError("not connected; call connect() or use 'with TelnetClient(...):'")
        return self._sock

    def write_raw(self, data: bytes) -> None:
        sock = self._ensure()
        sock.sendall(data)

    def write_line(self, line: str, end: Optional[str] = None) -> None:
        nl = self.newline if end is None else end
        self.write_raw((line + nl).encode(self.encoding, errors=self.errors))

    def read_available(self, max_bytes: int = 65536) -> bytes:
        """非阻塞读取当前可读数据（无数据则返回 b\"\"）。"""
        sock = self._ensure()
        prev = sock.gettimeout()
        sock.setblocking(False)
        try:
            r, _, _ = select.select([sock], [], [], 0.0)
            if not r:
                return b""
            chunk = sock.recv(max_bytes)
            if chunk:
                self._buf.extend(chunk)
            return chunk
        except BlockingIOError:
            return b""
        finally:
            sock.settimeout(prev if prev is not None else self.timeout_sec)

    def _take_from_buffer(self, pattern: bytes) -> Optional[bytes]:
        idx = self._buf.find(pattern)
        if idx < 0:
            return None
        out = bytes(self._buf[: idx + len(pattern)])
        del self._buf[: idx + len(pattern)]
        return out

    def _take_from_buffer_any(self, patterns: Sequence[bytes]) -> Optional[bytes]:
        matches = (
            (idx, pattern)
            for pattern in patterns
            if (idx := self._buf.find(pattern)) >= 0
        )
        match = min(matches, key=lambda item: item[0], default=None)
        if match is None:
            return None
        idx, pattern = match
        out = bytes(self._buf[: idx + len(pattern)])
        del self._buf[: idx + len(pattern)]
        return out

    def _take_all_from_buffer(self) -> bytes:
        out = bytes(self._buf)
        self._buf.clear()
        return out

    def read_until(
        self,
        pattern: Pattern,
        timeout_sec: Optional[float] = None,
        max_total_bytes: int = 512 * 1024,
    ) -> bytes:
        """从缓冲与 socket 读取，直到出现 pattern 或超时或超过 max_total_bytes。"""
        pat = _to_bytes(pattern, self.encoding)
        if not pat:
            raise ValueError("pattern must be non-empty")
        to = self.timeout_sec if timeout_sec is None else float(timeout_sec)
        deadline = time.monotonic() + to
        sock = self._ensure()

        hit = self._take_from_buffer(pat)
        if hit is not None:
            return hit

        total = len(self._buf)
        while total < max_total_bytes:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            sock.settimeout(remaining)
            try:
                chunk = sock.recv(8192)
            except socket.timeout:
                break
            if not chunk:
                break
            self._buf.extend(chunk)
            total += len(chunk)
            hit = self._take_from_buffer(pat)
            if hit is not None:
                return hit

        return self._take_all_from_buffer()

    def read_until_any(
        self,
        patterns: Sequence[Pattern],
        timeout_sec: Optional[float] = None,
        max_total_bytes: int = 512 * 1024,
    ) -> bytes:
        """从缓冲与 socket 读取，直到出现任一 pattern 或超时。"""
        pats = tuple(_to_bytes(pattern, self.encoding) for pattern in patterns)
        if not pats or any(not pattern for pattern in pats):
            raise ValueError("patterns must contain non-empty values")
        to = self.timeout_sec if timeout_sec is None else float(timeout_sec)
        deadline = time.monotonic() + to
        sock = self._ensure()

        hit = self._take_from_buffer_any(pats)
        if hit is not None:
            return hit

        total = len(self._buf)
        while total < max_total_bytes:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            sock.settimeout(remaining)
            try:
                chunk = sock.recv(8192)
            except socket.timeout:
                break
            if not chunk:
                break
            self._buf.extend(chunk)
            total += len(chunk)
            hit = self._take_from_buffer_any(pats)
            if hit is not None:
                return hit

        return self._take_all_from_buffer()

    def read_all(self, idle_sec: float = 0.3, max_rounds: int = 50) -> bytes:
        """读到一段时间内无新数据为止（适合一次性拉取 banner + 提示符）。"""
        sock = self._ensure()
        out = bytearray()
        rounds = 0
        while rounds < max_rounds:
            sock.settimeout(idle_sec)
            try:
                chunk = sock.recv(8192)
            except socket.timeout:
                break
            if not chunk:
                break
            out.extend(chunk)
            rounds += 1
        self._buf.extend(out)
        return bytes(self._buf)

    def execute(
        self,
        command: str,
        expect: Optional[Pattern] = None,
        timeout_sec: Optional[float] = None,
    ) -> bytes:
        """发送一行命令；若给定 expect，则 read_until(expect)；否则 read_all()。"""
        self.write_line(command)
        if expect is not None:
            return self.read_until(expect, timeout_sec=timeout_sec)
        return self.read_all()
