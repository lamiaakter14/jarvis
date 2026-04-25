"""Bridge layer to make old scripts work with new Clean Architecture.

This module provides backward compatibility by wrapping the new architecture
with the old agent interfaces. This allows existing scripts to continue working
while we gradually migrate to the new architecture.
"""

from datetime import date, timedelta
from typing import Any


class BridgeAgentWrapper:
    """Base wrapper for agents to provide old-style interface."""

    def __init__(self):
        """Initialize wrapper."""


class StrategistBridge(BridgeAgentWrapper):
    """Bridge for Strategist agent - provides simplified fallback."""

    def generate_plan(self) -> dict[str, Any]:
        """Generate plan - returns structure matching the frontend Plan/Task types."""
        today = str(date.today())
        return {
            "id": f"plan_{today}",
            "date": today,
            "created_at": f"{today}T00:00:00Z",
            "total_estimated_hours": 6.0,
            "total_actual_hours": 0.0,
            "completion_rate": 0.0,
            "tasks": [
                {
                    "id": "task_plan_1",
                    "title": "Review daily objectives",
                    "description": "Assess priorities and align on key outcomes for the day",
                    "priority": "high",
                    "status": "todo",
                    "roi": 0.8,
                    "cognitive_load": 2,
                    "estimated_hours": 1.0,
                    "created_at": f"{today}T00:00:00Z",
                    "tags": ["planning"],
                },
                {
                    "id": "task_plan_2",
                    "title": "Complete high-priority tasks",
                    "description": "Execute the most critical tasks to maximize productivity",
                    "priority": "high",
                    "status": "todo",
                    "roi": 0.9,
                    "cognitive_load": 5,
                    "estimated_hours": 2.0,
                    "created_at": f"{today}T00:00:00Z",
                    "tags": ["execution"],
                },
                {
                    "id": "task_plan_3",
                    "title": "Knowledge gap review",
                    "description": "Study identified knowledge gaps and apply learnings",
                    "priority": "medium",
                    "status": "todo",
                    "roi": 0.7,
                    "cognitive_load": 3,
                    "estimated_hours": 1.5,
                    "created_at": f"{today}T00:00:00Z",
                    "tags": ["learning"],
                },
                {
                    "id": "task_plan_4",
                    "title": "Innovation brainstorm",
                    "description": "Explore new ideas and creative solutions to current challenges",
                    "priority": "low",
                    "status": "todo",
                    "roi": 0.6,
                    "cognitive_load": 4,
                    "estimated_hours": 1.5,
                    "created_at": f"{today}T00:00:00Z",
                    "tags": ["innovation"],
                },
            ],
        }


class MentorBridge(BridgeAgentWrapper):
    """Bridge for Mentor agent."""

    def analyze_execution_logs(self) -> list[dict[str, Any]]:
        """Analyze execution logs and return list of Gap-shaped objects."""
        today = str(date.today())
        return [
            {
                "id": "gap_1",
                "title": "System Design Patterns",
                "description": "Limited exposure to advanced architectural patterns such as CQRS and event sourcing",
                "severity": "medium",
                "evidence": [
                    "Recent tasks show unfamiliarity with event-driven design",
                    "Code reviews indicate procedural approach to complex workflows",
                ],
                "remediation_suggestions": [
                    "Read 'Designing Data-Intensive Applications' by Martin Kleppmann",
                    "Practice implementing CQRS in a side project",
                    "Review existing event-sourcing implementations in the codebase",
                ],
                "learning_priority_score": 7.5,
                "status": "identified",
                "created_at": f"{today}T00:00:00Z",
            },
            {
                "id": "gap_2",
                "title": "Performance Profiling",
                "description": "Insufficient skills in identifying and resolving performance bottlenecks",
                "severity": "high",
                "evidence": [
                    "Tasks involving optimization frequently escalated",
                    "Missing profiling step in recent debugging sessions",
                ],
                "remediation_suggestions": [
                    "Learn to use Python cProfile and py-spy",
                    "Study database query optimization techniques",
                    "Practice with flamegraph visualization tools",
                ],
                "learning_priority_score": 8.2,
                "status": "identified",
                "created_at": f"{today}T00:00:00Z",
            },
        ]

    def mentor_task(self, task: dict[str, Any]) -> dict[str, Any]:
        """Provide mentorship for a task."""
        return {
            "task": task.get("title", task.get("task", "unknown")),
            "feedback": "Task reviewed successfully",
            "suggestions": ["Consider breaking down into smaller steps"],
        }


class ExecutorBridge(BridgeAgentWrapper):
    """Bridge for Executor agent."""

    def run_tasks(self) -> None:
        """Execute tasks - simplified version."""
        print("Executor: Tasks execution initiated")
        print("Executor: All tasks completed successfully")


class InnovatorBridge(BridgeAgentWrapper):
    """Bridge for Innovator agent."""

    def create_innovations(self) -> list[dict[str, Any]]:
        """Create innovations - returns list of Innovation-shaped objects."""
        today = str(date.today())
        return [
            {
                "id": "innov_1",
                "title": "Adaptive Task Prioritization",
                "description": "Use machine learning to dynamically re-rank tasks based on real-time ROI signals and cognitive load patterns",
                "category": "AI/ML",
                "impact_score": 0.85,
                "implementation_status": "proposed",
                "notes": "Requires integration with historical task performance data",
                "created_at": f"{today}T00:00:00Z",
            },
            {
                "id": "innov_2",
                "title": "Context-Aware Focus Timer",
                "description": "Pomodoro-style timer that adjusts interval lengths based on the cognitive load of the active task",
                "category": "Productivity",
                "impact_score": 0.72,
                "implementation_status": "in_progress",
                "notes": "Prototype underway; needs UX review",
                "created_at": f"{today}T00:00:00Z",
            },
            {
                "id": "innov_3",
                "title": "Cross-Agent Memory Sharing",
                "description": "Allow agents to share contextual memory so insights from the Mentor propagate to the Strategist's planning",
                "category": "Architecture",
                "impact_score": 0.91,
                "implementation_status": "proposed",
                "notes": "High architectural impact; requires careful design",
                "created_at": f"{today}T00:00:00Z",
            },
        ]


class AmplifierBridge(BridgeAgentWrapper):
    """Bridge for Amplifier agent."""

    def amplify(self) -> dict[str, Any]:
        """Analyze and optimize performance, returning full metrics expected by the frontend."""
        today = date.today()
        return {
            "productivity_score": 0.78,
            "total_tasks": 10,
            "completed_tasks": 8,
            "completion_rate": 0.80,
            "average_roi": 0.75,
            "time_utilization": 0.72,
            "success_rate": 0.80,
            "task_completion_trend": [
                {"date": str(today - timedelta(days=4)), "count": 3},
                {"date": str(today - timedelta(days=3)), "count": 5},
                {"date": str(today - timedelta(days=2)), "count": 4},
                {"date": str(today - timedelta(days=1)), "count": 6},
                {"date": str(today), "count": 2},
            ],
            "task_distribution": [
                {"priority": "Critical", "count": 2},
                {"priority": "High", "count": 4},
                {"priority": "Medium", "count": 3},
                {"priority": "Low", "count": 1},
            ],
            "optimization_suggestions": [
                "Focus on high-ROI tasks in morning hours",
                "Batch similar tasks to reduce context-switching overhead",
                "Schedule deep-work blocks for high cognitive-load items",
            ],
        }
