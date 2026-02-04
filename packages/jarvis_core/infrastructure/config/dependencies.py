"""Dependency injection container for the application."""

from typing import Optional
from functools import lru_cache

from jarvis_core.infrastructure.config.settings import settings
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository
from jarvis_core.infrastructure.persistence.sqlite_task_repository import SqliteTaskRepository
from jarvis_core.infrastructure.ai.openai_service import OpenAIService
from jarvis_core.infrastructure.agents.strategist_agent import StrategistAgent
from jarvis_core.infrastructure.agents.mentor_agent import MentorAgent
from jarvis_core.infrastructure.agents.executor_agent import ExecutorAgent
from jarvis_core.infrastructure.agents.innovator_agent import InnovatorAgent
from jarvis_core.infrastructure.agents.amplifier_agent import AmplifierAgent
from jarvis_core.infrastructure.monitoring.logger import Logger
from jarvis_core.infrastructure.monitoring.metrics_collector import MetricsCollector
from jarvis_core.infrastructure.monitoring.tracer import Tracer
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.repositories.i_task_repository import ITaskRepository
from jarvis_core.application.interfaces.i_ai_service import IAIService


# Repository Dependencies
@lru_cache()
def get_memory_repository() -> IMemoryRepository:
    """Get memory repository instance.
    
    Returns:
        Singleton instance of memory repository
    """
    return FileMemoryRepository(base_path=settings.memory_base_path)


@lru_cache()
def get_task_repository() -> ITaskRepository:
    """Get task repository instance.
    
    Returns:
        Singleton instance of task repository
    """
    return SqliteTaskRepository(db_path=settings.task_db_path)


# Service Dependencies
@lru_cache()
def get_ai_service() -> IAIService:
    """Get AI service instance.
    
    Returns:
        Singleton instance of AI service
    """
    return OpenAIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
        timeout=settings.openai_timeout,
        mock_mode=settings.enable_mock_mode,
    )


# Agent Dependencies
@lru_cache()
def get_strategist_agent() -> StrategistAgent:
    """Get strategist agent instance.
    
    Returns:
        Singleton instance of strategist agent
    """
    return StrategistAgent(
        ai_service=get_ai_service(),
        memory_repo=get_memory_repository(),
        task_repo=get_task_repository(),
    )


@lru_cache()
def get_mentor_agent() -> MentorAgent:
    """Get mentor agent instance.
    
    Returns:
        Singleton instance of mentor agent
    """
    return MentorAgent(
        ai_service=get_ai_service(),
        memory_repo=get_memory_repository(),
    )


@lru_cache()
def get_executor_agent() -> ExecutorAgent:
    """Get executor agent instance.
    
    Returns:
        Singleton instance of executor agent
    """
    return ExecutorAgent(
        task_repo=get_task_repository(),
        memory_repo=get_memory_repository(),
    )


@lru_cache()
def get_innovator_agent() -> InnovatorAgent:
    """Get innovator agent instance.
    
    Returns:
        Singleton instance of innovator agent
    """
    return InnovatorAgent(
        ai_service=get_ai_service(),
        memory_repo=get_memory_repository(),
    )


@lru_cache()
def get_amplifier_agent() -> AmplifierAgent:
    """Get amplifier agent instance.
    
    Returns:
        Singleton instance of amplifier agent
    """
    return AmplifierAgent(
        memory_repo=get_memory_repository(),
        metrics_collector=get_metrics_collector(),
    )


# Monitoring Dependencies
@lru_cache()
def get_logger() -> Logger:
    """Get logger instance.
    
    Returns:
        Singleton instance of logger
    """
    return Logger(
        level=settings.log_level,
        log_file=settings.log_file,
        log_format=settings.log_format,
    )


@lru_cache()
def get_metrics_collector() -> MetricsCollector:
    """Get metrics collector instance.
    
    Returns:
        Singleton instance of metrics collector
    """
    return MetricsCollector(
        enabled=settings.enable_metrics,
        metrics_file=settings.metrics_file,
    )


@lru_cache()
def get_tracer() -> Tracer:
    """Get tracer instance.
    
    Returns:
        Singleton instance of tracer
    """
    return Tracer(enabled=settings.enable_tracing)


# FastAPI dependency functions (for use with Depends)
def get_memory_repo() -> IMemoryRepository:
    """FastAPI dependency for memory repository."""
    return get_memory_repository()


def get_task_repo() -> ITaskRepository:
    """FastAPI dependency for task repository."""
    return get_task_repository()


def get_ai_svc() -> IAIService:
    """FastAPI dependency for AI service."""
    return get_ai_service()


def get_log() -> Logger:
    """FastAPI dependency for logger."""
    return get_logger()


def get_metrics() -> MetricsCollector:
    """FastAPI dependency for metrics collector."""
    return get_metrics_collector()


# Utility function to reset all caches (useful for testing)
def reset_dependencies():
    """Reset all cached dependencies."""
    get_memory_repository.cache_clear()
    get_task_repository.cache_clear()
    get_ai_service.cache_clear()
    get_strategist_agent.cache_clear()
    get_mentor_agent.cache_clear()
    get_executor_agent.cache_clear()
    get_innovator_agent.cache_clear()
    get_amplifier_agent.cache_clear()
    get_logger.cache_clear()
    get_metrics_collector.cache_clear()
    get_tracer.cache_clear()
