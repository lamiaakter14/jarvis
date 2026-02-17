"""Metrics Engine for JARVIS system performance tracking.

This module implements the Metrics Engine which calculates various performance
metrics to assess the system's progress and performance against strategic goals.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class MetricsReport(BaseModel):
    """Data Transfer Object for metrics reporting.
    
    Provides a structured output that holds calculated metrics data for
    performance evaluation and tracking.
    
    Attributes:
        timestamp: When the metrics were calculated
        strategic_alignment_score: Ratio of completed tasks related to primary mission
        cognitive_throughput: Tasks completed per active focus hour
        learning_velocity: Skill improvement per day
        momentum_index: Weighted combination of all metrics
        total_tasks: Total number of tasks in the period
        completed_tasks_related_to_mission: Tasks completed that align with primary mission
        completed_tasks: Total completed tasks
        active_focus_hours: Hours of active focused work
        skill_improvement_delta: Change in skill proficiency
        days_elapsed: Number of days in the measurement period
        metadata: Additional contextual information
    """
    
    model_config = ConfigDict(from_attributes=True)
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the metrics were calculated"
    )
    strategic_alignment_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Ratio of completed tasks related to primary mission"
    )
    cognitive_throughput: float = Field(
        ...,
        ge=0.0,
        description="Tasks completed per active focus hour"
    )
    learning_velocity: float = Field(
        ...,
        description="Skill improvement per day"
    )
    momentum_index: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Weighted combination of all metrics"
    )
    
    # Supporting metrics data
    total_tasks: int = Field(default=0, ge=0, description="Total number of tasks")
    completed_tasks_related_to_mission: int = Field(
        default=0,
        ge=0,
        description="Tasks completed that align with primary mission"
    )
    completed_tasks: int = Field(default=0, ge=0, description="Total completed tasks")
    active_focus_hours: float = Field(default=0.0, ge=0.0, description="Hours of active focus")
    skill_improvement_delta: float = Field(
        default=0.0,
        description="Change in skill proficiency"
    )
    days_elapsed: float = Field(default=1.0, gt=0.0, description="Days in measurement period")
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional contextual information"
    )
    
    @field_validator('strategic_alignment_score', 'momentum_index')
    @classmethod
    def validate_score_range(cls, v: float) -> float:
        """Validate that scores are within valid range."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics report to dictionary.
        
        Returns:
            Dictionary representation of the metrics report
        """
        return self.model_dump()
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the metrics.
        
        Returns:
            Summary string describing the metrics
        """
        return (
            f"Metrics Report ({self.timestamp.strftime('%Y-%m-%d %H:%M')}): "
            f"Strategic Alignment: {self.strategic_alignment_score:.2%}, "
            f"Cognitive Throughput: {self.cognitive_throughput:.2f} tasks/hour, "
            f"Learning Velocity: {self.learning_velocity:.3f}/day, "
            f"Momentum Index: {self.momentum_index:.2%}"
        )
    
    def is_high_performance(self) -> bool:
        """Check if system is in high performance state.
        
        Returns:
            True if momentum index >= 0.8 and strategic alignment >= 0.7
        """
        return self.momentum_index >= 0.8 and self.strategic_alignment_score >= 0.7


