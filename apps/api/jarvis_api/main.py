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

# ============================================================
# Phase 2: Intent Engine Import
# ============================================================
from jarvis_core.engine.intent_engine import detect_intent, generate_response

# ============================================================
# Phase 3: Planner Agent Import
# ============================================================
from jarvis_core.agents.planner_agent import PlannerAgent

# ============================================================
# Phase 4: Executor Agent Import
# ============================================================
from jarvis_core.agents.executor_agent import ExecutorAgent

# Create FastAPI app
app = FastAPI(
    title="JARVIS Cognitive Assistant API",
    description="AI-powered cognitive assistant with multi-agent architecture",
    version="4.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Phase 3 + Phase 4: Initialize Agents
# ============================================================
planner = PlannerAgent()
executor = ExecutorAgent()

# ---------------------------------------------------------------------------
# In-memory task store
# ---------------------------------------------------------------------------
_tasks: dict[str, dict[str, Any]] = {}

TaskStatus = Literal["todo", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high", "critical"]


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    roi: float = Field(0.5, ge=0.0, le=1.0)
    cognitive_load: int = Field(3, ge=1, le=10)
    estimated_hours: float = Field(1.0, gt=0.0)
    tags: list[str] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    roi: Optional[float] = Field(None, ge=0.0, le=1.0)
    cognitive_load: Optional[int] = Field(None, ge=1, le=10)
    estimated_hours: Optional[float] = Field(None, gt=0.0)
    tags: Optional[list[str]] = None


# ============================================================
# Phase 2: Chat Schema
# ============================================================
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


def _make_task(data: TaskCreate) -> dict[str, Any]:
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
    return {"message": "JARVIS Cognitive Assistant API", "version": "4.0.0", "status": "running"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "architecture": "clean_architecture",
        "agents": ["strategist", "mentor", "executor", "innovator", "amplifier", "planner"],
    }


# ============================================================
# Phase 2 + Phase 3 + Phase 4: Chat API
# ============================================================
@app.post("/api/chat")
async def chat(request: ChatRequest):
    r = detect_intent(request.message)
    response_text = generate_response(r["intent"], request.message)
    meta = {}
    
    # Phase 3: Planner integration
    if r["intent"] == "planner":
        try:
            plan_result = planner.plan(request.message)
            meta["project"] = plan_result["project"]
            meta["questions"] = plan_result["questions"]
            meta["analysis"] = plan_result["analysis"]
        except Exception as e:
            meta["planner_error"] = str(e)
    
    # Phase 4: Execution integration
    elif r["intent"] == "execution":
        if any(kw in request.message.lower() for kw in ["start", "execute", "run", "all"]):
            results = executor.run_all()
            meta["execution"] = {
                "tasks_executed": len(results),
                "completed": [t["title"] for t in results[:5]],
                "status": "completed"
            }
        meta["queue_status"] = executor.get_queue_status()
    
    return {
        "intent": r["intent"],
        "mode": r["mode"],
        "response": response_text,
        "confidence": r["confidence"],
        "meta": meta,
    }


# ============================================================
# Phase 4: Execution API Endpoints
# ============================================================

@app.post("/api/execute/start")
async def start_execution():
    """Execute all queued tasks."""
    results = executor.run_all()
    return {
        "status": "success",
        "tasks_executed": len(results),
        "tasks": [{"id": t["id"], "title": t["title"]} for t in results],
        "queue_status": executor.get_queue_status()
    }


@app.post("/api/execute/queue")
async def queue_project(data: dict = None):
    """Queue project tasks for execution."""
    if data and "project" in data:
        tasks = executor.queue_tasks(data["project"])
        return {
            "status": "queued",
            "tasks_queued": len(tasks),
            "queue_status": executor.get_queue_status()
        }
    return {"status": "ready", "message": "Send project data"}


@app.get("/api/execute/status")
async def get_execution_status():
    """Get current execution queue status."""
    return executor.get_queue_status()


# ---------------------------------------------------------------------------
# Cognitive Loop
# ---------------------------------------------------------------------------
@app.post("/api/cognitive-loop")
async def run_cognitive_loop() -> dict[str, Any]:
    try:
        strategist = StrategistBridge()
        mentor = MentorBridge()
        executor_bridge = ExecutorBridge()
        innovator = InnovatorBridge()
        amplifier = AmplifierBridge()

        plan = strategist.generate_plan()
        gaps = mentor.analyze_execution_logs()

        task_feedback = []
        for task in plan.get("tasks", []):
            feedback = mentor.mentor_task(task)
            task_feedback.append(feedback)

        executor_bridge.run_tasks()
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


@app.get("/api/plan/today")
async def get_daily_plan() -> dict[str, Any]:
    try:
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


@app.post("/api/plan/generate")
async def generate_plan() -> dict[str, Any]:
    try:
        strategist = StrategistBridge()
        plan = strategist.generate_plan()
        return {"status": "success", "plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate plan: {str(e)}")


@app.get("/api/gaps")
async def get_knowledge_gaps() -> dict[str, Any]:
    try:
        mentor = MentorBridge()
        gaps = mentor.analyze_execution_logs()
        return {"status": "success", "gaps": gaps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze gaps: {str(e)}")


@app.get("/api/innovations")
async def get_innovations() -> dict[str, Any]:
    try:
        innovator = InnovatorBridge()
        innovations = innovator.create_innovations()
        return {"status": "success", "innovations": innovations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create innovations: {str(e)}")


@app.get("/api/performance")
async def get_performance_metrics() -> dict[str, Any]:
    try:
        amplifier = AmplifierBridge()
        performance = amplifier.amplify()
        return {"status": "success", "performance": performance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze performance: {str(e)}")


@app.get("/api/tasks")
async def list_tasks() -> list[dict[str, Any]]:
    return list(_tasks.values())


@app.post("/api/tasks", status_code=201)
async def create_task(data: TaskCreate) -> dict[str, Any]:
    task = _make_task(data)
    _tasks[task["id"]] = task
    return task


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: str, data: TaskUpdate) -> dict[str, Any]:
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
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": "Not Found", "message": "The requested endpoint does not exist", "path": str(request.url)})


@app.exception_handler(500)
async def server_error_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": "An unexpected error occurred", "detail": str(exc)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)