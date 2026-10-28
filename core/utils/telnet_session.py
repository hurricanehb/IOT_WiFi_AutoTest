"""交互式 Telnet 会话：login + execute_command（基于 TelnetClient）。"""
from __future__ import annotations

from typing import List, Optional, Union

from core.utils.log_handler import get_logger
from core.utils.telnet_helper import TelnetClient

log = get_logger(__name__)

Port = Union[str, int]


class TelnetSession:
    """封装 TelnetClient，供 miniAP、陪测 AP、交换机等设备复用。"""

    def __init__(self, *, timeout_sec: float = 30.0) -> None:
        self._timeout_sec = timeout_sec
        self._client: Optional[TelnetClient] = None
        self._prompt: str = ""

    @property
    def connected(self) -> bool:
        return self._client is not None and self._client.connected

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
        self._prompt = ""

    def login(
        self,
        host: str,
        username: str,
        password: str,
        port: Port = 23,
        prompt: str = "",
    ) -> None:
        """连接设备并完成交互式登录，等待 shell 提示符。"""
        self.close()
        host = (host or "").strip()
        if not host:
            raise ValueError("Telnet host 为空")

        client = TelnetClient(host, port=int(port), timeout_sec=self._timeout_sec)
        client.connect()
        banner = client.read_all(idle_sec=0.8).decode(client.encoding, errors=client.errors)
        log.debug("telnet banner (%s): %r", host, banner[:200])

        user = (username or "").strip()
        pwd = (password or "").strip()
        prompt_s = (prompt or "").strip()

        if user:
            try:
                client.read_until(b"login:", timeout_sec=10)
            except Exception:
                client.read_until(b"Login:", timeout_sec=10)
            client.write_line(user)

        if pwd:
            try:
                client.read_until(b"Password:", timeout_sec=10)
            except Exception:
                client.read_until(b"password:", timeout_sec=10)
            client.write_line(pwd)

        if prompt_s:
            client.read_until(prompt_s, timeout_sec=30)
        else:
            client.read_all(idle_sec=0.5)

        self._client = client
        self._prompt = prompt_s
        log.info("telnet 登录成功：%s:%s prompt=%r", host, port, prompt_s or None)

    def execute_command(self, command: str, *, timeout_sec: Optional[float] = None) -> str:
        """发送命令（支持 \\n 多行），返回设备输出文本。"""
        if self._client is None:
            raise RuntimeError("Telnet 未登录，请先调用 login()")

        to = self._timeout_sec if timeout_sec is None else timeout_sec
        raw_lines = (command or "").replace("\r\n", "\n").split("\n")
        chunks: List[str] = []

        for line in raw_lines:
            if line or len(raw_lines) == 1:
                data = self._client.execute(line, timeout_sec=to)
                chunks.append(data.decode(self._client.encoding, errors=self._client.errors))

        if self._prompt:
            try:
                tail = self._client.read_until(self._prompt, timeout_sec=to)
                chunks.append(tail.decode(self._client.encoding, errors=self._client.errors))
            except Exception:
                pass

        text = "".join(chunks)
        log.debug("telnet cmd=%r out_len=%s", command[:80], len(text))
        return text
