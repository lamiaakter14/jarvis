# ADR 002: Schema Validation for Memory Management System

**Status**: Accepted  
**Date**: 2024-02  
**Deciders**: JARVIS Development Team  
**Consulted**: Data Engineering Best Practices, Pydantic Documentation  

---

## Context

The JARVIS memory management system handles critical data across three memory types:

1. **Working Memory**: Active tasks, daily context, execution logs (JSON format)
2. **Knowledge Memory**: Long-term learning, roadmaps, reflections (Markdown/YAML format)
3. **Strategic Memory**: Goals, milestones, architecture decisions (Markdown format)

### Current Challenges

**Data Integrity Issues**:
- No validation when reading/writing memory files
- Potential for malformed JSON or YAML
- Type safety issues leading to runtime errors
- Inconsistent data structures across memory entries

**Developer Experience Problems**:
- Unclear what fields are required vs optional
- No IDE autocomplete for memory objects
- Difficult to track schema changes over time
- No validation during development, errors discovered in production

**Maintenance Concerns**:
- Hard to evolve schemas without breaking existing data
- No versioning strategy for memory formats
- Migration between schema versions is manual and error-prone

### The Need for Schema Validation

To ensure data integrity, improve developer experience, and support long-term maintainability, we need a robust schema validation system that:

- Validates data at runtime before persistence
- Provides clear error messages for invalid data
- Supports schema evolution and versioning
- Integrates seamlessly with existing code

---

## Decision

We will implement **schema validation using Pydantic** for all memory operations in the JARVIS system.

### Why Pydantic?

1. **Runtime Validation**: Validates data at runtime with detailed error messages
2. **Type Safety**: Leverages Python type hints for IDE support
3. **JSON Schema Generation**: Automatically generates JSON schemas for documentation
4. **Performance**: Fast validation using Rust-based validators
5. **Ecosystem**: Wide adoption in FastAPI and modern Python projects
6. **Flexibility**: Supports custom validators and complex nested structures

---

## Implementation Design

### 1. Memory Schema Definitions

Create Pydantic models for all memory types in `core/entities/schemas/`:

```python
# core/entities/schemas/working_memory.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    """Schema for individual tasks in working memory."""
    id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    status: TaskStatus = TaskStatus.PENDING
    priority: int = Field(default=3, ge=1, le=5)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_agent: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('updated_at')
    def updated_must_be_after_created(cls, v, values):
        if 'created_at' in values and v < values['created_at']:
            raise ValueError('updated_at must be >= created_at')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "task-001",
                "title": "Implement schema validation",
                "status": "in_progress",
                "priority": 5
            }
        }

class DailyContext(BaseModel):
    """Schema for daily context in working memory."""
    date: str = Field(..., regex=r'^\d{4}-\d{2}-\d{2}$')
    tasks: List[Task] = Field(default_factory=list)
    focus_areas: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    
class ExecutionLog(BaseModel):
    """Schema for execution logs."""
    log_id: str
    task_id: str
    agent: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str
    details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
```

```python
# core/entities/schemas/knowledge_memory.py
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import date

class LearningEntry(BaseModel):
    """Schema for learning entries in knowledge memory."""
    id: str
    title: str = Field(..., min_length=1)
    content: str
    category: str
    tags: List[str] = Field(default_factory=list)
    source: Optional[HttpUrl] = None
    learned_date: date = Field(default_factory=date.today)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    
class Reflection(BaseModel):
    """Schema for reflection entries."""
    id: str
    date: date
    topic: str
    insights: List[str]
    action_items: List[str] = Field(default_factory=list)
    related_tasks: List[str] = Field(default_factory=list)
```

```python
# core/entities/schemas/strategic_memory.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum

class MilestoneStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

class Milestone(BaseModel):
    """Schema for strategic milestones."""
    id: str
    phase: str
    name: str = Field(..., min_length=1)
    description: str
    target_date: date
    status: MilestoneStatus
    deliverables: List[str]
    dependencies: List[str] = Field(default_factory=list)
    completion_percentage: int = Field(default=0, ge=0, le=100)
    
class Goal(BaseModel):
    """Schema for strategic goals."""
    id: str
    title: str
    description: str
    year: int
    quarter: Optional[int] = Field(None, ge=1, le=4)
    success_metrics: List[str]
    status: str
```

### 2. Memory Manager Integration

Update `MemoryManager` to use Pydantic schemas:

