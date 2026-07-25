from modules.subdomain import bruteforce as subdomain_bruteforce
from modules.smb import connect as smb_connect
from modules.smb import spray as smb_spray
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

    # smb
    smb_parser = modules.add_parser(
        "smb",
        help="SMB-related operations."
    )
    smb_actions = smb_parser.add_subparsers(dest="action", required=True)

    smb_connect.register(smb_actions)
    smb_spray.register(smb_actions)

    return parser