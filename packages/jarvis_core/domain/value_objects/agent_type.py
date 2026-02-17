"""Agent Type value object for domain entities."""

from enum import Enum


class AgentType(str, Enum):
    """Immutable agent type value object.

    Represents the type and capabilities of an agent in the system.
    """

    STRATEGIST = "strategist"
    MENTOR = "mentor"
    EXECUTOR = "executor"
    AMPLIFIER = "amplifier"
    INNOVATOR = "innovator"
    REFLECTOR = "reflector"
