from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from model.categorymodel import Category, CategoryCreate, CategoryUpdate
from services.categorycrud import CategoryCRUD
from utils.auth import verify_jwt_token

router = APIRouter(prefix="/categories", tags=["categories"])

# ============== CREATE ENDPOINT ==============
@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, current_user: dict = Depends(verify_jwt_token)):
    """
    Create a new category.
    
    - **name**: Category name (required)
    - **active**: Active status (default: true)
    """
    try:
        result = CategoryCRUD.create_category(category)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============== GET ENDPOINTS ==============
@router.get("", response_model=List[Category])
async def get_all_categories(current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve all categories.
    """
    try:
        categories = CategoryCRUD.get_all_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Retrieve a single category by ID.
    """
    try:
        category = CategoryCRUD.get_category(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== UPDATE ENDPOINT ==============
@router.put("/{category_id}", response_model=dict)
async def update_category(category_id: int, category: CategoryUpdate, current_user: dict = Depends(verify_jwt_token)):
    """
    Update an existing category.
    
    - **category_id**: Category ID (required in URL)
    - All other fields are optional
    """
    try:
        result = CategoryCRUD.update_category(category_id, category)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))

# ============== DELETE ENDPOINT ==============
@router.delete("/{category_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, current_user: dict = Depends(verify_jwt_token)):
    """
    Delete a category by ID.
    """
    try:
        result = CategoryCRUD.delete_category(category_id)
        return result
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
