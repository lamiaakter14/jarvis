"""FastAPI main application for JARVIS cognitive assistant."""

from datetime import datetime, timezone
from typing import Any, Optional
import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
import shutil

from jarvis_core.engine.intent_engine import detect_intent, generate_response
from jarvis_core.agents.planner_agent import PlannerAgent
from jarvis_core.agents.money_agent import money_agent
from jarvis_core.agents.executor_agent import ExecutorAgent
from jarvis_core.agents.life_agent import life_agent
from jarvis_core.memory.diary_service import DiaryService
from jarvis_core.memory.context_store import context_store

app = FastAPI(title="JARVIS OS", version="5.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

planner = PlannerAgent()
diary = DiaryService()
executor = ExecutorAgent()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)

class DiaryEntry(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'memory', 'diary')

@app.get("/")
async def root(): return {"message": "JARVIS OS", "version": "5.3.0"}

@app.get("/health")
async def health(): return {"status": "healthy"}

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

# Diary
@app.post("/api/diary")
async def create_diary(entry: DiaryEntry):
    return {"status": "saved", "entry": diary.create_entry(entry.text)}

@app.get("/api/diary")
async def list_diary(date: str = None):
    entries = diary.get_entries(date)
    return {"dates": diary.list_dates(), "entries": entries, "total": len(entries)}

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
    return {"status": "uploaded", "filename": filename, "date": today}

@app.get("/api/diary/files/{date}")
async def list_files(date: str):
    folder = os.path.join(UPLOAD_DIR, date, "files")
    if not os.path.exists(folder): return {"files": []}
    return {"date": date, "files": os.listdir(folder)}

# Money
@app.post("/api/money/plan")
async def money_plan(request: dict):
    result = money_agent.plan(request.get("target_amount", 10000), request.get("days", 7), request.get("skills", []))
    return {"status": "success", "plan": result}

@app.get("/api/money/get-plan")
async def money_get(target_amount: int = 10000, days: int = 7, skills: str = ""):
    skills_list = [s.strip() for s in skills.split(",")] if skills else []
    result = money_agent.plan(target_amount, days, skills_list)
    return {"status": "success", "plan": result}

@app.get("/api/money/progress")
async def money_progress(current: float = 0, target: float = 10000):
    return money_agent.track_progress(current, target)

# Context
@app.get("/api/context")
async def get_contexts(category: str = None):
    return context_store.get_all(category)

@app.post("/api/context")
async def add_context(request: dict):
    return context_store.add(key=request.get("key"), value=request.get("value"), category=request.get("category", "general"), location=request.get("location", "Sakhipur"))

@app.delete("/api/context/{context_id}")
async def delete_context(context_id: str):
    return {"status": "deleted" if context_store.delete(context_id) else "not found"}

@app.get("/api/context/categories")
async def get_categories():
    return {"categories": context_store.get_categories()}

# Execution
@app.post("/api/execute/queue")
async def exec_queue(data: dict = None):
    if data and "project" in data:
        executor.queue_tasks(data["project"])
        return {"status": "queued"}
    return {"status": "ready"}

@app.post("/api/execute/start")
async def exec_start():
    results = executor.run_all()
    return {"status": "success", "tasks_executed": len(results)}

@app.get("/api/execute/status")
async def exec_status():
    return executor.get_queue_status()

# Life System
@app.get("/api/life/dashboard")
async def life_dashboard():
    """Get complete life dashboard data"""
    return life_agent.get_dashboard()

@app.post("/api/life/skill")
async def life_update_skill(request: dict):
    """Update skill progress"""
    return life_agent.update_skill(
        skill_name=request.get("skill_name"),
        current_level=request.get("current_level")
    )

@app.post("/api/life/prayer")
async def life_update_prayer(request: dict):
    """Update daily prayer status"""
    return life_agent.update_prayer(
        prayer_name=request.get("prayer_name"),
        completed=request.get("completed")
    )

@app.post("/api/life/quran")
async def life_update_quran(request: dict):
    """Update Quran reading progress"""
    return life_agent.update_quran(pages=request.get("pages", 0))

@app.post("/api/life/contact")
async def life_add_contact(request: dict):
    """Add network contact"""
    return life_agent.add_contact(
        category=request.get("category"),
        name=request.get("name"),
        role=request.get("role")
    )

@app.post("/api/life/accountability")
async def life_add_accountability(request: dict):
    """Add daily accountability entry"""
    return life_agent.add_accountability(task=request.get("task"))

@app.post("/api/life/milestone")
async def life_update_milestone(request: dict):
    """Update milestone completion"""
    return life_agent.update_milestone(
        milestone_index=request.get("milestone_index"),
        completed=request.get("completed")
    )

# Financial API for Life System
@app.get("/api/life/financial")
async def life_get_financial():
    """Get financial goals for MP election"""
    return life_agent.get_financial_goals()

@app.post("/api/life/savings")
async def life_update_savings(request: dict):
    """Update current savings"""
    return life_agent.update_savings(amount=request.get("amount", 0))

@app.post("/api/life/funding")
async def life_add_funding(request: dict):
    """Add funding from source"""
    return life_agent.add_funding_source(
        source=request.get("source"),
        amount=request.get("amount", 0)
    )

@app.exception_handler(404)
async def nf(request, exc): return JSONResponse(status_code=404, content={"error": "Not Found"})
@app.exception_handler(500)
async def se(request, exc): return JSONResponse(status_code=500, content={"error": "Error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ============================================================
# Phase 9: Real-world Execution API
# ============================================================
from jarvis_core.agents.real_executor import RealExecutor
real_executor = RealExecutor()

@app.get("/api/execute/permission/{action}")
async def check_perm(action: str):
    return real_executor.check_permission(action)

@app.get("/api/execute/file/read")
async def file_read(path: str = ""):
    return real_executor.read_file(path)

@app.post("/api/execute/file/create")
async def file_create(data: dict):
    return real_executor.create_file(data.get("path", ""), data.get("content", ""))

@app.delete("/api/execute/file/delete")
async def file_delete(path: str = "", confirmation: str = ""):
    return real_executor.delete_file(path, confirmation)

@app.get("/api/execute/github/status")
async def github_status():
    return real_executor.git_status()

@app.post("/api/execute/github/commit")
async def github_commit(data: dict):
    return real_executor.git_commit(data.get("message", "JARVIS auto-commit"))

@app.post("/api/execute/github/push")
async def github_push(data: dict):
    return real_executor.git_push(data.get("confirmation", ""))

@app.post("/api/execute/pdf/generate")
async def pdf_generate(data: dict):
    return real_executor.generate_pdf(data.get("template", "document"), data.get("data", {}))

@app.get("/api/execute/queue")
async def execution_queue():
    return {"queue": real_executor.get_queue(), "log": real_executor.get_log()}
