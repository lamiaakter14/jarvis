# Application Layer Guide

## Overview

The Application Layer implements use cases and orchestrates domain objects to fulfill business requirements. It sits between the Presentation Layer (API/CLI) and the Domain Layer.

## Architecture Principles

1. **Use Case Oriented**: Each use case is a single class with a clear `execute()` method
2. **Dependency Injection**: All dependencies injected via constructor
3. **No Infrastructure Dependencies**: Uses interfaces for external services
4. **Domain Event Emission**: Emits events for important state changes
5. **DTO Pattern**: Uses DTOs for data transfer across boundaries

## Directory Structure

```
src/application/
├── dto/                      # Data Transfer Objects
│   ├── task_dto.py          # Task serialization
│   ├── plan_dto.py          # Plan serialization
│   └── analytics_dto.py     # Analytics data
├── interfaces/               # Service interfaces
│   ├── i_ai_service.py      # AI operations
│   └── i_notification_service.py  # Notifications
└── use_cases/               # Application use cases
    ├── execute_cognitive_loop.py   # Main loop
    ├── generate_daily_plan.py      # Planning
    ├── execute_tasks.py            # Execution
    ├── analyze_performance.py      # Analytics
    ├── identify_gaps.py            # Gap analysis
    └── create_innovations.py       # Innovation
```

## Data Transfer Objects (DTOs)

### Purpose
- Serialize domain entities for API responses
- Validate input data with Pydantic
- Decouple domain model from external representation

### TaskDTO

```python
from src.application.dto import TaskDTO
from src.domain.entities.task import Task

# Convert from entity
task = Task(title="Example Task")
dto = TaskDTO.from_entity(task)

# Convert to entity
task = dto.to_entity()

# Serialize to dict
data = dto.to_dict()
```

**Fields:**
- `task_id`: Unique identifier
- `title`: Task title
- `description`: Detailed description
- `priority`: Priority level (low/medium/high/critical)
- `cognitive_load`: Load level (low/medium/high)
- `roi`: Return on investment (0.0-1.0)
- `status`: Current status
- `agent_type`: Assigned agent type
- `created_at`, `updated_at`, `completed_at`: Timestamps
- `result`: Execution result

### PlanDTO

```python
from src.application.dto import PlanDTO
from src.domain.entities.plan import Plan

# Convert from entity
plan = Plan(date=today)
dto = PlanDTO.from_entity(plan)

# Get metrics
planned_hours = dto.get_planned_hours()
remaining = dto.get_remaining_hours()
completion = dto.get_completion_percentage()
```

**Fields:**
- `plan_id`: Unique identifier
- `date`: Plan date
- `tasks`: List of TaskDTO
- `total_hours`: Available hours
- `status`: Plan status (draft/active/completed/archived)
- `created_by`: Creator
- `created_at`: Creation timestamp

### AnalyticsDTO

```python
from src.application.dto import AnalyticsDTO

# Create analytics
analytics = AnalyticsDTO(
    period="weekly",
    total_tasks=25,
    completed_tasks=20,
    average_roi=0.75,
    productivity_score=0.82
)

# Get metrics
completion_rate = analytics.get_completion_rate()
is_high_perf = analytics.is_high_performance()
summary = analytics.get_summary()
```

**Fields:**
- `period`: Time period
- `total_tasks`, `completed_tasks`, `failed_tasks`, `pending_tasks`
- `average_roi`: Average ROI across tasks
- `top_gaps`: Identified knowledge gaps
- `recent_innovations`: Recent innovations
- `productivity_score`: Overall score (0.0-1.0)
- `success_rate`, `utilization_rate`: Performance metrics

## Application Interfaces

### IAIService

Interface for AI-powered operations.

```python
from src.application.interfaces import IAIService

class MyAIService(IAIService):
    async def generate_plan(self, context: Context) -> Plan:
        # AI-powered plan generation
        pass
    
    async def analyze_gaps(self, logs: List[Dict]) -> List[Dict]:
        # Gap identification
        pass
    
    async def generate_innovations(self, context: Context) -> List[Innovation]:
        # Innovation generation
        pass
    
    async def provide_mentorship(self, task: Task) -> Dict[str, Any]:
        # Task guidance
        pass
```

