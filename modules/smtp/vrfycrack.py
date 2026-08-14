from core.target import normalize_target_input
from core import output
from sys import exit
from pathlib import Path
import argparse
import socket

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    port = args.port
    banner = args.banner
    verbose = args.verbose
    with Path(args.wordlist).open(mode="r", encoding="utf-8") as f:
        wordlist_users = [line.strip() for line in f if line.strip()]

    for target in target_data.targets:
        result = vrfycrack(target, port, wordlist_users, verbose, banner)

        users = result
        print(f"===== VALID USERS ({target}) =====\n")

        if not users:
            output.warning(f"No users found on {target}")

        for user in users:
            output.success(f"User: {user} is a valid user!")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "vrfycrack",
        help="Verify if user exist in SMTP server (VRFY-based).",
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target or file containing targets.",
    )
    parser.add_argument(
        "-p", "--port",
        required=False,
        default=25,
        type=int,
        help="Set the port.",
    )
    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Wordlist file for users candidates.",
    )
    parser.add_argument(
        "-b", "--banner",
        required=False,
        action="store_true",
        help="Do a banner grabbing on SMTP server",
    )
    parser.add_argument(
        "-v", "--verbose",
        required=False,
        action="store_true",
        help="idk what put here",
    )
    parser.set_defaults(func=run)

def vrfycrack(target: str, port: int, wordlist_users: list[str], verbose: bool, banner: bool):
    valid_users = []
    try:
        results = socket.getaddrinfo(target, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    
    except socket.gaierror as e:
        if verbose:
            output.error(f"Fail to resolve {target}: {e}")
        return valid_users
        
    if not results:
        return None
    
    family, type_, proto, canonname, sockaddr = results[0]

    try:
        with socket.socket(family, type_, proto) as sock:
            sock.settimeout(15)
            resp = sock.connect_ex(sockaddr)

            if resp != 0:
                if verbose:
                    output.error(f"Fail to connect in {target}:{port}")
                    exit(1)
                return None

            server_banner = sock.recv(1024)
            if banner:
                output.info(f"Banner: {server_banner.decode(errors="ignore").strip()}\n")
            
            for user in wordlist_users:
                try:
                    sock.send(str.encode(f"VRFY {user}\r\n"))
                    response = sock.recv(1024).decode(errors="ignore")
                except (socket.timeout, OSError):
                    if verbose:
                        output.error(f"Connection lost while testing '{user}'.")
                    break

                if response.startswith(("250", "252")):
                    valid_users.append(user)
                    if verbose:
                        output.success(f"{user} - valid.")

            return valid_users

    except OSError as e:
        if verbose:
            output.error(f"Socket error on {target}: {e}")
        return None
    