
# Real SMB backend using Impacket.
# Requires Impacket (pip install impacket). Tested against Impacket 0.13.x.

from impacket.smbconnection import SMBConnection, SessionError
from impacket.nmb import NetBIOSError, NetBIOSTimeout
import socket

CONNECT_TIMEOUT = 5

class SMBBackend:
    def __init__(self) -> None:
        self._conn: SMBConnection | None = None

    def login(
        self,
        username: str | None = None,
        password: str | None = None,
        anonymous: bool = False,
        port: int = 445,
        target: str | None = None,
    ) -> bool:
        try:
            conn = SMBConnection(target, target, sess_port=port, timeout=CONNECT_TIMEOUT)

            if anonymous:
                conn.login("", "")
            else:
                conn.login(username or "", password or "")

        except (SessionError, NetBIOSError, NetBIOSTimeout, socket.error, OSError):
            self._conn = None
            return False

        self._conn = conn
        return True

    def list_shares(self) -> list[str]:
        if not self._conn:
            return []

        try:
            shares = self._conn.listShares()
        except (SessionError, NetBIOSError, NetBIOSTimeout):
            return []

        return [share["shi1_netname"][:-1] for share in shares]

    def use_share(self, share_name: str) -> bool:
        return share_name in self.list_shares()

    def list_current_path(self, share_name: str | None, path: str) -> list[str]:
        if not share_name or not self._conn:
            return []

        pattern = _to_smb_path(path) + "\\*"

        try:
            entries = self._conn.listPath(share_name, pattern)
        except (SessionError, NetBIOSError, NetBIOSTimeout):
            return []

        return [
            entry.get_longname()
            for entry in entries
            if entry.get_longname() not in (".", "..")
        ]

    def change_directory(self, share_name: str | None, current_path: str, new_path: str) -> str | None:
        if not share_name or not self._conn:
            return None

        if new_path == "..":
            if current_path == "/":
                return "/"

            parts = current_path.rstrip("/").split("/")
            return "/".join(parts[:-1]) or "/"

        new_full_path = (
            f"{current_path.rstrip('/')}/{new_path}"
            if current_path != "/"
            else f"/{new_path}"
        )

        try:
            entries = self._conn.listPath(share_name, _to_smb_path(new_full_path) + "\\*")
        except (SessionError, NetBIOSError, NetBIOSTimeout):
            return None

        return new_full_path if entries is not None else None

def _to_smb_path(path: str) -> str:
    return path.rstrip("/").replace("/", "\\")
