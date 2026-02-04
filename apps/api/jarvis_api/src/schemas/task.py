"""Task schemas."""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base task schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed|failed)$")


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|critical)$")
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed|failed)$")


class Task(TaskBase):
    """Task schema with ID."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
