from .takeover_lib.funcs_takeover import process_subdomain
from core.exceptions import ValidationError
from core.target import normalize_target_input
from core import output
from pathlib import Path
import argparse

def run(args: argparse.Namespace) -> None:
    target_data = normalize_target_input(args.target)
    verbose = args.verbose
    wordlist_subdomain = [line.strip() for line in Path(args.wordlist).open(mode="r", encoding="utf-8") if line.strip()]

    if target_data.kind != "domain":
        raise ValidationError("subdomain takeover only accepts subdomain targets")

    for target in target_data.targets:
        for subdomain in wordlist_subdomain:
            fqdn = f"{subdomain}.{target}"
            data = subdomain_takeover(fqdn)
            if data is None:
                continue

            status = data.get("status")

            if status == "NXDOMAIN" and verbose:
                output.warning(f"Subdomain: {data.get('subdomain')}")
                output.warning(f"Status: {status}, {data.get('detail')}")

            if status == "unknown_service" and verbose:
                output.info(f"Subdomain: {data.get('subdomain')}")
                output.info(f"CNAME: {data.get('cname')}, {data.get('detail')}")

            if status == "VULNERABLE":
                output.success(f"Subdomain: {data.get('subdomain')}")
                output.success(f"CNAME: {data.get('cname')}")
                output.success(f"Status: {status}")

            if status == "cname_points_but_ok":
                output.info(f"Subdomain: {data.get('subdomain')}")
                output.info(f"Status: {status}")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "takeover",
        help="Perform controlled scan subdomain takeover."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target domain."
    )
    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Wordlist file for subdomain candidates.",
    )
    parser.add_argument(
        "-v", "--verbose",
        required=False,
        action="store_true",
        help="Enable verbose output.",
    )
    parser.set_defaults(func=run)

def subdomain_takeover(target) -> dict | None:
    return process_subdomain(target)
