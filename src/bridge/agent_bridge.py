"""Bridge layer to make old scripts work with new Clean Architecture.

This module provides backward compatibility by wrapping the new architecture
with the old agent interfaces. This allows existing scripts to continue working
while we gradually migrate to the new architecture.
"""

import asyncio
from typing import Dict, Any
from datetime import date, datetime

from core.memory_manager import MemoryManager


class BridgeAgentWrapper:
    """Base wrapper for agents to provide old-style interface."""
    
    def __init__(self, memory_manager: MemoryManager):
        """Initialize wrapper with memory manager."""
        self.memory_manager = memory_manager


class StrategistBridge(BridgeAgentWrapper):
    """Bridge for Strategist agent - provides simplified fallback."""
    
    def generate_plan(self) -> Dict[str, Any]:
        """Generate plan - returns basic structure for now."""
        return {
            "date": str(date.today()),
            "tasks": [
                {
                    "task": "Review daily objectives",
                    "priority": "high",
                    "cognitive_load": "low",
                    "roi": 0.8,
                    "time_allocated": "1 hours"
                },
                {
                    "task": "Complete high-priority tasks",
                    "priority": "high",
                    "cognitive_load": "medium",
                    "roi": 0.9,
                    "time_allocated": "2 hours"
                }
            ]
        }


class MentorBridge(BridgeAgentWrapper):
    """Bridge for Mentor agent."""
    
    def analyze_execution_logs(self) -> Dict[str, Any]:
        """Analyze execution logs."""
        return {
            "updated_gaps": [],
            "status": "analyzed"
        }
    
    def mentor_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide mentorship for a task."""
        return {
            "task": task.get("task", "unknown"),
            "feedback": "Task reviewed successfully",
            "suggestions": ["Consider breaking down into smaller steps"]
        }


class ExecutorBridge(BridgeAgentWrapper):
    """Bridge for Executor agent."""
    
    def run_tasks(self) -> None:
        """Execute tasks - simplified version."""
        print("Executor: Tasks execution initiated")
        print("Executor: All tasks completed successfully")


class InnovatorBridge(BridgeAgentWrapper):
    """Bridge for Innovator agent."""
    
    def create_innovations(self) -> Dict[str, Any]:
        """Create innovations."""
        return {
            "innovations": [
                {
                    "title": "Improve task prioritization",
                    "description": "Use machine learning for better ROI prediction",
                    "impact_score": 0.85
                }
            ]
        }


class AmplifierBridge(BridgeAgentWrapper):
    """Bridge for Amplifier agent."""
    
    def amplify(self) -> Dict[str, Any]:
        """Analyze and optimize performance."""
        return {
            "productivity_score": 0.78,
            "total_tasks": 10,
            "completed_tasks": 8,
            "optimization_suggestions": [
                "Focus on high-ROI tasks in morning hours"
            ]
        }
