"""
JARVIS FastAPI Backend - Phase 4: Cognitive Orchestration
Bridge removed, Orchestrator + 3-Tier Memory System wired.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

# ============================================================
# Phase 4: Orchestrator Import
# ============================================================
from app.services.cognitive_orchestrator import CognitiveOrchestrator
from app.services.task_repository import SqliteTaskRepository

# ============================================================
# Phase 4: Orchestrator Initialization (manages all agents + memory)
# ============================================================
orchestrator = CognitiveOrchestrator()
task_repo = SqliteTaskRepository()

app = FastAPI(title="JARVIS Cognitive Assistant", version="4.0.0")

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
        "version": "4.0.0",
        "phase": "4 - Cognitive Orchestration + Memory",
        "active_components": ["orchestrator", "strategist", "amplifier", "reflector", "memory"],
        "memory_tiers": ["episodic", "semantic", "strategic"]
    }

# ============================================================
# Task CRUD Endpoints
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
# Phase 4: Orchestrated Task Understanding
# Pipeline: Perceive → Reason → Act → Reflect with Memory
# ============================================================
@app.get("/tasks/{task_id}/understanding")
async def get_task_understanding(task_id: str):
    """
    Phase 4: Full cognitive pipeline
    Memory context → Strategist → Amplifier → Reflector → Memory store
    """
    task = task_repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await orchestrator.process_task(task)

# ============================================================
# Phase 4: Orchestrated Perception Endpoints
# Routed through orchestrator with memory recording
# ============================================================

@app.get("/perception/context")
async def get_perception_context():
    """
    Phase 4: Context perception via orchestrator
    Strategist analysis + episodic memory recording
    """
    return await orchestrator.perceive_environment("context")

@app.get("/perception/aether")
async def get_aether_perception():
    """
    Phase 4: Creative amplification via orchestrator
    Amplifier signals + memory storage
    """
    return await orchestrator.perceive_environment("aether")

@app.get("/perception/stats")
async def get_perception_stats():
    """
    Phase 4: Statistics via orchestrator
    Amplifier metrics + memory tracking
    """
    return await orchestrator.perceive_environment("stats")

@app.get("/perception/recommendation")
async def get_recommendation():
    """
    Phase 4: Strategic recommendations via orchestrator
    Strategist planning + strategy memory
    """
    return await orchestrator.perceive_environment("recommendation")

# ============================================================
# Phase 4: Memory System Endpoint
# 3-Tier: Episodic | Semantic | Strategic
# ============================================================
@app.get("/memory/stats")
async def get_memory_stats():
    """
    Phase 4: Memory system statistics
    Shows all 3 memory tiers status
    """
    return orchestrator.get_memory_stats()

# ============================================================
# Startup
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)