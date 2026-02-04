"""Generic JSON storage utility for file-based persistence."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from jarvis_core.shared.exceptions import RepositoryError


class JsonStorage:
    """Generic JSON storage utility.
    
    Provides methods to safely load, save, and manage JSON files
    with automatic directory creation and error handling.
    """
    
    def __init__(self, base_path: str = "memory"):
        """Initialize JSON storage.
        
        Args:
            base_path: Base directory path for storage
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def load(self, file_path: str, default: Optional[Dict] = None) -> Dict[str, Any]:
        """Load JSON data from a file.
        
        Args:
            file_path: Relative path to the JSON file
            default: Default value if file doesn't exist
            
        Returns:
            Loaded JSON data or default
            
        Raises:
            RepositoryError: If file read or JSON parsing fails
        """
        full_path = self.base_path / file_path
        
        if not full_path.exists():
            return default if default is not None else {}
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RepositoryError(f"Invalid JSON in {file_path}: {e}")
        except Exception as e:
            raise RepositoryError(f"Failed to load {file_path}: {e}")
    
    def save(self, file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
        """Save JSON data to a file.
        
        Args:
            file_path: Relative path to the JSON file
            data: Data to save
            indent: JSON indentation level
            
        Raises:
            RepositoryError: If file write fails
        """
        full_path = self.base_path / file_path
        
        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=self._json_serializer, ensure_ascii=False)
        except Exception as e:
            raise RepositoryError(f"Failed to save {file_path}: {e}")
    
    def list_files(self, pattern: str = "*.json") -> List[Path]:
        """List all JSON files matching a pattern.
        
        Args:
            pattern: Glob pattern for matching files
            
        Returns:
            List of Path objects for matching files
        """
        try:
            return list(self.base_path.rglob(pattern))
        except Exception as e:
            raise RepositoryError(f"Failed to list files: {e}")
    
    def exists(self, file_path: str) -> bool:
        """Check if a file exists.
        
        Args:
            file_path: Relative path to check
            
        Returns:
            True if file exists
        """
        full_path = self.base_path / file_path
        return full_path.exists()
    
    def delete(self, file_path: str) -> None:
        """Delete a file.
        
        Args:
            file_path: Relative path to delete
            
        Raises:
            RepositoryError: If file deletion fails
        """
        full_path = self.base_path / file_path
        
        if not full_path.exists():
            return
        
        try:
            full_path.unlink()
        except Exception as e:
            raise RepositoryError(f"Failed to delete {file_path}: {e}")
    
    def get_full_path(self, file_path: str) -> Path:
        """Get full path for a relative path.
        
        Args:
            file_path: Relative path
            
        Returns:
            Full Path object
        """
        return self.base_path / file_path
    
    def ensure_directory(self, dir_path: str) -> None:
        """Ensure a directory exists.
        
        Args:
            dir_path: Relative directory path
        """
        full_path = self.base_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _json_serializer(obj: Any) -> str:
        """Custom JSON serializer for non-standard types.
        
        Args:
            obj: Object to serialize
            
        Returns:
            JSON-serializable representation
            
        Raises:
            TypeError: If object is not serializable
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        elif hasattr(obj, 'value'):  # For Enums
            return obj.value
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def append_to_list(self, file_path: str, item: Dict[str, Any]) -> None:
        """Append an item to a JSON list file.
        
        Args:
            file_path: Relative path to the JSON file
            item: Item to append
            
        Raises:
            RepositoryError: If operation fails
        """
        data = self.load(file_path, default={"items": []})
        
        if "items" not in data:
            data["items"] = []
        
        data["items"].append(item)
        self.save(file_path, data)
    
    def clear_list(self, file_path: str) -> None:
        """Clear all items in a JSON list file.
        
        Args:
            file_path: Relative path to the JSON file
        """
        self.save(file_path, {"items": []})
    
    def get_list_items(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all items from a JSON list file.
        
        Args:
            file_path: Relative path to the JSON file
            
        Returns:
            List of items
        """
        data = self.load(file_path, default={"items": []})
        return data.get("items", [])
