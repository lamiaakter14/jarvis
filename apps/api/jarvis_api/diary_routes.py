"""
Diary API Routes for Jarvis OS
Handles CRUD operations for digital diary
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import base64

from jarvis_core.memory.diary_service import DiaryService, DiaryEntry

router = APIRouter(tags=["diary"])

# Initialize diary service
diary_service = DiaryService()


# Request/Response Models
class DiaryEntryCreate(BaseModel):
    date: str  # YYYY-MM-DD
    content: str
    tags: Optional[List[str]] = []
    mood: Optional[str] = None


class DiaryEntryResponse(BaseModel):
    id: str
    date: str
    content: str
    attachments: List[dict]
    tags: List[str]
    mood: Optional[str]
    created_at: str
    updated_at: str


class DiarySearchResponse(BaseModel):
    results: List[DiaryEntryResponse]
    count: int


class DiaryStatsResponse(BaseModel):
    total_entries: int
    total_attachments: int
    total_size_mb: float
    storage_path: str


# Helper function to convert DiaryEntry to response model
def entry_to_response(entry: DiaryEntry) -> DiaryEntryResponse:
    return DiaryEntryResponse(
        id=entry.id,
        date=entry.date,
        content=entry.content,
        attachments=entry.attachments,
        tags=entry.tags,
        mood=entry.mood,
        created_at=entry.created_at,
        updated_at=entry.updated_at
    )


# ============= API Endpoints =============

@router.post("/diary/entry", response_model=DiaryEntryResponse)
async def create_or_update_entry(
    date: str = Form(...),
    content: str = Form(...),
    tags: Optional[str] = Form(None),
    mood: Optional[str] = Form(None)
):
    """
    Create or update a diary entry
    """
    try:
        # Validate date format
        datetime.strptime(date, "%Y-%m-%d")
        
        # Parse tags
        tags_list = tags.split(",") if tags else []
        tags_list = [tag.strip() for tag in tags_list if tag.strip()]
        
        entry = diary_service.save_entry(
            date=date,
            content=content,
            tags=tags_list,
            mood=mood
        )
        
        return entry_to_response(entry)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving entry: {str(e)}")


@router.post("/diary/entry/with-attachments")
async def create_entry_with_attachments(
    date: str = Form(...),
    content: str = Form(...),
    tags: Optional[str] = Form(None),
    mood: Optional[str] = Form(None),
    files: List[UploadFile] = File(None)
):
    """
    Create diary entry with file attachments
    """
    try:
        # Validate date
        datetime.strptime(date, "%Y-%m-%d")
        
        # First create the entry
        tags_list = tags.split(",") if tags else []
        tags_list = [tag.strip() for tag in tags_list if tag.strip()]
        
        entry = diary_service.save_entry(
            date=date,
            content=content,
            tags=tags_list,
            mood=mood
        )
        
        # Process attachments
        attachments = []
        if files:
            for file in files:
                # Determine file type
                content_type = file.content_type or ""
                if content_type.startswith('image/'):
                    file_type = 'image'
                elif content_type.startswith('video/'):
                    file_type = 'video'
                elif content_type.startswith('audio/'):
                    file_type = 'audio'
                else:
                    file_type = 'document'
                
                # Read file content
                file_content = await file.read()
                
                # Save attachment
                attachment_info = diary_service.save_attachment(
                    date=date,
                    entry_id=entry.id,
                    filename=file.filename,
                    file_content=file_content,
                    file_type=file_type
                )
                attachments.append(attachment_info)
        
        # Update entry with attachments
        if attachments:
            entry.attachments.extend(attachments)
            diary_service.save_entry(
                date=date,
                content=entry.content,
                tags=entry.tags,
                mood=entry.mood,
                attachments=entry.attachments
            )
        
        return {
            "entry": entry_to_response(entry),
            "uploaded_files": len(attachments),
            "attachments": attachments
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/diary/entry/{date}", response_model=DiaryEntryResponse)
async def get_entry_by_date(date: str):
    """
    Get diary entry for a specific date
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        entry = diary_service.get_entry_by_date(date)
        
        if not entry:
            raise HTTPException(status_code=404, detail=f"No entry found for date {date}")
        
        return entry_to_response(entry)
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diary/entries", response_model=List[DiaryEntryResponse])
async def get_all_entries(limit: int = 50, offset: int = 0):
    """
    Get all diary entries with pagination
    """
    try:
        entries = diary_service.get_all_entries(limit=limit, offset=offset)
        return [entry_to_response(entry) for entry in entries]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diary/search", response_model=DiarySearchResponse)
async def search_entries(q: str):
    """
    Search diary entries by content or tags
    """
    try:
        results = diary_service.search_entries(q)
        return DiarySearchResponse(
            results=[entry_to_response(entry) for entry in results],
            count=len(results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/diary/entry/{date}")
async def delete_entry(date: str):
    """
    Delete diary entry for a specific date
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        success = diary_service.delete_entry(date)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"No entry found for date {date}")
        
        return {"message": f"Entry for {date} deleted successfully", "success": True}
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diary/stats", response_model=DiaryStatsResponse)
async def get_diary_stats():
    """
    Get storage statistics for diary
    """
    try:
        stats = diary_service.get_storage_stats()
        return DiaryStatsResponse(**stats)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diary/summary/{date}")
async def get_entry_summary(date: str):
    """
    Get summary statistics for a specific entry
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        summary = diary_service.get_entry_summary(date)
        
        if not summary['exists']:
            raise HTTPException(status_code=404, detail=f"No entry found for date {date}")
        
        return summary
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))