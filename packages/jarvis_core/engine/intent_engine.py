"""Phase 2: Intent Engine."""

def detect_intent(message: str) -> dict:
    lower = message.lower().strip()
    planning_kw = ["plan", "idea", "start", "business", "create", "project", "strategy", "open", "launch", "shop", "store"]
    execution_kw = ["do", "execute", "run", "build", "deploy", "complete", "finish"]
    advisor_kw = ["what", "why", "how", "when", "who", "explain", "help", "analyze"]
    
    if any(kw in lower for kw in planning_kw):
        return {"intent": "planner", "mode": "planner", "confidence": 0.85, "trigger": "planning_keyword"}
    if any(kw in lower for kw in execution_kw):
        return {"intent": "execution", "mode": "execution", "confidence": 0.75, "trigger": "execution_keyword"}
    if any(kw in lower for kw in advisor_kw):
        return {"intent": "advisor", "mode": "advisor", "confidence": 0.7, "trigger": "question_keyword"}
    return {"intent": "unknown", "mode": "chat", "confidence": 0.3, "trigger": "default"}

def generate_response(intent: str, message: str) -> str:
    responses = {
        "planner": "🧠 Planner mode activated. Let's design your plan.",
        "execution": "⚡ Execution mode ready.",
        "advisor": "🎓 Advisor mode activated. How can I help?",
        "unknown": "I received your message. Plan or execute?",
    }
    return responses.get(intent, responses["unknown"])
