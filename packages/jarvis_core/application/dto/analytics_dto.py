"""Analytics Data Transfer Object for application layer."""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class AnalyticsDTO(BaseModel):
    """Data Transfer Object for analytics and performance metrics.
    
    Provides a serializable representation of analytics data for reporting
    and visualization purposes.
    """
    
    period: str = Field(..., description="Time period for analytics (e.g., 'daily', 'weekly', 'monthly')")
    total_tasks: int = Field(default=0, ge=0, description="Total number of tasks in period")
    completed_tasks: int = Field(default=0, ge=0, description="Number of completed tasks")
    average_roi: float = Field(default=0.0, ge=0.0, le=1.0, description="Average ROI across tasks")
    top_gaps: List[Dict[str, Any]] = Field(default_factory=list, description="Top identified gaps")
    recent_innovations: List[Dict[str, Any]] = Field(default_factory=list, description="Recent innovations")
    productivity_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall productivity score")
    
    # Additional metrics
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Task success rate")
    failed_tasks: int = Field(default=0, ge=0, description="Number of failed tasks")
    pending_tasks: int = Field(default=0, ge=0, description="Number of pending tasks")
    average_task_duration: float = Field(default=0.0, ge=0.0, description="Average task duration in hours")
    total_hours_spent: float = Field(default=0.0, ge=0.0, description="Total hours spent on tasks")
    utilization_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Time utilization rate")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "period": "weekly",
                "total_tasks": 25,
                "completed_tasks": 20,
                "average_roi": 0.75,
                "top_gaps": [
                    {"type": "knowledge", "description": "Advanced Python", "severity": "high"}
                ],
                "recent_innovations": [
                    {"title": "Automate testing", "impact_score": 0.8}
                ],
                "productivity_score": 0.82,
                "success_rate": 0.8,
                "failed_tasks": 2,
                "pending_tasks": 3,
                "average_task_duration": 2.5,
                "total_hours_spent": 50.0,
                "utilization_rate": 0.78
            }
        }
    
    def to_dict(self) -> Dict:
        """Convert DTO to dictionary.
        
        Returns:
            Dictionary representation of analytics
        """
        return self.model_dump()
    
    def get_completion_rate(self) -> float:
        """Calculate task completion rate.
        
        Returns:
            Completion rate as percentage (0.0 to 100.0)
        """
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100.0
    
    def get_failure_rate(self) -> float:
        """Calculate task failure rate.
        
        Returns:
            Failure rate as percentage (0.0 to 100.0)
        """
        if self.total_tasks == 0:
            return 0.0
        return (self.failed_tasks / self.total_tasks) * 100.0
    
    def is_high_performance(self) -> bool:
        """Check if performance is considered high.
        
        Returns:
            True if productivity score and success rate are both >= 0.8
        """
        return self.productivity_score >= 0.8 and self.success_rate >= 0.8
    
    def get_summary(self) -> str:
        """Get a human-readable summary of analytics.
        
        Returns:
            Summary string
        """
        return (
            f"Analytics for {self.period}: "
            f"{self.completed_tasks}/{self.total_tasks} tasks completed "
            f"({self.get_completion_rate():.1f}%), "
            f"Productivity: {self.productivity_score:.2f}, "
            f"ROI: {self.average_roi:.2f}"
        )
