#!/bin/bash
# Setup script for JARVIS monorepo

set -e

echo "🤖 JARVIS Setup Script"
echo "======================="
echo ""

# Get the absolute path to the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "❌ Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Install package in development mode
echo "📦 Installing JARVIS in development mode..."
pip install -q -e .
echo "✅ JARVIS installed"
echo ""

# Create runtime directory structure
echo "📁 Creating runtime directory structure..."
mkdir -p runtime/{working/execution_logs,metrics,innovations,cache}
echo "✅ Runtime directories created"
echo ""

# Set up environment file
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi
echo ""

# Add PYTHONPATH to environment
PYTHONPATH_EXPORT="export PYTHONPATH=$PROJECT_ROOT/packages:$PROJECT_ROOT/apps/api:$PROJECT_ROOT/apps/cli:\$PYTHONPATH"

echo "🔧 Setting up PYTHONPATH..."
echo ""
echo "Add this to your shell configuration (~/.bashrc or ~/.zshrc):"
echo ""
echo "    $PYTHONPATH_EXPORT"
echo ""

# Create a convenience script
cat > run-api.sh << EOF
#!/bin/bash
export PYTHONPATH=$PROJECT_ROOT/packages:$PROJECT_ROOT/apps/api:$PROJECT_ROOT/apps/cli
source venv/bin/activate
python -m uvicorn jarvis_api.main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x run-api.sh

cat > run-cli.sh << EOF
#!/bin/bash
export PYTHONPATH=$PROJECT_ROOT/packages:$PROJECT_ROOT/apps/api:$PROJECT_ROOT/apps/cli
source venv/bin/activate
python -m jarvis_cli.main "\$@"
EOF
chmod +x run-cli.sh

echo "✅ Created convenience scripts: run-api.sh and run-cli.sh"
echo ""

# Check if Node.js is installed for frontend
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js installed: $NODE_VERSION"
    
    if [ -f "apps/web/package.json" ]; then
        echo ""
        echo "To set up the web dashboard:"
        echo "    cd apps/web"
        echo "    npm install"
        echo "    npm run dev"
    fi
else
    echo "⚠️  Node.js not found. Install Node.js 16+ for web dashboard."
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Quick start:"
echo "  1. Edit .env and add your OpenAI API key"
echo "  2. Run the API:  ./run-api.sh"
echo "  3. Run the CLI:  ./run-cli.sh --help"
echo "  4. Or activate venv and set PYTHONPATH manually"
echo ""
echo "For more information, see README.md and docs/MIGRATION_GUIDE.md"
