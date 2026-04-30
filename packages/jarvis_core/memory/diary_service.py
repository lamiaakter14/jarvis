"""
Diary Service for JARVIS OS
Manages digital diary entries with date-wise folder structure
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import json


class DiaryService:
    """Service for managing diary entries (text, images, videos, audio, PDF)"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.path.expanduser("~/jarvis/memory/diary")
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Metadata file path
        self.metadata_file = self.base_path / "metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from JSON file"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"entries": []}
    
    def _save_metadata(self):
        """Save metadata to JSON file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _get_date_folder(self, date_str: str = None) -> Path:
        """Get folder path for a specific date (YYYY-MM-DD)"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        date_folder = self.base_path / date_str
        date_folder.mkdir(parents=True, exist_ok=True)
        return date_folder
    
    def save_entry(
        self,
        file_content: bytes,
        original_filename: str,
        file_type: str,
        date_str: str = None
    ) -> Dict:
        """
        Save a diary entry
        
        Args:
            file_content: Binary content of the file
            original_filename: Original name of the file
            file_type: Type of file (text, image, video, audio, pdf)
            date_str: Date string (YYYY-MM-DD) - defaults to today
        
        Returns:
            Dict with entry metadata
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Create date folder
        date_folder = self._get_date_folder(date_str)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        name_parts = original_filename.rsplit('.', 1)
        if len(name_parts) > 1:
            base_name, ext = name_parts
            new_filename = f"{base_name}_{timestamp}.{ext}"
        else:
            new_filename = f"{original_filename}_{timestamp}"
        
        file_path = date_folder / new_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Create entry metadata
        entry = {
            "id": f"{date_str}_{timestamp}",
            "date": date_str,
            "timestamp": f"{date_str}T{timestamp}",
            "original_filename": original_filename,
            "saved_filename": new_filename,
            "file_type": file_type,
            "file_size": len(file_content),
            "file_path": str(file_path.relative_to(self.base_path)),
            "created_at": datetime.now().isoformat()
        }
        
        # Add to metadata
        self.metadata["entries"].append(entry)
        self._save_metadata()
        
        return entry
    
    def get_entries(self, date_str: str = None) -> List[Dict]:
        """
        Get diary entries
        
        Args:
            date_str: Optional date filter (YYYY-MM-DD)
        
        Returns:
            List of entries sorted by date (newest first)
        """
        entries = self.metadata.get("entries", [])
        
        if date_str:
            entries = [e for e in entries if e["date"] == date_str]
        
        # Sort by date descending
        entries.sort(key=lambda x: x["date"] + x["timestamp"], reverse=True)
        
        return entries
    
    def get_entry_by_id(self, entry_id: str) -> Optional[Dict]:
        """Get a specific entry by ID"""
        for entry in self.metadata.get("entries", []):
            if entry["id"] == entry_id:
                return entry
        return None
    
    def get_file_path(self, entry: Dict) -> Path:
        """Get full file path for an entry"""
        return self.base_path / entry["file_path"]
    
    def delete_entry(self, entry_id: str) -> bool:
        """Delete an entry and its file"""
        entry = self.get_entry_by_id(entry_id)
        if not entry:
            return False
        
        # Delete the file
        file_path = self.get_file_path(entry)
        if file_path.exists():
            file_path.unlink()
        
        # Remove from metadata
        self.metadata["entries"] = [
            e for e in self.metadata["entries"]
            if e["id"] != entry_id
        ]
        self._save_metadata()
        
        return True
    
    def get_dates_with_entries(self) -> List[str]:
        """Get list of dates that have entries"""
        dates = set()
        for entry in self.metadata.get("entries", []):
            dates.add(entry["date"])
        return sorted(dates, reverse=True)


# Global instance for easy import
_diary_service = None

def get_diary_service() -> DiaryService:
    """Get global diary service instance"""
    global _diary_service
    if _diary_service is None:
        _diary_service = DiaryService()
    return _diary_service
