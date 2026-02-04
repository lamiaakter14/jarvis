"""Base Agent entity for the domain layer."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

from src.domain.value_objects.agent_type import AgentType
from src.shared.utils import generate_id, current_timestamp


@dataclass
class Agent(ABC):
    """Abstract base class for all agents in the system.
    
    Agents are the core executors in JARVIS, each with specific capabilities
    and responsibilities. This class defines the common interface and behavior
    for all agent types.
    """
    
    agent_id: str = field(default_factory=lambda: generate_id("agent_"))
    agent_type: AgentType = field(default_factory=AgentType.executor)
    name: str = ""
    description: str = ""
    
    # Execution metrics
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    total_execution_time: float = 0.0
    last_execution_time: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate agent after initialization."""
        if not self.name:
            self.name = f"{self.agent_type.type.value.title()} Agent"
        if not self.description:
            self.description = self.agent_type.description
    
    @abstractmethod
    async def execute(self, context: Any) -> Any:
        """Execute the agent's primary function.
        
        Args:
            context: Execution context containing relevant data
            
        Returns:
            Result of the agent's execution
            
        Raises:
            DomainException: If execution fails
        """
        pass
    
    def track_execution(
        self,
        success: bool,
        execution_time: float
    ) -> None:
        """Track metrics for an execution.
        
        Args:
            success: Whether the execution was successful
            execution_time: Time taken for execution in seconds
        """
        self.total_executions += 1
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        self.total_execution_time += execution_time
        self.last_execution_time = current_timestamp()
    
    def get_success_rate(self) -> float:
        """Calculate the success rate of executions.
        
        Returns:
            Success rate as a percentage (0.0 to 1.0)
        """
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    def get_average_execution_time(self) -> float:
        """Calculate the average execution time.
        
        Returns:
            Average execution time in seconds
        """
        if self.total_executions == 0:
            return 0.0
        return self.total_execution_time / self.total_executions
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all execution metrics.
        
        Returns:
            Dictionary containing all metrics
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": str(self.agent_type),
            "name": self.name,
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "success_rate": self.get_success_rate(),
            "total_execution_time": self.total_execution_time,
            "average_execution_time": self.get_average_execution_time(),
            "last_execution_time": self.last_execution_time.isoformat() if self.last_execution_time else None,
        }
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.name} ({self.agent_type})"
    
    def __repr__(self) -> str:
        """Detailed representation of the agent."""
        return (
            f"Agent(id={self.agent_id}, type={self.agent_type}, "
            f"name={self.name}, executions={self.total_executions})"
        )
