"""Task entity for the domain layer."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.shared.constants import TaskStatus
from jarvis_core.shared.exceptions import DomainException
from jarvis_core.shared.utils import current_timestamp, generate_id


@dataclass
class Task:
    """Task entity representing a unit of work in the system.

    Tasks are the fundamental units of execution, containing all information
    needed for planning, prioritization, and execution by agents.
    """

    task_id: str = field(default_factory=lambda: generate_id("task_"))
    title: str = ""
    description: str = ""
    priority: Priority = field(default_factory=lambda: Priority.MEDIUM)
    cognitive_load: CognitiveLoad = field(default_factory=lambda: CognitiveLoad.MEDIUM)
    roi: ROI = field(default_factory=lambda: ROI(0.5))
    status: TaskStatus = TaskStatus.PENDING
    agent_type: AgentType = field(default_factory=lambda: AgentType.EXECUTOR)

    created_at: datetime = field(default_factory=current_timestamp)
    updated_at: datetime = field(default_factory=current_timestamp)
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None

    def __post_init__(self):
        """Validate task after initialization."""
        if not self.title:
            raise DomainException("Task title cannot be empty")

    def mark_in_progress(self) -> None:
        """Mark the task as in progress.

        Raises:
            DomainException: If task is already completed or failed
        """
        if self.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            raise DomainException(f"Cannot mark {self.status.value} task as in progress")

        self.status = TaskStatus.IN_PROGRESS
        self.updated_at = current_timestamp()

    def mark_completed(self, result: Optional[Any] = None) -> None:
        """Mark the task as completed.

        Args:
            result: Optional result data from task execution

        Raises:
            DomainException: If task is already completed or failed
        """
        if self.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            raise DomainException(f"Cannot complete task with status: {self.status.value}")

        self.status = TaskStatus.COMPLETED
        self.completed_at = current_timestamp()
        self.updated_at = self.completed_at
        self.result = result

    def mark_failed(self, error: Optional[str] = None) -> None:
        """Mark the task as failed.

        Args:
            error: Optional error message describing the failure
        """
        self.status = TaskStatus.FAILED
        self.updated_at = current_timestamp()
        if error:
            self.result = {"error": error}

    def calculate_duration(self) -> Optional[float]:
        """Calculate the duration of task execution.

        Returns:
            Duration in seconds if completed, None otherwise
        """
        if self.completed_at is None:
            return None

        return (self.completed_at - self.created_at).total_seconds()

    def is_pending(self) -> bool:
        """Check if task is pending."""
        return self.status == TaskStatus.PENDING

    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == TaskStatus.IN_PROGRESS

    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == TaskStatus.COMPLETED

    def is_failed(self) -> bool:
        """Check if task is failed."""
        return self.status == TaskStatus.FAILED

    def is_high_priority(self) -> bool:
        """Check if task has high or critical priority."""
        return self.priority in (Priority.HIGH, Priority.CRITICAL)

    def is_high_roi(self) -> bool:
        """Check if task has high ROI."""
        return self.roi.is_high_value()

    def get_score(self) -> float:
        """Calculate overall task score for prioritization.

        Combines priority weight, ROI, and cognitive load into a single score.
        Higher score indicates higher importance and efficiency.

        Returns:
            Task score (0.0 to 1.0)
        """
        # Map priority to weight
        priority_weights = {
            Priority.LOW: 0.25,
            Priority.MEDIUM: 0.50,
            Priority.HIGH: 0.75,
            Priority.CRITICAL: 1.0,
        }
        priority_weight = priority_weights.get(self.priority, 0.5)

        # Weight: Priority 40%, ROI 40%, Efficiency 20%
        efficiency = 1.0 - min(self.cognitive_load.estimated_hours / 8.0, 1.0)
        score = priority_weight * 0.4 + self.roi.value * 0.4 + efficiency * 0.2
        return score

    def can_fit_in_schedule(self, available_hours: float) -> bool:
        """Check if task can fit in available time.

        Args:
            available_hours: Available hours in schedule

        Returns:
            True if task fits, False otherwise
        """
        return self.cognitive_load.estimated_hours <= available_hours

    def get_estimated_hours(self) -> float:
        """Get estimated hours for this task.

        Returns:
            Estimated hours based on cognitive load
        """
        return self.cognitive_load.estimated_hours

    def to_dict(self) -> dict:
        """Convert task to dictionary.

        Returns:
            Dictionary representation of the task
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "cognitive_load": self.cognitive_load.value,
            "roi": self.roi.value,
            "status": self.status.value if hasattr(self.status, "value") else self.status,
            "agent_type": self.agent_type.value if self.agent_type else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
        }

    def __eq__(self, other) -> bool:
        """Check equality based on task_id only."""
        if not isinstance(other, Task):
            return False
        return self.task_id == other.task_id

    def __hash__(self) -> int:
        """Hash based on task_id."""
        return hash(self.task_id)

    def __str__(self) -> str:
        """String representation of the task."""
        return f"{self.title} ({self.status.value})"

    def __repr__(self) -> str:
        """Detailed representation of the task."""
        return (
            f"Task(id={self.task_id}, title={self.title}, "
            f"priority={self.priority}, status={self.status.value})"
        )
