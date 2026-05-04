"""Unit tests for value objects."""

import pytest
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI


@pytest.mark.unit
class TestPriority:
    """Test Priority value object."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert Priority.LOW.value == "low"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.HIGH.value == "high"
        assert Priority.CRITICAL.value == "critical"

    def test_priority_comparison(self):
        """Test priority comparison logic."""
        assert Priority.CRITICAL > Priority.HIGH
        assert Priority.HIGH > Priority.MEDIUM
        assert Priority.MEDIUM > Priority.LOW

    def test_priority_from_string(self):
        """Test creating priority from string."""
        assert Priority("high") == Priority.HIGH
        assert Priority("low") == Priority.LOW


@pytest.mark.unit
class TestCognitiveLoad:
    """Test CognitiveLoad value object."""

    def test_cognitive_load_values(self):
        """Test cognitive load enum values."""
        assert CognitiveLoad.LOW.value == "low"
        assert CognitiveLoad.MEDIUM.value == "medium"
        assert CognitiveLoad.HIGH.value == "high"

    def test_cognitive_load_comparison(self):
        """Test cognitive load comparison."""
        assert CognitiveLoad.HIGH > CognitiveLoad.MEDIUM
        assert CognitiveLoad.MEDIUM > CognitiveLoad.LOW

    def test_cognitive_load_from_string(self):
        """Test creating cognitive load from string."""
        assert CognitiveLoad("medium") == CognitiveLoad.MEDIUM


@pytest.mark.unit
class TestROI:
    """Test ROI value object."""

    def test_create_roi_valid_value(self):
        """Test creating ROI with valid value."""
        roi = ROI(0.75)
        assert roi.value == 0.75

    def test_create_roi_boundary_values(self):
        """Test creating ROI with boundary values."""
        roi_min = ROI(0.0)
        assert roi_min.value == 0.0

        roi_max = ROI(1.0)
        assert roi_max.value == 1.0

    def test_create_roi_invalid_value_too_low(self):
        """Test creating ROI with value below minimum."""
        with pytest.raises((ValueError, Exception)):
            ROI(-0.1)

    def test_create_roi_invalid_value_too_high(self):
        """Test creating ROI with value above maximum."""
        with pytest.raises((ValueError, Exception)):
            ROI(1.1)

    def test_roi_comparison(self):
        """Test ROI comparison."""
        roi1 = ROI(0.8)
        roi2 = ROI(0.6)

        assert roi1 > roi2
        assert roi2 < roi1

    def test_roi_equality(self):
        """Test ROI equality."""
        roi1 = ROI(0.75)
        roi2 = ROI(0.75)

        assert roi1 == roi2

    def test_roi_to_percentage(self):
        """Test converting ROI to percentage."""
        roi = ROI(0.75)
        percentage = roi.to_percentage()
        assert percentage == 75.0


@pytest.mark.unit
class TestAgentType:
    """Test AgentType value object."""

    def test_agent_type_values(self):
        """Test agent type enum values."""
        assert AgentType.STRATEGIST.value == "strategist"
        assert AgentType.MENTOR.value == "mentor"
        assert AgentType.EXECUTOR.value == "executor"
        assert AgentType.INNOVATOR.value == "innovator"
        assert AgentType.AMPLIFIER.value == "amplifier"

    def test_agent_type_from_string(self):
        """Test creating agent type from string."""
        assert AgentType("strategist") == AgentType.STRATEGIST
        assert AgentType("executor") == AgentType.EXECUTOR

    def test_all_agent_types(self):
        """Test getting all agent types."""
        all_types = list(AgentType)
        assert AgentType.STRATEGIST in all_types
        assert AgentType.MENTOR in all_types
        assert AgentType.EXECUTOR in all_types
        assert AgentType.POLITICAL_MEDIA_OS in all_types
