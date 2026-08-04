from core.exceptions import FileInputError, TargetError
from dataclasses import dataclass
from pathlib import Path
import re
import ipaddress

DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$"
)

@dataclass(slots=True)
class TargetCollection:
    source: str
    kind: str
    targets: list[str]

def is_ipv4(target: str) -> bool:
    try:
        ip = ipaddress.ip_address(target)
        if ip == 4:
            return True
        else:
            return False
        
    except ValueError:
        return False

def is_ipv6(target: str) -> bool:
    try:
        ip = ipaddress.ip_address(target)
        if ip == 6:
            return True
        else:
            return False
        
    except ValueError:
        return False

def is_file_target(target: str) -> bool:
    return Path(target).is_file()

def is_domain(target: str) -> bool:
    return bool(DOMAIN_REGEX.fullmatch(target))

def classify_target(target: str) -> str:
    """Return the target type (ipv4, ipv6, or domain)."""
    if is_ipv4(target):
        return "ipv4"
    if is_ipv6(target):
        return "ipv6"
    if is_domain(target):
        return "domain"
    raise TargetError(f"Unsupported target format: {target}")

def load_targets_from_file(file_path: str) -> list[str]:
    """
    Load and sanitize targets from a file.

    Reads the file content, splits it into lines, strips whitespace,
    and filters out empty lines.

    Args:
        file_path (str): Path to the target file.

    Returns:
        list[str]: List of cleaned target strings.

    Raises:
        FileInputError:
            - if the file does not exist
            - if the path is not a file
            - if the file cannot be read
            - if the file is empty after processing
    """

    path = Path(file_path)

    if not path.exists():
        raise FileInputError(f"Target file not found: {file_path}")
    if not path.is_file():
        raise FileInputError(f"Target path is not a file: {file_path}")

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise FileInputError(f"Unable to read target file: {file_path}") from exc

    targets = [line.strip() for line in lines if line.strip()]

    if not targets:
        raise FileInputError(f"Target file is empty: {file_path}")

    return targets

def normalize_target_input(target: str) -> TargetCollection:    
    """
    Normalize user-provided target input into a structured TargetCollection.

    The input may be:
    - a single target (IPv4, IPv6, or domain)
    - a file path containing multiple targets

    For file inputs:
    - loads all targets from file
    - classifies each target
    - determines if targets are homogeneous or mixed

    Returns:
        TargetCollection: structured representation of the input

    Raises:
        TargetError: if input is empty or invalid
        FileInputError: if file cannot be read or is invalid
    """

    if not target or not target.strip():
        raise TargetError("Target input cannot be empty.")

    target = target.strip()

    if is_file_target(target):
        targets = load_targets_from_file(target)
        classified = [classify_target(item) for item in targets]
        kind = classified[0] if len(set(classified)) == 1 else "mixed"

        return TargetCollection(
            source="file",
            kind=kind,
            targets=targets,
        )

    return TargetCollection(
        source="single",
        kind=classify_target(target),
        targets=[target],
    )
