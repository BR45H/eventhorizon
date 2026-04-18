from core.backends.sbm_backend import SMBBackend
from core import output

class SessionState:
    #Setting type for variables in class
    connected: bool
    authenticated: bool
    target: str | None
    username: str | None
    current_share: str | None
    current_path: str
    running: bool

    def __init__(self) -> None:
        #Setting value for variables
        self.connected = False
        self.authenticated = False
        self.target = None
        self.username = None
        self.current_share = None
        self.current_path = "/"
        self.running = True

def cmd_exit(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    state.running = False

def cmd_help(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
        print("Available commands:")
        print("  help               Show this help message")
        print("  shares             List available shares")
        print("  use <share>        Select a share")
        print("  ls                 List contents of current path")
        print("  exit / quit        Exit shell")

# def cmd_ls(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    # NOTE:
    # Continue later
    
def cmd_shares(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    shares = backend.list_shares()

    if not shares:
        output.warning("No shares available.")
        return

    for share in shares:
        output.success(share)
    
def cmd_use(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    if not args:
        output.error("Usage: use <share>")
        return
    
    share_name = args [0]

    if not backend.use_share(share_name):
        output.error(f"Share not found: {share_name}")
        return

    state.current_share = share_name
    state.current_path = "/"
    output.success(f"Using share {share_name}")
    
COMMANDS = {
    "help": cmd_help,
    "ls": cmd_ls,
    "exit": cmd_exit,
    "quit": cmd_exit,
    "use": cmd_use,
    "shares": cmd_shares
}

def parsing_shell_input(input: str) -> (tuple[str, list[str]] | None):
    if not input.strip():
        return None
    
    parts = input.split()
    return parts[0], parts[1:]

def init_shell(state: SessionState, backend: SMBBackend) -> None:
    if not state.connected:
        output.error("Not connected.")
        return

    if not state.authenticated:
        output.error("Not authenticated.")
        return
    
    while state.running:
        raw = input(f"smb:{state.target}> ")
        parsed = parsing_shell_input(raw)

        if not parsed:
            continue

        cmd, args = parsed

        handler = COMMANDS.get(cmd)

        if not handler:
            output.error("Unknown command. Type 'help' for a list of commands.")
            continue

        handler(state, backend, args)
