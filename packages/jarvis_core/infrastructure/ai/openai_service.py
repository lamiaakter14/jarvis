"""OpenAI-based AI service implementation."""

import json
import logging
from typing import Any, Optional

from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.domain.entities.context import Context
from jarvis_core.domain.entities.innovation import Innovation
from jarvis_core.domain.entities.plan import Plan
from jarvis_core.domain.entities.task import Task
from jarvis_core.domain.value_objects.cognitive_load import CognitiveLoad
from jarvis_core.domain.value_objects.priority import Priority
from jarvis_core.domain.value_objects.roi import ROI
from jarvis_core.shared.exceptions import AIServiceError


class OpenAIService(IAIService):
    """OpenAI-based implementation of AI service.

    Uses OpenAI GPT models for intelligent operations like planning,
    gap analysis, innovation generation, and mentorship.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        timeout: int = 60,
        mock_mode: bool = False,
    ):
        """Initialize OpenAI service.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            temperature: Temperature for generation
            max_tokens: Maximum tokens per request
            timeout: API request timeout in seconds
            mock_mode: Use mock responses instead of real API
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.mock_mode = mock_mode

        if not mock_mode and not api_key:
            raise AIServiceError("OpenAI API key is required when not in mock mode")

        # Initialize OpenAI client if not in mock mode
        if not mock_mode:
            try:
                import openai

                self.client = openai.OpenAI(api_key=api_key, timeout=timeout)
            except ImportError:
                raise AIServiceError("openai package is required but not installed")
        else:
            self.client = None

    async def generate_plan(self, context: Context) -> Plan:
        """Generate a daily plan based on current context.

        Args:
            context: Current execution context

        Returns:
            Generated Plan with scheduled tasks

        Raises:
            AIServiceError: If plan generation fails
        """
        if self.mock_mode:
            return self._generate_mock_plan(context)

        try:
            prompt = self._build_plan_prompt(context)
            response = self._call_openai(prompt)
            plan = self._parse_plan_response(response, context)
            return plan
        except Exception as e:
            raise AIServiceError(f"Failed to generate plan: {e}")

    async def analyze_gaps(self, execution_logs: list[dict]) -> list[dict]:
        """Analyze execution logs to identify knowledge and skill gaps.

        Args:
            execution_logs: List of execution log entries

        Returns:
            List of identified gaps

        Raises:
            AIServiceError: If gap analysis fails
        """
        if self.mock_mode:
            return self._generate_mock_gaps(execution_logs)

        try:
            prompt = self._build_gaps_prompt(execution_logs)
            response = self._call_openai(prompt)
            gaps = self._parse_gaps_response(response)
            return gaps
        except Exception as e:
            raise AIServiceError(f"Failed to analyze gaps: {e}")

    async def generate_innovations(self, context: Context) -> list[Innovation]:
        """Generate innovative ideas and improvement suggestions.

        Args:
            context: Current execution context

        Returns:
            List of Innovation entities

        Raises:
            AIServiceError: If innovation generation fails
        """
        if self.mock_mode:
            return self._generate_mock_innovations(context)

        try:
            prompt = self._build_innovations_prompt(context)
            response = self._call_openai(prompt)
            innovations = self._parse_innovations_response(response)
            return innovations
        except Exception as e:
            raise AIServiceError(f"Failed to generate innovations: {e}")

    async def provide_mentorship(self, task: Task) -> dict[str, Any]:
        """Provide mentorship and guidance for a specific task.

        Args:
            task: Task requiring mentorship

        Returns:
            Dictionary containing mentorship guidance

        Raises:
            AIServiceError: If mentorship generation fails
        """
        if self.mock_mode:
            return self._generate_mock_mentorship(task)

        try:
            prompt = self._build_mentorship_prompt(task)
            response = self._call_openai(prompt)
            mentorship = self._parse_mentorship_response(response)
            return mentorship
        except Exception as e:
            raise AIServiceError(f"Failed to provide mentorship: {e}")

    def _call_openai(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Call OpenAI API with a prompt.

        Args:
            prompt: User prompt
            system_message: Optional system message

        Returns:
            Response text

        Raises:
            AIServiceError: If API call fails
        """
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            return response.choices[0].message.content
        except Exception as e:
            raise AIServiceError(f"OpenAI API call failed: {e}")

    def _build_plan_prompt(self, context: Context) -> str:
        """Build prompt for plan generation."""
        return f"""Generate a daily plan based on the following context:

Available Hours: {context.available_hours}
Current Focus Areas: {', '.join(context.current_focus) if context.current_focus else 'None'}
Strategic Goals: {', '.join(context.strategic_goals) if context.strategic_goals else 'None'}
Known Gaps: {len(context.gaps)} gaps identified
Recent Reflections: {len(context.reflections)} reflections

Create 3-5 tasks that:
1. Align with strategic goals
2. Address identified gaps
3. Fit within available hours
4. Balance high-priority and high-ROI items

Return tasks in JSON format:
[
  {{
    "title": "Task title",
    "description": "Task description",
    "priority": "high|medium|low",
    "estimated_hours": 2.0,
    "roi": 0.8,
    "agent_type": "executor"
  }}
]
"""

    def _build_gaps_prompt(self, execution_logs: list[dict]) -> str:
        """Build prompt for gap analysis."""
        logs_summary = "\n".join(
            [
                f"- {log.get('task', 'Unknown')}: {log.get('status', 'unknown')} "
                f"({log.get('notes', 'no notes')})"
                for log in execution_logs[:10]  # Limit to recent logs
            ]
        )

        return f"""Analyze the following execution logs to identify knowledge and skill gaps:

{logs_summary}

Identify patterns that indicate:
1. Knowledge gaps (missing information or understanding)
2. Skill gaps (technical abilities that need development)
3. Process gaps (workflow or methodology issues)

Return gaps in JSON format:
[
  {{
    "type": "knowledge|skill|process",
    "description": "Gap description",
    "severity": "high|medium|low",
    "evidence": ["Evidence 1", "Evidence 2"]
  }}
]
"""

    def _build_innovations_prompt(self, context: Context) -> str:
        """Build prompt for innovation generation."""
        return f"""Based on the current context, suggest innovative improvements:

Focus Areas: {', '.join(context.current_focus) if context.current_focus else 'None'}
Strategic Goals: {', '.join(context.strategic_goals) if context.strategic_goals else 'None'}

Suggest 2-3 innovations that:
1. Optimize current workflows
2. Introduce novel approaches
3. Leverage emerging technologies or methodologies
4. Have high potential impact

Return innovations in JSON format:
[
  {{
    "title": "Innovation title",
    "description": "Detailed description",
    "category": "process|technical|strategic",
    "impact_score": 0.8
  }}
]
"""

    def _build_mentorship_prompt(self, task: Task) -> str:
        """Build prompt for mentorship generation."""
        return f"""Provide mentorship guidance for the following task:

Task: {task.title}
Description: {task.description}
Priority: {task.priority.level.value}
Estimated Effort: {task.cognitive_load.estimated_hours} hours

Provide:
1. Main guidance for approaching this task
2. Best practices to follow
3. Common pitfalls to avoid
4. Relevant learning resources

Return in JSON format:
{{
  "guidance": "Main guidance text",
  "best_practices": ["Practice 1", "Practice 2"],
  "potential_issues": ["Issue 1", "Issue 2"],
  "resources": ["Resource 1", "Resource 2"]
}}
"""

    def _parse_plan_response(self, response: str, context: Context) -> Plan:
        """Parse AI response into a Plan entity."""
        try:
            # Extract JSON from response
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array found in response")

            tasks_data = json.loads(response[json_start:json_end])

            plan = Plan(
                date=context.date,
                total_hours=context.available_hours,
                created_by="ai_strategist",
            )

            for task_data in tasks_data:
                task = Task(
                    title=task_data["title"],
                    description=task_data.get("description", ""),
                    priority=Priority.from_level(task_data.get("priority", "medium")),
                    cognitive_load=CognitiveLoad(
                        level="medium",
                        estimated_hours=task_data.get("estimated_hours", 2.0),
                    ),
                    roi=ROI(task_data.get("roi", 0.5)),
                )
                try:
                    plan.add_task(task)
                except (ValueError, TypeError) as e:
                    logging.getLogger(__name__).info(
                        "Skipping task that doesn't fit plan constraints: %s", e
                    )
                    continue
                except Exception:
                    logging.getLogger(__name__).exception(
                        "Unexpected error adding task to plan; skipping"
                    )
                    continue

            return plan
        except Exception as e:
            raise AIServiceError(f"Failed to parse plan response: {e}")

    def _parse_gaps_response(self, response: str) -> list[dict]:
        """Parse AI response into gap list."""
        try:
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array found in response")

            gaps = json.loads(response[json_start:json_end])
            return gaps
        except Exception as e:
            raise AIServiceError(f"Failed to parse gaps response: {e}")

    def _parse_innovations_response(self, response: str) -> list[Innovation]:
        """Parse AI response into Innovation entities."""
        try:
            json_start = response.find("[")
            json_end = response.rfind("]") + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON array found in response")

            innovations_data = json.loads(response[json_start:json_end])

            innovations = []
            for inn_data in innovations_data:
                innovation = Innovation(
                    title=inn_data["title"],
                    description=inn_data.get("description", ""),
                    category=inn_data.get("category", "general"),
                    impact_score=inn_data.get("impact_score", 0.5),
                    created_by="ai_innovator",
                )
                innovations.append(innovation)

            return innovations
        except Exception as e:
            raise AIServiceError(f"Failed to parse innovations response: {e}")

    def _parse_mentorship_response(self, response: str) -> dict[str, Any]:
        """Parse AI response into mentorship dictionary."""
        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in response")

            mentorship = json.loads(response[json_start:json_end])
            return mentorship
        except Exception as e:
            raise AIServiceError(f"Failed to parse mentorship response: {e}")

    # Mock response generators
    def _generate_mock_plan(self, context: Context) -> Plan:
        """Generate a mock plan for testing."""
        plan = Plan(
            date=context.date,
            total_hours=context.available_hours,
            created_by="mock_ai",
        )

        # Add sample tasks
        task1 = Task(
            title="Review and prioritize tasks",
            description="Review task backlog and prioritize items",
            priority=Priority.high(),
            cognitive_load=CognitiveLoad("low", 1.0),
            roi=ROI(0.7),
        )

        task2 = Task(
            title="Implement core feature",
            description="Implement main functionality",
            priority=Priority.high(),
            cognitive_load=CognitiveLoad("high", 3.0),
            roi=ROI(0.9),
        )

        try:
            plan.add_task(task1)
            plan.add_task(task2)
        except Exception:
            logging.getLogger(__name__).exception("Failed to add mock tasks to plan")

        return plan

    def _generate_mock_gaps(self, execution_logs: list[dict]) -> list[dict]:
        """Generate mock gaps for testing."""
        return [
            {
                "type": "knowledge",
                "description": "Limited understanding of async patterns",
                "severity": "medium",
                "evidence": ["Multiple async-related errors in logs"],
            },
            {
                "type": "skill",
                "description": "Need to improve testing practices",
                "severity": "low",
                "evidence": ["Low test coverage in recent tasks"],
            },
        ]

    def _generate_mock_innovations(self, context: Context) -> list[Innovation]:
        """Generate mock innovations for testing."""
        return [
            Innovation(
                title="Automated task prioritization",
                description="Implement ML-based task prioritization system",
                category="technical",
                impact_score=0.8,
                created_by="mock_ai",
            ),
            Innovation(
                title="Knowledge base integration",
                description="Integrate external knowledge sources for better context",
                category="strategic",
                impact_score=0.7,
                created_by="mock_ai",
            ),
        ]

    def _generate_mock_mentorship(self, task: Task) -> dict[str, Any]:
        """Generate mock mentorship for testing."""
        return {
            "guidance": f"For '{task.title}', start by breaking down the work into smaller steps. "
            "Focus on understanding requirements before implementation.",
            "best_practices": [
                "Write tests first (TDD approach)",
                "Document your code as you go",
                "Seek feedback early and often",
            ],
            "potential_issues": [
                "Scope creep - keep focused on core requirements",
                "Over-engineering - start simple, refactor later",
            ],
            "resources": [
                "Official documentation",
                "Best practices guide",
                "Community forums",
            ],
        }
