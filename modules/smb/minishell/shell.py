from core.backends.smb_backend import SMBBackend
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

def cmd_pwd(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    output.success(f"{state.current_share}{state.current_path}\n")

def cmd_cd(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    if not args:
        output.error("Usage: cd <directory>\n")
        return

    new_path = backend.change_directory(state.current_share, state.current_path, args[0])

    if not new_path:
        output.error("Directory not found.\n")
        return

    state.current_path = new_path

def cmd_help(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    print("\n[ Event Horizon Shell ]\n")
    print("  help               Display this message")
    print("  shares             Enumerate available shares")
    print("  use <share>        Enter a share")
    print("  ls                 List current directory")
    print("  cd <dir>           Move through directories")
    print("  pwd                Show current location")
    print("  exit, quit         Terminate session\n")

def cmd_ls(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    if not state.current_share:
        output.error("No share selected.\n")
        return

    items = backend.list_current_path(state.current_share, state.current_path)

    if not items:
        output.warning("Empty directory.\n")
        return

    for item in items:
        output.success(item)
    print()
    
def cmd_shares(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    shares = backend.list_shares()

    if not shares:
        output.warning("No shares available.\n")
        return

    for share in shares:
        output.success(share)
    print()
    
def cmd_use(state: SessionState, backend: SMBBackend, args: list[str]) -> None:
    if not args:
        output.error("Usage: use <share>\n")
        return
    
    share_name = args[0]

    if not backend.use_share(share_name):
        output.error(f"Share not found: {share_name}\n")
        return

    state.current_share = share_name
    state.current_path = "/"
    output.success(f"Using share {share_name}\n")
    
COMMANDS = {
    "help": cmd_help,
    "ls": cmd_ls,
    "exit": cmd_exit,
    "quit": cmd_exit,
    "use": cmd_use,
    "shares": cmd_shares,
    "pwd": cmd_pwd,
    "cd": cmd_cd
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
        if not state.current_share:
            raw = input(f"{state.username}@{state.target}> ")
        else:
            raw = input(f"{state.username}@{state.target}:{state.current_share}{state.current_path}> ")
        parsed = parsing_shell_input(raw)

        if not parsed:
            continue

        cmd, args = parsed

        handler = COMMANDS.get(cmd)

        if not handler:
            output.error("Unknown command. Type 'help' for a list of commands.\n")
            continue

        handler(state, backend, args)
