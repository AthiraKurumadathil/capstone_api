from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EnrollmentBase(BaseModel):
    org_id: int = Field(..., description="Organization ID")
    batch_id: int = Field(..., description="Batch ID")
    student_id: int = Field(..., description="Student ID")
    enrolled_on: date = Field(..., description="Enrollment date")
    status: str = Field(..., min_length=1, max_length=30, description="Enrollment status")

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    org_id: Optional[int] = None
    batch_id: Optional[int] = None
    student_id: Optional[int] = None
    enrolled_on: Optional[date] = None
    status: Optional[str] = Field(None, min_length=1, max_length=30)

class Enrollment(EnrollmentBase):
    enrollment_id: int

    class Config:
        from_attributes = True
