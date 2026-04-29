"""Planner Agent - Converts ideas into structured project plans."""

from typing import Dict, List, Optional
from uuid import uuid4

from ..domain.project import Project, Phase, Task, PROJECT_TEMPLATES, TASK_TEMPLATES


class PlannerAgent:
    """
    Planner Agent analyzes user input and creates structured project plans.
    Phase 3: Template-based plan generation.
    """
    
    def __init__(self):
        self.name = "PlannerAgent"
        self.version = "3.0.0"
    
    def analyze_input(self, message: str) -> Dict:
        """
        Analyze user input to detect project type.
        """
        lower = message.lower()
        
        if any(kw in lower for kw in ["website", "web app", "site"]):
            return {"project_type": "website", "confidence": 0.8}
        elif any(kw in lower for kw in ["software", "app", "tool", "platform"]):
            return {"project_type": "software", "confidence": 0.8}
        elif any(kw in lower for kw in ["business", "shop", "store", "startup", "company"]):
            return {"project_type": "business", "confidence": 0.8}
        else:
            return {"project_type": "default", "confidence": 0.5}
    
    def generate_questions(self, project_title: str) -> List[str]:
        """
        Generate mandatory questions for the user.
        """
        return [
            f"কেন এই project: {project_title}? (Why this?)",
            "Target customer/audience কে?",
            "Competition কে বা কী?",
            "তুমি unique কী দিচ্ছো?",
            "Budget কত?",
            "Timeline কেমন?",
            "Risk factor কী কী?",
        ]
    
    def create_project_plan(self, title: str, description: str = "", project_type: str = "default") -> Project:
        """
        Create a structured project plan with phases and tasks.
        """
        template = PROJECT_TEMPLATES.get(project_type, PROJECT_TEMPLATES["default"])
        
        project = Project(
            id=f"PROJ-{uuid4().hex[:8].upper()}",
            title=title,
            description=description,
            status="planning",
        )
        
        # Generate phases
        for i, phase_name in enumerate(template["phases"]):
            phase = Phase(
                id=f"PH-{i+1:02d}",
                name=phase_name,
                order=i + 1,
                status="pending",
                description=f"Phase {i+1}: {phase_name}",
            )
            project.phases.append(phase)
            
            # Generate tasks for each phase
            task_templates = TASK_TEMPLATES.get(phase_name, ["Research", "Document findings"])
            for j, task_title in enumerate(task_templates[:template["tasks_per_phase"]]):
                task = Task(
                    id=f"{project.id}-T{i+1:02d}{j+1:02d}",
                    title=task_title,
                    phase_id=phase.id,
                    status="pending",
                    priority="medium" if i < 2 else "low",
                    estimated_hours=2.0 + (i * 1.5),
                    assignee="executor",
                )
                project.tasks.append(task)
        
        return project
    
    def plan(self, message: str) -> Dict:
        """
        Full planning pipeline: analyze → create project → return structured plan.
        """
        # Analyze input
        analysis = self.analyze_input(message)
        
        # Create project
        project = self.create_project_plan(
            title=message[:50] if len(message) > 50 else message,
            description=message,
            project_type=analysis["project_type"],
        )
        
        # Generate questions
        questions = self.generate_questions(project.title)
        
        return {
            "project": project.to_dict(),
            "questions": questions,
            "analysis": analysis,
            "planner_version": self.version,
        }