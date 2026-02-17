"""Base domain event class for event-driven architecture."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from jarvis_core.shared.utils import current_timestamp, generate_id


@dataclass(frozen=True)
class BaseEvent:
    """Base class for all domain events in the JARVIS system.

    Domain events represent significant occurrences within the domain
    that other parts of the system may need to react to. Events are
    immutable and contain all necessary information about what happened.
    """

    event_id: str = field(default_factory=lambda: generate_id("evt_"))
    event_type: str = field(default="")
    timestamp: datetime = field(default_factory=current_timestamp)
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate event after initialization."""
        # Set event_type if not provided (use class name)
        if not self.event_type:
            object.__setattr__(self, "event_type", self.__class__.__name__)

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary representation.

        Returns:
            Dictionary containing all event data
        """
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "payload": self.payload,
        }

    def __str__(self) -> str:
        """String representation of the event."""
        return f"{self.event_type}({self.event_id})"

    def __repr__(self) -> str:
        """Detailed representation of the event."""
        return f"{self.event_type}(id={self.event_id}, " f"timestamp={self.timestamp.isoformat()})"
