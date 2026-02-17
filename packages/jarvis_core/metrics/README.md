# Metrics Engine

The Metrics Engine provides performance tracking and measurement capabilities for the JARVIS system. It calculates various metrics to assess system progress and alignment with strategic goals.

## Overview

The Metrics Engine calculates four core metrics:

1. **Strategic Alignment Score** - Measures task alignment with primary mission
2. **Cognitive Throughput** - Measures task completion rate per focus hour
3. **Learning Velocity** - Measures skill improvement over time
4. **Momentum Index** - Weighted combination of all metrics

## Components

### MetricsReport (DTO)

Data Transfer Object for structured metrics reporting with:
- Pydantic validation
- Type safety
- Helper methods for summaries and performance checks

### MetricsEngine

Core calculation engine with:
- Individual metric calculation methods
- Configurable metric weights
- Comprehensive validation
- Full error handling

## Usage

### Basic Usage

```python
from jarvis_core.metrics import MetricsEngine, MetricsReport

# Create engine with default weights
engine = MetricsEngine()

# Calculate metrics for a period
report = engine.calculate_metrics(
    total_tasks=100,
    completed_tasks=85,
    completed_tasks_related_to_mission=70,
    active_focus_hours=50.0,
    skill_improvement_delta=2.5,
    days_elapsed=30.0,
    metadata={"period": "January 2024"}
)

# Display results
print(report.get_summary())
print(f"High Performance: {report.is_high_performance()}")
```

### Custom Weights

```python
# Create engine with custom metric weights
engine = MetricsEngine(
    strategic_weight=0.40,  # 40% weight on strategic alignment
    throughput_weight=0.30,  # 30% weight on throughput
    learning_weight=0.20,    # 20% weight on learning
    base_weight=0.10        # 10% weight on completion rate
)
```

### Individual Metric Calculations

```python
engine = MetricsEngine()

# Calculate individual metrics
alignment = engine.calculate_strategic_alignment_score(
    completed_tasks_related_to_primary_mission=70,
    total_tasks=100
)

throughput = engine.calculate_cognitive_throughput(
    completed_tasks=85,
    active_focus_hours=50.0
)

velocity = engine.calculate_learning_velocity(
    skill_improvement_delta=2.5,
    days_elapsed=30.0
)
```

## Metrics Definitions

### Strategic Alignment Score

**Formula:** `completed_tasks_related_to_primary_mission / total_tasks`

**Range:** 0.0 to 1.0

**Purpose:** Measures how well completed tasks align with the system's primary mission.

### Cognitive Throughput

**Formula:** `completed_tasks / active_focus_hours`

**Range:** 0.0 to infinity (typically 0.5 to 2.5 tasks/hour)

**Purpose:** Measures task completion efficiency during active focus time.

### Learning Velocity

**Formula:** `skill_improvement_delta / days_elapsed`

**Range:** -infinity to infinity (typically -0.1 to 0.2 per day)

**Purpose:** Measures rate of skill improvement or decay over time.

### Momentum Index

**Formula:** Weighted combination of:
- Strategic Alignment Score (35% weight by default)
- Normalized Cognitive Throughput (30% weight by default)
- Normalized Learning Velocity (20% weight by default)
- Task Completion Rate (15% weight by default)

**Range:** 0.0 to 1.0

**Purpose:** Provides an overall performance score combining all metrics.

## Validation

All inputs are validated:
- Non-negative task counts
- Non-negative hours
- Positive days elapsed
- Score ranges (0.0 to 1.0)
- Weight sum equals 1.0

Invalid inputs raise `ValueError` with descriptive messages.

## Testing

The metrics engine includes comprehensive unit tests:
- 41 test cases
- 98% code coverage
- Edge case handling
- Validation testing

Run tests with:
```bash
pytest tests/unit/metrics/test_metrics_engine.py -v
```

## Performance Indicators

The `MetricsReport` includes helper methods:

### is_high_performance()

Returns `True` if:
- Momentum Index >= 0.8 AND
- Strategic Alignment Score >= 0.7

### get_summary()

Returns a human-readable summary string with all key metrics.

## Examples

### High Performance Scenario

```python
report = engine.calculate_metrics(
    total_tasks=100,
    completed_tasks=95,
    completed_tasks_related_to_mission=90,
    active_focus_hours=50.0,
    skill_improvement_delta=4.0,
    days_elapsed=30.0
)
# Momentum: ~94%, High Performance: True
```

### Low Performance Scenario

```python
report = engine.calculate_metrics(
    total_tasks=100,
    completed_tasks=30,
    completed_tasks_related_to_mission=15,
    active_focus_hours=60.0,
    skill_improvement_delta=0.5,
    days_elapsed=30.0
)
# Momentum: ~21%, High Performance: False
```

### Edge Case: No Tasks

```python
report = engine.calculate_metrics(
    total_tasks=0,
    completed_tasks=0,
    completed_tasks_related_to_mission=0,
    active_focus_hours=10.0,
    skill_improvement_delta=1.0,
    days_elapsed=7.0
)
# Momentum: 0%, High Performance: False
```

## Integration

The Metrics Engine can be integrated with:
- Performance monitoring dashboards
- Strategic planning systems
- Analytics pipelines
- Reporting tools
- Task management systems

## Architecture

The Metrics Engine follows JARVIS Clean Architecture:
- **DTO Pattern** - `MetricsReport` for data transfer
- **Validation** - Pydantic for input validation
- **Type Safety** - Full type hints throughout
- **Documentation** - Comprehensive docstrings
- **Testing** - High test coverage

## Future Enhancements

Potential future improvements:
- Time-series metrics tracking
- Metric trend analysis
- Predictive metrics
- Multi-period comparisons
- Custom metric definitions
- Integration with memory system for historical tracking
