from core.target import normalize_target_input
from core import output
import argparse
import socket

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    port = args.port
    timeout = args.timeout

    for target in target_data.targets:
        if portpeek(target, port, timeout):
            output.success(f"{target}:{port} is open.")
        else:
            output.info(f"{target}:{port} is closed.")


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "portpeek",
        help="Verify if a port is open via TCP connect."
    )
    parser.add_argument(
        "-t","--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-p","--port",
        required=True,
        type=int,
        help="Set the port you want to peek.",
    )
    parser.add_argument(
        "--timeout",
        required=False,
        type=float,
        default=2.0,
        help="Set the timeout.",
    )
    parser.set_defaults(func=run)

def portpeek(target: str, port: int, timeout: float) -> bool:
    try:
        results = socket.getaddrinfo(target, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        output.error(f"Could not resolve {target}")
        return False

    family, type_, proto, _, sockaddr = results[0]

    with socket.socket(family, type_, proto) as sock:
        sock.settimeout(timeout)
        resp = sock.connect_ex(sockaddr)
        return resp == 0