# JARVIS Installation Guide

## Overview

This guide provides step-by-step instructions for installing JARVIS AI-Powered Cognitive Assistant on various platforms. Choose the installation method that best suits your needs.

**Estimated Time**: 15-30 minutes  
**Skill Level**: Beginner to Intermediate  

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Installation](#quick-installation)
3. [Manual Installation](#manual-installation)
4. [Docker Installation](#docker-installation)
5. [Development Setup](#development-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

**Minimum**:
- CPU: 2 cores
- RAM: 4GB
- Disk: 10GB free space
- OS: Linux, macOS, or Windows 10+

**Recommended**:
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 20GB+ SSD
- OS: Ubuntu 22.04+ or macOS 12+

### Required Software

- **Python 3.9-3.11** (3.11 recommended)
- **Node.js 18+** (for frontend)
- **PostgreSQL 13+** (or use Docker)
- **Redis 6+** (or use Docker)
- **Git**

### Optional Software

- **Docker** and **Docker Compose** (for containerized setup)
- **Make** (for using Makefile commands)

### API Keys

You'll need an OpenAI API key. Get one at: https://platform.openai.com/api-keys

---

## Quick Installation

### One-Command Setup (Linux/macOS)

```bash
# Clone and run setup script
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis
./scripts/setup/quick_start.sh
```

This script will:
1. Install all dependencies
2. Set up virtual environment
3. Create .env file
4. Start infrastructure services
5. Run database migrations
6. Build frontend

**After installation**:
```bash
make api   # Terminal 1: Start API (http://localhost:8000)
make web   # Terminal 2: Start web dashboard (http://localhost:3000)
```

---

## Manual Installation

### Step 1: Install System Dependencies

**Ubuntu/Debian**:
```bash
# Update package list
sudo apt update

# Install Python, Node.js, PostgreSQL, Redis
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib redis-server \
    nodejs npm git curl

# Verify installations
python3.11 --version  # Should be 3.11.x
node --version        # Should be 18.x or higher
```

**macOS** (using Homebrew):
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.11 node postgresql redis git

# Start services
brew services start postgresql
brew services start redis

# Verify installations
python3.11 --version
node --version
```

**Windows**:
```powershell
# Install using Chocolatey (run PowerShell as Administrator)
choco install python311 nodejs.install postgresql redis git

# Or download installers from:
# - Python: https://www.python.org/downloads/
# - Node.js: https://nodejs.org/
# - PostgreSQL: https://www.postgresql.org/download/windows/
# - Redis: https://github.com/microsoftarchive/redis/releases
```

### Step 2: Clone Repository

```bash
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -e ".[dev]"
```

### Step 4: Set Up Database

**PostgreSQL**:
```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE USER jarvis WITH PASSWORD 'your_secure_password';
CREATE DATABASE jarvis_dev OWNER jarvis;
GRANT ALL PRIVILEGES ON DATABASE jarvis_dev TO jarvis;
\q
EOF

# Verify connection
psql -U jarvis -d jarvis_dev -c "SELECT version();"
```

**Redis**:
```bash
# Start Redis (if not already running)
# Linux:
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS:
brew services start redis

# Verify
redis-cli ping  # Should return "PONG"
```

### Step 5: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Required .env variables**:
```bash
# Core Settings
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-this

# Database
DATABASE_URL=postgresql://jarvis:your_secure_password@localhost:5432/jarvis_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# OpenAI API
OPENAI_API_KEY=your-openai-api-key-here

# JWT Authentication
JWT_SECRET_KEY=your-jwt-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Generate secure keys**:
```python
# Run in Python to generate secure keys
import secrets
print("SECRET_KEY:", secrets.token_urlsafe(32))
print("JWT_SECRET_KEY:", secrets.token_urlsafe(32))
```

### Step 6: Create Runtime Directories

```bash
# Create necessary directories
mkdir -p runtime/{working,metrics,innovations,logs,state}
mkdir -p runtime/working/execution_logs
```

### Step 7: Run Database Migrations

```bash
# Navigate to API directory
cd apps/api

# Run migrations
alembic upgrade head

# Verify migrations
alembic current

# Return to root
cd ../..
```

### Step 8: Install Frontend Dependencies

```bash
# Navigate to frontend
cd apps/web

# Install dependencies
npm install

# Return to root
cd ../..
```

### Step 9: Build Frontend

```bash
cd apps/web
npm run build
cd ../..
```

---

## Docker Installation

### Step 1: Install Docker

**Linux**:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**macOS/Windows**:
- Download and install Docker Desktop from https://www.docker.com/products/docker-desktop

### Step 2: Clone and Configure

```bash
# Clone repository
git clone https://github.com/lamiaakter14/jarvis.git
cd jarvis

# Create .env file
cp .env.example .env

# Edit .env (set OPENAI_API_KEY and other variables)
nano .env
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access Points**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Web Dashboard: http://localhost:3000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## Development Setup

### Additional Development Tools

```bash
# Install pre-commit hooks (for code quality)
pip install pre-commit
pre-commit install

# Install testing tools
pip install pytest pytest-cov pytest-asyncio

# Install linting tools
pip install ruff black isort mypy
```

### Configure IDE

**VS Code** (recommended):
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

**PyCharm**:
1. Open project
2. File → Settings → Project → Python Interpreter
3. Add interpreter → Existing → Select `venv/bin/python`
4. Enable pytest: Settings → Tools → Python Integrated Tools → Testing → pytest

### Run Tests

```bash
# Run all tests
make test

# Run specific test types
make test-unit          # Unit tests only
make test-integration   # Integration tests only

# Run with coverage
pytest tests/ -v --cov=packages/jarvis_core --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Verification

### Verify Installation

Run these commands to verify your installation:

```bash
# 1. Check Python dependencies
pip list | grep -E "(fastapi|pydantic|sqlalchemy)"

# 2. Check database connection
python -c "import psycopg2; print('PostgreSQL OK')"

# 3. Check Redis connection
python -c "import redis; r = redis.Redis(); r.ping(); print('Redis OK')"

# 4. Start API server
cd apps/api
uvicorn jarvis_api.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
sleep 5

# 5. Test API health
curl http://localhost:8000/api/v1/health

# 6. Check API docs
echo "Open http://localhost:8000/docs in your browser"

# 7. Stop API
kill $API_PID

# 8. Start frontend
cd ../web
npm run dev &
WEB_PID=$!
sleep 5

# 9. Test frontend
echo "Open http://localhost:3000 in your browser"

# 10. Stop frontend
kill $WEB_PID
```

### Expected Outputs

**Health Check**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-15T21:00:00Z"
}
```

**API Docs**: Should show Swagger UI with all endpoints

**Frontend**: Should load the dashboard

---

## Troubleshooting

### Common Issues

#### Issue: Python version mismatch

**Error**: `python: command not found` or wrong version

**Solution**:
```bash
# Use python3.11 explicitly
python3.11 -m venv venv
source venv/bin/activate
python --version  # Verify it's 3.11.x
```

#### Issue: PostgreSQL connection refused

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS

# Start if not running
sudo systemctl start postgresql  # Linux
brew services start postgresql  # macOS

# Check port
sudo netstat -tulpn | grep 5432
```

#### Issue: Redis connection refused

**Error**: `Error connecting to Redis`

**Solution**:
```bash
# Check if Redis is running
redis-cli ping  # Should return PONG

# Start if not running
sudo systemctl start redis-server  # Linux
brew services start redis  # macOS
```

#### Issue: Port already in use

**Error**: `OSError: [Errno 98] Address already in use`

**Solution**:
```bash
# Find process using port 8000
sudo lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # Linux/macOS
taskkill /PID <PID> /F  # Windows

# Or use different port
uvicorn jarvis_api.main:app --port 8001
```

#### Issue: Module not found

**Error**: `ModuleNotFoundError: No module named 'jarvis_core'`

**Solution**:
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Install in editable mode
pip install -e .

# Verify installation
pip list | grep jarvis
```

#### Issue: Database migration failed

**Error**: `alembic.util.exc.CommandError`

**Solution**:
```bash
# Check database connection
psql -U jarvis -d jarvis_dev -c "SELECT 1;"

# Reset migrations (WARNING: destroys data)
cd apps/api
alembic downgrade base
alembic upgrade head

# Or create fresh database
dropdb jarvis_dev -U postgres
createdb jarvis_dev -U postgres -O jarvis
alembic upgrade head
```

#### Issue: Frontend build failed

**Error**: `npm ERR!` or build failures

**Solution**:
```bash
cd apps/web

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Try building again
npm run build
```

#### Issue: Permission denied

**Error**: `Permission denied` when running scripts

**Solution**:
```bash
# Make scripts executable
chmod +x scripts/**/*.sh

# Or run with bash
bash scripts/setup/quick_start.sh
```

---

## Post-Installation

### Next Steps

1. **Read the documentation**:
   - [Quick Start Guide](QUICK_START.md)
   - [Usage Guide](USAGE_GUIDE.md)
   - [API Documentation](API_DOCUMENTATION.md)

2. **Configure the system**:
   - Set up user preferences
   - Configure agents
   - Import sample data

## Advanced Configuration

### REFLECTOR Agent Setup

The REFLECTOR agent (introduced in JARVIS V1) analyzes execution patterns and provides self-correction recommendations. It requires:

1. **Historical execution data**: The agent needs at least 1 day of task execution history to provide meaningful insights.

2. **Memory repository access**: Ensure the memory repository is properly configured:
   ```bash
   # Memory directories are created during installation
   # Verify they exist:
   ls -la memory/
   # Should show: strategic/, knowledge/, working_template.json, etc.
   ```

3. **Enable REFLECTOR in configuration** (`.env`):
   ```bash
   # REFLECTOR Agent Configuration
   REFLECTOR_ENABLED=true
   REFLECTOR_ANALYSIS_SCHEDULE="0 6 * * *"  # Run at 6 AM daily
   REFLECTOR_MIN_TASKS_FOR_ANALYSIS=3  # Minimum tasks needed for analysis
   ```

4. **Verify REFLECTOR agent**:
   ```bash
   # Test REFLECTOR endpoint
   curl -X POST http://localhost:8000/api/agents/reflector/analyze \
     -H "Content-Type: application/json" \
     -d '{"date": "2024-01-01"}'
   ```

### Semantic Search & ML/NLU Services

JARVIS V1 includes semantic memory for vector-based knowledge retrieval:

1. **PostgreSQL with pgvector** (Production-ready):
   ```bash
   # Install pgvector extension
   psql -U postgres -d jarvis_dev
   CREATE EXTENSION IF NOT EXISTS vector;
   \q
   ```

2. **Configure semantic search** (`.env`):
   ```bash
   # Semantic Search Configuration
   SEMANTIC_SEARCH_ENABLED=true
   EMBEDDING_MODEL=text-embedding-ada-002  # OpenAI model
   EMBEDDING_DIMENSION=1536
   VECTOR_SIMILARITY_THRESHOLD=0.7
   ```

3. **Initialize semantic memory**:
   ```bash
   # Run initialization script
   python -m jarvis_core.memory.semantic init
   
   # Verify setup
   python -m jarvis_core.memory.semantic status
   ```

### Integration Services (Optional)

#### GitHub App Integration

1. **Create GitHub App**: Go to GitHub Settings > Developer settings > GitHub Apps
2. **Configure webhook URL**: `https://your-domain.com/api/integrations/github/webhook`
3. **Set permissions**: Repository contents (read), Issues (read/write), Pull requests (read/write)
4. **Add to `.env`**:
   ```bash
   GITHUB_APP_ID=your_app_id
   GITHUB_PRIVATE_KEY_PATH=/path/to/private-key.pem
   GITHUB_WEBHOOK_SECRET=your_webhook_secret
   ```

#### Slack Bot Integration

1. **Create Slack App**: Go to https://api.slack.com/apps
2. **Add Bot Token Scopes**: `chat:write`, `commands`, `app_mentions:read`
3. **Install to workspace** and get bot token
4. **Add to `.env`**:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your_signing_secret
   SLACK_APP_TOKEN=xapp-your-app-token  # For socket mode
   ```

#### VSCode Extension

1. **Install extension** from VSCode marketplace (search for "JARVIS AI")
2. **Configure in VSCode settings**:
   ```json
   {
     "jarvis.apiUrl": "http://localhost:8000",
     "jarvis.apiKey": "your_api_key",
     "jarvis.enableRealtime": true
   }
   ```

---

## Post-Installation
   - Create strategic goals
   - Manage tasks
   - View analytics dashboard

4. **Join the community**:
   - GitHub Discussions
   - Slack channel
   - Stack Overflow tag

### Useful Commands

```bash
# Start development environment
make dev

# Run API server
make api

# Run web dashboard
make web

# Run tests
make test

# Format code
make format

# Run linters
make lint

# View help
make help
```

---

## Uninstallation

### Remove JARVIS

```bash
# Stop services
docker-compose down -v  # If using Docker

# Remove virtual environment
rm -rf venv

# Remove runtime files
rm -rf runtime

# Remove database (optional)
dropdb jarvis_dev -U postgres

# Remove project directory
cd ..
rm -rf jarvis
```

---

## Support

### Getting Help

- **Documentation**: https://github.com/lamiaakter14/jarvis/tree/main/docs
- **Issues**: https://github.com/lamiaakter14/jarvis/issues
- **Discussions**: https://github.com/lamiaakter14/jarvis/discussions

### Reporting Issues

When reporting issues, please include:
1. Operating system and version
2. Python version (`python --version`)
3. Node.js version (`node --version`)
4. Error messages (full stack trace)
5. Steps to reproduce
6. Expected vs actual behavior

---

**Document Version**: 1.0  
**Last Updated**: February 17, 2026  
**Tested On**: Ubuntu 22.04, macOS 13, Windows 11
**JARVIS Version**: V1 (includes REFLECTOR agent)
