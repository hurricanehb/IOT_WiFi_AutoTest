"""Command-line control for the configured HJ Radio Rack."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.utils.attenuator import HJRadioRack
from core.utils.config_loader import get_settings


def _parse_assignment(text: str) -> tuple[int, float]:
    try:
        channel_text, value_text = text.split("=", maxsplit=1)
        return int(channel_text), float(value_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid assignment {text!r}; expected CHANNEL=DB"
        ) from exc


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Control the configured HJ Radio Rack")
    parser.add_argument("--host", help="override configured device IP address")
    parser.add_argument("--port", type=int, help="override configured device port")
    parser.add_argument("--timeout", type=float, help="override response timeout (s)")
    parser.add_argument(
        "--max-attenuation",
        type=float,
        help="override maximum attenuation (dB)",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("read", help="read all channel attenuation values")

    set_parser = commands.add_parser("set", help="set one channel")
    set_parser.add_argument("channel", type=int)
    set_parser.add_argument("attenuation_db", type=float)

    multi_parser = commands.add_parser("set-many", help="set multiple channels")
    multi_parser.add_argument(
        "assignments",
        nargs="+",
        type=_parse_assignment,
        metavar="CHANNEL=DB",
    )

    timeout_parser = commands.add_parser("socket-timeout", help="set idle timeout")
    timeout_parser.add_argument("minutes", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    config = get_settings().attenuator_device
    host = args.host or config.host
    if not host:
        parser.error(
            "attenuator host is not configured; set attenuator_device.host "
            "or ATTENUATOR_HOST"
        )

    with HJRadioRack(
        host=host,
        port=args.port or config.port,
        timeout_sec=args.timeout or config.timeout_sec,
        max_attenuation_db=args.max_attenuation or config.max_attenuation_db,
    ) as attenuator:
        if args.command == "read":
            values = attenuator.read_attenuations()
            print(
                "; ".join(
                    f"CH{channel}={value:g} dB"
                    for channel, value in values.items()
                )
            )
        elif args.command == "set":
            value = attenuator.set_attenuation(args.channel, args.attenuation_db)
            print(f"CH{args.channel}={value:g} dB")
        elif args.command == "set-many":
            values = attenuator.set_attenuations(dict(args.assignments))
            print(
                "; ".join(
                    f"CH{channel}={value:g} dB"
                    for channel, value in values.items()
                )
            )
        else:
            attenuator.set_socket_timeout(args.minutes)
            print(f"socket timeout={args.minutes} minute(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())