"""Application layer interfaces."""

from jarvis_core.application.interfaces.i_ai_service import IAIService
from jarvis_core.application.interfaces.i_notification_service import INotificationService

__all__ = [
    "IAIService",
    "INotificationService",
]
