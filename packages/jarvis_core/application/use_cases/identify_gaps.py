"""Identify Gaps use case."""


from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.application.interfaces.i_notification_service import INotificationService
from jarvis_core.domain.events import GapIdentifiedEvent
from jarvis_core.domain.repositories import IMemoryRepository
from jarvis_core.shared.exceptions import DomainException


class IdentifyGaps:
    """Use case for identifying knowledge and skill gaps.

    Analyzes execution logs and performance data to detect patterns
    indicating knowledge gaps, skill deficiencies, and learning opportunities.
    """

    def __init__(
        self,
        memory_repository: IMemoryRepository,
        ai_service: IAIService,
        notification_service: INotificationService,
    ):
        """Initialize use case with dependencies.

        Args:
            memory_repository: Repository for memory/context data
            ai_service: AI service for gap analysis
            notification_service: Service for sending notifications
        """
        self.memory_repository = memory_repository
        self.ai_service = ai_service
        self.notification_service = notification_service

    async def execute(self) -> list[dict]:
        """Identify gaps from execution logs.

        Returns:
            List of identified gaps with type, description, severity, and evidence

        Raises:
            DomainException: If gap identification fails
        """
        try:
            # Load execution logs
            execution_logs = await self._load_execution_logs()

            if not execution_logs:
                return []

            # Use AI to analyze gaps
            identified_gaps = await self.ai_service.analyze_gaps(execution_logs)

            # Enrich gaps with additional context
            enriched_gaps = await self._enrich_gaps(identified_gaps)

            # Store gaps in memory
            await self._store_gaps(enriched_gaps)

            # Emit events and notifications for high-severity gaps
            await self._notify_gaps(enriched_gaps)

            return enriched_gaps

        except Exception as e:
            raise DomainException(f"Failed to identify gaps: {str(e)}")

    async def _load_execution_logs(self, limit: int = 100) -> list[dict]:
        """Load recent execution logs.

        Args:
            limit: Maximum number of logs to load

        Returns:
            List of execution log entries
        """
        from jarvis_core.shared.constants import MemoryType

        logs_memories = await self.memory_repository.list(MemoryType.EXECUTION_LOG)

        if not logs_memories:
            return []

        # Extract content from memories and flatten
        all_logs = []
        for memory in logs_memories[:limit]:
            if isinstance(memory.content, dict):
                log_entry = memory.content.get("log", {})
                if log_entry:
                    all_logs.append(log_entry)

        return all_logs

    async def _enrich_gaps(self, gaps: list[dict]) -> list[dict]:
        """Enrich gaps with additional context.

        Args:
            gaps: Raw gaps from AI analysis

        Returns:
            Enriched gaps with additional metadata
        """
        enriched = []

        for gap in gaps:
            # Add timestamp
            from jarvis_core.shared.utils import current_timestamp

            gap["identified_at"] = current_timestamp().isoformat()

            # Add gap ID
            from jarvis_core.shared.utils import generate_id

            gap["gap_id"] = generate_id("gap_")

            # Ensure required fields
            gap.setdefault("type", "unknown")
            gap.setdefault("description", "")
            gap.setdefault("severity", "medium")
            gap.setdefault("evidence", [])

            # Add learning priority based on severity and evidence count
            severity_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            severity_score = severity_scores.get(gap.get("severity", "medium"), 2)
            evidence_count = len(gap.get("evidence", []))

            gap["learning_priority"] = min((severity_score + evidence_count / 5.0) / 5.0, 1.0)

            enriched.append(gap)

        return enriched

    async def _store_gaps(self, gaps: list[dict]) -> None:
        """Store identified gaps in memory.

        Args:
            gaps: Gaps to store
        """
        from jarvis_core.domain.entities.memory import Memory
        from jarvis_core.shared.constants import MemoryType

        # Get existing gaps
        existing_memory = await self.memory_repository.get("identified_gaps")

        if existing_memory and isinstance(existing_memory.content, dict):
            existing_gaps = existing_memory.content.get("gaps", [])
        else:
            existing_gaps = []

        if not isinstance(existing_gaps, list):
            existing_gaps = []

        # Merge with new gaps (avoid duplicates)
        existing_descriptions = {g.get("description") for g in existing_gaps}

        for gap in gaps:
            if gap.get("description") not in existing_descriptions:
                existing_gaps.append(gap)

        # Store updated gaps
        gaps_memory = Memory(
            type=MemoryType.KNOWLEDGE, key="identified_gaps", content={"gaps": existing_gaps}
        )
        await self.memory_repository.save(gaps_memory)

    async def _notify_gaps(self, gaps: list[dict]) -> None:
        """Send notifications for important gaps.

        Args:
            gaps: Gaps to potentially notify about
        """
        for gap in gaps:
            severity = gap.get("severity", "medium")

            # Notify for high and critical severity gaps
            if severity in ["high", "critical"]:
                try:
                    await self.notification_service.notify_gap_identified(gap)

                    # Emit domain event
                    GapIdentifiedEvent(
                        description=gap.get("description", ""),
                        category=gap.get("type", "unknown"),
                        severity=severity,
                        evidence=gap.get("evidence", []),
                    )

                    # In a real implementation, this would publish to an event bus

                except Exception as e:
                    # Log error but don't fail the whole operation
                    await self.notification_service.send_notification(
                        f"Failed to notify gap: {str(e)}", "warning"
                    )
