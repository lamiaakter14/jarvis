# Memory System

This package contains the memory subsystems for the JARVIS cognitive assistant, implementing episodic, semantic, and strategic memory capabilities.

## Modules

### Episodic Memory (`episodic.py`)

Handles chronological logs of daily activities and events.

**Key Functions:**
- `store_daily_log(entries: List[str])`: Store daily log entries in the database
- `retrieve_last_n_days(n: int)`: Retrieve logs from the last n days

**Features:**
- SQLite-based persistence (prepared for Postgres migration)
- Automatic timestamping and date indexing
- Input validation and error handling
- Chronological ordering

**Example:**
```python
from jarvis_core.memory import store_daily_log, retrieve_last_n_days

# Store daily logs
store_daily_log([
    "Completed task: Update memory system",
    "Started work on semantic embeddings"
])

# Retrieve last 7 days of logs
logs = retrieve_last_n_days(7)
for log in logs:
    print(f"{log['log_date']}: {log['entry']}")
```

### Semantic Memory (`semantic.py`)

Provides an interface for embedding storage and retrieval, enabling semantic search capabilities.

**Key Components:**
- `SemanticMemoryInterface`: Abstract interface for vector storage
- `InMemorySemanticStore`: In-memory implementation for development
- `get_semantic_store()`: Factory function to get store instance

**Features:**
- Vector embedding storage with metadata
- Cosine similarity search
- Pagination support
- Prepared for pgvector integration

**Example:**
```python
from jarvis_core.memory import get_semantic_store

store = get_semantic_store()

# Store an embedding
store.store_embedding(
    key="concept_001",
    embedding=[0.1, 0.2, 0.3, 0.4],
    metadata={"source": "documentation", "topic": "memory"}
)

# Search for similar embeddings
results = store.search_similar(
    query_embedding=[0.1, 0.2, 0.3, 0.4],
    top_k=5,
    threshold=0.8
)
```

### Strategic Memory (`strategic.py`)

Manages goal snapshots and trajectory tracking for strategic planning.

**Key Functions:**
- `store_goal_snapshot(goal_snapshot: Dict[str, Any])`: Save goal state snapshots
- `trajectory_delta(previous_snapshot, current_snapshot)`: Calculate delta between snapshots

**Features:**
- Automatic versioning of goal snapshots
- Snapshot history tracking
- Delta calculation for trajectory analysis
- Metadata field filtering (fields starting with `_`)

**Example:**
```python
from jarvis_core.memory import store_goal_snapshot, trajectory_delta

# Store a goal snapshot
snapshot = {
    "goal_id": "goal_001",
    "title": "Implement memory system",
    "status": "in_progress",
    "progress": 0.6,
    "tasks_completed": 3,
    "tasks_total": 5
}
snapshot_id = store_goal_snapshot(snapshot)

# Calculate trajectory delta
prev_snapshot = {"goal_id": "goal_001", "progress": 0.3, "status": "pending"}
curr_snapshot = {"goal_id": "goal_001", "progress": 0.6, "status": "in_progress"}

delta = trajectory_delta(prev_snapshot, curr_snapshot)
print(f"Modified fields: {delta['modified']}")
print(f"Has changes: {delta['has_changes']}")
```

## Database Storage

### Current Implementation
- Uses SQLite for local storage
- Automatic schema initialization
- Indexed queries for performance

### Future Migration to Postgres
The modules are designed with Postgres migration in mind:
- Connection management abstraction
- Schema-compatible SQL
- Prepared for pgvector integration (semantic memory)

To migrate to Postgres:
1. Update connection management to use `psycopg2`
2. Adjust SQL syntax if needed (minimal changes required)
3. Add pgvector extension for semantic memory
4. Update connection strings in configuration

## Testing

Comprehensive unit tests are provided in `tests/unit/memory/`:
- `test_episodic.py`: 13 tests for episodic memory
- `test_semantic.py`: 16 tests for semantic memory
- `test_strategic.py`: 18 tests for strategic memory

Run tests with:
```bash
pytest tests/unit/memory/ -v
```

## Architecture

The memory system follows clean architecture principles:
- **Separation of Concerns**: Each memory type has its own module
- **Interface-Based Design**: Semantic memory uses abstract interface
- **Dependency Injection**: Singleton pattern with factory functions
- **Input Validation**: Comprehensive validation at module boundaries
- **Error Handling**: Consistent exception handling using shared exceptions

## Integration

Import memory functions from the package:
```python
from jarvis_core.memory import (
    store_daily_log,
    retrieve_last_n_days,
    get_semantic_store,
    store_goal_snapshot,
    trajectory_delta
)
```

All functions include comprehensive docstrings and type hints for ease of use.
