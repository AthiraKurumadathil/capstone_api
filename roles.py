from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.rolemodel import Role, RoleCreate, RoleUpdate
from services.rolecrud import RoleCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/roles", tags=["roles"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new role.
    
    - **org_id**: Organization ID (required)
    - **name**: Role name (required)
    """
    try:
        result = RoleCRUD.create_role(role)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("/organization/{org_id}", response_model=List[Role])
async def get_roles_by_organization(org_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all roles for a specific organization.
    """
    try:
        roles = RoleCRUD.get_roles_by_org(org_id)
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[Role])
async def get_all_roles(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all roles.
    """
    try:
        roles = RoleCRUD.get_all_roles()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{role_id}", response_model=Role)
async def get_role(role_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single role by ID.
    """
    try:
        role = RoleCRUD.get_role(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{role_id}", response_model=dict)
async def update_role(role_id: int, role: RoleUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing role.
    
    - **role_id**: Role ID (required in URL)
    - All other fields are optional
    """
    try:
        result = RoleCRUD.update_role(role_id, role)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{role_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_role(role_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete a role by ID.
    """
    try:
        result = RoleCRUD.delete_role(role_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
