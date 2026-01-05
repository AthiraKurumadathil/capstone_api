from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Organization name")
    address: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: Optional[str] = Field(None, max_length=100, description="City name")
    zip: Optional[str] = Field(None, max_length=20, description="Zip code")
    state: Optional[str] = Field(None, max_length=50, description="State name")
    phone: str = Field(..., min_length=1, max_length=255, description="Phone number")
    email: str = Field(..., description="Email address")
    active: Optional[bool] = Field(True, description="Active status")

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    zip: Optional[str] = Field(None, max_length=20)
    state: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = None
    active: Optional[bool] = None

class Organization(OrganizationBase):
    org_id: int
    created_date: datetime

    class Config:
        from_attributes = True
