# Memory Management System

## Overview

The JARVIS memory management system provides a comprehensive framework for storing, retrieving, and managing different types of memories including working memory, knowledge, strategic goals, and execution logs. The system supports schema validation, versioning, **indexed storage**, and advanced search capabilities.

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

**New in Phase 1**: ADR content validation is now fully integrated with the `validate_memory_content()` function, supporting the `'adr'` memory type parameter.

### 2. Memory Indexing and Search

Advanced search capabilities for efficient knowledge retrieval:

- **Keyword Search**: Search memory content by keywords
- **Key Pattern Matching**: Find memories by key patterns
- **Tag-based Search**: Filter memories using tags
- **Type Filtering**: Search within specific memory types
- **Pagination Support**: Handle large result sets efficiently

**New in Phase 1**: Strategic memory now includes a dedicated indexing system (`StrategicMemoryIndex`) that provides:
- **Fast O(1) Lookups**: Indexed searches by priority, status, tags, and type
- **Persistent Index**: Automatic persistence to `.index.json` file
- **Multi-criteria Search**: Combined searches with union/intersection support
- **Statistics & Metadata**: Real-time statistics on strategic memory usage
- **Automatic Updates**: Index automatically maintained on save/delete operations

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

### Using Strategic Memory Index

**New in Phase 1**: Direct access to the strategic memory index for advanced queries:

```python
from jarvis_core.infrastructure.persistence.file_memory_repository import FileMemoryRepository

repository = FileMemoryRepository()
index = repository.strategic_index

# Find goals by priority
critical_goals = index.find_by_priority("critical")
high_priority_goals = index.find_by_priority("high")

# Find by status
active_goals = index.find_by_status("active")
completed_goals = index.find_by_status("completed")

# Find ADRs
all_adrs = index.find_by_type("adr")
accepted_adrs = index.find_by_status("accepted")

# Find by tags (any match)
perf_related = index.find_by_tags(["performance", "optimization"], match_all=False)

# Find by tags (all must match)
backend_high_priority = index.find_by_tags(["backend", "high"], match_all=True)

# Get statistics
stats = index.get_statistics()
print(f"Total strategic entries: {stats['total_entries']}")
print(f"Goals: {stats['by_type']['goal']}")
print(f"ADRs: {stats['by_type']['adr']}")
print(f"Active goals: {stats['by_status']['active']}")
print(f"Most used tags: {stats['most_used_tags'][:5]}")

# Get metadata for a specific entry
metadata = index.get_metadata("goal_123")
print(f"Type: {metadata['type']}")
print(f"Priority: {metadata['priority']}")
print(f"Tags: {metadata['tags']}")
```

### Validating Memory Content

**New in Phase 1**: Validate ADR content directly:

```python
from jarvis_core.domain.schemas.memory_content import validate_memory_content
from datetime import datetime

# Validate an ADR
adr_content = {
    "title": "Use microservices architecture",
    "status": "proposed",
    "date": datetime.now(),
    "context": "System scaling requirements",
    "decision": "Adopt microservices pattern",
    "consequences": "Improved scalability but increased complexity",
    "alternatives": ["Monolithic", "Serverless"]
}

validated_adr = validate_memory_content("adr", adr_content)
print(f"Valid ADR: {validated_adr.title}")

# Validate strategic goal
goal_content = {
    "goal": "Reduce latency by 50%",
    "priority": "high",
    "status": "active",
    "progress": 25.0
}

validated_goal = validate_memory_content("strategic", goal_content)
print(f"Valid goal: {validated_goal.goal}")
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

- **Unit Tests**: 
  - 24 tests for memory schemas (including ADR validation)
  - 10 tests for strategic memory index
- **Integration Tests**: 
  - 9 tests for strategic memory use cases
  - 9 tests for indexed storage integration
- **Total**: 52+ memory-related tests passing with high code coverage
  - Memory schemas: 100% coverage
  - Strategic memory index: 94% coverage
  - File memory repository: 70% coverage

Run tests:
```bash
# All memory tests
pytest tests/unit/domain/test_memory_schemas.py
pytest tests/unit/infrastructure/test_strategic_memory_index.py
pytest tests/integration/test_strategic_memory.py
pytest tests/integration/test_strategic_memory_index.py

# Unit tests only
pytest tests/unit/ -k memory

# Integration tests only
pytest tests/integration/ -k strategic_memory

# Run with coverage
pytest tests/unit/infrastructure/test_strategic_memory_index.py --cov=jarvis_core.infrastructure.persistence.strategic_memory_index
```

## Architecture

The memory management system follows Clean Architecture principles:

```
Domain Layer:
- entities/memory.py: Core Memory entity
- repositories/i_memory_repository.py: Repository interface
- schemas/memory_content.py: Pydantic schemas with ADR validation

Application Layer:
- dto/memory_dto.py: Data transfer objects
- use_cases/manage_strategic_memory.py: Strategic memory use cases

Infrastructure Layer:
- persistence/file_memory_repository.py: File-based implementation with indexing
- persistence/strategic_memory_index.py: Indexed storage for strategic memory (NEW)
- persistence/json_storage.py: JSON file storage
```

### Strategic Memory Index Architecture

The new indexing system provides efficient lookups for strategic memory:

```
StrategicMemoryIndex
├── In-Memory Indexes
│   ├── by_priority: {critical, high, medium, low} → Set[key]
│   ├── by_status: {active, paused, completed, ...} → Set[key]
│   ├── by_tag: {tag} → Set[key]
│   └── by_type: {goal, adr} → Set[key]
├── Metadata Store: key → {type, priority, status, tags, indexed_at}
└── Persistent Storage: .index.json (auto-saved)

Integration with FileMemoryRepository:
- save() → automatically updates index
- delete() → automatically removes from index
- search() → uses index for fast tag-based queries
```

## Future Enhancements

Potential future improvements:

1. ~~**Strategic Memory Indexing**: Indexed storage for fast strategic memory lookups~~ ✅ **COMPLETED in Phase 1**
2. ~~**ADR Schema Validation**: Full validation support for Architecture Decision Records~~ ✅ **COMPLETED in Phase 1**
3. **Semantic Search**: Implement vector-based semantic search using embeddings
4. **Memory Compression**: Automatic archival and compression of old memories
5. **Memory Pruning**: Smart cleanup of stale or redundant memories
6. **Distributed Storage**: Support for distributed memory storage
7. **Real-time Sync**: Real-time synchronization across instances
8. **Memory Analytics**: Advanced analytics and insights on memory usage
9. **Memory Migrations**: Automated schema migration tools
10. **Memory Replication**: Cross-region memory replication

### Phase 1 Completed Features

✅ **Strategic Memory Indexed Storage**
- In-memory and persistent indexes for goals and ADRs
- O(1) lookup performance by priority, status, tags, and type
- Automatic index maintenance on save/delete
- Statistics and metadata tracking
- Backward compatible with existing API

✅ **ADR Schema Validation**
- ADRContent fully integrated with validate_memory_content()
- Comprehensive validation for ADR fields
- Status validation (proposed, accepted, deprecated, superseded)
- Support for alternatives and related decisions tracking

## Contributing

When contributing to the memory management system:

1. Ensure all new features have comprehensive tests
2. Follow Pydantic schema patterns for validation
3. Maintain backward compatibility for memory schemas
4. Update documentation for new features
5. Run full test suite before submitting PRs

## License

This is part of the JARVIS project under MIT License.
