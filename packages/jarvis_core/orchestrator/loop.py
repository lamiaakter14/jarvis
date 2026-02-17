"""Cognitive Loop Orchestrator.

This module implements the complete cognitive loop orchestrator that coordinates
all agents in a deterministic and testable manner.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional

from jarvis_core.orchestrator.context import CognitiveContext, CognitiveProfile
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.repositories import ITaskRepository, IMemoryRepository
from jarvis_core.infrastructure.agents.strategist_agent import StrategistAgent
from jarvis_core.infrastructure.agents.executor_agent import ExecutorAgent
from jarvis_core.infrastructure.agents.innovator_agent import InnovatorAgent
from jarvis_core.infrastructure.agents.amplifier_agent import AmplifierAgent
from jarvis_core.agents.reflector import ReflectorAgent
from jarvis_core.cognition.service import CognitiveService
from jarvis_core.metrics.engine import MetricsEngine
from jarvis_core.shared.exceptions import DomainException
from jarvis_core.shared.utils import current_timestamp


@dataclass
class CognitiveLoopResult:
    """Result DTO from cognitive loop execution.
    
    Attributes:
        plan: Daily plan from strategist
        knowledge_gaps: Identified gaps from analysis
        innovations: Innovation suggestions
        reflection: Reflection analysis and corrections
        metrics: Performance metrics
        execution_time: Total execution time in seconds
        timestamp: When the loop was executed
    """
    
    plan: Dict[str, Any] = field(default_factory=dict)
    knowledge_gaps: List[Dict[str, Any]] = field(default_factory=list)
    innovations: List[Dict[str, Any]] = field(default_factory=list)
    reflection: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    timestamp: str = field(default_factory=lambda: current_timestamp().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary.
        
        Returns:
            Dictionary representation of the result
        """
        return {
            "plan": self.plan,
            "knowledge_gaps": self.knowledge_gaps,
            "innovations": self.innovations,
            "reflection": self.reflection,
            "metrics": self.metrics,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp,
        }


