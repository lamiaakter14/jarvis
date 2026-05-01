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
from jarvis_core.memory.diary_service import DiaryService
from jarvis_core.memory.context_store import context_store

app = FastAPI(title="JARVIS OS", version="5.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

planner = PlannerAgent()
diary = DiaryService()

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
    return {"dates": diary.list_dates(), "entries": diary.get_entries(date), "total": len(diary.get_entries(date))}

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

@app.exception_handler(404)
async def nf(request, exc): return JSONResponse(status_code=404, content={"error": "Not Found"})
@app.exception_handler(500)
async def se(request, exc): return JSONResponse(status_code=500, content={"error": "Error", "detail": str(exc)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
