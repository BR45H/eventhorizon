from .scan_lib.funcs_scan import *
from core.target import normalize_target_input
from core import output
import argparse
import socket

TOP_100_PORTS = [
    7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113,
    119, 135, 139, 143, 144, 179, 199, 254, 255, 280, 311, 389, 427, 443, 444,
    445, 465, 513, 514, 515, 543, 544, 548, 554, 587, 631, 646, 873, 990, 993,
    995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900,
    2000, 2001, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000,
    5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000,
    6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999,
    10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]

STATUS_OUTPUT = {
    "open": output.success,
    "closed": output.error,
    "filtered": output.warning,
    "unknown": output.info,
}

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    ports = parse_ports(args.port)
    verbose = args.verbose
    ttl = args.ttl
    srcp = args.srcp

    for target in target_data.targets:
        ip = normalize_target(target)

        if ip is None:
            continue
        if ports is None:
            return

        for port in ports:
            resp = csr_TCP(target, ttl, srcp, port)
            status = interpreting_response_TCP(resp)

            if status == "open" or verbose:
                STATUS_OUTPUT[status](f"{port}/tcp\t{status}")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "scan",
        help="Perform a controlled SYN portscan."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-p", "--port",
        required=False,
        default=",".join(str(p) for p in TOP_100_PORTS),
        help="Sets the ports you want to scan.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all ports scanned.",
    )
    parser.add_argument(
        "--ttl",
        default=255,
        type=int,
        help="Set a TTL for the packet.",
    )
    parser.add_argument(
        "-srcp", "--source-port",
        dest="srcp",
        default=53,
        type=int,
        help="Set a source port.",
    )
    parser.set_defaults(func=run)
    