"""FastAPI main application for JARVIS cognitive assistant."""

from datetime import datetime, timezone
from typing import Any, Literal, Optional
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from jarvis_core.engine.intent_engine import detect_intent, generate_response
from jarvis_core.agents.planner_agent import PlannerAgent
from jarvis_core.agents.money_agent import money_agent

from jarvis_core.bridge.agent_bridge import (
    AmplifierBridge, ExecutorBridge, InnovatorBridge, MentorBridge, StrategistBridge,
)

app = FastAPI(title="JARVIS Cognitive Assistant API", version="1.0.0")
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
async def root(): return {"message": "JARVIS Cognitive Assistant API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check(): return {"status": "healthy", "agents": ["planner", "executor", "strategist", "mentor", "innovator", "amplifier"]}

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
async def nf(request, exc): return JSONResponse(status_code=404, content={"error": "Not Found"})
@app.exception_handler(500)
async def se(request, exc): return JSONResponse(status_code=500, content={"error": "Error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ============================================================
# Phase 5: Diary API
# ============================================================
from jarvis_core.memory.diary_service import DiaryService
diary = DiaryService()

class DiaryEntry(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

@app.post("/api/diary")
async def create_diary(entry: DiaryEntry):
    result = diary.create_entry(entry.text)
    return {"status": "saved", "entry": result}

@app.get("/api/diary")
async def list_diary(date: str = None):
    entries = diary.get_entries(date)
    dates = diary.list_dates()
    return {"dates": dates, "entries": entries, "total": len(entries)}

# ============================================================
# Phase 5.1: File Upload for Diary
# ============================================================
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
import shutil

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'memory', 'diary')

@app.post("/api/diary/upload")
async def upload_diary_file(file: UploadFile = File(...)):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join(UPLOAD_DIR, today, "files")
    os.makedirs(folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(folder, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"status": "uploaded", "filename": filename, "date": today, "path": f"memory/diary/{today}/files/{filename}"}

@app.get("/api/diary/files/{date}")
async def list_files(date: str):
    folder = os.path.join(UPLOAD_DIR, date, "files")
    if not os.path.exists(folder):
        return {"files": []}
    files = os.listdir(folder)
    return {"date": date, "files": files}

@app.get("/api/diary/file/{date}/{filename}")
async def get_file(date: str, filename: str):
    filepath = os.path.join(UPLOAD_DIR, date, "files", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return JSONResponse(status_code=404, content={"error": "File not found"})

@app.get("/api/money/progress")
async def money_progress_endpoint(current: float, target: float):
    """Track income progress"""
    try:
        result = money_agent.track_progress(current, target)
        return result
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# Phase 6: Money Mode API
# ============================================================
from jarvis_core.agents.money_agent import money_agent

@app.post("/api/money/plan")
async def money_plan(request: dict):
    result = money_agent.plan(request.get("target_amount", 10000), request.get("days", 7), request.get("skills", []))
    return {"status": "success", "plan": result}

@app.get("/api/money/progress")
async def money_progress(current: int = 0, target: int = 10000):
    result = money_agent.track_progress(current, target)
    return {"status": "success", "progress": result}

@app.get("/api/money/plan")
async def money_plan_get(target_amount: int = 10000, days: int = 7, skills: str = "graphic_design"):
    """GET version for browser testing"""
    skills_list = [s.strip() for s in skills.split(",")]
    from jarvis_core.agents.money_agent import money_agent
    result = money_agent.plan(
        target_amount=target_amount,
        days=days,
        skills=skills_list
    )
    return {"status": "success", "plan": result}

