"""Planner Agent - Converts ideas into structured project plans."""

from typing import Dict, List
from uuid import uuid4

class PlannerAgent:
    def __init__(self):
        self.name = "PlannerAgent"
        self.version = "3.0.0"
    
    def analyze_input(self, message: str) -> Dict:
        lower = message.lower()
        if any(kw in lower for kw in ["website", "web", "site"]):
            return {"project_type": "website", "confidence": 0.8}
        elif any(kw in lower for kw in ["business", "shop", "store", "startup"]):
            return {"project_type": "business", "confidence": 0.8}
        return {"project_type": "default", "confidence": 0.5}
    
    def generate_questions(self, project_title: str) -> List[str]:
        return [
            f"কেন এই project: {project_title}?",
            "Target customer কে?",
            "Competition কে?",
            "তুমি unique কী দিচ্ছো?",
            "Budget কত?",
            "Timeline?",
            "Risk factor?",
        ]
    
    def create_project_plan(self, title: str, project_type: str = "default") -> Dict:
        phases = ["Research", "Planning", "Design", "Development", "Launch"]
        tasks = []
        for i, phase in enumerate(phases):
            tasks.append({"id": f"T{i+1:02d}", "title": f"{phase} task", "phase": phase, "status": "pending"})
        return {"id": f"PROJ-{uuid4().hex[:8].upper()}", "title": title, "phases": [{"name": p, "order": i+1} for i,p in enumerate(phases)], "tasks": tasks}
    
    def plan(self, message: str) -> Dict:
        analysis = self.analyze_input(message)
        project = self.create_project_plan(message[:50], analysis["project_type"])
        questions = self.generate_questions(message[:50])
        return {"project": project, "questions": questions, "analysis": analysis, "planner_version": self.version}
