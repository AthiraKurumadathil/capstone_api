from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class StudentBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    dob: Optional[date] = Field(None, description="Date of birth")
    guardian_name: Optional[str] = Field(None, max_length=150, description="Guardian name")
    guardian_phone: Optional[str] = Field(None, max_length=20, description="Guardian phone")
    guardian_email: Optional[str] = Field(None, max_length=150, description="Guardian email")
    notes: Optional[str] = Field(None, description="Additional notes")
    active: Optional[bool] = Field(True, description="Active status")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    org_id: Optional[int] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    dob: Optional[date] = None
    guardian_name: Optional[str] = Field(None, max_length=150)
    guardian_phone: Optional[str] = Field(None, max_length=20)
    guardian_email: Optional[str] = Field(None, max_length=150)
    notes: Optional[str] = None
    active: Optional[bool] = None

class Student(StudentBase):
    student_id: int
    created_at: datetime

    class Config:
        from_attributes = True
