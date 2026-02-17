"""Shared exceptions for the JARVIS application."""


class JarvisException(Exception):
    """Base exception for all JARVIS errors."""



class DomainException(JarvisException):
    """Base exception for domain layer errors."""



class ApplicationException(JarvisException):
    """Base exception for application layer errors."""



class InfrastructureException(JarvisException):
    """Base exception for infrastructure layer errors."""



class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""



class InvalidValueObjectError(DomainException):
    """Raised when a value object is invalid."""



class RepositoryError(InfrastructureException):
    """Raised when repository operations fail."""



class AIServiceError(InfrastructureException):
    """Raised when AI service operations fail."""



class ValidationError(ApplicationException):
    """Raised when validation fails."""



class UseCaseError(ApplicationException):
    """Raised when a use case operation fails."""



class ConfigurationError(InfrastructureException):
    """Raised when configuration is invalid."""

