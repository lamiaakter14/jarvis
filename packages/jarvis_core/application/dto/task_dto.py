"""Task Data Transfer Object for application layer."""

from datetime import datetime
from typing import Any, Optional

from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.shared.constants import TaskStatus
from pydantic import BaseModel, ConfigDict, Field


class TaskDTO(BaseModel):
    """Data Transfer Object for Task entity.

    Provides a serializable representation of tasks for API and
    application layer communication with data validation.
    """

    model_config = ConfigDict(from_attributes=True)

    task_id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Detailed task description")
    priority: str = Field(..., description="Task priority level")
    cognitive_load: str = Field(..., description="Cognitive load level")
    roi: float = Field(..., ge=0.0, le=1.0, description="Return on investment score")
    status: str = Field(..., description="Current task status")
    agent_type: Optional[str] = Field(None, description="Type of agent assigned to task")

    created_at: Optional[datetime] = Field(None, description="Task creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    result: Optional[Any] = Field(None, description="Task execution result")

    @classmethod
    def from_entity(cls, task: Task) -> "TaskDTO":
        """Convert Task entity to DTO.

        Args:
            task: Task entity to convert

        Returns:
            TaskDTO instance
        """
        return cls(
            task_id=task.task_id,
            title=task.title,
            description=task.description,
            priority=task.priority.value,
            cognitive_load=task.cognitive_load.value,
            roi=task.roi.value,
            status=task.status.value if hasattr(task.status, "value") else task.status,
            agent_type=task.agent_type.value if task.agent_type else None,
            created_at=task.created_at if hasattr(task, "created_at") else None,
            updated_at=task.updated_at if hasattr(task, "updated_at") else None,
            completed_at=task.completed_at if hasattr(task, "completed_at") else None,
            result=task.result if hasattr(task, "result") else None,
        )

    def to_entity(self) -> Task:
        """Convert DTO to Task entity.

        Returns:
            Task entity instance
        """
        # Parse priority
        priority = Priority(self.priority)

        # Parse cognitive load
        cognitive_load = CognitiveLoad(self.cognitive_load)

        # Create ROI
        roi = ROI(self.roi)

        # Parse agent type
        agent_type = AgentType(self.agent_type) if self.agent_type else None

        # Parse status
        try:
            status = TaskStatus(self.status)
        except (ValueError, AttributeError):
            status = self.status

        return Task(
            task_id=self.task_id,
            title=self.title,
            description=self.description,
            priority=priority,
            cognitive_load=cognitive_load,
            roi=roi,
            status=status,
            agent_type=agent_type,
            created_at=self.created_at,
            updated_at=self.updated_at,
            completed_at=self.completed_at,
            result=self.result,
        )

    def to_dict(self) -> dict:
        """Convert DTO to dictionary.

        Returns:
            Dictionary representation of the task
        """
        return self.model_dump()
