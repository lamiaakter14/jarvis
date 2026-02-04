"""Domain repository interfaces (ports) for the JARVIS system.

This module exports all repository interfaces that define the contracts
for persistence operations in the domain layer. These interfaces follow
the Repository Pattern and Dependency Inversion Principle from Clean Architecture.

Infrastructure layer implementations will provide concrete implementations
of these interfaces.
"""

from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.repositories.i_task_repository import ITaskRepository
from jarvis_core.domain.repositories.i_agent_repository import IAgentRepository
from jarvis_core.domain.repositories.i_analytics_repository import IAnalyticsRepository

__all__ = [
    "IMemoryRepository",
    "ITaskRepository",
    "IAgentRepository",
    "IAnalyticsRepository",
]
