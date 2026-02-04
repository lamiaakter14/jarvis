"""Infrastructure layer for JARVIS Clean Architecture.

This layer provides concrete implementations of all interfaces defined
in the domain and application layers, including:

- Configuration and dependency injection
- Repository implementations (file-based and SQLite)
- AI service implementation (OpenAI)
- Concrete agent implementations
- Monitoring and logging
"""

from src.infrastructure.config import settings, Settings
from src.infrastructure.persistence import (
    JsonStorage,
    FileMemoryRepository,
    SqliteTaskRepository,
)
from src.infrastructure.ai import OpenAIService
from src.infrastructure.agents import (
    StrategistAgent,
    MentorAgent,
    ExecutorAgent,
    InnovatorAgent,
    AmplifierAgent,
)
from src.infrastructure.monitoring import (
    Logger,
    MetricsCollector,
    Tracer,
)

__all__ = [
    # Config
    "settings",
    "Settings",
    # Persistence
    "JsonStorage",
    "FileMemoryRepository",
    "SqliteTaskRepository",
    # AI
    "OpenAIService",
    # Agents
    "StrategistAgent",
    "MentorAgent",
    "ExecutorAgent",
    "InnovatorAgent",
    "AmplifierAgent",
    # Monitoring
    "Logger",
    "MetricsCollector",
    "Tracer",
]
