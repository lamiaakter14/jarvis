"""Analyze Performance use case."""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any

from src.application.dto.analytics_dto import AnalyticsDTO
from src.domain.repositories import ITaskRepository, IAnalyticsRepository, IMemoryRepository
from src.shared.constants import TaskStatus
from src.shared.exceptions import DomainException


class AnalyzePerformance:
    """Use case for analyzing performance metrics.
    
    Calculates comprehensive analytics including task completion rates,
    ROI metrics, productivity scores, and identifies trends.
    """
    
    def __init__(
        self,
        task_repository: ITaskRepository,
        analytics_repository: IAnalyticsRepository,
        memory_repository: IMemoryRepository
    ):
        """Initialize use case with dependencies.
        
        Args:
            task_repository: Repository for task data
            analytics_repository: Repository for analytics storage
            memory_repository: Repository for memory/context data
        """
        self.task_repository = task_repository
        self.analytics_repository = analytics_repository
        self.memory_repository = memory_repository
    
    async def execute(self, start_date: date, end_date: date) -> AnalyticsDTO:
        """Analyze performance for specified date range.
        
        Args:
            start_date: Start date of analysis period
            end_date: End date of analysis period
            
        Returns:
            AnalyticsDTO with performance metrics
            
        Raises:
            DomainException: If analysis fails
        """
        if start_date > end_date:
            raise DomainException("Start date must be before or equal to end date")
        
        try:
            # Calculate period descriptor
            days = (end_date - start_date).days + 1
            if days == 1:
                period = "daily"
            elif days <= 7:
                period = "weekly"
            elif days <= 31:
                period = "monthly"
            else:
                period = f"{days}_days"
            
            # Get all tasks in date range
            all_tasks = await self.task_repository.list()
            tasks_in_period = [
                t for t in all_tasks
                if start_date <= t.created_at.date() <= end_date
            ]
            
            # Calculate basic metrics
            total_tasks = len(tasks_in_period)
            completed_tasks = len([t for t in tasks_in_period if t.is_completed()])
            failed_tasks = len([t for t in tasks_in_period if t.is_failed()])
            pending_tasks = len([t for t in tasks_in_period if t.is_pending()])
            
            # Calculate success rate
            attempted_tasks = completed_tasks + failed_tasks
            success_rate = completed_tasks / attempted_tasks if attempted_tasks > 0 else 0.0
            
            # Calculate average ROI
            average_roi = (
                sum(t.roi.value for t in tasks_in_period) / total_tasks
                if total_tasks > 0 else 0.0
            )
            
            # Calculate time metrics
            total_hours = sum(
                t.cognitive_load.estimated_hours
                for t in tasks_in_period
                if t.is_completed()
            )
            
            completed_with_duration = [
                t for t in tasks_in_period
                if t.is_completed() and t.calculate_duration()
            ]
            
            avg_duration_seconds = (
                sum(t.calculate_duration() for t in completed_with_duration) / 
                len(completed_with_duration)
                if completed_with_duration else 0.0
            )
            avg_task_duration_hours = avg_duration_seconds / 3600.0
            
            # Calculate utilization
            available_hours = days * 8.0  # Assume 8 hours per day
            utilization_rate = total_hours / available_hours if available_hours > 0 else 0.0
            
            # Get top gaps
            top_gaps = await self._get_top_gaps()
            
            # Get recent innovations
            recent_innovations = await self._get_recent_innovations()
            
            # Calculate productivity score
            productivity_score = self._calculate_productivity_score(
                success_rate=success_rate,
                completion_rate=completed_tasks / total_tasks if total_tasks > 0 else 0.0,
                average_roi=average_roi,
                utilization_rate=utilization_rate
            )
            
            # Create analytics DTO
            analytics = AnalyticsDTO(
                period=period,
                total_tasks=total_tasks,
                completed_tasks=completed_tasks,
                average_roi=average_roi,
                top_gaps=top_gaps,
                recent_innovations=recent_innovations,
                productivity_score=productivity_score,
                success_rate=success_rate,
                failed_tasks=failed_tasks,
                pending_tasks=pending_tasks,
                average_task_duration=avg_task_duration_hours,
                total_hours_spent=total_hours,
                utilization_rate=min(utilization_rate, 1.0),
            )
            
            # Store analytics
            await self.analytics_repository.save_execution_metrics({
                "period": period,
                "timestamp": end_date.isoformat(),
                "metrics": analytics.to_dict()
            })
            
            return analytics
            
        except Exception as e:
            raise DomainException(f"Failed to analyze performance: {str(e)}")
    
    async def _get_top_gaps(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top identified gaps.
        
        Args:
            limit: Maximum number of gaps to return
            
        Returns:
            List of top gaps
        """
        gaps_memory = await self.memory_repository.get("identified_gaps")
        
        if not gaps_memory or not isinstance(gaps_memory.content, dict):
            return []
        
        gaps_data = gaps_memory.content.get("gaps", [])
        if not isinstance(gaps_data, list):
            return []
        
        # Sort by severity and return top N
        severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        sorted_gaps = sorted(
            gaps_data,
            key=lambda g: severity_order.get(g.get("severity", "low"), 0),
            reverse=True
        )
        
        return sorted_gaps[:limit]
    
    async def _get_recent_innovations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent innovations.
        
        Args:
            limit: Maximum number of innovations to return
            
        Returns:
            List of recent innovations
        """
        innovations_memory = await self.memory_repository.get("recent_innovations")
        
        if not innovations_memory or not isinstance(innovations_memory.content, dict):
            return []
        
        innovations_data = innovations_memory.content.get("innovations", [])
        if not isinstance(innovations_data, list):
            return []
        
        # Return most recent
        return innovations_data[:limit]
    
    def _calculate_productivity_score(
        self,
        success_rate: float,
        completion_rate: float,
        average_roi: float,
        utilization_rate: float
    ) -> float:
        """Calculate overall productivity score.
        
        Args:
            success_rate: Task success rate
            completion_rate: Task completion rate
            average_roi: Average ROI of tasks
            utilization_rate: Time utilization rate
            
        Returns:
            Productivity score (0.0 to 1.0)
        """
        # Weighted average of different factors
        # Success: 30%, Completion: 25%, ROI: 25%, Utilization: 20%
        score = (
            success_rate * 0.30 +
            completion_rate * 0.25 +
            average_roi * 0.25 +
            min(utilization_rate, 1.0) * 0.20
        )
        
        return min(max(score, 0.0), 1.0)
