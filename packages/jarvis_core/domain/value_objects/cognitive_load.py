"""Cognitive Load value object for domain entities."""

from enum import Enum


class CognitiveLoad(str, Enum):
    """Immutable cognitive load value object.
    
    Represents the mental effort required for a task.
    """
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
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
