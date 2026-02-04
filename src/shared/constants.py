"""Shared constants for the JARVIS application."""

from enum import Enum


class AgentType(str, Enum):
    """Available agent types in the system."""
    STRATEGIST = "strategist"
    MENTOR = "mentor"
    EXECUTOR = "executor"
    INNOVATOR = "innovator"
    AMPLIFIER = "amplifier"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MemoryType(str, Enum):
    """Types of memory in the system."""
    WORKING = "working"
    KNOWLEDGE = "knowledge"
    STRATEGIC = "strategic"
    EXECUTION_LOG = "execution_log"


class CognitiveLoadLevel(str, Enum):
    """Cognitive load levels for tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CognitiveLoopStatus(str, Enum):
    """Status of the cognitive loop."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


# System-wide constants
DEFAULT_MEMORY_DIR = "memory"
API_VERSION = "v1"
DEFAULT_AI_MODEL = "gpt-4"
MAX_DAILY_TASKS = 10
DEFAULT_WORK_HOURS = 8
