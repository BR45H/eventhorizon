from core.target import normalize_target_input
from core import output
import argparse
import socket

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    port = args.port

    for target in target_data.targets:
        resp = portpeek(target, port)
        if resp is True:
            output.success(f"PORT: {port} is open.")
        else:
            output.info(f"PORT {port} is closed.")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "peek",
        help="Verify if port is open."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-p", "--port",
        required=True,
        type=int,
        help="Set the port you want to peek.",
    )
    parser.set_defaults(func=run)

def portpeek(target, port) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resp = sock.connect_ex((target, port))

    if (resp == 0):
        return True
    else:
        return False