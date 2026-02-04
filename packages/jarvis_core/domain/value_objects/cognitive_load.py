"""Cognitive Load value object for domain entities."""

from enum import Enum


class CognitiveLoad(str, Enum):
    """Immutable cognitive load value object.
    
    Represents the mental effort required for a task.
    """
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    @property
    def estimated_hours(self) -> float:
        """Get default estimated hours for this cognitive load level."""
        hours_map = {
            CognitiveLoad.LOW: 1.0,
            CognitiveLoad.MEDIUM: 2.0,
            CognitiveLoad.HIGH: 3.0
        }
        return hours_map[self]
    
    def __lt__(self, other):
        """Compare cognitive loads by order."""
        if not isinstance(other, CognitiveLoad):
            return NotImplemented
        order = {CognitiveLoad.LOW: 1, CognitiveLoad.MEDIUM: 2, CognitiveLoad.HIGH: 3}
        return order[self] < order[other]
    
    def __gt__(self, other):
        """Compare cognitive loads by order."""
        if not isinstance(other, CognitiveLoad):
            return NotImplemented
        order = {CognitiveLoad.LOW: 1, CognitiveLoad.MEDIUM: 2, CognitiveLoad.HIGH: 3}
        return order[self] > order[other]
    
    def __le__(self, other):
        """Compare cognitive loads by order."""
        if not isinstance(other, CognitiveLoad):
            return NotImplemented
        return self < other or self == other
    
    def __ge__(self, other):
        """Compare cognitive loads by order."""
        if not isinstance(other, CognitiveLoad):
            return NotImplemented
        return self > other or self == other
