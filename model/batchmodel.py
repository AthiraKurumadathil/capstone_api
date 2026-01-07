from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BatchBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    activity_id: int = Field(..., description="Activity ID")
    fee_plan_id: int = Field(..., description="Fee Plan ID")
    name: str = Field(..., min_length=1, max_length=100, description="Batch name")
    start_date: date = Field(..., description="Start date")
    end_date: Optional[date] = Field(None, description="End date")
    capacity: Optional[int] = Field(None, description="Batch capacity")
    location: Optional[str] = Field(None, max_length=150, description="Location")
    status: str = Field(..., min_length=1, max_length=30, description="Batch status")

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    org_id: Optional[int] = None
    activity_id: Optional[int] = None
    fee_plan_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    capacity: Optional[int] = None
    location: Optional[str] = Field(None, max_length=150)
    status: Optional[str] = Field(None, min_length=1, max_length=30)

class Batch(BatchBase):
    batch_id: int

    class Config:
        from_attributes = True
