# JARVIS Clean Architecture Overview

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   REST API      │  │   CLI (Typer)    │  │  Legacy Script │ │
│  │   (FastAPI)     │  │   + Rich UI      │  │   (Bridge)     │ │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬───────┘ │
└───────────┼──────────────────────┼─────────────────────┼─────────┘
            │                      │                     │
            └──────────────────────┼─────────────────────┘
                                   │
┌──────────────────────────────────┼──────────────────────────────┐
│              APPLICATION LAYER   │                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              USE CASES (Orchestration)                   │   │
│  ├──────────────────────────────────────────────────────────┤  │
│  │  • ExecuteCognitiveLoop  • GenerateDailyPlan            │   │
│  │  • ExecuteTasks          • IdentifyGaps                 │   │
│  │  • CreateInnovations     • AnalyzePerformance           │   │
│  └──────────────────┬──────────────────────────────────────┘   │
│  ┌─────────────────┴──────────────────┐                        │
│  │   DTOs (Data Transfer Objects)     │                        │
│  │   • TaskDTO  • PlanDTO             │                        │
│  │   • AnalyticsDTO                   │                        │
│  └────────────────────────────────────┘                        │
└───────────────────────────┬────────────────────────────────────┘
                            │
┌───────────────────────────┼────────────────────────────────────┐
│              DOMAIN LAYER │                                    │
│  ┌────────────────────────┴──────────────────────────────┐    │
│  │  ENTITIES (Core Business Objects)                     │    │
│  │  • Task • Plan • Context • Innovation • Memory        │    │
│  └───────────────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  VALUE OBJECTS (Immutable Values)                     │    │
│  │  • Priority • CognitiveLoad • ROI • AgentType         │    │
│  └───────────────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  DOMAIN SERVICES (Business Logic)                     │    │
│  │  • StrategyEngine • InnovationEngine                  │    │
│  │  • MemoryCoordinator • AgentOrchestrator              │    │
│  └───────────────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  REPOSITORY INTERFACES (Ports)                        │    │
│  │  • ITaskRepository • IMemoryRepository                │    │
│  │  • IAnalyticsRepository • IAgentRepository            │    │
│  └───────────────────────────────────────────────────────┘    │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  DOMAIN EVENTS                                        │    │
│  │  • TaskCompletedEvent • GapIdentifiedEvent            │    │
│  │  • InnovationCreatedEvent                             │    │
│  └───────────────────────────────────────────────────────┘    │
└──────────────────────────┬─────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│         INFRASTRUCTURE LAYER                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  AGENTS (Implementation)                                │   │
│  │  • StrategistAgent  • MentorAgent  • ExecutorAgent     │   │
│  │  • InnovatorAgent   • AmplifierAgent                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PERSISTENCE (Repository Implementations)              │   │
│  │  • FileMemoryRepository  • SQLiteTaskRepository        │   │
│  │  • JSONStorage                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  EXTERNAL SERVICES (Adapters)                          │   │
│  │  • OpenAIService  • LangChainService                   │   │
│  │  • NotificationService                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  MONITORING & OBSERVABILITY                            │   │
│  │  • StructuredLogger  • Tracer  • MetricsCollector      │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CONFIGURATION & DI                                     │   │
│  │  • Settings (Pydantic)  • DI Container                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Dependency Flow

```
Presentation Layer
        ↓  (depends on)
Application Layer
        ↓  (depends on)
Domain Layer
        ↑  (implements)
Infrastructure Layer
```

**KEY PRINCIPLE: Dependencies point INWARD**
- Domain Layer has ZERO external dependencies
- Application Layer depends only on Domain
- Infrastructure implements Domain interfaces
- Presentation uses Application (through DI)

## Component Interactions

### Cognitive Loop Execution Flow

```
1. CLI/API Request
        ↓
2. ExecuteCognitiveLoop Use Case
        ↓
3. Calls Individual Use Cases:
   ├─→ GenerateDailyPlan (Strategist)
   ├─→ IdentifyGaps (Mentor)
   ├─→ ExecuteTasks (Executor)
   ├─→ CreateInnovations (Innovator)
   └─→ AnalyzePerformance (Amplifier)
        ↓
4. Use Cases call Domain Services
        ↓
5. Domain Services use Entities & Value Objects
        ↓
6. Repositories save/retrieve data (Infrastructure)
        ↓
7. Results flow back up through DTOs
        ↓
8. Response to CLI/API
```

## Layer Responsibilities

### 1. Domain Layer (Pure Business Logic)
**What it does:**
- Defines core entities (Task, Plan, Innovation, etc.)
- Defines value objects (Priority, ROI, etc.)
- Contains business rules (StrategyEngine, InnovationEngine)
- Declares repository interfaces (what data we need, not how to get it)

**What it does NOT do:**
- No database access
- No HTTP/API calls
- No framework dependencies
- No infrastructure concerns

**Example:**
```python
# Task entity knows how to mark itself completed
task.mark_completed(result={"success": True})

# StrategyEngine knows how to prioritize tasks
prioritized = strategy_engine.prioritize_tasks(tasks)
```

