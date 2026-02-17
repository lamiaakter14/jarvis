"""AI Service Interface for application layer."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.domain.entities.plan import Plan
from jarvis_core.domain.entities.task import Task


class IAIService(ABC):
    """Abstract interface for AI-powered services.

    Defines the contract for AI services that provide intelligent
    capabilities like planning, gap analysis, innovation generation,
    and mentorship.
    """

    @abstractmethod
    async def generate_plan(self, context: Context) -> Plan:
        """Generate a daily plan based on current context.

        Uses AI to analyze context, priorities, and constraints to create
        an optimized daily plan with appropriate task selection and ordering.

        Args:
            context: Current execution context including goals, gaps, and resources

        Returns:
            Generated Plan with scheduled tasks

        Raises:
            AIServiceError: If plan generation fails
        """
        pass

    @abstractmethod
    async def analyze_gaps(self, execution_logs: List[Dict]) -> List[Dict]:
        """Analyze execution logs to identify knowledge and skill gaps.

        Uses AI to review execution history and identify patterns that
        indicate knowledge gaps, skill deficiencies, or learning opportunities.

        Args:
            execution_logs: List of execution log entries with task data

        Returns:
            List of identified gaps with type, description, severity, and evidence

        Raises:
            AIServiceError: If gap analysis fails
        """
        pass

    @abstractmethod
    async def generate_innovations(self, context: Context) -> List[Innovation]:
        """Generate innovative ideas and improvement suggestions.

        Uses AI to analyze current context, patterns, and performance to
        suggest novel approaches, optimizations, and creative solutions.

        Args:
            context: Current execution context

        Returns:
            List of Innovation entities with ideas and suggestions

        Raises:
            AIServiceError: If innovation generation fails
        """
        pass

    @abstractmethod
    async def provide_mentorship(self, task: Task) -> Dict[str, Any]:
        """Provide mentorship and guidance for a specific task.

        Uses AI to analyze task requirements and provide contextual
        guidance, best practices, potential pitfalls, and learning resources.

        Args:
            task: Task requiring mentorship

        Returns:
            Dictionary containing mentorship guidance:
                - guidance: Main guidance text
                - best_practices: List of best practice suggestions
                - resources: List of relevant learning resources
                - potential_issues: List of potential pitfalls to avoid

        Raises:
            AIServiceError: If mentorship generation fails
        """
        pass
