from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ActivityBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    name: str = Field(..., min_length=1, max_length=255, description="Activity name")
    category_id: int = Field(..., description="Category ID")
    description: Optional[str] = Field(None, description="Activity description")
    default_fee: Optional[float] = Field(None, description="Default fee")
    active: Optional[bool] = Field(True, description="Active status")

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    org_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category_id: Optional[int] = None
    description: Optional[str] = None
    default_fee: Optional[float] = None
    active: Optional[bool] = None

class Activity(ActivityBase):
    activity_id: int
    #created_date: datetime

    class Config:
        from_attributes = True
