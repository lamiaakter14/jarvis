"""FastAPI main application for JARVIS cognitive assistant."""

from datetime import datetime, timezone
from typing import Any, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from jarvis_core.bridge.agent_bridge import (
    AmplifierBridge,
    ExecutorBridge,
    InnovatorBridge,
    MentorBridge,
    StrategistBridge,
)

# Create FastAPI app
app = FastAPI(
    title="JARVIS Cognitive Assistant API",
    description="AI-powered cognitive assistant with multi-agent architecture",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory task store (no database required for development)
# ---------------------------------------------------------------------------
_tasks: dict[str, dict[str, Any]] = {}

TaskStatus = Literal["todo", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high", "critical"]


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    roi: float = Field(0.5, ge=0.0, le=1.0)
    cognitive_load: int = Field(3, ge=1, le=10)
    estimated_hours: float = Field(1.0, gt=0.0)
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    roi: Optional[float] = Field(None, ge=0.0, le=1.0)
    cognitive_load: Optional[int] = Field(None, ge=1, le=10)
    estimated_hours: Optional[float] = Field(None, gt=0.0)
    tags: Optional[list[str]] = None


def _make_task(data: TaskCreate) -> dict[str, Any]:
    """Create a new task dict with generated id and timestamps."""
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "id": str(uuid4()),
        "title": data.title,
        "description": data.description,
        "status": data.status,
        "priority": data.priority,
        "roi": data.roi,
        "cognitive_load": data.cognitive_load,
        "estimated_hours": data.estimated_hours,
        "tags": data.tags,
        "created_at": now,
        "completed_at": None,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "JARVIS Cognitive Assistant API", "version": "1.0.0", "status": "running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "architecture": "clean_architecture",
        "agents": ["strategist", "mentor", "executor", "innovator", "amplifier"],
    }


# ---------------------------------------------------------------------------
# Cognitive Loop
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
# Plans
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
    """Generate a new daily plan."""
    try:
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


# ---------------------------------------------------------------------------
# Knowledge Gaps
# ---------------------------------------------------------------------------


@app.get("/api/gaps")
async def get_knowledge_gaps() -> dict[str, Any]:
    """Get identified knowledge gaps."""
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
    """Get generated innovations."""
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
    """Get performance metrics and analytics."""
    try:
        amplifier = AmplifierBridge()
        performance = amplifier.amplify()
        return {"status": "success", "performance": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze performance: {str(e)}")


# ---------------------------------------------------------------------------
# Tasks (in-memory CRUD)
# ---------------------------------------------------------------------------


@app.get("/api/tasks")
async def list_tasks() -> list[dict[str, Any]]:
    """List all tasks."""
    return list(_tasks.values())


@app.post("/api/tasks", status_code=201)
async def create_task(data: TaskCreate) -> dict[str, Any]:
    """Create a new task."""
    task = _make_task(data)
    _tasks[task["id"]] = task
    return task


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, data: TaskUpdate) -> dict[str, Any]:
    """Update an existing task."""
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = _tasks[task_id]
    updates = data.model_dump(exclude_none=True)
    task.update(updates)
    if updates.get("status") == "done" and task.get("completed_at") is None:
        task["completed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    _tasks[task_id] = task
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str) -> None:
    """Delete a task."""
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]


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
            "detail": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
