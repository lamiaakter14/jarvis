"""Cognitive Context for orchestrator.

This module defines the CognitiveContext that combines cognitive models
and provides context for the orchestrator to execute the cognitive loop.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

from jarvis_core.cognition.models import (
    DecisionProfile,
    EnergyModel,
    IdentityModel,
    SkillGraph,
)
from jarvis_core.domain.entities.context import Context
from jarvis_core.shared.utils import current_date


@dataclass
class CognitiveProfile:
    """Cognitive Profile combining all cognitive models.

    This represents the complete cognitive state of the system,
    including identity, energy, skills, and decision-making preferences.

    Attributes:
        identity: Identity model with strategic direction
        energy: Energy model with current capacity
        skills: List of skill graphs for tracked skills
        decision: Decision profile for decision-making preferences
    """

    identity: IdentityModel = field(default_factory=IdentityModel)
    energy: EnergyModel = field(default_factory=EnergyModel)
    skills: List[SkillGraph] = field(default_factory=list)
    decision: DecisionProfile = field(default_factory=DecisionProfile)

    def to_dict(self) -> Dict[str, Any]:
        """Convert cognitive profile to dictionary.

        Returns:
            Dictionary representation of the cognitive profile
        """
        return {
            "identity": {
                "long_term_vision": self.identity.long_term_vision,
                "three_year_target": self.identity.three_year_target,
                "one_year_target": self.identity.one_year_target,
                "current_primary_mission": self.identity.current_primary_mission,
                "risk_tolerance": self.identity.risk_tolerance,
                "ambition_level": self.identity.ambition_level,
            },
            "energy": {
                "sleep_hours": self.energy.sleep_hours,
                "energy_score": self.energy.energy_score,
                "focus_window_hours": self.energy.focus_window_hours,
                "cognitive_load": self.energy.cognitive_load,
            },
            "skills": [
                {
                    "skill_name": skill.skill_name,
                    "proficiency_level": skill.proficiency_level,
                    "priority_weight": skill.priority_weight,
                    "last_practiced": (
                        skill.last_practiced.isoformat() if skill.last_practiced else None
                    ),
                }
                for skill in self.skills
            ],
            "decision": {
                "speed_bias": self.decision.speed_bias,
                "accuracy_bias": self.decision.accuracy_bias,
                "strategic_horizon_days": self.decision.strategic_horizon_days,
            },
        }


@dataclass
class CognitiveContext:
    """Enhanced context for cognitive loop execution.

    Combines the base Context with CognitiveProfile and additional
    orchestration metadata.

    Attributes:
        context: Base execution context
        profile: Cognitive profile with models
        metadata: Additional metadata for orchestration
    """

    context: Context = field(default_factory=Context)
    profile: CognitiveProfile = field(default_factory=CognitiveProfile)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create_default(cls, execution_date: Optional[date] = None) -> "CognitiveContext":
        """Create a default cognitive context.

        Args:
            execution_date: Date for execution context, defaults to today

        Returns:
            New CognitiveContext with default values
        """
        exec_date = execution_date or current_date()

        return cls(
            context=Context(date=exec_date),
            profile=CognitiveProfile(),
            metadata={
                "created_at": current_date().isoformat(),
                "version": "2.0",
            },
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert cognitive context to dictionary.

        Returns:
            Dictionary representation of the cognitive context
        """
        return {
            "context": self.context.get_summary(),
            "profile": self.profile.to_dict(),
            "metadata": self.metadata,
        }
