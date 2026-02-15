# Memory Management System

## Overview

The JARVIS memory management system provides a comprehensive framework for storing, retrieving, and managing different types of memories including working memory, knowledge, strategic goals, and execution logs. The system supports schema validation, versioning, indexing, and advanced search capabilities.

## Features

### 1. Schema Validation with Pydantic

All memory operations are validated using Pydantic schemas to ensure data integrity:

- **MemoryDTO**: Data transfer object with comprehensive validation
- **Memory Content Schemas**: Type-specific validation for different memory types
  - `WorkingMemoryContent`: Temporary session data
  - `KnowledgeMemoryContent`: Long-term knowledge storage
  - `StrategicMemoryContent`: Strategic goals and plans
  - `ExecutionLogContent`: Task execution records
  - `ADRContent`: Architecture Decision Records

### 2. Memory Indexing and Search

Advanced search capabilities for efficient knowledge retrieval:

- **Keyword Search**: Search memory content by keywords
- **Key Pattern Matching**: Find memories by key patterns
- **Tag-based Search**: Filter memories using tags
- **Type Filtering**: Search within specific memory types
- **Pagination Support**: Handle large result sets efficiently

### 3. Memory Versioning

Track and manage memory versions over time:

- **Automatic Versioning**: Versions increment with content updates
- **Version History**: Retrieve specific versions of memories
- **Version Tracking**: List all available versions
- **Migration Support**: Framework for migrating memory data

### 4. Strategic Memory Management

Specialized support for long-term planning:

- **Strategic Goals**: Define and track long-term objectives
- **Progress Tracking**: Monitor goal completion
- **Dependencies**: Model goal dependencies
- **Milestones**: Break goals into achievable milestones
- **Architecture Decision Records (ADRs)**: Document architectural decisions

## Usage Examples

### Creating a Memory with Validation

```python
from jarvis_core.domain.entities.memory import Memory
from jarvis_core.shared.constants import MemoryType

# Create a knowledge memory
memory = Memory(
    key="python_best_practices",
    type=MemoryType.KNOWLEDGE,
    content={
        "title": "Python Best Practices",
        "content": "Always use virtual environments...",
        "category": "programming",
        "tags": ["python", "best-practices"],
        "confidence": 0.95
    }
)

# Add tags for indexing
memory.add_tags(["tutorial", "guide"])
```

### Searching Memories

```python
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository

repository = FileMemoryRepository()

# Search by keywords
results = await repository.search(
    memory_type=MemoryType.KNOWLEDGE,
    keywords=["python", "best practices"],
    limit=10
)

# Search by tags
results = await repository.search(
    tags=["tutorial"],
    limit=20
)

# Search by key pattern
results = await repository.search(
    key_pattern="python_",
    limit=50
)
```

### Managing Strategic Goals

```python
from jarvis_core.application.use_cases.manage_strategic_memory import ManageStrategicMemory

use_case = ManageStrategicMemory(repository)

# Create a strategic goal
goal = await use_case.create_strategic_goal(
    goal="Improve system performance by 50%",
    description="Optimize database queries and caching",
    priority="high",
    target_date=datetime(2024, 12, 31),
    milestones=[
        {"name": "Database optimization", "status": "in_progress"},
        {"name": "Caching implementation", "status": "pending"}
    ],
    metrics={
        "response_time": {"target": "< 200ms", "current": "350ms"}
    }
)

# Update goal progress
await use_case.update_goal_progress(
    goal_key=goal.key,
    progress=25.0
)

# List active goals
active_goals = await use_case.list_active_goals()
```

### Creating Architecture Decision Records (ADRs)

```python
# Create an ADR
adr = await use_case.create_adr(
    title="Use PostgreSQL for primary database",
    context="We need a reliable, ACID-compliant database with good performance",
    decision="We will use PostgreSQL as our primary database",
    consequences="Strong consistency, ACID compliance, mature ecosystem",
    status="accepted",
    alternatives=["MySQL", "MongoDB", "DynamoDB"],
    related_decisions=["adr_002"]
)

# List all ADRs
all_adrs = await use_case.list_adrs()

# List only accepted ADRs
accepted_adrs = await use_case.list_adrs(status="accepted")
```

### Working with Memory Versions

```python
# Memory versions are automatically tracked
memory = Memory(
    key="versioned_doc",
    type=MemoryType.KNOWLEDGE,
    content={"version": "1.0", "data": "initial"}
)

await repository.save(memory)  # Version 1

# Update content (increments version)
memory.update_content({"version": "2.0", "data": "updated"})
await repository.save(memory)  # Version 2

# Retrieve specific version
v1_memory = await repository.get_by_version("versioned_doc", 1)

# List all versions
versions = await repository.list_versions("versioned_doc")
print(versions)  # [1, 2]
```

### Using Memory DTOs

```python
from jarvis_core.application.dto.memory_dto import (
    MemoryDTO,
    MemorySearchQueryDTO,
    MemorySearchResultDTO
)

# Create a validated DTO
dto = MemoryDTO(
    memory_id="mem_123",
    type="knowledge",
    key="my_key",
    content={"title": "Example"},
    created_at=datetime.now(),
    updated_at=datetime.now()
)

# Convert to entity
entity = dto.to_entity()

# Convert from entity
dto = MemoryDTO.from_entity(memory)

# Create a search query
query = MemorySearchQueryDTO(
    memory_type="strategic",
    keywords=["performance"],
    tags=["high-priority"],
    limit=50
)
```

