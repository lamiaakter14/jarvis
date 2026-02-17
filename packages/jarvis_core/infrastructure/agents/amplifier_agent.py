"""Amplifier agent implementation."""

import time
from typing import Any

from jarvis_core.domain.entities.agent import Agent
from jarvis_core.domain.repositories.i_memory_repository import IMemoryRepository
from jarvis_core.domain.value_objects.agent_type import AgentType
from jarvis_core.infrastructure.monitoring.metrics_collector import MetricsCollector
from jarvis_core.shared.exceptions import DomainException


class AmplifierAgent(Agent):
    """Amplifier agent for performance analysis and optimization.

    The amplifier analyzes performance metrics, identifies bottlenecks,
    and provides optimization recommendations to improve effectiveness.
    """

    def __init__(
        self,
        memory_repo: IMemoryRepository,
        metrics_collector: MetricsCollector,
    ):
        """Initialize amplifier agent.

        Args:
            memory_repo: Memory repository for accessing performance data
            metrics_collector: Metrics collector for performance tracking
        """
        super().__init__(
            agent_type=AgentType.AMPLIFIER,
            name="Amplifier Agent",
            description="Analyzes performance and optimizes effectiveness",
        )
        self.memory_repo = memory_repo
        self.metrics_collector = metrics_collector

    async def execute(self, context: Any = None) -> dict[str, Any]:
        """Execute amplifier's primary function: analyze and optimize.

        Args:
            context: Optional execution context

        Returns:
            Dictionary with performance analysis and recommendations

        Raises:
            DomainException: If execution fails
        """
        start_time = time.time()

        try:
            # Collect current metrics
            metrics = await self._collect_metrics()

            # Analyze performance
            analysis = await self.analyze_performance(metrics)

            # Generate optimization recommendations
            recommendations = await self.generate_recommendations(analysis)

            result = {
                "metrics": metrics,
                "analysis": analysis,
                "recommendations": recommendations,
            }

            execution_time = time.time() - start_time
            self.track_execution(success=True, execution_time=execution_time)

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            self.track_execution(success=False, execution_time=execution_time)
            raise DomainException(f"Amplifier execution failed: {e}")

    async def _collect_metrics(self) -> dict[str, Any]:
        """Collect current performance metrics.

        Returns:
            Dictionary with performance metrics
        """
        metrics = {
            "agent_metrics": {},
            "task_metrics": {},
            "system_metrics": {},
        }

        try:
            # Get agent metrics
            agent_metrics = self.metrics_collector.get_agent_metrics()
            metrics["agent_metrics"] = agent_metrics

            # Get task metrics
            task_metrics = self.metrics_collector.get_task_metrics()
            metrics["task_metrics"] = task_metrics

            # Get system metrics
            system_metrics = self.metrics_collector.get_system_metrics()
            metrics["system_metrics"] = system_metrics

        except Exception as e:
            print(f"Warning: Failed to collect some metrics: {e}")

        return metrics

    async def analyze_performance(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """Analyze performance metrics to identify patterns and issues.

        Args:
            metrics: Performance metrics

        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "bottlenecks": [],
            "strengths": [],
            "trends": [],
            "efficiency_score": 0.0,
        }

        # Analyze agent performance
        agent_metrics = metrics.get("agent_metrics", {})
        for agent_name, agent_data in agent_metrics.items():
            success_rate = agent_data.get("success_rate", 0)
            avg_time = agent_data.get("average_execution_time", 0)

            if success_rate < 0.7:
                analysis["bottlenecks"].append(
                    {
                        "area": f"Agent: {agent_name}",
                        "issue": "Low success rate",
                        "value": success_rate,
                        "severity": "high" if success_rate < 0.5 else "medium",
                    }
                )
            elif success_rate > 0.9:
                analysis["strengths"].append(
                    {
                        "area": f"Agent: {agent_name}",
                        "metric": "High success rate",
                        "value": success_rate,
                    }
                )

            if avg_time > 60:  # More than 1 minute
                analysis["bottlenecks"].append(
                    {
                        "area": f"Agent: {agent_name}",
                        "issue": "Slow execution time",
                        "value": avg_time,
                        "severity": "medium",
                    }
                )

        # Analyze task metrics
        task_metrics = metrics.get("task_metrics", {})
        completed_tasks = task_metrics.get("completed_tasks", 0)
        failed_tasks = task_metrics.get("failed_tasks", 0)
        total_tasks = completed_tasks + failed_tasks

        if total_tasks > 0:
            task_success_rate = completed_tasks / total_tasks

            if task_success_rate < 0.7:
                analysis["bottlenecks"].append(
                    {
                        "area": "Task Execution",
                        "issue": "High task failure rate",
                        "value": 1 - task_success_rate,
                        "severity": "high",
                    }
                )

            # Calculate efficiency score
            analysis["efficiency_score"] = task_success_rate * 100

        return analysis

    async def generate_recommendations(self, analysis: dict[str, Any]) -> list[str]:
        """Generate optimization recommendations based on analysis.

        Args:
            analysis: Performance analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Address bottlenecks
        bottlenecks = analysis.get("bottlenecks", [])
        high_severity = [b for b in bottlenecks if b.get("severity") == "high"]

        if high_severity:
            recommendations.append(
                f"URGENT: Address {len(high_severity)} high-severity bottlenecks"
            )
            for bottleneck in high_severity:
                recommendations.append(f"- Fix {bottleneck.get('area')}: {bottleneck.get('issue')}")

        # Leverage strengths
        strengths = analysis.get("strengths", [])
        if strengths:
            recommendations.append(
                f"Leverage {len(strengths)} identified strengths for better results"
            )

        # Efficiency improvements
        efficiency = analysis.get("efficiency_score", 0)
        if efficiency < 60:
            recommendations.append(
                "Overall efficiency is low - consider process review and optimization"
            )
        elif efficiency > 85:
            recommendations.append(
                "Excellent efficiency - maintain current practices and look for scaling opportunities"
            )

        if not recommendations:
            recommendations.append(
                "Performance is stable - continue monitoring for optimization opportunities"
            )

        return recommendations

    async def get_performance_summary(self) -> dict[str, Any]:
        """Get a high-level performance summary.

        Returns:
            Dictionary with performance summary
        """
        try:
            metrics = await self._collect_metrics()
            analysis = await self.analyze_performance(metrics)

            return {
                "efficiency_score": analysis.get("efficiency_score", 0),
                "bottleneck_count": len(analysis.get("bottlenecks", [])),
                "strength_count": len(analysis.get("strengths", [])),
                "status": self._determine_status(analysis),
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "unknown",
            }

    def _determine_status(self, analysis: dict[str, Any]) -> str:
        """Determine overall status based on analysis.

        Args:
            analysis: Performance analysis

        Returns:
            Status string (excellent, good, fair, poor)
        """
        efficiency = analysis.get("efficiency_score", 0)
        high_severity_bottlenecks = len(
            [b for b in analysis.get("bottlenecks", []) if b.get("severity") == "high"]
        )

        if high_severity_bottlenecks > 0:
            return "poor"
        elif efficiency >= 85:
            return "excellent"
        elif efficiency >= 70:
            return "good"
        elif efficiency >= 50:
            return "fair"
        else:
            return "poor"
