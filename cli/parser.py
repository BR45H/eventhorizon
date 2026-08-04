from modules.subdomain import bruteforce as subdomain_bruteforce
from modules.subdomain import takeover as subdomain_takeover
from modules.port import scan as port_scan
from modules.port import peek as port_peek
import argparse

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eventhorizon",
        description="Modular CLI for controlled network operations."
    )

    modules = parser.add_subparsers(dest="module", required=True)

    # subdomain
    subdomain_parser = modules.add_parser(
        "subdomain",
        help="Subdomain-related operations."
    )
    subdomain_actions = subdomain_parser.add_subparsers(dest="action", required=True)

    subdomain_bruteforce.register(subdomain_actions)
    subdomain_takeover.register(subdomain_actions)

    # ports
    port_parser = modules.add_parser(
        "port",
        help="Port-related operations."
    )
    port_actions = port_parser.add_subparsers(dest="action", required=True)

    port_scan.register(port_actions)
    port_peek.register(port_actions)
    return parser