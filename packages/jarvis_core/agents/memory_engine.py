"""Phase 12: Memory Engine V2 - Pattern learning + Predictive suggestions."""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from collections import Counter

MEMORY_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'memory')

class MemoryEngine:
    """Learns from user behavior, tracks patterns, makes predictions."""
    
    def __init__(self):
        self.name = "Memory Engine"
        self.version = "2.0.0"
        os.makedirs(MEMORY_DIR, exist_ok=True)
    
    def log_interaction(self, user_input: str, intent: Dict, outcome: str = "success") -> Dict:
        """Log every interaction for pattern learning."""
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": user_input[:200],
            "intent_type": intent.get("type", "unknown"),
            "domain": intent.get("domain", "general"),
            "outcome": outcome
        }
        
        log_file = os.path.join(MEMORY_DIR, "interaction_log.json")
        logs = []
        if os.path.exists(log_file):
            with open(log_file) as f:
                logs = json.load(f)
        logs.append(log_entry)
        logs = logs[-100:]  # Keep last 100
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_entry
    
    def get_patterns(self) -> Dict:
        """Analyze user behavior patterns."""
        log_file = os.path.join(MEMORY_DIR, "interaction_log.json")
        if not os.path.exists(log_file):
            return {"status": "no_data", "message": "Not enough data yet"}
        
        with open(log_file) as f:
            logs = json.load(f)
        
        if len(logs) < 5:
            return {"status": "learning", "message": f"Only {len(logs)} interactions recorded"}
        
        # Analyze patterns
        intent_types = Counter(log["intent_type"] for log in logs)
        domains = Counter(log["domain"] for log in logs)
        success_rate = sum(1 for log in logs if log["outcome"] == "success") / len(logs) * 100
        
        # Detect behavior
        plan_count = intent_types.get("plan", 0)
        execute_count = intent_types.get("execute", 0)
        
        insights = []
        if plan_count > execute_count * 2:
            insights.append("📊 You plan more than you execute")
        if success_rate < 60:
            insights.append("⚠️ Low execution success rate")
        if domains.get("business", 0) > domains.get("coding", 0):
            insights.append("💼 Business-focused mindset detected")
        
        return {
            "total_interactions": len(logs),
            "favorite_intent": intent_types.most_common(1)[0][0] if intent_types else "unknown",
            "top_domain": domains.most_common(1)[0][0] if domains else "general",
            "success_rate": round(success_rate, 1),
            "insights": insights,
            "recent_activity": logs[-5:]
        }
    
    def suggest_next_action(self, current_intent: Dict) -> List[str]:
        """Suggest next actions based on past behavior."""
        suggestions = []
        intent_type = current_intent.get("type", "")
        domain = current_intent.get("domain", "")
        
        if intent_type == "plan":
            suggestions.append("Review generated plan")
            suggestions.append("Check for missing requirements")
        elif intent_type == "execute":
            suggestions.append("Track progress in Execution Hub")
            suggestions.append("Log completion to Diary")
        
        if domain == "business":
            suggestions.append("Save business details to Context")
        elif domain == "coding":
            suggestions.append("Commit to GitHub")
        
        return suggestions
    
    def save_project_memory(self, project: Dict) -> str:
        """Save project to persistent memory."""
        projects_dir = os.path.join(MEMORY_DIR, "projects")
        os.makedirs(projects_dir, exist_ok=True)
        
        filename = f"{project.get('project_id', 'unknown')}.json"
        filepath = os.path.join(projects_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(project, f, indent=2)
        
        return filepath
    
    def get_project_history(self) -> List[Dict]:
        """Get all past projects."""
        projects_dir = os.path.join(MEMORY_DIR, "projects")
        if not os.path.exists(projects_dir):
            return []
        
        projects = []
        for filename in os.listdir(projects_dir):
            if filename.endswith('.json'):
                with open(os.path.join(projects_dir, filename)) as f:
                    projects.append(json.load(f))
        
        return sorted(projects, key=lambda p: p.get('created_at', ''), reverse=True)
