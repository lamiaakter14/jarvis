"""Task repository interface for the domain layer."""

import builtins
from abc import ABC, abstractmethod
from typing import Optional

from jarvis_core.domain.entities.task import Task
from jarvis_core.shared.constants import TaskStatus


class ITaskRepository(ABC):
    """Abstract interface for task persistence operations.

    This interface defines the contract for storing and retrieving tasks
    in the JARVIS system. Implementations handle the actual persistence
    mechanism and provide flexible querying capabilities.
    """

    @abstractmethod
    async def get(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: Unique identifier for the task

        Returns:
            Task instance if found, None otherwise

        Raises:
            RepositoryError: If retrieval operation fails
        """

    @abstractmethod
    async def save(self, task: Task) -> None:
        """Persist a task to storage.

        Args:
            task: Task instance to save

        Raises:
            RepositoryError: If save operation fails
            ValidationError: If task data is invalid
        """

    @abstractmethod
    async def list(self, filters: Optional[dict] = None) -> list[Task]:
        """List tasks with optional filtering.

        Args:
            filters: Optional dictionary of filter criteria
                     Examples: {"agent_type": "executor", "priority": "high"}

        Returns:
            List of Task instances matching the filters

        Raises:
            RepositoryError: If list operation fails
        """
    @abstractmethod
    async def delete(self, task_id: str) -> None:
        """Delete a task by its ID.

        Args:
            task_id: Unique identifier for the task to delete

        Raises:
            RepositoryError: If delete operation fails
            EntityNotFoundError: If task with ID does not exist
        """

    @abstractmethod
    async def get_by_status(self, status: TaskStatus) -> builtins.list[Task]:
        """Retrieve all tasks with a specific status.

        Args:
            status: Task status to filter by

        Returns:
            List of Task instances with the specified status

        Raises:
            RepositoryError: If retrieval operation fails
        """
