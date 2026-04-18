from core.target import normalize_target_input
from core.validator import validate_smb_connect_args
from modules.smb.minishell.shell import init_shell
from core import output
import argparse

def run(args: argparse.Namespace) -> None:
    validate_smb_connect_args(args)
    init_shell()


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
    parser.add_argument(
        "--port",
        help="Set port to connection (default -> 445)"
    )
    parser.set_defaults(func=run)
