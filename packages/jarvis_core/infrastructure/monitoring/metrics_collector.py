"""Metrics collector for performance tracking."""

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class MetricsCollector:
    """Metrics collector for tracking application performance.

    Collects and stores metrics about agent execution, task completion,
    system performance, and other operational data.
    """

    def __init__(
        self,
        enabled: bool = True,
        metrics_file: Optional[str] = None,
    ):
        """Initialize metrics collector.

        Args:
            enabled: Whether metrics collection is enabled
            metrics_file: Optional path to metrics file
        """
        self.enabled = enabled
        self.metrics_file = Path(metrics_file) if metrics_file else None

        # In-memory metrics storage
        self.agent_metrics: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "total_time": 0.0,
                "executions": [],
            }
        )

        self.task_metrics: Dict[str, int] = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "pending_tasks": 0,
            "in_progress_tasks": 0,
        }

        self.system_metrics: Dict[str, Any] = {
            "start_time": datetime.now().isoformat(),
            "api_requests": 0,
            "errors": 0,
        }

        # Load existing metrics if file exists
        if self.enabled and self.metrics_file and self.metrics_file.exists():
            self._load_metrics()

    def record_agent_execution(
        self,
        agent_name: str,
        success: bool,
        duration: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record agent execution metrics.

        Args:
            agent_name: Name of the agent
            success: Whether execution was successful
            duration: Execution duration in seconds
            metadata: Optional additional metadata
        """
        if not self.enabled:
            return

        metrics = self.agent_metrics[agent_name]
        metrics["total_executions"] += 1

        if success:
            metrics["successful_executions"] += 1
        else:
            metrics["failed_executions"] += 1

        metrics["total_time"] += duration

        # Record individual execution
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration,
        }

        if metadata:
            execution_record["metadata"] = metadata

        metrics["executions"].append(execution_record)

        # Keep only last 100 executions to limit memory
        if len(metrics["executions"]) > 100:
            metrics["executions"] = metrics["executions"][-100:]

        # Calculate derived metrics
        metrics["success_rate"] = (
            metrics["successful_executions"] / metrics["total_executions"]
            if metrics["total_executions"] > 0
            else 0.0
        )
        metrics["average_execution_time"] = (
            metrics["total_time"] / metrics["total_executions"]
            if metrics["total_executions"] > 0
            else 0.0
        )

        self._persist_metrics()

    def record_task_status(
        self,
        status: str,
        increment: int = 1,
    ) -> None:
        """Record task status change.

        Args:
            status: Task status (completed, failed, pending, in_progress)
            increment: Increment value
        """
        if not self.enabled:
            return

        status_key = f"{status}_tasks"
        if status_key in self.task_metrics:
            self.task_metrics[status_key] += increment
            self.task_metrics["total_tasks"] += increment

        self._persist_metrics()

    def record_api_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration: float,
    ) -> None:
        """Record API request metrics.

        Args:
            endpoint: API endpoint
            method: HTTP method
            status_code: Response status code
            duration: Request duration in seconds
        """
        if not self.enabled:
            return

        self.system_metrics["api_requests"] += 1

        if status_code >= 400:
            self.system_metrics["errors"] += 1

        self._persist_metrics()

    def record_error(self, error_type: str, message: str) -> None:
        """Record error occurrence.

        Args:
            error_type: Type of error
            message: Error message
        """
        if not self.enabled:
            return

        self.system_metrics["errors"] += 1

        if "error_log" not in self.system_metrics:
            self.system_metrics["error_log"] = []

        self.system_metrics["error_log"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "type": error_type,
                "message": message,
            }
        )

        # Keep only last 50 errors
        if len(self.system_metrics["error_log"]) > 50:
            self.system_metrics["error_log"] = self.system_metrics["error_log"][-50:]

        self._persist_metrics()

    def get_agent_metrics(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get agent metrics.

        Args:
            agent_name: Optional specific agent name

        Returns:
            Dictionary with agent metrics
        """
        if agent_name:
            return dict(self.agent_metrics.get(agent_name, {}))
        return {name: dict(metrics) for name, metrics in self.agent_metrics.items()}

    def get_task_metrics(self) -> Dict[str, int]:
        """Get task metrics.

        Returns:
            Dictionary with task metrics
        """
        return dict(self.task_metrics)

    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system metrics.

        Returns:
            Dictionary with system metrics
        """
        return dict(self.system_metrics)

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics.

        Returns:
            Dictionary with all metrics
        """
        return {
            "agent_metrics": self.get_agent_metrics(),
            "task_metrics": self.get_task_metrics(),
            "system_metrics": self.get_system_metrics(),
            "collected_at": datetime.now().isoformat(),
        }

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.agent_metrics.clear()
        self.task_metrics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "pending_tasks": 0,
            "in_progress_tasks": 0,
        }
        self.system_metrics = {
            "start_time": datetime.now().isoformat(),
            "api_requests": 0,
            "errors": 0,
        }

        self._persist_metrics()

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a high-level performance summary.

        Returns:
            Dictionary with performance summary
        """
        agent_metrics = self.get_agent_metrics()
        task_metrics = self.get_task_metrics()

        # Calculate overall success rates
        total_agent_executions = sum(m.get("total_executions", 0) for m in agent_metrics.values())
        total_agent_success = sum(m.get("successful_executions", 0) for m in agent_metrics.values())

        agent_success_rate = (
            total_agent_success / total_agent_executions if total_agent_executions > 0 else 0.0
        )

        total_tasks = task_metrics.get("total_tasks", 0)
        completed_tasks = task_metrics.get("completed_tasks", 0)

        task_completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0.0

        return {
            "agent_success_rate": agent_success_rate,
            "task_completion_rate": task_completion_rate,
            "total_agent_executions": total_agent_executions,
            "total_tasks": total_tasks,
            "active_agents": len(agent_metrics),
            "errors": self.system_metrics.get("errors", 0),
        }

    def _persist_metrics(self) -> None:
        """Persist metrics to file."""
        if not self.enabled or not self.metrics_file:
            return

        try:
            # Ensure parent directory exists
            self.metrics_file.parent.mkdir(parents=True, exist_ok=True)

            # Write metrics to file
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(self.get_all_metrics(), f, indent=2, default=str)

        except Exception as e:
            # Don't fail if persistence fails
            print(f"Warning: Failed to persist metrics: {e}")

    def _load_metrics(self) -> None:
        """Load metrics from file."""
        try:
            with open(self.metrics_file, encoding="utf-8") as f:
                data = json.load(f)

            # Load agent metrics
            if "agent_metrics" in data:
                for name, metrics in data["agent_metrics"].items():
                    self.agent_metrics[name] = metrics

            # Load task metrics
            if "task_metrics" in data:
                self.task_metrics.update(data["task_metrics"])

            # Load system metrics
            if "system_metrics" in data:
                self.system_metrics.update(data["system_metrics"])

        except Exception as e:
            # Don't fail if loading fails
            print(f"Warning: Failed to load metrics: {e}")
