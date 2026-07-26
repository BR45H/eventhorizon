from core.target import normalize_target_input
from core.exceptions import ValidationError
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

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    banner = args.banner

    if args.port == "-":
        ports = list(range(1, 65536))
    elif args.port:
        ports = [int(p) for p in args.port.split(",")]
    else:
        ports = TOP_100_PORTS

    for target in target_data.targets:
        output.info(f"Scanning {target}")
        for port in ports:
            conectou, bann = portscan(target, port, banner)
            if conectou:
                if bann:
                    output.success(f"[{port}] ABERTA — {bann}")
                else:
                    output.success(f"[{port}] ABERTA")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "scan",
        help="Perform controlled portscan."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-p", "--port",
        required=False,
        help="Sets the ports you want to scan.",
    )
    parser.add_argument(
        "-b", "--banner",
        action="store_true",
        help="Grab and display service banners from open ports.",
    )
    parser.set_defaults(func=run)

def portscan(target, port: int, banner: bool = False):
    connect = False
    bann = None

    try:
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.settimeout(1)
        result = mysocket.connect_ex((target, port))
        connect = (result == 0)

        if connect and banner:
            try:
                bann = mysocket.recv(1024).decode(errors="ignore").strip()
            except socket.timeout:
                bann = None

        mysocket.close()

    except OSError:
        connect = False

    return connect, bann