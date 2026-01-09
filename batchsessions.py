from fastapi import APIRouter, HTTPException, status
from typing import List
from model.batchsessionmodel import BatchSession, BatchSessionCreate, BatchSessionUpdate
from services.batchsessioncrud import BatchSessionCRUD

router = APIRouter(prefix="/batchsessions", tags=["batchsessions"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_batch_session(session: BatchSessionCreate):
    """
    Create a new batch session.
    
    - **batch_id**: Batch ID (required)
    - **session_date**: Session date (required)
    - **start_time**: Start time (required)
    - **end_time**: End time (required)
    - **status**: Session status (required)
    - **notes**: Session notes (optional)
    """
    try:
        result = BatchSessionCRUD.create_batch_session(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/batch/{batch_id}", response_model=List[BatchSession])
async def get_sessions_by_batch(batch_id: int):
    """
    Retrieve all sessions for a specific batch.
    """
    try:
        sessions = BatchSessionCRUD.get_sessions_by_batch(batch_id)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[BatchSession])
async def get_all_batch_sessions():
    """
    Retrieve all batch sessions.
    """
    try:
        batch_sessions = BatchSessionCRUD.get_all_batch_sessions()
        return batch_sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}", response_model=BatchSession)
async def get_batch_session(session_id: int):
    """
    Retrieve a single batch session by ID.
    """
    try:
        batch_session = BatchSessionCRUD.get_batch_session(session_id)
        if not batch_session:
            raise HTTPException(status_code=404, detail="Batch session not found")
        return batch_session
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{session_id}", response_model=dict)
async def update_batch_session(session_id: int, session: BatchSessionUpdate):
    """
    Update an existing batch session.
    
    - **session_id**: Session ID (required in URL)
    - All other fields are optional
    """
    try:
        result = BatchSessionCRUD.update_batch_session(session_id, session)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{session_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_batch_session(session_id: int):
    """
    Delete a batch session by ID.
    """
    try:
        result = BatchSessionCRUD.delete_batch_session(session_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
