# Jarvis - AI-Powered Cognitive Assistant

## Overview

Jarvis is an advanced AI-powered cognitive assistant that leverages a multi-agent architecture to help users with strategic planning, task execution, innovation, and performance optimization. The system implements **Clean Architecture** principles with a cognitive loop that coordinates multiple specialized agents to provide intelligent assistance.

## 🏗️ Project Structure (Monorepo)

JARVIS follows a modern monorepo architecture for better maintainability and scalability:

```
jarvis/
├── apps/                          # Applications (entry points)
│   ├── api/jarvis_api/           # FastAPI REST API
│   ├── cli/jarvis_cli/           # Typer CLI application
│   └── web/                       # React frontend
│
├── packages/jarvis_core/          # Core business logic
│   ├── domain/                    # Domain Layer (entities, value objects)
│   ├── application/               # Application Layer (use cases, DTOs)
│   ├── infrastructure/            # Infrastructure Layer (agents, AI, persistence)
│   ├── bridge/                    # Legacy bridge adapters
│   └── shared/                    # Shared utilities
│
├── memory/                        # ✅ Curated knowledge (version controlled)
├── runtime/                       # ❌ Generated state (gitignored)
├── tests/                         # Test suite
└── docs/                          # Documentation
```

### Memory vs Runtime

- **memory/** - Curated knowledge committed to git (roadmaps, strategic docs, templates)
- **runtime/** - Generated state unique to each instance (daily plans, logs, cache)

## 🎯 Clean Architecture

The system follows Clean Architecture principles with four distinct layers:

### Layer 1: Domain Layer (`packages/jarvis_core/domain/`)
**Pure business logic with zero external dependencies**
- Entities: Task, Plan, Context, Innovation, Memory, Agent
- Value Objects: Priority, CognitiveLoad, ROI, AgentType
- Domain Services: StrategyEngine, InnovationEngine, MemoryCoordinator
- Repository Interfaces: ITaskRepository, IMemoryRepository, IAnalyticsRepository
- Domain Events: TaskCompletedEvent, GapIdentifiedEvent, InnovationCreatedEvent

### Layer 2: Application Layer (`packages/jarvis_core/application/`)
**Use cases and application business rules**
- Use Cases: ExecuteCognitiveLoop, GenerateDailyPlan, ExecuteTasks, IdentifyGaps, CreateInnovations, AnalyzePerformance
- DTOs: TaskDTO, PlanDTO, AnalyticsDTO
- Application Interfaces: IAIService, INotificationService

### Layer 3: Infrastructure Layer (`packages/jarvis_core/infrastructure/`)
**Implementation details and external dependencies**
- Agents: StrategistAgent, MentorAgent, ExecutorAgent, InnovatorAgent, AmplifierAgent
- Persistence: FileMemoryRepository, SQLiteTaskRepository, JSONStorage
- AI Services: OpenAIService, LangChainService
- Monitoring: StructuredLogger, Tracer, MetricsCollector
- Configuration: Settings (Pydantic), Dependencies (DI Container)

### Layer 4: Presentation Layer (`apps/`)
**User interfaces (API, CLI, Web)**
- REST API (FastAPI): `/api/cognitive-loop`, `/api/plan/today`, `/api/gaps`, etc.
- CLI (Typer + Rich): Interactive command-line interface
- Web Dashboard (React): Modern web interface

### Bridge Layer (`packages/jarvis_core/bridge/`)
**Backward compatibility with legacy code**
- Provides adapters for old scripts to work with new architecture
- Enables gradual migration without breaking existing functionality

## Key Agents

The Jarvis system consists of five specialized agents:

1. **STRATEGIST** - Plans and organizes tasks, breaks down complex problems into manageable steps
2. **MENTOR** - Provides guidance, feedback, and helps identify knowledge gaps
3. **EXECUTOR** - Executes tasks and manages the implementation process
4. **INNOVATOR** - Generates creative solutions and innovative approaches to problems
5. **AMPLIFIER** - Analyzes performance metrics and optimizes system effectiveness

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lamiaakter14/jarvis.git
   cd jarvis
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running Applications

#### API
```bash
python -m jarvis_api.main
# Or: uvicorn jarvis_api.main:app --reload
# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

#### CLI
```bash
python -m jarvis_cli.main --help
python -m jarvis_cli.main run-loop
python -m jarvis_cli.main generate-plan
```

#### Web Dashboard
```bash
cd apps/web
npm install
npm run dev
# Access: http://localhost:3000
```

#### Docker
```bash
docker-compose up --build
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.md)
- [Architecture Overview](docs/architecture/clean-architecture-overview.md)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Implementation Details](docs/IMPLEMENTATION_COMPLETE.md)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jarvis_core --cov-report=html

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## 📦 Project Structure Details

### Apps vs Packages

- **apps/**: Application entry points that users interact with
  - Can be deployed independently
  - Import from `jarvis_core`
  
- **packages/**: Shared business logic
  - Reusable across all apps
  - Contains Clean Architecture layers

### Memory vs Runtime

- **memory/**: Curated knowledge (committed to git)
  - Templates, roadmaps, strategies
  - Documentation and plans
  - Version controlled
  
- **runtime/**: Generated state (gitignored)
  - Daily context and plans
  - Logs and metrics
  - Cache and temporary files
  - Unique per instance

## 🔧 Development

### Adding a New App

1. Create directory: `apps/my_app/`
2. Add entry point: `apps/my_app/main.py`
3. Import from: `jarvis_core.*`

### Adding a Feature

1. Add domain entity: `packages/jarvis_core/domain/entities/`
2. Add use case: `packages/jarvis_core/application/use_cases/`
3. Add infrastructure: `packages/jarvis_core/infrastructure/`
4. Expose via app: `apps/api/` or `apps/cli/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## 📄 License

MIT License

## 📧 Contact

For questions or support, please open an issue on GitHub.
