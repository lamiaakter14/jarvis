"""Unit tests for metrics engine."""

from datetime import datetime

import pytest
from jarvis_core.metrics.engine import MetricsEngine, MetricsReport


@pytest.mark.unit
class TestMetricsReport:
    """Unit tests for MetricsReport DTO."""
    
    def test_metrics_report_creation_with_valid_data(self):
        """Test creating a metrics report with valid data."""
        report = MetricsReport(
            strategic_alignment_score=0.75,
            cognitive_throughput=1.5,
            learning_velocity=0.05,
            momentum_index=0.80,
            total_tasks=100,
            completed_tasks_related_to_mission=75,
            completed_tasks=90,
            active_focus_hours=60.0,
            skill_improvement_delta=1.5,
            days_elapsed=30.0,
        )
        
        assert report.strategic_alignment_score == 0.75
        assert report.cognitive_throughput == 1.5
        assert report.learning_velocity == 0.05
        assert report.momentum_index == 0.80
        assert report.total_tasks == 100
        assert report.completed_tasks == 90
        assert isinstance(report.timestamp, datetime)
    
    def test_metrics_report_with_metadata(self):
        """Test metrics report with additional metadata."""
        metadata = {"period": "Q1 2024", "team": "engineering"}
        report = MetricsReport(
            strategic_alignment_score=0.8,
            cognitive_throughput=1.2,
            learning_velocity=0.03,
            momentum_index=0.75,
            metadata=metadata,
        )
        
        assert report.metadata == metadata
        assert report.metadata["period"] == "Q1 2024"
    
    def test_metrics_report_to_dict(self):
        """Test converting metrics report to dictionary."""
        report = MetricsReport(
            strategic_alignment_score=0.7,
            cognitive_throughput=1.0,
            learning_velocity=0.02,
            momentum_index=0.65,
        )
        
        result = report.to_dict()
        
        assert isinstance(result, dict)
        assert result["strategic_alignment_score"] == 0.7
        assert result["cognitive_throughput"] == 1.0
        assert result["learning_velocity"] == 0.02
        assert result["momentum_index"] == 0.65
    
    def test_metrics_report_get_summary(self):
        """Test getting human-readable summary."""
        report = MetricsReport(
            strategic_alignment_score=0.75,
            cognitive_throughput=1.5,
            learning_velocity=0.05,
            momentum_index=0.80,
        )
        
        summary = report.get_summary()
        
        assert "Strategic Alignment: 75.00%" in summary
        assert "Cognitive Throughput: 1.50 tasks/hour" in summary
        assert "Learning Velocity: 0.050/day" in summary
        assert "Momentum Index: 80.00%" in summary
    
    def test_metrics_report_is_high_performance_true(self):
        """Test high performance check returns true."""
        report = MetricsReport(
            strategic_alignment_score=0.85,
            cognitive_throughput=1.5,
            learning_velocity=0.05,
            momentum_index=0.85,
        )
        
        assert report.is_high_performance() is True
    
    def test_metrics_report_is_high_performance_false_low_momentum(self):
        """Test high performance check returns false with low momentum."""
        report = MetricsReport(
            strategic_alignment_score=0.85,
            cognitive_throughput=1.5,
            learning_velocity=0.05,
            momentum_index=0.75,
        )
        
        assert report.is_high_performance() is False
    
    def test_metrics_report_is_high_performance_false_low_alignment(self):
        """Test high performance check returns false with low alignment."""
        report = MetricsReport(
            strategic_alignment_score=0.65,
            cognitive_throughput=1.5,
            learning_velocity=0.05,
            momentum_index=0.85,
        )
        
        assert report.is_high_performance() is False
    
    def test_metrics_report_validation_negative_values(self):
        """Test validation rejects negative values."""
        with pytest.raises(ValueError):
            MetricsReport(
                strategic_alignment_score=0.8,
                cognitive_throughput=1.5,
                learning_velocity=0.05,
                momentum_index=0.75,
                total_tasks=-10,
            )
    
    def test_metrics_report_validation_score_out_of_range(self):
        """Test validation rejects scores outside 0-1 range."""
        with pytest.raises(ValueError):
            MetricsReport(
                strategic_alignment_score=1.5,
                cognitive_throughput=1.0,
                learning_velocity=0.05,
                momentum_index=0.75,
            )


