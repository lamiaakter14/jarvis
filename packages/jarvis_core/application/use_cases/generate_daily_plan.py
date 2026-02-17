"""Generate Daily Plan use case."""

from datetime import date

from jarvis_core.application.dto.plan_dto import PlanDTO
from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.plan import Plan
from jarvis_core.domain.repositories import IMemoryRepository, ITaskRepository
from jarvis_core.domain.services.strategy_engine import StrategyEngine
from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException


class GenerateDailyPlan:
    """Use case for generating optimized daily plans.

    Orchestrates the planning process by loading context, analyzing gaps,
    consulting strategic goals, and using AI to generate a feasible,
    high-impact daily plan.
    """

    def __init__(
        self,
        task_repository: ITaskRepository,
        memory_repository: IMemoryRepository,
        ai_service: IAIService,
        strategy_engine: StrategyEngine,
    ):
        """Initialize use case with dependencies.

        Args:
            task_repository: Repository for task persistence
            memory_repository: Repository for memory/context data
            ai_service: AI service for intelligent planning
            strategy_engine: Domain service for strategic planning
        """
        self.task_repository = task_repository
        self.memory_repository = memory_repository
        self.ai_service = ai_service
        self.strategy_engine = strategy_engine

    async def execute(self, target_date: date, available_hours: float = 8.0) -> PlanDTO:
        """Generate a daily plan for the specified date.

        Args:
            target_date: Date for which to generate the plan
            available_hours: Hours available for task execution (default: 8.0)

        Returns:
            PlanDTO containing the generated plan

        Raises:
            DomainException: If plan generation fails
        """
        try:
            # Load current context
            context = await self._load_context(target_date, available_hours)

            # Get pending tasks
            pending_tasks = await self.task_repository.list({"status": "pending"})

            if not pending_tasks:
                # Create empty plan if no tasks
                empty_plan = Plan(date=target_date, total_hours=available_hours, status="active")
                return PlanDTO.from_entity(empty_plan)

            # Calculate ROI for tasks based on context
            for task in pending_tasks:
                task.roi = self.strategy_engine.calculate_task_roi(task, context)

            # Use AI to generate plan
            plan = await self.ai_service.generate_plan(context)

            # Validate and optimize plan
            plan = await self._optimize_plan(plan, pending_tasks, context)

            # Set plan date and hours
            plan.date = target_date
            plan.total_hours = available_hours
            plan.activate()

            # Save tasks back with updated ROI
            for task in plan.tasks:
                await self.task_repository.save(task)

            # Store plan in memory
            from jarvis_core.domain.entities.memory import Memory

            plan_memory = Memory(
                type=MemoryType.STRATEGIC,
                key=f"plan_{target_date.isoformat()}",
                content={"plan_id": plan.plan_id, "date": str(plan.date)},
            )
            await self.memory_repository.save(plan_memory)

            return PlanDTO.from_entity(plan)

        except Exception as e:
            raise DomainException(f"Failed to generate daily plan: {str(e)}")

    async def _load_context(self, target_date: date, available_hours: float) -> Context:
        """Load execution context for planning.

        Args:
            target_date: Target date for the plan
            available_hours: Available hours for execution

        Returns:
            Context entity with loaded data
        """
        context = Context(date=target_date, available_hours=available_hours)

        # Load strategic goals from memory
        goals_memory = await self.memory_repository.get("strategic_goals")
        if goals_memory and isinstance(goals_memory.content, dict):
            goals_data = goals_memory.content.get("goals", [])
            if isinstance(goals_data, list):
                for goal in goals_data:
                    context.add_strategic_goal(goal)

        # Load current focus areas
        focus_memory = await self.memory_repository.get("current_focus")
        if focus_memory and isinstance(focus_memory.content, dict):
            focus_data = focus_memory.content.get("focus_areas", [])
            if isinstance(focus_data, list):
                for focus in focus_data:
                    context.add_focus_area(focus)

        # Load identified gaps
        gaps_memory = await self.memory_repository.get("identified_gaps")
        if gaps_memory and isinstance(gaps_memory.content, dict):
            gaps_data = gaps_memory.content.get("gaps", [])
            if isinstance(gaps_data, list):
                context.gaps = gaps_data

        return context

    async def _optimize_plan(self, plan: Plan, available_tasks: list, context: Context) -> Plan:
        """Optimize the generated plan.

        Args:
            plan: Initial plan from AI service
            available_tasks: Available tasks for scheduling
            context: Current context

        Returns:
            Optimized plan
        """
        # Ensure plan is feasible
        if not plan.is_feasible():
            # Re-prioritize and fit tasks
            scheduled = self.strategy_engine.create_schedule(plan.tasks, plan.total_hours)
            plan.tasks = scheduled

        # Optimize task sequence
        plan.tasks = self.strategy_engine.optimize_task_sequence(plan.tasks, context)

        return plan
