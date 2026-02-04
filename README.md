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

## Project Structure

```
jarvis/
├── src/                 # Clean Architecture implementation
│   ├── domain/          # Business logic and entities
│   ├── application/     # Use cases and DTOs
│   ├── infrastructure/  # External implementations
│   │   ├── agents/      # Agent implementations
│   │   ├── persistence/ # Data storage
│   │   └── ai/          # AI service integrations
│   ├── presentation/    # User interfaces
│   │   ├── api/         # REST API (FastAPI)
│   │   └── cli/         # Command-line interface
│   └── bridge/          # Backward compatibility layer
├── frontend/            # React web dashboard
│   ├── src/             # Frontend source code
│   │   ├── api/         # API client
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── contexts/    # React contexts
│   │   └── utils/       # Utilities
│   ├── public/          # Static assets
│   └── package.json     # Node.js dependencies
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── memory/              # Memory and knowledge storage
│   ├── working/         # Working memory for active tasks
│   ├── knowledge/       # Long-term knowledge base
│   ├── innovator/       # Innovation tracking
│   ├── amplifier/       # Performance metrics
│   └── strategic/       # Strategic planning
├── docs/                # Documentation
├── .github/             # GitHub workflows and configurations
├── Dockerfile           # Docker containerization
├── docker-compose.yml   # Docker orchestration
└── requirements.txt     # Python dependencies
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for web dashboard)
- pip package manager

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lamiaakter14/jarvis.git
   cd jarvis
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (OpenAI API key, etc.)
   ```

6. **Create runtime directory (optional - auto-created):**
   ```bash
   mkdir -p runtime/{working/execution_logs,metrics,innovations,cache}
   ```

## Running the Project

### Using the Web Dashboard (Recommended) 🎨

The web dashboard provides a modern, visual interface to interact with JARVIS:

**1. Start the Backend API:**
```bash
# Option 1: Using Python module
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli
python -m jarvis_api.main

# Option 2: Using uvicorn directly  
cd apps/api
uvicorn jarvis_api.main:app --reload --host 0.0.0.0 --port 8000
# Backend runs at http://localhost:8000
```

**2. Start the Frontend (in a new terminal):**
```bash
cd apps/web
npm install  # First time only
npm run dev
# Frontend runs at http://localhost:3000
```

**3. Open your browser:**
Visit http://localhost:3000 to access the dashboard.

**Features:**
- 📊 Dashboard with stats and system status
- 🧠 Run cognitive loop with real-time agent status
- 📅 View and generate daily plans
- ✅ Manage tasks
- 🎯 Track knowledge gaps
- 💡 Browse innovations
- 📈 Performance analytics with charts
- 🌙 Dark mode support
- 📱 Fully responsive design

See `apps/web/README.md` for detailed frontend documentation.

### Using the CLI

The CLI provides a user-friendly interface with rich formatting:

```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/jarvis/packages:/path/to/jarvis/apps/api:/path/to/jarvis/apps/cli

# Display help
python -m jarvis_cli.main --help

# Run complete cognitive loop
python -m jarvis_cli.main run

# Generate today's plan
python -m jarvis_cli.main plan

# Identify knowledge gaps
python -m jarvis_cli.main gaps

# Generate innovations
python -m jarvis_cli.main innovate

# View performance metrics
python -m jarvis_cli.main performance

# Show version info
python -m jarvis_cli.main version
```

### Using the REST API

Start the FastAPI server:

```bash
# Start the server
python -m jarvis_api.main

# Or use uvicorn directly
uvicorn jarvis_api.main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/cognitive-loop` - Run complete cognitive loop
- `GET /api/plan/today` - Get today's plan
- `GET /api/gaps` - Get knowledge gaps
- `GET /api/innovations` - Get innovations
- `GET /api/performance` - Get performance metrics

API documentation (Swagger): http://localhost:8000/docs

### Using Docker (Optional)

```bash
docker-compose up
```

## Configuration

Configure the system by editing the `.env` file with your specific settings, including API keys and other credentials.

## Memory System

The Jarvis memory system maintains:

- **Working Memory**: Active tasks and daily context
- **Knowledge Base**: Long-term learning, roadmaps, and reflections
- **Agent-Specific Memory**: Innovations and performance metrics

## 📅 Roadmap and Progress Tracking

JARVIS includes a comprehensive 2-year daily actionable roadmap and supporting tools for tracking progress:

### Learning Roadmap

The detailed roadmap is available at `memory/knowledge/learning_roadmap.md` and includes:
- Day-by-day tasks for 2 years (730 days)
- Quarterly milestones and objectives
- Daily routine templates
- Success metrics and tracking

### Daily Task Tracking

Track your progress using the JSON templates in `memory/working/`:
- **`daily_context.json`**: Current tasks and priorities
- **`gaps.json`**: Knowledge gaps (unresolved and resolved)
- **`reflections.json`**: Daily reflections, lessons learned, and productivity metrics

### Analysis Tools

#### Performance Analysis
Analyze your progress and identify patterns using the CLI:

```bash
python -m jarvis_cli.main performance
```

This provides insights on:
- Productivity score
- Task completion rates
- Optimization suggestions
- Performance trends

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add license information here]

## Contact

For questions or support, please open an issue on GitHub.
