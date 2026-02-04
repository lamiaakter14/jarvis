"""Domain events for event-driven architecture."""

from jarvis_core.domain.events.base_event import BaseEvent
from jarvis_core.domain.events.task_completed import TaskCompletedEvent
from jarvis_core.domain.events.gap_identified import GapIdentifiedEvent
from jarvis_core.domain.events.innovation_created import InnovationCreatedEvent

__all__ = [
    "BaseEvent",
    "TaskCompletedEvent",
    "GapIdentifiedEvent",
    "InnovationCreatedEvent",
]
