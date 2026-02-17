"""Reflector Agent for analyzing execution and suggesting corrections.

The Reflector Agent is responsible for:
- Analyzing the previous day's execution
- Detecting drift from the current mission
- Suggesting correction actions to improve alignment
- Updating SkillGraph weights based on patterns
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.domain.repositories import IMemoryRepository, ITaskRepository
from jarvis_core.cognition.models import SkillGraph
from jarvis_core.shared.exceptions import DomainException


class ReflectorAgent(Agent):
    """Reflector agent for self-correction and alignment.
    
    The reflector analyzes execution patterns, detects drift from strategic
    goals, and suggests corrections to improve alignment with the mission.
    """
    
    def __init__(
        self,
        memory_repo: IMemoryRepository,
        task_repo: ITaskRepository,
    ):
        """Initialize the reflector agent.
        
        Args:
            memory_repo: Repository for memory operations
            task_repo: Repository for task operations
        """
        super().__init__(
            agent_type=AgentType.REFLECTOR,
            name="Reflector Agent",
            description="Analyzes execution and suggests corrections for alignment"
        )
        self.memory_repo = memory_repo
        self.task_repo = task_repo
    
    async def execute(self, context: Context) -> Dict[str, Any]:
        """Execute reflector's primary function: analyze and suggest corrections.
        
        Args:
            context: Current execution context
            
        Returns:
            Dictionary containing:
                - reflection_summary: Summary of execution analysis
                - correction_actions: List of 3 correction actions
                - pattern_flags: Detected patterns and drift indicators
                - skill_graph_updates: Suggested skill weight updates
            
        Raises:
            DomainException: If execution fails
        """
        start_time = time.time()
        
        try:
            # Analyze previous day's execution
            execution_analysis = await self._analyze_execution(context)
            
            # Detect drift from mission
            drift_analysis = await self._detect_mission_drift(context, execution_analysis)
            
            # Generate correction actions
            correction_actions = await self._generate_correction_actions(
                context, execution_analysis, drift_analysis
            )
            
            # Update skill graph weights
            skill_updates = await self._update_skill_graph_weights(
                context, execution_analysis
            )
            
            # Create reflection summary
            reflection_summary = self._create_reflection_summary(
                execution_analysis, drift_analysis, correction_actions
            )
            
            # Store reflection in memory
            await self._store_reflection(
                context, reflection_summary, correction_actions, drift_analysis
            )
            
            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)
            
            return {
                "reflection_summary": reflection_summary,
                "correction_actions": correction_actions,
                "pattern_flags": drift_analysis.get("pattern_flags", []),
                "skill_graph_updates": skill_updates,
                "execution_time": execution_time
            }
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Reflector execution failed: {e}")
    
    async def _analyze_execution(self, context: Context) -> Dict[str, Any]:
        """Analyze the previous day's execution.
        
        Args:
            context: Current execution context
            
        Returns:
            Dictionary containing execution analysis
        """
        # Get tasks from previous day
        yesterday = context.date - timedelta(days=1)
        
        # Retrieve completed and missed tasks
        all_tasks = await self.task_repo.list_all()
        
        # Filter tasks from yesterday
        completed_tasks = [
            t for t in all_tasks
            if t.status == "completed" and 
            hasattr(t, 'completed_at') and
            t.completed_at and
            t.completed_at.date() == yesterday
        ]
        
        missed_tasks = [
            t for t in all_tasks
            if t.status in ["pending", "in_progress"] and
            hasattr(t, 'due_date') and
            t.due_date and
            t.due_date < context.date
        ]
        
        # Calculate completion metrics
        total_planned = len(completed_tasks) + len(missed_tasks)
        completion_rate = (
            len(completed_tasks) / total_planned if total_planned > 0 else 0.0
        )
        
        # Analyze task quality and alignment
        strategic_tasks = [
            t for t in completed_tasks
            if hasattr(t, 'tags') and any('strategic' in tag.lower() for tag in t.tags)
        ]
        
        strategic_alignment = (
            len(strategic_tasks) / len(completed_tasks)
            if len(completed_tasks) > 0 else 0.0
        )
        
        return {
            "date": yesterday.isoformat(),
            "total_planned": total_planned,
            "completed": len(completed_tasks),
            "missed": len(missed_tasks),
            "completion_rate": completion_rate,
            "strategic_alignment": strategic_alignment,
            "completed_task_ids": [t.task_id for t in completed_tasks],
            "missed_task_ids": [t.task_id for t in missed_tasks],
        }
    
    async def _detect_mission_drift(
        self, context: Context, execution_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect drift from current mission.
        
        Args:
            context: Current execution context
            execution_analysis: Analysis of execution
            
        Returns:
            Dictionary containing drift analysis and pattern flags
        """
        pattern_flags = []
        drift_score = 0.0
        
        # Check completion rate pattern
        completion_rate = execution_analysis.get("completion_rate", 0.0)
        if completion_rate < 0.5:
            pattern_flags.append({
                "type": "low_completion",
                "severity": "high",
                "description": f"Low completion rate: {completion_rate:.1%}"
            })
            drift_score += 0.3
        
        # Check strategic alignment
        strategic_alignment = execution_analysis.get("strategic_alignment", 0.0)
        if strategic_alignment < 0.6:
            pattern_flags.append({
                "type": "strategic_misalignment",
                "severity": "high",
                "description": f"Strategic alignment below target: {strategic_alignment:.1%}"
            })
            drift_score += 0.4
        
        # Check for repeated missed tasks
        missed_count = execution_analysis.get("missed", 0)
        if missed_count > 3:
            pattern_flags.append({
                "type": "task_accumulation",
                "severity": "medium",
                "description": f"Accumulation of missed tasks: {missed_count}"
            })
            drift_score += 0.3
        
        # Determine overall drift level
        drift_level = "none"
        if drift_score >= 0.7:
            drift_level = "critical"
        elif drift_score >= 0.4:
            drift_level = "moderate"
        elif drift_score > 0:
            drift_level = "minor"
        
        return {
            "drift_score": min(drift_score, 1.0),
            "drift_level": drift_level,
            "pattern_flags": pattern_flags,
            "requires_intervention": drift_score >= 0.4
        }
    
    async def _generate_correction_actions(
        self,
        context: Context,
        execution_analysis: Dict[str, Any],
        drift_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate 3 correction actions to improve alignment.
        
        Args:
            context: Current execution context
            execution_analysis: Analysis of execution
            drift_analysis: Drift detection results
            
        Returns:
            List of 3 correction actions
        """
        actions = []
        
        # Action 1: Address completion rate if low
        completion_rate = execution_analysis.get("completion_rate", 0.0)
        if completion_rate < 0.7:
            actions.append({
                "priority": 1,
                "action_type": "task_optimization",
                "title": "Reduce daily task load",
                "description": (
                    f"Current completion rate is {completion_rate:.1%}. "
                    "Reduce the number of planned tasks by 20-30% to improve "
                    "completion rate and reduce cognitive overload."
                ),
                "expected_impact": "high",
                "effort": "low"
            })
        
        # Action 2: Address strategic alignment
        strategic_alignment = execution_analysis.get("strategic_alignment", 0.0)
        if strategic_alignment < 0.6:
            actions.append({
                "priority": 1,
                "action_type": "strategic_focus",
                "title": "Increase strategic task focus",
                "description": (
                    f"Strategic alignment is {strategic_alignment:.1%}. "
                    "Prioritize tasks that directly contribute to strategic goals. "
                    "Review and tag strategic tasks clearly."
                ),
                "expected_impact": "high",
                "effort": "medium"
            })
        
        # Action 3: Address missed tasks
        missed_count = execution_analysis.get("missed", 0)
        if missed_count > 2:
            actions.append({
                "priority": 2,
                "action_type": "task_cleanup",
                "title": "Clear backlog of missed tasks",
                "description": (
                    f"There are {missed_count} missed tasks. "
                    "Review and either reschedule, delegate, or cancel tasks "
                    "that are no longer relevant."
                ),
                "expected_impact": "medium",
                "effort": "medium"
            })
        
        # Define default actions pool
        default_actions = [
            {
                "priority": 3,
                "action_type": "skill_development",
                "title": "Focus on skill development",
                "description": (
                    "Allocate time for skill improvement in areas related to "
                    "strategic goals. Identify gaps and create learning tasks."
                ),
                "expected_impact": "medium",
                "effort": "low"
            },
            {
                "priority": 3,
                "action_type": "process_improvement",
                "title": "Review and optimize daily planning process",
                "description": (
                    "Analyze task estimation accuracy and planning effectiveness. "
                    "Adjust planning approach based on recent execution patterns."
                ),
                "expected_impact": "medium",
                "effort": "low"
            },
            {
                "priority": 3,
                "action_type": "energy_management",
                "title": "Optimize energy and focus management",
                "description": (
                    "Review daily energy patterns and adjust task scheduling "
                    "to align high-priority work with peak energy periods."
                ),
                "expected_impact": "medium",
                "effort": "low"
            }
        ]
        
        # Add default actions if needed to reach 3
        for default_action in default_actions:
            if len(actions) >= 3:
                break
            actions.append(default_action)
        
        # Return exactly 3 actions, sorted by priority
        return sorted(actions, key=lambda x: x["priority"])[:3]
    
    async def _update_skill_graph_weights(
        self, context: Context, execution_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Update SkillGraph weights based on execution patterns.
        
        Args:
            context: Current execution context
            execution_analysis: Analysis of execution
            
        Returns:
            List of suggested skill weight updates
        """
        updates = []
        
        # Get completed tasks to analyze skill usage
        completed_task_ids = execution_analysis.get("completed_task_ids", [])
        
        # In a full implementation, we would:
        # 1. Extract skills from completed tasks
        # 2. Calculate frequency of skill usage
        # 3. Suggest weight adjustments based on usage patterns
        # 4. Consider strategic goals to boost relevant skills
        
        # For now, provide a simple pattern-based update
        strategic_alignment = execution_analysis.get("strategic_alignment", 0.0)
        
        if strategic_alignment < 0.6:
            updates.append({
                "skill_pattern": "strategic_planning",
                "suggested_weight": 0.9,
                "reason": "Low strategic alignment - boost strategic planning skills",
                "current_weight": 0.5
            })
        
        completion_rate = execution_analysis.get("completion_rate", 0.0)
        if completion_rate < 0.7:
            updates.append({
                "skill_pattern": "time_management",
                "suggested_weight": 0.85,
                "reason": "Low completion rate - boost time management skills",
                "current_weight": 0.5
            })
        
        return updates
    
    def _create_reflection_summary(
        self,
        execution_analysis: Dict[str, Any],
        drift_analysis: Dict[str, Any],
        correction_actions: List[Dict[str, Any]]
    ) -> str:
        """Create a human-readable reflection summary.
        
        Args:
            execution_analysis: Analysis of execution
            drift_analysis: Drift detection results
            correction_actions: Generated correction actions
            
        Returns:
            Reflection summary text
        """
        completion_rate = execution_analysis.get("completion_rate", 0.0)
        strategic_alignment = execution_analysis.get("strategic_alignment", 0.0)
        drift_level = drift_analysis.get("drift_level", "none")
        
        summary_parts = [
            f"# Daily Reflection - {execution_analysis.get('date', 'Unknown')}",
            "",
            "## Execution Performance",
            f"- Tasks Completed: {execution_analysis.get('completed', 0)} / {execution_analysis.get('total_planned', 0)}",
            f"- Completion Rate: {completion_rate:.1%}",
            f"- Strategic Alignment: {strategic_alignment:.1%}",
            f"- Missed Tasks: {execution_analysis.get('missed', 0)}",
            "",
            "## Drift Analysis",
            f"- Drift Level: {drift_level.upper()}",
            f"- Drift Score: {drift_analysis.get('drift_score', 0.0):.2f}",
        ]
        
        # Add pattern flags if any
        pattern_flags = drift_analysis.get("pattern_flags", [])
        if pattern_flags:
            summary_parts.extend(["", "## Detected Patterns"])
            for flag in pattern_flags:
                summary_parts.append(
                    f"- [{flag['severity'].upper()}] {flag['description']}"
                )
        
        # Add correction actions
        summary_parts.extend(["", "## Recommended Corrections"])
        for i, action in enumerate(correction_actions, 1):
            summary_parts.append(f"{i}. **{action['title']}** (Priority {action['priority']})")
            summary_parts.append(f"   {action['description']}")
        
        return "\n".join(summary_parts)
    
    async def _store_reflection(
        self,
        context: Context,
        reflection_summary: str,
        correction_actions: List[Dict[str, Any]],
        drift_analysis: Dict[str, Any]
    ) -> None:
        """Store reflection in memory for future reference.
        
        Args:
            context: Current execution context
            reflection_summary: Summary text
            correction_actions: List of correction actions
            drift_analysis: Drift analysis results
        """
        from jarvis_core.domain.entities.memory import Memory
        from jarvis_core.shared.constants import MemoryType
        
        reflection_memory = Memory(
            type=MemoryType.EXECUTION_LOG,
            key=f"reflection_{context.date.isoformat()}",
            content={
                "date": context.date.isoformat(),
                "summary": reflection_summary,
                "correction_actions": correction_actions,
                "drift_analysis": drift_analysis,
                "context_id": context.context_id,
            },
            metadata={
                "agent": "reflector",
                "drift_level": drift_analysis.get("drift_level", "none"),
                "requires_intervention": drift_analysis.get("requires_intervention", False)
            }
        )
        
        # Add tags using the add_tags method
        reflection_memory.add_tags(["reflection", "daily", "analysis"])
        
        await self.memory_repo.save(reflection_memory)
