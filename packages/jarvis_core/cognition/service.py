"""Cognitive service for processing cognitive models and intelligence operations.

This service provides methods to update energy states, compress goals into
actionable plans, and calculate alignment scores.
"""

from datetime import datetime
from typing import Any

from jarvis_core.cognition.models import (
    DecisionProfile,
    EnergyModel,
    IdentityModel,
    SkillGraph,
)


class CognitiveService:
    """Service for cognitive modeling and intelligence operations.

    Provides methods to:
    - Update energy states based on current conditions
    - Compress long-term goals into actionable daily plans
    - Calculate alignment scores between decision profiles and skill graphs
    """

    def __init__(self):
        """Initialize the cognitive service."""
        self._energy_state: dict[str, Any] = {}
        self._goal_cache: dict[str, Any] = {}

    def update_energy(self, energy_model: EnergyModel) -> dict[str, Any]:
        """Update energy attributes based on the provided energy model.

        Args:
            energy_model: The energy model to process

        Returns:
            Dictionary containing updated energy attributes and recommendations
        """
        # Calculate adjusted energy score based on sleep and cognitive load
        adjusted_energy = energy_model.energy_score * (
            1.0 - (energy_model.cognitive_load * 0.5)
        )

        # Determine optimal focus window based on energy
        optimal_focus_hours = energy_model.focus_window_hours * adjusted_energy

        # Store updated state
        self._energy_state = {
            "sleep_hours": energy_model.sleep_hours,
            "energy_score": energy_model.energy_score,
            "adjusted_energy_score": adjusted_energy,
            "cognitive_load": energy_model.cognitive_load,
            "focus_window_hours": energy_model.focus_window_hours,
            "optimal_focus_hours": optimal_focus_hours,
            "timestamp": datetime.now().isoformat(),
        }

        # Generate recommendations
        recommendations = []
        if adjusted_energy < 0.5:
            recommendations.append("Consider taking a break to restore energy")
        if energy_model.cognitive_load > 0.7:
            recommendations.append("Cognitive load is high, prioritize simpler tasks")
        if energy_model.sleep_hours < 7.0:
            recommendations.append("Insufficient sleep detected, plan for more rest")

        return {
            **self._energy_state,
            "recommendations": recommendations,
        }

    def compress_goal_to_daily_plan(
        self, identity_model: IdentityModel
    ) -> dict[str, Any]:
        """Convert long-term goals into actionable daily plans.

        Args:
            identity_model: The identity model containing strategic goals

        Returns:
            Dictionary containing daily action items derived from long-term goals
        """
        daily_plan = {
            "date": datetime.now().date().isoformat(),
            "primary_focus": identity_model.current_primary_mission,
            "action_items": [],
            "strategic_context": {},
        }

        # Extract action items from current primary mission
        if identity_model.current_primary_mission:
            daily_plan["action_items"].append({
                "title": f"Advance: {identity_model.current_primary_mission}",
                "priority": "high",
                "category": "primary_mission",
            })

        # Add strategic context for alignment
        daily_plan["strategic_context"] = {
            "one_year_target": identity_model.one_year_target,
            "three_year_target": identity_model.three_year_target,
            "long_term_vision": identity_model.long_term_vision,
            "risk_tolerance": identity_model.risk_tolerance,
            "ambition_level": identity_model.ambition_level,
        }

        # Add progressive steps based on targets
        if identity_model.one_year_target:
            daily_plan["action_items"].append({
                "title": f"One-year progress: {identity_model.one_year_target}",
                "priority": "medium",
                "category": "one_year_target",
            })

        if identity_model.three_year_target:
            daily_plan["action_items"].append({
                "title": f"Three-year alignment: {identity_model.three_year_target}",
                "priority": "low",
                "category": "three_year_target",
            })

        # Cache the plan
        self._goal_cache[datetime.now().date().isoformat()] = daily_plan

        return daily_plan

    def calculate_alignment_score(
        self, decision_profile: DecisionProfile, skill_graph: SkillGraph
    ) -> dict[str, Any]:
        """Calculate alignment scores based on decision profiles and skill graphs.

        Args:
            decision_profile: The decision-making profile
            skill_graph: The skill graph to evaluate

        Returns:
            Dictionary containing alignment scores and analysis
        """
        # Calculate base alignment considering proficiency and priority
        base_alignment = (
            skill_graph.proficiency_level * 0.6 +
            skill_graph.priority_weight * 0.4
        )

        # Adjust for decision profile characteristics
        # Higher accuracy bias benefits higher proficiency
        accuracy_adjustment = (
            decision_profile.accuracy_bias * skill_graph.proficiency_level * 0.2
        )

        # Higher speed bias reduces the weight of proficiency
        speed_penalty = (
            decision_profile.speed_bias * (1.0 - skill_graph.proficiency_level) * 0.1
        )

        # Calculate final alignment score
        alignment_score = base_alignment + accuracy_adjustment - speed_penalty
        alignment_score = max(0.0, min(1.0, alignment_score))

        # Determine if skill needs practice based on last practiced
        needs_practice = False
        days_since_practice = None
        if skill_graph.last_practiced:
            days_since_practice = (
                datetime.now() - skill_graph.last_practiced
            ).days
            needs_practice = days_since_practice > decision_profile.strategic_horizon_days

        return {
            "skill_name": skill_graph.skill_name,
            "alignment_score": alignment_score,
            "base_alignment": base_alignment,
            "proficiency_level": skill_graph.proficiency_level,
            "priority_weight": skill_graph.priority_weight,
            "needs_practice": needs_practice,
            "days_since_practice": days_since_practice,
            "decision_context": {
                "speed_bias": decision_profile.speed_bias,
                "accuracy_bias": decision_profile.accuracy_bias,
                "strategic_horizon_days": decision_profile.strategic_horizon_days,
            },
            "recommendation": self._generate_skill_recommendation(
                alignment_score, needs_practice, skill_graph.proficiency_level
            ),
        }

    def _generate_skill_recommendation(
        self, alignment_score: float, needs_practice: bool, proficiency: float
    ) -> str:
        """Generate a recommendation based on skill analysis.

        Args:
            alignment_score: The calculated alignment score
            needs_practice: Whether the skill needs practice
            proficiency: Current proficiency level

        Returns:
            Recommendation string
        """
        if needs_practice:
            return "Skill requires practice to maintain proficiency"
        elif alignment_score < 0.4:
            return "Low alignment - consider deprioritizing or improving proficiency"
        elif alignment_score < 0.7:
            if proficiency < 0.5:
                return "Moderate alignment - focus on building proficiency"
            else:
                return "Moderate alignment - maintain current practice level"
        else:
            return "High alignment - skill is well-positioned for current goals"
