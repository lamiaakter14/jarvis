"""Phase 10: Structured Output Builder."""

from typing import Dict, List, Any
from datetime import datetime

class OutputBuilder:
    """Builds structured, production-grade output."""
    
    @staticmethod
    def build(intent: str, mode: str, response: str, meta: Dict = None) -> Dict:
        return {
            "status": "success",
            "version": "10.0.0",
            "timestamp": datetime.now().isoformat(),
            "intent": intent,
            "mode": mode,
            "primary": {
                "message": response,
                "type": "chat" if intent == "unknown" else intent
            },
            "artifacts": OutputBuilder._build_artifacts(intent, meta or {}),
            "next_actions": OutputBuilder._build_next_actions(intent, meta or {}),
            "memory_updates": OutputBuilder._build_memory_updates(intent, meta or {}),
            "meta": meta or {}
        }
    
    @staticmethod
    def _build_artifacts(intent: str, meta: Dict) -> List[Dict]:
        artifacts = []
        if meta.get("project"):
            artifacts.append({"type": "project", "id": meta["project"].get("id"), "title": meta["project"].get("title")})
        if meta.get("questions"):
            artifacts.append({"type": "questions", "count": len(meta["questions"])})
        if meta.get("execution"):
            artifacts.append({"type": "execution", "tasks_done": meta["execution"].get("tasks_executed", 0)})
        return artifacts
    
    @staticmethod
    def _build_next_actions(intent: str, meta: Dict) -> List[str]:
        actions = []
        if intent == "planner" and meta.get("project"):
            actions = ["Review plan", "Edit details", "Approve & Execute"]
        elif intent == "execution":
            actions = ["Open Execution Hub", "View Diary"]
        elif intent == "unknown":
            actions = ["Try: 'start business'", "Try: 'log: today'", "Try: 'need 5000'"]
        return actions
    
    @staticmethod
    def _build_memory_updates(intent: str, meta: Dict) -> List[str]:
        updates = []
        if meta.get("project"):
            updates.append(f"Project {meta['project'].get('id')} created")
        if meta.get("context_used"):
            updates.append(f"Context loaded: {meta['context_used']}")
        return updates
