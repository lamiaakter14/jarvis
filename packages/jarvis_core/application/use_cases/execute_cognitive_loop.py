"""Execute Cognitive Loop use case."""

import logging
from typing import Any

from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.application.interfaces.i_notification_service import INotificationService
from jarvis_core.application.use_cases.analyze_performance import AnalyzePerformance
from jarvis_core.application.use_cases.create_innovations import CreateInnovations
from jarvis_core.application.use_cases.execute_tasks import ExecuteTasks
from jarvis_core.application.use_cases.generate_daily_plan import GenerateDailyPlan
from jarvis_core.application.use_cases.identify_gaps import IdentifyGaps
from jarvis_core.domain.repositories import IAnalyticsRepository, IMemoryRepository, ITaskRepository
from jarvis_core.domain.services.innovation_engine import InnovationEngine
from jarvis_core.domain.services.strategy_engine import StrategyEngine
from jarvis_core.shared.exceptions import DomainException
from jarvis_core.shared.utils import current_date, current_timestamp


class ExecuteCognitiveLoop:
    """Use case for executing the complete cognitive loop.

    Orchestrates the five-agent cognitive loop:
    1. Strategist - Planning and task organization
    2. Mentor - Diagnostics and gap identification
    3. Executor - Task execution
    4. Innovator - Creative synthesis and innovation
    5. Amplifier - Performance analysis and optimization

    This is the main orchestration use case that ties together
    all cognitive functions of the JARVIS system.
    """

    def __init__(
        self,
        task_repository: ITaskRepository,
        memory_repository: IMemoryRepository,
        analytics_repository: IAnalyticsRepository,
        ai_service: IAIService,
        notification_service: INotificationService,
        strategy_engine: StrategyEngine,
        innovation_engine: InnovationEngine,
    ):
        """Initialize use case with dependencies.

        Args:
            task_repository: Repository for task persistence
            memory_repository: Repository for memory/context data
            analytics_repository: Repository for analytics storage
            ai_service: AI service for intelligent operations
            notification_service: Service for sending notifications
            strategy_engine: Domain service for strategic planning
            innovation_engine: Domain service for innovation analysis
        """
        self.task_repository = task_repository
        self.memory_repository = memory_repository
        self.analytics_repository = analytics_repository
        self.ai_service = ai_service
        self.notification_service = notification_service
        self.strategy_engine = strategy_engine
        self.innovation_engine = innovation_engine

        # Initialize sub-use cases
        self.plan_use_case = GenerateDailyPlan(
            task_repository=task_repository,
            memory_repository=memory_repository,
            ai_service=ai_service,
            strategy_engine=strategy_engine,
        )

        self.execute_use_case = ExecuteTasks(
            task_repository=task_repository, notification_service=notification_service
        )

        self.gaps_use_case = IdentifyGaps(
            memory_repository=memory_repository,
            ai_service=ai_service,
            notification_service=notification_service,
        )

        self.innovations_use_case = CreateInnovations(
            memory_repository=memory_repository,
            task_repository=task_repository,
            innovation_engine=innovation_engine,
            ai_service=ai_service,
            notification_service=notification_service,
        )

        self.performance_use_case = AnalyzePerformance(
            task_repository=task_repository,
            analytics_repository=analytics_repository,
            memory_repository=memory_repository,
        )

    async def execute(self) -> dict[str, Any]:
        """Execute the complete cognitive loop.

        Returns:
            Dictionary containing summary of cognitive loop execution:
                - timestamp: Execution timestamp
                - strategist: Planning results
                - mentor: Diagnostics results
                - executor: Execution results
                - innovator: Innovation results
                - amplifier: Performance analysis results
                - overall_status: Success/failure status
                - errors: List of any errors encountered

        Raises:
            DomainException: If critical loop execution fails
        """
        start_time = current_timestamp()
        today = current_date()

        summary = {
            "timestamp": start_time.isoformat(),
            "date": today.isoformat(),
            "strategist": {},
            "mentor": {},
            "executor": {},
            "innovator": {},
            "amplifier": {},
            "overall_status": "success",
            "errors": [],
            "duration_seconds": 0.0,
        }

        try:
            # Phase 1: STRATEGIST - Planning
            await self.notification_service.send_notification(
                "Starting cognitive loop: Strategist phase", "info"
            )

            strategist_result = await self._run_strategist(today)
            summary["strategist"] = strategist_result

            # Phase 2: MENTOR - Diagnostics
            await self.notification_service.send_notification(
                "Cognitive loop: Mentor phase", "info"
            )

            mentor_result = await self._run_mentor()
            summary["mentor"] = mentor_result

            # Phase 3: EXECUTOR - Task Execution
            await self.notification_service.send_notification(
                "Cognitive loop: Executor phase", "info"
            )

            executor_result = await self._run_executor()
            summary["executor"] = executor_result

            # Phase 4: INNOVATOR - Creative Synthesis
            await self.notification_service.send_notification(
                "Cognitive loop: Innovator phase", "info"
            )

            innovator_result = await self._run_innovator()
            summary["innovator"] = innovator_result

            # Phase 5: AMPLIFIER - Performance Analysis
            await self.notification_service.send_notification(
                "Cognitive loop: Amplifier phase", "info"
            )

            amplifier_result = await self._run_amplifier(today)
            summary["amplifier"] = amplifier_result

            # Calculate total duration
            end_time = current_timestamp()
            summary["duration_seconds"] = (end_time - start_time).total_seconds()

            # Store loop execution summary
            await self._store_loop_summary(summary)

            # Send completion notification
            await self.notification_service.send_notification(
                f"Cognitive loop completed successfully in {summary['duration_seconds']:.1f}s",
                "success",
            )

            return summary

        except Exception as e:
            summary["overall_status"] = "failed"
            summary["errors"].append(str(e))

            await self.notification_service.send_notification(
                f"Cognitive loop failed: {str(e)}", "error"
            )

            raise DomainException(f"Cognitive loop execution failed: {str(e)}")

    async def _run_strategist(self, today) -> dict[str, Any]:
        """Run the Strategist agent (planning).

        Args:
            today: Current date

        Returns:
            Dictionary with planning results
        """
        try:
            # Generate daily plan
            plan_dto = await self.plan_use_case.execute(target_date=today, available_hours=8.0)

            return {
                "status": "success",
                "plan_id": plan_dto.plan_id,
                "total_tasks": len(plan_dto.tasks),
                "planned_hours": plan_dto.get_planned_hours(),
                "remaining_hours": plan_dto.get_remaining_hours(),
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _run_mentor(self) -> dict[str, Any]:
        """Run the Mentor agent (diagnostics).

        Returns:
            Dictionary with diagnostics results
        """
        try:
            # Identify gaps
            gaps = await self.gaps_use_case.execute()

            # Categorize gaps by severity
            critical_gaps = [g for g in gaps if g.get("severity") == "critical"]
            high_gaps = [g for g in gaps if g.get("severity") == "high"]

            return {
                "status": "success",
                "total_gaps": len(gaps),
                "critical_gaps": len(critical_gaps),
                "high_gaps": len(high_gaps),
                "gaps": gaps[:5],  # Top 5 gaps
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _run_executor(self) -> dict[str, Any]:
        """Run the Executor agent (task execution).

        Returns:
            Dictionary with execution results
        """
        try:
            # Get pending high-priority tasks
            pending_tasks = await self.task_repository.get_by_status("pending")
            high_priority = [t for t in pending_tasks if t.is_high_priority()]

            # Execute up to 3 high-priority tasks
            task_ids = [t.task_id for t in high_priority[:3]]

            if not task_ids:
                return {
                    "status": "success",
                    "message": "No high-priority tasks to execute",
                    "executed_tasks": 0,
                }

            executed = await self.execute_use_case.execute(task_ids)

            completed = len([t for t in executed if t.status == "completed"])
            failed = len([t for t in executed if t.status == "failed"])

            return {
                "status": "success",
                "executed_tasks": len(executed),
                "completed": completed,
                "failed": failed,
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _run_innovator(self) -> dict[str, Any]:
        """Run the Innovator agent (creative synthesis).

        Returns:
            Dictionary with innovation results
        """
        try:
            # Generate innovations
            innovations = await self.innovations_use_case.execute()

            # Categorize by impact
            high_impact = [i for i in innovations if i.is_high_impact()]

            return {
                "status": "success",
                "total_innovations": len(innovations),
                "high_impact_innovations": len(high_impact),
                "innovations": [
                    {"title": i.title, "category": i.category, "impact_score": i.impact_score}
                    for i in innovations[:5]  # Top 5
                ],
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _run_amplifier(self, today) -> dict[str, Any]:
        """Run the Amplifier agent (performance analysis).

        Args:
            today: Current date

        Returns:
            Dictionary with performance analysis results
        """
        try:
            # Analyze last 7 days
            from datetime import timedelta

            start_date = today - timedelta(days=6)

            analytics = await self.performance_use_case.execute(
                start_date=start_date, end_date=today
            )

            return {
                "status": "success",
                "productivity_score": analytics.productivity_score,
                "success_rate": analytics.success_rate,
                "completion_rate": analytics.get_completion_rate(),
                "average_roi": analytics.average_roi,
                "utilization_rate": analytics.utilization_rate,
                "is_high_performance": analytics.is_high_performance(),
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def _store_loop_summary(self, summary: dict[str, Any]) -> None:
        """Store cognitive loop execution summary.

        Args:
            summary: Loop execution summary
        """
        from jarvis_core.domain.entities.memory import Memory
        from jarvis_core.shared.constants import MemoryType

        try:
            loop_memory = Memory(
                type=MemoryType.EXECUTION_LOG,
                key=f"loop_{summary['date']}",
                content={"log": summary},
            )
            await self.memory_repository.save(loop_memory)
        except Exception:
            logging.getLogger(__name__).exception(
                "Failed to save cognitive loop summary memory (key=%s)",
                f"loop_{summary['date']}",
            )
