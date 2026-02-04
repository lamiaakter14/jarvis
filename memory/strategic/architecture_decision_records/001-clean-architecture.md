# ADR 001: Adoption of Clean Architecture Principles

**Status**: Accepted  
**Date**: 2024-02  
**Deciders**: JARVIS Development Team  
**Consulted**: Software Architecture Community Best Practices  

---

## Context

As the JARVIS project grows in complexity with multiple agents, memory systems, and integration points, we need a robust architectural approach that:

1. **Maintains separation of concerns** across different system components
2. **Enables independent testing** of core business logic without external dependencies
3. **Facilitates extensibility** for adding new agents and features
4. **Supports long-term maintainability** as the codebase scales
5. **Allows flexibility** to swap out infrastructure components (databases, APIs, etc.)

The current implementation has basic modularity, but lacks clear architectural boundaries and dependency rules that would ensure long-term code health.

---

## Decision

We will adopt **Clean Architecture** principles (as defined by Robert C. Martin) with the following layered structure:

### Layer 1: Entities (Core Domain)
**Location**: `core/entities/`  
**Purpose**: Business objects and domain models  
**Dependencies**: None (pure Python, no external dependencies)

**Components**:
- `Task`: Core task representation with state and metadata
- `Memory`: Abstract memory models (Working, Knowledge, Strategic)
- `Agent`: Base agent interface and contracts
- `Context`: Execution context and state management

**Rules**:
- No dependencies on outer layers
- Contains core business logic and rules
- Framework-agnostic, pure domain models

### Layer 2: Use Cases (Application Business Rules)
**Location**: `core/use_cases/`  
**Purpose**: Application-specific business rules and orchestration  
**Dependencies**: Only on Entities layer

**Components**:
- `ExecuteTask`: Task execution orchestration
- `ManageMemory`: Memory CRUD operations
- `CoordinateAgents`: Agent coordination logic
- `AnalyzePerformance`: Performance tracking and analysis

**Rules**:
- Defines application workflows
- Orchestrates entities to fulfill use cases
- Input/output ports defined as interfaces

### Layer 3: Interface Adapters
**Location**: `adapters/`  
**Purpose**: Convert data between use cases and external interfaces  
**Dependencies**: Entities and Use Cases layers

**Components**:
- `controllers/`: API controllers (FastAPI routes)
- `presenters/`: Output formatting and presentation logic
- `gateways/`: Interface to external systems (OpenAI, databases)
- `repositories/`: Data access abstractions

**Rules**:
- Converts data formats between layers
- Implements interfaces defined in use cases
- No business logic (only conversion and delegation)

### Layer 4: Frameworks & Drivers (External)
**Location**: `infrastructure/`  
**Purpose**: External frameworks, tools, and drivers  
**Dependencies**: All inner layers

**Components**:
- `api/`: FastAPI application setup
- `database/`: Database connections and configurations
- `external/`: Third-party service integrations
- `config/`: Environment and configuration management

