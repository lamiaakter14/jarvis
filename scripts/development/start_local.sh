#!/bin/bash
# Start local development environment

set -e

echo "Starting JARVIS local development environment..."

# Start Docker services
echo "Starting Docker services (PostgreSQL, Redis)..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Check service health
if docker-compose ps | grep -q "postgres.*Up"; then
    echo "✅ PostgreSQL is running"
else
    echo "❌ PostgreSQL failed to start"
    exit 1
fi

if docker-compose ps | grep -q "redis.*Up"; then
    echo "✅ Redis is running"
else
    echo "❌ Redis failed to start"
    exit 1
fi

# Set PYTHONPATH
export PYTHONPATH="${PWD}"

echo ""
echo "Services are ready!"
echo ""
echo "To start API server:"
echo "  python -m apps.api.jarvis_api.main"
echo ""
echo "To start web dashboard:"
echo "  cd apps/web/dashboard && npm run dev"
echo ""
echo "To stop services:"
echo "  docker-compose down"
