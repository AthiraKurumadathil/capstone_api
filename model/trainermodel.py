from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TrainerBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    email: Optional[str] = Field(None, max_length=150, description="Email address")
    hire_date: Optional[date] = Field(None, description="Hire date")
    active: Optional[bool] = Field(True, description="Active status")

class TrainerCreate(TrainerBase):
    pass

class TrainerUpdate(BaseModel):
    org_id: Optional[int] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=150)
    hire_date: Optional[date] = None
    active: Optional[bool] = None

class Trainer(TrainerBase):
    trainer_id: int

    class Config:
        from_attributes = True
