"""
Digital Diary Service for Jarvis OS
Manages daily journal entries with file attachments
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from uuid import uuid4

# Storage paths
BASE_DIR = Path("/Users/mahedihasanmuktadir/jarvis")
DIARY_ROOT = BASE_DIR / "memory" / "diary"

# Supported file types
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'video': ['.mp4', '.mov', '.avi', '.mkv'],
    'audio': ['.mp3', '.wav', '.m4a', '.ogg'],
    'document': ['.pdf', '.txt', '.md']
}

MAX_FILE_SIZE = {
    'image': 50 * 1024 * 1024,  # 50MB
    'video': 200 * 1024 * 1024,  # 200MB
    'audio': 100 * 1024 * 1024,  # 100MB
    'document': 50 * 1024 * 1024  # 50MB
}


@dataclass
class DiaryEntry:
    """Represents a diary entry"""
    id: str
    date: str  # YYYY-MM-DD
    content: str
    attachments: List[Dict[str, str]]  # [{filename: str, path: str, type: str, size: int}]
    tags: List[str]
    mood: Optional[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()


class DiaryService:
    """Service for managing diary entries"""
    
    def __init__(self):
        """Initialize diary service and ensure storage directory exists"""
        self.diary_root = DIARY_ROOT
        self.diary_root.mkdir(parents=True, exist_ok=True)
        self.entries_cache = {}
    
    def _get_date_path(self, date: str) -> Path:
        """Get directory path for a specific date"""
        return self.diary_root / date
    
    def _get_entry_file_path(self, date: str, entry_id: str) -> Path:
        """Get file path for entry metadata"""
        return self._get_date_path(date) / f"{entry_id}.json"
    
    def _get_attachment_path(self, date: str, entry_id: str, filename: str) -> Path:
        """Get path for an attachment"""
        return self._get_date_path(date) / "attachments" / entry_id / filename
    
    def save_entry(self, date: str, content: str, tags: List[str] = None, 
                   mood: str = None, attachments: List[Dict] = None) -> DiaryEntry:
        """Save or update a diary entry"""
        # Check if entry already exists for this date
        existing = self.get_entry_by_date(date)
        
        if existing:
            # Update existing entry
            entry = existing
            entry.content = content
            entry.tags = tags or entry.tags
            entry.mood = mood or entry.mood
            entry.updated_at = datetime.now().isoformat()
            if attachments:
                entry.attachments.extend(attachments)
        else:
            # Create new entry
            entry = DiaryEntry(
                id=str(uuid4()),
                date=date,
                content=content,
                attachments=attachments or [],
                tags=tags or [],
                mood=mood
            )
        
        # Save to disk
        date_path = self._get_date_path(date)
        date_path.mkdir(parents=True, exist_ok=True)
        
        entry_file = self._get_entry_file_path(date, entry.id)
        with open(entry_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(entry), f, indent=2, ensure_ascii=False)
        
        # Update cache
        self.entries_cache[date] = entry
        
        return entry
    
    def get_entry_by_date(self, date: str) -> Optional[DiaryEntry]:
        """Get entry for a specific date"""
        # Check cache first
        if date in self.entries_cache:
            return self.entries_cache[date]
        
        # Try to load from disk
        date_path = self._get_date_path(date)
        if not date_path.exists():
            return None
        
        # Find JSON file in this date directory
        json_files = list(date_path.glob("*.json"))
        if not json_files:
            return None
        
        entry_file = json_files[0]
        try:
            with open(entry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                entry = DiaryEntry(**data)
                self.entries_cache[date] = entry
                return entry
        except Exception as e:
            print(f"Error loading entry for {date}: {e}")
            return None
    
    def get_all_entries(self, limit: int = 50, offset: int = 0) -> List[DiaryEntry]:
        """Get all diary entries sorted by date (newest first)"""
        entries = []
        
        # Iterate through date directories
        date_dirs = sorted([d for d in self.diary_root.iterdir() if d.is_dir()], reverse=True)
        
        for date_dir in date_dirs:
            date = date_dir.name
            entry = self.get_entry_by_date(date)
            if entry:
                entries.append(entry)
        
        # Apply pagination
        return entries[offset:offset + limit]
    
    def search_entries(self, query: str) -> List[DiaryEntry]:
        """Search entries by content or tags"""
        results = []
        all_entries = self.get_all_entries(limit=1000)  # Get all for search
        
        query_lower = query.lower()
        for entry in all_entries:
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
        
        return results
    
    def save_attachment(self, date: str, entry_id: str, filename: str, 
                        file_content: bytes, file_type: str) -> Dict[str, str]:
        """Save an attachment for an entry"""
        # Validate file size
        file_size = len(file_content)
        max_size = MAX_FILE_SIZE.get(file_type, 50 * 1024 * 1024)
        
        if file_size > max_size:
            raise ValueError(f"File too large. Max {max_size // (1024*1024)}MB for {file_type}")
        
        # Validate extension
        ext = Path(filename).suffix.lower()
        allowed_exts = ALLOWED_EXTENSIONS.get(file_type, [])
        
        if allowed_exts and ext not in allowed_exts:
            raise ValueError(f"File type {ext} not allowed for {file_type}")
        
        # Create attachment directory
        attachment_dir = self._get_attachment_path(date, entry_id, "")
        attachment_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename to avoid collisions
        unique_filename = f"{datetime.now().strftime('%H%M%S')}_{filename}"
        attachment_path = attachment_dir / unique_filename
        
        # Save file
        with open(attachment_path, 'wb') as f:
            f.write(file_content)
        
        return {
            'filename': filename,
            'saved_as': unique_filename,
            'path': str(attachment_path.relative_to(BASE_DIR)),
            'type': file_type,
            'size': file_size
        }
    
    def delete_entry(self, date: str) -> bool:
        """Delete an entire diary entry and its attachments"""
        entry = self.get_entry_by_date(date)
        if not entry:
            return False
        
        # Delete entry directory
        date_path = self._get_date_path(date)
        if date_path.exists():
            shutil.rmtree(date_path)
        
        # Remove from cache
        if date in self.entries_cache:
            del self.entries_cache[date]
        
        return True
    
    def get_entry_summary(self, date: str) -> Dict[str, Any]:
        """Get summary statistics for an entry"""
        entry = self.get_entry_by_date(date)
        if not entry:
            return {'exists': False}
        
        return {
            'exists': True,
            'date': date,
            'word_count': len(entry.content.split()),
            'char_count': len(entry.content),
            'attachment_count': len(entry.attachments),
            'tags': entry.tags,
            'mood': entry.mood
        }
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics for diary"""
        total_size = 0
        total_entries = 0
        total_attachments = 0
        
        for date_dir in self.diary_root.iterdir():
            if date_dir.is_dir():
                total_entries += 1
                # Calculate size
                for file in date_dir.rglob('*'):
                    if file.is_file():
                        total_size += file.stat().st_size
                        if 'attachments' in str(file):
                            total_attachments += 1
        
        return {
            'total_entries': total_entries,
            'total_attachments': total_attachments,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'storage_path': str(self.diary_root)
        }