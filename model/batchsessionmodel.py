from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

class BatchSessionBase(BaseModel):
    batch_id: int = Field(..., description="Batch ID")
    session_name: str = Field(..., min_length=1, max_length=100, description="Session name")
    session_date: date = Field(..., description="Session date")
    start_time: time = Field(..., description="Session start time")
    end_time: time = Field(..., description="Session end time")
    status: str = Field(..., min_length=1, max_length=30, description="Session status")
    notes: Optional[str] = Field(None, max_length=500, description="Session notes")

class BatchSessionCreate(BatchSessionBase):
    pass

class BatchSessionUpdate(BaseModel):
    batch_id: Optional[int] = None
    session_name: Optional[str] = Field(None, min_length=1, max_length=100)
    session_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = Field(None, min_length=1, max_length=30)
    notes: Optional[str] = Field(None, max_length=500)

class BatchSession(BatchSessionBase):
    session_id: int

    class Config:
        from_attributes = True
