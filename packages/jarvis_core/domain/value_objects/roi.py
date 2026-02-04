"""ROI (Return on Investment) value object for domain entities."""

from dataclasses import dataclass
from jarvis_core.shared.exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class ROI:
    """Immutable ROI (Return on Investment) value object.
    
    Represents the expected return on investment for a task or learning activity.
    Value ranges from 0.0 (no return) to 1.0 (maximum return).
    """
    
    value: float
    
    def __post_init__(self):
        """Validate ROI after initialization."""
        if self.value < 0.0 or self.value > 1.0:
            raise InvalidValueObjectError("ROI value must be between 0.0 and 1.0")
    
    @classmethod
    def calculate(
        cls,
        impact_score: float,
        urgency_score: float,
        effort_hours: float,
        max_effort_hours: float = 8.0
    ) -> "ROI":
        """Calculate ROI from impact, urgency, and effort.
        
        Args:
            impact_score: Expected impact (0.0 to 1.0)
            urgency_score: Urgency level (0.0 to 1.0)
            effort_hours: Estimated effort in hours
            max_effort_hours: Maximum hours for normalization (default 8)
            
        Returns:
            Calculated ROI instance
            
        Raises:
            InvalidValueObjectError: If input values are invalid
        """
        if not (0.0 <= impact_score <= 1.0):
            raise InvalidValueObjectError("Impact score must be between 0.0 and 1.0")
        if not (0.0 <= urgency_score <= 1.0):
            raise InvalidValueObjectError("Urgency score must be between 0.0 and 1.0")
        if effort_hours <= 0:
            raise InvalidValueObjectError("Effort hours must be positive")
        
        # Normalize effort (inverse - less effort is better)
        normalized_effort = 1.0 - min(effort_hours / max_effort_hours, 1.0)
        
        # Calculate weighted ROI
        # Impact: 50%, Urgency: 30%, Effort efficiency: 20%
        roi_value = (impact_score * 0.5) + (urgency_score * 0.3) + (normalized_effort * 0.2)
        
        return cls(roi_value)
    
    @classmethod
    def from_gap_severity(cls, evidence_count: int) -> "ROI":
        """Calculate ROI from knowledge gap severity.
        
        Args:
            evidence_count: Number of evidence items for the gap
            
        Returns:
            ROI instance based on gap severity
        """
        # More evidence = higher severity = higher ROI
        severity_score = min(evidence_count / 5.0, 1.0)  # Cap at 5 evidence items
        # High urgency for knowledge gaps
        urgency_score = 0.8
        # Assume medium effort for learning
        effort_hours = 2.0
        
        return cls.calculate(severity_score, urgency_score, effort_hours)
    
    @classmethod
    def from_milestone(cls, days_until_due: int) -> "ROI":
        """Calculate ROI from milestone proximity.
        
        Args:
            days_until_due: Days remaining until milestone is due
            
        Returns:
            ROI instance based on deadline proximity
        """
        # Higher urgency for closer deadlines
        if days_until_due <= 0:
            urgency_score = 1.0
        elif days_until_due <= 7:
            urgency_score = 0.9
        elif days_until_due <= 30:
            urgency_score = 0.7
        else:
            urgency_score = 0.5
        
        # Assume high impact for milestones
        impact_score = 0.8
        # Assume high effort
        effort_hours = 3.0
        
        return cls.calculate(impact_score, urgency_score, effort_hours)
    
    def __str__(self) -> str:
        """String representation."""
        percentage = self.value * 100
        return f"{percentage:.1f}%"
    
    def __lt__(self, other: "ROI") -> bool:
        """Compare ROIs by value."""
        if not isinstance(other, ROI):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other: "ROI") -> bool:
        """Compare ROIs by value."""
        if not isinstance(other, ROI):
            return NotImplemented
        return self.value <= other.value
    
    def __gt__(self, other: "ROI") -> bool:
        """Compare ROIs by value."""
        if not isinstance(other, ROI):
            return NotImplemented
        return self.value > other.value
    
    def __ge__(self, other: "ROI") -> bool:
        """Compare ROIs by value."""
        if not isinstance(other, ROI):
            return NotImplemented
        return self.value >= other.value
    
    def is_high_value(self) -> bool:
        """Check if ROI is high value (>= 0.7)."""
        return self.value >= 0.7
    
    def is_medium_value(self) -> bool:
        """Check if ROI is medium value ([0.4, 0.7))."""
        return 0.4 <= self.value < 0.7
    
    def is_low_value(self) -> bool:
        """Check if ROI is low value (< 0.4)."""
        return self.value < 0.4
