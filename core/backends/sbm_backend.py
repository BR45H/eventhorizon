
# NOTE:
# Mock SMB backend used for development purposes.
# A real implementation using Impacket is planned, but currently skipped due to
# environment issues on Windows (pip/build problems).
# The architecture is already prepared to support a real backend later,
# especially in Linux/Unix environments.

class SMBBackend:
    def __init__(self) -> None:
        self._shares = {
            "PUBLIC": {
            "/": ["readme.txt", "notes.docx", "tools"],
            "/tools": ["scanner.py", "report.pdf"],
            },
            "TOOLS": {
            "/": ["scanner.py", "report.pdf", "bin"],
            "/bin": ["helper.exe", "config.ini"],
            },
        }

    def login(self, username: str | None = None, password: str | None = None, anonymous: bool = False, port: int = 445) -> bool:
        if port != 445:
            return False

        if anonymous:
            return True

        if username == "admin" and password == "admin":
            return True

        return False

    def list_shares(self) -> list[str]:
        return list(self._shares.keys())

    def use_share(self, share_name: str) -> bool:
        return share_name in self._shares

    def list_current_path(self, share_name: str | None, path: str) -> list[str]:
        if not share_name:
            return []

        share = self._shares.get(share_name)
        if not share:
            return []

        return share.get(path, [])
    
    def change_directory(self, share_name: str | None, current_path: str, new_path: str) -> str | None:
        if not share_name:
            return None
        
        share = self._shares.get(share_name)

        if new_path == "..":
            if current_path == "/":
                return "/"
            
            parts = current_path.rstrip("/").split("/")
            parent = "/".join(parts[:-1]) or "/"
            
            return parent if parent in share else "/"

        new_full_path = (
            f"{current_path.rstrip('/')}/{new_path}"
            if current_path != "/"
            else f"/{new_path}"
        )

        if new_full_path in share:
            return new_full_path

        return None
    