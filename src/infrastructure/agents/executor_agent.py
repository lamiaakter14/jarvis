"""Executor agent implementation."""

from typing import Any, Dict, Optional
import time

from src.domain.entities.agent import Agent
from src.domain.entities.task import Task
from src.domain.value_objects.agent_type import AgentType
from src.domain.repositories.i_task_repository import ITaskRepository
from src.domain.repositories.i_memory_repository import IMemoryRepository
from src.domain.entities.memory import Memory
from src.shared.constants import TaskStatus, MemoryType
from src.shared.exceptions import DomainException


class ExecutorAgent(Agent):
    """Executor agent for task execution and status management.
    
    The executor manages task execution, updates task status,
    and logs execution results for future analysis.
    """
    
    def __init__(
        self,
        task_repo: ITaskRepository,
        memory_repo: IMemoryRepository,
    ):
        """Initialize executor agent.
        
        Args:
            task_repo: Task repository for task management
            memory_repo: Memory repository for logging
        """
        super().__init__(
            agent_type=AgentType.executor(),
            name="Executor Agent",
            description="Executes tasks and manages implementation",
        )
        self.task_repo = task_repo
        self.memory_repo = memory_repo
    
    async def execute(self, context: Any) -> Dict[str, Any]:
        """Execute tasks based on context.
        
        Args:
            context: Execution context (task or task_id)
            
        Returns:
            Dictionary with execution results
            
        Raises:
            DomainException: If execution fails
        """
        start_time = time.time()
        
        try:
            # Determine what to execute
            if isinstance(context, Task):
                result = await self.execute_task(context)
            elif isinstance(context, str):
                # Assume it's a task_id
                task = await self.task_repo.get(context)
                if not task:
                    raise DomainException(f"Task '{context}' not found")
                result = await self.execute_task(task)
            elif isinstance(context, dict) and "task_id" in context:
                task = await self.task_repo.get(context["task_id"])
                if not task:
                    raise DomainException(f"Task '{context['task_id']}' not found")
                result = await self.execute_task(task)
            else:
                raise DomainException("Invalid context for executor")
            
            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)
            
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Executor execution failed: {e}")
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a specific task.
        
        Args:
            task: Task to execute
            
        Returns:
            Dictionary with execution result
        """
        # Mark task as in progress
        task.mark_in_progress()
        await self.task_repo.save(task)
        
        # Simulate task execution (in real implementation, this would do actual work)
        # For now, we'll mark it as completed and log the execution
        result = {
            "status": "completed",
            "message": f"Task '{task.title}' executed successfully",
            "duration": task.cognitive_load.estimated_hours,
        }
        
        # Mark task as completed
        task.mark_completed(result)
        await self.task_repo.save(task)
        
        # Log execution
        await self._log_execution(task, result)
        
        return result
    
    async def execute_task_with_error_handling(
        self,
        task: Task,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Execute a task with error handling and retries.
        
        Args:
            task: Task to execute
            max_retries: Maximum number of retry attempts
            
        Returns:
            Dictionary with execution result
        """
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            try:
                return await self.execute_task(task)
            except Exception as e:
                attempt += 1
                last_error = e
                
                if attempt < max_retries:
                    # Wait before retry (exponential backoff)
                    await self._wait(2 ** attempt)
                else:
                    # Max retries reached, mark as failed
                    task.mark_failed(str(e))
                    await self.task_repo.save(task)
                    
                    error_result = {
                        "status": "failed",
                        "error": str(e),
                        "attempts": attempt,
                    }
                    
                    await self._log_execution(task, error_result)
                    
                    return error_result
        
        # This should not be reached, but just in case
        return {
            "status": "failed",
            "error": str(last_error),
            "attempts": attempt,
        }
    
    async def _log_execution(self, task: Task, result: Dict[str, Any]) -> None:
        """Log task execution to memory.
        
        Args:
            task: Executed task
            result: Execution result
        """
        try:
            from datetime import datetime
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "task_id": task.task_id,
                "task_title": task.title,
                "status": result.get("status"),
                "duration": task.calculate_duration(),
                "result": result,
            }
            
            # Try to get existing logs
            logs_memory = await self.memory_repo.get("execution_logs")
            
            if logs_memory:
                # Append to existing logs
                logs = logs_memory.content.get("items", [])
                logs.append(log_entry)
                logs_memory.update_content({"items": logs})
                await self.memory_repo.save(logs_memory)
            else:
                # Create new logs memory
                logs_memory = Memory(
                    type=MemoryType.EXECUTION_LOG,
                    key="execution_logs",
                    content={"items": [log_entry]},
                )
                await self.memory_repo.save(logs_memory)
        
        except Exception as e:
            # Log error but don't fail the execution
            print(f"Warning: Failed to log execution: {e}")
    
    async def get_pending_tasks(self) -> list:
        """Get all pending tasks.
        
        Returns:
            List of pending tasks
        """
        return await self.task_repo.get_by_status(TaskStatus.PENDING)
    
    async def get_in_progress_tasks(self) -> list:
        """Get all in-progress tasks.
        
        Returns:
            List of in-progress tasks
        """
        return await self.task_repo.get_by_status(TaskStatus.IN_PROGRESS)
    
    async def cancel_task(self, task_id: str, reason: Optional[str] = None) -> None:
        """Cancel a task.
        
        Args:
            task_id: ID of task to cancel
            reason: Optional cancellation reason
        """
        task = await self.task_repo.get(task_id)
        if not task:
            raise DomainException(f"Task '{task_id}' not found")
        
        task.status = TaskStatus.CANCELLED
        if reason:
            task.result = {"cancelled_reason": reason}
        
        await self.task_repo.save(task)
    
    @staticmethod
    async def _wait(seconds: float) -> None:
        """Async wait helper.
        
        Args:
            seconds: Seconds to wait
        """
        import asyncio
        await asyncio.sleep(seconds)