### 2. Application Layer (Use Cases)
**What it does:**
- Orchestrates domain objects to fulfill use cases
- Coordinates repository calls
- Emits domain events
- Converts between DTOs and Entities
- Handles application flow

**What it does NOT do:**
- No business logic (delegates to domain services)
- No direct infrastructure access (uses interfaces)
- No presentation concerns

**Example:**
```python
class GenerateDailyPlan:
    def __init__(self, task_repo, memory_repo, ai_service, strategy_engine):
        self._task_repo = task_repo
        self._memory_repo = memory_repo
        self._ai_service = ai_service
        self._strategy = strategy_engine
    
    async def execute(self, date, hours):
        # 1. Load data via repositories
        tasks = await self._task_repo.get_pending()
        context = await self._memory_repo.retrieve("context")
        
        # 2. Use domain service for business logic
        prioritized = self._strategy.prioritize_tasks(tasks)
        plan = self._strategy.create_schedule(prioritized, hours)
        
        # 3. Save and return
        await self._memory_repo.save("plan", plan.to_dict())
        return PlanDTO.from_entity(plan)
```

### 3. Infrastructure Layer (Implementation Details)
**What it does:**
- Implements repository interfaces
- Handles database access (SQLite, Files, JSON)
- Integrates with external services (OpenAI, APIs)
- Provides concrete agent implementations
- Handles monitoring and logging
- Manages configuration

**Example:**
```python
class FileMemoryRepository(IMemoryRepository):
    def __init__(self, base_path):
        self.base_path = Path(base_path)
    
    async def save(self, memory_type, key, data):
        path = self.base_path / memory_type / f"{key}.json"
        with open(path, 'w') as f:
            json.dump(data, f)
```

### 4. Presentation Layer (User Interfaces)
**What it does:**
- Provides REST API endpoints (FastAPI)
- Provides CLI commands (Typer)
- Handles HTTP requests/responses
- Formats output for users
- Validates input
- Manages authentication/authorization

**Example:**
```python
@app.post("/api/cognitive-loop")
async def run_cognitive_loop():
    # Use case orchestration
    result = await execute_cognitive_loop_use_case.execute()
    return {"status": "success", "data": result}
```

## Testing Strategy

### Unit Tests (70% of tests)
- **Domain Layer**: Test entities, value objects, services with NO mocks
- **Application Layer**: Test use cases with mocked repositories
- Target: Fast, isolated, deterministic

### Integration Tests (20% of tests)
- **Repository Implementations**: Test with real file system/database
- **Agent Implementations**: Test with mocked AI services
- Target: Verify components work together

### E2E Tests (10% of tests)
- **Full Cognitive Loop**: Test entire flow
- **API Endpoints**: Test HTTP requests/responses
- **CLI Commands**: Test command execution
- Target: Verify system works end-to-end

## Benefits Achieved

### ✅ Testability
- Domain logic testable without mocks
- Can test business rules in isolation
- Easy to mock dependencies

### ✅ Flexibility
- Can swap file storage for database
- Can swap OpenAI for different LLM
- Can add new agents easily

### ✅ Maintainability
- Clear separation of concerns
- Each layer has single responsibility
- Changes isolated to specific layers

### ✅ Scalability
- Can deploy as API, CLI, or background worker
- Can scale horizontally
- Can add caching, queuing, etc.

### ✅ Independent Development
- Teams can work on different layers
- Can develop domain logic before deciding on database
- Can change UI without touching business logic

## Migration Strategy

### Phase 1: Coexistence (CURRENT)
- ✅ New architecture fully implemented
- ✅ Bridge layer provides backward compatibility
- ✅ Old scripts continue to work
- ✅ No breaking changes

### Phase 2: Gradual Migration (NEXT)
- [ ] Migrate old scripts to use new architecture directly
- [ ] Remove bridge layer
- [ ] Update all entry points
- [ ] Deprecate old code

### Phase 3: Complete Transition (COMPLETED ✓)
- [x] Remove old `agents/` and `core/` directories
- [x] All code uses clean architecture
- [x] Update all documentation
- [ ] Training for team

## Key Design Patterns Used

1. **Repository Pattern**: Abstract data access
2. **Use Case Pattern**: Single-responsibility use cases
3. **DTO Pattern**: Data transfer across boundaries
4. **Dependency Injection**: Constructor injection throughout
5. **Interface Segregation**: Small, focused interfaces
6. **Factory Pattern**: Value object creation
7. **Event-Driven**: Domain events for state changes
8. **Adapter Pattern**: Bridge layer for compatibility

## Next Enhancements

### Short Term
- [ ] Increase test coverage to 90%
- [ ] Complete DI container setup
- [ ] Add API authentication
- [ ] WebSocket support for real-time updates

### Medium Term
- [ ] Event bus implementation
- [ ] Caching layer
- [ ] Message queue integration
- [ ] Performance optimization

### Long Term
- [ ] Microservices architecture
- [ ] Distributed tracing
- [ ] Advanced analytics
- [ ] Machine learning integration