@pytest.mark.unit
class TestMetricsEngine:
    """Unit tests for MetricsEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create a metrics engine instance."""
        return MetricsEngine()
    
    def test_engine_initialization_default_weights(self):
        """Test engine initialization with default weights."""
        engine = MetricsEngine()
        
        assert engine.strategic_weight == 0.35
        assert engine.throughput_weight == 0.30
        assert engine.learning_weight == 0.20
        assert engine.base_weight == 0.15
    
    def test_engine_initialization_custom_weights(self):
        """Test engine initialization with custom weights."""
        engine = MetricsEngine(
            strategic_weight=0.4,
            throughput_weight=0.3,
            learning_weight=0.2,
            base_weight=0.1
        )
        
        assert engine.strategic_weight == 0.4
        assert engine.throughput_weight == 0.3
        assert engine.learning_weight == 0.2
        assert engine.base_weight == 0.1
    
    def test_engine_initialization_invalid_weights(self):
        """Test engine initialization rejects invalid weights."""
        with pytest.raises(ValueError, match="Weights must sum to 1.0"):
            MetricsEngine(
                strategic_weight=0.5,
                throughput_weight=0.3,
                learning_weight=0.3,
                base_weight=0.1
            )
    
    def test_calculate_strategic_alignment_score_perfect_alignment(self, engine):
        """Test strategic alignment calculation with perfect alignment."""
        score = engine.calculate_strategic_alignment_score(
            completed_tasks_related_to_primary_mission=100,
            total_tasks=100
        )
        
        assert score == 1.0
    
    def test_calculate_strategic_alignment_score_partial_alignment(self, engine):
        """Test strategic alignment calculation with partial alignment."""
        score = engine.calculate_strategic_alignment_score(
            completed_tasks_related_to_primary_mission=75,
            total_tasks=100
        )
        
        assert score == 0.75
    
    def test_calculate_strategic_alignment_score_no_alignment(self, engine):
        """Test strategic alignment calculation with no alignment."""
        score = engine.calculate_strategic_alignment_score(
            completed_tasks_related_to_primary_mission=0,
            total_tasks=100
        )
        
        assert score == 0.0
    
    def test_calculate_strategic_alignment_score_no_tasks(self, engine):
        """Test strategic alignment calculation with no tasks."""
        score = engine.calculate_strategic_alignment_score(
            completed_tasks_related_to_primary_mission=0,
            total_tasks=0
        )
        
        assert score == 0.0
    
    def test_calculate_strategic_alignment_score_validation_negative_total(self, engine):
        """Test strategic alignment validation rejects negative total tasks."""
        with pytest.raises(ValueError, match="total_tasks must be non-negative"):
            engine.calculate_strategic_alignment_score(
                completed_tasks_related_to_primary_mission=50,
                total_tasks=-10
            )
    
    def test_calculate_strategic_alignment_score_validation_negative_mission(self, engine):
        """Test strategic alignment validation rejects negative mission tasks."""
        with pytest.raises(ValueError, match="must be non-negative"):
            engine.calculate_strategic_alignment_score(
                completed_tasks_related_to_primary_mission=-5,
                total_tasks=100
            )
    
    def test_calculate_strategic_alignment_score_validation_exceeds_total(self, engine):
        """Test strategic alignment validation rejects mission tasks exceeding total."""
        with pytest.raises(ValueError, match="cannot exceed total_tasks"):
            engine.calculate_strategic_alignment_score(
                completed_tasks_related_to_primary_mission=150,
                total_tasks=100
            )
    
    def test_calculate_cognitive_throughput_normal(self, engine):
        """Test cognitive throughput calculation with normal values."""
        throughput = engine.calculate_cognitive_throughput(
            completed_tasks=30,
            active_focus_hours=20.0
        )
        
        assert throughput == 1.5
    
    def test_calculate_cognitive_throughput_high_productivity(self, engine):
        """Test cognitive throughput calculation with high productivity."""
        throughput = engine.calculate_cognitive_throughput(
            completed_tasks=50,
            active_focus_hours=20.0
        )
        
        assert throughput == 2.5
    
    def test_calculate_cognitive_throughput_no_hours(self, engine):
        """Test cognitive throughput calculation with no focus hours."""
        throughput = engine.calculate_cognitive_throughput(
            completed_tasks=10,
            active_focus_hours=0.0
        )
        
        assert throughput == 0.0
    
    def test_calculate_cognitive_throughput_validation_negative_tasks(self, engine):
        """Test cognitive throughput validation rejects negative tasks."""
        with pytest.raises(ValueError, match="completed_tasks must be non-negative"):
            engine.calculate_cognitive_throughput(
                completed_tasks=-5,
                active_focus_hours=10.0
            )
    
    def test_calculate_cognitive_throughput_validation_negative_hours(self, engine):
        """Test cognitive throughput validation rejects negative hours."""
        with pytest.raises(ValueError, match="active_focus_hours must be non-negative"):
            engine.calculate_cognitive_throughput(
                completed_tasks=10,
                active_focus_hours=-5.0
            )
    
    def test_calculate_learning_velocity_positive_improvement(self, engine):
        """Test learning velocity calculation with positive improvement."""
        velocity = engine.calculate_learning_velocity(
            skill_improvement_delta=3.0,
            days_elapsed=30.0
        )
        
        assert velocity == 0.1
    
    def test_calculate_learning_velocity_negative_improvement(self, engine):
        """Test learning velocity calculation with skill decay."""
        velocity = engine.calculate_learning_velocity(
            skill_improvement_delta=-1.5,
            days_elapsed=30.0
        )
        
        assert velocity == -0.05
    
    def test_calculate_learning_velocity_no_improvement(self, engine):
        """Test learning velocity calculation with no improvement."""
        velocity = engine.calculate_learning_velocity(
            skill_improvement_delta=0.0,
            days_elapsed=30.0
        )
        
        assert velocity == 0.0
    
    def test_calculate_learning_velocity_validation_zero_days(self, engine):
        """Test learning velocity validation rejects zero days."""
        with pytest.raises(ValueError, match="days_elapsed must be positive"):
            engine.calculate_learning_velocity(
                skill_improvement_delta=1.0,
                days_elapsed=0.0
            )
    
    def test_calculate_learning_velocity_validation_negative_days(self, engine):
        """Test learning velocity validation rejects negative days."""
        with pytest.raises(ValueError, match="days_elapsed must be positive"):
            engine.calculate_learning_velocity(
                skill_improvement_delta=1.0,
                days_elapsed=-5.0
            )
    
    def test_calculate_momentum_index_high_performance(self, engine):
        """Test momentum index calculation with high performance."""
        momentum = engine.calculate_momentum_index(
            strategic_alignment_score=0.9,
            cognitive_throughput=2.0,
            learning_velocity=0.1,
            completed_tasks=90,
            total_tasks=100,
            max_expected_throughput=2.0
        )
        
        # High values across all metrics should result in high momentum
        assert momentum > 0.8
    
    def test_calculate_momentum_index_low_performance(self, engine):
        """Test momentum index calculation with low performance."""
        momentum = engine.calculate_momentum_index(
            strategic_alignment_score=0.3,
            cognitive_throughput=0.5,
            learning_velocity=0.01,
            completed_tasks=30,
            total_tasks=100,
            max_expected_throughput=2.0
        )
        
        # Low values across all metrics should result in low momentum
        assert momentum < 0.5
    
    def test_calculate_momentum_index_mixed_performance(self, engine):
        """Test momentum index calculation with mixed performance."""
        momentum = engine.calculate_momentum_index(
            strategic_alignment_score=0.7,
            cognitive_throughput=1.0,
            learning_velocity=0.05,
            completed_tasks=60,
            total_tasks=100,
            max_expected_throughput=2.0
        )
        
        # Mixed performance should result in moderate momentum
        assert 0.4 < momentum < 0.8
    
    def test_calculate_momentum_index_negative_learning(self, engine):
        """Test momentum index with negative learning velocity."""
        momentum = engine.calculate_momentum_index(
            strategic_alignment_score=0.8,
            cognitive_throughput=1.5,
            learning_velocity=-0.05,
            completed_tasks=80,
            total_tasks=100,
            max_expected_throughput=2.0
        )
        
        # Negative learning should be penalized but not dominate
        assert 0.4 < momentum < 0.8
    
    def test_calculate_momentum_index_validation_alignment_out_of_range(self, engine):
        """Test momentum index validation rejects alignment score out of range."""
        with pytest.raises(ValueError, match="strategic_alignment_score must be between"):
            engine.calculate_momentum_index(
                strategic_alignment_score=1.5,
                cognitive_throughput=1.0,
                learning_velocity=0.05,
                completed_tasks=50,
                total_tasks=100,
                max_expected_throughput=2.0
            )
    
    def test_calculate_momentum_index_validation_negative_total_tasks(self, engine):
        """Test momentum index validation rejects negative total tasks."""
        with pytest.raises(ValueError, match="total_tasks must be non-negative"):
            engine.calculate_momentum_index(
                strategic_alignment_score=0.8,
                cognitive_throughput=1.0,
                learning_velocity=0.05,
                completed_tasks=50,
                total_tasks=-10,
                max_expected_throughput=2.0
            )
    
    def test_calculate_momentum_index_validation_invalid_max_throughput(self, engine):
        """Test momentum index validation rejects invalid max throughput."""
        with pytest.raises(ValueError, match="max_expected_throughput must be positive"):
            engine.calculate_momentum_index(
                strategic_alignment_score=0.8,
                cognitive_throughput=1.0,
                learning_velocity=0.05,
                completed_tasks=50,
                total_tasks=100,
                max_expected_throughput=0.0
            )
    
    def test_calculate_metrics_complete_report(self, engine):
        """Test calculating complete metrics report."""
        report = engine.calculate_metrics(
            total_tasks=100,
            completed_tasks=85,
            completed_tasks_related_to_mission=70,
            active_focus_hours=50.0,
            skill_improvement_delta=2.5,
            days_elapsed=30.0,
        )
        
        assert isinstance(report, MetricsReport)
        assert report.strategic_alignment_score == 0.7
        assert report.cognitive_throughput == 1.7
        assert abs(report.learning_velocity - 0.0833) < 0.001
        assert 0.0 <= report.momentum_index <= 1.0
        assert report.total_tasks == 100
        assert report.completed_tasks == 85
        assert report.completed_tasks_related_to_mission == 70
    
    def test_calculate_metrics_with_metadata(self, engine):
        """Test calculating metrics with custom metadata."""
        metadata = {"user": "test_user", "period": "2024-Q1"}
        report = engine.calculate_metrics(
            total_tasks=50,
            completed_tasks=40,
            completed_tasks_related_to_mission=35,
            active_focus_hours=30.0,
            skill_improvement_delta=1.5,
            days_elapsed=15.0,
            metadata=metadata
        )
        
        assert report.metadata == metadata
        assert report.metadata["user"] == "test_user"
    
    def test_calculate_metrics_edge_case_no_tasks(self, engine):
        """Test calculating metrics with no tasks."""
        report = engine.calculate_metrics(
            total_tasks=0,
            completed_tasks=0,
            completed_tasks_related_to_mission=0,
            active_focus_hours=10.0,
            skill_improvement_delta=0.5,
            days_elapsed=7.0,
        )
        
        assert report.strategic_alignment_score == 0.0
        assert report.cognitive_throughput == 0.0
        assert report.momentum_index == 0.0
    
    def test_calculate_metrics_edge_case_no_focus_hours(self, engine):
        """Test calculating metrics with no focus hours."""
        report = engine.calculate_metrics(
            total_tasks=50,
            completed_tasks=30,
            completed_tasks_related_to_mission=25,
            active_focus_hours=0.0,
            skill_improvement_delta=1.0,
            days_elapsed=10.0,
        )
        
        assert report.cognitive_throughput == 0.0
        assert report.strategic_alignment_score == 0.5
    
    def test_calculate_metrics_comprehensive_scenario(self, engine):
        """Test comprehensive realistic scenario."""
        # Scenario: 30-day period, strong strategic alignment, good throughput
        report = engine.calculate_metrics(
            total_tasks=120,
            completed_tasks=100,
            completed_tasks_related_to_mission=85,
            active_focus_hours=60.0,
            skill_improvement_delta=2.4,
            days_elapsed=30.0,
            max_expected_throughput=2.0,
            metadata={
                "period": "January 2024",
                "focus_area": "Backend Development"
            }
        )
        
        # Verify all metrics are calculated
        assert 0.0 <= report.strategic_alignment_score <= 1.0
        assert report.cognitive_throughput > 0.0
        assert report.learning_velocity > 0.0
        assert 0.0 <= report.momentum_index <= 1.0
        
        # Verify this scenario shows good performance
        assert report.strategic_alignment_score > 0.7
        assert report.cognitive_throughput > 1.5
        
        # Verify summary is informative
        summary = report.get_summary()
        assert "Strategic Alignment" in summary
        assert "Cognitive Throughput" in summary
