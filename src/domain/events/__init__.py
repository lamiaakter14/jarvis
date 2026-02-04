"""Domain events for event-driven architecture."""

from src.domain.events.base_event import BaseEvent
from src.domain.events.task_completed import TaskCompletedEvent
from src.domain.events.gap_identified import GapIdentifiedEvent
from src.domain.events.innovation_created import InnovationCreatedEvent

__all__ = [
    "BaseEvent",
    "TaskCompletedEvent",
    "GapIdentifiedEvent",
    "InnovationCreatedEvent",
]
