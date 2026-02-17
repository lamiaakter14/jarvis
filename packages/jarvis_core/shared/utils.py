"""Shared utility functions for the JARVIS application."""

import json
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix.

    Args:
        prefix: Optional prefix for the ID

    Returns:
        Unique identifier string
    """
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}{unique_id}" if prefix else unique_id


def safe_json_load(file_path: Path) -> dict[str, Any]:
    """Safely load JSON from a file, returning empty dict if file doesn't exist.

    Args:
        file_path: Path to the JSON file

    Returns:
        Loaded JSON data or empty dict
    """
    if file_path.exists():
        with open(file_path) as f:
            return json.load(f)
    return {}


def safe_json_dump(file_path: Path, data: dict[str, Any], indent: int = 4) -> None:
    """Safely dump JSON to a file, creating parent directories if needed.

    Args:
        file_path: Path to save the JSON file
        data: Data to serialize
        indent: JSON indentation level
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent, default=str)


def parse_date(date_str: str) -> date:
    """Parse a date string in YYYY-MM-DD format.

    Args:
        date_str: Date string to parse

    Returns:
        Parsed date object

    Raises:
        ValueError: If date string is invalid
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def current_date() -> date:
    """Get the current system date.

    Returns:
        Today's date
    """
    return date.today()


def current_timestamp() -> datetime:
    """Get the current system timestamp.

    Returns:
        Current datetime
    """
    return datetime.now()


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2h 30m", "45s")
    """
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.0f}m"
    else:
        hours = seconds / 3600
        minutes = (seconds % 3600) / 60
        return f"{hours:.0f}h {minutes:.0f}m"


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    r"""Sanitize a filename by removing invalid characters and path traversal attempts.

    This function provides protection against:
    - Invalid filesystem characters
    - Path traversal attacks (../, ..\)
    - Reserved filenames (CON, PRN, AUX, NUL, etc.)
    - Leading/trailing dots and spaces

    Args:
        filename: Original filename
        max_length: Maximum allowed filename length (default: 255)

    Returns:
        Sanitized filename safe for filesystem operations

    Raises:
        ValueError: If filename is empty or becomes empty after sanitization
    """
    import re

    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty")

    # Remove any path components (security: prevent directory traversal)
    filename = filename.split("/")[-1].split("\\")[-1]

    # Remove or replace invalid characters for common filesystems
    # Windows: < > : " / \ | ? *
    # Also remove control characters (0x00-0x1F) and brackets/parentheses
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f()\[\]]', "", filename)

    # Replace spaces and multiple underscores with single underscore
    sanitized = re.sub(r"\s+", "_", sanitized)
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing dots, spaces, and underscores (Windows reserved names)
    sanitized = sanitized.strip(". _")

    # Check for Windows reserved names
    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    name_without_ext = sanitized.split(".")[0].upper()
    if name_without_ext in reserved_names:
        sanitized = f"_{sanitized}"

    # Truncate to max length while preserving extension if possible
    if len(sanitized) > max_length:
        if "." in sanitized:
            name, ext = sanitized.rsplit(".", 1)
            max_name_len = max_length - len(ext) - 1
            sanitized = f"{name[:max_name_len]}.{ext}"
        else:
            sanitized = sanitized[:max_length]

    if not sanitized:
        raise ValueError("Filename becomes empty after sanitization")

    return sanitized
