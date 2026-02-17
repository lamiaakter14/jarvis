"""Cognitive models for the JARVIS system.

This module defines the foundational cognitive models that represent
the system's identity, energy state, skills, and decision-making profile.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class IdentityModel:
    """Model representing the system's identity and strategic direction.

    Attributes:
        long_term_vision: The overarching vision for the long-term future
        three_year_target: Strategic target for the next three years
        one_year_target: Strategic target for the next year
        current_primary_mission: The current primary mission or objective
        risk_tolerance: Level of risk tolerance (0.0 to 1.0)
        ambition_level: Level of ambition (0.0 to 1.0)
    """

    long_term_vision: str = ""
    three_year_target: str = ""
    one_year_target: str = ""
    current_primary_mission: str = ""
    risk_tolerance: float = 0.5
    ambition_level: float = 0.5

    def __post_init__(self):
        """Validate identity model after initialization."""
        if not 0.0 <= self.risk_tolerance <= 1.0:
            raise ValueError("risk_tolerance must be between 0.0 and 1.0")
        if not 0.0 <= self.ambition_level <= 1.0:
            raise ValueError("ambition_level must be between 0.0 and 1.0")


@dataclass
class EnergyModel:
    """Model representing the system's energy and cognitive capacity.

    Attributes:
        sleep_hours: Hours of sleep or rest time
        energy_score: Current energy level (0.0 to 1.0)
        focus_window_hours: Available hours for focused work
        cognitive_load: Current cognitive load (0.0 to 1.0)
    """

    sleep_hours: float = 8.0
    energy_score: float = 1.0
    focus_window_hours: float = 8.0
    cognitive_load: float = 0.0

    def __post_init__(self):
        """Validate energy model after initialization."""
        if self.sleep_hours < 0:
            raise ValueError("sleep_hours must be non-negative")
        if not 0.0 <= self.energy_score <= 1.0:
            raise ValueError("energy_score must be between 0.0 and 1.0")
        if self.focus_window_hours < 0:
            raise ValueError("focus_window_hours must be non-negative")
        if not 0.0 <= self.cognitive_load <= 1.0:
            raise ValueError("cognitive_load must be between 0.0 and 1.0")


@dataclass
class SkillGraph:
    """Model representing a skill and its attributes.

    Attributes:
        skill_name: Name of the skill (required)
        proficiency_level: Level of proficiency (0.0 to 1.0)
        last_practiced: Timestamp of last practice
        priority_weight: Priority weight for the skill (0.0 to 1.0)
    """

    skill_name: str
    proficiency_level: float = 0.0
    last_practiced: Optional[datetime] = None
    priority_weight: float = 0.5

    def __post_init__(self):
        """Validate skill graph after initialization."""
        if not 0.0 <= self.proficiency_level <= 1.0:
            raise ValueError("proficiency_level must be between 0.0 and 1.0")
        if not 0.0 <= self.priority_weight <= 1.0:
            raise ValueError("priority_weight must be between 0.0 and 1.0")


@dataclass
class DecisionProfile:
    """Model representing decision-making preferences and horizons.

    Attributes:
        speed_bias: Preference for speed in decision-making (0.0 to 1.0)
        accuracy_bias: Preference for accuracy in decision-making (0.0 to 1.0)
        strategic_horizon_days: Strategic planning horizon in days
    """

    speed_bias: float = 0.5
    accuracy_bias: float = 0.5
    strategic_horizon_days: int = 30

    def __post_init__(self):
        """Validate decision profile after initialization."""
        if not 0.0 <= self.speed_bias <= 1.0:
            raise ValueError("speed_bias must be between 0.0 and 1.0")
        if not 0.0 <= self.accuracy_bias <= 1.0:
            raise ValueError("accuracy_bias must be between 0.0 and 1.0")
        if self.strategic_horizon_days < 0:
            raise ValueError("strategic_horizon_days must be non-negative")
