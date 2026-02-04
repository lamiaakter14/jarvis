"""Gap identified domain event."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.domain.events.base_event import BaseEvent
from src.shared.utils import generate_id, current_timestamp


@dataclass(frozen=True)
class GapIdentifiedEvent(BaseEvent):
    """Event raised when a knowledge, skill, or process gap is identified.
    
    Gaps represent areas where improvement or learning is needed.
    This event triggers learning and improvement processes.
    """
    
    gap_id: str = field(default_factory=lambda: generate_id("gap_"))
    description: str = ""
    category: str = "knowledge"  # knowledge, skill, process, tool
    severity: str = "medium"  # low, medium, high, critical
    evidence: List[str] = field(default_factory=list)
    identified_by: str = "system"
    timestamp: datetime = field(default_factory=current_timestamp)
    
    def __post_init__(self):
        """Initialize event with proper payload."""
        # Call parent post_init
        super().__post_init__()
        
        # Build payload from gap data
        payload = {
            "gap_id": self.gap_id,
            "description": self.description,
            "category": self.category,
            "severity": self.severity,
            "evidence": self.evidence,
            "identified_by": self.identified_by,
        }
        
        # Update payload field (workaround for frozen dataclass)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "event_type", "GapIdentifiedEvent")
    
    def get_gap_id(self) -> str:
        """Get the gap ID.
        
        Returns:
            Gap ID
        """
        return self.gap_id
    
    def is_critical(self) -> bool:
        """Check if gap has critical severity.
        
        Returns:
            True if severity is critical
        """
        return self.severity == "critical"
    
    def is_high_severity(self) -> bool:
        """Check if gap has high or critical severity.
        
        Returns:
            True if severity is high or critical
        """
        return self.severity in ["high", "critical"]
    
    def get_evidence_count(self) -> int:
        """Get the number of evidence items.
        
        Returns:
            Count of evidence items
        """
        return len(self.evidence)
    
    def is_knowledge_gap(self) -> bool:
        """Check if this is a knowledge gap.
        
        Returns:
            True if category is knowledge
        """
        return self.category == "knowledge"
    
    def is_skill_gap(self) -> bool:
        """Check if this is a skill gap.
        
        Returns:
            True if category is skill
        """
        return self.category == "skill"
    
    def __str__(self) -> str:
        """String representation of the event."""
        return f"GapIdentifiedEvent({self.category}: {self.description[:50]}...)"
