"""Plan Data Transfer Object for application layer."""

from datetime import date as date_type, datetime
from typing import List, Dict, TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from jarvis_core.domain.entities.plan import Plan
    from jarvis_core.application.dto.task_dto import TaskDTO


class PlanDTO(BaseModel):
    """Data Transfer Object for Plan entity.
    
    Provides a serializable representation of daily plans for API and
    application layer communication with data validation.
    """
    
    plan_id: str = Field(..., description="Unique identifier for the plan")
    date: date_type = Field(..., description="Date for which the plan is created")
    tasks: List["TaskDTO"] = Field(default_factory=list, description="List of tasks in the plan")
    total_hours: float = Field(..., gt=0, le=24, description="Total hours available")
    status: str = Field(..., description="Plan status (draft, active, completed, archived)")
    created_by: str = Field(default="system", description="Creator of the plan")
    created_at: datetime = Field(..., description="Plan creation timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            date_type: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
    
    @classmethod
    def from_entity(cls, plan: "Plan") -> "PlanDTO":
        """Convert Plan entity to DTO.
        
        Args:
            plan: Plan entity to convert
            
        Returns:
            PlanDTO instance
        """
        from jarvis_core.application.dto.task_dto import TaskDTO
        
        return cls(
            plan_id=plan.plan_id,
            date=plan.date,
            tasks=[TaskDTO.from_entity(task) for task in plan.tasks],
            total_hours=plan.total_hours,
            status=plan.status,
            created_by=plan.created_by,
            created_at=plan.created_at,
        )
    
    def to_dict(self) -> Dict:
        """Convert DTO to dictionary.
        
        Returns:
            Dictionary representation of the plan
        """
        data = self.model_dump()
        # Convert nested task DTOs to dicts
        data["tasks"] = [task for task in data["tasks"]]
        return data
    
    def get_planned_hours(self) -> float:
        """Calculate total planned hours.
        
        Returns:
            Sum of all task estimated hours
        """
        # Parse cognitive load from task DTOs to get estimated hours
        total = 0.0
        for task in self.tasks:
            # Parse cognitive load to get hours
            from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
            load = CognitiveLoad.from_string(task.cognitive_load)
            total += load.estimated_hours
        return total
    
    def get_remaining_hours(self) -> float:
        """Calculate remaining available hours.
        
        Returns:
            Hours remaining after planned tasks
        """
        return self.total_hours - self.get_planned_hours()
    
    def get_completion_percentage(self) -> float:
        """Calculate plan completion percentage.
        
        Returns:
            Completion percentage (0.0 to 100.0)
        """
        if not self.tasks:
            return 0.0
        
        completed = sum(1 for task in self.tasks if task.status == "completed")
        return (completed / len(self.tasks)) * 100.0
