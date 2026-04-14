from core.target import normalize_target_input
from core.exceptions import ValidationError
from core import output
import argparse
import socket

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    verbose_mode = args.verbose

    if target_data.kind != "domain":
        raise ValidationError("subdomain resolve only accepts domain targets")
    
    for target in target_data.targets:
        output.info(f"Resolving {target}")
        result = resolve_domain(target, verbose_mode)
        if result is None:
            continue
        for entry in result:
            ip = entry[4][0]
            output.success(f"{target} -> {ip}")


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "resolve",
        help="Resolve a domain or a list of domains."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain or file containing domains."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.set_defaults(func=run)

def resolve_domain(target: str, verbose: bool = False) -> list | None:
    try:
        result = socket.getaddrinfo(target, None)
        return result

    except socket.gaierror:
        if verbose:
            output.warning(f"Error for {target}")
        return None
        