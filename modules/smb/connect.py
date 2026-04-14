from core.validator import validate_smb_connect_args
import argparse

def run(args: argparse.Namespace) -> None:
    validate_smb_connect_args(args)
    print("[smb:connect]")
    print(f"target    = {args.target}")
    print(f"user      = {args.user}")
    print(f"password  = {args.password}")
    print(f"anonymous = {args.anonymous}")
    print(f"verbose   = {args.verbose}")

def register(subparser: argparse._SubParsersAction) -> None:
    parser = subparser.add_parser(
        "connect",
        help="Perform a SMB connection."
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target host or file containing targets."
    )
    parser.add_argument(
        "-u", "--user",
        help="Username for SMB authentication."
    )
    parser.add_argument(
        "-p", "--password",
        help="Password for SMB authentication."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    parser.add_argument(
        "-a", "--anonymous",
        help="Use anonymous SMB authentication"
    )
    parser.set_defaults(func=run)