class MetricsEngine:
    """Engine for calculating performance metrics for the JARVIS system.
    
    This engine provides modular, well-documented, and testable methods for
    calculating various performance metrics to evaluate system progress and
    performance against strategic goals.
    """
    
    def __init__(
        self,
        strategic_weight: float = 0.35,
        throughput_weight: float = 0.30,
        learning_weight: float = 0.20,
        base_weight: float = 0.15
    ):
        """Initialize the MetricsEngine.
        
        Args:
            strategic_weight: Weight for strategic alignment in momentum calculation
            throughput_weight: Weight for cognitive throughput in momentum calculation
            learning_weight: Weight for learning velocity in momentum calculation
            base_weight: Weight for baseline completion rate in momentum calculation
            
        Raises:
            ValueError: If weights don't sum to 1.0
        """
        total_weight = strategic_weight + throughput_weight + learning_weight + base_weight
        if not 0.99 <= total_weight <= 1.01:  # Allow small floating point errors
            raise ValueError(
                f"Weights must sum to 1.0, got {total_weight}. "
                f"Weights: strategic={strategic_weight}, throughput={throughput_weight}, "
                f"learning={learning_weight}, base={base_weight}"
            )
        
        self.strategic_weight = strategic_weight
        self.throughput_weight = throughput_weight
        self.learning_weight = learning_weight
        self.base_weight = base_weight
    
    def calculate_strategic_alignment_score(
        self,
        completed_tasks_related_to_primary_mission: int,
        total_tasks: int
    ) -> float:
        """Calculate Strategic Alignment Score.
        
        Measures how well completed tasks align with the primary mission.
        Formula: completed_tasks_related_to_primary_mission / total_tasks
        
        Args:
            completed_tasks_related_to_primary_mission: Number of completed tasks 
                that align with the primary mission
            total_tasks: Total number of tasks
            
        Returns:
            Strategic alignment score between 0.0 and 1.0
            
        Raises:
            ValueError: If total_tasks is negative or if mission tasks exceed total
        """
        if total_tasks < 0:
            raise ValueError("total_tasks must be non-negative")
        if completed_tasks_related_to_primary_mission < 0:
            raise ValueError("completed_tasks_related_to_primary_mission must be non-negative")
        if completed_tasks_related_to_primary_mission > total_tasks:
            raise ValueError(
                "completed_tasks_related_to_primary_mission cannot exceed total_tasks"
            )
        
        if total_tasks == 0:
            return 0.0
        
        return completed_tasks_related_to_primary_mission / total_tasks
    
    def calculate_cognitive_throughput(
        self,
        completed_tasks: int,
        active_focus_hours: float
    ) -> float:
        """Calculate Cognitive Throughput.
        
        Measures the rate of task completion during active focus time.
        Formula: completed_tasks / active_focus_hours
        
        Args:
            completed_tasks: Number of completed tasks
            active_focus_hours: Hours of active focused work
            
        Returns:
            Cognitive throughput (tasks per hour)
            
        Raises:
            ValueError: If any parameter is negative
        """
        if completed_tasks < 0:
            raise ValueError("completed_tasks must be non-negative")
        if active_focus_hours < 0:
            raise ValueError("active_focus_hours must be non-negative")
        
        if active_focus_hours == 0:
            return 0.0
        
        return completed_tasks / active_focus_hours
    
    def calculate_learning_velocity(
        self,
        skill_improvement_delta: float,
        days_elapsed: float
    ) -> float:
        """Calculate Learning Velocity.
        
        Measures the rate of skill improvement over time.
        Formula: skill_improvement_delta / days_elapsed
        
        Args:
            skill_improvement_delta: Change in skill proficiency (can be negative)
            days_elapsed: Number of days in the measurement period
            
        Returns:
            Learning velocity (skill improvement per day)
            
        Raises:
            ValueError: If days_elapsed is not positive
        """
        if days_elapsed <= 0:
            raise ValueError("days_elapsed must be positive")
        
        return skill_improvement_delta / days_elapsed
    
    def calculate_momentum_index(
        self,
        strategic_alignment_score: float,
        cognitive_throughput: float,
        learning_velocity: float,
        completed_tasks: int,
        total_tasks: int,
        max_expected_throughput: float = 2.0
    ) -> float:
        """Calculate Momentum Index.
        
        A weighted combination of metrics that provides an overall performance score.
        The momentum index normalizes and weights different metrics to produce a
        single score between 0.0 and 1.0.
        
        Formula:
            momentum_index = (
                strategic_weight * strategic_alignment_score +
                throughput_weight * normalized_throughput +
                learning_weight * normalized_learning_velocity +
                base_weight * completion_rate
            )
        
        Args:
            strategic_alignment_score: Strategic alignment score (0.0 to 1.0)
            cognitive_throughput: Tasks completed per hour
            learning_velocity: Skill improvement per day
            completed_tasks: Number of completed tasks
            total_tasks: Total number of tasks
            max_expected_throughput: Maximum expected throughput for normalization
            
        Returns:
            Momentum index between 0.0 and 1.0
            
        Raises:
            ValueError: If strategic_alignment_score is out of range
        """
        if not 0.0 <= strategic_alignment_score <= 1.0:
            raise ValueError("strategic_alignment_score must be between 0.0 and 1.0")
        if total_tasks < 0:
            raise ValueError("total_tasks must be non-negative")
        if completed_tasks < 0:
            raise ValueError("completed_tasks must be non-negative")
        if max_expected_throughput <= 0:
            raise ValueError("max_expected_throughput must be positive")
        
        # Normalize cognitive throughput to 0-1 range
        normalized_throughput = min(cognitive_throughput / max_expected_throughput, 1.0)
        
        # Normalize learning velocity to 0-1 range
        # Assume learning velocity of 0.1 (10% improvement per day) is excellent
        normalized_learning_velocity = min(abs(learning_velocity) / 0.1, 1.0)
        # Penalize negative learning (skill decay)
        if learning_velocity < 0:
            normalized_learning_velocity *= 0.5
        
        # Calculate base completion rate
        completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0
        
        # If there are no tasks, momentum is driven only by learning
        # However, if there's no actual work being done, momentum should be minimal
        if total_tasks == 0 and completed_tasks == 0:
            # No tasks means no real momentum, even with learning
            return 0.0
        
        # Calculate weighted momentum index
        momentum_index = (
            self.strategic_weight * strategic_alignment_score +
            self.throughput_weight * normalized_throughput +
            self.learning_weight * normalized_learning_velocity +
            self.base_weight * completion_rate
        )
        
        return min(max(momentum_index, 0.0), 1.0)
    
    def calculate_metrics(
        self,
        total_tasks: int,
        completed_tasks: int,
        completed_tasks_related_to_mission: int,
        active_focus_hours: float,
        skill_improvement_delta: float,
        days_elapsed: float,
        max_expected_throughput: float = 2.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MetricsReport:
        """Calculate all metrics and generate a comprehensive report.
        
        This is the main method for generating a complete metrics report.
        It calculates all individual metrics and combines them into a
        MetricsReport DTO.
        
        Args:
            total_tasks: Total number of tasks in the period
            completed_tasks: Number of completed tasks
            completed_tasks_related_to_mission: Tasks completed that align with mission
            active_focus_hours: Hours of active focused work
            skill_improvement_delta: Change in skill proficiency
            days_elapsed: Number of days in the measurement period
            max_expected_throughput: Maximum expected throughput for normalization
            metadata: Additional contextual information
            
        Returns:
            MetricsReport containing all calculated metrics
            
        Raises:
            ValueError: If any input validation fails
        """
        # Calculate individual metrics
        strategic_alignment_score = self.calculate_strategic_alignment_score(
            completed_tasks_related_to_primary_mission=completed_tasks_related_to_mission,
            total_tasks=total_tasks
        )
        
        cognitive_throughput = self.calculate_cognitive_throughput(
            completed_tasks=completed_tasks,
            active_focus_hours=active_focus_hours
        )
        
        learning_velocity = self.calculate_learning_velocity(
            skill_improvement_delta=skill_improvement_delta,
            days_elapsed=days_elapsed
        )
        
        momentum_index = self.calculate_momentum_index(
            strategic_alignment_score=strategic_alignment_score,
            cognitive_throughput=cognitive_throughput,
            learning_velocity=learning_velocity,
            completed_tasks=completed_tasks,
            total_tasks=total_tasks,
            max_expected_throughput=max_expected_throughput
        )
        
        # Create and return metrics report
        return MetricsReport(
            strategic_alignment_score=strategic_alignment_score,
            cognitive_throughput=cognitive_throughput,
            learning_velocity=learning_velocity,
            momentum_index=momentum_index,
            total_tasks=total_tasks,
            completed_tasks_related_to_mission=completed_tasks_related_to_mission,
            completed_tasks=completed_tasks,
            active_focus_hours=active_focus_hours,
            skill_improvement_delta=skill_improvement_delta,
            days_elapsed=days_elapsed,
            metadata=metadata or {}
        )
