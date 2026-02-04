# Jarvis - AI-Powered Cognitive Assistant

## Overview

Jarvis is an advanced AI-powered cognitive assistant that leverages a multi-agent architecture to help users with strategic planning, task execution, innovation, and performance optimization. The system implements **Clean Architecture** principles with a cognitive loop that coordinates multiple specialized agents to provide intelligent assistance.

## 🎯 Clean Architecture

The system follows Clean Architecture principles with four distinct layers:

### Layer 1: Domain Layer (`src/domain/`)
**Pure business logic with zero external dependencies**
- Entities: Task, Plan, Context, Innovation, Memory, Agent
- Value Objects: Priority, CognitiveLoad, ROI, AgentType
- Domain Services: StrategyEngine, InnovationEngine, MemoryCoordinator
- Repository Interfaces: ITaskRepository, IMemoryRepository, IAnalyticsRepository
- Domain Events: TaskCompletedEvent, GapIdentifiedEvent, InnovationCreatedEvent

### Layer 2: Application Layer (`src/application/`)
**Use cases and application business rules**
- Use Cases: ExecuteCognitiveLoop, GenerateDailyPlan, ExecuteTasks, IdentifyGaps, CreateInnovations, AnalyzePerformance
- DTOs: TaskDTO, PlanDTO, AnalyticsDTO
- Application Interfaces: IAIService, INotificationService

### Layer 3: Infrastructure Layer (`src/infrastructure/`)
**Implementation details and external dependencies**
- Agents: StrategistAgent, MentorAgent, ExecutorAgent, InnovatorAgent, AmplifierAgent
- Persistence: FileMemoryRepository, SQLiteTaskRepository, JSONStorage
- AI Services: OpenAIService, LangChainService
- Monitoring: StructuredLogger, Tracer, MetricsCollector
- Configuration: Settings (Pydantic), Dependencies (DI Container)

### Layer 4: Presentation Layer (`src/presentation/`)
**User interfaces (API, CLI)**
- REST API (FastAPI): `/api/cognitive-loop`, `/api/plan/today`, `/api/gaps`, etc.
- CLI (Typer + Rich): Interactive command-line interface
- WebSocket: Real-time updates (planned)

### Bridge Layer (`src/bridge/`)
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
├── agents/              # Agent implementations
│   ├── strategist.py
│   ├── mentor.py
│   ├── executor.py
│   ├── innovator.py
│   └── amplifier.py
├── core/                # Core system components
│   ├── cognitive_loop.py
│   └── memory_manager.py
├── memory/              # Memory and knowledge storage
│   ├── working/         # Working memory for active tasks
│   │   ├── daily_context.json
│   │   ├── gaps.json
│   │   └── reflections.json
│   ├── knowledge/       # Long-term knowledge base
│   │   └── learning_roadmap.md
│   ├── innovator/       # Innovation tracking
│   ├── amplifier/       # Performance metrics
│   └── strategic/       # Strategic planning
├── tools/               # Analysis and automation tools
│   └── analyze_logs.py
├── scripts/             # Utility scripts
├── generate_quarterly_review.py  # Quarterly review automation
└── requirements.txt     # Python dependencies
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Running the Project

### Using the CLI (Recommended)

The new CLI provides a user-friendly interface with rich formatting:

```bash
# Display help
python src/presentation/cli/main.py --help

# Run complete cognitive loop
python src/presentation/cli/main.py run

# Generate today's plan
python src/presentation/cli/main.py plan

# Identify knowledge gaps
python src/presentation/cli/main.py gaps

# Generate innovations
python src/presentation/cli/main.py innovate

# View performance metrics
python src/presentation/cli/main.py performance

# Show version info
python src/presentation/cli/main.py version
```

### Using the Legacy Script

For backward compatibility, the original script still works:

```bash
python scripts/test_cognitive_loop.py
```

### Using the REST API

Start the FastAPI server:

```bash
# Start the server
python src/presentation/api/main.py

# Or use uvicorn directly
uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000
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

#### Log Analysis
Analyze your progress and identify patterns:

```bash
python tools/analyze_logs.py
```

This generates insights on:
- Frequently encountered gaps
- Most common lessons learned
- Task execution trends
- Productivity patterns
- Challenge analysis

#### Quarterly Reviews
Generate automated quarterly reviews:

```bash
# Generate review for current quarter
python generate_quarterly_review.py

# Generate review for specific quarter
python generate_quarterly_review.py --quarter Q1

# Save to custom file
python generate_quarterly_review.py --quarter Q2 --output my_review.json
```

Quarterly reviews include:
- Tasks summary
- Lessons learned
- Unresolved gaps
- Next quarter recommendations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add license information here]

## Contact

For questions or support, please open an issue on GitHub.
