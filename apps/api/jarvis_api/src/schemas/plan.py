"""Plan schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PlanItem(BaseModel):
    """Individual plan item."""

    task_id: str
    title: str
    priority: str
    estimated_duration: Optional[str] = None


class PlanBase(BaseModel):
    """Base plan schema."""

    date: str
    focus_area: Optional[str] = None
    tasks: list[PlanItem] = []


class Plan(PlanBase):
    """Plan schema with metadata."""

    id: str
    created_at: datetime

    class Config:
        from_attributes = True
