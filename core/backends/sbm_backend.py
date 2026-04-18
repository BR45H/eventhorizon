class SMBBackend:
    def __init__(self) -> None:
        self._shares = {
            "PUBLIC": ["readme.txt", "notes.docx", "tools"],
            "TOOLS": ["scanner.py", "report.pdf"],
        }

    def login(self, username: str | None = None, password: str | None = None, anonymous: bool = False) -> bool:
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
        return self._shares.get(share_name, [])
    