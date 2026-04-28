"""
JARVIS 3-Tier Memory System
Phase 4: Episodic, Semantic, Strategic Memory
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import os

class MemoryService:
    """3-tier cognitive memory: Episodic, Semantic, Strategic"""
    
    def __init__(self, storage_path: str = "memory_store"):
        self.storage_path = storage_path
        self.episodic: List[Dict] = []    # Recent experiences
        self.semantic: Dict[str, Any] = {} # Knowledge/facts
        self.strategic: List[Dict] = []    # Long-term patterns
        os.makedirs(storage_path, exist_ok=True)
    
    # Episodic Memory - Recent events
    def store_episode(self, event_type: str, data: Dict) -> Dict:
        episode = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "id": f"ep-{len(self.episodic)}"
        }
        self.episodic.append(episode)
        return episode
    
    def recall_recent(self, limit: int = 10) -> List[Dict]:
        return self.episodic[-limit:]
    
    # Semantic Memory - Knowledge/Facts
    def store_knowledge(self, key: str, value: Any) -> None:
        self.semantic[key] = {
            "value": value,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def recall_knowledge(self, key: str) -> Optional[Any]:
        item = self.semantic.get(key)
        return item["value"] if item else None
    
    # Strategic Memory - Patterns/Learnings
    def store_strategy(self, name: str, pattern: Dict) -> Dict:
        strategy = {
            "name": name,
            "pattern": pattern,
            "created_at": datetime.utcnow().isoformat(),
            "id": f"st-{len(self.strategic)}"
        }
        self.strategic.append(strategy)
        return strategy
    
    def get_strategies(self) -> List[Dict]:
        return self.strategic
    
    # Full context for agents
    def get_context(self, query: str = None) -> Dict:
        return {
            "recent_events": self.recall_recent(5),
            "knowledge_base": list(self.semantic.keys()),
            "strategies": len(self.strategic),
            "query": query
        }
