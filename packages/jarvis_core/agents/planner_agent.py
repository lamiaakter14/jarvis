"""Planner Agent - Dynamic question engine."""

from typing import Dict, List
from uuid import uuid4

class PlannerAgent:
    def __init__(self):
        self.name = "PlannerAgent"
        self.version = "5.3.0"
    
    def detect_type(self, message: str) -> str:
        lower = message.lower()
        if any(kw in lower for kw in ["website", "web", "site", "landing", "blog"]):
            return "website"
        elif any(kw in lower for kw in ["business", "shop", "store", "bar", "restaurant", "startup", "খুলতে"]):
            return "business"
        elif any(kw in lower for kw in ["money", "income", "earn", "টাকা", "salary"]):
            return "money"
        elif any(kw in lower for kw in ["goal", "life", "career", "future", "election", "mp"]):
            return "life"
        return "general"
    
    def generate_questions(self, project_type: str, title: str = "") -> List[str]:
        question_bank = {
            "business": [
                f"কেন এই business: {title}?",
                "Target customer কে? Location কোথায়?",
                "Competition analysis — কে আছে?",
                "তুমি unique কী দিচ্ছো?",
                "Initial budget কত? Monthly cost?",
                "Revenue model — কিভাবে টাকা আসবে?",
                "Timeline — কবে থেকে শুরু?",
                "Risk factors — কী কী হতে পারে?"
            ],
            "website": [
                f"Website-এর purpose কী? {title}",
                "Target audience কারা?",
                "কী ধরনের content/structure দরকার?",
                "Design style — modern/minimal/corporate?",
                "Tech stack — কোন technology?",
                "Hosting + Domain budget?",
                "Launch timeline?"
            ],
            "money": [
                "কত টাকা দরকার? কত দিনে?",
                "তোমার current skills কী কী?",
                "Daily কত ঘণ্টা দিতে পারবে?",
                "কোন platform-এ কাজ করতে চাও? (Fiverr/Upwork/Local)",
                "আগে কোনো freelance experience আছে?",
                "Portfolio/Profile ready আছে?",
                "Minimum hourly rate কত চাও?"
            ],
            "life": [
                f"এই goal-টি কেন important: {title}?",
                "Long-term vision — ৫/১০ বছর পর কী দেখতে চাও?",
                "Current position — এখন কোথায় আছো?",
                "Gap analysis — কী skills/resources দরকার?",
                "Milestones — ছোট ছোট target কী হবে?",
                "Timeline — realistic deadline কত?",
                "Support system — কারা help করবে?"
            ],
            "general": [
                f"এই project-এর main objective কী: {title}?",
                "Timeline — কত দিনের plan দরকার?",
                "Resources — কী কী লাগবে?",
                "Constraints — কী limitations আছে?",
                "Priority — কত urgent?",
                "Expected outcome — success দেখতে কেমন?"
            ]
        }
        return question_bank.get(project_type, question_bank["general"])
    
    def create_project_plan(self, title: str, project_type: str = "general", answers: Dict[int, str] = None) -> Dict:
        phases_map = {
            "business": ["Market Research", "Business Plan", "Legal Setup", "Branding", "Product/Service", "Marketing", "Launch"],
            "website": ["Planning", "Design", "Development", "Content", "Testing", "Launch"],
            "money": ["Skill Assessment", "Platform Setup", "Profile Creation", "Active Bidding", "Client Work", "Review & Scale"],
            "life": ["Vision Setting", "Gap Analysis", "Skill Building", "Network Building", "Milestone Tracking", "Review & Adjust"],
            "general": ["Research", "Planning", "Execution", "Review"]
        }
        phases = phases_map.get(project_type, phases_map["general"])
        return {
            "id": f"PROJ-{uuid4().hex[:8].upper()}",
            "title": title,
            "type": project_type,
            "phases": [{"name": p, "order": i+1} for i, p in enumerate(phases)],
            "tasks": [{"id": f"T{i+1:02d}", "title": f"{p} task", "phase": p, "status": "pending"} for i, p in enumerate(phases)],
            "answers": answers or {}
        }
    
    def plan(self, message: str, answers: Dict[int, str] = None) -> Dict:
        project_type = self.detect_type(message)
        title = message[:50] if len(message) > 50 else message
        questions = self.generate_questions(project_type, title)
        project = self.create_project_plan(title, project_type, answers)
        return {"project": project, "questions": questions, "type": project_type, "planner_version": self.version}
