"""Innovation created domain event."""

from dataclasses import dataclass, field
from datetime import datetime

from src.domain.events.base_event import BaseEvent
from src.shared.utils import generate_id, current_timestamp


@dataclass(frozen=True)
class InnovationCreatedEvent(BaseEvent):
    """Event raised when a new innovation is created or identified.
    
    Innovations represent novel ideas, process improvements, or creative
    solutions that could benefit the system or user.
    """
    
    innovation_id: str = field(default_factory=lambda: generate_id("inn_"))
    title: str = ""
    category: str = "general"  # general, process, technical, strategic, learning
    impact_score: float = 0.5
    created_by: str = "system"
    timestamp: datetime = field(default_factory=current_timestamp)
    
    def __post_init__(self):
        """Initialize event with proper payload."""
        # Call parent post_init
        super().__post_init__()
        
        # Build payload from innovation data
        payload = {
            "innovation_id": self.innovation_id,
            "title": self.title,
            "category": self.category,
            "impact_score": self.impact_score,
            "created_by": self.created_by,
        }
        
        # Update payload field (workaround for frozen dataclass)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "event_type", "InnovationCreatedEvent")
    
    def get_innovation_id(self) -> str:
        """Get the innovation ID.
        
        Returns:
            Innovation ID
        """
        return self.innovation_id
    
    def is_high_impact(self) -> bool:
        """Check if innovation has high impact (>= 0.7).
        
        Returns:
            True if impact score is high
        """
        return self.impact_score >= 0.7
    
    def is_medium_impact(self) -> bool:
        """Check if innovation has medium impact (0.4 - 0.7).
        
        Returns:
            True if impact score is medium
        """
        return 0.4 <= self.impact_score < 0.7
    
    def is_low_impact(self) -> bool:
        """Check if innovation has low impact (< 0.4).
        
        Returns:
            True if impact score is low
        """
        return self.impact_score < 0.4
    
    def is_technical(self) -> bool:
        """Check if innovation is technical.
        
        Returns:
            True if category is technical
        """
        return self.category == "technical"
    
    def is_process_improvement(self) -> bool:
        """Check if innovation is a process improvement.
        
        Returns:
            True if category is process
        """
        return self.category == "process"
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"InnovationCreatedEvent({self.title}, impact={self.impact_score:.2f})"
