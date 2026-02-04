#!/bin/bash
# Setup development environment

set -e

echo "Setting up JARVIS development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio black ruff mypy isort bandit

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pip install pre-commit
pre-commit install

# Check for Node.js
if command -v node &> /dev/null; then
    echo "Node.js version: $(node --version)"
    
    # Install web dashboard dependencies
    if [ -d "apps/web/dashboard" ]; then
        echo "Installing web dashboard dependencies..."
        cd apps/web/dashboard
        npm install
        cd ../../..
    fi
else
    echo "Warning: Node.js not found. Skipping web dashboard setup."
fi

# Create runtime directories
echo "Creating runtime directories..."
mkdir -p runtime/{working,metrics,innovations,state,logs}

# Check for Docker
if command -v docker &> /dev/null; then
    echo "Docker version: $(docker --version)"
    echo "Run 'docker-compose up -d' to start services"
else
    echo "Warning: Docker not found. Install Docker for local development."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and configure"
echo "  2. Run 'docker-compose up -d' to start services"
echo "  3. Run 'make dev' to start development server"
echo "  4. Run 'make test' to run tests"
