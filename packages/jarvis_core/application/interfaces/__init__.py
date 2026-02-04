"""Application layer interfaces."""

from src.application.interfaces.i_ai_service import IAIService
from src.application.interfaces.i_notification_service import INotificationService

__all__ = [
    "IAIService",
    "INotificationService",
]
