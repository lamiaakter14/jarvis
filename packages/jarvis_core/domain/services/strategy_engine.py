"""Strategy engine domain service."""

from typing import List

from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.shared.exceptions import DomainException


class StrategyEngine:
    """Service for strategic task planning and prioritization.
    
    The StrategyEngine applies business logic to prioritize tasks,
    create optimal schedules, and calculate ROI for strategic decision-making.
    """
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Prioritize tasks by ROI and other strategic factors.
        
        Sorts tasks in descending order of importance based on ROI,
        priority, and cognitive load efficiency.
        
        Args:
            tasks: List of tasks to prioritize
            
        Returns:
            Sorted list of tasks (highest priority first)
        """
        if not tasks:
            return []
        
        # Sort by task score (which combines ROI, priority, and efficiency)
        return sorted(tasks, key=lambda t: t.get_score(), reverse=True)
    
    def create_schedule(
        self,
        tasks: List[Task],
        available_hours: float
    ) -> List[Task]:
        """Create an optimal schedule fitting tasks into available time.
        
        Uses a greedy algorithm to select high-value tasks that fit
        within the available time constraint.
        
        Args:
            tasks: List of tasks to schedule
            available_hours: Hours available for task execution
            
        Returns:
            List of scheduled tasks that fit in available time
            
        Raises:
            DomainException: If available hours is invalid
        """
        if available_hours <= 0:
            raise DomainException("Available hours must be positive")
        
        if not tasks:
            return []
        
        # First prioritize tasks
        prioritized = self.prioritize_tasks(tasks)
        
        # Greedily select tasks that fit in schedule
        scheduled = []
        remaining_hours = available_hours
        
        for task in prioritized:
            if task.can_fit_in_schedule(remaining_hours):
                scheduled.append(task)
                remaining_hours -= task.cognitive_load.estimated_hours
                
                # Stop if no time remains
                if remaining_hours <= 0:
                    break
        
        return scheduled
    
    def calculate_task_roi(self, task: Task, context: Context) -> ROI:
        """Calculate ROI for a task given current context.
        
        Considers task impact, urgency based on context, and effort required.
        
        Args:
            task: Task to calculate ROI for
            context: Current execution context
            
        Returns:
            Calculated ROI value object
            
        Raises:
            DomainException: If calculation fails
        """
        # Base impact from priority
        impact_score = task.priority.weight
        
        # Adjust impact based on strategic goals alignment
        if context.strategic_goals:
            # Check if task aligns with strategic goals
            task_terms = set(task.title.lower().split() + 
                           task.description.lower().split())
            goal_terms = set()
            for goal in context.strategic_goals:
                goal_terms.update(goal.lower().split())
            
            # Increase impact if aligned with goals
            overlap = len(task_terms.intersection(goal_terms))
            if overlap > 0:
                impact_score = min(impact_score + 0.1, 1.0)
        
        # Urgency based on priority and context focus
        urgency_score = task.priority.weight
        
        # Increase urgency if task aligns with current focus
        if context.current_focus:
            for focus in context.current_focus:
                if focus.lower() in task.title.lower() or \
                   focus.lower() in task.description.lower():
                    urgency_score = min(urgency_score + 0.2, 1.0)
                    break
        
        # Effort from cognitive load
        effort_hours = task.cognitive_load.estimated_hours
        
        # Calculate ROI
        return ROI.calculate(
            impact_score=impact_score,
            urgency_score=urgency_score,
            effort_hours=effort_hours,
            max_effort_hours=8.0
        )
    
    def analyze_task_portfolio(
        self,
        tasks: List[Task]
    ) -> dict:
        """Analyze a portfolio of tasks for strategic insights.
        
        Provides metrics and recommendations for task management.
        
        Args:
            tasks: List of tasks to analyze
            
        Returns:
            Dictionary containing portfolio analysis
        """
        if not tasks:
            return {
                "total_tasks": 0,
                "average_roi": 0.0,
                "high_roi_count": 0,
                "total_estimated_hours": 0.0,
                "high_priority_count": 0,
                "recommendations": ["No tasks in portfolio"]
            }
        
        total_roi = sum(t.roi.value for t in tasks)
        high_roi_tasks = [t for t in tasks if t.is_high_roi()]
        high_priority_tasks = [t for t in tasks if t.is_high_priority()]
        total_hours = sum(t.cognitive_load.estimated_hours for t in tasks)
        
        analysis = {
            "total_tasks": len(tasks),
            "average_roi": total_roi / len(tasks),
            "high_roi_count": len(high_roi_tasks),
            "high_roi_percentage": len(high_roi_tasks) / len(tasks) * 100,
            "total_estimated_hours": total_hours,
            "average_hours_per_task": total_hours / len(tasks),
            "high_priority_count": len(high_priority_tasks),
            "high_priority_percentage": len(high_priority_tasks) / len(tasks) * 100,
            "recommendations": []
        }
        
        # Add recommendations
        if analysis["high_roi_percentage"] < 30:
            analysis["recommendations"].append(
                "Low percentage of high-ROI tasks - consider reprioritizing"
            )
        
        if analysis["average_hours_per_task"] > 4:
            analysis["recommendations"].append(
                "Tasks are large - consider breaking into smaller units"
            )
        
        if analysis["high_priority_count"] > len(tasks) * 0.7:
            analysis["recommendations"].append(
                "Too many high-priority tasks - review prioritization criteria"
            )
        
        return analysis
    
    def optimize_task_sequence(
        self,
        tasks: List[Task],
        context: Context
    ) -> List[Task]:
        """Optimize task execution sequence for maximum efficiency.
        
        Orders tasks to minimize context switching and maximize flow.
        Groups similar tasks together while respecting priority.
        
        Args:
            tasks: List of tasks to sequence
            context: Current execution context
            
        Returns:
            Optimally sequenced list of tasks
        """
        if not tasks:
            return []
        
        # First prioritize by importance
        prioritized = self.prioritize_tasks(tasks)
        
        # Group by agent type for better context continuity
        by_type = {}
        for task in prioritized:
            agent_type = str(task.agent_type)
            if agent_type not in by_type:
                by_type[agent_type] = []
            by_type[agent_type].append(task)
        
        # Interleave groups to maintain priority while reducing switching
        optimized = []
        while any(by_type.values()):
            for agent_type in sorted(by_type.keys()):
                if by_type[agent_type]:
                    optimized.append(by_type[agent_type].pop(0))
        
        return optimized
