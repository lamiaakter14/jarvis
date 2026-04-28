"""
JARVIS FastAPI Backend - Phase 5.3: Mobile-First AI Command Center
Orchestrator + Memory + Dashboard + System Status API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import os
from datetime import datetime

# Phase 4: Orchestrator Import
from app.services.cognitive_orchestrator import CognitiveOrchestrator
from app.services.task_repository import SqliteTaskRepository

# Orchestrator + Repository
orchestrator = CognitiveOrchestrator()
task_repo = SqliteTaskRepository()

app = FastAPI(title="JARVIS Cognitive Assistant", version="5.3.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for dashboard
os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
# Root Redirect to Dashboard
# ============================================================
@app.get("/", response_class=HTMLResponse)
async def root():
    """Phase 5: Redirect to JARVIS AI Command Center"""
    dashboard_path = os.path.join("app", "static", "dashboard.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ============================================================
# Health Check
# ============================================================
@app.get("/health")
async def health_check():
    return {
        "status": "operational",
        "version": "5.3.0",
        "phase": "5.3 - Mobile-First AI Command Center",
        "active_components": [
            "orchestrator", "dashboard", 
            "strategist", "executor", "mentor", 
            "innovator", "amplifier", "reflector", 
            "memory"
        ],
        "memory_tiers": ["episodic", "semantic", "strategic"],
        "uptime": "14h 32m 18s",
        "node": "Sakhipur"
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
    """Cognitive pipeline: full agent orchestration"""
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
    """Context perception via Strategist + memory"""
    return await orchestrator.perceive_environment("context")

@app.get("/perception/aether")
async def get_aether_perception():
    """Creative amplification via Amplifier + memory"""
    return await orchestrator.perceive_environment("aether")

@app.get("/perception/stats")
async def get_perception_stats():
    """System statistics via Amplifier + memory"""
    return await orchestrator.perceive_environment("stats")

@app.get("/perception/recommendation")
async def get_recommendation():
    """Strategic recommendations via Strategist + memory"""
    return await orchestrator.perceive_environment("recommendation")

# ============================================================
# Phase 4: Memory System
# ============================================================
@app.get("/memory/stats")
async def get_memory_stats():
    """3-Tier memory system statistics"""
    return orchestrator.get_memory_stats()

# ============================================================
# Phase 5: System Status API (Dashboard Data Source)
# ============================================================
@app.get("/system/status")
async def get_system_status():
    """Full system status for AI Command Center dashboard"""
    return {
        "system": "JARVIS Cognitive Assistant",
        "version": "5.3.0",
        "phase": "5.3 - Mobile-First AI Command Center",
        "node": "Sakhipur",
        "status": "ACTIVE",
        "uptime": "14h 32m 18s",
        "orchestrator": "active",
        "pipeline": ["perceive", "reason", "act", "reflect"],
        "active_agents": {
            "strategist": {"status": "planning", "action": "Generating plan & tasks...", "color": "#448AFF"},
            "executor": {"status": "running", "action": "TSK-023 (65%)", "color": "#00E676"},
            "mentor": {"status": "analyzing", "action": "Detecting knowledge gaps...", "color": "#FF9100"},
            "innovator": {"status": "idle", "action": "Waiting for trigger...", "color": "#B388FF"},
            "amplifier": {"status": "measuring", "action": "Performance metrics updated...", "color": "#40C4FF"},
            "reflector": {"status": "reflecting", "action": "System reflection cycle...", "color": "#FF80AB"}
        },
        "memory": orchestrator.get_memory_stats(),
        "metrics": {
            "plan_compliance": {"value": "85%", "trend": "up", "change": "12%"},
            "tasks_completed_today": {"value": 12, "trend": "up", "change": "28%"},
            "active_tasks": {"value": 3, "trend": "down", "change": "-25%"},
            "knowledge_gaps": {"value": 2, "trend": "up", "change": "33%"},
            "innovations_generated": {"value": 3, "trend": "up", "change": "50%"},
            "system_efficiency": {"value": "91%", "trend": "up", "change": "8%"}
        },
        "endpoints": {
            "dashboard": "/",
            "health": "/health",
            "tasks": "/tasks",
            "perception": [
                "/perception/context", 
                "/perception/aether", 
                "/perception/stats", 
                "/perception/recommendation"
            ],
            "memory": "/memory/stats",
            "system": "/system/status"
        }
    }

# ============================================================
# Phase 5: Dashboard Route
# ============================================================
@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """JARVIS AI Command Center Dashboard"""
    dashboard_path = os.path.join("app", "static", "dashboard.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# ============================================================
# Startup
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)