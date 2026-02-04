"""Agent Type value object for domain entities."""

from dataclasses import dataclass
from jarvis_core.shared.constants import AgentType as AgentTypeEnum
from jarvis_core.shared.exceptions import InvalidValueObjectError


@dataclass(frozen=True)
class AgentType:
    """Immutable agent type value object.
    
    Represents the type and capabilities of an agent in the system.
    """
    
    type: AgentTypeEnum
    description: str
    
    @classmethod
    def strategist(cls) -> "AgentType":
        """Create strategist agent type."""
        return cls(
            AgentTypeEnum.STRATEGIST,
            "Plans and organizes tasks, breaks down complex problems"
        )
    
    @classmethod
    def mentor(cls) -> "AgentType":
        """Create mentor agent type."""
        return cls(
            AgentTypeEnum.MENTOR,
            "Provides guidance, feedback, and identifies knowledge gaps"
        )
    
    @classmethod
    def executor(cls) -> "AgentType":
        """Create executor agent type."""
        return cls(
            AgentTypeEnum.EXECUTOR,
            "Executes tasks and manages implementation"
        )
    
    @classmethod
    def innovator(cls) -> "AgentType":
        """Create innovator agent type."""
        return cls(
            AgentTypeEnum.INNOVATOR,
            "Generates creative solutions and innovative approaches"
        )
    
    @classmethod
    def amplifier(cls) -> "AgentType":
        """Create amplifier agent type."""
        return cls(
            AgentTypeEnum.AMPLIFIER,
            "Analyzes performance and optimizes effectiveness"
        )
    
    @classmethod
    def from_string(cls, type_str: str) -> "AgentType":
        """Create AgentType from string representation.
        
        Args:
            type_str: String representation of agent type
            
        Returns:
            AgentType instance
            
        Raises:
            InvalidValueObjectError: If type string is invalid
        """
        type_map = {
            AgentTypeEnum.STRATEGIST.value: cls.strategist(),
            AgentTypeEnum.MENTOR.value: cls.mentor(),
            AgentTypeEnum.EXECUTOR.value: cls.executor(),
            AgentTypeEnum.INNOVATOR.value: cls.innovator(),
            AgentTypeEnum.AMPLIFIER.value: cls.amplifier(),
        }
        
        try:
            return type_map[type_str.lower()]
        except KeyError:
            raise InvalidValueObjectError(
                f"Invalid agent type: {type_str}. "
                f"Must be one of: {', '.join(type_map.keys())}"
            )
    
    def __str__(self) -> str:
        """String representation."""
        return self.type.value
    
    def __eq__(self, other: object) -> bool:
        """Check equality by agent type."""
        if not isinstance(other, AgentType):
            return NotImplemented
        return self.type == other.type
    
    def __hash__(self) -> int:
        """Hash based on agent type."""
        return hash(self.type)
