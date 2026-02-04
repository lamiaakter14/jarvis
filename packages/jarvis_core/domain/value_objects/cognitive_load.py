"""Cognitive Load value object for domain entities."""

from dataclasses import dataclass
from jarvis_core.shared.constants import CognitiveLoadLevel
from jarvis_core.shared.exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class CognitiveLoad:
    """Immutable cognitive load value object.
    
    Represents the mental effort required for a task.
    """
    
    level: CognitiveLoadLevel
    estimated_hours: float
    
    def __post_init__(self):
        """Validate cognitive load after initialization."""
        if self.estimated_hours <= 0:
            raise InvalidValueObjectError("Estimated hours must be positive")
        if self.estimated_hours > 8:
            raise InvalidValueObjectError("Estimated hours cannot exceed 8 hours per task")
    
    @classmethod
    def low(cls) -> "CognitiveLoad":
        """Create a low cognitive load (1 hour)."""
        return cls(CognitiveLoadLevel.LOW, 1.0)
    
    @classmethod
    def medium(cls) -> "CognitiveLoad":
        """Create a medium cognitive load (2 hours)."""
        return cls(CognitiveLoadLevel.MEDIUM, 2.0)
    
    @classmethod
    def high(cls) -> "CognitiveLoad":
        """Create a high cognitive load (3 hours)."""
        return cls(CognitiveLoadLevel.HIGH, 3.0)
    
    @classmethod
    def from_string(cls, load_str: str) -> "CognitiveLoad":
        """Create CognitiveLoad from string representation.
        
        Args:
            load_str: String representation of cognitive load level
            
        Returns:
            CognitiveLoad instance
            
        Raises:
            InvalidValueObjectError: If load string is invalid
        """
        load_map = {
            CognitiveLoadLevel.LOW.value: cls.low(),
            CognitiveLoadLevel.MEDIUM.value: cls.medium(),
            CognitiveLoadLevel.HIGH.value: cls.high(),
        }
        
        try:
            return load_map[load_str.lower()]
        except KeyError:
            raise InvalidValueObjectError(
                f"Invalid cognitive load: {load_str}. "
                f"Must be one of: {', '.join(load_map.keys())}"
            )
    
    @classmethod
    def from_hours(cls, hours: float) -> "CognitiveLoad":
        """Create CognitiveLoad from estimated hours.
        
        Args:
            hours: Estimated hours for the task
            
        Returns:
            CognitiveLoad instance with appropriate level
        """
        if hours <= 1.5:
            return cls(CognitiveLoadLevel.LOW, hours)
        elif hours <= 2.5:
            return cls(CognitiveLoadLevel.MEDIUM, hours)
        else:
            return cls(CognitiveLoadLevel.HIGH, hours)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.level.value} ({self.estimated_hours}h)"
    
    def can_fit_in_schedule(self, available_hours: float) -> bool:
        """Check if task can fit in available time.
        
        Args:
            available_hours: Available hours in schedule
            
        Returns:
            True if task fits, False otherwise
        """
        return self.estimated_hours <= available_hours
