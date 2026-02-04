"""Mock repository fixtures for testing."""
import pytest
from unittest.mock import AsyncMock, Mock
from typing import List, Optional, Dict, Any

from src.domain.repositories.i_task_repository import ITaskRepository
from src.domain.repositories.i_memory_repository import IMemoryRepository
from src.domain.repositories.i_analytics_repository import IAnalyticsRepository
from src.application.interfaces.i_ai_service import IAIService
from src.application.interfaces.i_notification_service import INotificationService


@pytest.fixture
def mock_task_repository():
    """Create a mock task repository."""
    mock = Mock(spec=ITaskRepository)
    mock.save = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.list = AsyncMock(return_value=[])
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    mock.get_by_status = AsyncMock(return_value=[])
    mock.get_by_date_range = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_memory_repository():
    """Create a mock memory repository."""
    mock = Mock(spec=IMemoryRepository)
    mock.save = AsyncMock()
    mock.retrieve = AsyncMock(return_value=None)
    mock.list = AsyncMock(return_value=[])
    mock.delete = AsyncMock()
    mock.exists = AsyncMock(return_value=False)
    return mock


@pytest.fixture
def mock_analytics_repository():
    """Create a mock analytics repository."""
    mock = Mock(spec=IAnalyticsRepository)
    mock.save_metrics = AsyncMock()
    mock.get_metrics = AsyncMock(return_value={})
    mock.get_metrics_by_period = AsyncMock(return_value=[])
    return mock


@pytest.fixture
def mock_ai_service():
    """Create a mock AI service."""
    mock = Mock(spec=IAIService)
    mock.generate_plan = AsyncMock()
    mock.analyze_gaps = AsyncMock(return_value=[])
    mock.generate_innovations = AsyncMock(return_value=[])
    mock.provide_mentorship = AsyncMock(return_value={})
    return mock


@pytest.fixture
def mock_notification_service():
    """Create a mock notification service."""
    mock = Mock(spec=INotificationService)
    mock.send_notification = AsyncMock()
    mock.notify_task_completed = AsyncMock()
    mock.notify_gap_identified = AsyncMock()
    return mock


class InMemoryTaskRepository(ITaskRepository):
    """In-memory implementation of task repository for testing."""
    
    def __init__(self):
        self.tasks: Dict[str, Any] = {}
    
    async def save(self, task: Any) -> None:
        self.tasks[task.task_id] = task
    
    async def get(self, task_id: str) -> Optional[Any]:
        return self.tasks.get(task_id)
    
    async def list(self, filters: Optional[Dict] = None) -> List[Any]:
        return list(self.tasks.values())
    
    async def update(self, task: Any) -> None:
        if task.task_id in self.tasks:
            self.tasks[task.task_id] = task
    
    async def delete(self, task_id: str) -> None:
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    async def get_by_status(self, status: str) -> List[Any]:
        return [t for t in self.tasks.values() if t.status == status]
    
    async def get_by_date_range(self, start_date: Any, end_date: Any) -> List[Any]:
        return list(self.tasks.values())


class InMemoryMemoryRepository(IMemoryRepository):
    """In-memory implementation of memory repository for testing."""
    
    def __init__(self):
        self.memory: Dict[str, Dict[str, Any]] = {}
    
    async def save(self, memory_type: str, key: str, data: Dict) -> None:
        if memory_type not in self.memory:
            self.memory[memory_type] = {}
        self.memory[memory_type][key] = data
    
    async def retrieve(self, memory_type: str, key: str) -> Optional[Dict]:
        if memory_type in self.memory:
            return self.memory[memory_type].get(key)
        return None
    
    async def list(self, memory_type: str) -> List[str]:
        if memory_type in self.memory:
            return list(self.memory[memory_type].keys())
        return []
    
    async def delete(self, memory_type: str, key: str) -> None:
        if memory_type in self.memory and key in self.memory[memory_type]:
            del self.memory[memory_type][key]
    
    async def exists(self, memory_type: str, key: str) -> bool:
        return memory_type in self.memory and key in self.memory[memory_type]


@pytest.fixture
def in_memory_task_repository():
    """Create an in-memory task repository for integration tests."""
    return InMemoryTaskRepository()


@pytest.fixture
def in_memory_memory_repository():
    """Create an in-memory memory repository for integration tests."""
    return InMemoryMemoryRepository()
