#!/bin/bash

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   JARVIS - AI Cognitive Assistant     ║"
echo "║   Quick Start Setup                    ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"

if ! command -v pip &> /dev/null; then
    echo -e "${RED}✗ pip is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip found${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker not found. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ Node.js not found. Please install Node.js first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

# Install Python dependencies
echo ""
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -e .

# Install Node dependencies
echo ""
echo -e "${BLUE}Installing Node dependencies...${NC}"
cd apps/web/dashboard
npm install
cd ../../..

# Create .env file
if [ ! -f .env ]; then
    echo ""
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env and add your OPENAI_API_KEY${NC}"
fi

# Create runtime directories
echo ""
echo -e "${BLUE}Creating runtime directories...${NC}"
mkdir -p runtime/{working,metrics,innovations,logs,state}
mkdir -p runtime/working/execution_logs

# Start infrastructure
echo ""
echo -e "${BLUE}Starting PostgreSQL and Redis...${NC}"
docker-compose up -d postgres redis

# Wait for services
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 5

# Run migrations
echo ""
echo -e "${BLUE}Running database migrations...${NC}"
cd apps/api/jarvis_api
if [ -f "alembic.ini" ]; then
    alembic -c alembic.ini upgrade head || echo -e "${YELLOW}⚠ Migration failed or no migrations to run${NC}"
else
    echo -e "${YELLOW}⚠ No alembic.ini found, skipping migrations${NC}"
fi
cd ../../..

# Success message
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║   Setup Complete! 🎉                  ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo ""
echo -e "${YELLOW}1. Configure your API key:${NC}"
echo "   Edit .env and add your OPENAI_API_KEY"
echo ""
echo -e "${YELLOW}2. Start the API server:${NC}"
echo "   make api"
echo "   or: python -m uvicorn apps.api.jarvis_api.main:app --reload"
echo ""
echo -e "${YELLOW}3. Start the web dashboard (in another terminal):${NC}"
echo "   make web"
echo "   or: cd apps/web/dashboard && npm run dev"
echo ""
echo -e "${YELLOW}4. Use the CLI:${NC}"
echo "   make cli ARGS=\"--help\""
echo "   make cli ARGS=\"strategist plan\""
echo ""
echo -e "${YELLOW}5. Access the application:${NC}"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo "   Web: http://localhost:3000"
echo ""
echo -e "${GREEN}For more commands, run: make help${NC}"
