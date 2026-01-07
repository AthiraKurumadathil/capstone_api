from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.activitymodel import Activity, ActivityCreate, ActivityUpdate
from services.activitycrud import ActivityCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/activities", tags=["activities"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_activity(activity: ActivityCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new activity.
    
    - **org_id**: Organization ID (required)
    - **name**: Activity name (required)
    - **category_id**: Category ID (required)
    - **description**: Activity description (optional)
    - **default_fee**: Default fee amount (optional)
    - **active**: Active status (default: true)
    """
    try:
        result = ActivityCRUD.create_activity(activity)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/{activity_id}", response_model=Activity)
async def get_activity(activity_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single activity by ID.
    """
    try:
        activity = ActivityCRUD.get_activity(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Activity])
async def get_all_activities(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all activities.
    """
    try:
        activities = ActivityCRUD.get_all_activities()
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/organization/{org_id}", response_model=List[Activity])
async def get_activities_by_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all activities for a specific organization.
    """
    try:
        activities = ActivityCRUD.get_activities_by_org(org_id)
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{activity_id}", response_model=dict)
async def update_activity(activity_id: int, activity: ActivityUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing activity.
    
    - **activity_id**: Activity ID (required in URL)
    - All other fields are optional
    """
    try:
        result = ActivityCRUD.update_activity(activity_id, activity)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{activity_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_activity(activity_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete an activity by ID.
    """
    try:
        result = ActivityCRUD.delete_activity(activity_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
