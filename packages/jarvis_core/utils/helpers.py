"""Utility helper functions for JARVIS Core"""
import uuid
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    """Generate unique ID with optional prefix"""
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id

def current_timestamp() -> str:
    """Return current ISO timestamp"""
    return datetime.now().isoformat()

def safe_filename(text: str) -> str:
    """Convert string to safe filename"""
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)[:100]