```python
# core/use_cases/memory_operations.py
from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError
from core.entities.schemas.working_memory import DailyContext, Task, ExecutionLog
from adapters.repositories.memory_repository import MemoryRepository

T = TypeVar('T', bound=BaseModel)

class MemoryOperations:
    """Use case for memory CRUD operations with schema validation."""
    
    def __init__(self, repository: MemoryRepository):
        self.repository = repository
    
    def save_with_validation(
        self, 
        file_name: str, 
        data: BaseModel, 
        memory_type: str = "working"
    ) -> None:
        """
        Save data to memory with automatic schema validation.
        
        Args:
            file_name: Target file name
            data: Pydantic model instance (already validated)
            memory_type: Type of memory (working, knowledge, strategic)
            
        Raises:
            ValidationError: If data doesn't match schema
        """
        # Data is already validated by Pydantic at instantiation
        serialized = data.model_dump(mode='json')
        self.repository.save(file_name, serialized, memory_type)
    
    def load_with_validation(
        self, 
        file_name: str, 
        schema: Type[T],
        memory_type: str = "working"
    ) -> T:
        """
        Load data from memory and validate against schema.
        
        Args:
            file_name: Source file name
            schema: Pydantic model class for validation
            memory_type: Type of memory
            
        Returns:
            Validated Pydantic model instance
            
        Raises:
            ValidationError: If loaded data doesn't match schema
        """
        raw_data = self.repository.load(file_name, memory_type)
        
        try:
            return schema.model_validate(raw_data)
        except ValidationError as e:
            # Enhanced error message with context
            raise ValidationError(
                f"Schema validation failed for {file_name}: {e}"
            )
```

### 3. Usage Examples

```python
# Example 1: Saving a task with automatic validation
from core.entities.schemas.working_memory import Task, TaskStatus

# This will validate at instantiation
task = Task(
    id="task-001",
    title="Implement feature X",
    status=TaskStatus.IN_PROGRESS,
    priority=4
)

# Save with validated data
memory_ops.save_with_validation("tasks.json", task)

# Example 2: Loading and validating daily context
daily_context = memory_ops.load_with_validation(
    "daily_context.json", 
    DailyContext
)

# Example 3: Validation error handling
try:
    invalid_task = Task(
        id="task-002",
        title="",  # Violates min_length=1
        priority=10  # Violates le=5
    )
except ValidationError as e:
    print(f"Validation errors: {e.errors()}")
    # Output: List of detailed validation errors
```

---

## Schema Versioning Strategy

### Version Format
Use semantic versioning embedded in schemas: `v{major}.{minor}.{patch}`

```python
class TaskV1(BaseModel):
    schema_version: str = Field(default="v1.0.0", const=True)
    # ... fields ...

class TaskV2(BaseModel):
    schema_version: str = Field(default="v2.0.0", const=True)
    # ... updated fields ...
```

### Migration Support

```python
# core/entities/schemas/migrations.py
from typing import Dict, Any

class SchemaMigrator:
    """Handles schema migrations for backward compatibility."""
    
    def migrate_task_v1_to_v2(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate Task from v1 to v2 schema."""
        if data.get('schema_version') == 'v1.0.0':
            # Apply migration transformations
            data['schema_version'] = 'v2.0.0'
            # Add new required fields with defaults
            data.setdefault('new_field', 'default_value')
        return data
    
    def auto_migrate(self, data: Dict[str, Any], target_schema: Type[BaseModel]):
        """Automatically migrate data to target schema version."""
        current_version = data.get('schema_version', 'v1.0.0')
        target_version = target_schema.model_fields['schema_version'].default
        
        if current_version != target_version:
            # Apply appropriate migration
            migration_func = self._get_migration_func(current_version, target_version)
            return migration_func(data)
        return data
```

---

## Validation Rules and Best Practices

### 1. Required vs Optional Fields
- Use `Field(...)` for required fields
- Use `Optional[Type]` with `Field(None)` for optional fields
- Provide sensible defaults where appropriate

### 2. Field Constraints
- String lengths: `min_length`, `max_length`
- Numeric ranges: `ge` (>=), `le` (<=), `gt` (>), `lt` (<)
- Regex patterns: `regex=r'pattern'`
- Custom validators: `@validator` decorator

### 3. Nested Validation
```python
class AgentResponse(BaseModel):
    agent_id: str
    tasks: List[Task]  # Automatically validates each task
    context: DailyContext  # Validates nested structure
```

### 4. Custom Validators
```python
@validator('email')
def validate_email(cls, v):
    if '@' not in v:
        raise ValueError('Invalid email format')
    return v.lower()
```

### 5. Documentation
- Use `Field(description="...")` for field documentation
- Provide `json_schema_extra` with examples
- Generate JSON schemas for API documentation

---

## Testing Strategy

### 1. Schema Unit Tests
```python
# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from core.entities.schemas.working_memory import Task, TaskStatus

def test_task_valid_creation():
    task = Task(id="test-1", title="Test Task")
    assert task.status == TaskStatus.PENDING
    assert task.priority == 3

def test_task_invalid_priority():
    with pytest.raises(ValidationError) as exc_info:
        Task(id="test-1", title="Test", priority=10)
    assert 'priority' in str(exc_info.value)

def test_task_serialization():
    task = Task(id="test-1", title="Test")
    data = task.model_dump()
    assert isinstance(data, dict)
    assert data['id'] == 'test-1'
```

