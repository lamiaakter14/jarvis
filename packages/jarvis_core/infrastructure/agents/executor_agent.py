"""Executor agent implementation."""

import time
from typing import Any, Dict, Optional

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.repositories.i_task_repository import ITaskRepository
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.shared.constants import MemoryType, TaskStatus
from jarvis_core.shared.exceptions import DomainException


class MissedTaskCounter:
    """Counter for tracking missed tasks and escalations.

    Maintains runtime state of missed tasks and their repetition counts
    to support priority escalation and drift detection.
    """

    def __init__(self):
        """Initialize missed task counter."""
        self._missed_tasks: Dict[str, int] = {}  # task_id -> miss count
        self._escalated_tasks: set = set()  # task_ids that have been escalated

    def record_miss(self, task_id: str) -> int:
        """Record a missed task.

        Args:
            task_id: ID of the missed task

        Returns:
            Number of times this task has been missed
        """
        if task_id not in self._missed_tasks:
            self._missed_tasks[task_id] = 0
        self._missed_tasks[task_id] += 1
        return self._missed_tasks[task_id]

    def get_miss_count(self, task_id: str) -> int:
        """Get the miss count for a task.

        Args:
            task_id: ID of the task

        Returns:
            Number of times the task was missed
        """
        return self._missed_tasks.get(task_id, 0)

    def is_escalated(self, task_id: str) -> bool:
        """Check if a task has been escalated.

        Args:
            task_id: ID of the task

        Returns:
            True if task has been escalated
        """
        return task_id in self._escalated_tasks

    def mark_escalated(self, task_id: str) -> None:
        """Mark a task as escalated.

        Args:
            task_id: ID of the task
        """
        self._escalated_tasks.add(task_id)

    def clear_task(self, task_id: str) -> None:
        """Clear tracking for a completed task.

        Args:
            task_id: ID of the task
        """
        self._missed_tasks.pop(task_id, None)
        self._escalated_tasks.discard(task_id)

    def get_repeatedly_missed_tasks(self, threshold: int = 2) -> list:
        """Get tasks that have been missed multiple times.

        Args:
            threshold: Minimum number of misses to include

        Returns:
            List of (task_id, miss_count) tuples
        """
        return [
            (task_id, count) for task_id, count in self._missed_tasks.items() if count >= threshold
        ]


class ExecutorAgent(Agent):
    """Executor agent for task execution and status management.

    The executor manages task execution, updates task status,
    and logs execution results for future analysis.
    """

    def __init__(
        self,
        task_repo: ITaskRepository,
        memory_repo: Optional[IMemoryRepository] = None,
    ):
        """Initialize executor agent.

        Args:
            task_repo: Task repository for task management
            memory_repo: Optional memory repository for logging
        """
        super().__init__(
            agent_type=AgentType.EXECUTOR,
            name="Executor Agent",
            description="Executes tasks and manages implementation",
        )
        self.task_repo = task_repo
        self.memory_repo = memory_repo
        self.missed_task_counter = MissedTaskCounter()
        self.escalation_threshold = 3  # Tasks missed 3+ times get escalated

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
        self, task: Task, max_retries: int = 3
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
                    await self._wait(2**attempt)
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
        # Memory repo is optional - skip logging if not available
        if not self.memory_repo:
            return

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

    async def check_and_flag_missed_tasks(self) -> Dict[str, Any]:
        """Check for missed tasks and flag them.

        Returns:
            Dictionary with flagged tasks and drift indicators
        """
        try:
            # Get all pending tasks
            all_tasks = await self.task_repo.list_all()

            from datetime import date

            today = date.today()

            overdue_tasks = [
                t
                for t in all_tasks
                if t.status == "pending"
                and hasattr(t, "due_date")
                and t.due_date
                and t.due_date < today
            ]

            flagged_tasks = []
            escalated_tasks = []
            drift_detected = False

            for task in overdue_tasks:
                miss_count = self.missed_task_counter.record_miss(task.task_id)

                task_info = {
                    "task_id": task.task_id,
                    "title": task.title,
                    "miss_count": miss_count,
                    "days_overdue": (today - task.due_date).days,
                }

                # Escalate if threshold reached
                if miss_count >= self.escalation_threshold:
                    if not self.missed_task_counter.is_escalated(task.task_id):
                        # Escalate priority
                        await self._escalate_task_priority(task)
                        self.missed_task_counter.mark_escalated(task.task_id)
                        escalated_tasks.append(task_info)
                        drift_detected = True

                flagged_tasks.append(task_info)

            return {
                "flagged_tasks": flagged_tasks,
                "escalated_tasks": escalated_tasks,
                "total_overdue": len(overdue_tasks),
                "drift_detected": drift_detected,
                "drift_severity": self._calculate_drift_severity(flagged_tasks),
            }

        except Exception as e:
            raise DomainException(f"Failed to check missed tasks: {e}")

    async def _escalate_task_priority(self, task: Task) -> None:
        """Escalate the priority of a repeatedly missed task."""
        from jarvis_core.shared.constants import TaskPriority

        # Escalate priority if not already at highest
        if task.priority != TaskPriority.CRITICAL:
            if task.priority == TaskPriority.HIGH:
                task.priority = TaskPriority.CRITICAL
            elif task.priority == TaskPriority.MEDIUM:
                task.priority = TaskPriority.HIGH
            elif task.priority == TaskPriority.LOW:
                task.priority = TaskPriority.MEDIUM

            await self.task_repo.save(task)

    def _calculate_drift_severity(self, flagged_tasks: list) -> str:
        """Calculate the severity of task drift."""
        if not flagged_tasks:
            return "none"

        total_missed = len(flagged_tasks)
        repeated_misses = sum(1 for t in flagged_tasks if t.get("miss_count", 0) > 1)

        if total_missed >= 10 or repeated_misses >= 5:
            return "critical"
        elif total_missed >= 5 or repeated_misses >= 3:
            return "high"
        elif total_missed >= 3 or repeated_misses >= 2:
            return "medium"
        elif total_missed >= 1:
            return "low"
        else:
            return "none"

    def get_drift_notification(self) -> Optional[Dict[str, Any]]:
        """Get drift notification for the orchestrator."""
        repeatedly_missed = self.missed_task_counter.get_repeatedly_missed_tasks(threshold=2)

        if not repeatedly_missed:
            return None

        return {
            "drift_type": "task_execution",
            "severity": "high" if len(repeatedly_missed) >= 3 else "medium",
            "repeatedly_missed_tasks": [
                {"task_id": task_id, "miss_count": count} for task_id, count in repeatedly_missed
            ],
            "recommendation": (
                "Multiple tasks are repeatedly missed. "
                "Consider reviewing task priorities and time allocation."
            ),
        }
