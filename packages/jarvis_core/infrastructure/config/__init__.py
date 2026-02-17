"""Infrastructure configuration module."""

from jarvis_core.infrastructure.config.dependencies import (
    get_ai_service,
    get_ai_svc,
    get_amplifier_agent,
    get_executor_agent,
    get_innovator_agent,
    get_log,
    get_logger,
    get_memory_repo,
    get_memory_repository,
    get_mentor_agent,
    get_metrics,
    get_metrics_collector,
    get_strategist_agent,
    get_task_repo,
    get_task_repository,
    get_tracer,
    reset_dependencies,
)
from jarvis_core.infrastructure.config.settings import Settings, settings

__all__ = [
    "Settings",
    "settings",
    "get_memory_repository",
    "get_task_repository",
    "get_ai_service",
    "get_strategist_agent",
    "get_mentor_agent",
    "get_executor_agent",
    "get_innovator_agent",
    "get_amplifier_agent",
    "get_logger",
    "get_metrics_collector",
    "get_tracer",
    "get_memory_repo",
    "get_task_repo",
    "get_ai_svc",
    "get_log",
    "get_metrics",
    "reset_dependencies",
]
