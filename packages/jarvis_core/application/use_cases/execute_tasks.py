"""Execute Tasks use case."""

from typing import List, Dict, Any, Optional

from jarvis_core.application.dto.task_dto import TaskDTO
from jarvis_core.application.interfaces.i_notification_service import INotificationService
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.events import TaskCompletedEvent
from jarvis_core.domain.repositories import ITaskRepository
from jarvis_core.shared.constants import TaskStatus, TaskPriority
from jarvis_core.shared.exceptions import DomainException


class ExecuteTasks:
    """Use case for executing specific tasks.
    
    Orchestrates task execution by coordinating with agents,
    tracking progress, and emitting completion events.
    """
    
    def __init__(
        self,
        task_repository: ITaskRepository,
        notification_service: INotificationService
    ):
        """Initialize use case with dependencies.
        
        Args:
            task_repository: Repository for task persistence
            notification_service: Service for sending notifications
        """
        self.task_repository = task_repository
        self.notification_service = notification_service
    
    async def execute(self, task_ids: List[str]) -> List[TaskDTO]:
        """Execute specified tasks.
        
        Args:
            task_ids: List of task IDs to execute
            
        Returns:
            List of TaskDTO with execution results
            
        Raises:
            DomainException: If task execution fails
        """
        executed_tasks = []
        
        for task_id in task_ids:
            try:
                # Load task
                task = await self.task_repository.get(task_id)
                if not task:
                    raise DomainException(f"Task not found: {task_id}")
                
                # Skip if already completed
                if task.is_completed():
                    executed_tasks.append(TaskDTO.from_entity(task))
                    continue
                
                # Execute task
                result_task = await self._execute_single_task(task)
                
                # Update task
                await self.task_repository.update(result_task)
                
                # Convert to DTO
                executed_tasks.append(TaskDTO.from_entity(result_task))
                
                # Send notification if completed
                if result_task.is_completed():
                    await self.notification_service.notify_task_completed(result_task)
                
            except Exception as e:
                # Log error and continue with next task
                await self.notification_service.send_notification(
                    f"Failed to execute task {task_id}: {str(e)}",
                    "error"
                )
                continue
        
        return executed_tasks
    
    async def _execute_single_task(self, task: Task) -> Task:
        """Execute a single task.
        
        Args:
            task: Task to execute
            
        Returns:
            Updated task with execution results
        """
        # Mark task as in progress
        task.mark_in_progress()
        await self.task_repository.update(task)
        
        try:
            # In a real implementation, this would delegate to agent infrastructure
            # For now, we simulate task execution
            result = await self._simulate_task_execution(task)
            
            # Mark task as completed
            task.mark_completed(result)
            
            # Emit task completed event
            event = TaskCompletedEvent(
                task_id=task.task_id,
                agent_id="system",
                agent_type=str(task.agent_type),
                result=result,
                duration_seconds=task.calculate_duration() or 0.0
            )
            
            # In a real implementation, this would publish to an event bus
            
        except Exception as e:
            # Mark task as failed
            task.mark_failed(str(e))
            raise DomainException(f"Task execution failed: {str(e)}")
        
        return task
    
    async def _simulate_task_execution(self, task: Task) -> Dict[str, Any]:
        """Simulate task execution (placeholder for actual agent execution).
        
        Args:
            task: Task to execute
            
        Returns:
            Simulated execution result
        """
        return {
            "status": "completed",
            "task_id": task.task_id,
            "agent_type": str(task.agent_type),
            "message": f"Task '{task.title}' executed successfully"
        }
    
    async def get_tasks_by_status(self, status: TaskStatus) -> List[TaskDTO]:
        """Retrieve tasks filtered by their current status.
        
        Args:
            status: TaskStatus to filter by (PENDING, IN_PROGRESS, COMPLETED, etc.)
            
        Returns:
            List of TaskDTO matching the specified status
        """
        # Get all tasks from repository
        all_tasks = await self.task_repository.list()
        
        # Filter tasks by status
        filtered_tasks = [task for task in all_tasks if task.status == status]
        
        # Convert to DTOs
        return [TaskDTO.from_entity(task) for task in filtered_tasks]
    
    async def get_tasks_by_priority(
        self, 
        priority: TaskPriority,
        status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """Retrieve tasks filtered by priority and optionally by status.
        
        Args:
            priority: TaskPriority to filter by (LOW, MEDIUM, HIGH, CRITICAL)
            status: Optional TaskStatus to further filter results
            
        Returns:
            List of TaskDTO matching the specified priority and status
        """
        # Get all tasks from repository
        all_tasks = await self.task_repository.list()
        
        # Filter tasks by priority
        filtered_tasks = [
            task for task in all_tasks 
            if task.priority.value == priority.value
        ]
        
        # Further filter by status if provided
        if status is not None:
            filtered_tasks = [
                task for task in filtered_tasks 
                if task.status == status
            ]
        
        # Convert to DTOs
        return [TaskDTO.from_entity(task) for task in filtered_tasks]