### INotificationService

Interface for notification delivery.

```python
from src.application.interfaces import INotificationService

class MyNotificationService(INotificationService):
    async def send_notification(self, message: str, type: str) -> None:
        # Send general notification
        pass
    
    async def notify_task_completed(self, task: Task) -> None:
        # Task completion notification
        pass
    
    async def notify_gap_identified(self, gap: Dict) -> None:
        # Gap identification notification
        pass
```

## Use Cases

### ExecuteCognitiveLoop

Main orchestration use case that runs the 5-agent cognitive loop.

```python
from src.application.use_cases import ExecuteCognitiveLoop

# Initialize with dependencies
loop = ExecuteCognitiveLoop(
    task_repository=task_repo,
    memory_repository=memory_repo,
    analytics_repository=analytics_repo,
    ai_service=ai_service,
    notification_service=notif_service,
    strategy_engine=strategy_engine,
    innovation_engine=innovation_engine
)

# Execute the loop
summary = await loop.execute()

# Summary contains results from all 5 agents:
# - strategist: Planning results
# - mentor: Diagnostics results
# - executor: Execution results
# - innovator: Innovation results
# - amplifier: Performance analysis results
```

**Flow:**
1. **Strategist** - Generate daily plan
2. **Mentor** - Identify knowledge gaps
3. **Executor** - Execute high-priority tasks
4. **Innovator** - Generate innovations
5. **Amplifier** - Analyze performance

### GenerateDailyPlan

Creates optimized daily plans using AI and strategic planning.

```python
from src.application.use_cases import GenerateDailyPlan
from datetime import date

# Initialize
planner = GenerateDailyPlan(
    task_repository=task_repo,
    memory_repository=memory_repo,
    ai_service=ai_service,
    strategy_engine=strategy_engine
)

# Generate plan
plan_dto = await planner.execute(
    target_date=date.today(),
    available_hours=8.0
)
```

**Process:**
1. Load context (goals, gaps, focus areas)
2. Get pending tasks
3. Calculate ROI for tasks
4. Use AI to generate plan
5. Optimize and validate plan
6. Store plan in memory

### ExecuteTasks

Executes specific tasks and tracks results.

```python
from src.application.use_cases import ExecuteTasks

# Initialize
executor = ExecuteTasks(
    task_repository=task_repo,
    notification_service=notif_service
)

# Execute tasks
task_ids = ["task_123", "task_456"]
results = await executor.execute(task_ids)

# Results are list of TaskDTO with updated status
```

**Features:**
- Marks tasks as in-progress
- Executes tasks (delegates to infrastructure)
- Marks as completed/failed
- Emits TaskCompletedEvent
- Sends notifications

### AnalyzePerformance

Analyzes performance metrics over a date range.

```python
from src.application.use_cases import AnalyzePerformance
from datetime import date, timedelta

# Initialize
analyzer = AnalyzePerformance(
    task_repository=task_repo,
    analytics_repository=analytics_repo,
    memory_repository=memory_repo
)

# Analyze last 7 days
start_date = date.today() - timedelta(days=6)
analytics = await analyzer.execute(
    start_date=start_date,
    end_date=date.today()
)
```

**Metrics Calculated:**
- Task completion rate
- Success rate
- Average ROI
- Time utilization
- Productivity score
- Top gaps and innovations

### IdentifyGaps

Identifies knowledge and skill gaps from execution logs.

```python
from src.application.use_cases import IdentifyGaps

# Initialize
gap_identifier = IdentifyGaps(
    memory_repository=memory_repo,
    ai_service=ai_service,
    notification_service=notif_service
)

# Identify gaps
gaps = await gap_identifier.execute()

# Returns list of dicts with:
# - gap_id, type, description
# - severity (low/medium/high/critical)
# - evidence, learning_priority
```

**Process:**
1. Load execution logs
2. Use AI to analyze patterns
3. Enrich gaps with metadata
4. Store in memory
5. Notify high-severity gaps
6. Emit GapIdentifiedEvent

