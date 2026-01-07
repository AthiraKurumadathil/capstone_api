from fastapi import APIRouter, HTTPException, status
from typing import List
from model.batchmodel import Batch, BatchCreate, BatchUpdate
from services.batchcrud import BatchCRUD

router = APIRouter(prefix="/batches", tags=["batches"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_batch(batch: BatchCreate):
    """
    Create a new batch.
    
    - **org_id**: Organization ID (required)
    - **activity_id**: Activity ID (required)
    - **fee_plan_id**: Fee Plan ID (required)
    - **name**: Batch name (required)
    - **start_date**: Start date (required)
    - **end_date**: End date (optional)
    - **capacity**: Batch capacity (optional)
    - **location**: Location (optional)
    - **status**: Batch status (required)
    """
    try:
        result = BatchCRUD.create_batch(batch)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[Batch])
async def get_batches_by_organization(org_id: int):
    """
    Retrieve all batches for a specific organization.
    """
    try:
        batches = BatchCRUD.get_batches_by_org(org_id)
        return batches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/activity/{activity_id}", response_model=List[Batch])
async def get_batches_by_activity(activity_id: int):
    """
    Retrieve all batches for a specific activity.
    """
    try:
        batches = BatchCRUD.get_batches_by_activity(activity_id)
        return batches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Batch])
async def get_all_batches():
    """
    Retrieve all batches.
    """
    try:
        batches = BatchCRUD.get_all_batches()
        return batches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{batch_id}", response_model=Batch)
async def get_batch(batch_id: int):
    """
    Retrieve a single batch by ID.
    """
    try:
        batch = BatchCRUD.get_batch(batch_id)
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")
        return batch
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{batch_id}", response_model=dict)
async def update_batch(batch_id: int, batch: BatchUpdate):
    """
    Update an existing batch.
    
    - **batch_id**: Batch ID (required in URL)
    - All other fields are optional
    """
    try:
        result = BatchCRUD.update_batch(batch_id, batch)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{batch_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_batch(batch_id: int):
    """
    Delete a batch by ID.
    """
    try:
        result = BatchCRUD.delete_batch(batch_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
