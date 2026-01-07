from pydantic import BaseModel, Field
from typing import Optional

class ActivityTrainerBase(BaseModel):
    activity_id: int = Field(..., description="Activity ID")
    trainer_id: int = Field(..., description="Trainer ID")
    role: Optional[str] = Field(None, description="Role of trainer for this activity")

class ActivityTrainerCreate(ActivityTrainerBase):
    pass

class ActivityTrainerUpdate(BaseModel):
    role: Optional[str] = Field(None, max_length=20)

class ActivityTrainer(ActivityTrainerBase):
    class Config:
        from_attributes = True
