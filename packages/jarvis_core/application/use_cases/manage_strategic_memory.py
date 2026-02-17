"""Use case for managing strategic memory and long-term goals."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from jarvis_core.domain.entities.memory import Memory
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.schemas.memory_content import ADRContent, StrategicMemoryContent
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import UseCaseError
from jarvis_core.shared.utils import current_timestamp, generate_id


class ManageStrategicMemory:
    """Use case for managing strategic memory operations.

    Handles creation, retrieval, and management of strategic goals,
    long-term plans, and architecture decision records (ADRs).
    """

    def __init__(self, memory_repository: IMemoryRepository):
        """Initialize the use case.

        Args:
            memory_repository: Repository for memory persistence
        """
        self.memory_repository = memory_repository

    async def create_strategic_goal(
        self,
        goal: str,
        description: str = "",
        priority: str = "medium",
        target_date: Optional[datetime] = None,
        milestones: Optional[List[Dict[str, Any]]] = None,
        dependencies: Optional[List[str]] = None,
        metrics: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """Create a new strategic goal.

        Args:
            goal: Strategic goal description
            description: Detailed description
            priority: Goal priority (low, medium, high, critical)
            target_date: Target completion date
            milestones: List of milestones
            dependencies: Dependencies on other goals
            metrics: Success metrics

        Returns:
            Created Memory instance

        Raises:
            UseCaseError: If goal creation fails
        """
        try:
            # Validate content using schema
            content_data = {
                "goal": goal,
                "description": description,
                "priority": priority,
                "status": "active",
                "progress": 0.0,
                "milestones": milestones or [],
                "dependencies": dependencies or [],
                "metrics": metrics or {},
            }

            if target_date:
                content_data["target_date"] = target_date

            # Validate using Pydantic schema
            validated_content = StrategicMemoryContent(**content_data)

            # Create memory
            key = f"goal_{generate_id('g_')}"
            memory = Memory(
                key=key,
                type=MemoryType.STRATEGIC,
                content=validated_content.model_dump(),
            )

            # Add tags for indexing
            tags = ["strategic", "goal", priority]
            if milestones:
                tags.append("has_milestones")
            memory.add_tags(tags)

            # Save to repository
            await self.memory_repository.save(memory)

            return memory

        except Exception as e:
            raise UseCaseError(f"Failed to create strategic goal: {e}")

    async def update_goal_progress(
        self, goal_key: str, progress: float, status: Optional[str] = None
    ) -> Memory:
        """Update the progress of a strategic goal.

        Args:
            goal_key: Key of the goal to update
            progress: Progress percentage (0-100)
            status: Optional new status

        Returns:
            Updated Memory instance

        Raises:
            UseCaseError: If update fails
        """
        try:
            # Retrieve existing goal
            memory = await self.memory_repository.get(goal_key)
            if not memory:
                raise UseCaseError(f"Goal '{goal_key}' not found")

            # Update progress
            memory.content["progress"] = min(max(progress, 0.0), 100.0)

            if status:
                memory.content["status"] = status

            memory.updated_at = current_timestamp()

            # Increment version
            current_version = memory.get_version()
            memory.set_version(current_version + 1)

            # Save updated memory
            await self.memory_repository.save(memory)

            return memory

        except Exception as e:
            raise UseCaseError(f"Failed to update goal progress: {e}")

    async def list_active_goals(self) -> List[Memory]:
        """List all active strategic goals.

        Returns:
            List of active goal memories

        Raises:
            UseCaseError: If listing fails
        """
        try:
            # Get all strategic memories
            all_strategic = await self.memory_repository.list(MemoryType.STRATEGIC)

            # Filter for goals with active status
            active_goals = [
                m
                for m in all_strategic
                if m.content.get("status") == "active" and "goal" in m.content
            ]

            # Sort by priority (critical > high > medium > low)
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            active_goals.sort(key=lambda m: priority_order.get(m.content.get("priority", "low"), 3))

            return active_goals

        except Exception as e:
            raise UseCaseError(f"Failed to list active goals: {e}")

    async def create_adr(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        status: str = "proposed",
        alternatives: Optional[List[str]] = None,
        related_decisions: Optional[List[str]] = None,
    ) -> Memory:
        """Create an Architecture Decision Record (ADR).

        Args:
            title: ADR title
            context: Context and background
            decision: The decision made
            consequences: Consequences of the decision
            status: ADR status (proposed, accepted, deprecated, superseded)
            alternatives: Alternative options considered
            related_decisions: Related ADR IDs

        Returns:
            Created Memory instance

        Raises:
            UseCaseError: If ADR creation fails
        """
        try:
            # Validate content using schema
            content_data = {
                "title": title,
                "status": status,
                "date": current_timestamp(),
                "context": context,
                "decision": decision,
                "consequences": consequences,
                "alternatives": alternatives or [],
                "related_decisions": related_decisions or [],
            }

            # Validate using Pydantic schema
            validated_content = ADRContent(**content_data)

            # Create memory with unique key
            key = f"adr_{generate_id('adr_')}"
            memory = Memory(
                key=key,
                type=MemoryType.STRATEGIC,
                content=validated_content.model_dump(),
            )

            # Add tags for indexing
            tags = ["adr", "architecture", status]
            memory.add_tags(tags)

            # Save to repository
            await self.memory_repository.save(memory)

            return memory

        except Exception as e:
            raise UseCaseError(f"Failed to create ADR: {e}")

    async def list_adrs(self, status: Optional[str] = None) -> List[Memory]:
        """List all Architecture Decision Records.

        Args:
            status: Filter by status (proposed, accepted, deprecated, superseded)

        Returns:
            List of ADR memories

        Raises:
            UseCaseError: If listing fails
        """
        try:
            # Search for ADRs using tags
            adrs = await self.memory_repository.search(
                memory_type=MemoryType.STRATEGIC, tags=["adr"]
            )

            # Filter by status if provided
            if status:
                adrs = [m for m in adrs if m.content.get("status") == status]

            # Sort by date (newest first)
            adrs.sort(key=lambda m: m.content.get("date", datetime.min), reverse=True)

            return adrs

        except Exception as e:
            raise UseCaseError(f"Failed to list ADRs: {e}")

    async def search_strategic_memory(
        self,
        keywords: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
    ) -> List[Memory]:
        """Search strategic memory by keywords and tags.

        Args:
            keywords: Keywords to search for
            tags: Tags to filter by
            limit: Maximum number of results

        Returns:
            List of matching memories

        Raises:
            UseCaseError: If search fails
        """
        try:
            results = await self.memory_repository.search(
                memory_type=MemoryType.STRATEGIC, keywords=keywords, tags=tags, limit=limit
            )

            return results

        except Exception as e:
            raise UseCaseError(f"Failed to search strategic memory: {e}")