## Memory Types

### Working Memory
Temporary data needed during execution, such as intermediate results or agent state.

**Use Cases:**
- Session data
- Temporary calculations
- Agent state
- Execution context

### Knowledge Memory
Long-term information and learned facts.

**Use Cases:**
- Best practices
- Tutorials
- Documentation
- Historical data
- Reference information

### Strategic Memory
Long-term goals, plans, and strategic decisions.

**Use Cases:**
- Organizational goals
- Strategic objectives
- Long-term planning
- Architecture Decision Records (ADRs)
- Success metrics

### Execution Log
Records of task executions and their results.

**Use Cases:**
- Task history
- Performance metrics
- Error tracking
- Audit trails
- Analytics data

## Schema Validation

All memory content is validated against type-specific Pydantic schemas:

### Working Memory Schema
```python
{
    "data": Dict[str, Any],  # Required
    "session_id": str,        # Optional
    "agent_id": str,          # Optional
    "expires_at": datetime    # Optional
}
```

### Knowledge Memory Schema
```python
{
    "title": str,              # Required, min_length=1
    "content": str,            # Required, min_length=1
    "description": str,        # Optional
    "category": str,           # Optional
    "tags": List[str],         # Optional
    "source": str,             # Optional
    "confidence": float,       # 0.0 to 1.0
    "last_accessed": datetime, # Optional
    "access_count": int        # >= 0
}
```

### Strategic Memory Schema
```python
{
    "goal": str,                      # Required, min_length=1
    "description": str,               # Optional
    "priority": str,                  # low|medium|high|critical
    "status": str,                    # active|paused|completed|cancelled
    "target_date": datetime,          # Optional
    "progress": float,                # 0.0 to 100.0
    "milestones": List[Dict],         # Optional
    "dependencies": List[str],        # Optional
    "metrics": Dict[str, Any]         # Optional
}
```

### Execution Log Schema
```python
{
    "task_id": str,            # Required
    "task_title": str,         # Required
    "agent_type": str,         # Optional
    "status": str,             # pending|in_progress|completed|failed|cancelled
    "started_at": datetime,    # Required
    "completed_at": datetime,  # Optional
    "duration_seconds": float, # >= 0
    "result": Any,             # Optional
    "error": str,              # Optional
    "metrics": Dict[str, Any]  # Optional
}
```

### ADR Schema
```python
{
    "title": str,              # Required, min_length=1
    "status": str,             # proposed|accepted|deprecated|superseded
    "date": datetime,          # Required
    "context": str,            # Required, min_length=1
    "decision": str,           # Required, min_length=1
    "consequences": str,       # Required, min_length=1
    "alternatives": List[str], # Optional
    "related_decisions": List[str],  # Optional
    "superseded_by": str       # Optional
}
```

## Repository Interface

The `IMemoryRepository` interface defines the contract for memory persistence:

```python
class IMemoryRepository(ABC):
    async def get(self, key: str) -> Optional[Memory]
    async def save(self, memory: Memory) -> None
    async def list(self, memory_type: MemoryType) -> List[Memory]
    async def delete(self, key: str) -> None
    async def search(...) -> List[Memory]
    async def get_by_version(self, key: str, version: int) -> Optional[Memory]
    async def list_versions(self, key: str) -> List[int]
```

## Testing

Comprehensive test coverage includes:

- **Unit Tests**: 48 tests for entities, schemas, and DTOs
- **Integration Tests**: 18 tests for repository and use case integration
- **Total**: 118 tests passing with 46% code coverage

Run tests:
```bash
# All tests
pytest tests/

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Memory-specific tests
pytest tests/unit/domain/test_memory_entity.py
pytest tests/unit/domain/test_memory_schemas.py
pytest tests/unit/application/test_memory_dto.py
pytest tests/integration/test_memory_repository.py
pytest tests/integration/test_strategic_memory.py
```

## Architecture

The memory management system follows Clean Architecture principles:

```
Domain Layer:
- entities/memory.py: Core Memory entity
- repositories/i_memory_repository.py: Repository interface
- schemas/memory_content.py: Pydantic schemas

Application Layer:
- dto/memory_dto.py: Data transfer objects
- use_cases/manage_strategic_memory.py: Strategic memory use cases

Infrastructure Layer:
- persistence/file_memory_repository.py: File-based implementation
```

## Future Enhancements

Potential future improvements:

1. **Semantic Search**: Implement vector-based semantic search using embeddings
2. **Memory Compression**: Automatic archival and compression of old memories
3. **Memory Pruning**: Smart cleanup of stale or redundant memories
4. **Distributed Storage**: Support for distributed memory storage
5. **Real-time Sync**: Real-time synchronization across instances
6. **Memory Analytics**: Advanced analytics and insights on memory usage
7. **Memory Migrations**: Automated schema migration tools
8. **Memory Replication**: Cross-region memory replication

## Contributing

When contributing to the memory management system:

1. Ensure all new features have comprehensive tests
2. Follow Pydantic schema patterns for validation
3. Maintain backward compatibility for memory schemas
4. Update documentation for new features
5. Run full test suite before submitting PRs

## License

This is part of the JARVIS project under MIT License.
