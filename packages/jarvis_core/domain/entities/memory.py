"""Memory entity for the domain layer."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from jarvis_core.shared.constants import MemoryType
from jarvis_core.shared.exceptions import DomainException
from jarvis_core.shared.utils import current_timestamp, generate_id


@dataclass
class Memory:
    """Memory entity representing stored information in the system.

    Memories maintain the system's knowledge base, execution history,
    and strategic context across sessions. Supports versioning for
    tracking changes and migration support.
    """

    memory_id: str = field(default_factory=lambda: generate_id("mem_"))
    type: MemoryType = MemoryType.WORKING
    key: str = ""
    content: dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=current_timestamp)
    updated_at: datetime = field(default_factory=current_timestamp)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate memory after initialization."""
        if not self.key:
            raise DomainException("Memory key cannot be empty")
        if not isinstance(self.content, dict):
            raise DomainException("Memory content must be a dictionary")

        # Initialize version in metadata if not present
        if "version" not in self.metadata:
            self.metadata["version"] = 1

    def update_content(
        self, new_content: dict[str, Any], merge: bool = False, increment_version: bool = True
    ) -> None:
        """Update the memory content.

        Args:
            new_content: New content to store
            merge: If True, merge with existing content; if False, replace
            increment_version: If True, increment version number

        Raises:
            DomainException: If new_content is not a dictionary
        """
        if not isinstance(new_content, dict):
            raise DomainException("New content must be a dictionary")

        if merge:
            self.content.update(new_content)
        else:
            self.content = new_content

        self.updated_at = current_timestamp()

        # Increment version if requested
        if increment_version:
            current_version = self.metadata.get("version", 1)
            self.metadata["version"] = current_version + 1

    def add_metadata(self, key: str, value: Any) -> None:
        """Add or update a metadata field.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.updated_at = current_timestamp()

    def get_content_value(self, path: str, default: Any = None) -> Any:
        """Get a value from nested content using dot notation.

        Args:
            path: Dot-separated path to the value (e.g., "user.name")
            default: Default value if path not found

        Returns:
            Value at the specified path or default
        """
        keys = path.split(".")
        value = self.content

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set_content_value(self, path: str, value: Any) -> None:
        """Set a value in nested content using dot notation.

        Args:
            path: Dot-separated path to set (e.g., "user.name")
            value: Value to set
        """
        keys = path.split(".")
        current = self.content

        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        self.updated_at = current_timestamp()

    def is_working_memory(self) -> bool:
        """Check if this is working memory."""
        return self.type == MemoryType.WORKING

    def is_knowledge_memory(self) -> bool:
        """Check if this is knowledge memory."""
        return self.type == MemoryType.KNOWLEDGE

    def is_strategic_memory(self) -> bool:
        """Check if this is strategic memory."""
        return self.type == MemoryType.STRATEGIC

    def is_execution_log(self) -> bool:
        """Check if this is an execution log."""
        return self.type == MemoryType.EXECUTION_LOG

    def get_age_in_days(self) -> float:
        """Calculate the age of this memory in days.

        Returns:
            Age in days
        """
        age = current_timestamp() - self.created_at
        return age.total_seconds() / 86400  # seconds per day

    def is_stale(self, max_age_days: float = 30.0) -> bool:
        """Check if memory is stale based on age.

        Args:
            max_age_days: Maximum age in days before considering stale

        Returns:
            True if memory is older than max_age_days
        """
        return self.get_age_in_days() > max_age_days

    def get_version(self) -> int:
        """Get the current version of the memory.

        Returns:
            Current version number
        """
        return self.metadata.get("version", 1)

    def set_version(self, version: int) -> None:
        """Set the version of the memory.

        Args:
            version: Version number to set

        Raises:
            DomainException: If version is invalid
        """
        if version < 1:
            raise DomainException("Version must be at least 1")

        self.metadata["version"] = version
        self.updated_at = current_timestamp()

    def add_tags(self, tags: list[str]) -> None:
        """Add tags to memory for indexing and search.

        Args:
            tags: List of tags to add
        """
        if "tags" not in self.metadata:
            self.metadata["tags"] = []

        # Add new tags that don't already exist
        existing_tags = set(self.metadata["tags"])
        for tag in tags:
            if tag and tag not in existing_tags:
                self.metadata["tags"].append(tag)
                existing_tags.add(tag)

        self.updated_at = current_timestamp()

    def get_tags(self) -> list[str]:
        """Get all tags associated with this memory.

        Returns:
            List of tags
        """
        return self.metadata.get("tags", [])

    def has_tag(self, tag: str) -> bool:
        """Check if memory has a specific tag.

        Args:
            tag: Tag to check for

        Returns:
            True if tag exists
        """
        return tag in self.get_tags()

    def __str__(self) -> str:
        """String representation of the memory."""
        return f"{self.type.value}: {self.key}"

    def __repr__(self) -> str:
        """Detailed representation of the memory."""
        return (
            f"Memory(id={self.memory_id}, type={self.type.value}, "
            f"key={self.key}, version={self.get_version()}, created={self.created_at.date()})"
        )
