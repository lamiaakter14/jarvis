"""Task Data Transfer Object for application layer."""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from src.domain.entities.task import Task
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.cognitive_load import CognitiveLoad
from src.domain.value_objects.roi import ROI
from src.domain.value_objects.agent_type import AgentType
from src.shared.constants import TaskStatus


class TaskDTO(BaseModel):
    """Data Transfer Object for Task entity.
    
    Provides a serializable representation of tasks for API and
    application layer communication with data validation.
    """
    
    task_id: str = Field(..., description="Unique identifier for the task")
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Detailed task description")
    priority: str = Field(..., description="Task priority level")
    cognitive_load: str = Field(..., description="Cognitive load level")
    roi: float = Field(..., ge=0.0, le=1.0, description="Return on investment score")
    status: str = Field(..., description="Current task status")
    agent_type: str = Field(..., description="Type of agent assigned to task")
    
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    result: Optional[Any] = Field(None, description="Task execution result")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
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
            priority=str(task.priority),
            cognitive_load=str(task.cognitive_load),
            roi=task.roi.value,
            status=task.status.value,
            agent_type=str(task.agent_type),
            created_at=task.created_at,
            updated_at=task.updated_at,
            completed_at=task.completed_at,
            result=task.result,
        )
    
    def to_entity(self) -> Task:
        """Convert DTO to Task entity.
        
        Returns:
            Task entity instance
        """
        # Parse priority
        priority = Priority.from_string(self.priority)
        
        # Parse cognitive load
        cognitive_load = CognitiveLoad.from_string(self.cognitive_load)
        
        # Create ROI
        roi = ROI(self.roi)
        
        # Parse agent type
        agent_type = AgentType.from_string(self.agent_type)
        
        # Parse status
        status = TaskStatus(self.status)
        
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
