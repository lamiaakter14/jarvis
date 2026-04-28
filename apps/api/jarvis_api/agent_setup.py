"""Agent setup factory for the JARVIS FastAPI application.

Creates and wires all agents with their required dependencies.
Uses mock_mode=True for the AI service when no OpenAI API key is set.
"""

import os
from dataclasses import dataclass

from jarvis_core.infrastructure.agents.amplifier_agent import AmplifierAgent
from jarvis_core.infrastructure.agents.executor_agent import ExecutorAgent
from jarvis_core.infrastructure.agents.innovator_agent import InnovatorAgent
from jarvis_core.infrastructure.agents.mentor_agent import MentorAgent
from jarvis_core.infrastructure.agents.strategist_agent import StrategistAgent
from jarvis_core.infrastructure.ai.openai_service import OpenAIService
from jarvis_core.infrastructure.monitoring.metrics_collector import MetricsCollector
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
from jarvis_core.infrastructure.persistence.sqlite_task_repository import SqliteTaskRepository


@dataclass
class Agents:
    """Container for all instantiated JARVIS agents."""

    strategist: StrategistAgent
    mentor: MentorAgent
    executor: ExecutorAgent
    innovator: InnovatorAgent
    amplifier: AmplifierAgent


def create_agents(
    db_path: str = "memory/tasks.db",
    memory_path: str = "memory",
) -> Agents:
    """Create and wire all agents with their dependencies.

    Uses mock_mode=True for the AI service when the OPENAI_API_KEY
    environment variable is not set, so the app runs without a real key.

    Args:
        db_path: Path to the SQLite database file for task persistence.
        memory_path: Base directory for file-based memory storage.

    Returns:
        Agents dataclass containing all five instantiated agents.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    mock_mode = not bool(api_key)

    ai_service = OpenAIService(api_key=api_key, mock_mode=mock_mode)
    task_repo = SqliteTaskRepository(db_path=db_path)
    memory_repo = FileMemoryRepository(base_path=memory_path)
    metrics_collector = MetricsCollector()

    return Agents(
        strategist=StrategistAgent(
            ai_service=ai_service,
            memory_repo=memory_repo,
            task_repo=task_repo,
        ),
        mentor=MentorAgent(
            ai_service=ai_service,
            memory_repo=memory_repo,
        ),
        executor=ExecutorAgent(
            task_repo=task_repo,
            memory_repo=memory_repo,
        ),
        innovator=InnovatorAgent(
            ai_service=ai_service,
            memory_repo=memory_repo,
        ),
        amplifier=AmplifierAgent(
            memory_repo=memory_repo,
            metrics_collector=metrics_collector,
        ),
    )
