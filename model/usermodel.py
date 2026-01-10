from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    org_id: int
    role_id: int
    email: str = Field(..., min_length=1, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    active: bool

class UserCreate(UserBase):
    """
    Create a new user.
    Note: password_hash is NOT required - a random password will be auto-generated,
    hashed with SHA256, and sent to the user's email.
    """
    password_hash: Optional[str] = Field(None, max_length=500)

class UserUpdate(BaseModel):
    org_id: Optional[int] = None
    role_id: Optional[int] = None
    email: Optional[str] = Field(None, min_length=1, max_length=150)
    phone: Optional[str] = Field(None, max_length=20)
    password_hash: Optional[str] = Field(None, max_length=500)
    active: Optional[bool] = None

class User(UserBase):
    user_id: int
    created_at: datetime
    last_login_at: Optional[datetime] = None
    class Config:
        from_attributes = True
