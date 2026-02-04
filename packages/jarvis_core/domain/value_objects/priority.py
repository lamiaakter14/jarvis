"""Priority value object for domain entities."""

from enum import Enum


class Priority(str, Enum):
    """Immutable priority value object.
    
    Represents task priority levels as enum values.
    """
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    def __lt__(self, other):
        """Compare priorities by order."""
        if not isinstance(other, Priority):
            return NotImplemented
        order = {Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 3, Priority.CRITICAL: 4}
        return order[self] < order[other]
    
    def __gt__(self, other):
        """Compare priorities by order."""
        if not isinstance(other, Priority):
            return NotImplemented
        order = {Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 3, Priority.CRITICAL: 4}
        return order[self] > order[other]
    
    def __le__(self, other):
        """Compare priorities by order."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self < other or self == other
    
    def __ge__(self, other):
        """Compare priorities by order."""
        if not isinstance(other, Priority):
            return NotImplemented
        return self > other or self == other
