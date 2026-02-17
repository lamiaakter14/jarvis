"""Tests for cognitive models."""

from datetime import datetime

import pytest
from jarvis_core.cognition.models import (
    DecisionProfile,
    EnergyModel,
    IdentityModel,
    SkillGraph,
)


@pytest.mark.unit
class TestIdentityModel:
    """Unit tests for IdentityModel."""

    def test_create_identity_model_with_defaults(self):
        """Test creating an identity model with default values."""
        model = IdentityModel()

        assert model.long_term_vision == ""
        assert model.three_year_target == ""
        assert model.one_year_target == ""
        assert model.current_primary_mission == ""
        assert model.risk_tolerance == 0.5
        assert model.ambition_level == 0.5

    def test_create_identity_model_with_custom_values(self):
        """Test creating an identity model with custom values."""
        model = IdentityModel(
            long_term_vision="Build AI systems",
            three_year_target="Launch product",
            one_year_target="Complete MVP",
            current_primary_mission="Develop core features",
            risk_tolerance=0.7,
            ambition_level=0.9,
        )

        assert model.long_term_vision == "Build AI systems"
        assert model.three_year_target == "Launch product"
        assert model.one_year_target == "Complete MVP"
        assert model.current_primary_mission == "Develop core features"
        assert model.risk_tolerance == 0.7
        assert model.ambition_level == 0.9

    def test_validate_risk_tolerance_range(self):
        """Test that risk_tolerance must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="risk_tolerance must be between 0.0 and 1.0"):
            IdentityModel(risk_tolerance=1.5)

        with pytest.raises(ValueError, match="risk_tolerance must be between 0.0 and 1.0"):
            IdentityModel(risk_tolerance=-0.1)

    def test_validate_ambition_level_range(self):
        """Test that ambition_level must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="ambition_level must be between 0.0 and 1.0"):
            IdentityModel(ambition_level=1.5)

        with pytest.raises(ValueError, match="ambition_level must be between 0.0 and 1.0"):
            IdentityModel(ambition_level=-0.1)


@pytest.mark.unit
class TestEnergyModel:
    """Unit tests for EnergyModel."""

    def test_create_energy_model_with_defaults(self):
        """Test creating an energy model with default values."""
        model = EnergyModel()

        assert model.sleep_hours == 8.0
        assert model.energy_score == 1.0
        assert model.focus_window_hours == 8.0
        assert model.cognitive_load == 0.0

    def test_create_energy_model_with_custom_values(self):
        """Test creating an energy model with custom values."""
        model = EnergyModel(
            sleep_hours=7.5,
            energy_score=0.8,
            focus_window_hours=6.0,
            cognitive_load=0.3,
        )

        assert model.sleep_hours == 7.5
        assert model.energy_score == 0.8
        assert model.focus_window_hours == 6.0
        assert model.cognitive_load == 0.3

    def test_validate_sleep_hours_non_negative(self):
        """Test that sleep_hours must be non-negative."""
        with pytest.raises(ValueError, match="sleep_hours must be non-negative"):
            EnergyModel(sleep_hours=-1.0)

    def test_validate_energy_score_range(self):
        """Test that energy_score must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="energy_score must be between 0.0 and 1.0"):
            EnergyModel(energy_score=1.5)

        with pytest.raises(ValueError, match="energy_score must be between 0.0 and 1.0"):
            EnergyModel(energy_score=-0.1)

    def test_validate_focus_window_hours_non_negative(self):
        """Test that focus_window_hours must be non-negative."""
        with pytest.raises(ValueError, match="focus_window_hours must be non-negative"):
            EnergyModel(focus_window_hours=-1.0)

    def test_validate_cognitive_load_range(self):
        """Test that cognitive_load must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="cognitive_load must be between 0.0 and 1.0"):
            EnergyModel(cognitive_load=1.5)

        with pytest.raises(ValueError, match="cognitive_load must be between 0.0 and 1.0"):
            EnergyModel(cognitive_load=-0.1)


@pytest.mark.unit
class TestSkillGraph:
    """Unit tests for SkillGraph."""

    def test_create_skill_graph_with_defaults(self):
        """Test creating a skill graph with default values."""
        model = SkillGraph(skill_name="Python")

        assert model.skill_name == "Python"
        assert model.proficiency_level == 0.0
        assert model.last_practiced is None
        assert model.priority_weight == 0.5

    def test_create_skill_graph_with_custom_values(self):
        """Test creating a skill graph with custom values."""
        now = datetime.now()
        model = SkillGraph(
            skill_name="Python",
            proficiency_level=0.8,
            last_practiced=now,
            priority_weight=0.9,
        )

        assert model.skill_name == "Python"
        assert model.proficiency_level == 0.8
        assert model.last_practiced == now
        assert model.priority_weight == 0.9

    def test_validate_skill_name_required(self):
        """Test that skill_name is required."""
        with pytest.raises(TypeError):
            SkillGraph()  # Missing required skill_name argument

    def test_validate_proficiency_level_range(self):
        """Test that proficiency_level must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="proficiency_level must be between 0.0 and 1.0"):
            SkillGraph(skill_name="Python", proficiency_level=1.5)

        with pytest.raises(ValueError, match="proficiency_level must be between 0.0 and 1.0"):
            SkillGraph(skill_name="Python", proficiency_level=-0.1)

    def test_validate_priority_weight_range(self):
        """Test that priority_weight must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="priority_weight must be between 0.0 and 1.0"):
            SkillGraph(skill_name="Python", priority_weight=1.5)

        with pytest.raises(ValueError, match="priority_weight must be between 0.0 and 1.0"):
            SkillGraph(skill_name="Python", priority_weight=-0.1)


@pytest.mark.unit
class TestDecisionProfile:
    """Unit tests for DecisionProfile."""

    def test_create_decision_profile_with_defaults(self):
        """Test creating a decision profile with default values."""
        model = DecisionProfile()

        assert model.speed_bias == 0.5
        assert model.accuracy_bias == 0.5
        assert model.strategic_horizon_days == 30

    def test_create_decision_profile_with_custom_values(self):
        """Test creating a decision profile with custom values."""
        model = DecisionProfile(
            speed_bias=0.7,
            accuracy_bias=0.9,
            strategic_horizon_days=60,
        )

        assert model.speed_bias == 0.7
        assert model.accuracy_bias == 0.9
        assert model.strategic_horizon_days == 60

    def test_validate_speed_bias_range(self):
        """Test that speed_bias must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="speed_bias must be between 0.0 and 1.0"):
            DecisionProfile(speed_bias=1.5)

        with pytest.raises(ValueError, match="speed_bias must be between 0.0 and 1.0"):
            DecisionProfile(speed_bias=-0.1)

    def test_validate_accuracy_bias_range(self):
        """Test that accuracy_bias must be between 0.0 and 1.0."""
        with pytest.raises(ValueError, match="accuracy_bias must be between 0.0 and 1.0"):
            DecisionProfile(accuracy_bias=1.5)

        with pytest.raises(ValueError, match="accuracy_bias must be between 0.0 and 1.0"):
            DecisionProfile(accuracy_bias=-0.1)

    def test_validate_strategic_horizon_days_non_negative(self):
        """Test that strategic_horizon_days must be non-negative."""
        with pytest.raises(ValueError, match="strategic_horizon_days must be non-negative"):
            DecisionProfile(strategic_horizon_days=-1)
