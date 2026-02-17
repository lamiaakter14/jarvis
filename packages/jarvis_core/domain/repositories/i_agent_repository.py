"""Agent repository interface for the domain layer."""

from abc import ABC, abstractmethod
from typing import Optional

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.value_objects.agent_type import AgentType


class IAgentRepository(ABC):
    """Abstract interface for agent persistence operations.

    This interface defines the contract for storing and retrieving agents
    in the JARVIS system. Implementations manage agent instances and their
    state across system sessions.
    """

    @abstractmethod
    async def get(self, agent_id: str) -> Optional[Agent]:
        """Retrieve an agent by its ID.

        Args:
            agent_id: Unique identifier for the agent

        Returns:
            Agent instance if found, None otherwise

        Raises:
            RepositoryError: If retrieval operation fails
        """

    @abstractmethod
    async def list_all(self) -> list[Agent]:
        """Retrieve all agents in the system.

        Returns:
            List of all Agent instances

        Raises:
            RepositoryError: If list operation fails
        """

    @abstractmethod
    async def get_by_type(self, agent_type: AgentType) -> Optional[Agent]:
        """Retrieve an agent by its type.

        Args:
            agent_type: Type of agent to retrieve

        Returns:
            Agent instance of the specified type if found, None otherwise

        Raises:
            RepositoryError: If retrieval operation fails
        """
