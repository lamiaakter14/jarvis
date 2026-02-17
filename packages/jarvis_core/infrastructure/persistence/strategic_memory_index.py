"""Strategic memory index for efficient retrieval and querying."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from jarvis_core.shared.exceptions import RepositoryError


class StrategicMemoryIndex:
    """Index service for strategic memory enabling fast lookups.

    Maintains in-memory and persistent indexes for strategic memory records
    including goals and ADRs. Supports indexing by priority, status, tags,
    and temporal relationships.
    """

    def __init__(self, base_path: str = "memory"):
        """Initialize the strategic memory index.

        Args:
            base_path: Base directory for memory storage
        """
        self.base_path = Path(base_path)
        self.index_file = self.base_path / "strategic" / ".index.json"

        # In-memory indexes
        self.by_priority: dict[str, set[str]] = {
            "critical": set(),
            "high": set(),
            "medium": set(),
            "low": set(),
        }
        self.by_status: dict[str, set[str]] = {
            "active": set(),
            "paused": set(),
            "completed": set(),
            "cancelled": set(),
            "proposed": set(),
            "accepted": set(),
            "deprecated": set(),
            "superseded": set(),
        }
        self.by_tag: dict[str, set[str]] = {}
        self.by_type: dict[str, set[str]] = {"goal": set(), "adr": set()}
        self.metadata: dict[str, dict] = {}  # key -> metadata

        # Load existing index
        self._load_index()

    def _ensure_directory(self) -> None:
        """Ensure the strategic memory directory exists."""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> None:
        """Load index from persistent storage."""
        if not self.index_file.exists():
            return

        try:
            with open(self.index_file) as f:
                data = json.load(f)

            # Restore indexes
            self.by_priority = {k: set(v) for k, v in data.get("by_priority", {}).items()}
            self.by_status = {k: set(v) for k, v in data.get("by_status", {}).items()}
            self.by_tag = {k: set(v) for k, v in data.get("by_tag", {}).items()}
            self.by_type = {k: set(v) for k, v in data.get("by_type", {}).items()}
            self.metadata = data.get("metadata", {})

        except Exception as e:
            raise RepositoryError(f"Failed to load strategic memory index: {e}")

    def _save_index(self) -> None:
        """Save index to persistent storage."""
        try:
            self._ensure_directory()

            data = {
                "by_priority": {k: list(v) for k, v in self.by_priority.items()},
                "by_status": {k: list(v) for k, v in self.by_status.items()},
                "by_tag": {k: list(v) for k, v in self.by_tag.items()},
                "by_type": {k: list(v) for k, v in self.by_type.items()},
                "metadata": self.metadata,
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.index_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            raise RepositoryError(f"Failed to save strategic memory index: {e}")

    def add_entry(
        self,
        key: str,
        entry_type: str,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> None:
        """Add or update an entry in the index.

        Args:
            key: Memory key
            entry_type: Type of entry ('goal' or 'adr')
            priority: Priority level
            status: Status value
            tags: List of tags
        """
        # Add to type index
        if entry_type in self.by_type:
            self.by_type[entry_type].add(key)

        # Add to priority index
        if priority and priority in self.by_priority:
            # Remove from other priorities
            for p in self.by_priority:
                self.by_priority[p].discard(key)
            self.by_priority[priority].add(key)

        # Add to status index
        if status and status in self.by_status:
            # Remove from other statuses
            for s in self.by_status:
                self.by_status[s].discard(key)
            self.by_status[status].add(key)

        # Add to tag indexes
        if tags:
            for tag in tags:
                if tag not in self.by_tag:
                    self.by_tag[tag] = set()
                self.by_tag[tag].add(key)

        # Store metadata
        self.metadata[key] = {
            "type": entry_type,
            "priority": priority,
            "status": status,
            "tags": tags or [],
            "indexed_at": datetime.now().isoformat(),
        }

        # Persist index
        self._save_index()

    def remove_entry(self, key: str) -> None:
        """Remove an entry from the index.

        Args:
            key: Memory key to remove
        """
        # Remove from all indexes
        for priority_set in self.by_priority.values():
            priority_set.discard(key)

        for status_set in self.by_status.values():
            status_set.discard(key)

        for tag_set in self.by_tag.values():
            tag_set.discard(key)

        for type_set in self.by_type.values():
            type_set.discard(key)

        # Remove metadata
        self.metadata.pop(key, None)

        # Persist index
        self._save_index()

    def find_by_priority(self, priority: str) -> set[str]:
        """Find all entries with given priority.

        Args:
            priority: Priority level to search for

        Returns:
            Set of matching memory keys
        """
        return self.by_priority.get(priority, set()).copy()

    def find_by_status(self, status: str) -> set[str]:
        """Find all entries with given status.

        Args:
            status: Status to search for

        Returns:
            Set of matching memory keys
        """
        return self.by_status.get(status, set()).copy()

    def find_by_tag(self, tag: str) -> set[str]:
        """Find all entries with given tag.

        Args:
            tag: Tag to search for

        Returns:
            Set of matching memory keys
        """
        return self.by_tag.get(tag, set()).copy()

    def find_by_tags(self, tags: list[str], match_all: bool = False) -> set[str]:
        """Find entries matching given tags.

        Args:
            tags: List of tags to search for
            match_all: If True, require all tags; if False, require any tag

        Returns:
            Set of matching memory keys
        """
        if not tags:
            return set()

        result_sets = [self.by_tag.get(tag, set()) for tag in tags]

        if match_all:
            # Intersection: entries must have all tags
            if result_sets:
                result = result_sets[0].copy()
                for s in result_sets[1:]:
                    result &= s
                return result
            return set()
        else:
            # Union: entries can have any of the tags
            result = set()
            for s in result_sets:
                result |= s
            return result

    def find_by_type(self, entry_type: str) -> set[str]:
        """Find all entries of given type.

        Args:
            entry_type: Type to search for ('goal' or 'adr')

        Returns:
            Set of matching memory keys
        """
        return self.by_type.get(entry_type, set()).copy()

    def get_metadata(self, key: str) -> Optional[dict]:
        """Get metadata for a specific entry.

        Args:
            key: Memory key

        Returns:
            Metadata dictionary or None if not found
        """
        return self.metadata.get(key)

    def get_all_tags(self) -> list[str]:
        """Get all tags in the index.

        Returns:
            List of all unique tags
        """
        return list(self.by_tag.keys())

    def get_statistics(self) -> dict:
        """Get statistics about the indexed strategic memory.

        Returns:
            Dictionary with statistics
        """
        return {
            "total_entries": len(self.metadata),
            "by_type": {entry_type: len(keys) for entry_type, keys in self.by_type.items()},
            "by_priority": {priority: len(keys) for priority, keys in self.by_priority.items()},
            "by_status": {status: len(keys) for status, keys in self.by_status.items()},
            "total_tags": len(self.by_tag),
            "most_used_tags": sorted(
                [(tag, len(keys)) for tag, keys in self.by_tag.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:10],
        }
