from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.orgmodel import Organization, OrganizationCreate, OrganizationUpdate
from services.orgcrud import OrganizationCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/organizations", tags=["organizations"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_organization(org: OrganizationCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new organization. Requires JWT authentication.
    
    - **name**: Organization name (required)
    - **address**: Street address (required)
    - **city**: City (optional)
    - **zip**: Zip code (optional)
    - **state**: State (optional)
    - **phone**: Phone number (required)
    - **email**: Email address (required)
    - **active**: Active status (default: true)
    """
    try:
        result = OrganizationCRUD.create_organization(org)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/{org_id}", response_model=Organization)
async def get_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single organization by ID. Requires JWT authentication.
    """
    try:
        org = OrganizationCRUD.get_organization(org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return org
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Organization])
async def get_all_organizations(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all organizations. Requires JWT authentication.
    """
    try:
        orgs = OrganizationCRUD.get_all_organizations()
        return orgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{org_id}", response_model=Organization)
async def update_organization(org_id: int, org: OrganizationUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing organization. Only provided fields will be updated. Requires JWT authentication.
    """
    try:
        updated_org = OrganizationCRUD.update_organization(org_id, org)
        if not updated_org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return updated_org
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete an organization by ID. Requires JWT authentication.
    """
    try:
        success = OrganizationCRUD.delete_organization(org_id)
        if not success:
            raise HTTPException(status_code=404, detail="Organization not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
