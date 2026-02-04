"""Fixtures for domain layer tests."""
import pytest
from datetime import datetime, date
from uuid import uuid4

from src.domain.entities.task import Task
from src.domain.entities.plan import Plan
from src.domain.entities.context import Context
from src.domain.entities.innovation import Innovation
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.cognitive_load import CognitiveLoad
from src.domain.value_objects.roi import ROI
from src.domain.value_objects.agent_type import AgentType


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        task_id=str(uuid4()),
        title="Test Task",
        description="This is a test task",
        priority=Priority.HIGH,
        cognitive_load=CognitiveLoad.MEDIUM,
        roi=ROI(0.8),
        status="pending",
        agent_type=AgentType.EXECUTOR,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_tasks():
    """Create multiple sample tasks."""
    return [
        Task(
            task_id=str(uuid4()),
            title=f"Task {i}",
            description=f"Description {i}",
            priority=Priority.HIGH if i % 2 == 0 else Priority.MEDIUM,
            cognitive_load=CognitiveLoad.MEDIUM,
            roi=ROI(0.7 + i * 0.05),
            status="pending",
            agent_type=AgentType.EXECUTOR,
            created_at=datetime.now()
        )
        for i in range(5)
    ]


@pytest.fixture
def sample_plan(sample_tasks):
    """Create a sample plan with tasks."""
    return Plan(
        plan_id=str(uuid4()),
        date=date.today(),
        tasks=sample_tasks,
        total_hours=8.0,
        status="active",
        created_by="strategist",
        created_at=datetime.now()
    )


@pytest.fixture
def sample_context():
    """Create a sample cognitive context."""
    return Context(
        context_id=str(uuid4()),
        current_focus="Testing",
        goals=["Write comprehensive tests", "Ensure 90% coverage"],
        recent_gaps=["Testing knowledge", "Mock creation"],
        available_hours=8.0,
        energy_level=0.8,
        timestamp=datetime.now()
    )


@pytest.fixture
def sample_innovation():
    """Create a sample innovation."""
    return Innovation(
        innovation_id=str(uuid4()),
        title="Test Innovation",
        description="An innovative testing approach",
        category="testing",
        impact_score=0.85,
        effort_score=0.3,
        roi_score=0.9,
        implementation_complexity="low",
        status="proposed",
        created_at=datetime.now()
    )
