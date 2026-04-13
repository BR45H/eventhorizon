import argparse

def run(args: argparse.Namespace) -> None:
    print("[subdomain:bruteforce]")
    print(f"target   = {args.target}")
    print(f"wordlist = {args.wordlist}")
    print(f"verbose  = {args.verbose}")

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
    parser.set_defaults(func=run)