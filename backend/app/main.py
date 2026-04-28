"""
JARVIS FastAPI Backend - Phase 3: Real Agent Wiring
Bridge layer removed, real agents connected to endpoints.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

# ============================================================
# Phase 3: Real Agent Imports
# [Phase 2 TODO removed - agents wired]
# ============================================================
from app.agents.strategist_agent import StrategistAgent
from app.agents.amplifier_agent import AmplifierAgent  
from app.agents.reflector_agent import ReflectorAgent
from app.services.task_repository import SqliteTaskRepository

# ============================================================
# Phase 3: Real Agent Initialization
# [Phase 2 TODO removed - instances created]
# ============================================================
strategist = StrategistAgent()
amplifier = AmplifierAgent()
reflector = ReflectorAgent()
task_repo = SqliteTaskRepository()

app = FastAPI(title="JARVIS Cognitive Assistant", version="3.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Models
# ============================================================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = []

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: str
    updated_at: str

# ============================================================
# Health Check
# ============================================================
@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "version": "3.0.0",
        "phase": "3 - Real Agent Wiring",
        "active_agents": ["strategist", "amplifier", "reflector"]
    }

# ============================================================
# Task Endpoints
# ============================================================
@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task"""
    task_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    new_task = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": "pending",
        "priority": task.priority,
        "tags": task.tags or [],
        "created_at": now,
        "updated_at": now
    }
    
    task_repo.save(new_task)
    return new_task

@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks():
    """List all tasks"""
    return task_repo.list_all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task"""
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskCreate):
    """Update an existing task"""
    existing = task_repo.get_by_id(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    existing["title"] = task_update.title
    existing["description"] = task_update.description
    existing["priority"] = task_update.priority
    existing["tags"] = task_update.tags or []
    existing["updated_at"] = datetime.utcnow().isoformat()
    
    task_repo.update(existing)
    return existing

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_repo.delete(task_id)
    return {"message": "Task deleted", "task_id": task_id}

# ============================================================
# Phase 3: Task Understanding - Strategist + Reflector
# [Bridge: TaskUnderstandingBridge → REMOVED]
# Wired: strategist.analyze_task() + reflector.reflect_on_task()
# ============================================================
@app.get("/tasks/{task_id}/understanding")
async def get_task_understanding(task_id: str):
    """
    Phase 3: Real agent analysis pipeline
    Strategist analyzes → Reflector validates
    """
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Real agent execution
    analysis = await strategist.analyze_task(task)
    reflection = await reflector.reflect_on_task(task, analysis)
    
    return {
        "task_id": task_id,
        "task_title": task["title"],
        "analysis": analysis,
        "reflection": reflection,
        "agent_pipeline": ["strategist", "reflector"],
        "phase": "3-real-agents"
    }

# ============================================================
# Phase 3: Perception Endpoints - Strategist + Amplifier
# [Bridge: GeneralPerceptionBridge → REMOVED]
# Wired: strategist.perceive_context(), strategist.recommend()
#        amplifier.amplify(), amplifier.get_stats()
# ============================================================

@app.get("/perception/context")
async def get_perception_context():
    """
    Phase 3: Context-aware perception
    Strategist agent analyzes environment holistically
    """
    result = await strategist.perceive_context()
    return {
        "perception_type": "context",
        "result": result,
        "agent": "strategist",
        "phase": "3-real-agents"
    }

@app.get("/perception/aether")
async def get_aether_perception():
    """
    Phase 3: Creative signal amplification
    Amplifier agent detects trends and amplifies signals
    """
    result = await amplifier.amplify()
    return {
        "perception_type": "aether",
        "result": result,
        "agent": "amplifier",
        "phase": "3-real-agents"
    }

@app.get("/perception/stats")
async def get_perception_stats():
    """
    Phase 3: System statistics & metrics
    Amplifier agent provides cognitive statistics
    """
    result = await amplifier.get_stats()
    return {
        "perception_type": "stats",
        "result": result,
        "agent": "amplifier",
        "phase": "3-real-agents"
    }

@app.get("/perception/recommendation")
async def get_recommendation():
    """
    Phase 3: Strategic recommendations
    Strategist agent generates action plan
    """
    result = await strategist.recommend()
    return {
        "perception_type": "recommendation",
        "result": result,
        "agent": "strategist",
        "phase": "3-real-agents"
    }

# ============================================================
# Startup
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
