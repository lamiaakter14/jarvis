"""
Local Context Engine — Bangladesh-specific knowledge base
Phase 7: Local Context for Sakhipur, Partex, and local markets
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

class ContextStore:
    """Store and retrieve local context (prices, places, culture)"""
    
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            storage_path = Path.home() / ".jarvis" / "contexts.json"
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.contexts = self._load()
    
    def _load(self) -> List[Dict[str, Any]]:
        """Load contexts from JSON file"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_sample_contexts()
    
    def _get_sample_contexts(self) -> List[Dict[str, Any]]:
        """Sample Bangladesh/Sakhipur contexts"""
        return [
            {
                "id": "ctx-001",
                "category": "market_price",
                "key": "Partex timber",
                "value": "৳1,200 per cft",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ctx-002",
                "category": "labour",
                "key": "Local labour rate",
                "value": "৳500 per day",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ctx-003",
                "category": "market_price",
                "key": "Cement price",
                "value": "৳450 per bag",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ctx-004",
                "category": "market_price",
                "key": "Brick (per 1000)",
                "value": "৳8,000-9,000",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ctx-005",
                "category": "labour",
                "key": "Mason wage",
                "value": "৳800 per day",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "ctx-006",
                "category": "transport",
                "key": "Partex to Sakhipur CNG",
                "value": "৳30-40 per trip",
                "location": "Sakhipur",
                "source": "system",
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def _save(self):
        """Save contexts to JSON file"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.contexts, f, indent=2, ensure_ascii=False)
    
    def get_all(self, category: str = None) -> List[Dict[str, Any]]:
        """Get all contexts, optionally filtered by category"""
        if category:
            return [c for c in self.contexts if c.get("category") == category]
        return self.contexts
    
    def get_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search contexts by keyword"""
        keyword_lower = keyword.lower()
        return [
            c for c in self.contexts 
            if keyword_lower in c.get("key", "").lower() 
            or keyword_lower in c.get("value", "").lower()
        ]
    
    def add(self, key: str, value: str, category: str, location: str = "Sakhipur") -> Dict[str, Any]:
        """Add new context"""
        new_context = {
            "id": f"ctx-{len(self.contexts)+1:03d}",
            "category": category,
            "key": key,
            "value": value,
            "location": location,
            "source": "user_input",
            "created_at": datetime.now().isoformat()
        }
        self.contexts.append(new_context)
        self._save()
        return new_context
    
    def update(self, context_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update existing context"""
        for i, ctx in enumerate(self.contexts):
            if ctx["id"] == context_id:
                self.contexts[i].update(updates)
                self._save()
                return self.contexts[i]
        return None
    
    def delete(self, context_id: str) -> bool:
        """Delete context by ID"""
        original_length = len(self.contexts)
        self.contexts = [c for c in self.contexts if c["id"] != context_id]
        if len(self.contexts) < original_length:
            self._save()
            return True
        return False
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return list(set(c.get("category", "other") for c in self.contexts))
    
    def get_for_planner(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Get relevant contexts for planner based on keywords"""
        results = []
        for keyword in keywords:
            results.extend(self.get_by_keyword(keyword))
        # Remove duplicates by id
        seen = set()
        unique_results = []
        for r in results:
            if r["id"] not in seen:
                seen.add(r["id"])
                unique_results.append(r)
        return unique_results[:10]  # Max 10 contexts

# Singleton instance
context_store = ContextStore()
