from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AttendanceBase(BaseModel):
    session_id: int = Field(..., description="Session ID")
    enrollment_id: int = Field(..., description="Enrollment ID")
    status: str = Field(..., min_length=1, max_length=20, description="Attendance status")
    marked_at: datetime = Field(..., description="Marked timestamp")
    marked_by: Optional[int] = Field(None, description="User ID who marked attendance")

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    session_id: Optional[int] = None
    enrollment_id: Optional[int] = None
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    marked_at: Optional[datetime] = None
    marked_by: Optional[int] = None

class Attendance(AttendanceBase):
    attendance_id: int
    session_name: Optional[str] = Field(None, description="Session name (from BatchSessions)")

    class Config:
        from_attributes = True