**Rules**:
- Contains glue code and configurations
- Framework-specific implementations
- Easily swappable without affecting core logic

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  Frameworks & Drivers (Infrastructure)                  │
│  - FastAPI, OpenAI SDK, File System                     │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Interface Adapters                                      │
│  - Controllers, Presenters, Gateways, Repositories       │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Use Cases (Application Business Rules)                 │
│  - Execute Task, Manage Memory, Coordinate Agents        │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│  Entities (Enterprise Business Rules)                   │
│  - Task, Memory, Agent, Context                          │
└─────────────────────────────────────────────────────────┘
```

**Dependency Rule**: Dependencies only point inward. Inner layers know nothing about outer layers.

---

## Current Implementation Mapping

### Existing Structure → Clean Architecture

**Current `agents/` directory**:
- Move core agent logic → `core/entities/agent_base.py`
- Move agent implementations → `adapters/agents/` (as they interact with external AI)
- Create agent use cases → `core/use_cases/agent_coordination.py`

**Current `core/` directory**:
- `cognitive_loop.py` → Split into:
  - Domain logic → `core/entities/cognitive_context.py`
  - Use case orchestration → `core/use_cases/execute_cognitive_loop.py`
  - Controller → `adapters/controllers/cognitive_controller.py`
  
- `memory_manager.py` → Split into:
  - Memory entities → `core/entities/memory.py`
  - Memory use cases → `core/use_cases/memory_operations.py`
  - Repository interface → `adapters/repositories/memory_repository.py`
  - File system implementation → `infrastructure/storage/file_memory_storage.py`

**Current `scripts/` directory**:
- Keep as-is (these are CLI tools that depend on all layers)

---

## Migration Strategy

### Phase 1: Foundation (Immediate)
1. Create new directory structure without breaking existing code
2. Define core entity interfaces in `core/entities/`
3. Extract pure business logic into entities
4. Create use case interfaces and contracts

### Phase 2: Refactoring (2-3 weeks)
1. Move agent implementations to adapters
2. Refactor `cognitive_loop.py` into layered components
3. Separate `memory_manager.py` into entity, use case, and repository
4. Update imports across the codebase

### Phase 3: Testing & Validation (1 week)
1. Ensure all tests pass with new structure
2. Add integration tests for layer boundaries
3. Verify no regression in functionality
4. Update documentation

### Phase 4: Cleanup (Ongoing)
1. Remove old deprecated code paths
2. Enforce architectural boundaries with linting rules
3. Document architectural patterns for future development

---

## Consequences

### Positive Consequences
✅ **Testability**: Core business logic can be tested without external dependencies  
✅ **Flexibility**: Easy to swap infrastructure (e.g., switch from file storage to database)  
✅ **Maintainability**: Clear separation makes code easier to understand and modify  
✅ **Scalability**: Architecture supports growth without major refactoring  
✅ **Independence**: Business logic is independent of frameworks and tools  
✅ **Onboarding**: New developers can understand system structure quickly  

### Negative Consequences
⚠️ **Initial complexity**: More files and abstractions initially  
⚠️ **Migration effort**: Requires refactoring existing code  
⚠️ **Learning curve**: Team needs to understand clean architecture principles  
⚠️ **Potential over-engineering**: For very simple features, layering might feel excessive  

### Mitigation Strategies
- Provide clear documentation and examples
- Gradual migration to minimize disruption
- Training sessions on clean architecture principles
- Pragmatic application (don't over-abstract simple cases)

---

## Validation and Compliance

### Architectural Rules to Enforce

1. **Dependency Rule**: Use tools like `import-linter` to ensure dependencies only point inward
   ```python
   # Example config in .importlinter
   [importlinter:contract:1]
   name = Entities have no external dependencies
   type = forbidden
   source_modules = core.entities
   forbidden_modules = adapters, infrastructure
   ```

2. **Interface Contracts**: All cross-layer interactions use interfaces (ABC classes)
   ```python
   # Example
   class MemoryRepository(ABC):
       @abstractmethod
       def save(self, memory: Memory) -> None: ...
   ```

3. **Testing Requirements**:
   - Entities: Unit tests with zero mocks
   - Use Cases: Unit tests with mocked repositories
   - Adapters: Integration tests with real dependencies

---

## References

- **Clean Architecture** by Robert C. Martin (Uncle Bob)
- **Hexagonal Architecture** (Ports and Adapters) by Alistair Cockburn
- **Domain-Driven Design** by Eric Evans
- [The Clean Architecture Blog Post](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## Alternatives Considered

### Alternative 1: MVC Pattern
**Pros**: Simpler, widely understood  
**Cons**: Doesn't enforce dependency rules, tighter coupling between layers  
**Verdict**: Rejected - Insufficient separation for our complexity

### Alternative 2: Microservices from the Start
**Pros**: Maximum flexibility and scalability  
**Cons**: Operational complexity, premature for current scale  
**Verdict**: Deferred - Will consider in Phase 4 (Scaling)

### Alternative 3: Continue with Current Structure
**Pros**: No migration effort  
**Cons**: Technical debt will grow, harder to maintain and test  
**Verdict**: Rejected - Not sustainable for long-term goals

---

## Review and Updates

- **Initial Decision**: February 2024
- **Implementation Start**: Milestone 1.4
- **Next Review**: End of Phase 1 (Month 6)
- **Owner**: Technical Lead

---

**Approval Signatures**:
- [x] Technical Lead
- [x] Architecture Review Board
- [x] Development Team Lead

**Status**: ✅ Accepted and In Progress
