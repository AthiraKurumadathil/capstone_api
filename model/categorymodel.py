from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    active: Optional[bool] = Field(True, description="Active status")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    active: Optional[bool] = None

class Category(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True
