"""Create Innovations use case."""

from typing import List

from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.application.interfaces.i_notification_service import INotificationService
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.domain.events import InnovationCreatedEvent
from jarvis_core.domain.repositories import IMemoryRepository, ITaskRepository
from jarvis_core.domain.services.innovation_engine import InnovationEngine
from jarvis_core.shared.exceptions import DomainException


class CreateInnovations:
    """Use case for generating and storing innovations.

    Combines AI-powered innovation generation with domain logic to create,
    rank, and store innovative ideas and improvement suggestions.
    """

    def __init__(
        self,
        memory_repository: IMemoryRepository,
        task_repository: ITaskRepository,
        innovation_engine: InnovationEngine,
        ai_service: IAIService,
        notification_service: INotificationService,
    ):
        """Initialize use case with dependencies.

        Args:
            memory_repository: Repository for memory/context data
            task_repository: Repository for task data
            innovation_engine: Domain service for innovation analysis
            ai_service: AI service for innovation generation
            notification_service: Service for sending notifications
        """
        self.memory_repository = memory_repository
        self.task_repository = task_repository
        self.innovation_engine = innovation_engine
        self.ai_service = ai_service
        self.notification_service = notification_service

    async def execute(self) -> List[Innovation]:
        """Generate and store innovations.

        Returns:
            List of created Innovation entities

        Raises:
            DomainException: If innovation creation fails
        """
        try:
            # Load current context
            context = await self._load_context()

            # Generate innovations using AI
            ai_innovations = await self.ai_service.generate_innovations(context)

            # Load recent tasks for pattern analysis
            recent_tasks = await self.task_repository.list()

            # Analyze patterns in tasks to generate additional innovations
            pattern_innovations = self.innovation_engine.analyze_patterns(recent_tasks, context)

            # Load performance data
            performance_data = await self._load_performance_data()

            # Generate improvement suggestions based on performance
            improvement_innovations = self.innovation_engine.suggest_improvements(performance_data)

            # Combine all innovations
            all_innovations = ai_innovations + pattern_innovations + improvement_innovations

            # Remove duplicates based on title similarity
            unique_innovations = self._deduplicate_innovations(all_innovations)

            # Rank innovations
            ranked_innovations = self.innovation_engine.rank_innovations(unique_innovations)

            # Filter to actionable innovations
            actionable_innovations = self.innovation_engine.filter_actionable_innovations(
                ranked_innovations, min_score=0.6
            )

            # Store innovations
            await self._store_innovations(actionable_innovations)

            # Emit events and notifications for high-impact innovations
            await self._notify_innovations(actionable_innovations)

            return actionable_innovations

        except Exception as e:
            raise DomainException(f"Failed to create innovations: {str(e)}")

    async def _load_context(self) -> Context:
        """Load current execution context.

        Returns:
            Context entity with loaded data
        """
        from jarvis_core.shared.utils import current_date

        context = Context(date=current_date())

        # Load strategic goals
        goals_memory = await self.memory_repository.get("strategic_goals")
        if goals_memory and isinstance(goals_memory.content, dict):
            goals = goals_memory.content.get("goals", [])
            if isinstance(goals, list):
                for goal in goals:
                    context.add_strategic_goal(goal)

        # Load gaps
        gaps_memory = await self.memory_repository.get("identified_gaps")
        if gaps_memory and isinstance(gaps_memory.content, dict):
            gaps = gaps_memory.content.get("gaps", [])
            if isinstance(gaps, list):
                context.gaps = gaps

        # Load focus areas
        focus_memory = await self.memory_repository.get("current_focus")
        if focus_memory and isinstance(focus_memory.content, dict):
            focus = focus_memory.content.get("focus_areas", [])
            if isinstance(focus, list):
                for f in focus:
                    context.add_focus_area(f)

        return context

    async def _load_performance_data(self) -> dict:
        """Load recent performance metrics.

        Returns:
            Dictionary with performance data
        """
        metrics_memory = await self.memory_repository.get("recent_metrics")

        if not metrics_memory or not isinstance(metrics_memory.content, dict):
            return {
                "success_rate": 1.0,
                "average_execution_time": 0.0,
                "completed_tasks": 0,
                "total_tasks": 0,
                "utilized_hours": 0.0,
                "available_hours": 8.0,
            }

        return metrics_memory.content.get("metrics", {})

    def _deduplicate_innovations(self, innovations: List[Innovation]) -> List[Innovation]:
        """Remove duplicate innovations based on title similarity.

        Args:
            innovations: List of innovations to deduplicate

        Returns:
            List with duplicates removed
        """
        if not innovations:
            return []

        unique = []
        seen_titles = set()

        for innovation in innovations:
            # Normalize title for comparison
            normalized_title = innovation.title.lower().strip()

            # Skip if we've seen a very similar title
            is_duplicate = False
            for seen_title in seen_titles:
                # Simple similarity check - could be more sophisticated
                if normalized_title in seen_title or seen_title in normalized_title:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique.append(innovation)
                seen_titles.add(normalized_title)

        return unique

    async def _store_innovations(self, innovations: List[Innovation]) -> None:
        """Store innovations in memory.

        Args:
            innovations: Innovations to store
        """
        from jarvis_core.domain.entities.memory import Memory
        from jarvis_core.shared.constants import MemoryType

        # Get existing innovations
        existing_memory = await self.memory_repository.get("recent_innovations")

        if existing_memory and isinstance(existing_memory.content, dict):
            existing = existing_memory.content.get("innovations", [])
        else:
            existing = []

        if not isinstance(existing, list):
            existing = []

        # Convert innovations to dicts and merge
        innovation_dicts = [
            {
                "innovation_id": inn.innovation_id,
                "title": inn.title,
                "description": inn.description,
                "category": inn.category,
                "impact_score": inn.impact_score,
                "status": inn.status,
                "created_at": inn.created_at.isoformat(),
            }
            for inn in innovations
        ]

        # Keep most recent 50 innovations
        all_innovations = innovation_dicts + existing
        all_innovations = all_innovations[:50]

        innovations_memory = Memory(
            type=MemoryType.KNOWLEDGE,
            key="recent_innovations",
            content={"innovations": all_innovations},
        )
        await self.memory_repository.save(innovations_memory)

    async def _notify_innovations(self, innovations: List[Innovation]) -> None:
        """Send notifications for high-impact innovations.

        Args:
            innovations: Innovations to potentially notify about
        """
        for innovation in innovations:
            if innovation.is_high_impact():
                try:
                    await self.notification_service.send_notification(
                        f"New high-impact innovation: {innovation.title}", "info"
                    )

                    # Emit domain event
                    event = InnovationCreatedEvent(
                        innovation_id=innovation.innovation_id,
                        title=innovation.title,
                        category=innovation.category,
                        impact_score=innovation.impact_score,
                    )

                    # In a real implementation, this would publish to an event bus

                except Exception:
                    # Log error but don't fail
                    pass
