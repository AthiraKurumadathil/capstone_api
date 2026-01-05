from fastapi import APIRouter, HTTPException, status
from typing import List
from model.orgmodel import Organization, OrganizationCreate, OrganizationUpdate
from services.orgcrud import OrganizationCRUD

router = APIRouter(prefix="/organizations", tags=["organizations"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_organization(org: OrganizationCreate):
    """
    Create a new organization.
    
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
async def get_organization(org_id: int):
    """
    Retrieve a single organization by ID.
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
async def get_all_organizations():
    """
    Retrieve all organizations.
    """
    try:
        orgs = OrganizationCRUD.get_all_organizations()
        return orgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{org_id}", response_model=Organization)
async def update_organization(org_id: int, org: OrganizationUpdate):
    """
    Update an existing organization. Only provided fields will be updated.
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
async def delete_organization(org_id: int):
    """
    Delete an organization by ID.
    """
    try:
        success = OrganizationCRUD.delete_organization(org_id)
        if not success:
            raise HTTPException(status_code=404, detail="Organization not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
