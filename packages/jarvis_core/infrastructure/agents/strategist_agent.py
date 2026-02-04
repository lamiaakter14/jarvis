"""Strategist agent implementation."""

from typing import Any, Dict
import time

from src.domain.entities.agent import Agent
from src.domain.entities.context import Context
from src.domain.entities.plan import Plan
from src.domain.value_objects.agent_type import AgentType
from src.application.interfaces.i_ai_service import IAIService
from src.domain.repositories.i_memory_repository import IMemoryRepository
from src.domain.repositories.i_task_repository import ITaskRepository
from src.shared.exceptions import DomainException


class StrategistAgent(Agent):
    """Strategist agent for planning and task organization.
    
    The strategist analyzes context, strategic goals, and available resources
    to create optimized daily plans with appropriate task selection and ordering.
    """
    
    def __init__(
        self,
        ai_service: IAIService,
        memory_repo: IMemoryRepository,
        task_repo: ITaskRepository,
    ):
        """Initialize strategist agent.
        
        Args:
            ai_service: AI service for plan generation
            memory_repo: Memory repository for context access
            task_repo: Task repository for task persistence
        """
        super().__init__(
            agent_type=AgentType.strategist(),
            name="Strategist Agent",
            description="Plans and organizes daily tasks based on strategic goals",
        )
        self.ai_service = ai_service
        self.memory_repo = memory_repo
        self.task_repo = task_repo
    
    async def execute(self, context: Context) -> Plan:
        """Execute strategist's primary function: generate daily plan.
        
        Args:
            context: Current execution context
            
        Returns:
            Generated daily plan
            
        Raises:
            DomainException: If plan generation fails
        """
        start_time = time.time()
        
        try:
            # Generate plan using AI service
            plan = await self.ai_service.generate_plan(context)
            
            # Persist all tasks from the plan
            for task in plan.tasks:
                await self.task_repo.save(task)
            
            # Track successful execution
            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)
            
            return plan
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Strategist execution failed: {e}")
    
    async def analyze_context(self, context: Context) -> Dict[str, Any]:
        """Analyze context to understand current state and priorities.
        
        Args:
            context: Context to analyze
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "available_hours": context.available_hours,
            "focus_areas": context.current_focus,
            "gaps_count": len(context.gaps),
            "high_severity_gaps": len(context.get_high_severity_gaps()),
            "strategic_goals_count": len(context.strategic_goals),
            "recommendations": [],
        }
        
        # Add recommendations based on analysis
        if context.available_hours < 4:
            analysis["recommendations"].append(
                "Limited time available - focus on high-priority items only"
            )
        
        if len(context.get_high_severity_gaps()) > 0:
            analysis["recommendations"].append(
                "High-severity gaps identified - consider addressing them"
            )
        
        if not context.current_focus:
            analysis["recommendations"].append(
                "No focus areas defined - consider setting priorities"
            )
        
        return analysis
    
    async def optimize_plan(self, plan: Plan) -> Plan:
        """Optimize an existing plan for better efficiency.
        
        Args:
            plan: Plan to optimize
            
        Returns:
            Optimized plan
        """
        # Sort tasks by score (priority + ROI + efficiency)
        plan.sort_tasks_by_score()
        
        # Check feasibility
        if not plan.is_feasible():
            # Remove lowest-scoring tasks until feasible
            while not plan.is_feasible() and len(plan.tasks) > 0:
                # Remove last task (lowest score after sorting)
                lowest_task = plan.tasks[-1]
                plan.remove_task(lowest_task.task_id)
        
        return plan
