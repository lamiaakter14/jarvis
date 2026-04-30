"""Phase 5: Digital Diary Service."""

import os
import json
from datetime import datetime
from typing import List, Optional

DIARY_BASE = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'memory', 'diary')

class DiaryService:
    def __init__(self):
        os.makedirs(DIARY_BASE, exist_ok=True)
    
    def create_entry(self, text: str, files: List[str] = None) -> dict:
        today = datetime.now().strftime("%Y-%m-%d")
        folder = os.path.join(DIARY_BASE, today)
        os.makedirs(folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"entry_{timestamp}.txt"
        filepath = os.path.join(folder, filename)
        
        with open(filepath, 'w') as f:
            f.write(text)
        
        metadata = {"date": today, "time": timestamp, "text": text, "files": files or []}
        meta_path = os.path.join(folder, "metadata.json")
        existing = []
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                existing = json.load(f)
        existing.append(metadata)
        with open(meta_path, 'w') as f:
            json.dump(existing, f, indent=2)
        
        return metadata
    
    def get_entries(self, date: str = None) -> List[dict]:
        if date:
            meta_path = os.path.join(DIARY_BASE, date, "metadata.json")
            if os.path.exists(meta_path):
                with open(meta_path) as f:
                    return json.load(f)
            return []
        
        entries = []
        if os.path.exists(DIARY_BASE):
            for date_folder in sorted(os.listdir(DIARY_BASE), reverse=True):
                meta_path = os.path.join(DIARY_BASE, date_folder, "metadata.json")
                if os.path.exists(meta_path):
                    with open(meta_path) as f:
                        entries.extend(json.load(f))
        return entries[:50]
    
    def list_dates(self) -> List[str]:
        if not os.path.exists(DIARY_BASE):
            return []
        return sorted([d for d in os.listdir(DIARY_BASE) if os.path.isdir(os.path.join(DIARY_BASE, d))], reverse=True)
