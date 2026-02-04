"""FastAPI main application for JARVIS cognitive assistant."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.bridge.agent_bridge import (
    StrategistBridge,
    MentorBridge,
    ExecutorBridge,
    InnovatorBridge,
    AmplifierBridge
)
from core.memory_manager import MemoryManager

# Create FastAPI app
app = FastAPI(
    title="JARVIS Cognitive Assistant API",
    description="AI-powered cognitive assistant with multi-agent architecture",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (would normally use DI container)
memory_manager = MemoryManager()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "JARVIS Cognitive Assistant API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "architecture": "clean_architecture",
        "agents": ["strategist", "mentor", "executor", "innovator", "amplifier"]
    }


@app.post("/api/cognitive-loop")
async def run_cognitive_loop() -> Dict[str, Any]:
    """Execute the complete cognitive loop with all 5 agents.
    
    Returns:
        Dictionary with results from all agents
    """
    try:
        # Initialize agents
        strategist = StrategistBridge(memory_manager)
        mentor = MentorBridge(memory_manager)
        executor = ExecutorBridge(memory_manager)
        innovator = InnovatorBridge(memory_manager)
        amplifier = AmplifierBridge(memory_manager)
        
        # Execute each agent
        plan = strategist.generate_plan()
        gaps = mentor.analyze_execution_logs()
        
        # Mentor each task in the plan
        task_feedback = []
        for task in plan.get("tasks", []):
            feedback = mentor.mentor_task(task)
            task_feedback.append(feedback)
        
        executor.run_tasks()
        innovations = innovator.create_innovations()
        performance = amplifier.amplify()
        
        return {
            "status": "success",
            "strategist": {
                "plan": plan
            },
            "mentor": {
                "gaps": gaps,
                "task_feedback": task_feedback
            },
            "executor": {
                "status": "completed"
            },
            "innovator": {
                "innovations": innovations
            },
            "amplifier": {
                "performance": performance
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cognitive loop failed: {str(e)}")


@app.get("/api/plan/today")
async def get_daily_plan() -> Dict[str, Any]:
    """Get today's daily plan.
    
    Returns:
        Daily plan with tasks
    """
    try:
        strategist = StrategistBridge(memory_manager)
        plan = strategist.generate_plan()
        return {
            "status": "success",
            "plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


@app.get("/api/gaps")
async def get_knowledge_gaps() -> Dict[str, Any]:
    """Get identified knowledge gaps.
    
    Returns:
        List of knowledge gaps
    """
    try:
        mentor = MentorBridge(memory_manager)
        gaps = mentor.analyze_execution_logs()
        return {
            "status": "success",
            "gaps": gaps
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze gaps: {str(e)}")


@app.get("/api/innovations")
async def get_innovations() -> Dict[str, Any]:
    """Get generated innovations.
    
    Returns:
        List of innovations
    """
    try:
        innovator = InnovatorBridge(memory_manager)
        innovations = innovator.create_innovations()
        return {
            "status": "success",
            "innovations": innovations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create innovations: {str(e)}")


@app.get("/api/performance")
async def get_performance_metrics() -> Dict[str, Any]:
    """Get performance metrics and analytics.
    
    Returns:
        Performance metrics
    """
    try:
        amplifier = AmplifierBridge(memory_manager)
        performance = amplifier.amplify()
        return {
            "status": "success",
            "performance": performance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze performance: {str(e)}")


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
