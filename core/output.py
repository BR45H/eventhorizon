def info(message: str) -> None:
    print(f"[+] {message}")


def warning(message: str) -> None:
    print(f"[!] {message}")


def error(message: str) -> None:
    print(f"[-] {message}")


def success(message: str) -> None:
    print(f"[✓] {message}")