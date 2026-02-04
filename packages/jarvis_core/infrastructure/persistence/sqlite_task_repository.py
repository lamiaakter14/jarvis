"""SQLite-based task repository implementation."""

import sqlite3
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from src.domain.repositories.i_task_repository import ITaskRepository
from src.domain.entities.task import Task
from src.domain.value_objects.priority import Priority
from src.domain.value_objects.cognitive_load import CognitiveLoad
from src.domain.value_objects.roi import ROI
from src.domain.value_objects.agent_type import AgentType as AgentTypeVO
from src.shared.constants import TaskStatus
from src.shared.exceptions import RepositoryError, EntityNotFoundError


class SqliteTaskRepository(ITaskRepository):
    """SQLite implementation of task repository.
    
    Uses SQLite database for task persistence with ACID guarantees
    and efficient querying capabilities.
    """
    
    def __init__(self, db_path: str = "memory/tasks.db"):
        """Initialize SQLite task repository.
        
        Args:
            db_path: Path to SQLite database file
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
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def _init_database(self) -> None:
        """Initialize database schema if not exists."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        task_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        priority TEXT NOT NULL,
                        priority_weight REAL NOT NULL,
                        cognitive_load_level TEXT NOT NULL,
                        cognitive_load_hours REAL NOT NULL,
                        roi_value REAL NOT NULL,
                        status TEXT NOT NULL,
                        agent_type TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        completed_at TEXT,
                        result TEXT
                    )
                """)
                
                # Create indexes for common queries
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_status 
                    ON tasks(status)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_agent_type 
                    ON tasks(agent_type)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_priority 
                    ON tasks(priority_weight DESC)
                """)
                
                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to initialize database: {e}")
    
    def _task_to_row(self, task: Task) -> tuple:
        """Convert Task entity to database row values.
        
        Args:
            task: Task entity
            
        Returns:
            Tuple of values for insertion
        """
        # Handle cognitive load level - can be enum or string
        cognitive_level = task.cognitive_load.level
        if hasattr(cognitive_level, 'value'):
            cognitive_level_str = cognitive_level.value
        else:
            cognitive_level_str = str(cognitive_level)
        
        return (
            task.task_id,
            task.title,
            task.description,
            task.priority.level.value,
            task.priority.weight,
            cognitive_level_str,
            task.cognitive_load.estimated_hours,
            task.roi.value,
            task.status.value,
            str(task.agent_type),
            task.created_at.isoformat(),
            task.updated_at.isoformat(),
            task.completed_at.isoformat() if task.completed_at else None,
            json.dumps(task.result) if task.result else None,
        )
    
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert database row to Task entity.
        
        Args:
            row: Database row
            
        Returns:
            Task entity
        """
        from src.shared.constants import CognitiveLoadLevel
        
        # Parse cognitive load level
        cognitive_level_str = row["cognitive_load_level"]
        cognitive_level = CognitiveLoadLevel(cognitive_level_str)
        
        return Task(
            task_id=row["task_id"],
            title=row["title"],
            description=row["description"],
            priority=Priority.from_string(row["priority"]),
            cognitive_load=CognitiveLoad(
                level=cognitive_level,
                estimated_hours=row["cognitive_load_hours"],
            ),
            roi=ROI(row["roi_value"]),
            status=TaskStatus(row["status"]),
            agent_type=AgentTypeVO.from_string(row["agent_type"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            result=json.loads(row["result"]) if row["result"] else None,
        )
    
    async def get(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Task instance if found, None otherwise
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM tasks WHERE task_id = ?",
                    (task_id,)
                )
                row = cursor.fetchone()
                
                if row is None:
                    return None
                
                return self._row_to_task(row)
        except Exception as e:
            raise RepositoryError(f"Failed to get task '{task_id}': {e}")
    
    async def save(self, task: Task) -> None:
        """Persist a task to storage.
        
        Args:
            task: Task instance to save
            
        Raises:
            RepositoryError: If save operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if task exists
                cursor.execute(
                    "SELECT task_id FROM tasks WHERE task_id = ?",
                    (task.task_id,)
                )
                exists = cursor.fetchone() is not None
                
                if exists:
                    # Update existing task
                    cursor.execute("""
                        UPDATE tasks SET
                            title = ?,
                            description = ?,
                            priority = ?,
                            priority_weight = ?,
                            cognitive_load_level = ?,
                            cognitive_load_hours = ?,
                            roi_value = ?,
                            status = ?,
                            agent_type = ?,
                            updated_at = ?,
                            completed_at = ?,
                            result = ?
                        WHERE task_id = ?
                    """, (
                        task.title,
                        task.description,
                        task.priority.level.value,
                        task.priority.weight,
                        task.cognitive_load.level.value,
                        task.cognitive_load.estimated_hours,
                        task.roi.value,
                        task.status.value,
                        str(task.agent_type),
                        task.updated_at.isoformat(),
                        task.completed_at.isoformat() if task.completed_at else None,
                        json.dumps(task.result) if task.result else None,
                        task.task_id,
                    ))
                else:
                    # Insert new task
                    cursor.execute("""
                        INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, self._task_to_row(task))
                
                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to save task '{task.task_id}': {e}")
    
    async def list(self, filters: Optional[Dict] = None) -> List[Task]:
        """List tasks with optional filtering.
        
        Args:
            filters: Optional dictionary of filter criteria
            
        Returns:
            List of Task instances matching the filters
            
        Raises:
            RepositoryError: If list operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM tasks"
                params = []
                
                if filters:
                    where_clauses = []
                    for key, value in filters.items():
                        if key in ["status", "agent_type", "priority"]:
                            where_clauses.append(f"{key} = ?")
                            params.append(value if isinstance(value, str) else value.value)
                    
                    if where_clauses:
                        query += " WHERE " + " AND ".join(where_clauses)
                
                query += " ORDER BY priority_weight DESC, created_at DESC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                return [self._row_to_task(row) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Failed to list tasks: {e}")
    
    async def delete(self, task_id: str) -> None:
        """Delete a task by its ID.
        
        Args:
            task_id: Unique identifier for the task to delete
            
        Raises:
            RepositoryError: If delete operation fails
            EntityNotFoundError: If task with ID does not exist
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
                
                if cursor.rowcount == 0:
                    raise EntityNotFoundError(f"Task '{task_id}' not found")
                
                conn.commit()
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise RepositoryError(f"Failed to delete task '{task_id}': {e}")
    
    async def get_by_status(self, status: TaskStatus) -> List[Task]:
        """Retrieve all tasks with a specific status.
        
        Args:
            status: Task status to filter by
            
        Returns:
            List of Task instances with the specified status
            
        Raises:
            RepositoryError: If retrieval operation fails
        """
        return await self.list(filters={"status": status})
    
    async def clear_all(self) -> None:
        """Clear all tasks from database (useful for testing).
        
        Raises:
            RepositoryError: If operation fails
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tasks")
                conn.commit()
        except Exception as e:
            raise RepositoryError(f"Failed to clear tasks: {e}")
