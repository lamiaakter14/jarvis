"""Context entity for the domain layer."""

from dataclasses import dataclass, field
from typing import Any, Optional

from jarvis_core.shared.exceptions import DomainException
from jarvis_core.shared.utils import current_date, generate_id


@dataclass
class Context:
    """Context entity representing the execution environment for agents.

    Context provides agents with situational awareness including current focus,
    available resources, strategic goals, and identified gaps.
    """

    context_id: str = field(default_factory=lambda: generate_id("ctx_"))
    date: date = field(default_factory=current_date)

    current_focus: list[str] = field(default_factory=list)
    available_hours: float = 8.0
    daily_plan: dict[str, Any] = field(default_factory=dict)
    gaps: list[dict[str, Any]] = field(default_factory=list)
    reflections: list[str] = field(default_factory=list)
    strategic_goals: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate context after initialization."""
        if self.available_hours < 0:
            raise DomainException("Available hours cannot be negative")
        if self.available_hours > 24:
            raise DomainException("Available hours cannot exceed 24")

    def add_focus_area(self, focus: str) -> None:
        """Add a focus area to the current context.

        Args:
            focus: Focus area description

        Raises:
            DomainException: If focus is empty
        """
        if not focus or not focus.strip():
            raise DomainException("Focus area cannot be empty")

        if focus not in self.current_focus:
            self.current_focus.append(focus)

    def remove_focus_area(self, focus: str) -> None:
        """Remove a focus area from the current context.

        Args:
            focus: Focus area description to remove
        """
        if focus in self.current_focus:
            self.current_focus.remove(focus)

    def update_available_hours(self, hours: float) -> None:
        """Update the available hours for the day.

        Args:
            hours: New available hours

        Raises:
            DomainException: If hours are invalid
        """
        if hours < 0:
            raise DomainException("Available hours cannot be negative")
        if hours > 24:
            raise DomainException("Available hours cannot exceed 24")

        self.available_hours = hours

    def consume_hours(self, hours: float) -> None:
        """Consume hours from available time.

        Args:
            hours: Hours to consume

        Raises:
            DomainException: If not enough hours available
        """
        if hours > self.available_hours:
            raise DomainException(
                f"Cannot consume {hours} hours, only {self.available_hours} available"
            )

        self.available_hours -= hours

    def add_gap(
        self,
        gap_type: str,
        description: str,
        severity: str = "medium",
        evidence: Optional[list[str]] = None,
    ) -> None:
        """Add a knowledge or skill gap to the context.

        Args:
            gap_type: Type of gap (e.g., "knowledge", "skill", "process")
            description: Description of the gap
            severity: Severity level (low, medium, high)
            evidence: Optional list of evidence items
        """
        gap = {
            "type": gap_type,
            "description": description,
            "severity": severity,
            "evidence": evidence or [],
        }
        self.gaps.append(gap)

    def add_reflection(self, reflection: str) -> None:
        """Add a reflection to the context.

        Args:
            reflection: Reflection text

        Raises:
            DomainException: If reflection is empty
        """
        if not reflection or not reflection.strip():
            raise DomainException("Reflection cannot be empty")

        self.reflections.append(reflection)

    def add_strategic_goal(self, goal: str) -> None:
        """Add a strategic goal to the context.

        Args:
            goal: Strategic goal description

        Raises:
            DomainException: If goal is empty
        """
        if not goal or not goal.strip():
            raise DomainException("Strategic goal cannot be empty")

        if goal not in self.strategic_goals:
            self.strategic_goals.append(goal)

    def has_available_hours(self, required_hours: float) -> bool:
        """Check if required hours are available.

        Args:
            required_hours: Hours required

        Returns:
            True if enough hours are available
        """
        return self.available_hours >= required_hours

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the context.

        Returns:
            Dictionary containing context summary
        """
        return {
            "context_id": self.context_id,
            "date": self.date.isoformat(),
            "available_hours": self.available_hours,
            "focus_areas": len(self.current_focus),
            "focus_list": self.current_focus,
            "gaps_count": len(self.gaps),
            "reflections_count": len(self.reflections),
            "strategic_goals_count": len(self.strategic_goals),
            "has_plan": bool(self.daily_plan),
        }

    def get_high_severity_gaps(self) -> list[dict[str, Any]]:
        """Get all high severity gaps.

        Returns:
            List of high severity gaps
        """
        return [gap for gap in self.gaps if gap.get("severity") == "high"]

    def get_gaps_by_type(self, gap_type: str) -> list[dict[str, Any]]:
        """Get gaps filtered by type.

        Args:
            gap_type: Type of gap to filter

        Returns:
            List of gaps matching the type
        """
        return [gap for gap in self.gaps if gap.get("type") == gap_type]

    def __str__(self) -> str:
        """String representation of the context."""
        return f"Context for {self.date} ({self.available_hours}h available)"

    def __repr__(self) -> str:
        """Detailed representation of the context."""
        return (
            f"Context(id={self.context_id}, date={self.date}, "
            f"hours={self.available_hours}, focus={len(self.current_focus)})"
        )
