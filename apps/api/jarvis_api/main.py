"""FastAPI main application for JARVIS cognitive assistant."""

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jarvis_core.bridge.agent_bridge import (
    AmplifierBridge,
    ExecutorBridge,
    InnovatorBridge,
    MentorBridge,
    StrategistBridge,
)

# ---------------------------------------------------------------------------
# CORS origins: read from env, default to localhost dev ports
# ---------------------------------------------------------------------------
_raw_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",") if o.strip()]

# ---------------------------------------------------------------------------
# In-memory task store (per-process; sufficient for demo/launch)
# ---------------------------------------------------------------------------
_TASKS: list[dict[str, Any]] = [
    {
        "task_id": "task_1",
        "title": "Review Q4 Objectives",
        "description": "Scan quarterly goals and align daily priorities",
        "priority": "high",
        "status": "pending",
        "agent_type": "strategist",
        "created_at": "2025-01-15T10:00:00Z",
    },
    {
        "task_id": "task_2",
        "title": "Update User Documentation",
        "description": "Revise user guide with latest features and improvements",
        "priority": "medium",
        "status": "in_progress",
        "agent_type": "executor",
        "created_at": "2025-01-14T09:30:00Z",
    },
    {
        "task_id": "task_3",
        "title": "Fix Critical Security Issue",
        "description": "Address vulnerability in authentication system",
        "priority": "critical",
        "status": "pending",
        "agent_type": "executor",
        "created_at": "2025-01-16T14:20:00Z",
    },
    {
        "task_id": "task_4",
        "title": "Database Optimization",
        "description": "Optimize database queries for better performance",
        "priority": "high",
        "status": "in_progress",
        "agent_type": "executor",
        "created_at": "2025-01-13T11:00:00Z",
    },
    {
        "task_id": "task_5",
        "title": "Deploy Version 1.2.0",
        "description": "Deploy latest version to production environment",
        "priority": "medium",
        "status": "completed",
        "agent_type": "executor",
        "created_at": "2025-01-12T16:45:00Z",
    },
    {
        "task_id": "task_6",
        "title": "Research AI Integration Options",
        "description": "Evaluate different AI models for task automation",
        "priority": "low",
        "status": "pending",
        "agent_type": "innovator",
        "created_at": "2025-01-10T08:15:00Z",
    },
]

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="JARVIS Cognitive Assistant API",
    description="AI-powered cognitive assistant with multi-agent architecture",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "JARVIS Cognitive Assistant API", "version": "1.0.0", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check (legacy path)."""
    return {
        "status": "healthy",
        "architecture": "clean_architecture",
        "agents": ["strategist", "mentor", "executor", "innovator", "amplifier"],
    }


@app.get("/api/v1/health")
async def health_check_v1():
    """Health check at versioned path (used by Docker healthcheck and deployment scripts)."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "api": "healthy",
            "bridge": "healthy",
        },
    }


# ---------------------------------------------------------------------------
# Cognitive loop
# ---------------------------------------------------------------------------

@app.post("/api/cognitive-loop")
async def run_cognitive_loop() -> dict[str, Any]:
    """Execute the complete cognitive loop with all 5 agents."""
    try:
        strategist = StrategistBridge()
        mentor = MentorBridge()
        executor = ExecutorBridge()
        innovator = InnovatorBridge()
        amplifier = AmplifierBridge()

        plan = strategist.generate_plan()
        gaps = mentor.analyze_execution_logs()

        task_feedback = []
        for task in plan.get("tasks", []):
            feedback = mentor.mentor_task(task)
            task_feedback.append(feedback)

        executor.run_tasks()
        innovations = innovator.create_innovations()
        performance = amplifier.amplify()

        return {
            "status": "success",
            "strategist": {"plan": plan},
            "mentor": {"gaps": gaps, "task_feedback": task_feedback},
            "executor": {"status": "completed"},
            "innovator": {"innovations": innovations},
            "amplifier": {"performance": performance},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cognitive loop failed: {str(e)}")


# ---------------------------------------------------------------------------
# Plan endpoints
# ---------------------------------------------------------------------------

@app.get("/api/plan/today")
async def get_daily_plan() -> dict[str, Any]:
    """Get today's daily plan."""
    try:
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


@app.post("/api/plan/generate")
async def generate_plan() -> dict[str, Any]:
    """Generate a fresh daily plan (alias used by the frontend Plans page)."""
    try:
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


# ---------------------------------------------------------------------------
# Gaps
# ---------------------------------------------------------------------------

@app.get("/api/gaps")
async def get_knowledge_gaps() -> dict[str, Any]:
    """Get identified knowledge gaps (returns a list matching the frontend Gap type)."""
    try:
        mentor = MentorBridge()
        gaps = mentor.analyze_execution_logs()
        return {"status": "success", "gaps": gaps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze gaps: {str(e)}")


# ---------------------------------------------------------------------------
# Innovations
# ---------------------------------------------------------------------------

@app.get("/api/innovations")
async def get_innovations() -> dict[str, Any]:
    """Get generated innovations (returns a list matching the frontend Innovation type)."""
    try:
        innovator = InnovatorBridge()
        innovations = innovator.create_innovations()
        return {"status": "success", "innovations": innovations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create innovations: {str(e)}")


# ---------------------------------------------------------------------------
# Performance
# ---------------------------------------------------------------------------

@app.get("/api/performance")
async def get_performance_metrics() -> dict[str, Any]:
    """Get performance metrics."""
    try:
        amplifier = AmplifierBridge()
        performance = amplifier.amplify()
        return {"status": "success", "performance": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze performance: {str(e)}")


# ---------------------------------------------------------------------------
# Tasks CRUD
# ---------------------------------------------------------------------------

@app.get("/api/tasks")
async def list_tasks() -> list[dict[str, Any]]:
    """List all tasks."""
    return _TASKS


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str) -> dict[str, Any]:
    """Get a single task by ID."""
    for task in _TASKS:
        if task["task_id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/api/tasks")
async def create_task(body: dict[str, Any]) -> dict[str, Any]:
    """Create a new task."""
    import uuid
    from datetime import datetime

    task = {
        "task_id": body.get("task_id", str(uuid.uuid4())),
        "title": body.get("title", ""),
        "description": body.get("description", ""),
        "priority": body.get("priority", "medium"),
        "status": body.get("status", "pending"),
        "agent_type": body.get("agent_type", "executor"),
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    _TASKS.append(task)
    return task


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, body: dict[str, Any]) -> dict[str, Any]:
    """Update an existing task."""
    for task in _TASKS:
        if task["task_id"] == task_id:
            task.update({k: v for k, v in body.items() if k != "task_id"})
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str) -> dict[str, Any]:
    """Delete a task."""
    for i, task in enumerate(_TASKS):
        if task["task_id"] == task_id:
            _TASKS.pop(i)
            return {"status": "deleted", "task_id": task_id}
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "path": str(request.url),
        },
    )


@app.exception_handler(500)
async def server_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        },
    )


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
