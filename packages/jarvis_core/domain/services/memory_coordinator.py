"""Memory coordinator domain service."""

from typing import Any, Dict, List

from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException


class MemoryCoordinator:
    """Service for coordinating memory operations across the system.

    The MemoryCoordinator manages working memory, context retrieval,
    and gap tracking. It provides a domain-level interface for memory
    operations without exposing infrastructure details.
    """

    def __init__(self, memory_repository: IMemoryRepository):
        """Initialize the memory coordinator.

        Args:
            memory_repository: Repository for memory persistence
        """
        self.memory_repository = memory_repository

    async def store_working_memory(self, key: str, content: Dict[str, Any]) -> None:
        """Store content in working memory.

        Working memory holds temporary data needed during execution,
        such as intermediate results or agent state.

        Args:
            key: Unique key for the memory
            content: Content to store

        Raises:
            DomainException: If storage fails
        """
        if not key:
            raise DomainException("Memory key cannot be empty")

        if not content:
            raise DomainException("Memory content cannot be empty")

        try:
            memory = Memory(key=key, content=content, memory_type=MemoryType.WORKING)
            await self.memory_repository.save(memory)

        except Exception as e:
            raise DomainException(f"Failed to store working memory: {str(e)}")

    async def retrieve_context(self) -> Context:
        """Retrieve the current execution context from memory.

        Loads context data including focus areas, gaps, strategic goals,
        and available resources.

        Returns:
            Context instance populated from memory

        Raises:
            DomainException: If context retrieval fails
        """
        try:
            # Retrieve context memory
            context_memory = await self.memory_repository.get("current_context")

            if context_memory is None:
                # Return default context if none exists
                return Context()

            # Build context from memory content
            content = context_memory.content
            context = Context(
                context_id=content.get("context_id", ""),
                current_focus=content.get("current_focus", []),
                available_hours=content.get("available_hours", 8.0),
                daily_plan=content.get("daily_plan", {}),
                gaps=content.get("gaps", []),
                reflections=content.get("reflections", []),
                strategic_goals=content.get("strategic_goals", []),
            )

            return context

        except Exception as e:
            raise DomainException(f"Failed to retrieve context: {str(e)}")

    async def save_context(self, context: Context) -> None:
        """Save the current execution context to memory.

        Persists context state for retrieval in future executions.

        Args:
            context: Context to save

        Raises:
            DomainException: If save fails
        """
        try:
            content = {
                "context_id": context.context_id,
                "date": context.date.isoformat(),
                "current_focus": context.current_focus,
                "available_hours": context.available_hours,
                "daily_plan": context.daily_plan,
                "gaps": context.gaps,
                "reflections": context.reflections,
                "strategic_goals": context.strategic_goals,
            }

            memory = Memory(key="current_context", content=content, memory_type=MemoryType.WORKING)

            await self.memory_repository.save(memory)

        except Exception as e:
            raise DomainException(f"Failed to save context: {str(e)}")

    async def update_gaps(self, gaps: List[Dict[str, Any]]) -> None:
        """Update the gap list in memory.

        Persists identified gaps for tracking and resolution.

        Args:
            gaps: List of gap dictionaries to store

        Raises:
            DomainException: If update fails
        """
        if not isinstance(gaps, list):
            raise DomainException("Gaps must be a list")

        try:
            memory = Memory(
                key="identified_gaps", content={"gaps": gaps}, memory_type=MemoryType.LONG_TERM
            )

            await self.memory_repository.save(memory)

        except Exception as e:
            raise DomainException(f"Failed to update gaps: {str(e)}")

    async def retrieve_gaps(self) -> List[Dict[str, Any]]:
        """Retrieve all identified gaps from memory.

        Returns:
            List of gap dictionaries

        Raises:
            DomainException: If retrieval fails
        """
        try:
            gaps_memory = await self.memory_repository.get("identified_gaps")

            if gaps_memory is None:
                return []

            return gaps_memory.content.get("gaps", [])

        except Exception as e:
            raise DomainException(f"Failed to retrieve gaps: {str(e)}")

    async def store_execution_result(self, task_id: str, result: Any) -> None:
        """Store task execution result in memory.

        Preserves execution results for analysis and future reference.

        Args:
            task_id: ID of the completed task
            result: Execution result to store

        Raises:
            DomainException: If storage fails
        """
        if not task_id:
            raise DomainException("Task ID cannot be empty")

        try:
            memory = Memory(
                key=f"result_{task_id}",
                content={"task_id": task_id, "result": result},
                memory_type=MemoryType.WORKING,
            )

            await self.memory_repository.save(memory)

        except Exception as e:
            raise DomainException(f"Failed to store execution result: {str(e)}")

    async def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of current memory state.

        Provides an overview of what's stored in memory without
        loading all content.

        Returns:
            Dictionary containing memory summary statistics
        """
        try:
            working_memories = await self.memory_repository.list(MemoryType.WORKING)
            long_term_memories = await self.memory_repository.list(MemoryType.LONG_TERM)

            return {
                "working_memory_count": len(working_memories),
                "long_term_memory_count": len(long_term_memories),
                "total_memories": len(working_memories) + len(long_term_memories),
                "has_context": any(m.key == "current_context" for m in working_memories),
                "has_gaps": any(m.key == "identified_gaps" for m in long_term_memories),
            }

        except Exception as e:
            raise DomainException(f"Failed to get memory summary: {str(e)}")
