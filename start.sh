#!/bin/bash

echo "🚀 Starting JARVIS OS v5.3.0..."

# Start backend
cd ~/jarvis
export PYTHONPATH=~/jarvis/packages:$PYTHONPATH
python3.11 -m uvicorn apps.api.jarvis_api.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

# Start frontend
cd ~/jarvis/apps/web
pnpm dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

echo ""
echo "🌐 JARVIS OS is running:"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both"

wait
