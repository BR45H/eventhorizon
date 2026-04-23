from core.exceptions import ValidationError
from core.target import normalize_target_input
from core.validator import validate_smb_connect_args
from modules.smb.minishell.shell import init_shell, SessionState
from core.backends.sbm_backend import SMBBackend
from core import output
import argparse

def run(args: argparse.Namespace) -> None:
    validate_smb_connect_args(args)
    target_data = normalize_target_input(args.target)
    port = args.port
    user = args.user
    password = args.password
    anonymous = args.anonymous
    
    state = SessionState()
    backend = SMBBackend()

    if target_data.source == "file":
        raise ValidationError("smb connect does not support file targets")
    
    if target_data.kind == "domain":
        raise ValidationError("Domain targets not supported yet. Use an IP address.")

    try:
        port = int(port)
        if port < 0 or port > 65535:
            output.error("Port must be between 0 and 65535.")
            return
    except ValueError:
        output.error("Invalid port. Use a numeric value.")
        return

    target = target_data.targets[0]

    authenticated = backend.login(
        username=user,
        password=password,
        anonymous=anonymous,
        port=port,
    )

    if not authenticated:
        output.error("Authentication failed.")
        return

    state.connected = True
    state.authenticated = True
    state.target = target
    state.username = "anonymous" if anonymous else user

    init_shell(state, backend)

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
        action="store_true",
        help="Use anonymous SMB authentication"
    )
    parser.add_argument(
        "--port",
        default=445,
        help="Set port to connection (default -> 445)"
    )
    parser.set_defaults(func=run)
