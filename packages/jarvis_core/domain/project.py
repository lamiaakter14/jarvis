"""Project domain model for JARVIS Planner Agent."""

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone


@dataclass
class Phase:
    """A phase within a project."""
    id: str
    name: str
    order: int
    status: str = "pending"  # pending, in_progress, completed
    description: str = ""


@dataclass
class Task:
    """A task within a phase."""
    id: str
    title: str
    phase_id: str
    status: str = "pending"  # pending, in_progress, done
    priority: str = "medium"  # low, medium, high, critical
    estimated_hours: float = 1.0
    assignee: str = "executor"


@dataclass
class Project:
    """A project created by Planner Agent."""
    id: str
    title: str
    description: str = ""
    phases: List[Phase] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    status: str = "draft"  # draft, planning, approved, in_progress, completed
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = f"PROJ-{uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "phases": [
                {"id": p.id, "name": p.name, "order": p.order, "status": p.status, "description": p.description}
                for p in self.phases
            ],
            "tasks": [
                {"id": t.id, "title": t.title, "phase_id": t.phase_id, "status": t.status, "priority": t.priority, "estimated_hours": t.estimated_hours, "assignee": t.assignee}
                for t in self.tasks
            ],
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# ============================================================
# Template-based project generation
# ============================================================
PROJECT_TEMPLATES = {
    "business": {
        "phases": [
            "Market Research",
            "Business Plan",
            "Legal Setup",
            "Branding",
            "Product/Service Development",
            "Marketing & Launch",
        ],
        "tasks_per_phase": 2,
    },
    "website": {
        "phases": [
            "Planning & Research",
            "Design",
            "Development",
            "Content Creation",
            "Testing",
            "Launch",
        ],
        "tasks_per_phase": 2,
    },
    "software": {
        "phases": [
            "Requirements Analysis",
            "System Design",
            "Implementation",
            "Testing",
            "Deployment",
            "Maintenance",
        ],
        "tasks_per_phase": 3,
    },
    "default": {
        "phases": [
            "Research & Analysis",
            "Planning",
            "Execution",
            "Review & Optimize",
        ],
        "tasks_per_phase": 2,
    },
}

TASK_TEMPLATES = {
    "Market Research": ["Identify target audience", "Analyze competitors"],
    "Business Plan": ["Write executive summary", "Define revenue model"],
    "Legal Setup": ["Register business name", "Get necessary licenses"],
    "Branding": ["Design logo concept", "Create brand guidelines"],
    "Product/Service Development": ["Define MVP features", "Create prototype"],
    "Marketing & Launch": ["Create social media strategy", "Plan launch event"],
    "Planning & Research": ["Define project scope", "Research competitors"],
    "Design": ["Create wireframes", "Design UI mockups"],
    "Development": ["Set up development environment", "Build core features"],
    "Content Creation": ["Write homepage copy", "Create blog content"],
    "Testing": ["Perform QA testing", "Fix critical bugs"],
    "Launch": ["Deploy to production", "Announce on social media"],
    "Requirements Analysis": ["Gather user requirements", "Document specifications"],
    "System Design": ["Design architecture", "Create database schema"],
    "Implementation": ["Set up project structure", "Implement core modules"],
    "Deployment": ["Configure server", "Deploy application"],
    "Maintenance": ["Set up monitoring", "Create backup strategy"],
    "Research & Analysis": ["Research topic", "Analyze findings"],
    "Planning": ["Create timeline", "Allocate resources"],
    "Execution": ["Execute main tasks", "Track progress"],
    "Review & Optimize": ["Review results", "Document learnings"],
}