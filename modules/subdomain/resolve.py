import argparse

def run(args: argparse.Namespace) -> None:
    print("[subdomain:resolve]")
    print(f"target  = {args.target}")
    print(f"vebose  = {args.verbose}")

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