### 2. Integration Tests
```python
def test_memory_save_with_validation(memory_ops):
    task = Task(id="test-1", title="Integration Test")
    memory_ops.save_with_validation("test_task.json", task)
    
    loaded = memory_ops.load_with_validation("test_task.json", Task)
    assert loaded.id == task.id
    assert loaded.title == task.title
```

### 3. Migration Tests
```python
def test_schema_migration():
    # Legacy data in v1 format
    v1_data = {"id": "task-1", "title": "Old Task", "schema_version": "v1.0.0"}
    
    migrator = SchemaMigrator()
    v2_data = migrator.migrate_task_v1_to_v2(v1_data)
    
    # Validate against v2 schema
    task_v2 = TaskV2.model_validate(v2_data)
    assert task_v2.schema_version == "v2.0.0"
```

---

## Performance Considerations

### Benchmarks
- Pydantic validation: ~1-5ms per object (acceptable for our use case)
- JSON serialization: Minimal overhead with `model_dump()`
- Memory footprint: Negligible increase

### Optimization Strategies
1. **Lazy Validation**: Only validate on write, trust read data (with option to validate)
2. **Caching**: Cache validated schemas for repeated operations
3. **Partial Validation**: Use `model_validate_partial()` for updates
4. **Compiled Mode**: Use Pydantic V2's compiled validators for 2-3x speed boost

---

## Consequences

### Positive Consequences
✅ **Data Integrity**: Prevents invalid data from entering the system  
✅ **Developer Experience**: Type hints and IDE autocomplete  
✅ **Self-Documentation**: Schemas serve as documentation  
✅ **Refactoring Safety**: Breaking changes caught at validation time  
✅ **API Integration**: Easy JSON schema generation for APIs  
✅ **Testing**: Easier to write tests with clear schemas  
✅ **Versioning**: Built-in support for schema evolution  

### Negative Consequences
⚠️ **Performance Overhead**: Small validation cost (1-5ms per operation)  
⚠️ **Migration Effort**: Existing data needs migration to new schemas  
⚠️ **Learning Curve**: Team needs to learn Pydantic patterns  
⚠️ **Verbosity**: More code for schema definitions  

### Mitigation Strategies
- Schema validation is fast enough for our use case
- Provide migration scripts for existing data
- Training and documentation for team
- Use schema generators for repetitive patterns

---

## Rollout Plan

### Phase 1: Schema Definition (Week 1)
- [ ] Define all Pydantic schemas for existing memory types
- [ ] Create schema documentation and examples
- [ ] Set up validation test suite

### Phase 2: Memory Manager Integration (Week 2)
- [ ] Update MemoryManager to use schemas
- [ ] Add validation layer to all save/load operations
- [ ] Implement error handling and logging

### Phase 3: Data Migration (Week 3)
- [ ] Analyze existing memory data
- [ ] Create migration scripts
- [ ] Migrate working memory data
- [ ] Migrate knowledge memory data

### Phase 4: Testing & Validation (Week 4)
- [ ] Run comprehensive test suite
- [ ] Validate no regressions
- [ ] Performance testing
- [ ] Update documentation

---

## Compliance and Monitoring

### Enforcement
1. **Pre-commit Hooks**: Validate schema changes don't break existing data
2. **CI/CD Checks**: Schema validation tests in pipeline
3. **Code Review**: Require schema updates for memory changes

### Monitoring
1. **Validation Errors**: Log all validation failures
2. **Schema Drift**: Alert on schema version mismatches
3. **Performance Metrics**: Track validation overhead

---

## References

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JSON Schema Specification](https://json-schema.org/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Data Validation Best Practices](https://martinfowler.com/articles/data-validation.html)

---

## Alternatives Considered

### Alternative 1: JSONSchema
**Pros**: Language-agnostic, widely supported  
**Cons**: External validation, no Python type integration  
**Verdict**: Rejected - Pydantic provides better DX

### Alternative 2: Marshmallow
**Pros**: Mature, similar features to Pydantic  
**Cons**: Slower, less modern API, less adoption  
**Verdict**: Rejected - Pydantic is faster and more popular

### Alternative 3: No Validation
**Pros**: No overhead, simpler code  
**Cons**: Data integrity issues, runtime errors  
**Verdict**: Rejected - Unacceptable for production system

### Alternative 4: Custom Validation
**Pros**: Full control  
**Cons**: Reinventing the wheel, maintenance burden  
**Verdict**: Rejected - Pydantic provides all needed features

---

## Review and Updates

- **Initial Decision**: February 2024
- **Implementation Start**: Milestone 1.4
- **Next Review**: End of Milestone 1.5
- **Owner**: Data Architecture Team

---

**Approval Signatures**:
- [x] Technical Lead
- [x] Data Engineering Lead
- [x] Development Team Lead

**Status**: ✅ Accepted and Implementation in Progress
