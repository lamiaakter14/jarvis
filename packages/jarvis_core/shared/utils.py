"""Shared utility functions for the JARVIS application."""

import json
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, Optional


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix.
    
    Args:
        prefix: Optional prefix for the ID
        
    Returns:
        Unique identifier string
    """
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}{unique_id}" if prefix else unique_id


def safe_json_load(file_path: Path) -> Dict[str, Any]:
    """Safely load JSON from a file, returning empty dict if file doesn't exist.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Loaded JSON data or empty dict
    """
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}


def safe_json_dump(file_path: Path, data: Dict[str, Any], indent: int = 4) -> None:
    """Safely dump JSON to a file, creating parent directories if needed.
    
    Args:
        file_path: Path to save the JSON file
        data: Data to serialize
        indent: JSON indentation level
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
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


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized
