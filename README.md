# Jarvis - AI-Powered Cognitive Assistant

> Enterprise-grade AI cognitive assistant with Clean Architecture

## 🚀 Quick Start (Local Development)

### One-Command Setup

```bash
# Clone and setup everything
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis
./scripts/setup/quick_start.sh
```

### Manual Setup

```bash
# 1. Install dependencies
make install

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start infrastructure
docker-compose up -d postgres redis

# 4. Run migrations
make db-migrate

# 5. Start applications
make api     # Terminal 1: API server
make web     # Terminal 2: Web dashboard
```

### Access Points

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Web Dashboard**: http://localhost:3000
- **CLI**: `make cli ARGS="--help"`

## 📋 Available Commands

```bash
make help              # Show all commands
make install           # Install dependencies
make dev               # Start development environment
make api               # Start API server
make web               # Start web dashboard
make cli               # Run CLI (use ARGS="command")
make test              # Run tests
make lint              # Run linters
make format            # Format code
make docker-up         # Start Docker services
make health            # Check service health
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test types
make test-unit
make test-integration
make test-e2e

# Check code quality
make lint
make type-check
```

## 📚 Documentation

### Getting Started
- [Quick Start](docs/QUICK_START.md) - Get up and running in minutes
- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [Local Testing Guide](docs/LOCAL_TESTING.md) - Test locally before deployment

### Usage & Operations
- [Usage Guide](docs/USAGE_GUIDE.md) - How to use JARVIS features
- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Solutions to common issues

### Deployment & Monitoring
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment instructions
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md) - Pre/post deployment checklist
- [Monitoring Guide](docs/MONITORING_GUIDE.md) - Set up monitoring and alerts
- [UAT Guide](docs/UAT_GUIDE.md) - User acceptance testing procedures

### Operations & Maintenance
- [Handover Document](docs/HANDOVER.md) - Complete operations guide
- [Future Enhancements](docs/FUTURE_ENHANCEMENTS.md) - Roadmap and recommendations

### Architecture
- [Architecture Overview](docs/architecture/clean-architecture-overview.md) - System design
- [Project Summary](docs/PROJECT_SUMMARY.md) - Complete project overview
- [Comprehensive Repository Report](COMPREHENSIVE_REPOSITORY_REPORT.md) - Full developer handoff & snapshot
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

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
├── docs/                          # Documentation
└── scripts/                       # Setup and deployment scripts
```

### Memory vs Runtime

- **memory/** - Curated knowledge committed to git (roadmaps, strategic docs, templates)
- **runtime/** - Generated state unique to each instance (daily plans, logs, cache)

See [docs/architecture/project-structure.md](docs/architecture/) for detailed structure information.

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
