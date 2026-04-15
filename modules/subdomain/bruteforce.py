from core.target import normalize_target_input
from core.exceptions import ValidationError
from core import output
from pathlib import Path
import argparse
import socket

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    wordlist_subdomain = [line.strip() for line in Path.open(args.wordlist, mode="r", encoding="utf-8") if line.strip()]
    verbose_mode = args.verbose
    show_ipv4 = args.show_ipv4

    if target_data.kind != "domain":
        raise ValidationError("subdomain bruteforce only accepts domain targets")

    if target_data.source == "file":
        output.warning("Running 'subdomain bruteforce' against a target file may produce a large amount of output")

    for target in target_data.targets:
        output.info(f"Initiating subdomain bruteforce in {target}")
        result = subdomain_bruteforce(target, wordlist_subdomain, verbose_mode)

        if not result:
            output.warning(f"No subdomains found for {target}")
            continue
        
        for full_domain, ip in result:
            if show_ipv4:
                output.success(f"{full_domain} -> {ip}")
            else:
                output.success(f"{full_domain} exist!")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "bruteforce",
        help="Perform controlled subdomain bruteforce."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Wordlist file for subdomain candidates."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.add_argument(
        "--show-ipv4",
        action="store_true",
        help="Show ipv4 from subdomain found."
    )
    parser.set_defaults(func=run)

def subdomain_bruteforce(target, wordlist_subdomain: list[str], verbose: bool = False) -> list[tuple[str, str]]:
    result = []
    for subdomain in wordlist_subdomain:
        full_domain = f"{subdomain}.{target}"
        try:
            ip = socket.gethostbyname(full_domain)
            result.append((full_domain, ip))
        
        except socket.gaierror:
            if verbose:
                output.warning(f"Failed to resolve {full_domain}")
            continue
        
    return result
