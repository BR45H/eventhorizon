from core.exceptions import FileInputError, TargetError
from dataclasses import dataclass
from pathlib import Path
import re

HEX_CHARS = set("0123456789ABCDEF")

DOMAIN_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$"
)

@dataclass(slots=True)
class TargetCollection:
    source: str
    kind: str
    targets: list[str]

def is_ipv4(target: str) -> bool:
    # Basic IPv4 validation using manual parsing (dotted decimal notation)
    if target.count(".") != 3:
        return False
    
    parts = target.split(".")

    try:
        for part in parts:
            num = int(part)

            if not (0 <= num <= 255):
                return False
            
    except ValueError:
        return False
    
    return True

def is_ipv6(target: str) -> bool:
    """Validate IPv6 addresses using manual parsing.

    Supports standard and compressed notation (e.g. '::') by validating
    group structure, hexadecimal characters, and group length (up to 4 hex digits per group).

    This implementation focuses on common IPv6 formats and does not cover
    all edge cases from the full IPv6 specification.
    """
    # NOTE:
    # IPv4-mapped IPv6 addresses (e.g. ::ffff:192.168.0.1) are not supported yet :(
    
    if not target:
        return False
    if target.count("::") > 1:
        return False
    
    if "::" in target:
        left, right = target.split("::")

        left_parts = left.split(":") if left else []
        right_parts = right.split(":") if right else []

        parts = left_parts + right_parts
        count = 0

        for part in parts:
            count += 1

        if count >= 8:
            return False

    else:
        if target.count(":") != 7:
            return False
    
        parts = target.split(":")
    
    for part in parts:
        if part == "":
            return False
        c = 0
        for char in part:
            c += 1
            if char.upper() not in HEX_CHARS:
                return False
            if c > 4:
                return False

    return True

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