class CognitiveOrchestrator:
    """Orchestrator for the complete cognitive loop.
    
    Implements a deterministic, testable cognitive loop that:
    1. Loads CognitiveProfile
    2. Injects EnergyModel
    3. Runs STRATEGIST for daily planning
    4. Runs EXECUTOR for task scheduling
    5. Runs INNOVATOR for automation ideas
    6. Runs AMPLIFIER for metrics collection
    7. Runs REFLECTOR for self-correction
    8. Persists outputs to memory
    9. Returns comprehensive DTO
    """
    
    def __init__(
        self,
        strategist_agent: StrategistAgent,
        executor_agent: ExecutorAgent,
        innovator_agent: InnovatorAgent,
        amplifier_agent: AmplifierAgent,
        reflector_agent: ReflectorAgent,
        cognitive_service: CognitiveService,
        metrics_engine: MetricsEngine,
        task_repository: ITaskRepository,
        memory_repository: IMemoryRepository,
    ):
        """Initialize the cognitive orchestrator.
        
        Args:
            strategist_agent: Agent for strategic planning
            executor_agent: Agent for task execution
            innovator_agent: Agent for innovation generation
            amplifier_agent: Agent for performance amplification
            reflector_agent: Agent for reflection and correction
            cognitive_service: Service for cognitive operations
            metrics_engine: Engine for metrics calculation
            task_repository: Repository for tasks
            memory_repository: Repository for memory
        """
        self.strategist = strategist_agent
        self.executor = executor_agent
        self.innovator = innovator_agent
        self.amplifier = amplifier_agent
        self.reflector = reflector_agent
        self.cognitive_service = cognitive_service
        self.metrics_engine = metrics_engine
        self.task_repo = task_repository
        self.memory_repo = memory_repository
    
    async def run(
        self, cognitive_context: Optional[CognitiveContext] = None
    ) -> CognitiveLoopResult:
        """Execute the complete cognitive loop.
        
        Args:
            cognitive_context: Optional cognitive context, creates default if None
            
        Returns:
            CognitiveLoopResult with all outputs
            
        Raises:
            DomainException: If cognitive loop execution fails
        """
        start_time = time.time()
        
        try:
            # Step 1: Load CognitiveProfile (or use provided)
            if cognitive_context is None:
                cognitive_context = CognitiveContext.create_default()
            
            profile = cognitive_context.profile
            context = cognitive_context.context
            
            # Step 2: Inject EnergyModel into cognitive service
            energy_state = self.cognitive_service.update_energy(profile.energy)
            
            # Update context with energy information
            if "optimal_focus_hours" in energy_state:
                context.update_available_hours(energy_state["optimal_focus_hours"])
            
            # Step 3: Run STRATEGIST to create daily plan
            plan_result = await self._run_strategist(context, profile)
            
            # Step 4: Run EXECUTOR for task scheduling
            execution_result = await self._run_executor(context)
            
            # Step 5: Run INNOVATOR for automation/delegation ideas
            innovation_result = await self._run_innovator(context)
            
            # Step 6: Run AMPLIFIER to collect metrics
            amplifier_result = await self._run_amplifier(context)
            
            # Step 7: Run REFLECTOR for self-correction
            reflection_result = await self._run_reflector(context)
            
            # Step 8: Calculate comprehensive metrics
            metrics_result = await self._calculate_metrics(
                context, plan_result, execution_result, amplifier_result
            )
            
            # Step 9: Persist outputs to memory
            await self._persist_loop_results(
                cognitive_context,
                plan_result,
                innovation_result,
                reflection_result,
                metrics_result
            )
            
            execution_time = time.time() - start_time
            
            # Step 10: Return comprehensive DTO
            return CognitiveLoopResult(
                plan=plan_result,
                knowledge_gaps=self._extract_knowledge_gaps(context, reflection_result),
                innovations=innovation_result,
                reflection=reflection_result,
                metrics=metrics_result,
                execution_time=execution_time
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            raise DomainException(
                f"Cognitive loop execution failed after {execution_time:.2f}s: {e}"
            )
    
    async def _run_strategist(
        self, context: Context, profile: CognitiveProfile
    ) -> Dict[str, Any]:
        """Run strategist agent for planning.
        
        Args:
            context: Execution context
            profile: Cognitive profile
            
        Returns:
            Plan result dictionary
        """
        # Update context with strategic goals from profile
        if profile.identity.current_primary_mission:
            context.add_strategic_goal(profile.identity.current_primary_mission)
        
        plan = await self.strategist.execute(context)
        
        return {
            "date": context.date.isoformat(),
            "tasks": [
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "priority": task.priority.value if hasattr(task.priority, 'value') else str(task.priority),
                    "estimated_hours": task.cognitive_load.estimated_hours if hasattr(task, 'cognitive_load') else 0.0,
                }
                for task in (plan.tasks if hasattr(plan, 'tasks') else [])
            ],
            "total_tasks": len(plan.tasks) if hasattr(plan, 'tasks') else 0,
            "plan_id": plan.plan_id if hasattr(plan, 'plan_id') else "unknown",
        }
    
    async def _run_executor(self, context: Context) -> Dict[str, Any]:
        """Run executor agent for task execution.
        
        Args:
            context: Execution context
            
        Returns:
            Execution result dictionary
        """
        # Get pending tasks for today
        all_tasks = await self.task_repo.list_all()
        pending_tasks = [
            t for t in all_tasks
            if t.status == "pending" and 
            hasattr(t, 'due_date') and
            t.due_date and
            t.due_date <= context.date
        ]
        
        executed_count = 0
        failed_count = 0
        
        # Execute tasks (in a real implementation, this would actually run them)
        for task in pending_tasks[:5]:  # Limit to 5 for now
            try:
                await self.executor.execute(task)
                executed_count += 1
            except Exception:
                failed_count += 1
        
        return {
            "executed": executed_count,
            "failed": failed_count,
            "pending": len(pending_tasks) - executed_count - failed_count,
            "status": "completed" if failed_count == 0 else "partial",
        }
    
    async def _run_innovator(self, context: Context) -> List[Dict[str, Any]]:
        """Run innovator agent for innovation generation.
        
        Args:
            context: Execution context
            
        Returns:
            List of innovations
        """
        innovations = await self.innovator.execute(context)
        
        return [
            {
                "title": inn.title if hasattr(inn, 'title') else "Unknown",
                "description": inn.description if hasattr(inn, 'description') else "",
                "impact_score": inn.impact_score if hasattr(inn, 'impact_score') else 0.5,
                "category": inn.category if hasattr(inn, 'category') else "general",
            }
            for inn in (innovations if isinstance(innovations, list) else [])
        ]
    
    async def _run_amplifier(self, context: Context) -> Dict[str, Any]:
        """Run amplifier agent for metrics collection.
        
        Args:
            context: Execution context
            
        Returns:
            Amplifier result dictionary
        """
        result = await self.amplifier.execute(context)
        
        return {
            "productivity_score": result.get("productivity_score", 0.0) if isinstance(result, dict) else 0.0,
            "optimization_suggestions": result.get("optimization_suggestions", []) if isinstance(result, dict) else [],
            "performance_trends": result.get("performance_trends", {}) if isinstance(result, dict) else {},
        }
    
    async def _run_reflector(self, context: Context) -> Dict[str, Any]:
        """Run reflector agent for self-correction.
        
        Args:
            context: Execution context
            
        Returns:
            Reflection result dictionary
        """
        result = await self.reflector.execute(context)
        
        return {
            "summary": result.get("reflection_summary", ""),
            "correction_actions": result.get("correction_actions", []),
            "pattern_flags": result.get("pattern_flags", []),
            "skill_graph_updates": result.get("skill_graph_updates", []),
            "drift_level": result.get("drift_level", "none"),
        }
    
    async def _calculate_metrics(
        self,
        context: Context,
        plan_result: Dict[str, Any],
        execution_result: Dict[str, Any],
        amplifier_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics.
        
        Args:
            context: Execution context
            plan_result: Plan from strategist
            execution_result: Execution results
            amplifier_result: Amplifier results
            
        Returns:
            Metrics dictionary
        """
        # Get tasks for metrics calculation
        all_tasks = await self.task_repo.list_all()
        
        completed_tasks = [t for t in all_tasks if t.status == "completed"]
        strategic_tasks = [
            t for t in completed_tasks
            if hasattr(t, 'tags') and any('strategic' in tag.lower() for tag in t.tags)
        ]
        
        # Calculate metrics using metrics engine
        try:
            metrics_report = self.metrics_engine.calculate_metrics(
                completed_tasks_related_to_mission=len(strategic_tasks),
                total_tasks=len(all_tasks),
                completed_tasks=len(completed_tasks),
                active_focus_hours=context.available_hours,
                skill_improvement_delta=0.1,  # Placeholder
                days_elapsed=1,
            )
            
            return {
                "strategic_alignment_score": metrics_report.strategic_alignment_score,
                "cognitive_throughput": metrics_report.cognitive_throughput,
                "learning_velocity": metrics_report.learning_velocity,
                "momentum_index": metrics_report.momentum_index,
                "total_tasks": len(all_tasks),
                "completed_tasks": len(completed_tasks),
                "productivity_score": amplifier_result.get("productivity_score", 0.0),
            }
        except Exception:
            # Return default metrics if calculation fails
            return {
                "strategic_alignment_score": 0.5,
                "cognitive_throughput": 0.0,
                "learning_velocity": 0.0,
                "momentum_index": 0.5,
                "total_tasks": len(all_tasks),
                "completed_tasks": len(completed_tasks),
                "productivity_score": amplifier_result.get("productivity_score", 0.0),
            }
    
    def _extract_knowledge_gaps(
        self, context: Context, reflection_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract knowledge gaps from context and reflection.
        
        Args:
            context: Execution context
            reflection_result: Reflection results
            
        Returns:
            List of knowledge gaps
        """
        gaps = []
        
        # Add gaps from context
        for gap in context.gaps:
            gaps.append(gap)
        
        # Extract gaps from reflection pattern flags
        for flag in reflection_result.get("pattern_flags", []):
            if flag.get("type") in ["strategic_misalignment", "low_completion"]:
                gaps.append({
                    "type": "process",
                    "description": flag.get("description", ""),
                    "severity": flag.get("severity", "medium"),
                    "evidence": ["reflection_analysis"]
                })
        
        return gaps
    
    async def _persist_loop_results(
        self,
        cognitive_context: CognitiveContext,
        plan_result: Dict[str, Any],
        innovation_result: List[Dict[str, Any]],
        reflection_result: Dict[str, Any],
        metrics_result: Dict[str, Any]
    ) -> None:
        """Persist cognitive loop results to memory.
        
        Args:
            cognitive_context: Cognitive context
            plan_result: Plan results
            innovation_result: Innovation results
            reflection_result: Reflection results
            metrics_result: Metrics results
        """
        from jarvis_core.domain.entities.memory import Memory
        from jarvis_core.shared.constants import MemoryType
        
        # Store cognitive loop summary
        loop_summary = Memory(
            type=MemoryType.EXECUTION_LOG,
            key=f"cognitive_loop_{cognitive_context.context.date.isoformat()}",
            content={
                "date": cognitive_context.context.date.isoformat(),
                "plan": plan_result,
                "innovations_count": len(innovation_result),
                "reflection_drift_level": reflection_result.get("drift_level", "none"),
                "metrics": metrics_result,
                "timestamp": current_timestamp().isoformat(),
            },
            metadata={
                "orchestrator": "cognitive_loop_v2",
                "version": cognitive_context.metadata.get("version", "2.0"),
            }
        )
        
        loop_summary.add_tags(["cognitive_loop", "daily", "orchestrator"])
        
        await self.memory_repo.save(loop_summary)
