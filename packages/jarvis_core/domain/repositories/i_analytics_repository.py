"""Analytics repository interface for the domain layer."""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any


class IAnalyticsRepository(ABC):
    """Abstract interface for analytics and metrics persistence operations.

    This interface defines the contract for storing and retrieving analytics
    data in the JARVIS system. Implementations handle metrics tracking,
    performance data, and insights about gaps and innovations.
    """

    @abstractmethod
    async def save_execution_metrics(self, metrics: dict[str, Any]) -> None:
        """Save execution metrics for analysis.

        Args:
            metrics: Dictionary containing execution metrics
                     Expected keys: agent_id, task_id, execution_time,
                     success, timestamp, etc.

        Raises:
            RepositoryError: If save operation fails
            ValidationError: If metrics data is invalid
        """

    @abstractmethod
    async def get_performance_data(self, start_date: date, end_date: date) -> dict[str, Any]:
        """Retrieve performance data for a date range.

        Args:
            start_date: Start date for the performance data range
            end_date: End date for the performance data range

        Returns:
            Dictionary containing aggregated performance metrics
            Expected keys: total_tasks, completed_tasks, success_rate,
            average_execution_time, agent_performance, etc.

        Raises:
            RepositoryError: If retrieval operation fails
        """

    @abstractmethod
    async def get_gaps_summary(self) -> list[dict[str, Any]]:
        """Retrieve summary of identified knowledge and capability gaps.

        Returns:
            List of dictionaries, each representing a gap
            Expected keys: gap_id, category, description, severity,
            identified_date, etc.

        Raises:
            RepositoryError: If retrieval operation fails
        """

    @abstractmethod
    async def get_innovations_summary(self) -> list[dict[str, Any]]:
        """Retrieve summary of identified innovations and improvements.

        Returns:
            List of dictionaries, each representing an innovation
            Expected keys: innovation_id, title, description, impact,
            implementation_date, etc.

        Raises:
            RepositoryError: If retrieval operation fails
        """
