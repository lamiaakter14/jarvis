"""Shared exceptions for the JARVIS application."""


class JarvisException(Exception):
    """Base exception for all JARVIS errors."""
    pass


class DomainException(JarvisException):
    """Base exception for domain layer errors."""
    pass


class ApplicationException(JarvisException):
    """Base exception for application layer errors."""
    pass


class InfrastructureException(JarvisException):
    """Base exception for infrastructure layer errors."""
    pass


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""
    pass


class InvalidValueObjectError(DomainException):
    """Raised when a value object is invalid."""
    pass


class RepositoryError(InfrastructureException):
    """Raised when repository operations fail."""
    pass


class AIServiceError(InfrastructureException):
    """Raised when AI service operations fail."""
    pass


class ValidationError(ApplicationException):
    """Raised when validation fails."""
    pass


class UseCaseError(ApplicationException):
    """Raised when a use case operation fails."""
    pass


class ConfigurationError(InfrastructureException):
    """Raised when configuration is invalid."""
    pass
