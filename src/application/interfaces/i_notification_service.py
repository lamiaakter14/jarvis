"""Notification Service Interface for application layer."""

from abc import ABC, abstractmethod
from typing import Dict

from src.domain.entities.task import Task


class INotificationService(ABC):
    """Abstract interface for notification services.
    
    Defines the contract for sending notifications about important
    events in the JARVIS system, such as task completion, gap identification,
    and other significant activities.
    """
    
    @abstractmethod
    async def send_notification(self, message: str, type: str) -> None:
        """Send a general notification.
        
        Args:
            message: Notification message content
            type: Notification type (e.g., 'info', 'warning', 'error', 'success')
            
        Raises:
            NotificationError: If notification sending fails
        """
        pass
    
    @abstractmethod
    async def notify_task_completed(self, task: Task) -> None:
        """Send notification when a task is completed.
        
        Sends a structured notification with task completion details,
        including task title, status, duration, and results.
        
        Args:
            task: Completed task entity
            
        Raises:
            NotificationError: If notification sending fails
        """
        pass
    
    @abstractmethod
    async def notify_gap_identified(self, gap: Dict) -> None:
        """Send notification when a gap is identified.
        
        Sends a notification about newly identified knowledge or skill gaps
        that require attention, including gap type, severity, and evidence.
        
        Args:
            gap: Dictionary containing gap information:
                - type: Gap type (knowledge, skill, process, etc.)
                - description: Gap description
                - severity: Severity level (low, medium, high, critical)
                - evidence: Supporting evidence for the gap
                
        Raises:
            NotificationError: If notification sending fails
        """
        pass
