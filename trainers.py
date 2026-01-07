from fastapi import APIRouter, HTTPException, status
from typing import List
from model.trainermodel import Trainer, TrainerCreate, TrainerUpdate
from services.trainercrud import TrainerCRUD

router = APIRouter(prefix="/trainers", tags=["trainers"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_trainer(trainer: TrainerCreate):
    """
    Create a new trainer.
    
    - **org_id**: Organization ID (required)
    - **first_name**: First name (required)
    - **last_name**: Last name (required)
    - **phone**: Phone number (optional)
    - **email**: Email address (optional)
    - **hire_date**: Hire date (optional)
    - **active**: Active status (default: true)
    """
    try:
        result = TrainerCRUD.create_trainer(trainer)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/{trainer_id}", response_model=Trainer)
async def get_trainer(trainer_id: int):
    """
    Retrieve a single trainer by ID.
    """
    try:
        trainer = TrainerCRUD.get_trainer(trainer_id)
        if not trainer:
            raise HTTPException(status_code=404, detail="Trainer not found")
        return trainer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Trainer])
async def get_all_trainers():
    """
    Retrieve all trainers.
    """
    try:
        trainers = TrainerCRUD.get_all_trainers()
        return trainers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/organization/{org_id}", response_model=List[Trainer])
async def get_trainers_by_organization(org_id: int):
    """
    Retrieve all trainers for a specific organization.
    """
    try:
        trainers = TrainerCRUD.get_trainers_by_org(org_id)
        return trainers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{trainer_id}", response_model=dict)
async def update_trainer(trainer_id: int, trainer: TrainerUpdate):
    """
    Update an existing trainer.
    
    - **trainer_id**: Trainer ID (required in URL)
    - All other fields are optional
    """
    try:
        result = TrainerCRUD.update_trainer(trainer_id, trainer)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{trainer_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_trainer(trainer_id: int):
    """
    Delete a trainer by ID.
    """
    try:
        result = TrainerCRUD.delete_trainer(trainer_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