### CreateInnovations

Generates and ranks innovation ideas.

```python
from src.application.use_cases import CreateInnovations

# Initialize
innovator = CreateInnovations(
    memory_repository=memory_repo,
    task_repository=task_repo,
    innovation_engine=innovation_engine,
    ai_service=ai_service,
    notification_service=notif_service
)

# Generate innovations
innovations = await innovator.execute()

# Returns list of Innovation entities
```

**Sources:**
1. AI-generated innovations from context
2. Pattern analysis from tasks
3. Performance-based improvements

**Processing:**
- Deduplicates similar ideas
- Ranks by comprehensive score
- Filters to actionable items (score >= 0.6)
- Notifies high-impact innovations

## Usage Patterns

### Dependency Injection

All use cases use constructor injection:

```python
# Define dependencies
task_repo = get_task_repository()
memory_repo = get_memory_repository()
ai_service = get_ai_service()

# Inject into use case
use_case = GenerateDailyPlan(
    task_repository=task_repo,
    memory_repository=memory_repo,
    ai_service=ai_service,
    strategy_engine=StrategyEngine()
)

# Execute
result = await use_case.execute(date.today())
```

### Error Handling

All use cases use consistent error handling:

```python
try:
    result = await use_case.execute(params)
except DomainException as e:
    # Handle domain-level errors
    logger.error(f"Domain error: {e}")
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    raise
```

### Event Emission

Use cases emit domain events for important actions:

```python
# In use case
event = TaskCompletedEvent(
    task_id=task.task_id,
    agent_id="agent_123",
    agent_type="executor",
    result=result
)
# Publish to event bus (infrastructure layer)
```

## Testing

### Unit Testing Use Cases

```python
import pytest
from unittest.mock import Mock, AsyncMock

@pytest.mark.asyncio
async def test_generate_daily_plan():
    # Mock dependencies
    task_repo = Mock()
    task_repo.list = AsyncMock(return_value=[])
    
    memory_repo = Mock()
    memory_repo.retrieve = AsyncMock(return_value=None)
    
    ai_service = Mock()
    ai_service.generate_plan = AsyncMock(return_value=Plan())
    
    # Create use case
    planner = GenerateDailyPlan(
        task_repository=task_repo,
        memory_repository=memory_repo,
        ai_service=ai_service,
        strategy_engine=StrategyEngine()
    )
    
    # Execute
    result = await planner.execute(date.today())
    
    # Assert
    assert result is not None
    assert isinstance(result, PlanDTO)
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_cognitive_loop_integration():
    # Use real repositories with test data
    task_repo = InMemoryTaskRepository()
    memory_repo = InMemoryMemoryRepository()
    
    # Mock external services
    ai_service = MockAIService()
    notif_service = MockNotificationService()
    
    # Create use case
    loop = ExecuteCognitiveLoop(...)
    
    # Execute
    summary = await loop.execute()
    
    # Verify all phases completed
    assert summary["overall_status"] == "success"
    assert "strategist" in summary
    assert "mentor" in summary
    # ... etc
```

## Best Practices

1. **Single Responsibility**: Each use case does one thing
2. **Dependency Injection**: Inject all dependencies
3. **No Business Logic**: Delegate to domain services
4. **Error Handling**: Catch and wrap exceptions appropriately
5. **Async/Await**: Use async for I/O operations
6. **Type Hints**: All parameters and returns typed
7. **Documentation**: Comprehensive docstrings
8. **Testability**: Design for easy mocking and testing

## Common Pitfalls

1. **Putting domain logic in use cases** - Belongs in domain layer
2. **Direct infrastructure dependencies** - Use interfaces
3. **Complex orchestration in DTOs** - Keep them simple
4. **Skipping validation** - Let Pydantic handle it
5. **Not emitting events** - Important for event-driven architecture

## Next Steps

- Implement infrastructure layer services (AI, notifications)
- Add event bus for domain event publishing
- Create API endpoints using these use cases
- Add comprehensive integration tests
- Set up monitoring and logging
