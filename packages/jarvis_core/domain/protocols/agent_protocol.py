"""Agent Protocol for standardized agent interfaces."""

from typing import Any, Protocol

from jarvis_core.domain.entities.context import Context


class AgentProtocol(Protocol):
    """Protocol defining the standard interface for all agents."""

    async def execute(self, context: Context) -> Any:
        """Execute the agent's primary function."""
        ...

    def track_execution(self, success: bool, execution_time: float) -> None:
        """Track execution metrics for monitoring."""
        ...

    def get_metrics(self) -> dict[str, Any]:
        """Get execution metrics for the agent."""
        ...


def validate_agent_protocol(agent: Any) -> bool:
    """Validate that an agent conforms to the AgentProtocol."""
    required_methods = ["execute", "track_execution", "get_metrics"]

    for method in required_methods:
        if not hasattr(agent, method):
            return False
        if not callable(getattr(agent, method)):
            return False

    return True
