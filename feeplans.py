from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.feeplanmodel import FeePlan, FeePlanCreate, FeePlanUpdate
from services.feeplancrud import FeePlanCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/feeplans", tags=["feeplans"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_fee_plan(fee_plan: FeePlanCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new fee plan.
    
    - **org_id**: Organization ID (required)
    - **name**: Fee plan name (required)
    - **billing_type**: Billing type (required)
    - **amount**: Fee amount (required)
    - **currency**: Currency code (3 chars, required)
    - **active**: Active status (default: true)
    """
    try:
        result = FeePlanCRUD.create_fee_plan(fee_plan)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[FeePlan])
async def get_fee_plans_by_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all fee plans for a specific organization.
    """
    try:
        fee_plans = FeePlanCRUD.get_fee_plans_by_org(org_id)
        return fee_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[FeePlan])
async def get_all_fee_plans(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all fee plans.
    """
    try:
        fee_plans = FeePlanCRUD.get_all_fee_plans()
        return fee_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{fee_plan_id}", response_model=FeePlan)
async def get_fee_plan(fee_plan_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single fee plan by ID.
    """
    try:
        fee_plan = FeePlanCRUD.get_fee_plan(fee_plan_id)
        if not fee_plan:
            raise HTTPException(status_code=404, detail="Fee plan not found")
        return fee_plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{fee_plan_id}", response_model=dict)
async def update_fee_plan(fee_plan_id: int, fee_plan: FeePlanUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing fee plan.
    
    - **fee_plan_id**: Fee Plan ID (required in URL)
    - All other fields are optional
    """
    try:
        result = FeePlanCRUD.update_fee_plan(fee_plan_id, fee_plan)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{fee_plan_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_fee_plan(fee_plan_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete a fee plan by ID.
    """
    try:
        result = FeePlanCRUD.delete_fee_plan(fee_plan_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
