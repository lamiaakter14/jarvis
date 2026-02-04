"""Task completed domain event."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from jarvis_core.domain.events.base_event import BaseEvent
from jarvis_core.shared.utils import generate_id, current_timestamp


@dataclass(frozen=True)
class TaskCompletedEvent(BaseEvent):
    """Event raised when a task is successfully completed.
    
    This event captures all relevant information about task completion,
    including execution time, agent details, and results.
    """
    
    task_id: str = ""
    agent_id: str = ""
    agent_type: str = ""
    timestamp: datetime = field(default_factory=current_timestamp)
    result: Optional[Any] = None
    duration_seconds: float = 0.0
    
    def __post_init__(self):
        """Initialize event with proper payload."""
        # Call parent post_init
        super().__post_init__()
        
        # Build payload from task completion data
        payload = {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "result": self.result,
            "duration_seconds": self.duration_seconds,
        }
        
        # Update payload field (workaround for frozen dataclass)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "event_type", "TaskCompletedEvent")
    
    def get_task_id(self) -> str:
        """Get the ID of the completed task.
        
        Returns:
            Task ID
        """
        return self.task_id
    
    def get_agent_id(self) -> str:
        """Get the ID of the agent that completed the task.
        
        Returns:
            Agent ID
        """
        return self.agent_id
    
    def was_successful(self) -> bool:
        """Check if task completed successfully.
        
        Returns:
            True if result exists and doesn't contain errors
        """
        if self.result is None:
            return False
        
        if isinstance(self.result, dict) and "error" in self.result:
            return False
        
        return True
    
    def get_duration_minutes(self) -> float:
        """Get task duration in minutes.
        
        Returns:
            Duration in minutes
        """
        return self.duration_seconds / 60.0
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"TaskCompletedEvent(task={self.task_id}, agent={self.agent_type})"
