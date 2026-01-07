from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.activitytrainermodel import ActivityTrainer, ActivityTrainerCreate, ActivityTrainerUpdate
from services.activitytrainercrud import ActivityTrainerCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/activitytrainers", tags=["activitytrainers"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=ActivityTrainer, status_code=status.HTTP_201_CREATED)
async def create_activity_trainer(activity_trainer: ActivityTrainerCreate):
    """
    Create a new activity-trainer relationship.
    
    - **activity_id**: Activity ID (required)
    - **trainer_id**: Trainer ID (required)
    - **role**: Trainer role for this activity (optional)
    """
    try:
        result = ActivityTrainerCRUD.create_activity_trainer(activity_trainer)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
# Note: Specific routes must be defined before generic parameterized routes
@router.get("/activity/{activity_id}", response_model=List[ActivityTrainer])
async def get_trainers_by_activity(activity_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all trainers assigned to a specific activity.
    """
    try:
        trainers = ActivityTrainerCRUD.get_trainers_by_activity(activity_id)
        return trainers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trainer/{trainer_id}", response_model=List[ActivityTrainer])
async def get_activities_by_trainer(trainer_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all activities assigned to a specific trainer.
    """
    try:
        activities = ActivityTrainerCRUD.get_activities_by_trainer(trainer_id)
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[ActivityTrainer])
async def get_all_activity_trainers(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all activity-trainer relationships.
    """
    try:
        activity_trainers = ActivityTrainerCRUD.get_all_activity_trainers()
        return activity_trainers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{activity_id}/{trainer_id}", response_model=ActivityTrainer)
async def get_activity_trainer(activity_id: int, trainer_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a specific activity-trainer relationship.
    """
    try:
        activity_trainer = ActivityTrainerCRUD.get_activity_trainer(activity_id, trainer_id)
        if not activity_trainer:
            raise HTTPException(status_code=404, detail="Activity trainer relationship not found")
        return activity_trainer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{activity_id}/{trainer_id}", response_model=dict)
async def update_activity_trainer(activity_id: int, trainer_id: int, activity_trainer: ActivityTrainerUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing activity-trainer relationship.
    
    - **activity_id**: Activity ID (required in URL)
    - **trainer_id**: Trainer ID (required in URL)
    - **role**: Trainer role (optional)
    """
    try:
        result = ActivityTrainerCRUD.update_activity_trainer(activity_id, trainer_id, activity_trainer)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{activity_id}/{trainer_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_activity_trainer(activity_id: int, trainer_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete an activity-trainer relationship.
    """
    try:
        result = ActivityTrainerCRUD.delete_activity_trainer(activity_id, trainer_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
