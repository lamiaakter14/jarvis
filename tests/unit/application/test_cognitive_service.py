"""Tests for cognitive service."""

from datetime import datetime, timedelta

import pytest
from jarvis_core.cognition.models import (
    DecisionProfile,
    EnergyModel,
    IdentityModel,
    SkillGraph,
)
from jarvis_core.cognition.service import CognitiveService


@pytest.mark.unit
class TestCognitiveService:
    """Unit tests for CognitiveService."""

    @pytest.fixture
    def service(self):
        """Create cognitive service instance."""
        return CognitiveService()

    def test_update_energy_with_high_energy(self, service):
        """Test updating energy with high energy state."""
        energy_model = EnergyModel(
            sleep_hours=8.0,
            energy_score=0.9,
            focus_window_hours=8.0,
            cognitive_load=0.2,
        )

        result = service.update_energy(energy_model)

        assert result["sleep_hours"] == 8.0
        assert result["energy_score"] == 0.9
        assert "adjusted_energy_score" in result
        assert result["adjusted_energy_score"] > 0.8  # High energy after adjustment
        assert result["cognitive_load"] == 0.2
        assert result["focus_window_hours"] == 8.0
        assert "optimal_focus_hours" in result
        assert "timestamp" in result
        assert "recommendations" in result

    def test_update_energy_with_low_energy(self, service):
        """Test updating energy with low energy state."""
        energy_model = EnergyModel(
            sleep_hours=5.0,
            energy_score=0.4,
            focus_window_hours=6.0,
            cognitive_load=0.8,
        )

        result = service.update_energy(energy_model)

        assert result["sleep_hours"] == 5.0
        assert result["energy_score"] == 0.4
        assert "adjusted_energy_score" in result
        assert result["adjusted_energy_score"] < 0.4  # Lower after load adjustment
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0

        # Check for specific recommendations
        recommendations_text = " ".join(result["recommendations"])
        assert "break" in recommendations_text.lower() or "energy" in recommendations_text.lower()

    def test_update_energy_generates_recommendations_for_high_cognitive_load(self, service):
        """Test that high cognitive load generates recommendations."""
        energy_model = EnergyModel(
            sleep_hours=8.0,
            energy_score=0.8,
            focus_window_hours=8.0,
            cognitive_load=0.9,
        )

        result = service.update_energy(energy_model)

        assert len(result["recommendations"]) > 0
        recommendations_text = " ".join(result["recommendations"])
        assert "cognitive" in recommendations_text.lower()

    def test_update_energy_generates_recommendations_for_low_sleep(self, service):
        """Test that low sleep generates recommendations."""
        energy_model = EnergyModel(
            sleep_hours=5.0,
            energy_score=0.7,
            focus_window_hours=6.0,
            cognitive_load=0.3,
        )

        result = service.update_energy(energy_model)

        assert len(result["recommendations"]) > 0
        recommendations_text = " ".join(result["recommendations"])
        assert "sleep" in recommendations_text.lower()

    def test_compress_goal_to_daily_plan_with_full_identity(self, service):
        """Test compressing goals to daily plan with complete identity model."""
        identity_model = IdentityModel(
            long_term_vision="Build world-class AI systems",
            three_year_target="Launch AI product suite",
            one_year_target="Complete core platform",
            current_primary_mission="Develop cognitive layer",
            risk_tolerance=0.7,
            ambition_level=0.9,
        )

        result = service.compress_goal_to_daily_plan(identity_model)

        assert "date" in result
        assert result["primary_focus"] == "Develop cognitive layer"
        assert "action_items" in result
        assert len(result["action_items"]) >= 1
        assert "strategic_context" in result

        # Check strategic context
        assert result["strategic_context"]["one_year_target"] == "Complete core platform"
        assert result["strategic_context"]["three_year_target"] == "Launch AI product suite"
        assert result["strategic_context"]["long_term_vision"] == "Build world-class AI systems"
        assert result["strategic_context"]["risk_tolerance"] == 0.7
        assert result["strategic_context"]["ambition_level"] == 0.9

        # Check action items
        action_titles = [item["title"] for item in result["action_items"]]
        assert any("Develop cognitive layer" in title for title in action_titles)

    def test_compress_goal_to_daily_plan_with_minimal_identity(self, service):
        """Test compressing goals with minimal identity model."""
        identity_model = IdentityModel(
            current_primary_mission="Focus on testing",
        )

        result = service.compress_goal_to_daily_plan(identity_model)

        assert "date" in result
        assert result["primary_focus"] == "Focus on testing"
        assert "action_items" in result
        assert len(result["action_items"]) >= 1
        assert "strategic_context" in result

    def test_compress_goal_to_daily_plan_creates_action_items(self, service):
        """Test that daily plan includes action items for each target level."""
        identity_model = IdentityModel(
            long_term_vision="Long-term vision",
            three_year_target="Three-year target",
            one_year_target="One-year target",
            current_primary_mission="Current mission",
        )

        result = service.compress_goal_to_daily_plan(identity_model)

        assert len(result["action_items"]) >= 1

        # Check for different priority levels
        priorities = [item["priority"] for item in result["action_items"]]
        assert "high" in priorities or "medium" in priorities or "low" in priorities

    def test_calculate_alignment_score_high_proficiency_high_priority(self, service):
        """Test alignment calculation with high proficiency and priority."""
        decision_profile = DecisionProfile(
            speed_bias=0.3,
            accuracy_bias=0.8,
            strategic_horizon_days=30,
        )
        skill_graph = SkillGraph(
            skill_name="Python",
            proficiency_level=0.9,
            last_practiced=datetime.now() - timedelta(days=5),
            priority_weight=0.9,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["skill_name"] == "Python"
        assert "alignment_score" in result
        assert result["alignment_score"] > 0.7  # High proficiency + high priority
        assert result["proficiency_level"] == 0.9
        assert result["priority_weight"] == 0.9
        assert result["needs_practice"] is False
        assert result["days_since_practice"] == 5
        assert "recommendation" in result

    def test_calculate_alignment_score_low_proficiency(self, service):
        """Test alignment calculation with low proficiency."""
        decision_profile = DecisionProfile(
            speed_bias=0.5,
            accuracy_bias=0.5,
            strategic_horizon_days=30,
        )
        skill_graph = SkillGraph(
            skill_name="Rust",
            proficiency_level=0.2,
            last_practiced=datetime.now() - timedelta(days=10),
            priority_weight=0.3,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["skill_name"] == "Rust"
        assert result["alignment_score"] < 0.5  # Low proficiency + low priority
        assert result["needs_practice"] is False
        assert "recommendation" in result

    def test_calculate_alignment_score_needs_practice(self, service):
        """Test alignment calculation when skill needs practice."""
        decision_profile = DecisionProfile(
            speed_bias=0.5,
            accuracy_bias=0.5,
            strategic_horizon_days=30,
        )
        skill_graph = SkillGraph(
            skill_name="Java",
            proficiency_level=0.7,
            last_practiced=datetime.now() - timedelta(days=45),
            priority_weight=0.6,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["skill_name"] == "Java"
        assert result["needs_practice"] is True
        assert result["days_since_practice"] == 45
        assert "practice" in result["recommendation"].lower()

    def test_calculate_alignment_score_never_practiced(self, service):
        """Test alignment calculation when skill has never been practiced."""
        decision_profile = DecisionProfile(
            speed_bias=0.5,
            accuracy_bias=0.5,
            strategic_horizon_days=30,
        )
        skill_graph = SkillGraph(
            skill_name="Go",
            proficiency_level=0.1,
            last_practiced=None,
            priority_weight=0.5,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["skill_name"] == "Go"
        assert result["needs_practice"] is False
        assert result["days_since_practice"] is None
        assert "recommendation" in result

    def test_calculate_alignment_score_includes_decision_context(self, service):
        """Test that alignment result includes decision context."""
        decision_profile = DecisionProfile(
            speed_bias=0.6,
            accuracy_bias=0.7,
            strategic_horizon_days=45,
        )
        skill_graph = SkillGraph(
            skill_name="TypeScript",
            proficiency_level=0.8,
            last_practiced=datetime.now(),
            priority_weight=0.8,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert "decision_context" in result
        assert result["decision_context"]["speed_bias"] == 0.6
        assert result["decision_context"]["accuracy_bias"] == 0.7
        assert result["decision_context"]["strategic_horizon_days"] == 45

    def test_calculate_alignment_score_recommendation_for_low_alignment(self, service):
        """Test recommendation generation for low alignment."""
        decision_profile = DecisionProfile()
        skill_graph = SkillGraph(
            skill_name="Skill1",
            proficiency_level=0.2,
            priority_weight=0.2,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["alignment_score"] < 0.4
        assert "deprioritizing" in result["recommendation"].lower() or "low" in result["recommendation"].lower()

    def test_calculate_alignment_score_recommendation_for_high_alignment(self, service):
        """Test recommendation generation for high alignment."""
        decision_profile = DecisionProfile(accuracy_bias=0.9)
        skill_graph = SkillGraph(
            skill_name="Skill2",
            proficiency_level=0.9,
            priority_weight=0.9,
        )

        result = service.calculate_alignment_score(decision_profile, skill_graph)

        assert result["alignment_score"] >= 0.7
        assert "high" in result["recommendation"].lower() or "well-positioned" in result["recommendation"].lower()
