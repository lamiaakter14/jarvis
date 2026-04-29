"""
JARVIS Intent Engine
Phase 2: Basic rule-based intent detection
"""

from typing import Dict, Any


def detect_intent(message: str) -> Dict[str, Any]:
    """
    Detect user intent from message text.
    
    Returns:
        dict with intent, mode, confidence
    """
    lower = message.lower().strip()
    
    # Planning keywords
    planning_keywords = ["plan", "idea", "start", "business", "create", "project", "build plan", "strategy"]
    
    # Execution keywords
    execution_keywords = ["do", "execute", "run", "build", "deploy", "complete", "finish", "start task"]
    
    # Advisor/Question keywords
    advisor_keywords = ["what", "why", "how", "when", "who", "explain", "help", "analyze"]
    
    # Check planning
    if any(kw in lower for kw in planning_keywords):
        return {
            "intent": "planner",
            "mode": "planner",
            "confidence": 0.85,
            "trigger": "planning_keyword"
        }
    
    # Check execution
    if any(kw in lower for kw in execution_keywords):
        return {
            "intent": "execution",
            "mode": "execution",
            "confidence": 0.75,
            "trigger": "execution_keyword"
        }
    
    # Check advisor
    if any(kw in lower for kw in advisor_keywords):
        return {
            "intent": "advisor",
            "mode": "advisor",
            "confidence": 0.7,
            "trigger": "question_keyword"
        }
    
    # Default
    return {
        "intent": "unknown",
        "mode": "chat",
        "confidence": 0.3,
        "trigger": "default"
    }


def generate_response(intent: str, message: str) -> str:
    """
    Generate response based on detected intent.
    Phase 2: Template-based responses.
    """
    responses = {
        "planner": "🧠 Planner mode activated. Let's design your plan. I will ask you key questions to structure it properly.",
        "execution": "⚡ Execution mode ready. Waiting for approved tasks to begin processing.",
        "advisor": "🎓 Advisor mode activated. I can help you analyze and understand this better.",
        "unknown": "I received your message. Can you clarify if you want to plan something, execute tasks, or get advice?",
    }
    return responses.get(intent, responses["unknown"])