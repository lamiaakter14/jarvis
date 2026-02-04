"""Plan entity for the domain layer."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

from src.domain.entities.task import Task
from src.shared.constants import TaskStatus
from src.shared.utils import generate_id, current_date, current_timestamp
from src.shared.exceptions import DomainException


@dataclass
class Plan:
    """Plan entity representing a structured collection of tasks.
    
    Plans organize tasks for execution, typically on a daily basis,
    ensuring feasibility within available time and resources.
    """
    
    plan_id: str = field(default_factory=lambda: generate_id("plan_"))
    date: date = field(default_factory=current_date)
    tasks: List[Task] = field(default_factory=list)
    total_hours: float = 8.0
    created_by: str = "system"
    created_at: datetime = field(default_factory=current_timestamp)
    status: str = "draft"  # draft, active, completed, archived
    
    def __post_init__(self):
        """Validate plan after initialization."""
        if self.total_hours <= 0:
            raise DomainException("Total hours must be positive")
        if self.total_hours > 24:
            raise DomainException("Total hours cannot exceed 24")
    
    def add_task(self, task: Task) -> None:
        """Add a task to the plan.
        
        Args:
            task: Task to add
            
        Raises:
            DomainException: If task would exceed available hours
        """
        # Check if adding task would exceed total hours
        planned_hours = self.get_planned_hours()
        required_hours = task.cognitive_load.estimated_hours
        
        if planned_hours + required_hours > self.total_hours:
            raise DomainException(
                f"Cannot add task: would exceed total hours "
                f"({planned_hours + required_hours} > {self.total_hours})"
            )
        
        # Check if task already exists
        if any(t.task_id == task.task_id for t in self.tasks):
            raise DomainException(f"Task {task.task_id} already in plan")
        
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the plan.
        
        Args:
            task_id: ID of task to remove
            
        Raises:
            DomainException: If task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            raise DomainException(f"Task {task_id} not found in plan")
        
        self.tasks.remove(task)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID.
        
        Args:
            task_id: Task ID to find
            
        Returns:
            Task if found, None otherwise
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high priority tasks in the plan.
        
        Returns:
            List of high or critical priority tasks
        """
        return [task for task in self.tasks if task.is_high_priority()]
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks in the plan.
        
        Returns:
            List of pending tasks
        """
        return [task for task in self.tasks if task.is_pending()]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks in the plan.
        
        Returns:
            List of completed tasks
        """
        return [task for task in self.tasks if task.is_completed()]
    
    def get_in_progress_tasks(self) -> List[Task]:
        """Get all in-progress tasks in the plan.
        
        Returns:
            List of in-progress tasks
        """
        return [task for task in self.tasks if task.is_in_progress()]
    
    def get_planned_hours(self) -> float:
        """Calculate total planned hours for all tasks.
        
        Returns:
            Total planned hours
        """
        return sum(task.cognitive_load.estimated_hours for task in self.tasks)
    
    def get_remaining_hours(self) -> float:
        """Calculate remaining available hours.
        
        Returns:
            Hours remaining after planned tasks
        """
        return self.total_hours - self.get_planned_hours()
    
    def is_feasible(self) -> bool:
        """Check if plan is feasible within available hours.
        
        Returns:
            True if total task hours <= total available hours
        """
        return self.get_planned_hours() <= self.total_hours
    
    def get_completion_percentage(self) -> float:
        """Calculate plan completion percentage.
        
        Returns:
            Completion percentage (0.0 to 100.0)
        """
        if not self.tasks:
            return 0.0
        
        completed = len(self.get_completed_tasks())
        return (completed / len(self.tasks)) * 100.0
    
    def is_completed(self) -> bool:
        """Check if all tasks in plan are completed.
        
        Returns:
            True if all tasks are completed
        """
        return len(self.tasks) > 0 and all(task.is_completed() for task in self.tasks)
    
    def sort_tasks_by_priority(self) -> None:
        """Sort tasks by priority (highest first)."""
        self.tasks.sort(key=lambda t: t.priority.weight, reverse=True)
    
    def sort_tasks_by_score(self) -> None:
        """Sort tasks by calculated score (highest first)."""
        self.tasks.sort(key=lambda t: t.get_score(), reverse=True)
    
    def activate(self) -> None:
        """Mark plan as active."""
        self.status = "active"
    
    def complete(self) -> None:
        """Mark plan as completed."""
        self.status = "completed"
    
    def archive(self) -> None:
        """Archive the plan."""
        self.status = "archived"
    
    def __str__(self) -> str:
        """String representation of the plan."""
        return f"Plan for {self.date} ({len(self.tasks)} tasks, {self.get_planned_hours():.1f}h)"
    
    def __repr__(self) -> str:
        """Detailed representation of the plan."""
        return (
            f"Plan(id={self.plan_id}, date={self.date}, "
            f"tasks={len(self.tasks)}, status={self.status})"
        )
