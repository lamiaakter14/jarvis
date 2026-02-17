"""Logger implementation for structured logging."""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class Logger:
    """Structured logger for the JARVIS application.

    Provides centralized logging with support for file and console output,
    structured log formats, and different log levels.
    """

    def __init__(
        self,
        level: str = "INFO",
        log_file: Optional[str] = None,
        log_format: Optional[str] = None,
        name: str = "jarvis",
    ):
        """Initialize logger.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file
            log_format: Optional custom log format
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self._get_level(level))

        # Remove existing handlers
        self.logger.handlers.clear()

        # Set format
        if not log_format:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (if log_file provided)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def _get_level(self, level: str) -> int:
        """Convert string level to logging level constant.

        Args:
            level: Level string

        Returns:
            Logging level constant
        """
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(level.upper(), logging.INFO)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log(logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log(logging.INFO, message, kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log(logging.WARNING, message, kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log(logging.ERROR, message, kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message.

        Args:
            message: Log message
            **kwargs: Additional structured data
        """
        self._log(logging.CRITICAL, message, kwargs)

    def exception(self, message: str, exc_info: bool = True, **kwargs: Any) -> None:
        """Log exception with traceback.

        Args:
            message: Log message
            exc_info: Include exception info
            **kwargs: Additional structured data
        """
        self._log(logging.ERROR, message, kwargs, exc_info=exc_info)

    def _log(
        self, level: int, message: str, extra_data: Dict[str, Any], exc_info: bool = False
    ) -> None:
        """Internal log method with structured data support.

        Args:
            level: Log level
            message: Log message
            extra_data: Additional structured data
            exc_info: Include exception info
        """
        # Format extra data if provided
        if extra_data:
            extra_str = " | ".join([f"{k}={v}" for k, v in extra_data.items()])
            full_message = f"{message} | {extra_str}"
        else:
            full_message = message

        self.logger.log(level, full_message, exc_info=exc_info)

    def log_agent_execution(
        self,
        agent_name: str,
        action: str,
        status: str,
        duration: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        """Log agent execution with structured format.

        Args:
            agent_name: Name of the agent
            action: Action performed
            status: Execution status
            duration: Execution duration in seconds
            **kwargs: Additional data
        """
        data = {
            "agent": agent_name,
            "action": action,
            "status": status,
        }

        if duration is not None:
            data["duration"] = f"{duration:.2f}s"

        data.update(kwargs)

        if status == "success":
            self.info("Agent execution completed", **data)
        elif status == "failed":
            self.error("Agent execution failed", **data)
        else:
            self.info("Agent execution status", **data)

    def log_task_execution(
        self,
        task_id: str,
        task_title: str,
        status: str,
        duration: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        """Log task execution with structured format.

        Args:
            task_id: Task ID
            task_title: Task title
            status: Execution status
            duration: Execution duration in seconds
            **kwargs: Additional data
        """
        data = {
            "task_id": task_id,
            "task_title": task_title,
            "status": status,
        }

        if duration is not None:
            data["duration"] = f"{duration:.2f}s"

        data.update(kwargs)

        if status == "completed":
            self.info("Task completed", **data)
        elif status == "failed":
            self.error("Task failed", **data)
        else:
            self.info("Task status update", **data)

    def log_api_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        duration: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        """Log API request with structured format.

        Args:
            method: HTTP method
            endpoint: API endpoint
            status_code: Response status code
            duration: Request duration in seconds
            **kwargs: Additional data
        """
        data = {
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code,
        }

        if duration is not None:
            data["duration"] = f"{duration:.3f}s"

        data.update(kwargs)

        if 200 <= status_code < 300:
            self.info("API request", **data)
        elif status_code >= 400:
            self.error("API request failed", **data)
        else:
            self.info("API request", **data)

    def set_level(self, level: str) -> None:
        """Change logging level.

        Args:
            level: New logging level
        """
        self.logger.setLevel(self._get_level(level))

    def get_logger(self) -> logging.Logger:
        """Get underlying Python logger.

        Returns:
            Python logger instance
        """
        return self.logger
