"""Episodic memory module for storing and retrieving daily logs.

This module handles episodic memory, which stores chronological logs of daily
activities and events. It uses database storage (prepared for Postgres) to
maintain a persistent record of system activities.
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from jarvis_core.shared.exceptions import RepositoryError


class EpisodicMemoryStore:
    """Store for episodic memories using database persistence.

    This implementation uses SQLite for local storage but is structured
    to facilitate migration to Postgres in the future.
    """

    def __init__(self, db_path: str = "memory/episodic.db"):
        """Initialize episodic memory store.

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
                    CREATE TABLE IF NOT EXISTS daily_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        entry TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        log_date TEXT NOT NULL
                    )
                """)

                # Create index for date-based queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_log_date
                    ON daily_logs(log_date)
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_created_at
                    ON daily_logs(created_at)
                """)

                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to initialize episodic memory database: {e}")

    def store_entries(self, entries: List[str]) -> None:
        """Store multiple log entries for the current day.

        Args:
            entries: List of log entry strings to store

        Raises:
            RepositoryError: If storage operation fails
            ValueError: If entries is empty or contains invalid data
        """
        if not entries:
            raise ValueError("Entries list cannot be empty")

        if not all(isinstance(entry, str) for entry in entries):
            raise ValueError("All entries must be strings")

        # Filter out empty entries
        valid_entries = [e.strip() for e in entries if e.strip()]
        if not valid_entries:
            raise ValueError("No valid entries to store after filtering empty strings")

        try:
            current_time = datetime.now()
            log_date = current_time.date().isoformat()

            with self._get_connection() as conn:
                cursor = conn.cursor()
                for entry in valid_entries:
                    cursor.execute(
                        "INSERT INTO daily_logs (entry, created_at, log_date) VALUES (?, ?, ?)",
                        (entry, current_time.isoformat(), log_date),
                    )
                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to store daily log entries: {e}")

    def retrieve_last_n_days(self, n: int) -> List[dict]:
        """Retrieve logs from the last n days.

        Args:
            n: Number of days to retrieve logs for (must be positive)

        Returns:
            List of dictionaries containing log entries with metadata

        Raises:
            RepositoryError: If retrieval operation fails
            ValueError: If n is not a positive integer
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Number of days must be a positive integer")

        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=n - 1)

            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, entry, created_at, log_date
                    FROM daily_logs
                    WHERE log_date >= ? AND log_date <= ?
                    ORDER BY created_at DESC
                """,
                    (start_date.isoformat(), end_date.isoformat()),
                )

                rows = cursor.fetchall()

                return [
                    {
                        "id": row["id"],
                        "entry": row["entry"],
                        "created_at": row["created_at"],
                        "log_date": row["log_date"],
                    }
                    for row in rows
                ]
        except Exception as e:
            raise RepositoryError(f"Failed to retrieve logs for last {n} days: {e}")


# Module-level store instance (singleton pattern)
_store: Optional[EpisodicMemoryStore] = None


def _get_store() -> EpisodicMemoryStore:
    """Get or create the episodic memory store instance.

    Returns:
        EpisodicMemoryStore instance
    """
    global _store
    if _store is None:
        _store = EpisodicMemoryStore()
    return _store


def store_daily_log(entries: List[str]) -> None:
    """Store daily logs in the database.

    This function stores a list of log entries for the current day in the
    episodic memory database. Each entry is timestamped and associated with
    the current date for easy retrieval.

    Args:
        entries: List of log entry strings to store

    Raises:
        RepositoryError: If storage operation fails
        ValueError: If entries is empty or contains invalid data

    Example:
        >>> store_daily_log([
        ...     "Completed task: Update memory system",
        ...     "Started work on semantic embeddings"
        ... ])
    """
    store = _get_store()
    store.store_entries(entries)


def retrieve_last_n_days(n: int) -> List[dict]:
    """Retrieve logs from the last n days.

    This function retrieves all log entries from the last n days, ordered
    by creation time (most recent first). Each entry includes the log text,
    timestamps, and associated date.

    Args:
        n: Number of days to retrieve logs for (must be positive)

    Returns:
        List of dictionaries containing log entries with metadata:
        - id: Unique identifier for the log entry
        - entry: The log entry text
        - created_at: ISO format timestamp when entry was created
        - log_date: ISO format date the entry belongs to

    Raises:
        RepositoryError: If retrieval operation fails
        ValueError: If n is not a positive integer

    Example:
        >>> logs = retrieve_last_n_days(7)
        >>> for log in logs:
        ...     print(f"{log['log_date']}: {log['entry']}")
    """
    store = _get_store()
    return store.retrieve_last_n_days(n)
