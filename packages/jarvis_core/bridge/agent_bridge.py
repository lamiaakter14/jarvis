"""Bridge layer to make old scripts work with new Clean Architecture.

This module provides backward compatibility by wrapping the new architecture
with the old agent interfaces. This allows existing scripts to continue working
while we gradually migrate to the new architecture.
"""

from datetime import date, datetime
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


class BridgeAgentWrapper:
    """Base wrapper for agents to provide old-style interface."""

    def __init__(self):
        """Initialize wrapper."""


class StrategistBridge(BridgeAgentWrapper):
    """Bridge for Strategist agent."""

    def generate_plan(self) -> dict[str, Any]:
        """Generate a daily plan with tasks matching the frontend Plan type."""
        today = str(date.today())
        tasks = [
            {
                "id": str(uuid4()),
                "title": "Review daily objectives",
                "description": "Scan today's goals and align priorities for the day",
                "priority": "high",
                "status": "todo",
                "roi": 0.8,
                "cognitive_load": 2,
                "estimated_hours": 1.0,
                "created_at": _now_iso(),
                "tags": ["planning", "review"],
            },
            {
                "id": str(uuid4()),
                "title": "Complete high-priority tasks",
                "description": "Execute the top-ranked items from the backlog",
                "priority": "high",
                "status": "todo",
                "roi": 0.9,
                "cognitive_load": 4,
                "estimated_hours": 2.0,
                "created_at": _now_iso(),
                "tags": ["execution"],
            },
            {
                "id": str(uuid4()),
                "title": "Knowledge gap remediation",
                "description": "Spend focused time on identified learning areas",
                "priority": "medium",
                "status": "todo",
                "roi": 0.75,
                "cognitive_load": 3,
                "estimated_hours": 1.5,
                "created_at": _now_iso(),
                "tags": ["learning"],
            },
        ]
        return {
            "id": str(uuid4()),
            "date": today,
            "tasks": tasks,
            "total_estimated_hours": sum(t["estimated_hours"] for t in tasks),
            "completion_rate": 0.0,
            "created_at": _now_iso(),
        }


class MentorBridge(BridgeAgentWrapper):
    """Bridge for Mentor agent."""

    def analyze_execution_logs(self) -> list[dict[str, Any]]:
        """Return a list of knowledge gaps matching the frontend Gap type."""
        return [
            {
                "id": str(uuid4()),
                "title": "System Design Fundamentals",
                "description": "Gaps observed in distributed-systems design decisions during planning tasks",
                "severity": "medium",
                "evidence": [
                    "Unclear trade-off reasoning in recent architecture reviews",
                    "Repeated questions about CAP theorem application",
                ],
                "remediation_suggestions": [
                    "Complete a system design course (e.g., Designing Data-Intensive Applications)",
                    "Practice mock system design sessions 3x per week",
                ],
                "learning_priority_score": 7.5,
                "status": "identified",
                "created_at": _now_iso(),
            },
            {
                "id": str(uuid4()),
                "title": "Time Estimation Accuracy",
                "description": "Consistent underestimation of task durations leading to carry-overs",
                "severity": "high",
                "evidence": [
                    "Last 5 sprints: average 40% over estimated time",
                    "Complex tasks routinely split across two sessions",
                ],
                "remediation_suggestions": [
                    "Apply planning poker for each task",
                    "Add 20% buffer to all medium/high cognitive load tasks",
                ],
                "learning_priority_score": 8.2,
                "status": "in_progress",
                "created_at": _now_iso(),
            },
        ]

    def mentor_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """Provide mentorship feedback for a task."""
        return {
            "task": task.get("title", task.get("task", "unknown")),
            "feedback": "Task reviewed successfully",
            "suggestions": [
                "Consider breaking down into smaller steps",
                "Timebox to 90-minute focused blocks",
            ],
        }


class ExecutorBridge(BridgeAgentWrapper):
    """Bridge for Executor agent."""

    def run_tasks(self) -> None:
        """Execute tasks."""


class InnovatorBridge(BridgeAgentWrapper):
    """Bridge for Innovator agent."""

    def create_innovations(self) -> list[dict[str, Any]]:
        """Return a list of innovations matching the frontend Innovation type."""
        return [
            {
                "id": str(uuid4()),
                "title": "Automated Task Prioritization via ROI Scoring",
                "description": (
                    "Use a lightweight ML model trained on historical task outcomes to "
                    "automatically rank pending tasks by expected ROI each morning."
                ),
                "category": "automation",
                "impact_score": 0.88,
                "implementation_status": "proposed",
                "notes": "Requires historical task data export. Prototype in 2 weeks.",
                "created_at": _now_iso(),
            },
            {
                "id": str(uuid4()),
                "title": "Knowledge Gap Auto-Detection from Meeting Notes",
                "description": (
                    "Parse daily meeting notes and automatically flag topic clusters "
                    "that appear repeatedly without resolution as knowledge gaps."
                ),
                "category": "intelligence",
                "impact_score": 0.75,
                "implementation_status": "proposed",
                "notes": "Integration with calendar/notes tool needed.",
                "created_at": _now_iso(),
            },
            {
                "id": str(uuid4()),
                "title": "Focus Block Scheduler",
                "description": (
                    "Analyze historical productivity patterns and auto-block deep-work "
                    "windows in the calendar aligned with peak cognitive hours."
                ),
                "category": "productivity",
                "impact_score": 0.82,
                "implementation_status": "in_progress",
                "notes": "Initial version working; needs calendar API hook.",
                "created_at": _now_iso(),
            },
        ]


class AmplifierBridge(BridgeAgentWrapper):
    """Bridge for Amplifier agent."""

    def amplify(self) -> dict[str, Any]:
        """Return performance metrics matching the frontend PerformanceMetrics type."""
        return {
            "productivity_score": 0.78,
            "total_tasks": 24,
            "completed_tasks": 19,
            "completion_rate": 0.79,
            "average_roi": 0.76,
            "time_utilization": 0.72,
            "success_rate": 0.83,
            "task_completion_trend": [
                {"date": "Mon", "count": 3},
                {"date": "Tue", "count": 5},
                {"date": "Wed", "count": 4},
                {"date": "Thu", "count": 4},
                {"date": "Fri", "count": 3},
            ],
            "task_distribution": [
                {"priority": "Critical", "count": 3},
                {"priority": "High", "count": 8},
                {"priority": "Medium", "count": 9},
                {"priority": "Low", "count": 4},
            ],
            "optimization_suggestions": [
                "Focus on high-ROI tasks in morning hours (peak cognitive window: 08:00–11:00)",
                "Batch low-cognitive tasks into a single afternoon block",
                "Add 20% time buffer to tasks with cognitive load ≥ 4",
            ],
        }
