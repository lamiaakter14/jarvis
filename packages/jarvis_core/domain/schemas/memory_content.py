"""Schema definitions for memory content validation using Pydantic."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WorkingMemoryContent(BaseModel):
    """Schema for working memory content.

    Working memory holds temporary data needed during execution,
    such as intermediate results or agent state.
    """

    model_config = ConfigDict(extra="allow")

    data: dict[str, Any] = Field(..., description="Working memory data")
    session_id: Optional[str] = Field(None, description="Session identifier")
    agent_id: Optional[str] = Field(None, description="Agent that created this memory")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")


class KnowledgeMemoryContent(BaseModel):
    """Schema for knowledge memory content.

    Knowledge memory stores long-term information and learned facts.
    """

    model_config = ConfigDict(extra="allow")

    title: str = Field(..., min_length=1, description="Knowledge title")
    description: str = Field(default="", description="Knowledge description")
    content: str = Field(..., min_length=1, description="Knowledge content")
    category: Optional[str] = Field(None, description="Knowledge category")
    tags: list[str] = Field(default_factory=list, description="Knowledge tags for indexing")
    source: Optional[str] = Field(None, description="Source of this knowledge")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    last_accessed: Optional[datetime] = Field(None, description="Last access timestamp")
    access_count: int = Field(default=0, ge=0, description="Number of times accessed")


class StrategicMemoryContent(BaseModel):
    """Schema for strategic memory content.

    Strategic memory stores long-term goals, plans, and strategic decisions.
    """

    model_config = ConfigDict(extra="allow")

    goal: str = Field(..., min_length=1, description="Strategic goal")
    description: str = Field(default="", description="Goal description")
    priority: str = Field(..., description="Goal priority (low, medium, high, critical)")
    status: str = Field(
        default="active", description="Goal status (active, paused, completed, cancelled)"
    )
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress percentage")
    milestones: list[dict[str, Any]] = Field(default_factory=list, description="List of milestones")
    dependencies: list[str] = Field(default_factory=list, description="Dependencies on other goals")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Success metrics")

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority value."""
        valid_priorities = ["low", "medium", "high", "critical"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v.lower()

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status value."""
        valid_statuses = ["active", "paused", "completed", "cancelled"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return v.lower()


class ExecutionLogContent(BaseModel):
    """Schema for execution log memory content.

    Execution logs store records of task executions and their results.
    """

    model_config = ConfigDict(extra="allow")

    task_id: str = Field(..., description="Task identifier")
    task_title: str = Field(..., description="Task title")
    agent_type: Optional[str] = Field(None, description="Agent that executed the task")
    status: str = Field(..., description="Execution status")
    started_at: datetime = Field(..., description="Execution start time")
    completed_at: Optional[datetime] = Field(None, description="Execution completion time")
    duration_seconds: Optional[float] = Field(None, ge=0, description="Execution duration")
    result: Optional[Any] = Field(None, description="Execution result")
    error: Optional[str] = Field(None, description="Error message if failed")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Execution metrics")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate execution status."""
        valid_statuses = ["pending", "in_progress", "completed", "failed", "cancelled"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return v.lower()


class ADRContent(BaseModel):
    """Schema for Architecture Decision Record (ADR) content.

    ADRs document important architectural decisions and their rationale.
    """

    model_config = ConfigDict(extra="allow")

    title: str = Field(..., min_length=1, description="ADR title")
    status: str = Field(
        default="proposed", description="ADR status (proposed, accepted, deprecated, superseded)"
    )
    date: datetime = Field(..., description="Decision date")
    context: str = Field(..., min_length=1, description="Context and background")
    decision: str = Field(..., min_length=1, description="The decision made")
    consequences: str = Field(..., min_length=1, description="Consequences of the decision")
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative options considered"
    )
    related_decisions: list[str] = Field(default_factory=list, description="Related ADR IDs")
    superseded_by: Optional[str] = Field(None, description="ADR ID that supersedes this one")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate ADR status."""
        valid_statuses = ["proposed", "accepted", "deprecated", "superseded"]
        if v.lower() not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        return v.lower()


def validate_memory_content(memory_type: str, content: dict[str, Any]) -> BaseModel:
    """Validate memory content against its type-specific schema.

    Args:
        memory_type: Type of memory (working, knowledge, strategic, execution_log, adr)
        content: Content dictionary to validate

    Returns:
        Validated Pydantic model instance

    Raises:
        ValueError: If memory type is invalid or content validation fails
    """
    schema_map = {
        "working": WorkingMemoryContent,
        "knowledge": KnowledgeMemoryContent,
        "strategic": StrategicMemoryContent,
        "execution_log": ExecutionLogContent,
        "adr": ADRContent,
    }

    schema_class = schema_map.get(memory_type.lower())
    if schema_class is None:
        raise ValueError(f"Unknown memory type: {memory_type}")

    # Validate and return the model
    return schema_class(**content)
