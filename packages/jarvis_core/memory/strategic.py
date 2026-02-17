"""Strategic memory module for goal management and trajectory tracking.

This module handles strategic memory, which stores goal snapshots and tracks
the trajectory of goal progress over time. It enables the system to understand
how goals evolve and calculate deltas between different states.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from jarvis_core.shared.exceptions import RepositoryError


class StrategicMemoryStore:
    """Store for strategic memories using database persistence.

    This implementation uses SQLite for local storage but is structured
    to facilitate migration to Postgres in the future.
    """

    def __init__(self, db_path: str = "memory/strategic.db"):
        """Initialize strategic memory store.

        Args:
            db_path: Path to the database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection.

        Returns:
            SQLite connection
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_database(self) -> None:
        """Initialize database schema if not exists."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS goal_snapshots (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        goal_id TEXT NOT NULL,
                        snapshot_data TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        version INTEGER NOT NULL DEFAULT 1
                    )
                """)

                # Create indexes for efficient queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_goal_id
                    ON goal_snapshots(goal_id)
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_created_at
                    ON goal_snapshots(created_at)
                """)

                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to initialize strategic memory database: {e}")

    def store_snapshot(self, goal_snapshot: Dict[str, Any]) -> int:
        """Store a goal snapshot in the database.

        Args:
            goal_snapshot: Dictionary containing goal state information

        Returns:
            The ID of the stored snapshot

        Raises:
            RepositoryError: If storage operation fails
            ValueError: If goal_snapshot is invalid
        """
        if not goal_snapshot:
            raise ValueError("Goal snapshot cannot be empty")

        if not isinstance(goal_snapshot, dict):
            raise ValueError("Goal snapshot must be a dictionary")

        if "goal_id" not in goal_snapshot:
            raise ValueError("Goal snapshot must contain 'goal_id' field")

        try:
            goal_id = goal_snapshot["goal_id"]
            current_time = datetime.now().isoformat()

            # Get the next version number for this goal
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Find the latest version for this goal
                cursor.execute(
                    "SELECT MAX(version) as max_version FROM goal_snapshots WHERE goal_id = ?",
                    (goal_id,),
                )
                row = cursor.fetchone()
                next_version = (row["max_version"] or 0) + 1

                # Store the snapshot
                cursor.execute(
                    """INSERT INTO goal_snapshots
                       (goal_id, snapshot_data, created_at, version)
                       VALUES (?, ?, ?, ?)""",
                    (goal_id, json.dumps(goal_snapshot), current_time, next_version),
                )

                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            raise RepositoryError(f"Failed to store goal snapshot: {e}")

    def get_latest_snapshot(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the latest snapshot for a goal.

        Args:
            goal_id: Unique identifier for the goal

        Returns:
            Dictionary containing the latest snapshot, or None if not found

        Raises:
            RepositoryError: If retrieval operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT snapshot_data, created_at, version
                    FROM goal_snapshots
                    WHERE goal_id = ?
                    ORDER BY version DESC
                    LIMIT 1
                """,
                    (goal_id,),
                )

                row = cursor.fetchone()
                if row:
                    return {
                        **json.loads(row["snapshot_data"]),
                        "_created_at": row["created_at"],
                        "_version": row["version"],
                    }
                return None
        except Exception as e:
            raise RepositoryError(f"Failed to retrieve latest snapshot for goal {goal_id}: {e}")

    def get_snapshot_history(self, goal_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve snapshot history for a goal.

        Args:
            goal_id: Unique identifier for the goal
            limit: Maximum number of snapshots to retrieve

        Returns:
            List of snapshot dictionaries, ordered by version (newest first)

        Raises:
            RepositoryError: If retrieval operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT snapshot_data, created_at, version
                    FROM goal_snapshots
                    WHERE goal_id = ?
                    ORDER BY version DESC
                    LIMIT ?
                """,
                    (goal_id, limit),
                )

                rows = cursor.fetchall()
                return [
                    {
                        **json.loads(row["snapshot_data"]),
                        "_created_at": row["created_at"],
                        "_version": row["version"],
                    }
                    for row in rows
                ]
        except Exception as e:
            raise RepositoryError(f"Failed to retrieve snapshot history for goal {goal_id}: {e}")


# Module-level store instance (singleton pattern)
_store: Optional[StrategicMemoryStore] = None


def _get_store() -> StrategicMemoryStore:
    """Get or create the strategic memory store instance.

    Returns:
        StrategicMemoryStore instance
    """
    global _store
    if _store is None:
        _store = StrategicMemoryStore()
    return _store


def store_goal_snapshot(goal_snapshot: Dict[str, Any]) -> int:
    """Save a goal state snapshot to the database.

    This function stores a snapshot of the current goal state, enabling
    tracking of goal evolution over time. Each snapshot is versioned
    automatically.

    Args:
        goal_snapshot: Dictionary containing goal state information.
                      Must include 'goal_id' field.

    Returns:
        The ID of the stored snapshot

    Raises:
        RepositoryError: If storage operation fails
        ValueError: If goal_snapshot is invalid

    Example:
        >>> snapshot = {
        ...     "goal_id": "goal_001",
        ...     "title": "Implement memory system",
        ...     "status": "in_progress",
        ...     "progress": 0.6,
        ...     "tasks_completed": 3,
        ...     "tasks_total": 5
        ... }
        >>> snapshot_id = store_goal_snapshot(snapshot)
    """
    store = _get_store()
    return store.store_snapshot(goal_snapshot)


def trajectory_delta(
    previous_snapshot: Dict[str, Any], current_snapshot: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate the difference between two goal snapshots.

    This function computes the delta between a previous and current goal
    snapshot, identifying what has changed, been added, or removed. This
    enables tracking of goal trajectory and understanding progress patterns.

    Args:
        previous_snapshot: Earlier goal state snapshot
        current_snapshot: More recent goal state snapshot

    Returns:
        Dictionary containing:
        - added: Fields present in current but not in previous
        - removed: Fields present in previous but not in current
        - modified: Fields present in both with different values
        - unchanged: Fields present in both with same values

    Raises:
        ValueError: If snapshots are invalid

    Example:
        >>> prev = {"goal_id": "g1", "progress": 0.3, "status": "in_progress"}
        >>> curr = {"goal_id": "g1", "progress": 0.6, "status": "in_progress", "notes": "Updated"}
        >>> delta = trajectory_delta(prev, curr)
        >>> print(delta["modified"])
        {'progress': {'old': 0.3, 'new': 0.6}}
        >>> print(delta["added"])
        {'notes': 'Updated'}
    """
    if not isinstance(previous_snapshot, dict):
        raise ValueError("Previous snapshot must be a dictionary")

    if not isinstance(current_snapshot, dict):
        raise ValueError("Current snapshot must be a dictionary")

    # Extract keys from both snapshots (excluding metadata fields)
    prev_keys = {k for k in previous_snapshot if not k.startswith("_")}
    curr_keys = {k for k in current_snapshot if not k.startswith("_")}

    # Calculate differences
    added_keys = curr_keys - prev_keys
    removed_keys = prev_keys - curr_keys
    common_keys = prev_keys & curr_keys

    added = {k: current_snapshot[k] for k in added_keys}
    removed = {k: previous_snapshot[k] for k in removed_keys}

    modified = {}
    unchanged = {}

    for key in common_keys:
        prev_val = previous_snapshot[key]
        curr_val = current_snapshot[key]

        if prev_val != curr_val:
            modified[key] = {"old": prev_val, "new": curr_val}
        else:
            unchanged[key] = curr_val

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
        "has_changes": bool(added or removed or modified),
    }
