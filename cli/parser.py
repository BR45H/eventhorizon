from modules.subdomain import bruteforce as subdomain_bruteforce
from modules.subdomain import takeover as subdomain_takeover
from modules.tcp import synscan as tcp_synscan
from modules.tcp import connectscan as tcp_connectscan
from modules.tcp import portpeek as tcp_portpeek
from modules.smtp import vrfycrack as smtp_vrfycrack
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

    #TCP
    tcp_parser = modules.add_parser(
        "tcp",
        help="TCP-related operations."
    )
    tcp_actions = tcp_parser.add_subparsers(dest="action", required=True)

    tcp_connectscan.register(tcp_actions)
    tcp_synscan.register(tcp_actions)
    tcp_portpeek.register(tcp_actions)

    # smtp
    smtp_parser = modules.add_parser(
        "smtp",
        help="SMTP-related operations."
    )
    smtp_actions = smtp_parser.add_subparsers(dest="action", required=True)

    smtp_vrfycrack.register(smtp_actions)
    return parser