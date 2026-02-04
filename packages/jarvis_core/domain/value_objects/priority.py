"""Priority value object for domain entities."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from jarvis_core.shared.constants import TaskPriority
from jarvis_core.shared.exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class Priority:
    """Immutable priority value object.
    
    Represents task priority with associated weight for calculations.
    """
    
    level: TaskPriority
    weight: float
    
    def __post_init__(self):
        """Validate priority after initialization."""
        if self.weight < 0 or self.weight > 1:
            raise InvalidValueObjectError("Priority weight must be between 0 and 1")
    
    @classmethod
    def low(cls) -> "Priority":
        """Create a low priority."""
        return cls(TaskPriority.LOW, 0.25)
    
    @classmethod
    def medium(cls) -> "Priority":
        """Create a medium priority."""
        return cls(TaskPriority.MEDIUM, 0.50)
    
    @classmethod
    def high(cls) -> "Priority":
        """Create a high priority."""
        return cls(TaskPriority.HIGH, 0.75)
    
    @classmethod
    def critical(cls) -> "Priority":
        """Create a critical priority."""
        return cls(TaskPriority.CRITICAL, 1.0)
    
    @classmethod
    def from_string(cls, priority_str: str) -> "Priority":
        """Create Priority from string representation.
        
        Args:
            priority_str: String representation of priority level
            
        Returns:
            Priority instance
            
        Raises:
            InvalidValueObjectError: If priority string is invalid
        """
        priority_map = {
            TaskPriority.LOW.value: cls.low(),
            TaskPriority.MEDIUM.value: cls.medium(),
            TaskPriority.HIGH.value: cls.high(),
            TaskPriority.CRITICAL.value: cls.critical(),
        }
        
        try:
            return priority_map[priority_str.lower()]
        except KeyError:
            raise InvalidValueObjectError(
                f"Invalid priority: {priority_str}. "
                f"Must be one of: {', '.join(priority_map.keys())}"
            )
    
    def __str__(self) -> str:
        """String representation."""
        return self.level.value
    
    def __lt__(self, other: "Priority") -> bool:
        """Compare priorities by weight."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.weight < other.weight
    
    def __le__(self, other: "Priority") -> bool:
        """Compare priorities by weight."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.weight <= other.weight
    
    def __gt__(self, other: "Priority") -> bool:
        """Compare priorities by weight."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.weight > other.weight
    
    def __ge__(self, other: "Priority") -> bool:
        """Compare priorities by weight."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self.weight >= other.weight
