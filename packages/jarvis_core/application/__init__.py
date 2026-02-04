"""Application layer for JARVIS Clean Architecture.

This layer contains:
- DTOs (Data Transfer Objects): Serializable representations of domain entities
- Interfaces: Contracts for external services (AI, notifications, etc.)
- Use Cases: Application-specific business logic and orchestration

The application layer orchestrates domain objects and implements use cases
without depending on infrastructure details.
"""

from jarvis_core.application import dto, interfaces, use_cases

__all__ = [
    "dto",
    "interfaces",
    "use_cases",
]
