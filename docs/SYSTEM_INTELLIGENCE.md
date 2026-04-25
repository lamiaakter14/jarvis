# JARVIS System Intelligence — Full Technical Report

> **Audience**: Developers, contributors, and serious users who want a complete understanding of JARVIS internals, design decisions, and system behaviour.

---

## Table of Contents

1. [What is JARVIS?](#1-what-is-jarvis)
2. [Core Philosophy](#2-core-philosophy)
3. [The Cognitive Loop](#3-the-cognitive-loop)
4. [Six Specialized Agents](#4-six-specialized-agents)
5. [Three-Tier Memory System](#5-three-tier-memory-system)
6. [Clean Architecture](#6-clean-architecture)
7. [API & Interfaces](#7-api--interfaces)
8. [Security Model](#8-security-model)
9. [Observability & Metrics](#9-observability--metrics)
10. [Technology Stack](#10-technology-stack)
11. [Testing Strategy](#11-testing-strategy)
12. [Deployment Architecture](#12-deployment-architecture)
13. [Extension Points](#13-extension-points)
14. [Design Decisions (ADRs)](#14-design-decisions-adrs)
15. [Known Limitations & Roadmap](#15-known-limitations--roadmap)

---

## 1. What is JARVIS?

JARVIS is an **enterprise-grade AI cognitive assistant** built on a multi-agent architecture. It is not a single model wrapper — it is an orchestrated system of six purpose-built agents that collaborate through a shared cognitive loop to help users with:

- Strategic planning and prioritisation
- Task execution and progress tracking
- Gap identification and knowledge coaching
- Innovation generation
- Performance amplification
- Meta-cognitive self-reflection and course correction

JARVIS is designed from the ground up with **Clean Architecture** so that business logic is completely independent of AI provider, database, or interface choice.

---

## 2. Core Philosophy

| Principle | Description |
|-----------|-------------|
| **Cognitive autonomy** | JARVIS reasons, reflects, and self-corrects rather than passively responding |
| **Architecture purity** | Domain logic has zero infrastructure dependencies — can test everything without touching a database or LLM |
| **Separation of concerns** | Each of the six agents has a single, well-defined cognitive role |
| **Memory continuity** | A three-tier memory system maintains context across sessions |
| **Composability** | Agents can be run independently or coordinated through the full cognitive loop |

---

## 3. The Cognitive Loop

The cognitive loop is the central execution cycle of JARVIS. Each cycle activates all six agents in a coordinated sequence, producing a coherent output from their combined reasoning.

### Execution Sequence

```
Input (user request / scheduled trigger)
        │
        ▼
┌───────────────────────────────────────┐
│   ExecuteCognitiveLoop (Use Case)     │
│                                       │
│  1. GenerateDailyPlan   → STRATEGIST  │
│  2. IdentifyGaps        → MENTOR      │
│  3. ExecuteTasks        → EXECUTOR    │
│  4. CreateInnovations   → INNOVATOR   │
│  5. AnalyzePerformance  → AMPLIFIER   │
│  6. ReflectAndCorrect   → REFLECTOR   │
└───────────────────────────────────────┘
        │
        ▼
Output (plan, results, reflections, corrections)
        │
        ▼
Memory updated (Episodic + Semantic + Strategic)
```

### Agent Coordination

Agents run with **priority-based task queuing** managed by `AgentCoordinator`:

- **Critical** → **High** → **Medium** → **Low**
- Parallel execution with semaphore-based concurrency control
- Each agent registers its capabilities on startup
- The coordinator handles failure isolation — one failing agent does not abort the loop

### Triggering the Loop

| Method | Path |
|--------|------|
| REST API | `POST /api/cognitive-loop` |
| CLI | `make cli ARGS="loop run"` |
| Scheduled | Configurable cron via environment |
| WebSocket | Real-time trigger + streaming updates |

---

## 4. Six Specialized Agents

### STRATEGIST

**Role**: Plans and organises tasks, breaks down complex goals into prioritised, actionable steps.

**Use Case**: `GenerateDailyPlan`

**Responsibilities**:
- Loads pending tasks from task repository
- Retrieves current context from working memory
- Applies `StrategyEngine` to prioritise tasks by ROI and cognitive load
- Produces a time-blocked daily schedule
- Writes the plan to strategic memory

**Key Domain Service**: `StrategyEngine.prioritize_tasks()`, `StrategyEngine.create_schedule()`

---

### MENTOR

**Role**: Identifies knowledge gaps, provides guidance, and surfaces coaching recommendations.

**Use Case**: `IdentifyGaps`

**Responsibilities**:
- Analyses completed and failed tasks for patterns
- Queries semantic memory for related knowledge
- Produces a ranked list of knowledge gaps
- Attaches learning suggestions to each gap
- Updates `gaps` field in working memory

**Key Domain Service**: `MemoryCoordinator.retrieve_semantic()`

---

### EXECUTOR

**Role**: Drives the actual execution of tasks and manages implementation progress.

**Use Case**: `ExecuteTasks`

**Responsibilities**:
- Selects tasks from the daily plan by priority
- Dispatches execution (AI-assisted or rule-based)
- Updates task status in `SQLiteTaskRepository`
- Logs execution events to episodic memory
- Reports success/failure outcomes per task

**Key Domain Service**: `AgentOrchestrator.execute()`

---

### INNOVATOR

**Role**: Generates creative approaches and novel solutions to identified problems.

**Use Case**: `CreateInnovations`

**Responsibilities**:
- Reads gap list produced by MENTOR
- Queries LLM with structured prompts for innovative ideas
- Scores ideas by feasibility and ROI
- Persists top-N innovations to knowledge memory
- Tags innovations with relevant task and gap IDs

**Key Domain Service**: `InnovationEngine.score()`, `InnovationEngine.generate()`

---

### AMPLIFIER

**Role**: Analyses performance metrics and recommends optimisations.

**Use Case**: `AnalyzePerformance`

**Responsibilities**:
- Reads execution logs from episodic memory
- Computes agent-level and system-level KPIs
- Identifies bottlenecks (latency spikes, failure clusters)
- Produces a performance summary with improvement actions
- Feeds data into the analytics dashboard

**Key Domain Service**: `MetricsCollector.aggregate()`

---

### REFLECTOR

**Role**: Meta-cognitive analysis and self-correction for strategic alignment.

**Use Case**: `ReflectAndCorrect`

**Responsibilities**:
- Reviews the full cognitive loop output of the current cycle
- Detects drift from the long-term strategic mission
- Produces three concrete correction actions
- Updates `SkillGraph` weights based on execution patterns
- Appends a reflection entry to working memory for the next cycle

**Key Domain Service**: Internally defined reflection logic against `long_term_goal.md`

> **Why REFLECTOR matters**: Without self-reflection, AI systems gradually drift from their original objectives as local optimisations accumulate. REFLECTOR closes the alignment loop.

---

## 5. Three-Tier Memory System

JARVIS maintains memory across three distinct tiers, each optimised for a different access pattern.

### Tier 1 — Episodic Memory (SQLite)

- **What**: Time-ordered execution logs, daily plans, task outcomes
- **Storage**: `SQLiteTaskRepository` → local SQLite database
- **Access pattern**: Append-heavy, date-range queries
- **Retention**: Configurable; defaults to 90 days rolling window
- **Used by**: EXECUTOR (write), AMPLIFIER (read), REFLECTOR (read)

### Tier 2 — Semantic Memory (Vector Search)

- **What**: Knowledge fragments, innovations, embeddings for similarity search
- **Storage**: `SemanticMemory` → pgvector-ready, currently file-backed with embedding stubs
- **Access pattern**: Embedding similarity search (k-NN)
- **Retention**: Indefinite; managed via version tags
- **Used by**: MENTOR (read/write), INNOVATOR (read/write)

### Tier 3 — Strategic Memory (Indexed JSON / Markdown)

- **What**: Long-term goals, Architecture Decision Records (ADRs), roadmaps, milestones
- **Storage**: `memory/strategic/` directory — version controlled in git
- **Access pattern**: Low-frequency reads, human-editable
- **Retention**: Permanent; history via git
- **Used by**: STRATEGIST (read), REFLECTOR (read)

### Memory Validation & Migration

The `MemoryMigrationService` (`packages/jarvis_core/infrastructure/memory/memory_migration.py`) automatically validates all five memory types on startup:

| Memory Type | Auto-fixed fields |
|-------------|------------------|
| Strategic | `priority`, `status`, `progress` bounds |
| Knowledge | `confidence` range, required fields |
| Working | `data` field initialisation |
| Execution Log | `status` values, timestamp formats |
| ADR | `status` values, date parsing |

---

## 6. Clean Architecture

JARVIS uses **Robert C. Martin's Clean Architecture** with four layers. The key invariant is: **dependencies only point inward**.

```
┌─────────────────────────────────────────────────────┐
│  PRESENTATION (FastAPI · Typer CLI · React)          │
│  apps/api/  apps/cli/  apps/web/                    │
├─────────────────────────────────────────────────────┤
│  APPLICATION (Use Cases · DTOs)                     │
│  packages/jarvis_core/application/                  │
├─────────────────────────────────────────────────────┤
│  DOMAIN (Entities · Value Objects · Interfaces)     │
│  packages/jarvis_core/domain/      ← zero deps      │
├─────────────────────────────────────────────────────┤
│  INFRASTRUCTURE (Agents · DB · AI · Monitoring)     │
│  packages/jarvis_core/infrastructure/               │
└─────────────────────────────────────────────────────┘
```

### Domain Layer (`packages/jarvis_core/domain/`)

Pure Python — no imports from infrastructure, no framework imports.

| Component | Examples |
|-----------|---------|
| Entities | `Task`, `Plan`, `Context`, `Innovation`, `Memory`, `Agent` |
| Value Objects | `Priority`, `CognitiveLoad`, `ROI`, `AgentType` |
| Domain Services | `StrategyEngine`, `InnovationEngine`, `MemoryCoordinator`, `AgentOrchestrator` |
| Repository Interfaces | `ITaskRepository`, `IMemoryRepository`, `IAnalyticsRepository` |
| Domain Events | `TaskCompletedEvent`, `GapIdentifiedEvent`, `InnovationCreatedEvent` |

### Application Layer (`packages/jarvis_core/application/`)

Orchestrates domain objects to fulfil use cases. No business logic lives here.

| Use Case | Agent | Description |
|----------|-------|-------------|
| `ExecuteCognitiveLoop` | All | Master orchestrator |
| `GenerateDailyPlan` | STRATEGIST | Builds prioritised daily schedule |
| `IdentifyGaps` | MENTOR | Surfaces knowledge gaps |
| `ExecuteTasks` | EXECUTOR | Runs tasks |
| `CreateInnovations` | INNOVATOR | Generates solutions |
| `AnalyzePerformance` | AMPLIFIER | Computes KPIs |
| `ReflectAndCorrect` | REFLECTOR | Self-correction pass |

### Infrastructure Layer (`packages/jarvis_core/infrastructure/`)

Implements domain interfaces. All external I/O lives here.

| Subsystem | Implementations |
|-----------|----------------|
| Agents | `StrategistAgent`, `MentorAgent`, `ExecutorAgent`, `InnovatorAgent`, `AmplifierAgent`, `ReflectorAgent` |
| Persistence | `FileMemoryRepository`, `SQLiteTaskRepository`, `JSONStorage`, `SemanticMemory` |
| AI Services | `OpenAIService`, `LangChainService` |
| Monitoring | `StructuredLogger`, `Tracer`, `MetricsCollector` |
| Configuration | `Settings` (Pydantic), DI container |

### Bridge Layer (`packages/jarvis_core/bridge/`)

Backwards-compatible adapters for legacy scripts. Allows gradual migration without breaking existing tooling.

---

## 7. API & Interfaces

### REST API (FastAPI)

Base URL: `http://localhost:8000`

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/cognitive-loop` | Run full cognitive loop |
| `GET` | `/api/plan/today` | Retrieve today's plan |
| `GET` | `/api/gaps` | List knowledge gaps |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks` | List tasks |
| `PATCH` | `/api/tasks/{id}` | Update task status |
| `GET` | `/api/analytics` | Performance metrics |
| `GET` | `/api/agents` | List registered agents |
| `POST` | `/api/auth/token` | Obtain JWT access token |
| `POST` | `/api/auth/refresh` | Refresh JWT token |
| `WS` | `/ws/cognitive-loop` | Real-time loop stream |

Auto-generated OpenAPI docs: `http://localhost:8000/docs`

### CLI (Typer + Rich)

```bash
make cli ARGS="loop run"          # Run cognitive loop
make cli ARGS="plan today"        # Show today's plan
make cli ARGS="gaps list"         # Show knowledge gaps
make cli ARGS="tasks create"      # Create a task
make cli ARGS="analytics summary" # Show performance summary
```

### Web Dashboard (React 18 + TypeScript)

URL: `http://localhost:3000`

| Feature | Description |
|---------|-------------|
| Analytics Dashboard | Area, Pie, Bar, and Line charts (Recharts) |
| Task Manager | Create, update, filter tasks |
| Agent Status | Live agent activity view |
| Memory Browser | Inspect working and strategic memory |
| User Preferences | Theme (light/dark/system), font size, compact mode |

---

## 8. Security Model

### Authentication

- **JWT** with access tokens (15-minute expiry) and refresh tokens (7-day expiry)
- Environment-based secret key — no hardcoded secrets
- Role-based access control: `user` / `admin`
- Secure decoding with full error handling

### Rate Limiting

Implemented via Token Bucket algorithm (`apps/api/jarvis_api/middleware/rate_limit.py`):

| Window | Limit |
|--------|-------|
| Per minute | 60 requests |
| Per hour | 1,000 requests |

Client identified by IP address or API key header.

### Security Headers (OWASP)

| Header | Value |
|--------|-------|
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `X-XSS-Protection` | `1; mode=block` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Strict allow-list |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Server` | Removed (no information disclosure) |

### Input Validation

- Pydantic schemas validate all API request bodies
- TypeScript enforces types on the frontend
- SQLAlchemy ORM prevents SQL injection
- HTML output sanitised before rendering

### Security Scanning

CodeQL analysis runs on every CI push. Current status: **0 alerts**.

---

## 9. Observability & Metrics

### Structured Logging

`StructuredLogger` emits JSON-formatted logs with:
- `timestamp`, `level`, `agent`, `use_case`, `duration_ms`, `outcome`
- Correlates logs across a single cognitive loop cycle with a `loop_id`

### Distributed Tracing

`Tracer` (OpenTelemetry-compatible stubs) instruments:
- Each agent execution
- Repository calls
- AI API calls

### Metrics

`MetricsCollector` tracks:

| Metric | Description |
|--------|-------------|
| `agent.task_count` | Tasks processed per agent per cycle |
| `agent.success_rate` | Percentage of tasks completing successfully |
| `api.latency_p50/p95/p99` | API response time percentiles |
| `api.throughput` | Requests per second |
| `memory.size_bytes` | Memory tier sizes |
| `cache.hit_rate` | Cache hit percentage |

Analytics Dashboard auto-refreshes every 30 seconds and supports 24h, 7d, 30d time windows.

---

## 10. Technology Stack

### Backend

| Library | Version | Purpose |
|---------|---------|---------|
| Python | 3.9+ | Core language |
| FastAPI | latest | REST API framework |
| Pydantic | v2 | Settings and schema validation |
| PyJWT | latest | JWT authentication |
| SQLAlchemy | latest | ORM and database abstraction |
| Alembic | latest | Schema migrations |
| asyncio | stdlib | Non-blocking concurrency |
| OpenAI SDK | latest | LLM integration |
| LangChain | latest | Agent tooling and chains |

### Frontend

| Library | Version | Purpose |
|---------|---------|---------|
| React | 18 | UI framework |
| TypeScript | 5.0+ | Type safety |
| Vite | latest | Build tooling |
| Tailwind CSS | latest | Styling |
| Recharts | latest | Analytics charts |
| Radix UI | latest | Accessible components |
| Axios | latest | HTTP client |

### Infrastructure

| Tool | Purpose |
|------|---------|
| Docker / Docker Compose | Containerisation and local orchestration |
| PostgreSQL | Primary relational database |
| Redis | Caching and session storage |
| Nginx | Reverse proxy and TLS termination |
| Kubernetes | Optional production orchestration |
| GitHub Actions | CI/CD pipeline |

---

## 11. Testing Strategy

### Test Pyramid

```
           /\
          /E2E\       (planned — critical user flows)
         /──────\
        / Integr.\   (18 tests — repository, API, agents)
       /────────────\
      /  Unit Tests  \ (169 tests — domain, use cases, services)
     /────────────────\
```

**Total: 187 tests** | **Coverage: 51%** | **Execution time: ~3s**

### Test Categories

| Layer | Location | Approach |
|-------|----------|---------|
| Domain | `tests/unit/domain/` | Pure Python, no mocks |
| Application | `tests/unit/use_cases/` | Mocked repositories |
| Infrastructure | `tests/integration/` | Real file system / SQLite |
| API | `tests/integration/api/` | TestClient with mock agents |
| Memory Migration | `tests/unit/test_memory_migration.py` | All 5 memory types |
| Agent Coordinator | `tests/unit/test_agent_coordinator.py` | Priority ordering, failure isolation |

### Running Tests

```bash
make test             # All tests
make test-unit        # Unit tests only
make test-integration # Integration tests only
make type-check       # mypy static analysis
make lint             # ruff + black + isort
```

---

## 12. Deployment Architecture

### Local Development

```bash
docker-compose up -d postgres redis
make api    # Terminal 1 — FastAPI on :8000
make web    # Terminal 2 — Vite dev server on :3000
```

### Production (Docker Compose)

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Includes health checks, restart policies, and log rotation.

### Production (Kubernetes)

Manifests available in `infrastructure/k8s/`:
- `deployment.yaml` — API and worker pods
- `service.yaml` — ClusterIP and LoadBalancer services
- `ingress.yaml` — Nginx ingress with TLS
- `hpa.yaml` — Horizontal Pod Autoscaler

### Environment Variables

| Variable | Description | Required |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `JWT_SECRET_KEY` | JWT signing secret | Yes |
| `ENVIRONMENT` | `development` / `production` | Yes |
| `LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` | No |

---

## 13. Extension Points

### Adding a New Agent

1. Create domain entity update if needed: `packages/jarvis_core/domain/entities/`
2. Create use case: `packages/jarvis_core/application/use_cases/`
3. Implement agent: `packages/jarvis_core/infrastructure/agents/`
4. Register with `AgentCoordinator` in DI container
5. Wire into `ExecuteCognitiveLoop`

### Swapping the LLM Provider

All AI interactions go through `IAIService`. Implement the interface for any provider:

```python
class MyLLMService(IAIService):
    async def complete(self, prompt: str, **kwargs) -> str:
        ...
```

Inject via DI container — no changes required to agents or use cases.

### Adding a New Memory Type

1. Define schema validation rules in `MemoryMigrationService`
2. Implement repository method if needed
3. Add migration in `memory_migration.py`

### Adding a New API Endpoint

1. Add route in `apps/api/jarvis_api/api/v1/`
2. Add Pydantic schema in `apps/api/jarvis_api/schemas/`
3. Call an existing use case or create a new one

### Third-Party Integrations

Pre-built integration stubs are available in `apps/integrations/`:

| Integration | Location |
|-------------|---------|
| GitHub App | `apps/integrations/github-app/` |
| Slack Bot | `apps/integrations/slack-bot/` |
| VSCode Extension | `apps/integrations/vscode-extension/` |

---

## 14. Design Decisions (ADRs)

Full ADRs are in `memory/strategic/architecture_decision_records/`.

### ADR-001: Clean Architecture

**Decision**: Use Robert C. Martin's Clean Architecture.

**Rationale**: Domain logic must remain testable in isolation, independent of LLM provider, database, and interface. This enables painless provider swaps and confident refactoring.

**Consequence**: Higher initial ceremony (interfaces, DTOs, use cases); pays off at scale.

### ADR-002: Schema Validation

**Decision**: Pydantic v2 for all settings, API schemas, and domain value objects.

**Rationale**: Type safety at the boundary prevents entire classes of runtime errors and makes API contracts self-documenting.

**Consequence**: Requires schema updates when adding fields; Pydantic v2 migration cost was one-time.

### Why No LangGraph / AutoGen?

JARVIS deliberately avoids orchestration frameworks that impose their own abstractions over agents. The `AgentCoordinator` and cognitive loop are hand-written so that:
- Execution order is deterministic and observable
- Failure isolation is explicit, not framework-inferred
- The domain model owns agent behaviour, not a third-party graph library

---

## 15. Known Limitations & Roadmap

### Current Limitations

| Limitation | Impact | Planned Fix |
|-----------|--------|-------------|
| Test coverage at 51% | Risk in refactors | Reach 90% over next quarter |
| Semantic memory is file-backed | Slow similarity search at scale | Migrate to pgvector |
| No E2E test suite | User flows untested in CI | Add Playwright tests |
| Single-tenant architecture | Cannot serve multiple users | Multi-tenancy in roadmap |
| LLM calls not cached | Increased latency and cost | Semantic cache with Redis |

### Short-Term Roadmap (1–3 months)

- [ ] Increase test coverage to 70%
- [ ] E2E tests for critical cognitive loop flows
- [ ] WebSocket real-time updates (UI ↔ live loop events)
- [ ] Performance benchmarking suite

### Medium-Term Roadmap (3–6 months)

- [ ] 90% test coverage
- [ ] pgvector semantic memory backend
- [ ] Multi-language support
- [ ] A/B testing framework for agent prompt variations

### Long-Term Roadmap (6–12 months)

- [ ] Multi-tenancy with SSO
- [ ] Fine-tuned domain model (not just prompt engineering)
- [ ] Mobile applications
- [ ] Enterprise audit logging and compliance exports
- [ ] Distributed tracing with OpenTelemetry backend

---

*Last updated: April 2026 | Version: 1.0 | Audience: Developers, contributors, serious users*
