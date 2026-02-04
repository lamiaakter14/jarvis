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
│   ├── knowledge/       # Long-term knowledge base
│   ├── innovator/       # Innovation tracking
│   └── amplifier/       # Performance metrics
├── scripts/             # Utility scripts
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add license information here]

## Contact

For questions or support, please open an issue on GitHub.
