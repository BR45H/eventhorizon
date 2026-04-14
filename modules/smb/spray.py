import argparse

def run(args: argparse.Namespace) -> None:
    print("[smb:spray]")
    print(f"target            = {args.target}")
    print(f"users_wordlist    = {args.users}")
    print(f"password_wordlist = {args.passwords}")
    print(f"verbose           = {args.verbose}")

def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "spray",
        help="Perform controlled SMB password spraying."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target host or file containing targets."
    )
    parser.add_argument(
        "-U", "--users",
        required=True,
        help="File containing usernames."
    )
    parser.add_argument(
        "-P", "--passwords",
        required=True,
        help="File containing passwords."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.set_defaults(func=run)