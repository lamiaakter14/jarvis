"""FastAPI main application for JARVIS cognitive assistant."""

from datetime import datetime, timezone
from typing import Any, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from jarvis_core.engine.intent_engine import detect_intent, generate_response
from jarvis_core.agents.planner_agent import PlannerAgent

from jarvis_core.bridge.agent_bridge import (
    AmplifierBridge,
    ExecutorBridge,
    InnovatorBridge,
    MentorBridge,
    StrategistBridge,
)

app = FastAPI(
    title="JARVIS Cognitive Assistant API",
    description="AI-powered cognitive assistant with multi-agent architecture",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

planner = PlannerAgent()

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

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

def _make_task(data: TaskCreate) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {"id": str(uuid4()), "title": data.title, "description": data.description, "status": data.status, "priority": data.priority, "roi": data.roi, "cognitive_load": data.cognitive_load, "estimated_hours": data.estimated_hours, "tags": data.tags, "created_at": now, "completed_at": None}

@app.get("/")
async def root():
    return {"message": "JARVIS Cognitive Assistant API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": ["strategist", "mentor", "executor", "innovator", "amplifier", "planner"]}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    r = detect_intent(request.message)
    meta = {}
    if r["intent"] == "planner":
        try:
            plan_result = planner.plan(request.message)
            meta["project"] = plan_result["project"]
            meta["questions"] = plan_result["questions"]
        except Exception as e:
            meta["planner_error"] = str(e)
    return {"intent": r["intent"], "mode": r["mode"], "response": generate_response(r["intent"], request.message), "confidence": r["confidence"], "meta": meta}

@app.get("/api/tasks")
async def list_tasks(): return list(_tasks.values())

@app.post("/api/tasks", status_code=201)
async def create_task(data: TaskCreate):
    task = _make_task(data)
    _tasks[task["id"]] = task
    return task

@app.exception_handler(404)
async def not_found_handler(request, exc): return JSONResponse(status_code=404, content={"error": "Not Found"})

@app.exception_handler(500)
async def server_error_handler(request, exc): return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
