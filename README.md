# Jarvis - AI-Powered Cognitive Assistant

## Overview

Jarvis is an advanced AI-powered cognitive assistant that leverages a multi-agent architecture to help users with strategic planning, task execution, innovation, and performance optimization. The system implements a cognitive loop that coordinates multiple specialized agents to provide intelligent assistance.

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

### Run the Cognitive Loop

```bash
python scripts/test_cognitive_loop.py
```

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
