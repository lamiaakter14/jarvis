"""Phase 11: Strategist Agent - Advanced planning with domain expertise."""

from typing import Dict, List
from uuid import uuid4
from datetime import datetime, timezone

class StrategistAgent:
    """Generates structured plans with phases, tasks, and resource estimates."""
    
    def __init__(self):
        self.name = "Strategist"
        self.version = "2.0.0"
    
    def generate_plan(self, message: str, domain: str = "general", entities: Dict = None) -> Dict:
        project_id = f"PROJ-{uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        
        templates = {
            "business": {
                "phases": ["Market Research", "Business Plan", "Legal Setup", "Branding", "Product/Service", "Marketing", "Launch"],
                "tasks_per_phase": 2
            },
            "coding": {
                "phases": ["Requirements", "Architecture", "Development", "Testing", "Deployment", "Maintenance"],
                "tasks_per_phase": 2
            },
            "life": {
                "phases": ["Vision Setting", "Gap Analysis", "Skill Building", "Network Building", "Milestone Tracking", "Review"],
                "tasks_per_phase": 2
            },
            "money": {
                "phases": ["Skill Assessment", "Platform Setup", "Active Hustle", "Client Work", "Scale", "Optimize"],
                "tasks_per_phase": 2
            },
            "general": {
                "phases": ["Research", "Planning", "Execution", "Review"],
                "tasks_per_phase": 1
            }
        }
        
        template = templates.get(domain, templates["general"])
        phases = []
        tasks = []
        
        for i, phase_name in enumerate(template["phases"]):
            phase = {"name": phase_name, "order": i+1, "status": "pending", "id": f"PH-{i+1:02d}"}
            phases.append(phase)
            for j in range(template["tasks_per_phase"]):
                task = {
                    "id": f"{project_id}-T{i+1:02d}{j+1:02d}",
                    "title": f"{phase_name} - Task {j+1}",
                    "phase_id": phase["id"],
                    "status": "pending",
                    "estimated_hours": 2.0 + (i * 0.5)
                }
                tasks.append(task)
        
        return {
            "project_id": project_id,
            "title": message[:60],
            "domain": domain,
            "phases": phases,
            "tasks": tasks,
            "estimated_total_hours": sum(t["estimated_hours"] for t in tasks),
            "created_at": now,
            "status": "draft"
        }
    
    def plan(self, message: str, domain: str = "general", entities: Dict = None) -> Dict:
        return self.generate_plan(message, domain, entities)
