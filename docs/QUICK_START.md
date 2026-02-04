# JARVIS Clean Architecture - Quick Start Guide

## 🚀 Getting Started

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys (OpenAI, etc.)
```

## 🎯 Usage Options

### Option 1: CLI (Recommended for Interactive Use)

```bash
# Run complete cognitive loop
python -m src.presentation.cli.main run

# Generate today's plan
python -m src.presentation.cli.main plan

# Identify knowledge gaps
python -m src.presentation.cli.main gaps

# Generate innovations
python -m src.presentation.cli.main innovate

# View performance metrics
python -m src.presentation.cli.main performance

# Show help
python -m src.presentation.cli.main --help
```

### Option 2: REST API (Recommended for Integration)

```bash
# Start the API server
python -m src.presentation.api.main

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

**API Endpoints:**
- `GET /health` - Health check
- `POST /api/cognitive-loop` - Run complete cognitive loop
- `GET /api/plan/today` - Get today's plan
- `GET /api/gaps` - Get knowledge gaps
- `GET /api/innovations` - Get innovations
- `GET /api/performance` - Get performance metrics

**Example API Usage:**
```bash
# Health check
curl http://localhost:8000/health

# Run cognitive loop
curl -X POST http://localhost:8000/api/cognitive-loop

# Get today's plan
curl http://localhost:8000/api/plan/today
```

### Option 3: Docker

```bash
# Start API server
docker-compose up jarvis-api

# Run CLI (one-time)
docker-compose run --rm jarvis-cli

# Access API at http://localhost:8000
```

## 🏗️ Architecture Overview

The system follows **Clean Architecture** with 4 layers:

1. **Domain Layer** (`src/domain/`)
   - Pure business logic
   - Entities: Task, Plan, Innovation, Context, Memory
   - Value Objects: Priority, ROI, CognitiveLoad, AgentType
   - Domain Services: StrategyEngine, InnovationEngine
   - Zero external dependencies

2. **Application Layer** (`src/application/`)
   - Use cases: ExecuteCognitiveLoop, GenerateDailyPlan, etc.
   - DTOs: TaskDTO, PlanDTO, AnalyticsDTO
   - Application interfaces: IAIService, INotificationService
   - Orchestrates domain objects

3. **Infrastructure Layer** (`src/infrastructure/`)
   - Agent implementations (5 agents)
   - Repository implementations (File, SQLite)
   - External service adapters (OpenAI, LangChain)
   - Monitoring and configuration

4. **Presentation Layer** (`src/presentation/`)
   - REST API (FastAPI)
   - CLI (Typer + Rich)
   - Multiple interfaces for the same business logic

## 🤖 The 5 Agents

1. **Strategist** - Plans and organizes tasks
2. **Mentor** - Identifies knowledge gaps and provides feedback
3. **Executor** - Executes tasks
4. **Innovator** - Generates creative solutions
5. **Amplifier** - Analyzes and optimizes performance

## 📊 Example Workflow

```python
# The cognitive loop executes all 5 agents in sequence:

1. Strategist generates daily plan
   → Returns prioritized tasks with ROI calculations

2. Mentor analyzes execution logs
   → Identifies knowledge gaps
   → Provides feedback on tasks

3. Executor runs high-priority tasks
   → Marks tasks in progress
   → Completes tasks
   → Tracks results

4. Innovator generates innovations
   → AI-powered idea generation
   → Pattern analysis from tasks
   → Ranks by impact score

5. Amplifier analyzes performance
   → Calculates productivity score
   → Identifies optimization opportunities
   → Generates actionable recommendations
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test types
pytest -m unit        # Unit tests only
pytest -m integration # Integration tests only
pytest -m e2e         # End-to-end tests only

# View coverage report
open htmlcov/index.html
```

## 🔧 Development

### Adding a New Agent

1. **Domain**: Create agent interface in `src/domain/entities/agent.py`
2. **Application**: Create use case in `src/application/use_cases/`
3. **Infrastructure**: Implement agent in `src/infrastructure/agents/`
4. **Presentation**: Add API endpoint and CLI command

### Adding a New Use Case

1. Define interface dependencies (repositories, services)
2. Implement `execute()` method
3. Use domain services for business logic
4. Emit domain events as needed
5. Return DTOs

### Project Structure

```
jarvis/
├── src/
│   ├── domain/          # Core business logic
│   ├── application/     # Use cases
│   ├── infrastructure/  # Implementation details
│   │   ├── agents/      # Agent implementations
│   │   ├── persistence/ # Data storage
│   │   └── ai/          # AI service integrations
│   ├── presentation/    # User interfaces
│   │   ├── api/         # REST API
│   │   └── cli/         # Command-line interface
│   ├── bridge/          # Backward compatibility
│   └── shared/          # Common utilities
├── tests/
│   ├── unit/            # Fast, isolated tests
│   ├── integration/     # Component integration tests
│   ├── e2e/             # End-to-end tests
│   └── fixtures/        # Test fixtures
├── memory/              # Persistent storage
│   ├── working/         # Active tasks, context
│   ├── knowledge/       # Long-term knowledge
│   └── strategic/       # Strategic planning
└── docs/                # Documentation
```

## 📚 Additional Documentation

- [Clean Architecture Overview](architecture/clean-architecture-overview.md)
- [Implementation Complete](IMPLEMENTATION_COMPLETE.md)

## 🐛 Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH=/path/to/jarvis:$PYTHONPATH
```

**Issue: Database locked**
```bash
# Solution: Close other connections or delete lock file
rm memory/tasks.db-journal
```

**Issue: OpenAI API errors**
```bash
# Solution: Check your API key in .env
# Ensure OPENAI_API_KEY is set correctly
```

## 🤝 Contributing

1. Follow Clean Architecture principles
2. Write tests for new features (maintain 80%+ coverage)
3. Use type hints for all functions
4. Add docstrings
5. Run linters: `flake8`, `black`, `mypy`

## 📝 License

[Add your license here]

## 🙏 Credits

Built with Clean Architecture principles following:
- Robert C. Martin's Clean Architecture
- Domain-Driven Design (DDD)
- SOLID principles
- Dependency Inversion Principle

## 🔗 Links

- [GitHub Repository](https://github.com/lamiaakter14/jarvis)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Issue Tracker](https://github.com/lamiaakter14/jarvis/issues)
