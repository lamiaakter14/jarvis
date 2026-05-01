"""Phase 11: Advanced Intent Engine V2 - Goal Type + Urgency + Complexity."""

from typing import Dict, Any, List
import re

class IntentEngineV2:
    """Detects intent with goal type, urgency level, complexity, and required agents."""
    
    def __init__(self):
        self.version = "2.0.0"
    
    def detect(self, message: str) -> Dict[str, Any]:
        lower = message.lower()
        
        return {
            "type": self._detect_type(lower),
            "domain": self._detect_domain(lower),
            "urgency": self._detect_urgency(lower),
            "complexity": self._detect_complexity(message),
            "required_agents": self._get_required_agents(lower),
            "confidence": self._get_confidence(lower),
            "entities": self._extract_entities(message)
        }
    
    def _detect_type(self, text: str) -> str:
        if any(kw in text for kw in ["plan", "idea", "start", "create", "build", "design", "strategy", "খুলতে", "বানাবো"]):
            return "plan"
        elif any(kw in text for kw in ["do", "execute", "run", "deploy", "push", "commit"]):
            return "execute"
        elif any(kw in text for kw in ["what", "why", "how", "explain", "কি", "কেন", "কিভাবে"]):
            return "question"
        elif any(kw in text for kw in ["log", "diary", "note", "remember", "save"]):
            return "memory"
        elif any(kw in text for kw in ["money", "income", "earn", "টাকা", "budget", "price"]):
            return "money"
        return "chat"
    
    def _detect_domain(self, text: str) -> str:
        domains = {
            "business": ["business", "shop", "store", "bar", "restaurant", "startup", "client", "revenue", "profit"],
            "coding": ["code", "website", "app", "api", "github", "deploy", "bug", "feature", "programming"],
            "life": ["goal", "career", "future", "election", "mp", "marriage", "study", "skill", "network"],
            "money": ["money", "income", "earn", "টাকা", "budget", "price", "sell", "buy", "investment"],
            "content": ["blog", "article", "post", "video", "social media", "youtube", "write", "content"]
        }
        for domain, keywords in domains.items():
            if any(kw in text for kw in keywords):
                return domain
        return "general"
    
    def _detect_urgency(self, text: str) -> str:
        # Check for time pressure keywords
        high_urgency = ["asap", "urgent", "immediately", "now", "today", "আজই", "জলদি", "emergency"]
        medium_urgency = ["this week", "soon", "quick", "fast", "৭ দিন", "3 day", "5 day"]
        
        if any(kw in text for kw in high_urgency):
            return "high"
        elif any(kw in text for kw in medium_urgency):
            return "medium"
        return "low"
    
    def _detect_complexity(self, text: str) -> str:
        word_count = len(text.split())
        has_multi_step = any(kw in text.lower() for kw in ["phase", "step", "first", "then", "after", "plan", "strategy"])
        has_tech = any(kw in text.lower() for kw in ["code", "api", "database", "server", "deploy", "github"])
        
        if word_count > 20 and (has_multi_step or has_tech):
            return "high"
        elif word_count > 10:
            return "medium"
        return "low"
    
    def _get_required_agents(self, text: str) -> List[str]:
        agents = []
        if self._detect_type(text) == "plan":
            agents.append("strategist")
            if self._detect_complexity(text) in ["medium", "high"]:
                agents.append("validator")
        if any(kw in text for kw in ["execute", "run", "do", "build"]):
            agents.append("executor")
        if any(kw in text for kw in ["remember", "context", "learn", "past"]):
            agents.append("memory")
        agents.append("communicator")
        return agents
    
    def _get_confidence(self, text: str) -> float:
        # Higher confidence when keywords clearly match
        type_indicators = len([kw for kw in ["plan", "execute", "question", "log", "money"] if kw in text])
        return min(0.95, 0.5 + (type_indicators * 0.15))
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        entities = {}
        
        # Extract amounts
        amount_match = re.search(r'(\d+)\s*(টাকা|taka|bdt|tk|usd|\$)', text.lower())
        if amount_match:
            entities["amount"] = int(amount_match.group(1))
        
        # Extract days
        days_match = re.search(r'(\d+)\s*(day|দিন|days)', text.lower())
        if days_match:
            entities["days"] = int(days_match.group(1))
        
        # Extract project name
        project_match = re.search(r'(?:called|named|নাম)\s+["\']?(\w+)', text.lower())
        if project_match:
            entities["project_name"] = project_match.group(1)
        
        return entities
